import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Screener from './components/Screener'
import Navbar from './components/Navbar'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/screener" element={<Screener />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
