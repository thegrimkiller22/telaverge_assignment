import { useState } from 'react';
import PropTypes from 'prop-types';
import './Navbar.css'
import { Link } from 'react-router-dom';
const Navbar = ({ isLogin, setIsLogin }) => {
    const [activeTab, setActiveTab] = useState('home');

    const handleTabClick = target => {
        setActiveTab(target);

    };
    const handleLogout = () => {
        localStorage.removeItem('loginData');
        setIsLogin(false)
    }


    return (
        <div className='nav-container'>
            <div className='nav-tab navbar'>
                <div
                    className={`navtab  ${activeTab === 'home' ? 'active' : ''}`}
                >
                    <Link to="/" className={`${activeTab === 'home' ? 'active' : ''}`} onClick={() => handleTabClick('home')}>Home</Link>
                </div>
                {
                    !isLogin && <>
                        <div
                            className={`navtab `}
                            onClick={() => handleTabClick('login')}>
                            <Link to="/login" className={`${activeTab === 'login' ? 'active' : ''}`} onClick={() => handleTabClick('login')}>Login</Link>
                        </div >
                        <div
                            className={`navtab ${activeTab === 'register' ? 'active' : ''}`}
                        >
                            <Link to="/register" className={`${activeTab === 'register' ? 'active' : ''}`} onClick={() => handleTabClick('register')}>Register</Link>
                        </div >
                    </>
                }

                {
                    isLogin && <>
                        <div
                            className={`navtab `}
                        >
                            <Link to="/products" className={`${activeTab === 'products' ? 'active' : ''}`} onClick={() => handleTabClick('products')}>Products</Link>
                        </div >
                        <div
                            className={`navtab `}
                        >
                            <Link to="/" className={`${activeTab === 'register' ? 'active' : ''}`} onClick={() => handleLogout()}>Logout</Link>
                        </div >
                    </>
                }


                <div className='underline'></div>
            </div >

        </ div>
    );
};

Navbar.propTypes = {
    isLogin: PropTypes.bool.isRequired,
    setIsLogin: PropTypes.func.isRequired
};

export default Navbar;