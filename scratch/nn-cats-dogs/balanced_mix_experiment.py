"""
balanced_mix_experiment.py
----------------------------
Isolates the effect of class MIX from the effect of population SCALE on
the real Oxford-IIIT Pet run in train_nn.py, using the identical
load_split(), Pipeline, and MLPClassifier hyperparameters -- only the
training pool composition changes. Evaluated against the exact same
120-image held-out test set both times, for a fair comparison.

Three points of comparison:
  A. baseline    -- full imbalanced training pool, as train_nn.py ran it
                     (2,340 cats + 4,930 dogs = 7,270)
  B. undersample -- balanced by dropping dogs down to the cat count
                     (2,340 cats + 2,340 dogs = 4,680, smaller AND balanced)
  C. oversample  -- balanced by duplicating cats up to the dog count
                     (4,930 cats [with repeats] + 4,930 dogs = 9,860,
                     same class balance as B but back to (and past) A's scale)

Comparing A vs B isolates "does balance help, even at a smaller scale."
Comparing B vs C isolates "does scale help, once balance is already fixed."
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
IMG_SIZE = 48
RANDOM_STATE = 42


def load_split(split):
    X, y, paths = [], [], []
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
            paths.append(path)
    return np.array(X), np.array(y), paths


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


def run_variant(name, X_pool, y_pool, X_test, y_test):
    X_train, X_val, y_train, y_val = train_test_split(
        X_pool, y_pool, test_size=0.15, random_state=RANDOM_STATE, stratify=y_pool,
    )
    clf = make_pipeline()
    clf.fit(X_train, y_train)
    mlp = clf.named_steps["mlp"]
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["cat", "dog"], output_dict=True)
    result = {
        "variant": name,
        "n_cats": int((y_pool == 0).sum()),
        "n_dogs": int((y_pool == 1).sum()),
        "n_train_pool": int(len(y_pool)),
        "epochs_run": int(mlp.n_iter_),
        "test_accuracy": float(acc),
        "cat_recall": float(report["cat"]["recall"]),
        "dog_recall": float(report["dog"]["recall"]),
        "confusion_matrix": cm.tolist(),
    }
    print(json.dumps(result, indent=2))
    return result


def main():
    print("Loading full training pool and test set ...")
    X_train_full, y_train_full, _ = load_split("train")
    X_test, y_test, _ = load_split("test")

    cat_idx = np.where(y_train_full == 0)[0]
    dog_idx = np.where(y_train_full == 1)[0]
    print(f"Full pool: {len(cat_idx)} cats, {len(dog_idx)} dogs")

    rng = np.random.RandomState(RANDOM_STATE)

    results = []

    # A. baseline -- exactly what train_nn.py already ran (rerun here for
    # an apples-to-apples print, same seed, should match results.json)
    results.append(run_variant("A_baseline_imbalanced", X_train_full, y_train_full, X_test, y_test))

    # B. undersample dogs down to the cat count -- balanced, smaller
    dog_under = rng.choice(dog_idx, size=len(cat_idx), replace=False)
    under_idx = np.concatenate([cat_idx, dog_under])
    results.append(run_variant(
        "B_balanced_undersampled",
        X_train_full[under_idx], y_train_full[under_idx], X_test, y_test,
    ))

    # C. oversample cats up to the dog count (with replacement) -- balanced, larger
    cat_over = rng.choice(cat_idx, size=len(dog_idx), replace=True)
    over_idx = np.concatenate([cat_over, dog_idx])
    results.append(run_variant(
        "C_balanced_oversampled",
        X_train_full[over_idx], y_train_full[over_idx], X_test, y_test,
    ))

    with open(os.path.join(os.path.dirname(__file__), "mix_experiment_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("\n=== Summary ===")
    for r in results:
        print(f"{r['variant']:30s} n_train={r['n_train_pool']:5d} "
              f"({r['n_cats']}c/{r['n_dogs']}d)  "
              f"test_acc={r['test_accuracy']:.3f}  "
              f"cat_recall={r['cat_recall']:.2f}  dog_recall={r['dog_recall']:.2f}")


if __name__ == "__main__":
    main()
