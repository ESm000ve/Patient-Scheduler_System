/**
 * API Service Layer for MedSync OS
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface AppointmentBooking {
  date: string;
  time: string;
  name: string;
  notes: string;
  phone?: string;
  email?: string;
  dateOfBirth?: string;
  address?: string;
  insuranceProvider?: string;
  insuranceId?: string;
  emergencyContactName?: string;
  emergencyContactPhone?: string;
  doctor?: string;
  visitType?: string;
  status?: string;
  tags?: string[];
}

interface AppointmentUpdate {
  name?: string;
  condition?: string;
  phone?: string;
  email?: string;
  dateOfBirth?: string;
  notes?: string;
  visitType?: string;
  status?: string;
  doctor?: string;
}

/**
 * Fetch wrapper with error handling
 */
async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(error.detail || `HTTP error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error);
    throw error;
  }
}

/**
 * API Methods
 */
export const api = {
  /**
   * Get list of all doctors
   */
  async getDoctors() {
    return fetchAPI('/api/doctors');
  },

  /**
   * Get available visit types
   */
  async getVisitTypes() {
    return fetchAPI('/api/visit-types');
  },

  /**
   * Get available appointment statuses
   */
  async getStatuses() {
    return fetchAPI('/api/statuses');
  },

  /**
   * Get quick medical tags
   */
  async getTags() {
    return fetchAPI('/api/tags');
  },

  /**
   * Get full schedule for a specific date
   */
  async getSchedule(date: string) {
    return fetchAPI(`/api/schedule/${date}`);
  },

  /**
   * Get available slots for a date (optionally by doctor)
   */
  async getAvailableSlots(date: string, doctorId?: string) {
    const params = doctorId ? `?doctor=${doctorId}` : '';
    return fetchAPI(`/api/schedule/${date}/available${params}`);
  },

  /**
   * Get filtered appointments
   */
  async getFilteredSchedule(
    date: string,
    filters: { doctor?: string; visitType?: string; status?: string }
  ) {
    const params = new URLSearchParams();
    if (filters.doctor && filters.doctor !== 'all') params.append('doctor', filters.doctor);
    if (filters.visitType && filters.visitType !== 'all') params.append('visitType', filters.visitType);
    if (filters.status && filters.status !== 'all') params.append('status', filters.status);

    const queryString = params.toString();
    return fetchAPI(`/api/schedule/${date}/filtered${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Get statistics for a date
   */
  async getStatistics(date: string) {
    return fetchAPI(`/api/schedule/${date}/statistics`);
  },

  /**
   * Book a new appointment
   */
  async bookAppointment(booking: AppointmentBooking) {
    return fetchAPI('/api/appointments', {
      method: 'POST',
      body: JSON.stringify(booking),
    });
  },

  /**
   * Update an existing appointment
   */
  async updateAppointment(date: string, time: string, updates: AppointmentUpdate) {
    return fetchAPI(`/api/appointments/${date}/${time}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },

  /**
   * Move appointment to different date/time
   */
  async moveAppointment(date: string, time: string, newDate: string, newTime: string) {
    return fetchAPI(`/api/appointments/${date}/${time}/move`, {
      method: 'POST',
      body: JSON.stringify({ newDate, newTime }),
    });
  },

  /**
   * Cancel an appointment (returns deleted data for undo)
   */
  async cancelAppointment(date: string, time: string) {
    return fetchAPI(`/api/appointments/${date}/${time}`, {
      method: 'DELETE',
    });
  },

  /**
   * Restore a cancelled appointment (undo functionality)
   */
  async restoreAppointment(date: string, time: string, patient: any, doctor: string) {
    return fetchAPI(`/api/appointments/${date}/${time}/restore`, {
      method: 'POST',
      body: JSON.stringify({ patient, doctor }),
    });
  },

  /**
   * Get all dates with schedules
   */
  async getAllDates() {
    return fetchAPI('/api/dates');
  },
};

export default api;
