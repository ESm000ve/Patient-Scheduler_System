import json
import os

class Patient:
    def __init__(self, name, ailment):
        self.name = name
        self.ailment = ailment

    def to_dict(self):
        return {"name": self.name, "ailment": self.ailment}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["ailment"])

class Doctor:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
        self.MAX_PATIENTS = 16
        self.schedule = self._initialize_schedule()
        self.data_file = "schedule_data.json"
        self._load_data()

    def _initialize_schedule(self):
        """Creates 16 slots from 09:00 to 16:30"""
        times = []
        start_hour = 9
        for i in range(16):
            hour = start_hour + (i // 2)
            minute = "00" if i % 2 == 0 else "30"
            times.append(f"{hour:02d}:{minute}")
        return {time: None for time in times}

    def book_appointment(self, patient, time_slot):
        """Books a patient into a slot."""
        if time_slot not in self.schedule:
            raise ValueError("Invalid time slot.")
        
        # NOTE: We allow overwriting slots now for the Table Editor to work smoothly
        self.schedule[time_slot] = patient
        self._save_data()
        return f"Successfully booked {patient.name} at {time_slot}."

    def cancel_appointment(self, time_slot):
        """Removes a patient from a slot."""
        if time_slot not in self.schedule:
            raise ValueError("Invalid time slot.")
        
        # If it's already empty, just return (no error needed for UI smoothness)
        if self.schedule[time_slot] is None:
            return "Slot was already empty."

        removed_patient = self.schedule[time_slot].name
        self.schedule[time_slot] = None
        self._save_data()
        return f"Cancelled appointment for {removed_patient}."

    def _save_data(self):
        data_to_save = {
            time: (patient.to_dict() if patient else None)
            for time, patient in self.schedule.items()
        }
        with open(self.data_file, "w") as f:
            json.dump(data_to_save, f, indent=4)

    def _load_data(self):
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                for time, patient_data in data.items():
                    if time in self.schedule and patient_data:
                        self.schedule[time] = Patient.from_dict(patient_data)
        except (json.JSONDecodeError, KeyError):
            pass