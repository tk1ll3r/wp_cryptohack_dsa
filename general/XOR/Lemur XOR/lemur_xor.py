from PIL import Image
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_flag = os.path.join(current_dir, "flag.png")
file_path_lemur = os.path.join(current_dir, "lemur.png")

img_flag = Image.open(file_path_flag)
img_lemur = Image.open(file_path_lemur)

arr_flag = np.array(img_flag)
arr_lemur = np.array(img_lemur)

result_arr = np.bitwise_xor(arr_flag, arr_lemur)
result_img = Image.fromarray(result_arr)

result_img.save(os.path.join(current_dir, "decrypted_flag.png"))
result_img.show()