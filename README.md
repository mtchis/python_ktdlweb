# python_ktweb

YÊU CẦU CHI TIẾT
1. Tạo Crawler và tiến hành thực hiện thu thập các dữ liệu tối thiểu 02 nguồn
Website có các thông tin trong các lĩnh vực sau:

• Giáo dục
• Y tế
• Khoa học – Công nghệ
• Giải trí
• Thể thao
• Sức khoẻ
• Đời sống
• Du lịch

2. Cho phép người dùng nhập vào địa chỉ website cần thu thập dữ liệu. Lưu ý nếu
website chặn không cho phép thu thập dữ liệu, chương trình sẽ hiển thị thông
báo và cho phép người dùng nhập vào địa chỉ website khác.
3. Chương trình tự động lấy ra được danh sách các chủ đề nhỏ của website đó
và cho phép người dùng chọn.
4. Tổ chức thư mục lưu trữ dữ liệu hợp lý theo yêu cầu (tên website là tên thư
mục gốc, tiếp theo là các danh sách chủ đề). Mọi dữ liệu thu thập được sẽ lưu
vào file .TXT trong từng thư mục chủ đề cụ thể đã tạo. Ví dụ:
~\\BaoVnExpress\\GiaoDuc\GiaoDuc.txt
5. Tiến hành thực hiện các yêu cầu trên dữ liệu đã thu thập, kết quả sẽ được lưu
trữ tại thư mục cùng với thư mục dữ liệu gốc.
• Làm sạch dữ liệu (Clear)
• Tách câu (SentenceTokenize)

Đại học Khoa học Tự nhiên – Đại học Quốc gia TPHCM
Khoa CNTT – Môn: Khai thác dữ liệu web
• Tách từ (WordTokenize)
• Loại bỏ hư từ (Stopwords)
• Chuẩn hoá từ (StemmingAndLemmatization)

6. Cho phép người dùng chọn 1 trong 2 phương pháp để biểu diễn văn bản trong
mô hình không gian vector:
• Túi từ (Bag of Words)
• TF_IDF.

7. Tìm các văn bản liên quan nhau thông qua độ đo tương đồng Cosine Similarity
và so sánh kết quả với một độ đo tương đồng khác tuỳ chọn.
8. Thực hiện truy vấn văn bản và đánh giá hiệu quả dựa vào các độ đo Precision,
Recall và F-Score.

• Vẽ ma trận nhầm lẫn (confusion matrix)
• Tính toán các độ đo Precision, Recall, F-score
• Vẽ đồ thị biểu diễn các độ đo trên.
