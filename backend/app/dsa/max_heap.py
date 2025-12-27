from typing import List, Optional, Dict, Any


class Trader:
    """Represents a trader with their ROI information."""
    
    def __init__(self, trader_id: str, name: str, roi: float, portfolio_value: float = 0.0):
        """
        Initialize a trader.
        
        Args:
            trader_id: Unique identifier for the trader
            name: Trader's name
            roi: Return on Investment percentage
            portfolio_value: Total portfolio value in USDT
        """
        self.trader_id = trader_id
        self.name = name
        self.roi = roi
        self.portfolio_value = portfolio_value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trader to dictionary."""
        return {
            'trader_id': self.trader_id,
            'name': self.name,
            'roi': self.roi,
            'portfolio_value': self.portfolio_value,
        }
    
    def __lt__(self, other: 'Trader') -> bool:
        """Less than comparison for heap operations."""
        return self.roi < other.roi
    
    def __gt__(self, other: 'Trader') -> bool:
        """Greater than comparison for heap operations."""
        return self.roi > other.roi


class LeaderboardHeap:
    """
    A Max-Heap implementation to manage traders sorted by their ROI.
    The trader with the highest ROI is always at the root.
    """
    
    def __init__(self):
        """Initialize an empty max-heap."""
        self.heap: List[Trader] = []
    
    def _parent_index(self, index: int) -> int:
        """Get the parent index of a given node index."""
        return (index - 1) // 2
    
    def _left_child_index(self, index: int) -> int:
        """Get the left child index of a given node index."""
        return 2 * index + 1
    
    def _right_child_index(self, index: int) -> int:
        """Get the right child index of a given node index."""
        return 2 * index + 2
    
    def _swap(self, i: int, j: int) -> None:
        """Swap two elements in the heap."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _heapify_up(self, index: int) -> None:
        """
        Move an element up the heap to maintain max-heap property.
        Used after inserting a new element.
        """
        while index > 0:
            parent_idx = self._parent_index(index)
            
            # If current node is greater than parent, swap
            if self.heap[index].roi > self.heap[parent_idx].roi:
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break
    
    def _heapify_down(self, index: int) -> None:
        """
        Move an element down the heap to maintain max-heap property.
        Used after extracting the root.
        """
        while True:
            largest = index
            left = self._left_child_index(index)
            right = self._right_child_index(index)
            
            # Compare with left child
            if left < len(self.heap) and self.heap[left].roi > self.heap[largest].roi:
                largest = left
            
            # Compare with right child
            if right < len(self.heap) and self.heap[right].roi > self.heap[largest].roi:
                largest = right
            
            # If largest is not the current node, swap and continue
            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break
    
    def insert(self, trader: Trader) -> None:
        """
        Insert a new trader into the max-heap.
        
        Args:
            trader: The trader to insert
        """
        # Add trader to the end of the heap
        self.heap.append(trader)
        
        # Restore max-heap property by moving the new element up
        self._heapify_up(len(self.heap) - 1)
    
    def extract_max(self) -> Optional[Trader]:
        """
        Extract and return the trader with the highest ROI (root of max-heap).
        
        Returns:
            The trader with the highest ROI, or None if heap is empty
        """
        if self.is_empty():
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # Store the root (max element)
        max_trader = self.heap[0]
        
        # Move the last element to the root
        self.heap[0] = self.heap.pop()
        
        # Restore max-heap property by moving the root down
        self._heapify_down(0)
        
        return max_trader
    
    def peek_max(self) -> Optional[Trader]:
        """
        Return the trader with the highest ROI without removing it.
        
        Returns:
            The trader with the highest ROI, or None if heap is empty
        """
        if self.is_empty():
            return None
        return self.heap[0]
    
    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Return the number of traders in the heap."""
        return len(self.heap)
    
    def get_all_sorted(self) -> List[Trader]:
        """
        Get all traders sorted by ROI (highest to lowest) without modifying the heap.
        Note: This creates a copy and sorts it, so it doesn't affect the heap structure.
        
        Returns:
            List of all traders sorted by ROI (descending)
        """
        # Create a copy to avoid modifying the original heap
        traders = [trader for trader in self.heap]
        traders.sort(key=lambda t: t.roi, reverse=True)
        return traders

