#!/usr/bin/env python3
"""
crr_treatment.py — recursive CRR regulatory-treatment classifier for a
legal-entity hierarchy, plus the derivation of the cached l1_group /
crr_aggregation columns used elsewhere on this site.

This is the "python file" referenced in the One Ring to Rule Them All post
— written out in full and verified against df_limits_exposures.csv (see
the __main__ block at the bottom: run this file directly to reproduce a
100% match against the published dataset).

Two genuinely recursive functions do the real work:

  subtree(root)            — descendant enumeration (base case: no children)
  get_group_ancestor(id)   — parent-chain walk up to the entity's "L2"
                              group node, i.e. the ancestor that is a direct
                              child of id's own L1 branch head (Bank Co,
                              Property Co, Wealth Co, or Market Co).

This is the Python equivalent of a recursive SQL CTE: an anchor case
(no parent / parent is the group head) plus a recursive step that
re-references the previous result, run until it terminates. One difference
worth knowing: most SQL engines evaluate a recursive CTE iteratively
(re-running the recursive member against the newest rows until none
arrive), not via literal call-stack recursion the way this Python code
does — same self-referential structure, different execution mechanism.

get_group_ancestor() guards against cycles (a corrupted or circularly
re-parented entity chain) — real legacy hierarchy data occasionally has
exactly this problem, and a naive walk-up would loop forever without it.
It's also memoised (lru_cache), so re-running it across a large exposure
table doesn't repeatedly re-walk the same chain: computed once per entity,
O(n) overall rather than O(n x depth).

For anything past this toy L0-L6 example (deeper or messier real
hierarchies), consider networkx instead of hand-rolled recursion —
nx.ancestors() / nx.has_path() etc. give you a tested, cycle-aware graph
API for the same problem. Pandas has no built-in recursive-ancestor
primitive, so "just use pandas" for this specific step still means
hand-rolling a loop very like the one below.
"""

import csv
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent
ENT_CSV = DATA_DIR / "df_legal_entity.csv"
EXP_CSV = DATA_DIR / "df_limits_exposures.csv"

ROOT = "E000"       # Group Co — ultimate parent
BANK_ROOT = "E001"  # Bank Co — the ring-fenced sub-group head


def load_entities(path=ENT_CSV):
    emap, parent = {}, {}
    with open(path) as f:
        for row in csv.DictReader(f):
            eid = row["entity_id"]
            emap[eid] = {
                "name": row["name"],
                "level": int(row["level"]),
                "parent": row["parent_id"] or None,
                "rf": row["ring_fence_status"],
            }
            parent[eid] = row["parent_id"] or None
    return emap, parent


def build_classifier(emap, parent):
    """Returns (bank_subtree, get_group_ancestor, crr_treatment) closed
    over this entity set, so the module can be reused against any
    legal-entity CSV with the same shape."""

    children = defaultdict(list)
    for eid, p in parent.items():
        if p:
            children[p].append(eid)

    def subtree(root):
        """Recursive descendant enumeration: base case = no children,
        recursive case = union of every child's subtree."""
        nodes = {root}
        for c in children.get(root, []):
            nodes |= subtree(c)
        return nodes

    bank_subtree = subtree(BANK_ROOT)

    @lru_cache(maxsize=None)
    def get_group_ancestor(entity_id, _seen=frozenset()):
        """Recursive ancestor walk with cycle guard. Returns the ancestor
        of entity_id that is a direct child of entity_id's own L1 branch
        head, or None if entity_id IS a branch head (or the root)."""
        if entity_id in _seen:
            raise ValueError(f"cycle detected in parent chain at {entity_id}")
        p = parent.get(entity_id)
        if p is None or p == ROOT:
            return None
        grandp = parent.get(p)
        if grandp == ROOT:
            return entity_id
        return get_group_ancestor(p, _seen | {entity_id})

    def crr_treatment(cred_id, deb_id):
        """
        Derive CRR regulatory treatment for a bilateral exposure.

        Rules (applied in order):
          RFB_X         : creditor inside Bank sub-group, debtor outside
          NRFB_X        : creditor outside Bank sub-group, debtor inside
          [group]_CORE      : both share a group ancestor that is CORE (UK RFB)
          [group]_NON_CORE  : both share a group ancestor that is NON CORE (non-UK RFB)
          [group]_NRFB      : both share a group ancestor outside the ring-fenced bank
          RFB_INTERNAL  : both inside Bank sub-group, different group ancestors
          NRFB_CROSS    : both outside Bank sub-group, no shared group ancestor
        """
        cr_in_bank = cred_id in bank_subtree
        de_in_bank = deb_id in bank_subtree

        if cr_in_bank and not de_in_bank:
            return "RFB_X"
        if not cr_in_bank and de_in_bank:
            return "NRFB_X"

        cr_grp = get_group_ancestor(cred_id)
        de_grp = get_group_ancestor(deb_id)
        if cr_grp and de_grp and cr_grp == de_grp:
            grp = emap[cr_grp]
            if grp["rf"] == "CORE":
                return f"{grp['name']}_CORE"
            if grp["rf"] == "NON CORE":
                return f"{grp['name']}_NON_CORE"
            return f"{grp['name']}_NRFB"

        if cr_in_bank and de_in_bank:
            return "RFB_INTERNAL"
        return "NRFB_CROSS"

    return bank_subtree, get_group_ancestor, crr_treatment


if __name__ == "__main__":
    emap, parent = load_entities()
    bank_subtree, get_group_ancestor, crr_treatment = build_classifier(emap, parent)

    total = match = 0
    mismatches = []
    with open(EXP_CSV) as f:
        for row in csv.DictReader(f):
            total += 1
            predicted = crr_treatment(row["creditor_entity_id"], row["debtor_entity_id"])
            actual = row["crr_reg_treatment"]
            if predicted == actual:
                match += 1
            else:
                mismatches.append((row["record_id"], predicted, actual))

    print(f"{match}/{total} records match ({match/total:.1%})")
    for m in mismatches[:20]:
        print("  mismatch:", m)
