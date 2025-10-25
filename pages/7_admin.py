import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000"  # backend của bạn

st.title("Admin Dashboard - Bệnh Viện")

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
session_token = st.session_state["cookies"].get("session", "")
# -------------------- Tabs --------------------
tab1, tab2 = st.tabs(["Quản Lý Bác Sĩ", "Quản Lý Lịch Trực"])

# -------------------- Tab 1: Quản Lý Bác Sĩ --------------------
with tab1:
    st.header("Danh Sách Bác Sĩ")

    try:
        res = requests.get(f"{API_BASE}/api/doctors/")
        doctors = res.json()
    except:
        st.error("Không thể kết nối tới server!")
        doctors = []

    for doc in doctors:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{doc['full_name']} - ID: {doc['doctor_id']} - Chuyên khoa: {doc.get('specialization', '')}")
        with col2:
            if st.button(f"Xoá", key=f"del_doc_{doc['doctor_id']}"):
                try:
                    del_res = requests.delete(f"{API_BASE}/api/doctors/{doc['doctor_id']}")

                    # Xử lý an toàn
                    msg = ""
                    try:
                        # Nếu backend trả JSON
                        msg = del_res.json().get('message', '')
                    except ValueError:
                        # Nếu backend trả text rỗng hoặc HTML
                        msg = del_res.text.strip()

                    if del_res.status_code == 200:
                        st.success(f"Đã xoá bác sĩ {doc['full_name']} - {msg}")
                        st.experimental_rerun()
                    elif del_res.status_code == 404:
                        st.error(f"Bác sĩ không tồn tại hoặc đã bị xoá. {msg}")
                    else:
                        st.error(f"Xoá thất bại (status {del_res.status_code}): {msg or 'Không có thông tin'}")
                except Exception as e:
                    st.error(f"Lỗi khi xoá: {str(e)}")

    st.subheader("Thêm Bác sĩ Mới")

    with st.form("add_doctor_form"):
        full_name = st.text_input("Họ và tên *")
        gender = st.selectbox("Giới tính *", ["Nam", "Nữ", "Khác"])
        specialization = st.text_input("Chuyên khoa *")
        email = st.text_input("Email")
        phone = st.text_input("Số điện thoại")

        st.markdown("---")
        st.subheader("Tài khoản đăng nhập")
        username = st.text_input("Tên đăng nhập *")
        password = st.text_input("Mật khẩu *", type="password")

        submitted = st.form_submit_button("Tạo tài khoản & hồ sơ bác sĩ")

    if submitted:
        if not all([full_name, gender, specialization, username, password]):
            st.warning("Vui lòng nhập đầy đủ các trường bắt buộc (*)")
        else:
            data = {
                "username": username,
                "password": password,
                "full_name": full_name,
                "gender": gender,
                "specialization": specialization,
                "email": email,
                "phone": phone
            }

            try:
                res = requests.post(
                    f"{API_BASE}/api/admin/create_doctor",
                    json=data,
                    cookies={"session": session_token}
                )
                if res.status_code == 201:
                    info = res.json()
                    st.success(f"✅ {info['message']} (Bác sĩ ID: {info['doctor_id']}, User ID: {info['user_id']})")
                    st.experimental_rerun()
                elif res.status_code == 409:
                    st.warning(res.json().get("message", "Tên tài khoản đã tồn tại"))
                else:
                    st.error(f"⚠️ Lỗi: {res.text}")
            except Exception as e:
                st.error(f"🚨 Không thể kết nối tới server: {e}")

# -------------------- Tab 2: Quản Lý Lịch Trực --------------------
with tab2:
    st.header("Danh sách ca trực")

    doctor_filter = st.number_input("Lọc theo ID bác sĩ (0 = tất cả)", min_value=0, step=1)
    params = {}
    if doctor_filter != 0:
        params['doctor_id'] = doctor_filter

    try:
        res = requests.get(f"{API_BASE}/api/shifts/", params=params)
        if res.status_code == 200:
            shifts = res.json()
            if shifts:
                for s in shifts:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"ID ca trực: {s['shift_id']}, ID Bác sĩ: {s['doctor_id']}, "
                                 f"Ngày: {s['shift_date']}, {s['start_time']} – {s['end_time']}, "
                                 f"Phòng: {s.get('room', '')}")
                    with col2:
                        if st.button("Xóa", key=f"del_shift_{s['shift_id']}"):
                            try:
                                del_res = requests.delete(
                                    f"{API_BASE}/api/shifts/{s['shift_id']}",
                                    cookies={"session": session_token}
                                )
                                if del_res.status_code == 200:
                                    st.success(f"Đã xóa ca trực ID {s['shift_id']}")
                                    st.experimental_rerun()  # reload lại danh sách
                                else:
                                    msg = ""
                                    try:
                                        msg = del_res.json().get("message", "")
                                    except ValueError:
                                        msg = del_res.text
                                    st.error(f"Xóa thất bại: {msg}")
                            except Exception as e:
                                st.error(f"Lỗi khi xóa ca trực: {e}")
            else:
                st.info("Chưa có ca trực nào.")
        else:
            st.error("Lỗi khi lấy dữ liệu ca trực")
    except Exception as e:
        st.error(f"❌ Không kết nối được server: {e}")

    #thêm ca trực
    st.header("Thêm ca trực mới")

    with st.form("create_shift_form"):
        doctor_id = st.number_input("ID bác sĩ", min_value=1, step=1)
        shift_date = st.date_input("Ngày trực")
        start_time = st.time_input("Giờ bắt đầu")
        end_time = st.time_input("Giờ kết thúc")
        room = st.text_input("Phòng trực (tùy chọn)")

        submitted = st.form_submit_button("Tạo ca trực")
        if submitted:
            payload = {
                "doctor_id": doctor_id,
                "shift_date": shift_date.isoformat(),
                "start_time": start_time.strftime("%H:%M:%S"),
                "end_time": end_time.strftime("%H:%M:%S"),
                "room": room if room else None
            }
            # Gửi POST request đến Flask
            try:
                res = requests.post(
                    f"{API_BASE}/api/shifts",
                    json=payload,
                    cookies={"session": session_token}
                )
                if res.status_code == 201:
                    st.success("✅ Tạo ca trực thành công!")
                else:
                    st.error(f"❌ Lỗi: {response.json().get('message')}")
            except Exception as e:
                st.error(f"❌ Không kết nối được server: {e}")
