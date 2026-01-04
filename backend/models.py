"""
Enhanced data models for MedSync OS
Supports multi-day, multi-doctor scheduling with full patient information
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum


class VisitType(str, Enum):
    """Visit type categories"""
    FOLLOW_UP = "follow-up"
    ROUTINE = "routine"
    CONSULTATION = "consultation"
    TEST = "test"
    ANNUAL = "annual"


class AppointmentStatus(str, Enum):
    """Appointment status types"""
    CONFIRMED = "confirmed"
    PENDING = "pending"
    COMPLETED = "completed"


class Patient:
    """Enhanced patient model with full information"""

    def __init__(
        self,
        name: str,
        condition: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        address: Optional[str] = None,
        insurance_provider: Optional[str] = None,
        insurance_id: Optional[str] = None,
        emergency_contact_name: Optional[str] = None,
        emergency_contact_phone: Optional[str] = None,
        notes: Optional[str] = None,
        visit_type: str = VisitType.CONSULTATION.value,
        status: str = AppointmentStatus.PENDING.value,
        doctor_id: str = "chen",
        tags: Optional[List[str]] = None
    ):
        self.name = name
        self.condition = condition
        self.phone = phone
        self.email = email
        self.date_of_birth = date_of_birth
        self.address = address
        self.insurance_provider = insurance_provider
        self.insurance_id = insurance_id
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.notes = notes
        self.visit_type = visit_type
        self.status = status
        self.doctor_id = doctor_id
        self.tags = tags or []
        self.created_at = datetime.now().isoformat()
        self.last_modified = datetime.now().isoformat()

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "condition": self.condition,
            "phone": self.phone,
            "email": self.email,
            "dateOfBirth": self.date_of_birth,
            "address": self.address,
            "insuranceProvider": self.insurance_provider,
            "insuranceId": self.insurance_id,
            "emergencyContactName": self.emergency_contact_name,
            "emergencyContactPhone": self.emergency_contact_phone,
            "notes": self.notes,
            "visitType": self.visit_type,
            "status": self.status,
            "doctor": self.doctor_id,
            "tags": self.tags,
            "createdAt": self.created_at,
            "lastModified": self.last_modified
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Patient from dictionary"""
        patient = cls(
            name=data["name"],
            condition=data.get("condition", ""),
            phone=data.get("phone"),
            email=data.get("email"),
            date_of_birth=data.get("dateOfBirth"),
            address=data.get("address"),
            insurance_provider=data.get("insuranceProvider"),
            insurance_id=data.get("insuranceId"),
            emergency_contact_name=data.get("emergencyContactName"),
            emergency_contact_phone=data.get("emergencyContactPhone"),
            notes=data.get("notes"),
            visit_type=data.get("visitType", "consultation"),
            status=data.get("status", "pending"),
            doctor_id=data.get("doctor", "chen"),
            tags=data.get("tags", [])
        )
        patient.created_at = data.get("createdAt", patient.created_at)
        patient.last_modified = data.get("lastModified", patient.last_modified)
        return patient


class Doctor:
    """Doctor information"""

    def __init__(self, id: str, name: str, specialty: str):
        self.id = id
        self.name = name
        self.specialty = specialty

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty
        }


# Doctor roster
DOCTORS = {
    "chen": Doctor("chen", "Dr. Sarah Chen", "Cardiology"),
    "park": Doctor("park", "Dr. Michael Park", "Pediatrics"),
    "kumar": Doctor("kumar", "Dr. Lisa Kumar", "Internal Medicine"),
    "williams": Doctor("williams", "Dr. James Williams", "Orthopedics"),
}


# Visit types
VISIT_TYPES = [
    {"id": "follow-up", "label": "Follow-up", "icon": "🔄"},
    {"id": "routine", "label": "Routine Checkup", "icon": "✓"},
    {"id": "consultation", "label": "Consultation", "icon": "💬"},
    {"id": "test", "label": "Tests & Labs", "icon": "🧪"},
    {"id": "annual", "label": "Annual Physical", "icon": "📋"}
]


# Appointment statuses
STATUSES = [
    {"id": "confirmed", "label": "Confirmed", "color": "green"},
    {"id": "pending", "label": "Pending", "color": "yellow"},
    {"id": "completed", "label": "Completed", "color": "blue"}
]


# Quick tags
QUICK_TAGS = [
    'Blood Pressure',
    'Medication Review',
    'Follow-up Required',
    'Lab Work Needed',
    'X-Ray Ordered',
    'Referral Given',
    'Symptoms Improved',
    'New Prescription',
]
