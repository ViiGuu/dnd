import json

class HarptosCalendar:
    months = [
        "Hammer",      # 1
        "Alturiak",    # 2
        "Ches",        # 3
        "Tarsakh",     # 4
        "Mirtul",      # 5
        "Kythorn",     # 6
        "Flamerule",   # 7
        "Eleasis",     # 8
        "Eleint",      # 9
        "Marpenoth",   #10
        "Uktar",       #11
        "Nightal"      #12
    ]
    days_per_month = 30

    def __init__(self, year, month, day, hour=0):
        self.year = year
        self.hour = hour
        # We start with a “normal” day (month 1..12, day 1..30)
        self.month = month
        self.day = day
        self.is_festival = False
        self.festival_name = None
        # Internally, we track an absolute day-of-year which includes the festivals.
        self.absolute_day = self.normal_to_absolute(month, day)
        self.update_state()

    def is_leap_year(self):
        return self.year % 4 == 0

    def total_days_in_year(self):
        # There are 360 regular days plus:
        # 5 festival days in a non-leap year and 6 in a leap year.
        return 360 + (6 if self.is_leap_year() else 5)

    def get_festival_days_num(self):
        # These are the absolute day numbers for the festivals.
        # (They are determined by the Harptos ordering:
        #   Hammer (30 days) → Midwinter → Alturiak (30 days) → Ches (30) → Tarsakh (30)
        #   → Greengrass → Mirtul (30) → Kythorn (30) → Flamerule (30)
        #   → Midsummer [and Shieldmeet in leap years] → Eleasis (30) → Eleint (30)
        #   → Highharvestide → Marpenoth (30) → Uktar (30) → Feast of the Moon → Nightal (30))
        if self.is_leap_year():
            return [
                ("Midwinter", 31),
                ("Greengrass", 122),
                ("Midsummer", 213),
                ("Shieldmeet", 214),
                ("Highharvestide", 275),
                ("Feast of the Moon", 336)
            ]
        else:
            return [
                ("Midwinter", 31),
                ("Greengrass", 122),
                ("Midsummer", 213),
                ("Highharvestide", 274),
                ("Feast of the Moon", 335)
            ]

    def normal_to_absolute(self, month, day):
        """
        Converts a normal date (month and day) into an absolute day-of-year.
        (This “offset” adds in all the festival days that come before the given month.)
        """
        offset = 0
        if month > 1:
            offset += 1  # Midwinter (after Hammer)
        if month > 4:
            offset += 1  # Greengrass (after Tarsakh)
        if month > 7:
            # After Flamerule comes Midsummer, and in leap years Shieldmeet too.
            offset += (2 if self.is_leap_year() else 1)
        if month > 9:
            offset += 1  # Highharvestide (after Eleint)
        if month > 11:
            offset += 1  # Feast of the Moon (after Uktar)
        return (month - 1) * self.days_per_month + day + offset

    def update_state(self):
        """
        Given the current absolute_day and year, determine if today is a festival
        (and, if so, which one) or a normal day. If it is a normal day, recalculate month/day.
        """
        # First, check for festivals.
        for fest_name, fest_day in self.get_festival_days_num():
            if self.absolute_day == fest_day:
                self.is_festival = True
                self.festival_name = fest_name
                return

        # Otherwise, it’s a normal day.
        self.is_festival = False
        self.festival_name = None

        # Now we “invert” the normal_to_absolute mapping.
        # The normal days fall into blocks whose start/end depend on the festival positions.
        if self.is_leap_year():
            blocks = [
                (1, 30, 1),       # Hammer
                (32, 61, 2),      # Alturiak (since day 31 is Midwinter)
                (62, 91, 3),      # Ches
                (92, 121, 4),     # Tarsakh
                (123, 152, 5),    # Mirtul
                (153, 182, 6),    # Kythorn
                (183, 212, 7),    # Flamerule
                (215, 244, 8),    # Eleasis (213 = Midsummer, 214 = Shieldmeet)
                (245, 274, 9),    # Eleint
                (276, 305, 10),   # Marpenoth
                (306, 335, 11),   # Uktar
                (337, 366, 12)    # Nightal
            ]
        else:
            blocks = [
                (1, 30, 1),       # Hammer
                (32, 61, 2),      # Alturiak
                (62, 91, 3),      # Ches
                (92, 121, 4),     # Tarsakh
                (123, 152, 5),    # Mirtul
                (153, 182, 6),    # Kythorn
                (183, 212, 7),    # Flamerule
                (214, 243, 8),    # Eleasis (213 is Midsummer)
                (244, 273, 9),    # Eleint
                (275, 304, 10),   # Marpenoth
                (305, 334, 11),   # Uktar
                (336, 365, 12)    # Nightal
            ]
        for start, end, m in blocks:
            if start <= self.absolute_day <= end:
                self.month = m
                self.day = self.absolute_day - start + 1
                return

    def progress_hours(self, hours):
        self.hour += hours
        extra_days = self.hour // 24
        self.hour %= 24
        if extra_days:
            self.progress_days(extra_days)

    def progress_days(self, days):
        for _ in range(days):
            self.increment_day()

    def increment_day(self):
        self.absolute_day += 1
        if self.absolute_day > self.total_days_in_year():
            self.absolute_day -= self.total_days_in_year()
            self.year += 1
        self.update_state()

    def progress_months(self, months):
        """
        Advance by a number of months while preserving the day-of-month.
        (If the current day is a festival, first progress one day.)
        """
        if self.is_festival:
            self.increment_day()
            months -= 1
        for _ in range(months):
            cur_month, cur_day = self.month, self.day
            next_month = cur_month + 1
            next_year = self.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            # Build a temporary calendar for the target date.
            temp = HarptosCalendar(next_year, next_month, cur_day, self.hour)
            self.year, self.month, self.day = temp.year, temp.month, temp.day
            self.hour = temp.hour
            self.absolute_day = temp.absolute_day
            self.is_festival = temp.is_festival
            self.festival_name = temp.festival_name

    def progress_years(self, years):
        self.year += years
        if self.is_festival:
            # Adjust the absolute day to the festival day in the new year.
            for fest_name, fest_day in self.get_festival_days_num():
                if fest_name == self.festival_name:
                    self.absolute_day = fest_day
                    break
        else:
            self.absolute_day = self.normal_to_absolute(self.month, self.day)
        self.update_state()

    def __str__(self):
        if self.is_festival:
            return f"{self.festival_name}, hour {self.hour}, {self.year} DR"
        else:
            return f"{self.day} {self.months[self.month - 1]}, hour {self.hour}, {self.year} DR"
        
    ### SAVE AND LOAD SYSTEM ###
    
    def save_to_file(self, filename="calendar_save.json"):
        """ Saves the current calendar state to a JSON file. """
        data = {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "absolute_day": self.absolute_day,
            "is_festival": self.is_festival,
            "festival_name": self.festival_name
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Calendar saved to {filename}.")

    @classmethod
    def load_from_file(cls, filename="calendar_save.json"):
        """ Loads the calendar state from a JSON file. """
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            cal = cls(data["year"], data["month"], data["day"], data["hour"])
            cal.absolute_day = data["absolute_day"]
            cal.is_festival = data["is_festival"]
            cal.festival_name = data["festival_name"]
            cal.update_state()  # Ensure everything is consistent
            print(f"Calendar loaded from {filename}.")
            return cal
        except FileNotFoundError:
            print(f"Save file {filename} not found. Creating a new calendar instance.")
            return cls(1491, 1, 1)


# === Testing the fixed calendar ===
# if __name__ == '__main__':
#     # Test 1: Normal year
#     calendar = HarptosCalendar(1491, 1, 30)  # 30 Hammer, 1491 DR
#     print(calendar)  # Expected: "30 Hammer, 1491 DR"

#     calendar.progress_days(1)
#     print(calendar)  # Expected: "Midwinter, 1491 DR"

#     calendar.progress_days(1)
#     print(calendar)  # Expected: "1 Alturiak, 1491 DR"

#     # Test 2: Leap year (1492 is a leap year)
#     calendar = HarptosCalendar(1492, 7, 30)  # 30 Flamerule, 1492 DR (Leap Year)
#     print(calendar)  # Expected: "30 Flamerule, 1492 DR"

#     calendar.progress_days(1)
#     print(calendar)  # Expected: "Midsummer, 1492 DR"

#     calendar.progress_days(1)
#     print(calendar)  # Expected: "Shieldmeet, 1492 DR"

#     calendar.progress_days(1)
#     print(calendar)  # Expected: "1 Eleasis, 1492 DR"

#     # Test 3: Year transition
#     calendar = HarptosCalendar(1491, 12, 30)  # 30 Nightal, 1491 DR
#     print(calendar)  # Expected: "30 Nightal, 1491 DR"

#     calendar.progress_days(1)
#     print(calendar)  # Expected: "1 Hammer, 1492 DR"

#     calendar.progress_hours(5)
#     print(calendar)

#         # Create a calendar and advance a few days
#     calendar = HarptosCalendar(1491, 1, 30)
#     print(calendar)  # Output: 30 Hammer, 1491 DR

#     calendar.progress_days(2)  # Move forward 2 days (to 1 Alturiak, 1491 DR)
#     print(calendar)  # Output: 1 Alturiak, 1491 DR

#     # Save the current state
#     calendar.save_to_file()

#     # Load the calendar from the save file
#     loaded_calendar = HarptosCalendar.load_from_file()
#     print(loaded_calendar)  # Should match the last saved state (1 Alturiak, 1491 DR)

