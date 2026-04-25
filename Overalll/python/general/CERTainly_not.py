from pathlib import Path

from Crypto.PublicKey import RSA

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
DATA_DIRS = [
    SCRIPT_DIR,
    REPO_ROOT / "general" / "CERTainly not",
]


def find_input_file(name):
    for directory in DATA_DIRS:
        path = directory / name
        if path.exists():
            return path
    raise FileNotFoundError(f"Could not find {name}")


with open(find_input_file("2048b-rsa-example-cert.der"), "rb") as f:
    der_data = f.read()

key = RSA.importKey(der_data)

print(key.n)
