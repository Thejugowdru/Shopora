import React from "react";
import { FaFacebook, FaInstagram, FaTwitter, FaYoutube, FaGithub } from "react-icons/fa";
import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">

      <div className="container footer-grid">

        {/* About */}
        <div className="footer-col">
          <h5 className="footer-logo">Shopora</h5>
          <p>
            Shopora is a multi-vendor marketplace where customers
            discover products from trusted vendors with fast delivery
            and secure payments.
          </p>
        </div>

        {/* Quick Links */}
        <div className="footer-col">
          <h6>Quick Links</h6>
          <ul>
            <li>Home</li>
            <li>Trending</li>
            <li>Categories</li>
            <li>Featured Products</li>
          </ul>
        </div>

        {/* Categories */}
        <div className="footer-col">
          <h6>Categories</h6>
          <ul>
            <li>Electronics</li>
            <li>Fashion</li>
            <li>Groceries</li>
            <li>Kitchen</li>
          </ul>
        </div>

        {/* Social */}
        <div className="footer-col">
          <h6>Follow Us</h6>

          <div className="footer-social">

            <a href="#"><FaFacebook /></a>
            <a href="#"><FaInstagram /></a>
            <a href="#"><FaTwitter /></a>
            <a href="#"><FaYoutube /></a>
            <a href="#"><FaGithub /></a>

          </div>

        </div>

      </div>

      <div className="footer-bottom">
        © 2026 Shopora. All Rights Reserved.
      </div>

    </footer>
  );
}

export default Footer;