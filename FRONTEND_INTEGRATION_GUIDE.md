# Frontend Integration Guide

## Overview

Your React components (from Figma Make) are ready to be integrated with the Python FastAPI backend.

## File Organization

Place your existing React components in this structure:

```
frontend/
├── src/
│   ├── components/
│   │   ├── AppointmentSlot.tsx
│   │   ├── BookingModal.tsx
│   │   ├── CurrentTimeIndicator.tsx
│   │   ├── DateNavigator.tsx
│   │   ├── EnhancedNotesField.tsx
│   │   ├── FilterPanel.tsx
│   │   ├── Header.tsx
│   │   ├── MetricsGrid.tsx
│   │   ├── NotificationCenter.tsx
│   │   ├── PatientDetailsView.tsx
│   │   ├── QuickActionMenu.tsx
│   │   ├── SafeCancellationFlow.tsx
│   │   ├── ScheduleView.tsx
│   │   ├── SearchBar.tsx
│   │   ├── ScreenReaderAnnouncer.tsx
│   │   ├── ThemeToggle.tsx
│   │   └── Toast.tsx
│   │
│   ├── context/
│   │   └── ThemeContext.tsx
│   │
│   ├── services/
│   │   └── api.ts  ← Already created!
│   │
│   ├── App.tsx
│   ├── globals.css
│   └── main.tsx
│
├── index.html
├── package.json  ← Already created!
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.ts
```

## Integration Steps

### Step 1: Copy Your Component Files

Copy all your `.tsx` component files to `frontend/src/components/`

### Step 2: Update App.tsx to Use API

Your current `App.tsx` has hardcoded data. Here's how to connect it to the backend:

```typescript
// Add this import at the top
import { api } from './services/api';

// Replace the hardcoded initialAppointmentsByDate with:
const [appointmentsByDate, setAppointmentsByDate] = useState<AppointmentsByDate>({});

// Add effect to load data from backend
useEffect(() => {
  const loadSchedule = async () => {
    try {
      const data = await api.getSchedule(selectedDate);

      // Convert API response to your format
      const appointments = Object.entries(data).map(([time, apt]: [string, any]) => ({
        time,
        patient: apt?.patient ? {
          name: apt.patient.name,
          condition: apt.patient.condition,
          doctor: apt.doctor,
          visitType: apt.patient.visitType,
          status: apt.patient.status,
          // ... other fields
        } : undefined
      }));

      setAppointmentsByDate(prev => ({
        ...prev,
        [selectedDate]: appointments
      }));
    } catch (error) {
      console.error('Failed to load schedule:', error);
    }
  };

  loadSchedule();
}, [selectedDate]);
```

### Step 3: Update Booking to Call API

```typescript
const handleConfirmBooking = async (patientData: any, date?: string, time?: string) => {
  const targetDate = date || selectedDate;
  const targetTime = time || bookingTime;

  try {
    // Call backend API
    const result = await api.bookAppointment({
      date: targetDate,
      time: targetTime,
      name: patientData.name,
      notes: patientData.notes,
      phone: patientData.phone,
      email: patientData.email,
      dateOfBirth: patientData.dateOfBirth,
      address: patientData.address,
      insuranceProvider: patientData.insuranceProvider,
      insuranceId: patientData.insuranceId,
      emergencyContactName: patientData.emergencyContactName,
      emergencyContactPhone: patientData.emergencyContactPhone,
      doctor: 'chen',
      visitType: 'routine',
      status: 'confirmed'
    });

    // Store undo data
    setUndoAction({
      type: 'book',
      data: result.appointment
    });

    // Update local state
    // ... rest of your existing code

    showToast(
      `Appointment booked for ${patientData.name} at ${targetTime}`,
      'success',
      () => handleUndoBook(targetDate, targetTime),
      'UNDO'
    );
  } catch (error) {
    console.error('Booking failed:', error);
    showToast('Failed to book appointment', 'error');
  }
};
```

### Step 4: Update Cancel to Call API

```typescript
const handleConfirmCancel = async (time: string, name: string) => {
  try {
    // Call backend API
    const result = await api.cancelAppointment(selectedDate, time);

    // Store undo data
    setUndoAction({
      type: 'cancel',
      data: result.deleted
    });

    // Update local state
    // ... rest of your existing code

    showToast(
      `Appointment cancelled for ${name}`,
      'error',
      () => handleUndoCancel(),
      'UNDO'
    );
  } catch (error) {
    console.error('Cancel failed:', error);
    showToast('Failed to cancel appointment', 'error');
  }
};
```

### Step 5: Implement Undo with API

```typescript
const handleUndoCancel = async () => {
  if (!undoAction || undoAction.type !== 'cancel') return;

  const { time, patient, doctor } = undoAction.data;

  try {
    // Call backend API to restore
    await api.restoreAppointment(selectedDate, time, patient, doctor);

    // Update local state
    // ... rest of your existing code

    dismissToast();
    showToast('Appointment restored', 'success', undefined, undefined, 3000);
  } catch (error) {
    console.error('Undo failed:', error);
    showToast('Failed to restore appointment', 'error');
  }
};
```

### Step 6: Update Filters to Use API

```typescript
const handleFilterChange = async (newFilters: FilterState) => {
  setFilters(newFilters);

  try {
    // Call backend API for filtered results
    const filtered = await api.getFilteredSchedule(selectedDate, newFilters);

    // Convert and update local state
    // ... (similar to Step 2)
  } catch (error) {
    console.error('Filter failed:', error);
  }
};
```

## Configuration Files Needed

### `vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthrough ThroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### `tailwind.config.ts`

```typescript
import type { Config } from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
} satisfies Config
```

### `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>MedSync OS</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### `main.tsx`

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './globals.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## Running the Integrated App

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to see your integrated app!

## Testing Integration

1. **Book an appointment** - Should save to backend
2. **Refresh page** - Data should persist
3. **Cancel appointment** - Should call API
4. **Click UNDO** - Should restore via API
5. **Filter appointments** - Should use backend filtering
6. **Change dates** - Should load different days from backend

## Troubleshooting

### "Failed to fetch" errors

1. Check backend is running on port 8000
2. Check console for CORS errors
3. Verify `api.ts` has correct `API_BASE_URL`

### Types not matching

If TypeScript complains about types, make sure the Patient interface in `App.tsx` matches the API response format.

### Components not loading

Make sure all component imports in `App.tsx` have the correct relative paths:
```typescript
import { Header } from './components/Header';
import { Toast } from './components/Toast';
// etc.
```

---

**Next**: After setting up these files, your frontend will be fully integrated with the FastAPI backend!
