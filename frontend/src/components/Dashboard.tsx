import { motion } from 'framer-motion'
import PriceTicker from './PriceTicker'
import Leaderboard from './Leaderboard'

const Dashboard = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="container mx-auto px-4 py-8"
    >
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Trading Dashboard</h1>
        <p className="text-slate-400">Monitor live prices and top traders</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Price Ticker Card */}
        <div className="lg:col-span-1">
          <PriceTicker />
        </div>

        {/* Leaderboard Card */}
        <div className="lg:col-span-1">
          <Leaderboard />
        </div>
      </div>
    </motion.div>
  )
}

export default Dashboard

