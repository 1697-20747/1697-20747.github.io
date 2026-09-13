"""
yolo_classify.py
-----------------
Runs the same cat/dog image sets used throughout this project (all
7,390 real Oxford-IIIT Pet photos, train and test pools combined --
no subsampling) through a pretrained YOLO26n object detector, zero
training on this project's data at all. YOLO26n was already trained
end-to-end on COCO (330k images, 80 object classes, including 'cat'
class 15 and 'dog' class 16) by Ultralytics; this script does no
fine-tuning, just inference, converting each image's detections into
a single cat/dog label the same way train_nn.py and svm_model.py
produce one: whichever of the two classes gets the detector's highest
confidence box in that image. No box of either class at all counts as
"no detection" -- reported separately, not silently dropped.

Images are processed in small explicit slices (predict() called fresh
per slice, not once over the full 7,390-path list) -- calling
predict() with one huge source list was observed to blow up memory
and stall indefinitely, while the same work done in slices of ~200
runs at the expected ~40ms/image. Each slice is checkpointed to disk
immediately so a restart never loses completed work.

Usage:
    source venv/bin/activate
    pip install ultralytics
    python3 yolo_classify.py
"""
import os
import json
import time
import numpy as np
from ultralytics import YOLO
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMG_SIZE = 320
BATCH = 16
SLICE_SIZE = 200
CKPT_PATH = os.path.join(os.path.dirname(__file__), "yolo_predictions.json")


def gather(split):
    items = []
    for label, class_id in (("cats", 0), ("dogs", 1)):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            items.append((os.path.join(folder, fname), class_id, split))
    return items


def main():
    print("Loading pretrained yolo26n.pt (COCO weights, no fine-tuning) ...", flush=True)
    model = YOLO("yolo26n.pt")
    names = model.names
    cat_id = [k for k, v in names.items() if v == "cat"][0]
    dog_id = [k for k, v in names.items() if v == "dog"][0]
    print(f"COCO class ids -- cat: {cat_id}, dog: {dog_id}", flush=True)

    items = gather("train") + gather("test")
    print(f"Running zero-shot detection on {len(items)} images "
          f"(train+test pools combined, full set, imgsz={IMG_SIZE}, "
          f"slices of {SLICE_SIZE}) ...", flush=True)

    records = []
    if os.path.exists(CKPT_PATH):
        with open(CKPT_PATH) as f:
            records = json.load(f)
        print(f"Resuming from checkpoint: {len(records)} images already done.", flush=True)

    t0 = time.time()
    start = len(records)
    for s in range(start, len(items), SLICE_SIZE):
        chunk = items[s:s + SLICE_SIZE]
        paths = [p for p, _, _ in chunk]
        results = model.predict(source=paths, imgsz=IMG_SIZE, batch=BATCH,
                                 device="cpu", verbose=False)
        for (path, true_id, split), result in zip(chunk, results):
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

        elapsed = time.time() - t0
        done = len(records)
        rate = (done - start) / elapsed if elapsed > 0 else 0
        print(f"  {done}/{len(items)} done ({elapsed:.0f}s elapsed, {rate:.1f} img/s)", flush=True)
        with open(CKPT_PATH, "w") as f:
            json.dump(records, f)

    elapsed = time.time() - t0
    print(f"\nDone: {len(records)} images total, "
          f"{elapsed:.1f}s for this run's slices\n", flush=True)

    def summarize(recs, label):
        y_true = np.array([r["true"] for r in recs])
        y_pred_raw = [r["pred"] for r in recs]
        n_detected = sum(p is not None for p in y_pred_raw)
        coverage = n_detected / len(recs)

        y_pred_strict = np.array([p if p is not None else 1 - t
                                   for p, t in zip(y_pred_raw, y_true)])
        acc_strict = accuracy_score(y_true, y_pred_strict)

        idxs = [i for i, p in enumerate(y_pred_raw) if p is not None]
        acc_detected = accuracy_score(y_true[idxs], [y_pred_raw[i] for i in idxs]) if idxs else float("nan")

        cm = confusion_matrix(y_true, y_pred_strict)
        report = classification_report(y_true, y_pred_strict, target_names=["cat", "dog"])

        print(f"--- {label} (n={len(recs)}) ---", flush=True)
        print(f"Coverage (detector found a cat or dog at all): {coverage:.3f} ({n_detected}/{len(recs)})", flush=True)
        print(f"Accuracy among detected only:                  {acc_detected:.3f}", flush=True)
        print(f"Accuracy overall (no-detection counted wrong): {acc_strict:.3f}", flush=True)
        print(report, flush=True)
        print("Confusion matrix [[TN, FP], [FN, TP]] (0=cat, 1=dog), no-detection counted wrong:", flush=True)
        print(cm, flush=True)
        print(flush=True)
        return {
            "n": len(recs), "coverage": coverage,
            "accuracy_among_detected": acc_detected,
            "accuracy_overall": acc_strict,
            "confusion_matrix": cm.tolist(),
            "classification_report": report,
        }

    all_summary = summarize(records, "Full pool: all 7,390 train+test images")
    test_only = [r for r in records if r["split"] == "test"]
    test_summary = summarize(test_only, "Held-out 120-image test set only (comparable to MLP/SVM numbers)")

    with open(os.path.join(os.path.dirname(__file__), "yolo_results.json"), "w") as f:
        json.dump({"full_pool": all_summary, "test_only": test_summary}, f, indent=2)
    print("Saved: yolo_predictions.json, yolo_results.json", flush=True)


if __name__ == "__main__":
    main()
