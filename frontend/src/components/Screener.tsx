import { motion } from 'framer-motion'

const Screener = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="container mx-auto px-4 py-8"
    >
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Market Screener</h1>
        <p className="text-slate-400">Screen and analyze cryptocurrency markets</p>
      </div>

      <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-6 shadow-2xl">
        <p className="text-slate-400">Screener component coming soon...</p>
      </div>
    </motion.div>
  )
}

export default Screener

