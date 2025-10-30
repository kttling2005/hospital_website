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
    page_title="login",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Đăng nhập")

# xử lý trang
page = st.query_params.get("page", "login")

if page == "home":
    st.switch_page("Home.py")
elif page == "register":
    st.switch_page("pages/2_register.py")
elif page =="login":
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

    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")

    API_URL = "http://127.0.0.1:5000/api/auth/login"

    if st.button("Đăng nhập"):
        if not username or not password:
            st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
        else:
            try:
                session_req = requests.Session()
                response = session_req.post(API_URL, json={
                    "username": username,
                    "password": password
                })

                if response.status_code == 200:
                    data = response.json()
                    cookies_dict = session_req.cookies.get_dict()

                    if cookies_dict:
                        # ✅ Lưu cookies + user vào session_state
                        st.session_state["cookies"] = cookies_dict
                        user_info = data.get("user", {})
                        st.session_state["user"] = user_info

                        # ✅ Lưu cookies vào query params để phục hồi sau reload
                        #st.query_params["session"] = cookies_dict.get("session")
                        st.session_state["session_cookie"] = cookies_dict.get("session")

                        st.success("🎉 Đăng nhập thành công!")

                        #chuyển hướng dựa theo role
                        role = user_info.get("role")
                        if not role:
                            st.error("❌ Không xác định được vai trò user.")
                        else:
                            st.success(f"🎉 Đăng nhập thành công với vai trò {role}!")

                            if role == "patient":
                                st.switch_page("pages/3_patienthome.py")
                            elif role == "doctor":
                                st.switch_page("pages/4_doctorhome.py")
                            elif role == "admin":
                                st.switch_page("pages/7_admin.py")
                            else:
                                st.warning("Vai trò chưa được định nghĩa, không chuyển trang.")

                    else:
                        st.error("🚫 Không nhận được cookie từ server.")

                elif response.status_code == 401:
                    st.error("❌ Sai tên đăng nhập hoặc mật khẩu.")
                elif response.status_code == 400:
                    st.error("⚠️ Thiếu thông tin đăng nhập.")
                else:
                    st.error(f"🚫 Lỗi {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Không thể kết nối tới server backend.")
