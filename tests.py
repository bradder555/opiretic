import unittest
from datetime import datetime, timedelta
from models import Program, DayOfWeek, Trigger 
import logging
import sys 
from time import sleep 

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


dates_to_test = [
    f"2025-04-{x:02}"
    for x 
    in range(4,21)
]

class DayOfWeekTest(unittest.TestCase):
    def test_day_of_week(self):
        program = Program(
            trigger = Trigger.day_of_week,
            start_time = datetime.fromisoformat("1970-01-01T17:00:00"),
            duration = timedelta(minutes=30),
            week_day= DayOfWeek.sunday,
            enabled= True
        )

        for test_date in dates_to_test:
            d = datetime.fromisoformat(f"{test_date}T00:00:01")
            dow = DayOfWeek(d.weekday())
            logging.info(f"Testing date {d}({dow.to_long()})")

            times_to_test_false = [
                "04:00",
                "04:30",
                "04:59",
                "05:00",
                "05:01",
                "12:00",
                "16:00",
                "16:30",
                "16:59"
            ]
            for test_time in times_to_test_false:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                self.assertFalse(is_active)
            
            times_to_test_true = [
                "17:00",
                "17:01",
                "17:05",
                "17:15",
                "17:25",
                "17:29"
            ]

            trigger_time = datetime.fromisoformat(f"{test_date}T17:00:00")
            for test_time in times_to_test_true:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                if dow == DayOfWeek.sunday:
                    self.assertTrue(is_active)
                    self.assertEqual(trigger_time, program.last_triggered)
                else:
                    self.assertFalse(is_active)

            times_to_test_false = [
                "17:31",
                "17:35",
                "18:00",
                "19:00"
            ]
            for test_time in times_to_test_false:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                if test_dt >= datetime.fromisoformat("2025-04-08T17:30:00"):
                    pass
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                self.assertFalse(is_active)

class EveryDay(unittest.TestCase):
    def test_every_day(self):
        program = Program(
            trigger = Trigger.daily,
            start_time = datetime.fromisoformat("1970-01-01T17:00:00"),
            duration = timedelta(minutes=30),
            week_day= DayOfWeek.sunday,
            enabled= True
        )

        for test_date in dates_to_test:
            d = datetime.fromisoformat(f"{test_date}T00:00:01")
            dow = DayOfWeek(d.weekday())
            logging.info(f"Testing date {d}({dow.to_long()})")

            times_to_test_false = [
                "04:00",
                "04:30",
                "04:59",
                "05:00",
                "05:01",
                "12:00",
                "16:00",
                "16:30",
                "16:59"
            ]
            for test_time in times_to_test_false:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                self.assertFalse(is_active)
            
            times_to_test_true = [
                "17:00",
                "17:01",
                "17:05",
                "17:15",
                "17:25",
                "17:29"
            ]

            trigger_time = datetime.fromisoformat(f"{test_date}T17:00")
            for test_time in times_to_test_true:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                self.assertTrue(is_active)
                self.assertEqual(trigger_time, program.last_triggered)

            times_to_test_false = [
                "17:30",
                "17:31",
                "17:35",
                "18:00",
                "19:00"
            ]
            for test_time in times_to_test_false:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                if test_dt >= datetime.fromisoformat("2025-04-08 17:30:00"):
                    pass
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                self.assertFalse(is_active)


class Weekends(unittest.TestCase):
    def test_weekends(self):
        program = Program(
            trigger = Trigger.week_ends,
            start_time = datetime.fromisoformat("1970-01-01T17:00:00"),
            duration = timedelta(minutes=30),
            week_day= DayOfWeek.sunday,
            enabled= True
        )

        for test_date in dates_to_test:
            d = datetime.fromisoformat(f"{test_date}T00:00:01")
            dow = DayOfWeek(d.weekday())
            logging.info(f"Testing date {d}({dow.to_long()})")

            times_to_test_false = [
                "04:00",
                "04:30",
                "04:59",
                "05:00",
                "05:01",
                "12:00",
                "16:00",
                "16:30",
                "16:59"
            ]
            for test_time in times_to_test_false:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                self.assertFalse(is_active)
            
            times_to_test_true = [
                "17:00",
                "17:01",
                "17:05",
                "17:15",
                "17:25",
                "17:29"
            ]

            trigger_time = datetime.fromisoformat(f"{test_date}T17:00")
            for test_time in times_to_test_true:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                if dow in (DayOfWeek.sunday, DayOfWeek.saturday) :
                    self.assertTrue(is_active)
                    self.assertEqual(trigger_time, program.last_triggered)
                else:
                    self.assertFalse(is_active)

            times_to_test_false = [
                "17:30",
                "17:31",
                "17:35",
                "18:00",
                "19:00"
            ]
            for test_time in times_to_test_false:
                test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
                is_active = program.is_active(test_dt)
                logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
                self.assertFalse(is_active)

class MidnightCrossing(unittest.TestCase):
    def test_late_night(self):
        program = Program(
            trigger = Trigger.daily,
            start_time = datetime.fromisoformat("1970-01-01 23:30"),
            duration = timedelta(minutes=60),
            week_day= DayOfWeek.sunday,
            enabled= True
        )

        d_now = datetime.now().date()
        test_date = str(d_now)

        d = datetime.fromisoformat(f"{test_date}T00:00:01")
        dow = DayOfWeek(d.weekday())
        logging.info(f"Testing date {d}({dow.to_long()})")

        times_to_test_false = [
            "22:00",
            "22:30",
            "23:28",
            "23:29",
        ]
        for test_time in times_to_test_false:
            test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
            is_active = program.is_active(test_dt)
            logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
            self.assertFalse(is_active)
        
        times_to_test_true = [
            "23:30",
            "23:31",
            "23:45",
            "23:59",
        ]

        for test_time in times_to_test_true:
            test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
            is_active = program.is_active(test_dt)
            logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
            self.assertTrue(is_active)
        
        d_now = d_now + timedelta(days=1)
        test_date = str(d_now)
        
        times_to_test_true = [
            "00:01",
            "00:02",
            "00:15",
            "00:28",
            "00:29"
        ]

        for test_time in times_to_test_true:
            test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
            is_active = program.is_active(test_dt)
            logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
            self.assertTrue(is_active)

        times_to_test_false = [
            "00:30",
            "00:31",
            "00:32",
            "00:45",
            "05:30"
        ]


        for test_time in times_to_test_false:
            test_dt = datetime.fromisoformat(f"{test_date}T{test_time}:00")
            is_active = program.is_active(test_dt)
            logging.info(f"Testing at {test_dt}, state: {program.get_state_h()}")
            self.assertFalse(is_active)
                

if __name__ == "__main__":
    unittest.main(verbosity=2)
