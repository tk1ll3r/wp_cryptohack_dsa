from PIL import Image
import numpy as np

img_flag = Image.open("D:\wp_cryptohack_dsa\general\XOR\Lemur XOR\\flag_7ae18c704272532658c10b5faad06d74.png")
img_lemur = Image.open("D:\wp_cryptohack_dsa\general\XOR\Lemur XOR\lemur_ed66878c338e662d3473f0d98eedbd0d.png")

arr_flag = np.array(img_flag)
arr_lemur = np.array(img_lemur)

result_arr = np.bitwise_xor(arr_flag, arr_lemur)

result_img = Image.fromarray(result_arr)

result_img.save("D:\wp_cryptohack_dsa\general\XOR\Lemur XOR\\decrypted_flag.png")
result_img.show()