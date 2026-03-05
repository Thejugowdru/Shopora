import React from "react";
import navbarLogo from "../assets/shopora_navbar_logo.png";
import "./Navbar.css";
import { Link, useLocation } from "react-router-dom";
import {
  FaSearch, 
  FaUserCircle,
  FaStore,
  FaUserShield,
  FaHeart,
  FaShoppingCart,
  FaBox,
  FaUser,
  FaSignOutAlt
} from "react-icons/fa";

function Navbar({ hideSearch }) {

  const location = useLocation();

  const role = "shopora"; // dynamic later
  const isLoggedIn = false;

  const isLoginPage = location.pathname === "/login";
  const isRegisterPage = location.pathname === "/register";

  return (
    <nav className="navbar navbar-custom sticky-top">

      <div className="container-fluid navbar-wrapper">

        {/* Logo */}
        <Link to={'/'}>
          <div className="logo-wrapper">
            <img
              src={navbarLogo}
              alt="Shopora"
              className="navbar-logo"
            />
          </div>
        </Link>


        {/* Search */}
        {!hideSearch && (
          <form className="search-form">

            <input
              type="search"
              placeholder="Search products, brands and categories..."
              className="search-input"
            />

            <button className="search-btn">
              <FaSearch />
            </button>

          </form>
        )}

        {/* If NOT Logged In */}
        {!isLoggedIn && (
          <div className="auth-links">

            {isLoginPage && (
              <Link to="/register" className="auth-btn">
                Register
              </Link>
            )}

            {isRegisterPage && (
              <Link to="/login" className="auth-btn">
                Login
              </Link>
            )}

            {!isLoginPage && !isRegisterPage && (
              <Link to="/login" className="auth-btn">
                Login
              </Link>
            )}

          </div>
        )}

        {/* If Logged In */}
        {isLoggedIn && (
          <div className="dropdown profile-dropdown">

            <button
              className="profile-btn"
              data-bs-toggle="dropdown"
            >
              <FaUserCircle />
            </button>

            <ul className="dropdown-menu dropdown-menu-end profile-menu">

              {role === "vendor" && (
                <li>
                  <a className="dropdown-item d-flex align-items-center gap-2">
                    <FaStore />
                    Vendor Dashboard
                  </a>
                </li>
              )}
              {role === "shopora" && (
                <li>
                  <a className="dropdown-item d-flex align-items-center gap-2">
                    <FaUserShield />
                    Shopora Team Dashboard
                  </a>
                </li>
              )}
              
              <hr className="dropdown-divider" />

              <li>
                <a className="dropdown-item d-flex align-items-center gap-2">
                  <FaHeart />
                  Wishlist
                </a>
              </li>

              <hr className="dropdown-divider" />

              <li>
                <a className="dropdown-item d-flex align-items-center gap-2">
                  <FaShoppingCart />
                  Cart
                </a>
              </li>

              <hr className="dropdown-divider" />

              <li>
                <a className="dropdown-item d-flex align-items-center gap-2">
                  <FaBox />
                  Orders
                </a>
              </li>
              
              <hr className="dropdown-divider" />

              <li>
                <a className="dropdown-item d-flex align-items-center gap-2">
                  <FaUser />
                  Account
                </a>
              </li>
              
              <hr className="dropdown-divider" />

              <li>
                <a className="dropdown-item d-flex align-items-center gap-2">
                  <FaSignOutAlt />
                  Logout
                </a>
              </li>
            </ul>

          </div>
        )}

      </div>

    </nav>
  );
}

export default Navbar;