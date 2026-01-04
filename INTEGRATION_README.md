# MedSync OS - Full Stack Integration

## Overview

This repository now contains a **complete full-stack medical scheduling application**:

- **Frontend**: React + TypeScript with Tailwind CSS (Figma Make export)
- **Backend**: Python FastAPI with multi-day, multi-doctor scheduling
- **Features**: WCAG 2.1 AA compliant, undo functionality, advanced filtering

---

## 🏗️ Project Structure

```
Patient-Scheduler_System/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # All UI components
│   │   ├── context/       # Theme context
│   │   ├── services/      # API service layer
│   │   └── App.tsx        # Main app component
│   ├── package.json
│   └── globals.css
│
├── backend/               # Python FastAPI
│   ├── main.py           # FastAPI application
│   ├── models.py         # Data models
│   ├── schedule_manager.py  # Core scheduling logic
│   ├── requirements.txt
│   └── schedule_data.json   # Persisted data
│
├── app.py                # Original Streamlit app (legacy)
├── scheduler.py          # Original Python code (legacy)
└── test_scheduler.py     # Unit tests
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The React app will be available at `http://localhost:5173`

---

## 📡 API Endpoints

### Doctors & Metadata

- `GET /api/doctors` - List all doctors
- `GET /api/visit-types` - Get visit type options
- `GET /api/statuses` - Get appointment status options
- `GET /api/tags` - Get quick medical tags

### Schedule Operations

- `GET /api/schedule/{date}` - Get full schedule for date
- `GET /api/schedule/{date}/available` - Get available time slots
- `GET /api/schedule/{date}/filtered` - Get filtered appointments
- `GET /api/schedule/{date}/statistics` - Get date statistics

### Appointment CRUD

- `POST /api/appointments` - Book new appointment
- `PATCH /api/appointments/{date}/{time}` - Update appointment
- `DELETE /api/appointments/{date}/{time}` - Cancel appointment
- `POST /api/appointments/{date}/{time}/restore` - Restore cancelled (undo)
- `POST /api/appointments/{date}/{time}/move` - Move to different date/time

---

## 🎨 Features Implemented

### From Documentation

All 6 documentation files have been fully implemented:

1. ✅ **WCAG 2.1 AA Compliance** - Full accessibility support
2. ✅ **Calendar Navigation** - Week view + month calendar modal
3. ✅ **Advanced Filtering** - Doctor, visit type, status filters
4. ✅ **Toast Feedback** - 8-second undo functionality
5. ✅ **Enhanced Notes** - Rich text formatting, character counter, tags
6. ✅ **Safe Cancellation** - 3-screen confirmation flow

### Backend Capabilities

- **Multi-day scheduling** - Book appointments months in advance
- **Multi-doctor support** - 4 doctors (Chen, Park, Kumar, Williams)
- **Visit type tracking** - Follow-up, routine, consultation, test, annual
- **Status management** - Confirmed, pending, completed
- **Full patient data** - Insurance, emergency contacts, notes
- **Undo support** - All operations return previous state
- **Data persistence** - JSON-based storage
- **Filtering** - By doctor, visit type, and status
- **Statistics** - Utilization rates, appointment breakdowns

---

## 🧪 Testing

### Backend Tests

```bash
# From project root
python test_scheduler.py
```

### API Testing

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

### CORS Configuration

Backend is configured to allow requests from:
- `http://localhost:3000` (Create React App)
- `http://localhost:5173` (Vite)
- `http://localhost:8080` (Alternative)

Modify in `backend/main.py` if needed.

---

## 📊 Data Model

### Patient Object

```json
{
  "name": "John Smith",
  "condition": "Annual physical examination",
  "phone": "555-123-4567",
  "email": "john.smith@email.com",
  "dateOfBirth": "1985-03-15",
  "address": "123 Main St",
  "insuranceProvider": "Blue Cross",
  "insuranceId": "ABC123456",
  "emergencyContactName": "Jane Smith",
  "emergencyContactPhone": "555-987-6543",
  "notes": "Patient reports no current symptoms",
  "visitType": "annual",
  "status": "confirmed",
  "doctor": "chen",
  "tags": ["Blood Pressure", "Medication Review"],
  "createdAt": "2026-01-04T10:30:00",
  "lastModified": "2026-01-04T10:30:00"
}
```

### Schedule Structure

```json
{
  "2026-01-07": {
    "09:00": null,
    "09:30": {
      "patient": { /* Patient object */ },
      "doctor": "chen"
    },
    "10:00": {
      "patient": { /* Patient object */ },
      "doctor": "park"
    }
    // ... more slots
  }
}
```

---

## 🎯 Next Steps

### For Development

1. **Add authentication** - User login for doctors
2. **Real-time updates** - WebSocket for live schedule changes
3. **Email notifications** - Appointment confirmations
4. **SMS reminders** - Text message reminders
5. **Analytics dashboard** - Usage statistics
6. **Export functionality** - PDF reports, CSV exports

### For Deployment

1. **Frontend**: Deploy to Vercel/Netlify
2. **Backend**: Deploy to Heroku/Railway/Render
3. **Database**: Migrate from JSON to PostgreSQL
4. **CI/CD**: GitHub Actions for automated testing

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend won't connect to backend

1. Check backend is running on port 8000
2. Check CORS settings in `backend/main.py`
3. Verify `VITE_API_URL` in frontend `.env`

### CORS errors

Add your frontend URL to `allow_origins` in `backend/main.py`:

```python
allow_origins=[
    "http://localhost:3000",
    "http://your-frontend-url.com",
],
```

---

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (when running)
- **Component Docs**: See individual `.tsx` files for JSDoc comments
- **Design Specs**: See `WCAG_AUDIT.md`, `NAVIGATION_UX_IMPROVEMENTS.md`, etc.

---

## 👥 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Test thoroughly (frontend + backend)
4. Submit a pull request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **shadcn/ui** - UI components (MIT License)
- **Lucide Icons** - Icon library
- **Unsplash** - Demo images
- **FastAPI** - Backend framework
- **React** - Frontend library

---

**Built with ❤️ by Eric**
Medical Scheduling System for the Modern Age
