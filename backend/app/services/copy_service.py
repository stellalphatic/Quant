import uuid
import time
from typing import Dict, List, Optional, Any
from app.dsa.order_queue import OrderQueue, Order, OrderType
from app.dsa.max_heap import LeaderboardHeap, Trader
from app.models.trader import TraderCreate, TraderResponse


class CopyService:
    """
    Service for managing copy trading functionality.
    Handles leader trades, follower execution, and trader management.
    """
    
    def __init__(self):
        """Initialize the copy trading service."""
        self.order_queue = OrderQueue()
        self.leaderboard_heap = LeaderboardHeap()
        self.traders: Dict[str, Trader] = {}  # Store traders by trader_id
        self.followers: Dict[str, List[str]] = {}  # Map leader_id -> [follower_ids]
        self.is_processing = False
    
    def register_trader(self, trader_data: TraderCreate, trader_id: Optional[str] = None) -> Trader:
        """
        Register a new trader or update existing trader.
        
        Args:
            trader_data: Trader data from request
            trader_id: Optional trader ID (generated if not provided)
        
        Returns:
            Trader object
        """
        if trader_id is None:
            trader_id = str(uuid.uuid4())
        
        # Create or update trader
        trader = Trader(
            trader_id=trader_id,
            name=trader_data.name,
            roi=trader_data.roi,
            portfolio_value=trader_data.portfolio_value
        )
        
        # If trader exists, remove from heap first before updating
        if trader_id in self.traders:
            # Rebuild heap (simple approach - in production, use update operation)
            self._rebuild_heap()
        
        self.traders[trader_id] = trader
        
        # Add/update in leaderboard heap
        self.leaderboard_heap.insert(trader)
        
        return trader
    
    def _rebuild_heap(self) -> None:
        """Rebuild the heap with current traders."""
        self.leaderboard_heap = LeaderboardHeap()
        for trader in self.traders.values():
            self.leaderboard_heap.insert(trader)
    
    def execute_leader_trade(self, leader_id: str, order_type: OrderType, 
                            symbol: str, quantity: float, price: float) -> Order:
        """
        When a leader executes a trade, push it to the OrderQueue.
        
        Args:
            leader_id: ID of the leader trader
            order_type: BUY or SELL
            symbol: Trading pair symbol
            quantity: Amount to trade
            price: Price per unit
        
        Returns:
            Created Order object
        
        Raises:
            ValueError: If leader_id is not found
        """
        if leader_id not in self.traders:
            raise ValueError(f"Leader with ID {leader_id} not found")
        
        # Create order with leader_id
        order = Order(
            order_id=str(uuid.uuid4()),
            order_type=order_type,
            symbol=symbol,
            quantity=quantity,
            price=price,
            timestamp=int(time.time() * 1000),  # Milliseconds
            leader_id=leader_id
        )
        
        # Push to order queue for followers to copy
        self.order_queue.enqueue(order)
        
        return order
    
    def process_orders_for_followers(self) -> List[Dict[str, Any]]:
        """
        Process orders from the queue and execute for followers.
        This is called by the background task.
        
        Returns:
            List of execution results
        """
        executed_orders = []
        
        while not self.order_queue.is_empty():
            order = self.order_queue.dequeue()
            
            if order is None:
                break
            
            # Execute trade for followers of the specific leader who created this order
            follower_count = 0
            if order.leader_id and order.leader_id in self.followers:
                follower_ids = self.followers[order.leader_id]
                for follower_id in follower_ids:
                    if follower_id in self.traders:
                        # Execute trade for follower
                        result = self._execute_follower_trade(follower_id, order)
                        executed_orders.append(result)
                        follower_count += 1
            
            executed_orders.append({
                'order_id': order.order_id,
                'status': 'processed',
                'symbol': order.symbol,
                'type': order.order_type.value,
                'leader_id': order.leader_id,
                'followers_count': follower_count
            })
        
        return executed_orders
    
    def _execute_follower_trade(self, follower_id: str, order: Order) -> Dict[str, Any]:
        """
        Execute a trade for a follower (simulated).
        
        Args:
            follower_id: ID of the follower
            order: Order to execute
        
        Returns:
            Execution result dictionary
        """
        follower = self.traders.get(follower_id)
        if follower is None:
            return {
                'follower_id': follower_id,
                'status': 'failed',
                'reason': 'Follower not found'
            }
        
        # Simulate trade execution
        # In a real system, this would interact with an exchange API
        trade_value = order.quantity * order.price
        
        # Update follower's portfolio (simplified)
        if order.order_type == OrderType.BUY:
            # Buying: reduce cash, increase holdings
            follower.portfolio_value -= trade_value * 0.001  # Small fee
        else:  # SELL
            # Selling: increase cash, reduce holdings
            follower.portfolio_value += trade_value * 0.999  # Small fee
        
        return {
            'follower_id': follower_id,
            'follower_name': follower.name,
            'order_id': order.order_id,
            'status': 'executed',
            'symbol': order.symbol,
            'type': order.order_type.value,
            'quantity': order.quantity,
            'price': order.price
        }
    
    def add_follower(self, leader_id: str, follower_id: str) -> bool:
        """
        Add a follower to a leader.
        
        Args:
            leader_id: ID of the leader
            follower_id: ID of the follower
        
        Returns:
            True if successful, False otherwise
        """
        if leader_id not in self.traders or follower_id not in self.traders:
            return False
        
        if leader_id not in self.followers:
            self.followers[leader_id] = []
        
        if follower_id not in self.followers[leader_id]:
            self.followers[leader_id].append(follower_id)
        
        return True
    
    def get_top_traders(self, limit: int = 5) -> List[Trader]:
        """
        Get top N traders from the leaderboard heap.
        
        Args:
            limit: Number of top traders to return
        
        Returns:
            List of top traders sorted by ROI (descending)
        """
        # Get all traders sorted by ROI
        sorted_traders = self.leaderboard_heap.get_all_sorted()
        
        # Return top N
        return sorted_traders[:limit]
    
    def get_trader(self, trader_id: str) -> Optional[Trader]:
        """Get a trader by ID."""
        return self.traders.get(trader_id)

