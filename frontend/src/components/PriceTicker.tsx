import { useEffect, useState } from 'react'
import axios from 'axios'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface PriceData {
  symbol: string
  price: number
  bid: number
  ask: number
  high: number
  low: number
  volume: number
  timestamp: number
}

const PriceTicker = () => {
  const [priceData, setPriceData] = useState<PriceData | null>(null)
  const [previousPrice, setPreviousPrice] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPrice = async () => {
      try {
        const response = await axios.get<PriceData>('http://localhost:8000/api/price/BTC/USDT')
        setPreviousPrice(priceData?.price || null)
        setPriceData(response.data)
        setLoading(false)
        setError(null)
      } catch (err) {
        console.error('Error fetching price:', err)
        setError('Failed to fetch price data')
        setLoading(false)
      }
    }

    // Fetch immediately
    fetchPrice()

    // Then poll every 2 seconds
    const interval = setInterval(fetchPrice, 2000)

    return () => clearInterval(interval)
  }, [priceData?.price])

  const priceChange = priceData && previousPrice 
    ? priceData.price - previousPrice 
    : 0
  const priceChangePercent = priceData && previousPrice 
    ? ((priceChange / previousPrice) * 100).toFixed(2)
    : '0.00'

  const isPositive = priceChange >= 0

  return (
    <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-6 shadow-2xl">
      <h2 className="text-2xl font-semibold text-white mb-4">Bitcoin Price</h2>
      
      {loading && !priceData && (
        <div className="text-slate-400">Loading price data...</div>
      )}
      
      {error && (
        <div className="text-red-400">{error}</div>
      )}
      
      {priceData && (
        <div className="space-y-4">
          {/* Main Price Display */}
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">{priceData.symbol}</p>
              <div className="flex items-center gap-3">
                <span className="text-4xl font-bold text-white">
                  ${priceData.price.toLocaleString('en-US', { 
                    minimumFractionDigits: 2, 
                    maximumFractionDigits: 2 
                  })}
                </span>
                {previousPrice !== null && (
                  <div className={`flex items-center gap-1 ${
                    isPositive ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {isPositive ? (
                      <TrendingUp className="w-5 h-5" />
                    ) : (
                      <TrendingDown className="w-5 h-5" />
                    )}
                    <span className="font-semibold">
                      {isPositive ? '+' : ''}{priceChangePercent}%
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Price Details Grid */}
          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/10">
            <div>
              <p className="text-slate-400 text-sm mb-1">Bid</p>
              <p className="text-white font-medium">
                ${priceData.bid.toLocaleString('en-US', { 
                  minimumFractionDigits: 2, 
                  maximumFractionDigits: 2 
                })}
              </p>
            </div>
            <div>
              <p className="text-slate-400 text-sm mb-1">Ask</p>
              <p className="text-white font-medium">
                ${priceData.ask.toLocaleString('en-US', { 
                  minimumFractionDigits: 2, 
                  maximumFractionDigits: 2 
                })}
              </p>
            </div>
            <div>
              <p className="text-slate-400 text-sm mb-1">24h High</p>
              <p className="text-white font-medium">
                ${priceData.high.toLocaleString('en-US', { 
                  minimumFractionDigits: 2, 
                  maximumFractionDigits: 2 
                })}
              </p>
            </div>
            <div>
              <p className="text-slate-400 text-sm mb-1">24h Low</p>
              <p className="text-white font-medium">
                ${priceData.low.toLocaleString('en-US', { 
                  minimumFractionDigits: 2, 
                  maximumFractionDigits: 2 
                })}
              </p>
            </div>
            <div className="col-span-2">
              <p className="text-slate-400 text-sm mb-1">24h Volume</p>
              <p className="text-white font-medium">
                {priceData.volume.toLocaleString('en-US', { 
                  minimumFractionDigits: 2, 
                  maximumFractionDigits: 2 
                })} BTC
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PriceTicker

