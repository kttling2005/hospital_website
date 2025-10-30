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

API_DOCTOR_URL = "http://127.0.0.1:5000/api/doctors/"
API_APPOINT_URL = "http://127.0.0.1:5000/api/appointments/"
API_PATIENT_URL = "http://127.0.0.1:5000/api/patients/"

#lấy tên bệnh nhân để hiện lên lịch khám
res_patients = requests.get(API_PATIENT_URL, cookies=cookies)
patients = res_patients.json() if res_patients.status_code == 200 else []
patient_dict = {p["patient_id"]: p["full_name"] for p in patients}


# --------------------------
# Lấy danh sách lịch hẹn của bác sĩ
# --------------------------
appointments = []
if cookies:
    try:
        res = requests.get(API_APPOINT_URL, cookies=cookies)
        if res.status_code == 200:
            appointments = res.json()
        elif res.status_code == 401:
            st.warning("⚠️ Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.")
            st.switch_page("1_login.py")  # hoặc st.experimental_set_query_params(page="login")
        else:
            st.error(f"Lỗi tải lịch hẹn: {res.status_code}")
    except Exception as e:
        st.error(f"Không thể kết nối API: {e}")
else:
    st.warning("Vui lòng đăng nhập để xem lịch hẹn.")
    st.switch_page("1_login.py")

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
page = st.query_params.get("page", "Doctor-appointment")
session_token = st.session_state["cookies"].get("session", "")

if page == "Doctor-home":
    st.switch_page("pages/4_doctorhome.py")
elif page == "Doctor-shift":
    st.switch_page("pages/8_doctor_shift.py")
elif page == "Doctor-appointment":
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
    def generate_calendar_html(year, month):
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
                    day_appts = [
                        a for a in appointments
                        if datetime.fromisoformat(a["appointment_date"]).date() == day_date
                    ]
                    if day_appts:
                        html += f'<td class="has-appointment">{day}<br>'
                        for a in day_appts:
                            time_str = datetime.fromisoformat(a["appointment_date"]).strftime("%H:%M")
                            patient_name = patient_dict.get(a["patient_id"], f"Patient {a['patient_id']}")  # nếu có tên bệnh nhân
                            status = a.get("status", "")
                            html += f"{time_str} - {patient_name} ({status})<br>"
                        html += '</td>'
                    else:
                        html += f'<td>{day}</td>'
            html += '</tr>'
        html += '</table>'
        return html


    # --------------------------
    # Giao diện
    # --------------------------
    st.title("Lịch Khám Bác Sĩ Theo Tháng")

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
    html_calendar = generate_calendar_html(selected_year, selected_month)
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
            background-color: #ffe0b2;
            font-weight: bold;
            border: 2px solid #ff9800;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --------------------------
    # Hiển thị danh sách lịch khám
    # --------------------------
    API_RECORD_URL = "http://127.0.0.1:5000/api/records/"
    st.title("Danh sách lịch khám tháng")

    if not appointments:
        st.info("Chưa có lịch khám nào.")
    else:
        # Sắp xếp theo ngày giờ
        appointments = sorted(appointments, key=lambda a: a["appointment_date"])

        for a in appointments:
            app_dt = datetime.fromisoformat(a["appointment_date"])
            date_str = app_dt.strftime("%d/%m/%Y")
            time_str = app_dt.strftime("%H:%M")
            patient_name = patient_dict.get(a["patient_id"], f"Patient {a['patient_id']}")
            reason = a.get("reason", "-")
            status = a.get("status", "")

            # CSS inline để hiện chữ mờ nếu đã hủy
            if status == "Hủy":
                st.markdown(
                    f"<span style='color:grey; text-decoration:line-through;'>**Ngày {date_str} | {time_str}** — Bệnh nhân: {patient_name} | Lý do: {reason} ({status})</span>",
                    unsafe_allow_html=True
                )
            elif status == "Đã đặt":
                st.markdown(
                    f"**Ngày {date_str} | {time_str}** — Bệnh nhân: {patient_name} | Lý do: {reason} ({status})",
                    unsafe_allow_html=True
                )
                with st.expander(f"Nhập kết quả khám cho {patient_name}"):
                    diagnosis = st.text_area(f"Chẩn đoán cho {patient_name}")
                    prescription = st.text_area("Đơn thuốc (nếu có)")
                    notes = st.text_area("Ghi chú thêm (nếu có)")

                    if st.button(f"Hoàn tất khám ({patient_name})", key=a["appointment_id"]):
                        payload = {
                            "appointment_id": a["appointment_id"],
                            "diagnosis": diagnosis,
                            "prescription": prescription,
                            "notes": notes
                        }
                        res = requests.post(API_RECORD_URL, json=payload, cookies=cookies)
                        if res.status_code == 201:
                            st.success("Tạo kết quả khám thành công!")
                            st.rerun()  # reload để cập nhật status "Đã khám"
                        else:
                            st.error(f"Lỗi: {res.json().get('message') or res.text}")

            else:
                st.markdown(
                    f"**Ngày {date_str} | {time_str}** — Bệnh nhân: {patient_name} | Lý do: {reason} ({status})",
                    unsafe_allow_html=True
                )