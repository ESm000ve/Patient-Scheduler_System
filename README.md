# 🏥 Patient-Doctor Scheduler
**A Full-Stack Python Application for Medical Appointment Management**

![App Dashboard](screenshot.png)

This project demonstrates the intersection of **Object-Oriented Programming (OOP)** and **User Experience (UX/UI) Design**.  
It is built with a modular architecture that cleanly separates business logic from the presentation layer.

---

## 🎯 The Challenge

Design a system that manages a doctor's 8-hour workday (9:00 AM – 5:00 PM) with a maximum capacity of 16 patients.  
The system must:

- Prevent double-booking  
- Validate all user input  
- Persist data across sessions so schedules are never lost  

---

## ✨ Features

### 🛠️ The Engine (Backend)
- **OOP Logic:** Structured with `Doctor` and `Patient` classes for data integrity  
- **Conflict Prevention:** Intelligent validation blocks overlapping or invalid bookings  
- **Persistence:** JSON-based local database auto-saves and loads schedules  
- **Unit Tested:** Automated test suite for backend reliability  

### 🎨 The Interface (UX/UI)
- **Streamlit Dashboard:** Clean, modern web interface  
- **Live Metrics:** Real-time counters for capacity, bookings, and availability  
- **Data Visualization:** Scannable tables powered by Pandas  

---

## 📂 Project Architecture

| Component | Responsibility |
|---------|----------------|
| **`app.py`** | **The View** — Streamlit frontend & UI interactions |
| **`scheduler.py`** | **The Model** — Core logic, time-slot generation, booking rules |
| **`test_scheduler.py`** | **Quality Assurance** — Automated backend testing |
| **`schedule_data.json`** | **The Database** — Lightweight JSON storage |

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Patient-Doctor-Scheduler.git
cd Patient-Doctor-Scheduler
```

### 2️⃣ Install Requirements
```bash
pip install streamlit pandas watchdog
```

### 3️⃣ Run the Application
```bash
streamlit run app.py
```

---

## 🧪 Technical Validation

Run the automated test suite:

```bash
python3 test_scheduler.py
```

---

## 👤 Author

**Eric**  
User Experience Designer & Creative Director  
Exploring the bridge between design systems and functional code.

---

## 🎨 Make It Look Amazing on GitHub

### 📸 Add a Screenshot
Save a screenshot of the app as `screenshot.png` in the project root.

### 📦 Create `requirements.txt`
```
streamlit
pandas
watchdog
```
