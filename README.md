# Fantasy Calendar Class
Python abstract class that supports any fantasy calendar, being useful for worldbuilding

## Features
It currently supports addition, subtraction and comparison of dates, analogous to datetime. When creating a calendar, one must inherit from the `Calendar` class and define 3 methods: `days_in_year`, `months_in_year`, `days_in_month`.

## Example code
```python
class GregorianCalendar(Calendar):

    # Optional method
    def is_leap_year(self,year):
        if year%400 == 0:
            return True
        elif year%100 == 0:
            return False
        elif year%4 == 0:
            return True
        else:
            return False

    def days_in_year(self,year):
        return (366 if self.is_leap_year(year) else 365)

    def months_in_year(self,year):
        return 12

    def days_in_month(self,year,month):
        if self.is_leap_year(year):
            return [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
        else:
            return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]

date1 = GregorianCalendar(2023,8,21)
date2 = GregorianCalendar(2022,7,31)
some_interval = CalendarDelta(days=24)

print(f'Difference: {date1 - date2}')        # 386 days
print(f'Addition: {date1 + some_interval}')  # 2023-9-14
```
