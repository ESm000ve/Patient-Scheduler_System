"""
Multi-day, multi-doctor schedule management system
Handles booking, cancellation, updates, and filtering
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models import Patient, DOCTORS


class ScheduleManager:
    """Manages schedules for all doctors across multiple dates"""

    MAX_PATIENTS = 16
    WORK_START_HOUR = 9
    FILE_NAME = "schedule_data.json"

    def __init__(self):
        # Format: {date: {time: {patient, doctor_id}}}
        self.schedules: Dict[str, Dict[str, Optional[dict]]] = {}
        self.load_data()

    def _create_empty_schedule(self) -> Dict[str, Optional[dict]]:
        """Create 16 empty 30-minute slots from 09:00-16:30"""
        schedule = {}
        current_time = datetime.strptime("09:00", "%H:%M")

        for _ in range(self.MAX_PATIENTS):
            time_str = current_time.strftime("%H:%M")
            schedule[time_str] = None
            current_time += timedelta(minutes=30)

        return schedule

    def get_schedule_for_date(self, date: str) -> Dict[str, Optional[dict]]:
        """Get all appointments for a specific date"""
        if date not in self.schedules:
            self.schedules[date] = self._create_empty_schedule()
        return self.schedules[date]

    def book_appointment(
        self,
        date: str,
        time: str,
        patient: Patient,
        doctor_id: str = "chen"
    ) -> dict:
        """Book appointment for specific doctor on specific date"""
        schedule = self.get_schedule_for_date(date)

        if time not in schedule:
            raise ValueError(f"Time {time} is not a valid slot")

        if schedule[time] is not None:
            raise ValueError(f"Slot {time} is already booked")

        # Store appointment
        schedule[time] = {
            "patient": patient,
            "doctor": doctor_id
        }

        self.save_data()

        return {
            "success": True,
            "message": f"Booked {patient.name} with {DOCTORS[doctor_id].name} at {time}",
            "appointment": {
                "time": time,
                "patient": patient.to_dict(),
                "doctor": doctor_id
            }
        }

    def get_available_slots(
        self,
        date: str,
        doctor_id: Optional[str] = None
    ) -> List[str]:
        """Get unbooked slots, optionally filtered by doctor"""
        schedule = self.get_schedule_for_date(date)
        available = []

        for time, appointment in schedule.items():
            if appointment is None:
                available.append(time)
            elif doctor_id and appointment.get("doctor") != doctor_id:
                # Slot is booked by another doctor
                pass

        return available

    def filter_appointments(
        self,
        date: str,
        doctor_id: Optional[str] = None,
        visit_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Optional[dict]]:
        """Filter appointments by criteria"""
        schedule = self.get_schedule_for_date(date)
        filtered = {}

        for time, appointment in schedule.items():
            if appointment is None:
                # Always include empty slots
                filtered[time] = None
                continue

            patient = appointment["patient"]

            # Apply filters
            if doctor_id and doctor_id != "all" and appointment["doctor"] != doctor_id:
                filtered[time] = None
                continue

            if visit_type and visit_type != "all" and patient.visit_type != visit_type:
                filtered[time] = None
                continue

            if status and status != "all" and patient.status != status:
                filtered[time] = None
                continue

            # Appointment matches all filters
            filtered[time] = appointment

        return filtered

    def cancel_appointment(self, date: str, time: str) -> dict:
        """Cancel and free up a slot, returning deleted data for undo"""
        schedule = self.get_schedule_for_date(date)

        if time not in schedule:
            raise ValueError(f"Time {time} is invalid")

        if schedule[time] is None:
            raise ValueError(f"No appointment at {time} to cancel")

        # Store cancelled appointment data for undo
        cancelled = schedule[time]
        patient_name = cancelled["patient"].name

        # Clear the slot
        schedule[time] = None
        self.save_data()

        return {
            "success": True,
            "message": f"Cancelled appointment for {patient_name}",
            "deleted": {
                "time": time,
                "patient": cancelled["patient"].to_dict(),
                "doctor": cancelled["doctor"]
            }
        }

    def restore_appointment(self, date: str, time: str, patient_dict: dict, doctor_id: str) -> dict:
        """Restore a cancelled appointment (for undo)"""
        schedule = self.get_schedule_for_date(date)

        if time not in schedule:
            raise ValueError(f"Time {time} is invalid")

        if schedule[time] is not None:
            raise ValueError(f"Slot {time} is already booked")

        # Restore the appointment
        patient = Patient.from_dict(patient_dict)
        schedule[time] = {
            "patient": patient,
            "doctor": doctor_id
        }

        self.save_data()

        return {
            "success": True,
            "message": f"Appointment restored for {patient.name}"
        }

    def update_appointment(
        self,
        date: str,
        time: str,
        **updates
    ) -> dict:
        """Update appointment details"""
        schedule = self.get_schedule_for_date(date)

        if time not in schedule or schedule[time] is None:
            raise ValueError(f"No appointment at {time}")

        # Store old data for undo
        old_appointment = schedule[time]
        old_patient_dict = old_appointment["patient"].to_dict()

        patient = old_appointment["patient"]

        # Update patient fields
        if "name" in updates:
            patient.name = updates["name"]
        if "condition" in updates:
            patient.condition = updates["condition"]
        if "phone" in updates:
            patient.phone = updates["phone"]
        if "email" in updates:
            patient.email = updates["email"]
        if "dateOfBirth" in updates:
            patient.date_of_birth = updates["dateOfBirth"]
        if "notes" in updates:
            patient.notes = updates["notes"]
        if "visitType" in updates:
            patient.visit_type = updates["visitType"]
        if "status" in updates:
            patient.status = updates["status"]
        if "doctor" in updates:
            old_appointment["doctor"] = updates["doctor"]

        patient.last_modified = datetime.now().isoformat()

        self.save_data()

        return {
            "success": True,
            "message": f"Updated appointment for {patient.name}",
            "old": {
                "patient": old_patient_dict,
                "doctor": old_appointment["doctor"]
            },
            "new": {
                "patient": patient.to_dict(),
                "doctor": old_appointment["doctor"]
            }
        }

    def move_appointment(
        self,
        old_date: str,
        old_time: str,
        new_date: str,
        new_time: str
    ) -> dict:
        """Move appointment to different date/time"""
        # Get appointment from old slot
        old_schedule = self.get_schedule_for_date(old_date)

        if old_time not in old_schedule or old_schedule[old_time] is None:
            raise ValueError(f"No appointment at {old_time}")

        # Check new slot is available
        new_schedule = self.get_schedule_for_date(new_date)

        if new_time not in new_schedule:
            raise ValueError(f"Time {new_time} is not valid")

        if new_schedule[new_time] is not None:
            raise ValueError(f"Slot {new_time} is already booked")

        # Move appointment
        appointment = old_schedule[old_time]
        old_schedule[old_time] = None
        new_schedule[new_time] = appointment

        appointment["patient"].last_modified = datetime.now().isoformat()

        self.save_data()

        return {
            "success": True,
            "message": f"Moved appointment to {new_date} at {new_time}",
            "old": {"date": old_date, "time": old_time},
            "new": {"date": new_date, "time": new_time}
        }

    def save_data(self):
        """Save all schedules to JSON file"""
        data_to_save = {}

        for date, schedule in self.schedules.items():
            data_to_save[date] = {}
            for time, appointment in schedule.items():
                if appointment is None:
                    data_to_save[date][time] = None
                else:
                    data_to_save[date][time] = {
                        "patient": appointment["patient"].to_dict(),
                        "doctor": appointment["doctor"]
                    }

        with open(self.FILE_NAME, "w") as f:
            json.dump(data_to_save, f, indent=2)

        print(f"[System] Data saved to {self.FILE_NAME}")

    def load_data(self):
        """Load all schedules from JSON file"""
        if not os.path.exists(self.FILE_NAME):
            print(f"[System] No existing schedule file found, starting fresh")
            return

        try:
            with open(self.FILE_NAME, "r") as f:
                loaded_data = json.load(f)

            for date, schedule in loaded_data.items():
                self.schedules[date] = {}
                for time, appointment in schedule.items():
                    if appointment is None:
                        self.schedules[date][time] = None
                    else:
                        patient = Patient.from_dict(appointment["patient"])
                        self.schedules[date][time] = {
                            "patient": patient,
                            "doctor": appointment["doctor"]
                        }

            print(f"[System] Loaded schedules for {len(self.schedules)} dates")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"[System] Error loading data: {e}. Starting with fresh schedule.")

    def get_all_dates(self) -> List[str]:
        """Get all dates that have schedules"""
        return sorted(list(self.schedules.keys()))

    def get_statistics(self, date: str) -> dict:
        """Get statistics for a date"""
        schedule = self.get_schedule_for_date(date)

        total_slots = len(schedule)
        booked_slots = sum(1 for apt in schedule.values() if apt is not None)
        available_slots = total_slots - booked_slots

        appointments_by_doctor = {}
        appointments_by_type = {}
        appointments_by_status = {}

        for appointment in schedule.values():
            if appointment is not None:
                doctor = appointment["doctor"]
                appointments_by_doctor[doctor] = appointments_by_doctor.get(doctor, 0) + 1

                patient = appointment["patient"]
                visit_type = patient.visit_type
                appointments_by_type[visit_type] = appointments_by_type.get(visit_type, 0) + 1

                status = patient.status
                appointments_by_status[status] = appointments_by_status.get(status, 0) + 1

        return {
            "total_slots": total_slots,
            "booked_slots": booked_slots,
            "available_slots": available_slots,
            "utilization": round((booked_slots / total_slots) * 100, 1),
            "by_doctor": appointments_by_doctor,
            "by_type": appointments_by_type,
            "by_status": appointments_by_status
        }
