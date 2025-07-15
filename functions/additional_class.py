from datetime import date, timedelta

class ExtendedDate(date):
    @classmethod
    def from_date(cls, date_obj):
        """Create an ExtendedDate from a standard date object."""
        return cls(date_obj.year, date_obj.month, date_obj.day)

    def to_date(self):
        """Return a standard Python date object from the ExtendedDate."""
        return date(self.year, self.month, self.day)    
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            # Handle addition of an integer or float by converting to timedelta
            return super().__add__(timedelta(days=int(other)))
        elif isinstance(other, timedelta):
            # Handle addition of timedelta
            return super().__add__(other)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            # Handle subtraction of an integer or float by converting to timedelta
            return super().__sub__(timedelta(days=int(other)))
        elif isinstance(other, timedelta):
            # Handle subtraction of timedelta
            return super().__sub__(other)
        elif isinstance(other, (date, ExtendedDate)):
            # Handle subtraction of another date/ExtendedDate instance
            return super().__sub__(other).days
        return NotImplemented
    
    def __le__(self, __value: date) -> bool:
        if not __value:
            return None
        return super().__le__(__value)
    
    def __lt__(self, __value: date) -> bool:
        if not __value:
            return None
        return super().__lt__(__value)