from pathlib import Path

import numpy as np
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
DATA_DIRS = [
    SCRIPT_DIR,
    REPO_ROOT / "general" / "XOR" / "Lemur XOR",
]


def find_input_file(name):
    for directory in DATA_DIRS:
        path = directory / name
        if path.exists():
            return path
    raise FileNotFoundError(f"Could not find {name}")


img_flag = Image.open(find_input_file("flag.png"))
img_lemur = Image.open(find_input_file("lemur.png"))

arr_flag = np.array(img_flag)
arr_lemur = np.array(img_lemur)

result_arr = np.bitwise_xor(arr_flag, arr_lemur)
result_img = Image.fromarray(result_arr)

output_path = SCRIPT_DIR / "decrypted_flag.png"
result_img.save(output_path)
print(output_path)
