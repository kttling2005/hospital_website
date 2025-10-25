import streamlit as st
from datetime import date

st.set_page_config(page_title="Trang bệnh nhân", layout="wide")

# -----------------------------
# ✅ Phục hồi cookies nếu session_state mất
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
# ✅ Dữ liệu người dùng
# -----------------------------
user = st.session_state.get("user", {})
username = user.get("username", "Bệnh nhân")

# -------------------------------
# CẤU HÌNH PAGE
# -------------------------------
st.set_page_config(
    page_title="Patient-Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ẩn thanh bar mặc định của Streamlit
st.markdown(
    """
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Icon của Google
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)


session_token = st.session_state["cookies"].get("session", "")
# -------------------------------
# XỬ LÝ ĐIỀU HƯỚNG
# -------------------------------
page = st.query_params.get("page", "patienthome")

if page == "patient_appointment":
    st.switch_page("pages/6_patient_appointment.py")

if page == "appointment_register":
    st.switch_page("pages/5_appointment_register.py")

if page == "brighteyes_10years":
    st.switch_page("pages/10_brighteyes_10years.py")

elif page == "patienthome":
    #HTML
    st.markdown(f"""
    <html>
    <body>
    <div class="navbar">
        <div class="navbar-left">
            <span class="material-icons" style="vertical-align: middle;">help_outline</span>
            <span style="font-size:22px; vertical-align: middle;">Hướng dẫn</span>
        </div>
        <div class="navbar-right">
            <a href="?page=patienthome&session={session_token}" target="_self">Trang chủ</a>
            <a href="?page=patient_appointment&session={session_token}" target="_self">Lịch khám</a>
            <!-- Profile -->
            <div class="profile-dropdown">
                <div class="profile-avatar">
                    <img src="https://i.pinimg.com/1200x/ea/96/48/ea96485daff64bc586ffcc6db5a09490.jpg" alt="avatar">
                </div>
                <span class="material-icons chevron">expand_more</span>
                <span style="font-size:18px;">{username}</span>
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
            <a href="?page=appointment_register&session={session_token}" target="_self">
                <span class="material-icons" style="font-size:48px; color:white;">calendar_today</span>
                <div class="box-title">Đăng ký khám bệnh trực tuyến</div>
            </a>
        </div>
        <div class="box2" onclick="window.location.href='?page=doctor_intro'">
            <a href="?page=brighteyes_10years&session={session_token}" target="_self">
                <span class="material-icons" style="font-size:48px; color: white;">person</span>
                <div class="box-title">Hành trình 10 năm cùng BrightEyes</div>
            </a>
        </div>
    </div>
    </body>
    </html>
    """, unsafe_allow_html=True)
    # -------------------------------
    # CSS TÙY CHỈNH
    # -------------------------------
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

    .profile-dropdown {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
    }

    .profile-avatar {
        width: 40px;
        height: 40px;
        border: 2px solid white;
        border-radius: 50%;
        overflow: hidden;
    }

    .profile-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
    }

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

    .address {
        font-size: 18px;
        color: black;
    }

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

    .boxes-container {
        display: flex;
        justify-content: center;
        gap: 100px;
        padding: 40px;
        color: white;
        margin-top: -80px;
        z-index: 10;
        position: relative;
    }

    .box1 {
        background-color: #27A49E;
        flex: 1;
        max-width: 300px;
        height:180px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s ease;
    }

    .box1:hover {
        transform: scale(1.05);
        background-color: #24948F;
    }

    .box2 {
        background-color: #2C7E2F;
        flex: 1;
        max-width: 300px;
        height:180px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        text-align: center;
        transition: transform 0.2s ease;
    }

    .box2:hover {
        transform: scale(1.05);
        background-color: #276D29;
    }

    .box-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        color: #FFFFFF;
    }

    html, body, [data-testid="stAppViewContainer"], .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }

    .stApp {
        height: 100vh;
        width: 100vw;
        overflow-x: hidden;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

