import unittest
import os
from scheduler import Doctor, Patient  # This imports the classes from your main file

class TestDoctorScheduler(unittest.TestCase):

    def setUp(self):
        """This runs before EVERY single test function.
        It creates a fresh doctor so previous tests don't mess up new ones."""
        self.doctor = Doctor("Test House", "Testing")
        # We want to ensure we aren't using the real 'schedule_data.json' for tests
        self.doctor.FILE_NAME = "test_schedule_data.json"

    def tearDown(self):
        """This runs after EVERY test. We use it to clean up the test file."""
        if os.path.exists("test_schedule_data.json"):
            os.remove("test_schedule_data.json")

    def test_initialization(self):
        """Does the doctor start with 16 empty slots?"""
        schedule = self.doctor.get_schedule()
        self.assertEqual(len(schedule), 16)
        # Check specific time
        self.assertIn("09:00", schedule)
        self.assertIsNone(schedule["09:00"])

    def test_booking_success(self):
        """Can we successfully book a valid slot?"""
        p = Patient("Eric", "Flu")
        result = self.doctor.book_appointment(p, "09:30")
        
        # Check the return message
        self.assertIn("Successfully booked", result)
        
        # Check the actual data
        schedule = self.doctor.get_schedule()
        self.assertEqual(schedule["09:30"].name, "Eric")

    def test_booking_conflict(self):
        """Does the system stop us from double-booking?"""
        p1 = Patient("Eric", "Flu")
        p2 = Patient("Ariana", "Headache")
        
        # Book first one
        self.doctor.book_appointment(p1, "10:00")
        
        # Try to book second one at same time - Should raise ValueError
        with self.assertRaises(ValueError):
            self.doctor.book_appointment(p2, "10:00")

    def test_invalid_time(self):
        """Does the system reject weird times?"""
        p = Patient("Eric", "Flu")
        
        with self.assertRaises(ValueError):
            self.doctor.book_appointment(p, "23:00") # 11 PM is outside work hours

if __name__ == "__main__":
    unittest.main()