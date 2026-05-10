"""Memory register service — M+, M-, MR, MC operations."""


class MemoryService:
    """Manages a single memory register for the calculator."""

    def __init__(self) -> None:
        self._value: float = 0.0

    @property
    def value(self) -> float:
        return self._value

    @property
    def has_value(self) -> bool:
        return self._value != 0.0

    def store(self, value: float) -> None:
        """MC + MS: overwrite memory with value."""
        self._value = float(value)

    def add(self, value: float) -> None:
        """M+: add value to memory."""
        self._value += float(value)

    def subtract(self, value: float) -> None:
        """M-: subtract value from memory."""
        self._value -= float(value)

    def recall(self) -> float:
        """MR: return memory value."""
        return self._value

    def clear(self) -> None:
        """MC: reset memory to zero."""
        self._value = 0.0
