import os
from getpass import getpass
import pickle
from getpass import getpass
from PIL import ImageFont, ImageDraw
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import subprocess
import requests
from time import sleep
from urllib.parse import urlparse, parse_qs


def tam_ngung_den_khi(driver, xpath):
    """Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath"""
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                xpath,
            )
        ),
    )


def tam_ngung_va_tim(driver, xpath):
    """Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath và chọn xpath đó"""
    tam_ngung_den_khi(driver, xpath)
    return driver.find_element(by="xpath", value=xpath)


def chay_trinh_duyet(headless=True):
    """Mở trình duyệt và trả về driver"""
    options = Options()
    options.headless = headless
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(
        options=options,
        service=service,
    )


def dang_nhap_facebook(driver):
    """Hàm đăng nhập facebook"""
    url = "https://www.facebook.com/"
    # ten_dang_nhap = input("Nhập tên đăng nhập: ")
    # mat_khau = getpass(prompt="Nhập mật khẩu: ")
    ten_dang_nhap = input("Tên đăng nhập: ")
    mat_khau = getpass("Mật khẩu: ")

    # Mở trang
    driver.get(url)

    xpath_username = '//input[@id="email"]'
    xpath_password = '//input[@id="pass"]'
    xpath_login = '//button[@name="login"]'
    username = driver.find_element(by="xpath", value=xpath_username)
    username.send_keys(ten_dang_nhap)
    password = driver.find_element(by="xpath", value=xpath_password)
    password.send_keys(mat_khau)
    button = driver.find_element(by="xpath", value=xpath_login)
    button.click()
    return driver


def dang_nhap_bang_cookies(driver, duong_dan_tep_cookie):
    """Hàm đăng nhập facebook bằng cookies"""
    url = "https://www.facebook.com/"
    driver.get(url)
    with open(duong_dan_tep_cookie, "rb") as tep_cookie:
        for value in pickle.load(tep_cookie):
            if "expiry" in value:
                del value["expiry"]
            driver.add_cookie(value)

    # Tải lại trang để lấy cookies
    driver.get(url)
    return driver


def luu_cookies(driver, ten_tep_cookie=None):
    """Hàm lưu cookies trình duyệt"""
    if ten_tep_cookie is None:
        thu_muc_goc = os.getcwd()
        duong_dan_tep_cookie = build_cookies_file_name(driver, thu_muc_goc)
    else:
        # Nếu có tên thì lưu bằng tên được chỉ định
        duong_dan_tep_cookie = ten_tep_cookie

    # Lưu cookies
    with open(duong_dan_tep_cookie, "wb") as tep_tin:
        pickle.dump(driver.get_cookies(), tep_tin)
    return duong_dan_tep_cookie


# TODO Rename this here and in `luu_cookies`
def build_cookies_file_name(driver, thu_muc_goc):
    # Nếu không chỉ định tên thì lấy tên người dùng để lưu
    link_facebook_ca_nhan = "https://www.facebook.com/me"
    driver.get(link_facebook_ca_nhan)
    xpath_ten_nguoi_dung = (
        '//h1[@class="gmql0nx0 l94mrbxd p1ri9a11 ' 'lzcic4wl bp9cbjyn j83agx80"]'
    )
    ten_nguoi_dung = driver.find_element(by="xpath", value=xpath_ten_nguoi_dung).text
    ten_nguoi_dung = ten_nguoi_dung.split("\n")[0]
    return os.path.join(thu_muc_goc, f"{ten_nguoi_dung}.bak")


def resize_window(driver):
    driver.maximize_window()
    size = driver.get_window_size()
    driver.set_window_size(size["width"] / 2, size["height"])
    driver.set_window_position(
        (size["width"] / 2) + size["width"],
        0,
        windowHandle="current",
    )
    return driver


def send_invitation(
    driver, wedding_day, my_pronoun, friend_pronoun, friend_name, friend_id, web_link
):
    messenger_url = "https://www.facebook.com/messages/t"
    driver.get(f"{messenger_url}/{friend_id}")
    send_message(
        driver,
        f"{web_link}",
    )
    send_message(driver, f"{my_pronoun} chào {friend_pronoun} {friend_name}")

    send_message(
        driver,
        f"Ngày {wedding_day} tới {my_pronoun} có tổ chức hôn lễ, trân trọng kính mời "
        f"{friend_pronoun} cùng người thân tới chung vui cùng vợ chồng {my_pronoun}",
    )
    # send_message(
    #     driver,
    #     f"Đây là tin tự động, vì vậy nếu {friend_pronoun} có thể đến được thì trả "
    #     f"lời lại để {my_pronoun} sắp xếp đón tiếp nhé. Nếu {friend_pronoun} không thể "
    #     "đến, hãy cứ thoải mái bỏ qua tin nhắn này nhé",
    # )
    # send_message(
    #     driver,
    #     f"{friend_pronoun} nhận được tin nhắn này vì {friend_pronoun} là người đã từng"
    #     f" hoặc đang giúp đỡ {my_pronoun} rất nhiều. Nếu có lỡ làm phiền hoặc gây khó "
    #     f"chịu cho {friend_pronoun} thì xin bỏ qua cho {my_pronoun}. Và {my_pronoun} "
    #     f"cảm ơn {friend_pronoun} vì tất cả!",
    # )
    send_message(
        driver,
        f"Thông tin chi tiết mời {friend_pronoun} vào trang https://huutuananh.com/weddings"
        f"/true-love/tuan-anh-kim-oanh để xem và chúc phúc cho vợ chồng {my_pronoun} nhé",
    )


def send_message(driver, message):
    message_input = tam_ngung_va_tim(driver, '//div[@aria-label="Tin nhắn"]')
    for char in message:
        message_input.send_keys(char)
    sleep(7)
    message_input.send_keys(Keys.ENTER)


def create_invitation_img(
    invitation_path,
    invitation_img_path,
    coor,
    font_path,
    font_size,
    friend_pronoun,
    friend_name,
    friend_id,
    uid,
):
    text = f"{friend_pronoun} {friend_name}"
    file_name = f"{friend_id}-{uid}.png" if friend_id else f"{friend_name}-{uid}.png"
    local_output_img = os.path.join(invitation_path, file_name)
    rclone_output_path = os.path.join(
        "od_personal_appid:tuananh", "invitations", file_name
    )
    insert_text_to_image(
        invitation_img_path, text, coor, font_path, font_size, local_output_img
    )
    upload_to_rclone(local_output_img, rclone_output_path)
    os.remove(local_output_img)
    return get_rclone_link(rclone_output_path)


def insert_text_to_image(
    img_path,
    text,
    coor,
    font_path,
    font_size,
    img_out_path,
):
    font = ImageFont.truetype(font=font_path, size=font_size)
    image = Image.open(img_path)
    # Create an ImageDraw object onto which the font text will be placed
    draw = ImageDraw.Draw(im=image)
    # Draw the text onto our image
    draw.text(xy=coor, text=text, font=font, fill="black", anchor="mm")
    image.save(img_out_path)


def upload_to_rclone(img_path, rclone_path):
    cmd = ["rclone", "copyto", img_path, rclone_path]
    subprocess.call(cmd)


def get_rclone_link(rclone_path):
    return subprocess.check_output(
        [
            "rclone",
            "link",
            rclone_path,
            "--onedrive-link-scope",
            "anonymous",
            "--onedrive-link-type",
            "view",
        ],
        encoding="utf-8",
    )


def get_web_link_from_share_link(share_link):
    root_link = share_link.strip().rsplit("/", maxsplit=1)[0]
    print(root_link)
    res = requests.get(root_link, timeout=30)
    data = res.json()
    return data.get("webUrl", None), data.get("image", {})


def extract_share_link(web_link):
    response = requests.head(web_link, timeout=30)
    if redirect_link := response.headers.get("Location"):
        url_parser = urlparse(redirect_link)
        query_strings = parse_qs(url_parser.query)
        return query_strings.get("resId")[0], query_strings.get("authkey")[0]
    return None, None
