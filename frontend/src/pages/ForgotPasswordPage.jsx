import React, { useState } from "react";
import { FaEnvelope } from "react-icons/fa";
import { Link } from "react-router-dom";
import shoporaLogo from "../assets/shopora_logo.png";

function ForgotPasswordPage() {

  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Reset link sent to:", email);
  };

  return (
    <div className="login-page d-flex justify-content-center align-items-center bg-white">

      <div className="login-card border p-4">

        <div className="text-center mb-3">
          <img src={shoporaLogo} alt="Shopora" style={{ width: "120px" }} />
        </div>

        <h4 className="text-center mb-4">Reset Password</h4>

        <form onSubmit={handleSubmit}>

          <div className="input-group input-group-sm mb-3">

            <span className="input-group-text">
              <FaEnvelope />
            </span>

            <input
              type="email"
              className="form-control"
              placeholder="Enter your email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              required
            />

          </div>

          <button className="btn btn-warning w-100 mb-3">
            Send Reset Link
          </button>

        </form>

        <div className="text-center">
          <Link to="/login" className="text-decoration-none">
            Back to Login
          </Link>
        </div>

      </div>

    </div>
  );
}

export default ForgotPasswordPage;