Patient-Doctor Scheduler 🏥
A full-stack Python application that manages medical appointments. This project explores the intersection of Object-Oriented Programming (OOP) logic and User Interface (UI) design.

⚡ Key Features
Constraint Management: The system enforces a 16-patient limit per 8-hour shift.

Conflict Detection: Logic prevents double-booking time slots.

Data Persistence: Automatic JSON saving ensures data isn't lost.

Modern UI: A responsive web interface built with Streamlit.

🛠️ Tech Stack
Language: Python 3.10+

Interface: Streamlit

Data Handling: Pandas, JSON

Testing: unittest

🚀 How to Run It
Install Dependencies:

Bash

pip install streamlit pandas watchdog
Launch the App:

Bash

streamlit run app.py
📂 Project Structure
app.py: The web interface.

scheduler.py: The core logic (Doctor/Patient classes).

test_scheduler.py: Automated logic tests.

schedule_data.json: The local database.