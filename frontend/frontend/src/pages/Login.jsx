import "./Login.css";

const Login = () => {
  return (
    <div className="login-container">
      {/* Header */}
      <div className="login-header">UTH - COMFMS</div>

      {/* Background */}
      <div className="login-background">
        {/* Login Card */}
        <div className="login-card">
          <h2>LOG IN TO THE SYSTEM</h2>

          <input type="text" placeholder="Email / Username" />

          <input type="password" placeholder="Password" />

          <button className="login-btn">LOGIN</button>

          <a href="#" className="forgot-password">
            FORGOT PASSWORD?
          </a>
        </div>
      </div>
    </div>
  );
};

export default Login;
