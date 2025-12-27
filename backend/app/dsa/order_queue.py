from typing import List, Optional, Dict, Any
from enum import Enum


class OrderType(Enum):
    """Enumeration for order types."""
    BUY = "BUY"
    SELL = "SELL"


class Order:
    """Represents a trading order."""
    
    def __init__(self, order_id: str, order_type: OrderType, symbol: str, 
                 quantity: float, price: float, timestamp: Optional[int] = None,
                 leader_id: Optional[str] = None):
        """
        Initialize an order.
        
        Args:
            order_id: Unique identifier for the order
            order_type: BUY or SELL
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
            quantity: Amount of the asset
            price: Price per unit
            timestamp: Optional timestamp for the order
            leader_id: Optional ID of the leader who created this order
        """
        self.order_id = order_id
        self.order_type = order_type
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.leader_id = leader_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert order to dictionary."""
        return {
            'order_id': self.order_id,
            'order_type': self.order_type.value,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.timestamp,
            'leader_id': self.leader_id,
        }


class OrderQueue:
    """
    A FIFO (First-In-First-Out) queue implementation for handling trading orders.
    Orders are processed in the order they were added.
    """
    
    def __init__(self):
        """Initialize an empty order queue."""
        self.queue: List[Order] = []
    
    def enqueue(self, order: Order) -> None:
        """
        Add an order to the end of the queue (FIFO).
        
        Args:
            order: The order to add to the queue
        """
        self.queue.append(order)
    
    def dequeue(self) -> Optional[Order]:
        """
        Remove and return the order at the front of the queue (FIFO).
        
        Returns:
            The oldest order in the queue, or None if queue is empty
        """
        if self.is_empty():
            return None
        
        # Remove and return the first element (oldest order)
        return self.queue.pop(0)
    
    def peek(self) -> Optional[Order]:
        """
        Return the front order without removing it.
        
        Returns:
            The oldest order in the queue, or None if queue is empty
        """
        if self.is_empty():
            return None
        return self.queue[0]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.queue) == 0
    
    def size(self) -> int:
        """Return the number of orders in the queue."""
        return len(self.queue)
    
    def get_all(self) -> List[Order]:
        """
        Get all orders in the queue (in order from oldest to newest).
        
        Returns:
            List of all orders in the queue
        """
        return self.queue.copy()
    
    def clear(self) -> None:
        """Remove all orders from the queue."""
        self.queue.clear()

