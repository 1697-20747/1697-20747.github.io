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

Image loading uses scikit-image (skimage.io), an open-source computer
vision library, purely to read pixels into numpy arrays -- no
convolution, no image-specific model architecture. The network itself
only ever sees a flat vector of numbers, which is the point the blog post
makes explicit.
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
            img = imread(path)                       # (H, W, 3) uint8 array (varies: gray/RGBA/single-frame stacks too)
            if img.ndim == 4 and img.shape[0] == 1:
                img = img[0]
            if img.ndim == 2:
                img = gray2rgb(img)
            elif img.shape[2] == 4:
                img = rgba2rgb(img)
            img = resize(img, (IMG_SIZE, IMG_SIZE, 3), anti_aliasing=True)  # -> float [0,1]
            X.append(img.flatten())                  # (H*W*3,) 1-D feature vector
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

    # Carve a validation slice out of the training pool, exactly the
    # train_test_split pattern used throughout the sklearn user guide.
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
    print(f"Stopped after {mlp.n_iter_} epochs "
          f"(converged={mlp.n_iter_ < mlp.max_iter})")

    val_acc = accuracy_score(y_val, clf.predict(X_val))
    y_pred = clf.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["cat", "dog"])
    cm = confusion_matrix(y_test, y_pred)

    print(f"\nValidation accuracy (held out of the training pool): {val_acc:.3f}")
    print(f"Test accuracy (never seen during training):           {test_acc:.3f}\n")
    print(report)
    print("Confusion matrix [[TN, FP], [FN, TP]] (0=cat, 1=dog):")
    print(cm)

    # Persist everything the plotting script and the blog post need.
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

    # A handful of test images to show, with predictions, for the figure.
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
