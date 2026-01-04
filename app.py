import streamlit as st
import pandas as pd
from scheduler import Doctor, Patient

# 1. Config must be the very first Streamlit command
st.set_page_config(page_title="Doctor Scheduler", page_icon="🏥", layout="wide")

# 2. Helper to load the doctor (Cached so it doesn't reset every click)
@st.cache_resource
def get_doctor_system():
    # Initialize the doctor
    doc = Doctor("Gregory House", "Diagnostician")
    return doc

try:
    doctor = get_doctor_system()
except Exception as e:
    st.error(f"Error loading Doctor System: {e}")
    st.stop()

# --- SIDEBAR: Booking Form ---
st.sidebar.header("📝 Book Appointment")

with st.sidebar.form("booking_form"):
    st.write("Enter patient details below:")
    patient_name = st.text_input("Patient Name")
    patient_ailment = st.text_input("Ailment / Reason")
    
    # Dropdown for time slots
    available_slots = list(doctor.schedule.keys())
    selected_time = st.selectbox("Select Time Slot", available_slots)
    
    submitted = st.form_submit_button("Book Appointment")

    if submitted:
        if not patient_name or not patient_ailment:
            st.warning("⚠️ Please enter both a name and an ailment.")
        else:
            try:
                new_patient = Patient(patient_name, patient_ailment)
                # Attempt booking
                msg = doctor.book_appointment(new_patient, selected_time)
                st.success(msg)
                # Force a page reload to show the new booking in the table immediately
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {e}")

# --- MAIN PAGE: Dashboard ---
st.title("🏥 Patient Scheduler System")
st.markdown(f"**Doctor:** {doctor.name} | **Specialty:** {doctor.specialty}")

# Create the data for the table
table_data = []
for time_slot, patient in doctor.schedule.items():
    status = "Available"
    p_name = "-"
    p_ailment = "-"
    
    if patient:
        status = "🔴 Booked" # Added emoji for visual flair
        p_name = patient.name
        p_ailment = patient.ailment
    else:
        status = "🟢 Available"

    table_data.append({
        "Time": time_slot,
        "Status": status,
        "Patient Name": p_name,
        "Condition": p_ailment
    })

# Convert to Pandas DataFrame
df = pd.DataFrame(table_data)

# Display metrics at the top
total_slots = doctor.MAX_PATIENTS
booked_slots = sum(1 for p in doctor.schedule.values() if p is not None)
remaining_slots = total_slots - booked_slots

col1, col2, col3 = st.columns(3)
col1.metric("Total Capacity", total_slots)
col2.metric("Patients Booked", booked_slots)
col3.metric("Slots Available", remaining_slots)

st.divider()

# Display the main table
st.subheader("Daily Schedule")
st.dataframe(df, use_container_width=True, hide_index=True)