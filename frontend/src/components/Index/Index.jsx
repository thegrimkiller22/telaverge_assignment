import "./Index.css"

function Index() {
    return (
        <div className="container">
            <h1>Welcome to the Home Page</h1>
            <div className="button-container">
                <a href="/login" className="login-button">Login</a>
                <a href="/register" className="signup-button">Sign Up</a>
                
            </div>
        </div>
    );
}

export default Index;