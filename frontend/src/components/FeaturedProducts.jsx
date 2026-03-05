import React from "react";
import { FaHeart } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./FeaturedProducts.css";

function FeaturedProducts() {

  const products = [
    { id: 1, name: "Smart Watch", price: "₹2,999", image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80" },
    { id: 2, name: "Perfume", price: "₹1,499", image: "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=500&q=80" },
    { id: 3, name: "Running Shoes", price: "₹3,499", image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=500&q=80" },
    { id: 4, name: "Headphones", price: "₹999", image: "https://images.unsplash.com/photo-1518444065439-e933c06ce9cd?auto=format&fit=crop&w=500&q=80" },
    { id: 5, name: "Backpack", price: "₹1,199", image: "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=500&q=80" }
  ];

  return (

    <section className="product-section">

      <div className="container">

        <h2 className="section-header text-center">
          Featured Products
        </h2>

        <div className="row g-4">

          {products.map(product => (

            <div key={product.id} className="col-6 col-md-4 col-lg-2">

              <div className="card product-card">

                <button className="wishlist-btn">
                  <FaHeart />
                </button>

                <img src={product.image} alt={product.name} />

                <div className="card-body text-center">

                  <h6>{product.name}</h6>
                  <p>{product.price}</p>

                  <button className="btn btn-orange w-100">
                    Add to Cart
                  </button>

                </div>

              </div>

            </div>

          ))}

          {/* View All */}

          <div className="col-6 col-md-4 col-lg-2">

            <div className="card view-more-card h-100 d-flex align-items-center justify-content-center text-center">

              <div>
                <h6 className="fw-bold text-orange">
                  View More
                </h6>
                <p className="small text-muted">
                  Featured
                </p>
              </div>

            </div>

          </div>

        </div>

      </div>

    </section>

  );
}

export default FeaturedProducts;