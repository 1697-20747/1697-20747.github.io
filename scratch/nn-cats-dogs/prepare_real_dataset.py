"""
prepare_real_dataset.py
-------------------------
Run this on a machine with an ordinary, unrestricted internet connection --
a plain Terminal window, or a Claude Code session started directly on your
Mac (NOT through the Cowork device bridge, which sits behind a governed
network allowlist and cannot reach these hosts). It downloads the real,
open-source Oxford-IIIT Pet Dataset and sorts it into the exact
data/train/{cats,dogs}/, data/test/{cats,dogs}/ layout train_nn.py expects
-- at that point generate_dataset.py is no longer needed at all, and
train_nn.py runs unmodified against real photographs.

Usage:
    python3 -m venv venv && source venv/bin/activate
    pip install requests pillow scikit-learn scikit-image matplotlib numpy
    python3 prepare_real_dataset.py
    python3 train_nn.py

Dataset: Oxford-IIIT Pet Dataset (Parkhi et al., 2012), University of
Oxford VGG group -- https://www.robots.ox.ac.uk/~vgg/data/pets/
37 breeds, ~200 images each, ~7,400 images total, ~800MB download.
No account or API key required (unlike Kaggle's Dogs vs. Cats).

Species convention used by this dataset: a filename's breed name is
capitalized for the 12 cat breeds (Abyssinian, Bengal, Birman, Bombay,
British_Shorthair, Egyptian_Mau, Maine_Coon, Persian, Ragdoll,
Russian_Blue, Siamese, Sphynx) and lowercase for the 25 dog breeds --
that capitalization is what this script uses to sort cat vs. dog.
"""
import os
import random
import shutil
import tarfile
import urllib.request

IMAGES_URL = "https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz"
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), "_oxford_pet_images.tar.gz")
EXTRACT_DIR = os.path.join(os.path.dirname(__file__), "_oxford_pet_extracted")

N_TEST_PER_CLASS = 60
RANDOM_STATE = 42

CAT_BREEDS = {
    "Abyssinian", "Bengal", "Birman", "Bombay", "British_Shorthair",
    "Egyptian_Mau", "Maine_Coon", "Persian", "Ragdoll", "Russian_Blue",
    "Siamese", "Sphynx",
}


def download():
    if os.path.exists(DOWNLOAD_PATH):
        print("Already downloaded:", DOWNLOAD_PATH)
        return
    print("Downloading Oxford-IIIT Pet images (~800MB) ...")
    urllib.request.urlretrieve(IMAGES_URL, DOWNLOAD_PATH)
    print("Done.")


def extract():
    if os.path.isdir(EXTRACT_DIR):
        print("Already extracted:", EXTRACT_DIR)
        return
    print("Extracting ...")
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    with tarfile.open(DOWNLOAD_PATH) as tf:
        tf.extractall(EXTRACT_DIR)
    print("Done.")


def sort_into_splits():
    random.seed(RANDOM_STATE)
    src = os.path.join(EXTRACT_DIR, "images")
    files = [f for f in os.listdir(src) if f.lower().endswith(".jpg")]

    cats, dogs = [], []
    for f in files:
        breed = f.rsplit("_", 1)[0]
        (cats if breed in CAT_BREEDS else dogs).append(f)

    print(f"Found {len(cats)} cat images, {len(dogs)} dog images")
    random.shuffle(cats)
    random.shuffle(dogs)

    for label, pool in (("cats", cats), ("dogs", dogs)):
        test_files = pool[:N_TEST_PER_CLASS]
        train_files = pool[N_TEST_PER_CLASS:]
        for split, split_files in (("test", test_files), ("train", train_files)):
            dest = os.path.join(OUT_DIR, split, label)
            os.makedirs(dest, exist_ok=True)
            for fname in split_files:
                shutil.copy(os.path.join(src, fname), os.path.join(dest, fname))
        print(f"{label}: {len(train_files)} train, {len(test_files)} test")

    print("\nDataset ready at", OUT_DIR)
    print("Run: python3 train_nn.py")


if __name__ == "__main__":
    download()
    extract()
    sort_into_splits()
