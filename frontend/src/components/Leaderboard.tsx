import { useEffect, useState } from 'react'
import axios from 'axios'
import { Trophy, TrendingUp } from 'lucide-react'

interface Trader {
  trader_id: string
  name: string
  roi: number
  portfolio_value: number
}

interface LeaderboardResponse {
  top_traders: Trader[]
  count: number
}

const Leaderboard = () => {
  const [traders, setTraders] = useState<Trader[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await axios.get<LeaderboardResponse>('http://localhost:8000/api/leaderboard')
        setTraders(response.data.top_traders)
        setLoading(false)
        setError(null)
      } catch (err) {
        console.error('Error fetching leaderboard:', err)
        setError('Failed to fetch leaderboard')
        setLoading(false)
      }
    }

    fetchLeaderboard()

    // Refresh every 5 seconds
    const interval = setInterval(fetchLeaderboard, 5000)

    return () => clearInterval(interval)
  }, [])

  const getRankIcon = (index: number) => {
    switch (index) {
      case 0:
        return <Trophy className="w-5 h-5 text-yellow-400" />
      case 1:
        return <Trophy className="w-5 h-5 text-slate-400" />
      case 2:
        return <Trophy className="w-5 h-5 text-amber-600" />
      default:
        return <span className="text-slate-400 font-semibold">#{index + 1}</span>
    }
  }

  return (
    <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-6 shadow-2xl">
      <div className="flex items-center gap-2 mb-4">
        <Trophy className="w-6 h-6 text-yellow-400" />
        <h2 className="text-2xl font-semibold text-white">Top Traders</h2>
      </div>
      
      {loading && traders.length === 0 && (
        <div className="text-slate-400">Loading leaderboard...</div>
      )}
      
      {error && (
        <div className="text-red-400">{error}</div>
      )}
      
      {traders.length === 0 && !loading && !error && (
        <div className="text-slate-400">No traders found. Register some traders to see the leaderboard!</div>
      )}
      
      {traders.length > 0 && (
        <div className="space-y-3">
          {traders.map((trader, index) => (
            <div
              key={trader.trader_id}
              className="backdrop-blur-md bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-all duration-200"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-8">
                    {getRankIcon(index)}
                  </div>
                  <div>
                    <p className="text-white font-semibold">{trader.name}</p>
                    <p className="text-slate-400 text-sm">ID: {trader.trader_id.substring(0, 8)}...</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-2 text-green-400">
                    <TrendingUp className="w-4 h-4" />
                    <span className="font-bold text-lg">{trader.roi.toFixed(2)}%</span>
                  </div>
                  <p className="text-slate-400 text-sm mt-1">
                    ${trader.portfolio_value.toLocaleString('en-US', { 
                      minimumFractionDigits: 2, 
                      maximumFractionDigits: 2 
                    })}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Leaderboard

