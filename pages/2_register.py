import streamlit as st
import requests

#ẩn thanh bar mặc định của
st.markdown(
    """
    <style>
    /* Ẩn thanh menu mặc định Streamlit (Deploy, Settings, ... ) */
    header {visibility: hidden;}
    /* Ẩn footer "Made with Streamlit" */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

#icon của google
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

#page config
st.set_page_config(
    page_title="Register",
    layout="wide",
    initial_sidebar_state="expanded",
)

# xử lý trang
page = st.query_params.get("page", "register")

if page == "home":
    st.switch_page("Home.py")
elif page == "login":
    st.switch_page("pages/1_login.py")
elif page =="register":
    # HTML
    st.markdown("""
            <html>
            <body>
            <div class="navbar">
                <div class="navbar-left">
                    <span class="material-icons" style="vertical-align: middle;">help_outline</span>
                    <span style="font-size:22px; vertical-align: middle;">Hướng dẫn</span>
                </div>
                <div>
                    <a href="?page=home" target="_self">Trang chủ</a>
                    <a href="?page=login" target="_self">Đăng nhập</a>
                    <a href="?page=register" target="_self">Đăng ký</a>
                </div>
            </div>
            </body>
            </html>
    """, unsafe_allow_html=True
    )
    # CUSTOM CSS
    st.markdown("""
            <style>
            .stApp {
                font-family: 'Arial', sans-serif;
                background-color: white;
                color: black;
                font-size: 32px;
            }

            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #0078C2;
                color: white;
                padding: 10px 30px;
                font-weight: bold;
                position: fixed;
                top: 0;
                left: 0;
                width:100%;
                z-index:999;
            }
            .navbar a {
                color: white;
                text-decoration: none;
                margin-left: 25px;
            }

            .navbar-left {
                display: flex;
                align-items: center;
                gap: 10px;
            }


            /* Đảm bảo chiếm toàn màn hình */
            .stApp {
                height: 100vh;
                width: 100vw;
                overflow-x: hidden;
                overflow-y: auto;
            }

            </style>
            """
    , unsafe_allow_html=True)

    # CSS cho tất cả text_input, password_input và button
    st.markdown(
        """
        <style>
        /* Tất cả text_input và password_input */
        div.stTextInput>div>div>input {
            background-color: #f0f8ff !important;  /* nền sáng */
            color: #000000 !important;             /* chữ màu đen */
        }

        /* Button */
        div.stButton>button {
            background-color: #f0f8ff !important;  /* nền sáng */
            color: #000000 !important;             /* chữ màu đen */
            border: 1px solid #ccc !important;     /* viền nhẹ */
            border-radius: 8px !important;         /* bo tròn */
        }

        div.stTextInput>label {
        color: #000000 !important;             /* label màu đen */
        font-weight: bold;
        }
        div.stButton>button:hover {
            background-color: #e0f0ff !important;  /* nền sáng hơn khi hover */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Đăng ký tài khoản bệnh nhân")

    fullname = st.text_input("Họ và tên")
    gender = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])
    date_of_birth = st.date_input("Ngày sinh")
    phone = st.text_input("Số điện thoại")
    email = st.text_input("Email")

    st.markdown("---")

    #Thông tin tài khoản
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    confirm = st.text_input("Nhập lại mật khẩu", type="password")

    agree = st.checkbox("Tôi đồng ý với Điều khoản sử dụng")

    API_URL = "http://127.0.0.1:5000/api/auth/register"


    if st.button("Đăng ký"):
        if not agree:
            st.warning("⚠️ Vui lòng đồng ý với điều khoản trước khi đăng ký.")
        elif password != confirm:
            st.error("Mật khẩu nhập lại không khớp.")
        elif not (fullname and username and password and email):
            st.error("Vui lòng nhập đầy đủ thông tin.")
        else:
            # ⚠️ Backend chỉ nhận username + password nên chỉ gửi 2 trường này
            payload = {
                "username": username,
                "password": password,
                "full_name": fullname,
                "gender": gender,
                "date_of_birth": str(date_of_birth),
                "phone": phone,
                "email": email
            }

            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 201:
                    st.success("Đăng ký thành công! Bạn có thể đăng nhập ngay.")
                elif response.status_code == 409:
                    st.error("Tên tài khoản đã tồn tại, vui lòng chọn tên khác.")
                elif response.status_code == 400:
                    st.error("⚠Thiếu tên đăng nhập hoặc mật khẩu.")
                else:
                    st.error(f"Lỗi {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Không thể kết nối tới server. Hãy kiểm tra xem backend đã chạy chưa.")
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")
