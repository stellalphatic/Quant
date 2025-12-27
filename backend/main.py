import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.services.market_data import MarketDataService
from app.services.copy_service import CopyService
from app.models.trader import TraderCreate, TraderResponse
from app.dsa.order_queue import OrderType

app = FastAPI(title="AlgoTrading API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
market_data_service = MarketDataService()
copy_service = CopyService()


# Background task to continuously process orders
async def process_orders_continuously():
    """Background task that continuously processes orders from the queue."""
    while True:
        try:
            if not copy_service.order_queue.is_empty():
                results = copy_service.process_orders_for_followers()
                if results:
                    print(f"Processed {len(results)} orders for followers")
            # Sleep for 1 second before checking again
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error processing orders: {e}")
            await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    """Start background task when application starts."""
    asyncio.create_task(process_orders_continuously())


# Request models
class TradeExecuteRequest(BaseModel):
    leader_id: str
    order_type: str  # "BUY" or "SELL"
    symbol: str
    quantity: float
    price: float


class FollowRequest(BaseModel):
    leader_id: str
    follower_id: str


@app.get("/")
async def hello_world():
    """Hello World route."""
    return {"message": "Hello World"}


@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    """
    Get live price for a cryptocurrency symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTC/USDT', 'ETH/USDT')
    
    Returns:
        Price data for the specified symbol
    """
    try:
        price_data = market_data_service.get_live_price(symbol)
        return price_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/traders", response_model=TraderResponse)
async def register_trader(trader_data: TraderCreate):
    """
    Register a new trader.
    
    Args:
        trader_data: Trader information
    
    Returns:
        Created trader with ID
    """
    try:
        trader = copy_service.register_trader(trader_data)
        return TraderResponse(
            trader_id=trader.trader_id,
            name=trader.name,
            roi=trader.roi,
            portfolio_value=trader.portfolio_value
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/leaders/{leader_id}/trade")
async def execute_leader_trade(leader_id: str, trade_request: TradeExecuteRequest):
    """
    Execute a trade as a leader. This will push the order to the queue for followers.
    
    Args:
        leader_id: ID of the leader trader
        trade_request: Trade details
    
    Returns:
        Created order information
    """
    try:
        # Validate order type
        order_type = OrderType.BUY if trade_request.order_type.upper() == "BUY" else OrderType.SELL
        
        order = copy_service.execute_leader_trade(
            leader_id=leader_id,
            order_type=order_type,
            symbol=trade_request.symbol,
            quantity=trade_request.quantity,
            price=trade_request.price
        )
        
        return {
            "message": "Trade order queued successfully",
            "order": order.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/leaderboard")
async def get_leaderboard():
    """
    Get the top 5 traders from the leaderboard.
    
    Returns:
        List of top 5 traders sorted by ROI
    """
    try:
        top_traders = copy_service.get_top_traders(limit=5)
        
        return {
            "top_traders": [
                {
                    "trader_id": trader.trader_id,
                    "name": trader.name,
                    "roi": trader.roi,
                    "portfolio_value": trader.portfolio_value
                }
                for trader in top_traders
            ],
            "count": len(top_traders)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/follow")
async def follow_leader(follow_request: FollowRequest):
    """
    Add a follower to a leader.
    
    Args:
        follow_request: Leader and follower IDs
    
    Returns:
        Success message
    """
    try:
        success = copy_service.add_follower(
            leader_id=follow_request.leader_id,
            follower_id=follow_request.follower_id
        )
        
        if success:
            return {
                "message": f"Follower {follow_request.follower_id} is now following leader {follow_request.leader_id}",
                "leader_id": follow_request.leader_id,
                "follower_id": follow_request.follower_id
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Leader or follower not found"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

