import streamlit as st
from streamlit_navigation_bar import st_navbar
from datetime import date

# ẩn thanh bar mặc định của
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
# icon của google
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

# page config
st.set_page_config(
    page_title="Doctor-Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Phục hồi cookies nếu session_state mất
# -----------------------------
if "cookies" not in st.session_state:
    if "session" in st.query_params:
        st.session_state["cookies"] = {"session": st.query_params["session"]}
    else:
        st.session_state["cookies"] = None

if not st.session_state["cookies"]:
    st.warning("⚠️ Bạn cần đăng nhập trước.")
    st.switch_page("pages/1_login.py")
    st.stop()
# -----------------------------
# Dữ liệu người dùng
# -----------------------------
user = st.session_state.get("user", {})
username = user.get("username", "Bệnh nhân")
session_token = st.session_state["cookies"].get("session", "")

# xử lý trang
page = st.query_params.get("page", "Doctor-home")

if page == "Doctor-shift":
    st.switch_page("pages/8_doctor_shift.py")

elif page == "Doctor-appointment":
    st.switch_page("pages/9_doctor_appointment.py")

if page == "chamcong":
    st.switch_page("pages/11_chamcong.py")

if page == "hoithao":
    st.switch_page("pages/12_hoithao.py")

elif page == "Doctor-home":
    # HTML
    st.markdown(f"""
    <html>
    <body>
    <div class="navbar">
        <div class="navbar-left">
            <span class="material-icons" style="vertical-align: middle;">help_outline</span>
            <span style="font-size:22px; vertical-align: middle;">Hướng dẫn</span>
        </div>
        <div class="navbar-right">
            <a href="?page=Doctor-home&session={session_token}" target="_self">Trang chủ</a>
            <a href="?page=Doctor-shift&session={session_token}" target="_self">Lịch Trực</a>
            <a href="?page=Doctor-appointment&session={session_token}" target="_self">Lịch khám</a>
            <!-- Profile -->
            <div class="profile-dropdown">
                <div class="profile-avatar">
                    <img src="https://i.pinimg.com/736x/67/5f/83/675f834f14724a3708bbf7ea781c7157.jpg" alt="avatar">
                </div>
                <span class="material-icons chevron">expand_more</span>
            </div>
            <a href="?logout=1" class="navbar-logout" target="_self">Đăng xuất</a>
        </div>
    </div>

    <div class="logo-section">
        <div>
            <div class="logo-text">BrightEyes</div>
            <div class="logo-sub">Phòng khám mắt tiêu chuẩn quốc gia</div>
        </div>
        <div class="address"><span class="material-icons" style="vertical-align: middle;">location_on</span>
        Số 1, đường Lê Lợi, phường Minh Khai, thành phố Huế</div>
    </div>

    <div class="hospital-image">
        <img src="https://benhvienmat.vn/upload_images/images/old/2023/05/NTL_6039-1024x683.jpg" alt="hospital_image">
    </div>

    <div class="boxes-container">
        <div class="box1">
            <a href="?page=chamcong&session={session_token}" target="_self">
                <span class="material-icons" style="font-size:48px; color:white;">calendar_today</span>
                <div class="box-title">Chấm công</div>
            </a>
        </div>
        <div class="box2" onclick="window.location.href='?page=doctor_intro'">
            <a href="?page=hoithao&session={session_token}" target="_self">
                <span class="material-icons" style="font-size:48px; color: white;">person</span>
                <div class="box-title">Lịch họp chuyên môn, hội thảo</div>
            </a>
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

    .navbar-right {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    /* Profile container */
    .profile-dropdown {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
    }

    /* Avatar với border/elip */
    .profile-avatar {
        width: 40px;
        height: 40px;
        border: 2px solid white; /* viền elip */
        border-radius: 50%;
        overflow: hidden;
    }

    .profile-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
    }

    /* Chevron */
    .chevron {
        font-size: 24px;
        color: white;
    }

    .logo-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        background: white;
        padding: 40px 40px 35px 40px;
    }

    .logo-text {
        color: #006699;
        font-weight: 800;
        font-size: 55px;
    }

    .logo-sub {
        font-size: 16px;
        color: #333;
    }

    /* Địa chỉ */
    .address {
        font-size: 18px;
        color: black;
    }

    /* Ảnh bệnh viện */
    .hospital-image {
        background-color: #e0e0e0;
        position: relative;
        width: 100%;
        overflow: hidden;
        height: 390px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #888;
        font-size: 28px;
        font-weight: 600;
    }

    .hospital-image img{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Container chứa 2 box ngang hàng */
    .boxes-container {
        display: flex;
        justify-content: center;
        gap: 100px;
        padding: 40px;
        color: white;
        /* Nổi lên đè lên ảnh bệnh viện */
        margin-top: -80px; /* đè lên 20px */
        z-index: 10;
        position: relative;
    }

    /* Box */
    .box1 {
        background-color: #27A49E;
        flex: 1;
        max-width: 300px;
        height:180px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        text-align: center;
    }

    .box2 {
        background-color: #2C7E2F;
        flex: 1;
        max-width: 300px;
        height:180px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        text-align: center;
    }

    /* Tiêu đề box */
    .box-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        color: #FFFFFF;
    }


    /* Loại bỏ toàn bộ padding/margin mặc định của Streamlit */
    html, body, [data-testid="stAppViewContainer"], .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
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