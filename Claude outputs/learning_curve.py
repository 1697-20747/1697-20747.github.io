"""
learning_curve.py
------------------
Answers a concrete question: with the same flatten-pixels-into-an-MLP
approach as train_nn.py, does more real training data close the gap
between the 93.3% synthetic-silhouette result and the 55.0% real-photo
result? Retrains the identical pipeline (StandardScaler + MLPClassifier,
same hyperparameters as train_nn.py) on stratified subsamples of the
real Oxford-IIIT Pet training pool, at increasing sizes, always scored
against the same untouched 120-image held-out test set.
"""
import os
import json
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.color import gray2rgb, rgba2rgb
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMG_SIZE = 48
RANDOM_STATE = 42
TRAIN_SIZES = [300, 500, 1000, 2000, 4000, 6000, 7270]


def load_split(split):
    X, y = [], []
    for label, class_id in (("cats", 0), ("dogs", 1)):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            path = os.path.join(folder, fname)
            img = imread(path)
            if img.ndim == 4 and img.shape[0] == 1:
                img = img[0]
            if img.ndim == 2:
                img = gray2rgb(img)
            elif img.shape[2] == 4:
                img = rgba2rgb(img)
            img = resize(img, (IMG_SIZE, IMG_SIZE, 3), anti_aliasing=True)
            X.append(img.flatten())
            y.append(class_id)
    return np.array(X), np.array(y)


def make_pipeline():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation="relu",
            solver="adam",
            alpha=1e-4,
            batch_size=32,
            learning_rate_init=1e-3,
            max_iter=400,
            early_stopping=True,
            n_iter_no_change=15,
            validation_fraction=0.15,
            random_state=RANDOM_STATE,
        )),
    ])


def main():
    print("Loading full training pool and held-out test set ...")
    X_train_full, y_train_full = load_split("train")
    X_test, y_test = load_split("test")
    n_total = X_train_full.shape[0]
    print(f"Full train pool: {n_total} images. Test set: {X_test.shape[0]} images.\n")

    results = []
    for size in TRAIN_SIZES:
        if size >= n_total:
            X_sub, y_sub = X_train_full, y_train_full
            actual_size = n_total
        else:
            X_sub, _, y_sub, _ = train_test_split(
                X_train_full, y_train_full,
                train_size=size, stratify=y_train_full, random_state=RANDOM_STATE,
            )
            actual_size = size

        clf = make_pipeline()
        clf.fit(X_sub, y_sub)
        mlp = clf.named_steps["mlp"]
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        n_cats = int((y_sub == 0).sum())
        n_dogs = int((y_sub == 1).sum())

        print(f"n_train={actual_size:5d} (cats={n_cats}, dogs={n_dogs})  "
              f"epochs={mlp.n_iter_:3d}  test_acc={acc:.3f}")

        results.append({
            "n_train": actual_size,
            "n_cats": n_cats,
            "n_dogs": n_dogs,
            "epochs_run": int(mlp.n_iter_),
            "test_accuracy": float(acc),
        })

    with open(os.path.join(os.path.dirname(__file__), "learning_curve_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved: learning_curve_results.json")


if __name__ == "__main__":
    main()
