---
title: "One Ring to Rule them All...."
date: 2026-03-21T22:07:39Z
draft: false
categories: ["credit-risk"]
tags: []
description: "Mapping CRR exposures against legal entity hierarchy from legacy systems. A dynamic overlay approach to maintain full data integrity"
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## The Problem

This is a combined overview of credit, entity relationships, object oriented data sciences, all aligned to regulatory objectives. All items included are made up and functional, with the broad structure reflecting actual real world problems. The relevant bits of code will be provided, but this is about understanding the problem, defining the problem statement (properly), and learning the wrong ways so you don’t make mistakes.

### Assumptions
Available systems are probably limited in scope, are circa 1990’s, and are designed around single instances.
This means we will need to resolve the trickier aspects outside of limited core systems.
* Assume corporate structure featuring level 0 through level 6.
* Each corporate thing is an entity. It must have a unique data identifier.
* Level 0 is the parent company.
* Level 1 is a subsidiary of level 0, and so on.
* A level 1 must have a data field or edge that joins it to the level 0.
* This is the same concept for a level 2 that is connected to a level 1
* Each entity needs a domicile attribute, being country.
* * Each entity needs an address.
* Each entity needs a city, to be defined by the address.

Now a primer on what is going on here, why its a genuine problem, and shock horror, some data science. If you know me, you will have heard this lecture a few times now, so apologies dear readers who have suffered this lecture previously. Read the book, refer book review for **Alien Phenomenology What It Means to Be a Thing** especially if you are new to networks, or the concept of object oriented programming and data. We are also going to cover the basis of statistics, and stratification. Bad luck if you don’t want to.

### The Wrong Way

Back to the basics. Imagine you have two friends, Bob and Jane. Bob and Jane live somewhere. You are tasked with crating some kind of relational system, why is irrelevant for now. After some thought, you decide to assemble the relational system, which later we will correctly call a network. Without much effort, you construct your system of an entity for Bob, and Entity for Jane, and to cover off where they live an Address for Bob and Jane, and an entity for their house, bob_house and jane_house. From this you create your basic network and off you go. Now there is a presumption of scale here, our example of two is implied to reflect the reality of thousands. Scale matters as we will so, so get your design right.

IRL shall mean In Real Life for the rest of this post, and the rest of the site. This means the realistic parts of life that cannot be assumed away. In general you will have oversimplified something, removing elements that are essential but inconveniently complex, and as a result your system is crap and stops working as intended.

All is well, you are happy. Then sometime later, Bob goes and moves, and your data goes to crap. Because you didn’t do it properly. The entity bob_house no longer applies, as Bob has gone and moved. So you delete it and create a new one bob2_house. Now you lose chunks of your network, and downstream history and data for bob_house. Because you screwed up.

### The Right Way

IRL there is one, and only one instance of you. Even if you are a biological identical twin, genes and environment will have forged you in to a genetically identical, but biologically tweaked version of you. So the sample size of ‘you’ defined by all possible attributes is n=1.

So there is one of you.

This leads to a couple of immediate questions. Who are you? As in how, in data are we going to adequately define you. Stated properly this is ‘how are you to be adequately defined using a combination of observable and deducible attributes?’. The presumption here is that you know the end use of your system. There is a lot of thinking required to get the problem statement correct here, as there will be inherent conflicts in all of these choices. For our purposes, a key requirement is going to be driven by KYC legislation, or Know Your Client. Over simplified, this means there can only be one instance of you, or as we move forward, the relevant legal entity.

>  A lot of the jokes play on the obviously quite problematic idea in Roman times of knowing who you are. Another "identity" joke sees a man meet an acquaintance and say "it's funny, I was told you were dead". He says "well, you can see I'm still alive." But the first man disputes this on the grounds that "the man who told me you were dead is much more reliable than you”. — Classicist Mary Beard,  *Laughter in Ancient Rome: On Joking, Tickling, and Cracking Up (Sather Classical Lectures): 71*


Who knew the Roman’s were into data science?

Now, if you have ever suffered the experience of dealing with any government department of immigration (and suffering is the precise word to use), you will have deep experience of understanding that it does not matter that you know who ‘you’ are, ALL that matters is what the system thinks ‘you’ are. This is why the joke above resonates so much in the modern world. The presumed ‘reliable’ source of information is the ‘system’. No government employee is empowered to use sanity, logic or reasonableness. If the ‘system’ version of you is wrong, you are screwed.

### One Ring to Rule them All

Romans to Tolkien, quite the journey. Back to data science soon. Promise. This is concept of super ordinance at play, and how choosing your path to it is rather important. Seriously read the book. 

> superordinate (or hypernym) is a general, umbrella term that encompasses the meanings of more specific words, known as hyponyms. It acts as a higher-level category in hierarchical relationships (e.g., "bird" is the superordinate of "robin" or “pigeon”). Thanks AI…..

In statistics, when you have a multi dimensional population, stratification or classification models are a common approach to resolving the population into coherent sets for a particular purpose. If you have a population of say one thousand people, there are very many, but not infinite ways you can objectively classify them. Height, biological sex, pre and post puberty, colour, eye colour, etc, etc. There are potentially infinite ways to subjectively classify them. The strata or classes don’t really matter, what does matter is the that for each n in the population, it can belong in one and ONLY ONE classification. Lets go with a picture of flora, and we want to classify it into tree’s and bushes. For what ever reason. This requires you going down the rabbit hole and explicitly defining what is a tree, and what is a bush. Answer cannot be either or, not sure, or both. This usually requires you expanding your data fields until you get to an answer. One Ring to Rule them means a definitive classifier. Back to the problem, this means a superordinate way to classify for the purpose at hand. This means you might need more than one.

There are two ways of doing this, subjective, deciding and adding a yes no attribute for whatever the strata is. Or much better, you can derive that attribute from the data. So the subject element is laying the logic rules for class-action X, and then running the data through a classifier, and adding the new data field to the data.
If you study machine learning, you will be sick to death of this. And you will know a lot about pigeons and penguins. Go and do it. Source: 
https://huggingface.co/SIH/penguin-classifier-sklearn



A Primer on Ring Fencing concepts is appended if you have not crossed paths with this. Its sort of essential for this piece of work.

So, ‘you’ means just you. Great. How many instances of you are there in the world? Biologically, one. If you have a bank account, then there is one KYC for you in every bank you deal with. There is one of you for whatever memberships you have. Leases, property titles, streaming services, library card, etc, etc. IRL there are possibly thousands of instances of ‘you’ in hundreds and hundreds of systems. Not all will be correct. So we are at many instances of classifiers where ‘you’ needs to be just you. This is a classic many to many entity relationship problem. Thankfully there are ways of dealing with this. Intelligently.

> Warning: There is no magic system solution. You are going to have to DIY it to do it properly. And very likely outside of whatever crap core system you use for you job. Layered solution is probably the only way forward. This means you need a brain, you need a back end to your core system data, and you need the ability to run code on something, on a server, outside of said core system. Easy on a desktop if you are a decent programmer, and have some basic tools. Come back in five years if you need a robust enterprise wide system solution. Oh, and get approval for a lot of money. That no one senior who is not a programmer will ever want to give you. Consider giving up now is my advice. Or write a blog about it.

Based on the above nonsense, you should get the broad idea now. A bit more philosophy, then into the doing it part.

Bogost argues that everything that exists—humans, animals, machines, objects—has its own way of being, and we should try to take those non-human perspectives seriously. This approach is part of a broader philosophical movement called. Object-Oriented Ontology (OOO). That sounds a lot like object oriented programming, because it is a lot like that. So you don’t have 10,000 objects representing trees. You have a class of objects. Of which some are trees, and some are bushes.  The key mental part here is:

* In strict class hierarchies → they are different types
In flexible systems → they are different configurations 

To sort out this mess, we will need both of the above.

Bogost says we should be ‘Writing code that mimics how an object interacts with others’. Could not agree more, and we are about to do all of that. The context of which will be the interaction of legal entities within a banking structure, layering on the multi dimensional aspects of regulatory treatment. The end game is being able to compressive answer ‘what is the…..’ type questions across the legal entity and regulatory credit risk landscape. Which needs a network data landscape that one on is going to give you, that aligns with the regulatory landscape in ways no one who designed KYC systems ever bothered to think about. To be fair, they could have, but someone would have cheaped out and not wanted to pay for it back in the day. This is the problem of someone who does not know what they are doing being pushed into making a decision they shouldn’t make.

---
## The Problem Statement Restated

Before moving onto solution paths, its worth reallty digging into the gritty details of the problem. I want this to be crystal clear. The broad idea is superordinance. The specifics we are going to dig into is just where and what we should apply the concept to. The answer is not where you first think.

To strip things back to basics here is a simplified netwrok diagram of just 5 of the legal entities. For simplicity sake they have a notional 100 loan to each other.

![£100 loan network — 5 entities](/images/network_mini_loan.png)

Forgetting about code. Any exposure from Bank Co down to the non UK domiciled entity, for CRR has to be NON CORE.

> The legal entity is just that, there is no CRR treatment for just the one entity. It is the relationship between two entities, across a credit product, that drives CRR treatment.

This is why we want to leave legal entities as they are.

For the single loan it (lentity - exposure - entity) is NON CORE. That is fine. Now the Market Co lending to the Corp Co, that has to be a different CRR treatment. But wait, we have the Corp Co in NON CORE. But it cannot be that from the perspective of the Market Co. Conundrum! I know, I will create a new group name that is not a legal entity level. This will mirror Corp Co. So one instance of Corp Co for the NON CORE book of exposures, and then another instance of Corp Co for anthing that crosses the ring fence perimiter. I guess we can do that for each instance where we have a product from one legal entity to multiple other legal entities, some of which will map the exposure into different CRR buckets.

You can appreciate that in doing this you will:

* have a lot of duplications
* have lost the integrity of you legal entity structure
* run the risk of manual op errors in creating and linking the duplications
* probably go mad eventually wit the mess you have made....

---

So how best to avoid the traps laid out? Apply the concept of superordinance of course! But.... apply it to each exposure, **not** the legal entities.



---
## The Right Problem Statement

Or the less wrong one if you want. We want to be able to answer question about our portfolio, about the legal structure, and regulatory aspects, and exposures, and often all three at once. Therefor the correct problem statement is something like ‘what is the minimum data and attribute set that will permit investigation of the portfolio across the legal and regulatory landscape to fulfil regulatory report requirements together with portfolio management obligations’. Bit of a word salad, but you get the drift. To do the job, what do I need as the minimum viable data set. Of which other bits I can derive later.

CRR waiver letters, over simplified will list legal entities that extend exposure, and a list of all legal entities that said exposure can have the noted CRR waivers in the letter applied to. What they really are in intent is two fold; (i) they identify what the new rules shall apply to; and (ii) the afford permission to apply 'different' regulatory treatment where permitted. This is probably why they are actually titled Permission letters IRL. The what, in the case of the letter is the identified 'firm/s', or legal entities. From which exposures to any listed subsidiaries may receive the diminished CRR treatment. At no point do the letters tell you there cannot be other exposures, or how to go about applying the reduced CRR regulations.

**What the letter does not stipulate is that the legal entities may only have exposure to the listed entities. It says only the listed one's can benefit from the CRR waivers listed** In other words, the same legal entities at the top can, and probably do have many different exposures to other non listed legal entities. This is both necessary and expected for the group to function as whole. You just won't get the same CRR waiver or RWA adjustments. It is this critical aspect that tilts the logic of the solution away from treatment of the legal entity arrangement, to treatment of the exposures themselves. The path to the solution at this point should drive you away from static excel files of any kind.

As per bobs_house, the mistake is that you abuse your legal entity structure by switching a legal aggregation level at L1 out for a regulatory classifier. Eg make up a name inside_ring_fence, and presumable outside_ring_fence. Then hey presto you can slice your portfolio by ring fencing attribute! Done. No, actually.

You have taken a legal entity attribute, and swapped if for a regulatory alignment attribute. Your portfolio of things now uses one type, legal entity, for two different things. This will break things down the track. DO NOT DO THIS. Its just lazy, or a constraint applied my management that won’t work. You have given up the coherence of your entity data. Nothing good can come from this, even as you might be tempted for this quick fix.

## The doing

Enough nonsense, lets lay out a basic approach, using made up but realistic data set. And actually work through the problems. I am going to do this in python, but you can use whatever you like or have. At enterprise scale level it won’t be python, but you could probably set up a parallel reporting system that would work quite well.

As laid out above, we are going to establish a pretend bank, add some made up data, and then figure out a way to present the portfolio from BOTH a legal entity basis with no loss of coherence, as well as from a regulatory risk exposure perspective. Then, because we did not screw up the data, you can interrogate the portfolio however you like. Subsidiary to Group, Ring Fenced to Not Ring Fenced, trade or product level. Who cares, its up to you once you get the data stack right. Output is multidimensional portfolio query. Why???

You’re trying to:

> Optimise a portfolio under multiple dimensions of data, constraints, and uncertainty

The off the shelf IT system that will do this to your exact needs and data is; there isn’t ever one. Every constraint you add also breaks your existing approach. There is one more critical assumption that underpins this approach:

> Across the entire group, a decision made many years ago was that each functional business would share the same IT architecture. So for KYC, the same shared system operates across each sub group. Separate instances of systems, e.g. independent installation and data, are NOT implemented at each sub group level.

Hence the fix must be applied outside of the core system (whatever it is). Unless you are feeling brave and someone is going to let you fix the code base properly. Which would be fine, but good luck with getting that approved.

To start with we are going to adopt a fairly standard legal entity hierarchy, Level 0 of L0 is ultimate parent. Then on down to L6. That is sufficent for most structures as L6 and below can be flattened as required. This is all populated with made up entities and structures, but it is a rough proxy for what you get IRL. Its good enough for the purpose at hand, I don't want to burn the hours to re model an existing bank in all its glory. Yes, its ugly, but it is limited. IRL large domestic banks run to several hundred legal entities. The brings enough scale for later, when we add (pretend) products, limits and exposures:

![Legal entity structure](/images/legal_entity_structure.png)

In database problems, sometimes there is a unique ID challenge. Instead of renaming everything and fundamentally changing tables, you can create a unique ID by combining individual attributes in a unique fashion. For our pretend back, we are going to start with just the legal entity structure, and then we are going to add some deductive reasoning to be derive ways in which we can strata the data based on regulatory approach.

See data, files at bottom. Now I did the initial set up the hard way for a small sample structure, then used AI (Claude) to expand the data set to what you see in the python file. I am not lazy, but there are limits.

The basic model being adopted here is (i) Legal Entity data; (ii) Limit and Product Data; then (iii) Product and exposure data applied across the structure. We have preserved all original content from legacy system on legal entity. Then the important attributes, which boils down to RWA CRR treatment, will be derived and linked. The end game is a dynamic portfolio view that reflects all data, and reports as required for CRR reporting.

I know this seems a bit painful, there is a reason why. Approaching the problem this way means you can apply n rules, or change the rules, without destroying the data. So no deleting bobs_house when bob moves. If CRR rules change, fine. Adapt the dynamic model. Slow now, fast later.

Here is the data model as an image:

![Data model overview](/images/data_model_overview.png)

The following rules will be applied to the data:

* The Bank entity is an RFB entity. So are all of its directly held subsidiaries. These will be deemed to be RFB.
* Of the RFB entities, all UK domiciled entities will be deemed to be CORE. 
* All non UK domiciled entities will deemed to be NON CORE. Now, this is a bit of a hack, but to be honest it is very close to how the CRR legislation is actually applied. Good enough for now.
* The Group entity, and all other non Bank subs will be deemed to be outside the RFB, and will be characterised as NRFB.

Now this is an abstraction of the IRL rules. But, all the actual CRR rules could be applied. Too much work for this mini project, but it is achievable.

This results in the decision tree as shown:



Now to complete our pretend Bank we are going to add a bunch of random exposures across the entities. The products, limits and types will be as follows. This is of course grossly over simplified.

| Limit Type | Limit Sub Type | Product |
|---|---|---|
| Hard | Traded | FX Forward |
| Hard | Traded | Committed Repo |
| Hard | Lending | Committed Loan |
| Hard | Lending | Overdraft |
| Hard | Traded | Bond Borrow |
| Hard | Traded | Xccy Swap |
| Soft | Settlement | Payment Intraday |

---

![CRR treatment decision tree](/images/crr_decision_tree.png)

---

The basics of the code snippet setting CRR treatment are below:

```
def crr_treatment(cred_id, deb_id):
    """
    Derive CRR regulatory treatment for a bilateral exposure.

    Rules (applied in order):
      RFB_X        : creditor inside Bank sub-group, debtor outside
      NRFB_X       : creditor outside Bank sub-group, debtor inside
      [L2]_CORE    : both in same L2 sub-group, L2 is CORE (UK-domiciled RFB)
      [L2]_NON_CORE: both in same L2 sub-group, L2 is NON CORE (non-UK RFB)
      RFB_INTERNAL : both inside Bank sub-group, different L2 sub-groups
      NRFB_CROSS   : both outside Bank sub-group, different L2 sub-groups
    """
    cr_in_bank = cred_id in bank_subtree
    de_in_bank = deb_id  in bank_subtree
    cr_l2      = get_l2_ancestor(cred_id)
    de_l2      = get_l2_ancestor(deb_id)

    if cr_in_bank and not de_in_bank:
        return 'RFB_X'

    if not cr_in_bank and de_in_bank:
        return 'NRFB_X'

    if cr_l2 and de_l2 and cr_l2 == de_l2:
        l2 = emap[cr_l2]
        if l2['rf'] == 'CORE':     return f"{l2['name']}_CORE"
        if l2['rf'] == 'NON CORE': return f"{l2['name']}_NON_CORE"

    if cr_in_bank and de_in_bank:
        return 'RFB_INTERNAL'

    return 'NRFB_CROSS'
```
No, its not all the code, just the simplified part. To do the whole thing you need to deploy the equivalent of recursive SQL techniques. This lets you walk back up from the exposure at whatever subsidiary, to the relevant grouping. This is akin to figuring who someone's parents are from family data. Common use cases of this technique include counting sequences and finding family tree ancestors using common table expressions (CTEs). In this manner say you started at an L6 subsidiary. You walk back up the hierarchy until you run out of options, or more eloquantly apply common table expression (CTE) as a query that continuously references a previous result until it returns an empty result. You can use panda's dataframes for this, or you can tell your favourite AI to use that tool suite. Code is irrelevant, concept is important.

As an aside, don't knock old school SQL. It was invented in the 1970's to solve real world problems. If you write a bit of code or small language and someone is using it 60 years later, you probably did something smart. You also probably did it with pencil and paper. Development tools were largely no existant then. These people really were geniuses in their day. Que Ted Codd reference ....

Read about the crazy early days here if you have the interest:

https://archive.computerhistory.org/resources/access/text/2013/05/102702562-05-01-acc.pdf

Best quote:

> Ted looked at what was going on out there and saw what I like the call “higgledy-piggledy” systems. There was no abstraction; there was no mathematics. It was just write code and hope it works.

Some things really don't change. The original vibe coders...... Now I will shut up or I'll have to move this to the Comp Science section, and I cannot be bothered.

---

## The solution

Now we have our standing assumptions. We have run the rules over the data to create the tables shown above. And if the rules change, we can change the tables of derived attributes as needed. That part is buried in the python. The tables used for below are static, as in the rules set out applied to the made up structure, with made up products and limits applied at subsidiary level. Note that aggregation is permitted. So at L3, exposure is all of the exposure at L4 and below aggregated.

Brief pause, IRL there will be netting, and subadditivity problems all over the place. I am aware, but don't want this project to get out of control for scope. As presented is good enough, but its not complete or accurate to the nth degree.

Now, wrapping the data tables up in a little widget, we now have a dynamic reporting tool. Anything you like in combination. If we had made the decision to have lost say L3 and used that as the regulatory bucket aggregator (eg NON CORE), then that would be a set aggregator. You could sum for that, but noting else. You would also have lost the ability to aggregate at L4 group for any other reason. By keeping the legal entity data pure, we have avoided that problem all together.

It is harder to establish regulatory risk attributes by applying a suite of rules at the product exposure level, but not as hard you might think. Once done, its set and forget until the position runs off. But the trouble is rewarded, as you can then report any entity, to any entity (or group), with or without the CRR lens applied.

---
Lets take our subset of the portfolio from the above image, and lay it out in table form. Same rules have been applied, nothing manual has been adjusted.

## Regulatory Treatment — £100 Loan Matrix (5 Entities)


---

### NRFB_CROSS — both parties outside Bank sub-group (2 records)

| Creditor | Domicile | Debtor | Domicile | Limit GBP | Exposure GBP |
|---|---|---|---|---:|---:|
| Group Co | UK | Market Co | UK | £100 | £100 |
| Market Co | UK | Group Co | UK | £100 | £100 |

---

### NRFB_X — creditor outside Bank sub-group → debtor inside (6 records)

| Creditor | Domicile | Debtor | Domicile | Limit GBP | Exposure GBP |
|---|---|---|---|---:|---:|
| Group Co | UK | Bank Co | UK | £100 | £100 |
| Group Co | UK | Retail Co | UK | £100 | £100 |
| Group Co | UK | Corp Co | AU | £100 | £100 |
| Market Co | UK | Bank Co | UK | £100 | £100 |
| Market Co | UK | Retail Co | UK | £100 | £100 |
| Market Co | UK | Corp Co | AU | £100 | £100 |

---

### RFB_X — creditor inside Bank sub-group → debtor outside (6 records)

| Creditor | Domicile | Debtor | Domicile | Limit GBP | Exposure GBP |
|---|---|---|---|---:|---:|
| Bank Co | UK | Group Co | UK | £100 | £100 |
| Bank Co | UK | Market Co | UK | £100 | £100 |
| Retail Co | UK | Group Co | UK | £100 | £100 |
| Retail Co | UK | Market Co | UK | £100 | £100 |
| Corp Co | AU | Group Co | UK | £100 | £100 |
| Corp Co | AU | Market Co | UK | £100 | £100 |

---

### RFB_INTERNAL — both inside Bank sub-group, cross L2 boundary (6 records)

#### CORE → CORE

| Creditor | Domicile | Debtor | Domicile | Limit GBP | Exposure GBP |
|---|---|---|---|---:|---:|
| Bank Co | UK | Retail Co | UK | £100 | £100 |
| Retail Co | UK | Bank Co | UK | £100 | £100 |

#### CORE → NON CORE

| Creditor | Domicile | Debtor | Domicile | Limit GBP | Exposure GBP |
|---|---|---|---|---:|---:|
| Bank Co | UK | Corp Co | AU | £100 | £100 |
| Retail Co | UK | Corp Co | AU | £100 | £100 |

#### NON CORE → CORE

| Creditor | Domicile | Debtor | Domicile | Limit GBP | Exposure GBP |
|---|---|---|---|---:|---:|
| Corp Co | AU | Bank Co | UK | £100 | £100 |
| Corp Co | AU | Retail Co | UK | £100 | £100 |

---


Note that RFB_INTERNAL covers cross-boundary flows within the Bank sub-group — Bank Co ↔ Retail Co and Bank Co ↔ Corp Co, as well as Retail Co ↔ Corp Co. These are intra-RFB but cross different L2 sub-groups, which is precisely the consolidation elimination problem the post is about: same ring fence, different legal entity, £100 each way that nets to zero at the group level but needs to be tracked individually at the entity level.

---


### How the Widget Works
The widget is a self-contained interactive data application built entirely in vanilla HTML, CSS and JavaScript — no frameworks, no external dependencies beyond the world map fetch.

#### Data model
Three normalised JavaScript arrays mirror the three CSV dataframes exactly:

ENTITIES — 62 legal entities with all attributes
LIMIT_TYPES — 7 product taxonomy entries
LIMITS_EXP — 300 bilateral limit and exposure records (all made up!)

These are stored in legal-entity-widget.js and loaded as a static file. The JS builds two lookup maps on startup — EMAP (entity by ID) and LTMAP (limit type by product name) — which act as the join keys, replicating what pandas.merge() does in the Python model.

Yes, I cheated a bit here. I laid it out, did some of the basic setups in python as proof on concept. Made sure the geographic part worked. Then I had Claude clean up my messy files and join it all to render in the one window. It did not work right off the bat though, there were a lot of fixes required to get it to render properly. I'll add the js file below. You can take the concept and morph the basic approach into anything you like. I spent quite some time on this as I will recycle the concept in other posts.

## Said widget

{{< legal-entity-widget >}}

## Static Networks

Some static views of the legal structure, shown as network node diagrams. Because the data was random and made up, it does not make for a very interesting output. IRL this would be more informative. The point here I suppose is that the best way of thinking about exposures across a large bank IRL is as a network node diagram. Then you can make the edges what you want, eg CRR regulatory exposures, etc, etc.

For completeness, here are the static png files. 

![Exposure network — full portfolio](/images/network_full.png)

![Exposure network — L3 aggregated](/images/network_l3_tree.png)

![Exposure network — L2 aggregated](/images/network_l2_tree.png)

## Closing comments

The lesson here is that while yes, legacy systems suck, computer science has moved on a long way. There are a lot of ways to build out reporting using additional tooling outside of said legacy systems. Really all you need is a back end data access (ssh, api, sql, whatever) and then some brains. You can do pretty much the whole lot without resorting to licensed products. Python and java and some related libraries are all very useful things. Experiment like crazy, and when you love what you have, go spend the bucks to get an enterprise version.

The trick is thinking it all the way through first. No junior software developer is going to know what the data means, and how it should be used. Now ideally you are a very experienced finance professional and also really good at comp science. Good luck with that.

> We started with a legacy system setup, preventing multiple instances of KYC entities across the group structure. We duplicated the entity structure outside of the existing data. We did not give up a level in the legal entity structure to achieve regulatory reporting, we kept our data intact. We added dynamic regulatory attributes calculated on a rules based approach that broadly mapped the IRL approaches. We ran our reporting system as an external overlay, tied to legacy data. We did this using java scripted widget, as an example that approaching the problem properly with a bit of thought resulted in a more flexible and intelligent outcome. We considered the view of a single entity to any other (one to many), we considered the reverse of all limits to any entity (many to one). We considered the entire portfolio (many to many). We enabled any combination of exposures from any entity, to any other or many others, based on regulatory approach. We did not break existing infrastructure doing this. A lot more could be done on the logic to improve things. More would be needed for proper IRL solution. But this was an afternoons work. Yes, I cheated and used AI to do the network node diagrams. If the data was not made up nonsense it would work better. Slow is fast and fast is slow.

---

## References

---

## Appendix — Ring Fencing Primer

Ring fencing, like it says on the tin, is an approach to corralling (lets stick with the fence metaphor) the parts of the bank that do deposit taking, from the rest of the bank of group. Key details are below, but in essence the pre crisis banks were (i) run too thin on capital; and (ii) run by self serving morons in the main who did not know where their ability ended. That a bit sharp, but without government intervention, a lot more banks would have failed. Governments don’t like bailing out banks. But its quite hard to have an economy without functional banks for some complex reasons we will get into later. For now Bank is an authorised deposit taking institution, and Shadow Bank means something that does lending minus the deposit part. That is a long story for another time.

#### Background
Following the Global Financial Crisis (GFC) of 2007-08, HM Treasury, on the recommendation of
the Independent Commission on Banking (ICB), established a ring-fencing regime for large banks in the UK. The regime was legislated for in the Financial Services (Banking Reform) Act 2013. The
regime came into full effect on 1 January 2019. The government made two Orders under the
Financial Services and Markets Act (FSMA) 2000, which set the detailed calibration of the ring-
fence:
i. The Financial Services and Markets Act 2000 (Ring-fenced Bodies and Core Activities) Order
ii. (CAO) 20141; and
The Financial Services and Markets Act 2000 (Excluded Activities and Prohibitions) Order
(EAPO) 2014.2

The regime’s objectives, as outlined by the ICB, are to “make it easier to sort out both ring-fenced
banks and non-ring-fenced banks which get into trouble, without the provision of taxpayer-funded
solvency support” and to “insulate vital banking services on which households and SMEs depend
from problems elsewhere in the financial system”.3 Ring-fencing requires the largest UK banks to
separate core retail banking from investment banking in order to support financial stability by
making banking groups simpler and easier to ‘resolve’. 

#### Parameters
The key parameters of the ring-fence, as set in the Core Activities Order and Excluded Activities
and Prohibitions Order, are:

* Scope: Banking groups with more than £25bn of “core deposits”, defined as UK or EEA retail
and SME deposits, must comply with the regime. They are required to separate their retail and
investment banking activities into a ring-fenced body (RFB) and a non-ring-fenced body (NRFB)
and hold core deposits within the RFB.
* Excluded Activities: RFBs are prohibited from dealing in investments and commodities as
principal, with the exceptions of dealing in investments to manage their own risks and to sell
simple derivatives to their customers.
* Prohibitions: RFBs cannot have exposures to “relevant financial institutions” (RFIs), such as
NRFBs, investment firms, globally systemically important insurers (GSIIs), and investment funds.
They can provide specified products including trade finance products. They are largely
prohibited from operating outside the EEA.

Source for above is :
https://www.legislation.gov.uk/uksi/2025/30/pdfs/uksiod_20250030_en_001.pdf

---

## Data Files

I mean they are all made up nonsense and you can see the content in the widget, but hey, why not.

- [Legal entities](/data/df_legal_entity.csv)
- [Limit types](/data/df_limit_type.csv)
- [Limits and exposures](/data/df_limits_exposures.csv)
