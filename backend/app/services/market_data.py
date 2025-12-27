import ccxt
from typing import Dict, Any


class MarketDataService:
    """Service for fetching market data from cryptocurrency exchanges."""
    
    def __init__(self):
        """Initialize the Binance exchange instance."""
        self.exchange = ccxt.binance({
            'apiKey': None,  # Not needed for public data
            'secret': None,  # Not needed for public data
            'enableRateLimit': True,  # Respect rate limits
        })
    
    def get_live_price(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch the live ticker price for a given symbol from Binance.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT', 'ETH/USDT')
        
        Returns:
            Dictionary containing price information
        
        Raises:
            Exception: If the symbol is invalid or the API call fails
        """
        try:
            # Fetch ticker data
            ticker = self.exchange.fetch_ticker(symbol)
            
            # Return relevant price information
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high': ticker['high'],
                'low': ticker['low'],
                'volume': ticker['baseVolume'],
                'timestamp': ticker['timestamp'],
            }
        except Exception as e:
            raise Exception(f"Failed to fetch price for {symbol}: {str(e)}")

