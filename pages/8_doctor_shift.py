import streamlit as st
import calendar
from datetime import datetime, date
import requests

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
API_ME_URL = "http://127.0.0.1:5000/api/auth/me"

API_SHIFT_URL = "http://127.0.0.1:5000/api/shifts/"
API_DOCTOR_URL = "http://127.0.0.1:5000/api/doctors/"

# --------------------------
# 1 Lấy thông tin người dùng hiện tại
# --------------------------
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

# --------------------------
# 2 Lấy danh sách ca trực
# --------------------------
try:
    res_shifts = requests.get(API_SHIFT_URL, cookies=cookies)
    shifts = res_shifts.json() if res_shifts.status_code == 200 else []
except Exception as e:
    st.error(f"Không thể kết nối tới server ca trực: {e}")
    shifts = []

# --------------------------
# 3 Nếu là bác sĩ → lọc ca trực riêng
# --------------------------
if user_info and user_info.get("role") == "doctor":
    doctor_id = user_info.get("doctor_id")
    doctor_name = user_info.get("username", "Bác sĩ")

    if doctor_id:
        # 🔥 Lọc ca trực của bác sĩ hiện tại
        shifts = [s for s in shifts if s.get("doctor_id") == doctor_id]
    else:
        st.warning("Không tìm thấy Doctor ID trong dữ liệu người dùng.")

# --------------------------
# 4 Lấy danh sách bác sĩ (để hiển thị tên trong lịch)
# --------------------------
try:
    res_docs = requests.get(API_DOCTOR_URL, cookies=cookies)
    doctors_list = res_docs.json() if res_docs.status_code == 200 else []
except Exception as e:
    st.error(f"Không thể kết nối tới server danh sách bác sĩ: {e}")
    doctors_list = []

doctor_dict = {d["doctor_id"]: d["full_name"] for d in doctors_list}

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
page = st.query_params.get("page", "Doctor-shift")
session_token = st.session_state["cookies"].get("session", "")

if page == "Doctor-home":
    st.switch_page("pages/4_doctorhome.py")
elif page == "Doctor-appointment":
    st.switch_page("pages/9_doctor_appointment.py")
elif page == "Doctor-shift":
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
        </body>
        </html>
        """, unsafe_allow_html=True
    )
    # --------------------------
    # Hàm tạo HTML lịch tháng
    # --------------------------
    def generate_calendar_html(year, month, shifts):
        cal = calendar.Calendar(firstweekday=6)  # Chủ nhật là ngày đầu tuần
        month_days = cal.monthdayscalendar(year, month)

        html = '<table class="calendar">'
        # Header
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
                    day_shifts = [s for s in shifts if datetime.fromisoformat(s["shift_date"]).date() == day_date]
                    if day_shifts:
                        html += f'<td class="has-appointment">{day}<br>'
                        for s in day_shifts:
                            doctor_name = doctor_dict.get(s["doctor_id"], f"Doctor {s['doctor_id']}")
                            html += f"{s['start_time']}-{s['end_time']} {doctor_name} ({s.get('room', 'N/A')})<br>"
                        html += '</td>'
                    else:
                        html += f'<td>{day}</td>'
            html += '</tr>'
        html += '</table>'
        return html


    # --------------------------
    # Giao diện
    # --------------------------
    st.title("Lịch Ca Trực Bác Sĩ Theo Tháng")

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
        selected_month = st.selectbox("Chọn tháng", months, index=current_month - 1)
        selected_year = st.selectbox("Chọn năm", years, index=years.index(current_year))

    # Hiển thị lịch
    html_calendar = generate_calendar_html(selected_year, selected_month, shifts)
    st.markdown(html_calendar, unsafe_allow_html=True)

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
            background-color: #639fff;
            font-weight: bold;
            border: 2px solid #0062ff;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    if not shifts:
        st.info("Hiện chưa có ca trực nào được tạo.")