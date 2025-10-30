import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import requests

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
    page_title="Chấm công",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------
# Kiểm tra cookies
# --------------------------
if "cookies" not in st.session_state:
    if "session" in st.query_params:
        st.session_state["cookies"] = {"session": st.query_params["session"]}
    else:
        st.session_state["cookies"] = None

if not st.session_state["cookies"]:
    st.warning("⚠️ Bạn cần đăng nhập trước.")
    st.stop()

cookies = st.session_state["cookies"]

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
session_token = st.session_state["cookies"].get("session", "")

# xử lý trang
page = st.query_params.get("page", "chamcong")

if page == "Doctor-shift":
    st.switch_page("pages/8_doctor_shift.py")
elif page == "Doctor-appointment":
    st.switch_page("pages/9_doctor_appointment.py")
elif page == "Doctor-home":
    st.switch_page("pages/4_doctorhome.py")
elif page == "chamcong":
    # HTML Navbar
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
        </body>
        </html>
    """, unsafe_allow_html=True)

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

        /* Chevron */
        .chevron {
            font-size: 24px;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    ########
    API_ME_URL = "http://127.0.0.1:5000/api/auth/me"
    try:
        res_user = requests.get(API_ME_URL, cookies=cookies)
        if res_user.status_code == 200:
            user_info = res_user.json()
        else:
            user_info = None
            st.warning("Không lấy được thông tin người dùng.")
    except Exception as e:
        user_info = None
        st.error(f"Không kết nối được API người dùng: {e}")

    # if user_info:
    #     st.subheader("Thông tin người dùng hiện tại")
    #     st.json(user_info)  # In ra dữ liệu người dùng dạng JSON
    # else:
    #     st.warning("Không có thông tin người dùng để hiển thị")
    ########


    DOCTOR_NAME = user_info.get("full_name", " ")
    DOCTOR_ID = user_info.get("doctor_id", 1)  # cần có doctor_id để gọi API

    # --------------------------
    # Tiêu đề & chọn ngày
    # --------------------------
    st.title("Chấm công & Lịch làm việc")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### Bác sĩ: **{DOCTOR_NAME}**")
    with col2:
        selected_date = st.date_input("Chọn ngày", date.today())

    st.markdown("---")

    # --------------------------
    # Lấy lịch trực từ API
    # --------------------------
    API_SHIFT_URL = "http://127.0.0.1:5000/api/shifts/"
    try:
        resp = requests.get(API_SHIFT_URL, params={"doctor_id": DOCTOR_ID})
        if resp.status_code == 200:
            shifts = resp.json()
            df_schedule = pd.DataFrame(shifts)
            if not df_schedule.empty:
                df_schedule['shift_date'] = pd.to_datetime(df_schedule['shift_date']).dt.date
                df_schedule['start_time'] = pd.to_datetime(df_schedule['start_time']).dt.time
                df_schedule['end_time'] = pd.to_datetime(df_schedule['end_time']).dt.time
                filtered_df = df_schedule[df_schedule["shift_date"] == selected_date]
            else:
                filtered_df = pd.DataFrame()
        else:
            st.error(f"Lỗi khi lấy dữ liệu lịch trực: {resp.status_code}")
            filtered_df = pd.DataFrame()
    except Exception as e:
        st.error(f"Lỗi kết nối API: {e}")
        filtered_df = pd.DataFrame()

    # Hiển thị lịch
    st.subheader("Lịch làm việc trong ngày")
    if filtered_df.empty:
        st.info("Hôm nay bạn không có lịch làm việc.")
    else:
        st.dataframe(
            filtered_df[['shift_date', 'start_time', 'end_time', 'room']],
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")
    API_BASE = "http://127.0.0.1:5000/api/attendance"
    # --------------------------
    # Form chấm công
    # --------------------------
    # Khởi tạo session_state để lưu thời gian chấm công
    if "checkin_time" not in st.session_state:
        st.session_state.checkin_time = None
    if "checkout_time" not in st.session_state:
        st.session_state.checkout_time = None

    # Kiểm tra xem đã check-in/checkout từ backend chưa
    if st.session_state.checkin_time is None:
        res = requests.get(f"{API_BASE}/today_status", cookies=cookies)  # tạo route API để lấy status hôm nay
        if res.status_code == 200:
            data = res.json()
            st.session_state.checkin_time = data.get("check_in_time")
            st.session_state.checkout_time = data.get("check_out_time")

    # Xác định trạng thái nút
    button_disabled = st.session_state.checkout_time is not None

    #form chấm công
    with st.form("attendance_form"):
        st.write("Nhấn nút để chấm công:")

        # Disable nút dựa trên trạng thái
        button_disabled = st.session_state.checkout_time is not None

        submit_btn = st.form_submit_button("Chấm công", disabled=button_disabled)

        if submit_btn:
            if st.session_state.checkin_time is None:
                # Gọi API check-in
                res = requests.post(f"{API_BASE}/checkin", cookies=cookies)
                if res.status_code == 201:
                    st.session_state.checkin_time = res.json()["check_in_time"]
                    st.success(f"Check-in thành công lúc {st.session_state.checkin_time}")
                else:
                    st.error(res.json().get("message", "Check-in lỗi"))
            elif st.session_state.checkout_time is None:
                # Gọi API check-out
                res = requests.put(f"{API_BASE}/checkout", cookies=cookies)
                if res.status_code == 200:
                    st.session_state.checkout_time = res.json()["check_out_time"]
                    st.success(f"Check-out thành công lúc {st.session_state.checkout_time}")
                else:
                    st.error(res.json().get("message", "Check-out lỗi"))
            else:
                st.info("Bạn đã hoàn tất chấm công hôm nay.")

    # --------------------------
    # Hiển thị giờ chấm công hiện tại
    # --------------------------
    if st.session_state.checkin_time:
        st.write("Check-in:", st.session_state.checkin_time)
    if st.session_state.checkout_time:
        st.write("Check-out:", st.session_state.checkout_time)

    st.markdown("---")

    # --------------------------
    # Thống kê nhanh
    # --------------------------
    with st.expander("📊 Thống kê nhanh"):
        total_shifts = len(df_schedule) if not df_schedule.empty else 0
        upcoming = len(df_schedule[df_schedule["shift_date"] >= date.today()]) if not df_schedule.empty else 0
        st.metric("Tổng ca trong tuần", total_shifts)
        st.metric("Ca sắp tới", upcoming)

    st.caption("Bệnh viện BrightEyes — Hệ thống chấm công bác sĩ © 2025")
