import string
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

import requests

BASE_URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/"
BLOCK_SIZE = 16
MAX_FLAG_LEN = 64
MAX_WORKERS = 8

# Tập ký tự thử nghiệm
alphabet = string.printable

_thread_local = threading.local()


def _get_session():
    # Tạo session riêng cho mỗi thread để tái sử dụng kết nối HTTP
    if not hasattr(_thread_local, "session"):
        _thread_local.session = requests.Session()
    return _thread_local.session

@lru_cache(maxsize=4096)
# Hàm gọi API để lấy bản mã
def encrypt(plaintext):
    # API yêu cầu gửi data dưới dạng chuỗi hex
    hex_data = plaintext.encode().hex()
    url = f"{BASE_URL}{hex_data}/"
    response = _get_session().get(url, timeout=10)
    response.raise_for_status()
    return response.json()['ciphertext']


def _find_next_char(executor, padding, known_flag, start_idx, end_idx, target_block):
    futures = {
        executor.submit(encrypt, padding + known_flag + char): char
        for char in alphabet
    }

    found_char = None
    try:
        for future in as_completed(futures):
            char = futures[future]
            guess_ciphertext = future.result()
            guess_block = guess_ciphertext[start_idx:end_idx]
            if guess_block == target_block:
                found_char = char
                break
    finally:
        # Hủy các request chưa chạy để tránh backlog khi đã tìm ra ký tự đúng
        for future in futures:
            future.cancel()

    return found_char


def main():
    flag = ""

    # Duyệt để tìm từng ký tự của flag
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i in range(1, MAX_FLAG_LEN + 1):
            # Đặt ký tự cần tìm vào cuối block để so sánh chính xác
            pad_length = (BLOCK_SIZE - (i % BLOCK_SIZE)) % BLOCK_SIZE
            padding = "A" * pad_length

            target_block_index = (i - 1) // BLOCK_SIZE
            if pad_length == 0:
                # API không chấp nhận plaintext rỗng (encrypt// -> 404),
                # nên thêm 1 block đệm và dịch block mục tiêu sang phải 1 block.
                padding = "A" * BLOCK_SIZE
                target_block_index += 1

            target_ciphertext = encrypt(padding)

            # Mỗi block = 16 bytes = 32 ký tự hex
            start_idx = target_block_index * 32
            end_idx = start_idx + 32
            target_block = target_ciphertext[start_idx:end_idx]

            next_char = _find_next_char(
                executor,
                padding,
                flag,
                start_idx,
                end_idx,
                target_block,
            )

            if next_char is None:
                raise RuntimeError("Không tìm được ký tự tiếp theo. Hãy thử giảm MAX_WORKERS.")

            flag += next_char
            print(f"Flag: {flag}")

            if flag.endswith("}"):
                break


if __name__ == "__main__":
    main()