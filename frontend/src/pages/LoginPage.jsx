import React, { useState } from "react";
import { FaUser, FaLock, FaEye, FaEyeSlash } from "react-icons/fa";
import { Link } from "react-router-dom";
import shoporaLogo from "../assets/shopora_logo.png";
import "./LoginPage.css";

function LoginPage() {

  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="login-page d-flex justify-content-center align-items-center bg-white">

      <div className="login-card border p-4">

        <div className="text-center mb-3">
          <img src={shoporaLogo} alt="Shopora" style={{ width: "120px" }} />
        </div>

        <h4 className="text-center mb-4">Login to Shopora</h4>


        {/* USERNAME / EMAIL */}

        <div className="input-group input-group-sm mb-3">

          <span className="input-group-text">
            <FaUser />
          </span>

          <input
            type="text"
            className="form-control"
            placeholder="Email or Username"
          />

        </div>

        {/* PASSWORD */}
      
        <div className="input-group input-group-sm">

          <span className="input-group-text">
            <FaLock />
          </span>

          <input
            type={showPassword ? "text" : "password"}
            className="form-control"
            placeholder="Enter Password"
          />

          <span
            className="input-group-text"
            style={{ cursor: "pointer" }}
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </span>

        </div>

        <div className="d-flex justify-content-end mb-3">
          <Link to="/forgot-password" className="text-decoration-none small">
            Forgot Password?
          </Link>
        </div>

        {/* LOGIN BUTTON */}

        <button className="btn btn-warning w-100 mb-3">
          Login
        </button>


        {/* LINKS */}

        <div className="text-center">
          <p>
            New user?{" "}
            <Link to="/register" className="text-decoration-none">
              Create account
            </Link>
          </p>

        </div>

      </div>

    </div>
  );


  
}

export default LoginPage;