import streamlit as st
from typing import List, Dict
import requests
from datetime import datetime

st.set_page_config(page_title="Danh sách bác sĩ - chuyên gia", layout="wide")

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
page = st.query_params.get("page", "appointment_register")

if page == "patient_appointment":
    st.switch_page("pages/6_patient_appointment.py")

if page == "patienthome":
    st.switch_page("pages/3_patienthome.py")
elif page=="appointment_register":
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
                <a href="?logout=1" target="_self" style="font-size">Đăng xuất</a>  
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

    """, unsafe_allow_html=True)


    # -----------------------------
    # Sample data (thay bằng API hoặc DB khi cần)
    # -----------------------------
    doctor_images = {
        1: "https://cdn.pixabay.com/photo/2017/01/29/21/16/nurse-2019420_1280.jpg",
        4: "https://cdn.pixabay.com/photo/2023/03/09/07/21/spine-surgeon-7839395_1280.jpg",
        5: "https://cdn.pixabay.com/photo/2017/05/23/17/12/doctor-2337835_1280.jpg",
        9: "https://cdn.pixabay.com/photo/2016/02/10/13/03/dentist-1191671_1280.jpg",
        11: "https://cdn.pixabay.com/photo/2017/09/06/20/36/doctor-2722941_1280.jpg",
        12: "https://cdn.pixabay.com/photo/2017/07/23/10/43/dentist-2530988_1280.jpg",
        13: "https://i.pinimg.com/736x/0e/4a/11/0e4a111c994200dc7b68d4c210fd659b.jpg",
        14: "https://i.pinimg.com/736x/0e/4a/11/0e4a111c994200dc7b68d4c210fd659b.jpg0",
        15: "https://i.pinimg.com/736x/0e/4a/11/0e4a111c994200dc7b68d4c210fd659b.jpg",
        16: "https://i.pinimg.com/736x/0e/4a/11/0e4a111c994200dc7b68d4c210fd659b.jpg"
    }

    API_URL = "http://127.0.0.1:5000/api/doctors/"
    API_APT = "http://127.0.0.1:5000/api/appointments/"
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            DOCTORS = response.json()
        else:
            st.error(f"Không thể tải danh sách bác sĩ (mã lỗi {response.status_code})")
            DOCTORS = []
    except Exception as e:
        st.error(f"Lỗi khi gọi API: {e}")
        DOCTORS = []

    # -----------------------------
    # Styling (card-like)
    # -----------------------------
    CARD_STYLE = """
    <style>
    .doctor-card{ 
      border:1px solid #e6e6e6; 
      border-radius:12px; 
      padding:12px; 
      margin-bottom:12px; 
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .doc-name{ font-weight:600; font-size:16px; }
    .doc-role{ color:#555; margin-bottom:6px; }
    .small-muted{ color:#777; font-size:13px; }
    </style>
    """

    st.markdown(CARD_STYLE, unsafe_allow_html=True)

    # -----------------------------
    # Header + Filters
    # -----------------------------
    st.title("Danh sách bác sĩ - chuyên gia")
    col1, col2 = st.columns([1, 1])

    with col1:
        q = st.text_input("Tìm theo tên hoặc chuyên khoa", value="")
    with col2:
        depts = ["Tất cả"] + sorted({d["specialization"] for d in DOCTORS})
        selected_dept = st.selectbox("Chọn khoa", depts)

    # -----------------------------
    # Filter & Search logic
    # -----------------------------
    filtered = []
    for d in DOCTORS:
        if q.strip():
            if q.lower() not in d["full_name"].lower() and q.lower() not in d["specialization"].lower():
                continue
        if selected_dept != "Tất cả" and d["specialization"] != selected_dept:
            continue
        filtered.append(d)

    # Pagination
    if "page" not in st.session_state:
        st.session_state.page = 1

    total = len(filtered)


    # -----------------------------
    # Render doctor cards in a responsive grid
    # -----------------------------
    visible = filtered
    if not visible:
        st.info("Không có bác sĩ nào khớp với tìm kiếm.")
    else:
        cols = st.columns(2)
        for i, doc in enumerate(visible):
            col = cols[i % 2]
            with col:
                key_suffix = f"{doc['doctor_id']}_{i}"
                st.markdown(
                    f"""
                    <div style="text-align:center;">
                        <img src="{doctor_images[doc['doctor_id']]}" alt="Bác sĩ {doc['full_name']}"
                             style="width:500px;height:380px;object-fit:cover;
                                    border-radius:10px;border:1px solid #eee;display:block;margin:auto;"/>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(f"<div class='doc-name'>{doc['full_name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='doc-role'>Chuyên ngành: {doc['specialization']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='small-muted'>Giới tính: {doc['gender']} | {doc['phone']}</div>", unsafe_allow_html=True)

                # Đặt form nhỏ cho nút đăng ký để thu thập info người dùng & giờ khám
                with st.form(key=f"reg_form_{key_suffix}"):
                    appointment_date = st.date_input("Ngày hẹn", key=f"date_{key_suffix}")
                    appointment_time = st.time_input("Giờ hẹn", key=f"time_{key_suffix}")
                    reason = st.text_area("Lý do khám", key=f"reason_{key_suffix}",
                                          placeholder="VD: Khám lại định kỳ, mỏi mắt, v.v.")
                    submitted = st.form_submit_button("Đặt lịch khám", use_container_width=True)

                    if submitted:
                        # Kết hợp ngày & giờ
                        appointment_dt = datetime.combine(appointment_date, appointment_time).isoformat()
                        payload = {
                            "doctor_id": doc["doctor_id"],
                            "appointment_date": appointment_dt,
                            "reason": reason
                        }

                        try:
                            response = requests.post(
                                API_APT,
                                json=payload,
                                cookies=st.session_state["cookies"]  # gửi session cookie để xác thực
                            )
                            if response.status_code == 201:
                                st.success(" Đặt lịch hẹn thành công!")
                            else:
                                msg = response.json().get("message", response.text)
                                st.error(f" {msg}")
                        except Exception as e:
                            st.error(f" Không thể kết nối đến server: {e}")

                st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .main {
        padding-top: 100px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    # -----------------------------
    # Tips / Footer
    # -----------------------------
