"""
yolo_classify_chunk.py
-----------------------
Worker for yolo_classify.py's full-dataset run, split into N parallel
chunks so the full 7,390-image pass fits comfortably inside a single
background command's time budget. Each chunk uses its own slice of
CPU threads (torch.set_num_threads) so N chunks running at once don't
oversubscribe the machine's cores. Writes its own JSON file; a
separate merge step (yolo_classify_merge.py) combines them.

Usage: python3 yolo_classify_chunk.py <chunk_index> <n_chunks> <threads_per_chunk>
"""
import os
import sys
import json
import time
import numpy as np
import torch

CHUNK_IDX = int(sys.argv[1])
N_CHUNKS = int(sys.argv[2])
THREADS = int(sys.argv[3])
torch.set_num_threads(THREADS)

from ultralytics import YOLO

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMG_SIZE = 320
BATCH = 16


def gather(split):
    items = []
    for label, class_id in (("cats", 0), ("dogs", 1)):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            items.append((os.path.join(folder, fname), class_id, split))
    return items


def main():
    all_items = gather("train") + gather("test")
    items = all_items[CHUNK_IDX::N_CHUNKS]
    paths = [p for p, _, _ in items]

    model = YOLO("yolo26n.pt")
    names = model.names
    cat_id = [k for k, v in names.items() if v == "cat"][0]
    dog_id = [k for k, v in names.items() if v == "dog"][0]

    print(f"[chunk {CHUNK_IDX}] {len(paths)} images, {THREADS} threads", flush=True)
    t0 = time.time()
    records = []
    idx = 0
    for result in model.predict(source=paths, imgsz=IMG_SIZE, batch=BATCH,
                                 device="cpu", verbose=False, stream=True):
        path, true_id, split = items[idx]
        idx += 1
        cls = result.boxes.cls.numpy().astype(int) if result.boxes is not None else np.array([])
        conf = result.boxes.conf.numpy() if result.boxes is not None else np.array([])
        mask = (cls == cat_id) | (cls == dog_id)
        pred_id, pred_conf = None, None
        if mask.any():
            best = np.argmax(conf[mask])
            best_cls = cls[mask][best]
            pred_id = 0 if best_cls == cat_id else 1
            pred_conf = float(conf[mask][best])
        records.append({"path": path, "split": split, "true": true_id,
                         "pred": pred_id, "conf": pred_conf})
        if idx % 200 == 0:
            print(f"[chunk {CHUNK_IDX}] {idx}/{len(paths)} ({time.time()-t0:.0f}s)", flush=True)

    out_path = os.path.join(os.path.dirname(__file__), f"yolo_chunk_{CHUNK_IDX}.json")
    with open(out_path, "w") as f:
        json.dump(records, f)
    print(f"[chunk {CHUNK_IDX}] done: {len(records)} images in {time.time()-t0:.0f}s -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
