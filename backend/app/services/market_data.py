import ccxt
from typing import Dict, Any
from app.dsa.circular_buffer import CircularBuffer


class MarketDataService:
    """Service for fetching market data from cryptocurrency exchanges."""
    
    def __init__(self):
        """Initialize the Binance exchange instance."""
        self.exchange = ccxt.binance({
            'apiKey': None,  # Not needed for public data
            'secret': None,  # Not needed for public data
            'enableRateLimit': True,  # Respect rate limits
        })
        # Dictionary to store CircularBuffer for each symbol
        # Each buffer stores the last 50 historical prices
        self.price_buffers: Dict[str, CircularBuffer] = {}
    
    def _get_or_create_buffer(self, symbol: str) -> CircularBuffer:
        """
        Get or create a CircularBuffer for a given symbol.
        
        Args:
            symbol: Trading pair symbol
        
        Returns:
            CircularBuffer instance for the symbol
        """
        if symbol not in self.price_buffers:
            self.price_buffers[symbol] = CircularBuffer(size=50)
        return self.price_buffers[symbol]
    
    def get_live_price(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch the live ticker price for a given symbol from Binance.
        Automatically stores the price in the CircularBuffer for historical tracking.
        
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
            
            current_price = ticker['last']
            
            # Store price in CircularBuffer for historical tracking
            buffer = self._get_or_create_buffer(symbol)
            buffer.add(current_price)
            
            # Return relevant price information
            return {
                'symbol': symbol,
                'price': current_price,
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high': ticker['high'],
                'low': ticker['low'],
                'volume': ticker['baseVolume'],
                'timestamp': ticker['timestamp'],
            }
        except Exception as e:
            raise Exception(f"Failed to fetch price for {symbol}: {str(e)}")
    
    def get_historical_prices(self, symbol: str) -> list:
        """
        Get historical prices for a symbol from the CircularBuffer.
        
        Args:
            symbol: Trading pair symbol
        
        Returns:
            List of historical prices (up to 50 most recent)
        """
        if symbol not in self.price_buffers:
            return []
        return self.price_buffers[symbol].get_all()

