from abc import ABC, abstractmethod

class FinancialEntity(ABC):
    """
    Abstract base class for financial items in the budgeting system.
    Used for inheritance + polymorphism in Project 3.
    """

    @abstractmethod
    def calculate_balance_effect(self) -> float:
        """How this entity changes the user's balance."""
        pass

    @abstractmethod
    def summary(self) -> str:
        """Human-readable description for reports and logs."""
        pass
