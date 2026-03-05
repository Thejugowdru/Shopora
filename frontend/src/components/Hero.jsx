import React, { useState, useEffect } from "react";
import "./Hero.css";

// Hero section
function Hero() {

  const role = "customer";

  // hero images
  const heroImages = [
    "https://images.unsplash.com/photo-1607082349566-187342175e2f?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80"
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  // auto slide image
  useEffect(() => {

    const interval = setInterval(() => {
      setCurrentIndex(prev =>
        prev === heroImages.length - 1 ? 0 : prev + 1
      );
    }, 3000);

    return () => clearInterval(interval);

  }, []);

  return (

    <section className="hero-section">

      <div className="container">

        <div className="row align-items-center">

          {/* text content */}
          <div className="col-lg-6">

            <h1 className="hero-title">
              Empowering Vendors <br />
              Simplifying Commerce
            </h1>

            <p className="hero-desc">
              Shop from multiple vendors in one place with secure payments.
            </p>

            <div className="hero-buttons">

              <a href="#recommended-section" className="btn btn-orange">
                Start Shopping
              </a>

              {role !== "vendor" && (
                <button className="btn btn-outline-dark">
                  Become Vendor
                </button>
              )}

            </div>

          </div>

          {/* hero image */}
          <div className="col-lg-6 text-center">

            <img
              src={heroImages[currentIndex]}
              alt="hero"
              className="hero-image"
            />

          </div>

        </div>

      </div>

    </section>

  );
}

export default Hero;