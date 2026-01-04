"""
MedSync OS - FastAPI Backend
Provides REST API for multi-day, multi-doctor medical scheduling
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date as date_type

from schedule_manager import ScheduleManager
from models import Patient, DOCTORS, VISIT_TYPES, STATUSES, QUICK_TAGS


# FastAPI app
app = FastAPI(
    title="MedSync OS API",
    description="Medical appointment scheduling system with multi-doctor support",
    version="2.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://localhost:8080",  # Alternative dev port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize schedule manager
schedule_manager = ScheduleManager()


# Request/Response Models
class AppointmentBooking(BaseModel):
    """Request model for booking appointment"""
    date: str = Field(..., description="ISO date string (YYYY-MM-DD)")
    time: str = Field(..., description="Time slot (HH:MM)")
    patient_name: str = Field(..., alias="name")
    condition: str = Field(default="", alias="notes")
    phone: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    address: Optional[str] = None
    insurance_provider: Optional[str] = Field(None, alias="insuranceProvider")
    insurance_id: Optional[str] = Field(None, alias="insuranceId")
    emergency_contact_name: Optional[str] = Field(None, alias="emergencyContactName")
    emergency_contact_phone: Optional[str] = Field(None, alias="emergencyContactPhone")
    doctor_id: str = Field(default="chen", alias="doctor")
    visit_type: str = Field(default="consultation", alias="visitType")
    status: str = Field(default="pending")
    tags: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class AppointmentUpdate(BaseModel):
    """Request model for updating appointment"""
    name: Optional[str] = None
    condition: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    dateOfBirth: Optional[str] = None
    notes: Optional[str] = None
    visitType: Optional[str] = None
    status: Optional[str] = None
    doctor: Optional[str] = None


class AppointmentMove(BaseModel):
    """Request model for moving appointment"""
    newDate: str
    newTime: str


class UndoRestore(BaseModel):
    """Request model for restoring cancelled appointment"""
    patient: dict
    doctor: str


# API Endpoints

@app.get("/")
def read_root():
    """API health check"""
    return {
        "name": "MedSync OS API",
        "version": "2.0.0",
        "status": "operational"
    }


@app.get("/api/doctors")
def get_doctors():
    """Get list of all doctors"""
    return {
        "doctors": [doctor.to_dict() for doctor in DOCTORS.values()]
    }


@app.get("/api/visit-types")
def get_visit_types():
    """Get available visit types"""
    return {"visit_types": VISIT_TYPES}


@app.get("/api/statuses")
def get_statuses():
    """Get available appointment statuses"""
    return {"statuses": STATUSES}


@app.get("/api/tags")
def get_tags():
    """Get quick tags for medical notes"""
    return {"tags": QUICK_TAGS}


@app.get("/api/schedule/{date}")
def get_schedule(date: str):
    """Get full schedule for a specific date"""
    try:
        schedule = schedule_manager.get_schedule_for_date(date)

        # Convert to JSON-friendly format
        result = {}
        for time, appointment in schedule.items():
            if appointment is None:
                result[time] = None
            else:
                result[time] = {
                    "patient": appointment["patient"].to_dict(),
                    "doctor": appointment["doctor"]
                }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/schedule/{date}/available")
def get_available_slots(
    date: str,
    doctor_id: Optional[str] = Query(None, alias="doctor")
):
    """Get available time slots for a date, optionally by doctor"""
    try:
        slots = schedule_manager.get_available_slots(date, doctor_id)
        return {"available_slots": slots}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/schedule/{date}/filtered")
def get_filtered_schedule(
    date: str,
    doctor_id: Optional[str] = Query(None, alias="doctor"),
    visit_type: Optional[str] = Query(None, alias="visitType"),
    status: Optional[str] = Query(None)
):
    """Get filtered appointments for a date"""
    try:
        filtered = schedule_manager.filter_appointments(
            date, doctor_id, visit_type, status
        )

        # Convert to JSON
        result = {}
        for time, appointment in filtered.items():
            if appointment is None:
                result[time] = None
            else:
                result[time] = {
                    "patient": appointment["patient"].to_dict(),
                    "doctor": appointment["doctor"]
                }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/schedule/{date}/statistics")
def get_statistics(date: str):
    """Get statistics for a specific date"""
    try:
        stats = schedule_manager.get_statistics(date)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/appointments")
def book_appointment(booking: AppointmentBooking):
    """Book a new appointment"""
    try:
        # Create patient object
        patient = Patient(
            name=booking.patient_name,
            condition=booking.condition,
            phone=booking.phone,
            email=booking.email,
            date_of_birth=booking.date_of_birth,
            address=booking.address,
            insurance_provider=booking.insurance_provider,
            insurance_id=booking.insurance_id,
            emergency_contact_name=booking.emergency_contact_name,
            emergency_contact_phone=booking.emergency_contact_phone,
            notes=booking.condition,  # Use condition as notes
            visit_type=booking.visit_type,
            status=booking.status,
            doctor_id=booking.doctor_id,
            tags=booking.tags
        )

        result = schedule_manager.book_appointment(
            booking.date,
            booking.time,
            patient,
            booking.doctor_id
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/appointments/{date}/{time}")
def update_appointment(
    date: str,
    time: str,
    updates: AppointmentUpdate
):
    """Update appointment details"""
    try:
        update_dict = updates.dict(exclude_unset=True)

        result = schedule_manager.update_appointment(date, time, **update_dict)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/appointments/{date}/{time}/move")
def move_appointment(
    date: str,
    time: str,
    move_data: AppointmentMove
):
    """Move appointment to different date/time"""
    try:
        result = schedule_manager.move_appointment(
            date,
            time,
            move_data.newDate,
            move_data.newTime
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/appointments/{date}/{time}")
def cancel_appointment(date: str, time: str):
    """Cancel an appointment (returns deleted data for undo)"""
    try:
        result = schedule_manager.cancel_appointment(date, time)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/appointments/{date}/{time}/restore")
def restore_appointment(
    date: str,
    time: str,
    restore_data: UndoRestore
):
    """Restore a cancelled appointment (for undo functionality)"""
    try:
        result = schedule_manager.restore_appointment(
            date,
            time,
            restore_data.patient,
            restore_data.doctor
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dates")
def get_all_dates():
    """Get all dates that have schedules"""
    try:
        dates = schedule_manager.get_all_dates()
        return {"dates": dates}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run with: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
