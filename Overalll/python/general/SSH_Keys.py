from pathlib import Path

from Crypto.PublicKey import RSA

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
DATA_DIRS = [
    SCRIPT_DIR,
    REPO_ROOT / "general" / "Sshkey",
]


def find_input_file(name):
    for directory in DATA_DIRS:
        path = directory / name
        if path.exists():
            return path
    raise FileNotFoundError(f"Could not find {name}")


file_name = "bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub"

with open(find_input_file(file_name), "r") as f:
    key = RSA.importKey(f.read())

print(key.n)
