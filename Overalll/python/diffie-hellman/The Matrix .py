def bits_to_bytes(bits):
    """Chuyển đổi danh sách bit thành chuỗi bytes"""
    chars = []
    for i in range(0, len(bits), 8):
        byte_str = "".join(map(str, bits[i:i+8]))
        chars.append(int(byte_str, 2))
    return bytes(chars)

# Giả sử sau khi dùng SageMath bạn đã tìm được ma trận M 50x50
# Ở đây tôi ví dụ với dữ liệu ma trận rỗng để bạn thấy logic trích xuất
N = 50
matrix_M = [[0 for _ in range(N)] for _ in range(N)] 

# Logic trích xuất bit theo hàng và cột từ script .sage gốc:
# rows = [msg[i::N] for i in range(N)]
# Điều này có nghĩa là mat[i][j] = msg[i + j*N]

extracted_bits = [0] * (N * N)
for i in range(N):
    for j in range(N):
        # Lấy giá trị tại hàng i, cột j gán lại vào vị trí ban đầu của msg
        # extracted_bits[i + j*N] = matrix_M[i][j]
        pass 

# In kết quả (sau khi đã có dữ liệu thật)
# print(bits_to_bytes(extracted_bits))