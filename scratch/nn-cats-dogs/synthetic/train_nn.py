"""
train_nn.py
------------
Trains a feed-forward neural network (an sklearn MLPClassifier, i.e. a
Multi-Layer Perceptron with backpropagation) from scratch -- random
initial weights, no pretrained model -- to tell cat images from dog
images.

Follows the workflow scikit-learn's own "Supervised learning" guide uses
throughout (https://scikit-learn.org/stable/supervised_learning.html),
whose neural-network section is
https://scikit-learn.org/stable/modules/neural_networks_supervised.html:

    1. load data as a flat (n_samples, n_features) array + a label vector
    2. train_test_split
    3. wrap preprocessing + estimator in a Pipeline
    4. StandardScaler to zero-mean/unit-variance the features
    5. fit the estimator
    6. predict on held-out data and score it with classification_report /
       confusion_matrix

This is the full version, including the bookkeeping (results.json, loss
curve, confusion matrix, sample predictions) trimmed from the code block
shown in the blog post for readability.
"""
import os
import json
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMG_SIZE = 48  # must match generate_dataset.py
RANDOM_STATE = 42


def load_split(split):
    """Read every PNG under data/<split>/{cats,dogs}/ into (X, y)."""
    X, y, paths = [], [], []
    for label, class_id in (("cats", 0), ("dogs", 1)):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            path = os.path.join(folder, fname)
            img = imread(path)                                          # (H, W, 3) uint8
            img = resize(img, (IMG_SIZE, IMG_SIZE), anti_aliasing=True)  # -> float [0, 1]
            X.append(img.flatten())                                     # 1-D feature vector
            y.append(class_id)
            paths.append(path)
    return np.array(X), np.array(y), paths


def main():
    print("Loading images with skimage.io.imread ...")
    X_train_full, y_train_full, _ = load_split("train")
    X_test, y_test, test_paths = load_split("test")

    print(f"Train pool: {X_train_full.shape[0]} images, "
          f"{X_train_full.shape[1]} features each "
          f"({IMG_SIZE}x{IMG_SIZE}x3 flattened)")
    print(f"Held-out test set: {X_test.shape[0]} images")

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full,
        test_size=0.15, random_state=RANDOM_STATE, stratify=y_train_full,
    )

    clf = Pipeline([
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

    print("Training MLPClassifier ...")
    clf.fit(X_train, y_train)

    mlp = clf.named_steps["mlp"]
    print(f"Stopped after {mlp.n_iter_} epochs (converged={mlp.n_iter_ < mlp.max_iter})")

    val_acc = accuracy_score(y_val, clf.predict(X_val))
    y_pred = clf.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)

    print(f"\nValidation accuracy: {val_acc:.3f}")
    print(f"Test accuracy:       {test_acc:.3f}\n")
    report = classification_report(y_test, y_pred, target_names=["cat", "dog"])
    print(report)
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion matrix [[TN, FP], [FN, TP]] (0=cat, 1=dog):")
    print(cm)

    np.save(os.path.join(os.path.dirname(__file__), "loss_curve.npy"),
            np.array(mlp.loss_curve_))
    if getattr(mlp, "validation_scores_", None) is not None:
        np.save(os.path.join(os.path.dirname(__file__), "val_curve.npy"),
                np.array(mlp.validation_scores_))
    np.save(os.path.join(os.path.dirname(__file__), "confusion_matrix.npy"), cm)

    results = {
        "n_train": int(X_train.shape[0]),
        "n_val": int(X_val.shape[0]),
        "n_test": int(X_test.shape[0]),
        "n_features": int(X_train.shape[1]),
        "epochs_run": int(mlp.n_iter_),
        "max_iter": int(mlp.max_iter),
        "converged_before_max_iter": bool(mlp.n_iter_ < mlp.max_iter),
        "final_training_loss": float(mlp.loss_curve_[-1]),
        "validation_accuracy": float(val_acc),
        "test_accuracy": float(test_acc),
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
        "hidden_layer_sizes": list(mlp.hidden_layer_sizes),
        "n_layers_total": int(mlp.n_layers_),
        "n_parameters": int(sum(w.size for w in mlp.coefs_) + sum(b.size for b in mlp.intercepts_)),
    }
    with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    rng = np.random.RandomState(RANDOM_STATE)
    sample_idx = rng.choice(len(test_paths), size=8, replace=False)
    sample_info = [
        {
            "path": test_paths[i],
            "true": "cat" if y_test[i] == 0 else "dog",
            "pred": "cat" if y_pred[i] == 0 else "dog",
        }
        for i in sample_idx
    ]
    with open(os.path.join(os.path.dirname(__file__), "sample_predictions.json"), "w") as f:
        json.dump(sample_info, f, indent=2)

    print("\nSaved: results.json, loss_curve.npy, confusion_matrix.npy, sample_predictions.json")


if __name__ == "__main__":
    main()
