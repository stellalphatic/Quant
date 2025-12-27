import { Link, useLocation } from 'react-router-dom'
import { BarChart3, Search } from 'lucide-react'

const Navbar = () => {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="backdrop-blur-xl bg-white/10 border-b border-white/20 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-white">
            AlgoTrading
          </Link>
          
          <div className="flex items-center gap-4">
            <Link
              to="/"
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                isActive('/')
                  ? 'bg-white/20 text-white'
                  : 'text-slate-300 hover:bg-white/10 hover:text-white'
              }`}
            >
              <BarChart3 className="w-5 h-5" />
              <span>Dashboard</span>
            </Link>
            
            <Link
              to="/screener"
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                isActive('/screener')
                  ? 'bg-white/20 text-white'
                  : 'text-slate-300 hover:bg-white/10 hover:text-white'
              }`}
            >
              <Search className="w-5 h-5" />
              <span>Screener</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

