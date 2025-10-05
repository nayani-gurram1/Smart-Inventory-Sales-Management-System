# src/models/customer.py
from typing import Optional
from datetime import datetime

class Customer:
    def __init__(self, cust_id: Optional[int] = None, name: str = "", email: str = "",
                 phone: str = "", city: Optional[str] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.cust_id = cust_id
        self.name = name
        self.email = email
        self.phone = phone
        self.city = city
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    # -------------------------------
    # Validations
    # -------------------------------
    def is_valid_email(self) -> bool:
        """Check if email has basic valid format."""
        import re
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, self.email))

    def is_valid_phone(self) -> bool:
        """Check if phone number is numeric and 7-15 digits."""
        return self.phone.isdigit() and 7 <= len(self.phone) <= 15

    def validate(self) -> bool:
        """Return True if all validations pass."""
        return self.is_valid_email() and self.is_valid_phone() and bool(self.name)

    # -------------------------------
    # Utility Methods
    # -------------------------------
    def to_dict(self) -> dict:
        """Convert Customer object to dictionary."""
        return {
            "cust_id": self.cust_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "city": self.city,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Customer object from dictionary."""
        return cls(
            cust_id=data.get("cust_id"),
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            city=data.get("city"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    # -------------------------------
    # Display Methods
    # -------------------------------
    def __str__(self):
        return f"{self.name} ({self.email}) - {self.phone}"

    def short_info(self):
        return f"{self.cust_id}: {self.name} ({self.city or 'N/A'})"

