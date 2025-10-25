import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date
import requests

# ✅ Kiểm tra cookies từ session_state hoặc query_params
if "cookies" not in st.session_state:
    if "session" in st.query_params:
        st.session_state["cookies"] = {"session": st.query_params["session"]}
    else:
        st.session_state["cookies"] = None

if not st.session_state["cookies"]:
    st.warning("⚠️ Bạn cần đăng nhập trước.")
    st.switch_page("pages/1_login.py")
    st.stop()

cookies = st.session_state["cookies"]

API_URL = "http://127.0.0.1:5000/api/appointments/"
response = requests.get(API_URL, cookies=cookies)

appointments = []

if response.status_code == 200:
    appointments = response.json()
else:
    st.error(f"Lỗi tải dữ liệu: {response.status_code}")
#lay ten bac si tu id bac si(tai backend ko có api doctor)
API_DOCTOR_URL = "http://127.0.0.1:5000/api/doctors/"
response = requests.get(API_DOCTOR_URL, cookies=cookies)

if response.status_code == 200:
    doctors_list = response.json()
else:
    st.error(f"Lỗi tải danh sách bác sĩ: {response.status_code}")
    doctor_dict = {}

# Tạo mapping: doctor_id → full_name
doctor_dict = {d["doctor_id"]: d["full_name"] for d in doctors_list}
# --------------------------
# PARSE NGÀY GIỜ
# --------------------------
for a in appointments:
    dt = datetime.fromisoformat(a["appointment_date"])
    a["date"] = dt.date()
    a["time"] = dt.strftime("%H:%M")
    if "doctor" not in a:
        a["doctor"] = doctor_dict.get(a["doctor_id"], f"Doctor {a['doctor_id']}")
# --------------------------
# CẤU HÌNH GIAO DIỆN CƠ BẢN
# --------------------------
st.set_page_config(
    page_title="Patient-Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ẩn thanh menu mặc định của Streamlit
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

# --------------------------
# XỬ LÝ ĐIỀU HƯỚNG TRANG
# --------------------------
session_token = st.session_state["cookies"].get("session", "")
page = st.query_params.get("page", "patient_appointment")

if page == "patienthome":
    st.switch_page("pages/3_patienthome.py")

elif page == "patient_appointment":
    # --------------------------
    # NAVBAR
    # --------------------------
    st.markdown(f"""
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
                </div>
                <a href="?logout=1" class="navbar-logout" target="_self">Đăng xuất</a>  
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --------------------------
    # HÀM TẠO HTML LỊCH THÁNG
    # --------------------------
    def generate_calendar_html(year, month, appointments):
        cal = calendar.Calendar(firstweekday=6)  # Chủ nhật là ngày đầu tuần
        month_days = cal.monthdayscalendar(year, month)

        html = '<table class="calendar">'
        # Header ngày
        html += '<tr>'
        for day_name in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            html += f'<th>{day_name}</th>'
        html += '</tr>'

        for week in month_days:
            html += '<tr>'
            for day in week:
                if day == 0:
                    html += '<td></td>'
                else:
                    day_date = date(year, month, day)
                    # Kiểm tra ngày có lịch không
                    day_appointments = [a for a in appointments if a["date"] == day_date]
                    if day_appointments:
                        html += f'<td class="has-appointment">{day}<br>'
                        for a in day_appointments:
                            html += f'{a["time"]} {a["doctor"]}<br>'
                        html += '</td>'
                    else:
                        html += f'<td>{day}</td>'
            html += '</tr>'
        html += '</table>'
        return html

    # --------------------------
    # GIAO DIỆN TRANG LỊCH KHÁM
    # --------------------------
    st.set_page_config(page_title="Lịch khám bệnh", layout="centered")
    st.title("Lịch khám bệnh của bạn")

    # CSS Custom
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
    .calendar {
        border-collapse: collapse;
        width: 100%;
        max-width: 1200px;
    }
    .calendar th, .calendar td {
        border: 1px solid #ccc;
        padding: 12px;
        text-align: center;
        vertical-align: top;
        width: 150px;
        height: 100px;
    }
    .calendar th {
        background-color: #f2f2f2;
    }
    .calendar .has-appointment {
        background-color: #ffe0b2;
        font-weight: bold;
        border: 2px solid #ff9800;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------
    # CHỌN THÁNG / NĂM
    # --------------------------
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    exp = st.expander(f"Chọn tháng/năm", expanded=False)
    with exp:
        months = list(range(1, 13))
        years = list(range(2023, 2031))
        selected_month = st.selectbox("Chọn tháng", months, index=current_month-1)
        selected_year = st.selectbox("Chọn năm", years, index=years.index(current_year))

    # --------------------------
    # HIỂN THỊ LỊCH
    # --------------------------
    html_calendar = generate_calendar_html(selected_year, selected_month, appointments)
    st.markdown(html_calendar, unsafe_allow_html=True)

    # --------------------------
    # HIỂN THỊ CHI TIẾT LỊCH
    # --------------------------
    st.subheader("Chi tiết các lịch khám")
    appointments_by_day = {}
    for a in appointments:
        if a["date"].month == selected_month and a["date"].year == selected_year:
            appointments_by_day.setdefault(a["date"], []).append(f"{a['time']} {a['doctor']}")

    if appointments_by_day:
        for d in sorted(appointments_by_day):
            st.markdown(f"**{d.strftime('%d/%m/%Y')}**")
            for item in appointments_by_day[d]:
                st.markdown(f"- {item}")
    else:
        st.info("Không có lịch khám trong tháng này.")
