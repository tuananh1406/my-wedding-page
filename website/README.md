# Website đám cưới của mình
- Sử dụng django
- [Xem demo](https://huutuananh.com/weddings/true-love/tuan-anh-kim-oanh)
# Chuẩn bị:
- 1 link youtube video đám cưới
- 1 ảnh dùng để hiện thị khi share trên fb hoặc mxh khác
- 1 ảnh avatar chú rể, cô dâu, bố mẹ 2 bên
- 2 ảnh logo, cắt hình tròn, kích thước 200x200 và 100x100
- 2 ảnh slide (có thể nhiều hơn)
- 2 ảnh QR code của cô dâu, chú rể tạo ở VietQR (https://my.vietqr.io/login)
- Ảnh album (tùy ý)
# Cài đặt
- Clone repo
- cd vào thư mục website
- Cài pipenv: python -m pip install pipenv
- Cài đặt: pipenv install
- Migrate data: PIPENV_DOTENV_LOCATION=local.env pipenv run python manage.py migrate
- Tạo tài khoản admin: PIPENV_DOTENV_LOCATION=local.env pipenv run python manage.py createsuperuser
- Chạy server: PIPENV_DOTENV_LOCATION=local.env pipenv run python manage.py runserver
# Tạo đám cưới mới
- Vào trang admin django (http://localhost:8000/admin/)
- Chọn "Mối quan hệ"
    - Ấn thêm vào, cần 1 mqh có mã là "BM" tức bố mẹ, tên tùy ý
- Chọn "Người tham gia"
    - Thêm lần lượt cô dâu, chú rể. Chỉ cần thêm các trường in đậm.
    - Thêm bố mẹ 2 bên tương tự, lúc chọn mối quan hệ là bố mẹ như ở trên
- Chọn "Lễ cưới"
    - Thêm mới 1 lễ cưới theo các thông tin đã chuẩn bị. Lưu ý: ảnh xem trước khi chia sẻ là ảnh hiển thị khi đăng link lên facebook
    - Logo: ảnh logo 200x200, Logo SM: ảnh logo 100x100
- Chọn "Thông tin mừng cưới"
    - Mã QR: Ảnh QR tạo từ VietQR
    - Ảnh nền: Chọn ảnh nền mới
    - Ảnh logo: Chọn ảnh logo, không cần thì có thể bỏ qua
    - Ấn lưu lại, ảnh QR mới và QR có logo sẽ tự sinh
- Vào lại "Người tham gia"
    - Cập nhật thông tin mừng cưới cho cô dâu, chú rể
    - Chọn cô dâu (chú rể)
    - Thông tin mừng cưới chọn tương ứng
    - Ấn lưu lại
- Chọn "Chuyện tình yêu"
    - Thêm chuyện tình yêu tương ứng
- Chọn "Ngày trọng đại"
    - Thêm ngày trọng đại tương ứng
- Sau khi thêm xong, quay lại "Lễ cưới". Chọn vào lễ cưới mới tạo, xem tên rút gọn.
    - Thay tên rút gọn vào ten-rut-gon ở link sau để xem: http://localhost:8000/weddings/true-love/ten-rut-gon
- Chỉnh sửa lại ảnh hiển thị cho đep là xong

# Cách xóa hết tạo lại
- Xóa file db.sqlite3
- Chạy lại lệnh migrate
- Tạo lại admin user
- Run server và setup lại
