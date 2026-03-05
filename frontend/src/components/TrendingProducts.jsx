import React from "react";
import { FaHeart } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./TrendingProducts.css";

function TrendingProducts() {
  const products = [
      {
          id: 1,
          name: "Bluetooth Speaker",
          price: "₹1,999",
          image: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=500&q=80"
      },

      {
          id: 2,
          name: "Gaming Mouse",
          price: "₹799",
          image: "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=500&q=80"
      },

      {
          id: 3,
          name: "Laptop Stand",
          price: "₹599",
          image: "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=500&q=80"
      },

      {
          id: 4,
          name: "Wireless Keyboard",
          price: "₹1,299",
          image: "https://images.unsplash.com/photo-1541140532154-b024d705b90a?auto=format&fit=crop&w=500&q=80"
      },

      {
          id: 5,
          name: "Smart Light",
          price: "₹899",
          image: "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=500&q=80"
      }
  ];
  return (

    <section className="product-section">

      <div className="container">

        <h2 className="section-header text-center">
          Trending Products
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
                  View All
                </h6>
                <p className="small text-muted">
                  Trending
                </p>
              </div>

            </div>

          </div>

        </div>

      </div>

    </section>

  );
}

export default TrendingProducts;