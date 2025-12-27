from typing import List, Optional, Any


class CircularBuffer:
    """
    A fixed-size circular buffer to store the last N historical prices.
    When the buffer is full, new items overwrite the oldest ones.
    """
    
    def __init__(self, size: int = 50):
        """
        Initialize the circular buffer.
        
        Args:
            size: Maximum number of items to store (default: 50)
        """
        self.size = size
        self.buffer: List[Optional[Any]] = [None] * size
        self.write_index = 0
        self.count = 0  # Track how many items have been added
    
    def add(self, price: float) -> None:
        """
        Add a new price to the buffer.
        If the buffer is full, overwrites the oldest entry.
        
        Args:
            price: The price value to add
        """
        self.buffer[self.write_index] = price
        self.write_index = (self.write_index + 1) % self.size
        
        if self.count < self.size:
            self.count += 1
    
    def get_all(self) -> List[float]:
        """
        Get all stored prices in chronological order (oldest to newest).
        
        Returns:
            List of all prices stored in the buffer
        """
        if self.count == 0:
            return []
        
        result: List[float] = []
        
        if self.count < self.size:
            # Buffer is not full yet, return items from index 0 to count
            for i in range(self.count):
                if self.buffer[i] is not None:
                    result.append(self.buffer[i])
        else:
            # Buffer is full, start from write_index (oldest item)
            for i in range(self.size):
                idx = (self.write_index + i) % self.size
                if self.buffer[idx] is not None:
                    result.append(self.buffer[idx])
        
        return result
    
    def is_full(self) -> bool:
        """Check if the buffer is full."""
        return self.count == self.size
    
    def __len__(self) -> int:
        """Return the number of items currently in the buffer."""
        return self.count

