import { useState } from "react";
import "./Login.css"
function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const handleSubmit = async (e) => {
        e.preventDefault()
        console.log(email, password)
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        console.log(responseData);
        localStorage.setItem('loginData', JSON.stringify(responseData));
        window.location.href = "/"
        setEmail("");
        setPassword("");

    }
    return (
        <div className="container">
            <h1>Login</h1>
            <form onSubmit={handleSubmit} >
                <div className="label-input">
                    <label htmlFor="email">Email:</label>
                    <input type="email" id="email" name="email" placeholder="Email" autoComplete="off" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
                <div className="label-input">
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" placeholder="Password" autoComplete="off" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <div>
                    <input type="submit" value="Login" />
                </div>
            </form>
            <p>Dont have an account? <a href='/register'>Register here</a></p>
        </div>
    );
}

export default Login;