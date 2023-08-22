from abc import ABC, abstractmethod
from dataclasses import dataclass

class Calendar(ABC):
    __slots__ = ['year','month','day']

    @abstractmethod
    def days_in_year(self,year):
        pass

    @abstractmethod
    def months_in_year(self,year):
        pass

    @abstractmethod
    def days_in_month(self,year,month):
        pass

    def __init__(self,year,month,day):
        if not isinstance(year,int):
            raise ValueError("Year must be an integer")
        if not (isinstance(month,int) and 1 <= month <= self.months_in_year(year)):
            raise ValueError("Month must be a valid integer")
        if not (isinstance(day,int) and 1 <= day <= self.days_in_month(year,month)):
            raise ValueError("Day must be a valid integer")

        self.year = year
        self.month = month
        self.day = day

    def __add__(self, other):
        if not isinstance(other,CalendarDelta):
            raise TypeError

        rem_days = other.days
        year, month, day = self.year, self.month, self.day

        days_left = self.days_in_year(year)
        for i in range(1,month):
            days_left -= self.days_in_month(year,i)
        days_left -= day -1
        if days_left <= rem_days:
            rem_days -= days_left
            year, month, day = year+1, 1, 1

            while True:
                days_in_year = self.days_in_year(year)
                if rem_days < days_in_year:
                    break
                rem_days -= days_in_year
                year += 1

            while True:
                days_in_month = self.days_in_month(year,month)
                if rem_days < days_in_month:
                    break
                rem_days -= days_in_month
                month += 1
        else:
            days_in_month = self.days_in_month(year, month)
            while True:
                if rem_days > 0:
                    if day == days_in_month:
                        month += 1
                        day = 1
                        days_in_month = self.days_in_month(year, month)
                    else:
                        day += 1
                    rem_days -= 1
                else:
                    break

        day += rem_days

        return self.__class__(year,month,day)

    def __eq__(self, other):
        if isinstance(other, Calendar):
            return vars(self) == vars(other)
        return False

    def __lt__(self, other):
        if not isinstance(other,Calendar):
            raise TypeError

        if self.year != other.year:
            return self.year < other.year
        elif self.month != other.month:
            return self.month < other.month
        else:
            return self.day < other.day

    def __sub__(self, other):
        if not isinstance(other,Calendar):
            raise TypeError

        neg = False

        if self < other:
            byear, bmonth, bday = other.year, other.month, other.day
            syear, smonth, sday = self.year, self.month, self.day
            neg = True
        else:
            byear, bmonth, bday = self.year, self.month, self.day
            syear, smonth, sday = other.year, other.month, other.day

        difference = 0

        if syear != byear:
            days_left = self.days_in_year(syear)
            for i in range(1, smonth):
                days_left -= self.days_in_month(syear, i)
            days_left -= sday
            difference += days_left+1
            syear, smonth, sday = syear+1, 1, 1

            while syear != byear:
                difference += self.days_in_year(syear)
                syear += 1

            while smonth != bmonth:
                difference += self.days_in_month(syear, smonth)
                smonth += 1

            difference += bday - sday

        else:
            days_in_month = self.days_in_month(syear, smonth)
            while (smonth,sday) != (bmonth,bday):
                if sday == days_in_month:
                    smonth += 1
                    sday = 1
                    days_in_month = self.days_in_month(syear, smonth)
                else:
                    sday += 1
                difference += 1

        return CalendarDelta(difference*(-1 if neg else 1))

    def __str__(self):
        return f'{self.year}-{self.month}-{self.day}'


@dataclass
class CalendarDelta():
    days: int