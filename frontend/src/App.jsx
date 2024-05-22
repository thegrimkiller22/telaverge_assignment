
import Index from "./components/Index/Index"
import Dashboard from './components/Dashboard/Dashboard'
import Login from './components/Login/Login'
import Register from './components/Register/Register'
import Products from './components/Products/Products'
import { Route, Routes } from 'react-router-dom';
import "./App.css"
import Navbar from "./components/Navbar/Navbar"
import { useEffect, useState } from 'react';
const App = () => {
  const [isLogin, setIsLogin] = useState(false);
  useEffect(() => {
    if (localStorage.getItem('loginData')) {
      setIsLogin(true)
    }
  }, [])
  return (
    <div className="app">
      <Navbar isLogin={isLogin} setIsLogin={setIsLogin} />

      <Routes>
        <Route exact path="/" element={!isLogin ? <Index /> : <Dashboard />} />
        {!isLogin &&
          <>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </>
        }
        {isLogin &&
          <>
            <Route path="/products" element={<Products />} />
          </>
        }
      </Routes>

    </div>
  )
}

export default App