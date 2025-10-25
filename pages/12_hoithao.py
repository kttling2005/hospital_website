import streamlit as st
import pandas as pd
from datetime import date, timedelta

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
    page_title="Lịch họp hội thảo",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
page = st.query_params.get("page", "hoithao")

if page == "Doctor-shift":
    st.switch_page("pages/8_doctor_shift.py")
elif page == "Doctor-appointment":
    st.switch_page("pages/9_doctor_appointment.py")
elif page == "Doctor-home":
    st.switch_page("pages/4_doctorhome.py")
elif page == "hoithao":
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
            </style>
            """
    , unsafe_allow_html=True)

    st.title("Lịch họp chuyên môn & Hội thảo bác sĩ")
    st.markdown("#### Quản lý lịch theo từng khoa trong bệnh viện Mắt")

    # -----------------------------
    # Dữ liệu mẫu (tạm thời)
    # -----------------------------
    data = [
        {"department": "Glaucoma", "title": "Cập nhật kỹ thuật đo nhãn áp", "type": "Buổi học chuyên môn",
         "date": "2025-10-25", "time": "08:00 - 10:00", "location": "Phòng họp tầng 3", "presenter": "BS. Lê Minh An"},
        {"department": "Glaucoma", "title": "Hội thảo điều trị tăng nhãn áp", "type": "Hội thảo",
         "date": "2025-10-28", "time": "14:00 - 16:30", "location": "Hội trường lớn", "presenter": "PGS. TS. Nguyễn Văn A"},
        {"department": "Nhãn nhi", "title": "Cập nhật điều trị lác và nhược thị", "type": "Buổi học chuyên môn",
         "date": "2025-10-27", "time": "09:00 - 11:00", "location": "Phòng 204", "presenter": "BS. Trần Thu Hà"},
        {"department": "Phẫu thuật khúc xạ", "title": "Thực hành LASIK nâng cao", "type": "Workshop",
         "date": "2025-10-29", "time": "13:30 - 17:00", "location": "Phòng phẫu thuật 2", "presenter": "ThS. Phạm Đức Huy"},
        {"department": "Đáy mắt", "title": "Ca lâm sàng bệnh võng mạc tiểu đường", "type": "Buổi học chuyên môn",
         "date": "2025-10-26", "time": "10:00 - 12:00", "location": "Phòng họp tầng 2", "presenter": "BS. Nguyễn Thị Hòa"},
    ]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    # -----------------------------
    # Bộ lọc ngay trên giao diện
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_department = st.selectbox(
            "Chọn khoa",
            options=["Tất cả"] + sorted(df["department"].unique().tolist())
        )

    with col2:
        start_date = st.date_input("Từ ngày", value=date.today())

    with col3:
        end_date = st.date_input("Đến ngày", value=date.today() + timedelta(days=7))

    # -----------------------------
    # Lọc dữ liệu
    # -----------------------------
    filtered_df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]
    if selected_department != "Tất cả":
        filtered_df = filtered_df[filtered_df["department"] == selected_department]

    filtered_df = filtered_df.sort_values("date")

    # -----------------------------
    # Hiển thị bảng
    # -----------------------------
    st.markdown(f"### Lịch {selected_department if selected_department != 'Tất cả' else 'toàn viện'}")

    if filtered_df.empty:
        st.info("Không có buổi học hay hội thảo nào trong khoảng thời gian này.")
    else:
        display_df = filtered_df.copy()
        display_df["Ngày"] = display_df["date"].dt.strftime("%d/%m/%Y")
        display_df = display_df[["Ngày", "time", "department", "type", "title", "presenter", "location"]]
        display_df.columns = ["Ngày", "Giờ", "Khoa", "Loại", "Tên buổi học / Hội thảo", "Báo cáo viên", "Địa điểm"]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
