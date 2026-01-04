import sys
import json
from datetime import datetime, timedelta
import os

# ==========================================
# PART 1: THE LOGIC (Backend)
# ==========================================

class Patient:
    def __init__(self, name: str, ailment: str):
        self.name = name
        self.ailment = ailment

    def __str__(self):
        return f"{self.name} ({self.ailment})"

    # NEW: Convert object to dictionary for JSON saving
    def to_dict(self):
        return {
            "name": self.name,
            "ailment": self.ailment
        }

    # NEW: Create object from dictionary for JSON loading
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["ailment"])

class Doctor:
    MAX_PATIENTS = 16
    WORK_START_HOUR = 9
    FILE_NAME = "schedule_data.json"

    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.schedule = {} 
        self._initialize_slots()
        self.load_data() # Load data immediately upon creation

    def _initialize_slots(self):
        """Creates empty slots. This is the 'default' state."""
        current_time = datetime.strptime(f"{self.WORK_START_HOUR}:00", "%H:%M")
        for _ in range(self.MAX_PATIENTS):
            time_str = current_time.strftime("%H:%M")
            self.schedule[time_str] = None
            current_time += timedelta(minutes=30)

    def book_appointment(self, patient: Patient, time: str) -> str:
        if time not in self.schedule:
            raise ValueError(f"Time {time} is not a valid slot.")
        
        if self.schedule[time] is not None:
            raise ValueError(f"Slot {time} is already booked.")

        self.schedule[time] = patient
        self.save_data() # Auto-save after every change
        return f"Successfully booked {patient.name} at {time}."

    # --- NEW: PERSISTENCE METHODS ---

    def save_data(self):
        """Converts the schedule to JSON and writes to file."""
        data_to_save = {}
        for time_slot, patient_obj in self.schedule.items():
            if patient_obj:
                # We save the patient as a dictionary
                data_to_save[time_slot] = patient_obj.to_dict()
            else:
                data_to_save[time_slot] = None
        
        with open(self.FILE_NAME, "w") as f:
            json.dump(data_to_save, f, indent=4)
        print(f"(System: Data saved to {self.FILE_NAME})")

    def load_data(self):
        """Reads JSON and reconstructs Patient objects."""
        if not os.path.exists(self.FILE_NAME):
            return # No file exists yet, start fresh

        try:
            with open(self.FILE_NAME, "r") as f:
                loaded_data = json.load(f)
            
            for time_slot, patient_data in loaded_data.items():
                if time_slot in self.schedule and patient_data is not None:
                    # Convert dict back to Patient object
                    self.schedule[time_slot] = Patient.from_dict(patient_data)
                    
        except (json.JSONDecodeError, KeyError):
            print("Error loading data. Starting with fresh schedule.")

    def get_schedule(self):
        return self.schedule

# ==========================================
# PART 2: THE INTERFACE (Frontend)
# ==========================================

def get_valid_time_input():
    while True:
        time_str = input("Enter time (HH:MM, e.g., 09:30): ").strip()
        try:
            datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            print(">>> Invalid format! Please use HH:MM.")

def main():
    dr_house = Doctor("Gregory House", "Diagnostician")
    
    while True:
        print(f"\n--- SYSTEM: Dr. {dr_house.name} ---")
        print("1. View Schedule")
        print("2. Book Appointment")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            print(f"\n--- Schedule for Dr. {dr_house.name} ---")
            schedule = dr_house.get_schedule()
            for time, patient in schedule.items():
                status = patient if patient else "[Available]"
                print(f"{time}: {status}")

        elif choice == "2":
            print("\n--- New Appointment ---")
            name = input("Patient Name: ").strip()
            ailment = input("Patient Ailment: ").strip()
            
            if not name or not ailment:
                print(">>> Error: Name and Ailment cannot be empty.")
                continue

            time_slot = get_valid_time_input()
            new_patient = Patient(name, ailment)

            try:
                result = dr_house.book_appointment(new_patient, time_slot)
                print(f">>> {result}")
            except ValueError as e:
                print(f">>> ERROR: {e}")

        elif choice == "3":
            print("Exiting system...")
            sys.exit()
        
        else:
            print(">>> Invalid selection.")

if __name__ == "__main__":
    main()