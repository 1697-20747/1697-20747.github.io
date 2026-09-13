"""
svm_model.py
------------
Replicates the approach from github.com/codewithRakz/SCT_ML_3: a
Support Vector Machine (linear kernel) trained on raw, flattened pixel
vectors -- images loaded with OpenCV, resized to 64x64, no feature
scaling. Same modeling recipe as that repo, applied to the real
Oxford-IIIT Pet dataset we already downloaded and split via
prepare_real_dataset.py, using its held-out data/test/{cats,dogs} set
so results are directly comparable to train_nn.py's MLP run.

Usage:
    source venv/bin/activate
    pip install opencv-python
    python3 svm_model.py
"""
import os
import json
import numpy as np
import cv2
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMG_SIZE = 64  # matches the referenced repo
RANDOM_STATE = 42


def load_split(split):
    X, y = [], []
    for label, class_id in (("cats", 0), ("dogs", 1)):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            path = os.path.join(folder, fname)
            image = cv2.imread(path)          # always BGR, 3-channel
            image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
            X.append(image.flatten())
            y.append(class_id)
    return np.array(X), np.array(y)


def main():
    print("Loading images with cv2.imread ...")
    X_train, y_train = load_split("train")
    X_test, y_test = load_split("test")

    print(f"Train pool: {X_train.shape[0]} images, {X_train.shape[1]} features each "
          f"({IMG_SIZE}x{IMG_SIZE}x3 flattened)")
    print(f"Held-out test set: {X_test.shape[0]} images")

    model = SVC(kernel="linear")
    print("Training linear-kernel SVC ...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["cat", "dog"])
    cm = confusion_matrix(y_test, y_pred)

    print(f"\nTest accuracy (never seen during training): {test_acc:.3f}\n")
    print(report)
    print("Confusion matrix [[TN, FP], [FN, TP]] (0=cat, 1=dog):")
    print(cm)

    results = {
        "n_train": int(X_train.shape[0]),
        "n_test": int(X_test.shape[0]),
        "n_features": int(X_train.shape[1]),
        "img_size": IMG_SIZE,
        "kernel": "linear",
        "test_accuracy": float(test_acc),
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
    }
    with open(os.path.join(os.path.dirname(__file__), "svm_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved: svm_results.json")


if __name__ == "__main__":
    main()
