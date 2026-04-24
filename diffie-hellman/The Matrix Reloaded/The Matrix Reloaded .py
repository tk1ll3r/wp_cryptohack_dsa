import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Thông số hệ thống
P = 13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471

def solve():
    print("[-] Đang đọc file flag.enc...")
    try:
        with open("flag.enc", "r") as f:
            data = json.load(f)
            iv = bytes.fromhex(data['iv'])
            ciphertext = bytes.fromhex(data['ciphertext'])
    except Exception as e:
        print(f"[!] Lỗi đọc file: {e}")
        return

    # SECRET ĐÚNG trích xuất từ Matrix DLP của bạn:
    # Sau khi giải lambda^x = target (mod P)
    SECRET = 10645601267882200251106606020521503814890665595907406184910906232750661148816782298715886982974917454316065471412093863778550275814120967000305886470366627

    print(f"[+] SECRET tìm được: {SECRET}")
    print("[-] Đang giải mã Flag...")

    # Tạo Key theo đúng matrix_reloaded.sage: SHA256(str(SECRET))[:16]
    key = hashlib.sha256(str(SECRET).encode()).digest()[:16]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted = unpad(cipher.decrypt(ciphertext), 16)
        print("\n" + "="*40)
        print(f"FLAG: {decrypted.decode()}")
        print("="*40)
    except Exception as e:
        print(f"[!] Giải mã thất bại: {e}. Kiểm tra lại SECRET.")

if __name__ == "__main__":
    solve()