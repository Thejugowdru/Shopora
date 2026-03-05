import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FaEye, FaEyeSlash, FaTimes } from "react-icons/fa";
import logo from "../assets/shopora_logo.png";
import "./RegisterPage.css";

function RegisterPage() {

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [showOtpPopup, setShowOtpPopup] = useState(false);
  const [otp, setOtp] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleRegister = (e) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    setShowOtpPopup(true);
  };

  const verifyOtp = () => {

    if (!otp) {
      alert("Enter OTP");
      return;
    }

    alert("Account verified successfully");
    setShowOtpPopup(false);
  };

  return (
    <>

      <div className="register-page d-flex justify-content-center align-items-center bg-white">

        <div className="register-card border p-4">

          <div className="text-center mb-3">
            <img src={logo} alt="Shopora" className="register-logo" />
          </div>

          <h4 className="text-center mb-4">Create Account</h4>

          <form onSubmit={handleRegister}>

            {/* USERNAME */}

            <div className="mb-3">
              <input
                type="text"
                name="username"
                className="form-control"
                placeholder="Username"
                required
                onChange={handleChange}
              />
            </div>

            {/* EMAIL */}

            <div className="mb-3">
              <input
                type="email"
                name="email"
                className="form-control"
                placeholder="Email Address"
                required
                onChange={handleChange}
              />
            </div>

            {/* PASSWORD */}

            <div className="input-group mb-3">

              <input
                type={showPassword ? "text" : "password"}
                name="password"
                className="form-control"
                placeholder="Password"
                required
                onChange={handleChange}
              />

              <span
                className="input-group-text password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </span>

            </div>


            {/* CONFIRM PASSWORD */}

            <div className="input-group mb-3">

              <input
                type={showConfirmPassword ? "text" : "password"}
                name="confirmPassword"
                className="form-control"
                placeholder="Confirm Password"
                required
                onChange={handleChange}
              />

              <span
                className="input-group-text password-toggle"
                onClick={() =>
                  setShowConfirmPassword(!showConfirmPassword)
                }
              >
                {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
              </span>

            </div>


            {/* REGISTER BUTTON */}

            <button className="btn btn-warning w-100">
              Register
            </button>

          </form>


          {/* LINKS */}

          <div className="text-center mt-3">

            <p>
              Already have an account?{" "}
              <Link to="/login" className="text-decoration-none">
                Login
              </Link>
            </p>

          </div>

        </div>

      </div>

      {/* OTP POPUP */}

      {showOtpPopup && (

        <div className="otp-overlay">

          <div className="card p-4 otp-card">

            <button
              className="btn-close otp-close"
              onClick={() => setShowOtpPopup(false)}
            ></button>

            <h5 className="text-center mb-3">
              Email Verification
            </h5>

            <p className="text-center text-muted">
              Enter OTP sent to your email
            </p>

            <input
              type="text"
              className="form-control mb-3"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
            />

            <button
              className="btn btn-warning w-100"
              onClick={verifyOtp}
            >
              Verify OTP
            </button>

          </div>

        </div>

      )}

    </>
  );
}

export default RegisterPage;