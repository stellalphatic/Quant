from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.market_data import MarketDataService

app = FastAPI(title="AlgoTrading API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the market data service
market_data_service = MarketDataService()


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

