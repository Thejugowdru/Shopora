import React from "react";
import { FaHeart } from "react-icons/fa";
import "./RecentlyViewed.css";

function RecentlyViewed() {

  const products = [
    {
      id: 1,
      name: "Leather Wallet",
      price: "₹899",
      image: "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 2,
      name: "Analog Watch",
      price: "₹2,199",
      image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 3,
      name: "Travel Bag",
      price: "₹1,499",
      image: "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 4,
      name: "Sunglasses",
      price: "₹799",
      image: "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 5,
      name: "Sports Shoes",
      price: "₹2,999",
      image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 6,
      name: "Bluetooth Speaker",
      price: "₹1,999",
      image: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 7,
      name: "Laptop Stand",
      price: "₹599",
      image: "https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 8,
      name: "Gaming Mouse",
      price: "₹799",
      image: "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 9,
      name: "Smart Watch",
      price: "₹2,499",
      image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 10,
      name: "Wireless Keyboard",
      price: "₹1,299",
      image: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 11,
      name: "Fitness Band",
      price: "₹1,199",
      image: "https://images.unsplash.com/photo-1576243345690-4e4b79b63288?auto=format&fit=crop&w=500&q=80"
    },

    {
      id: 12,
      name: "Backpack",
      price: "₹1,399",
      image: "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=500&q=80"
    }

  ];

  return (
    <section className="recent-section">

      <div className="container">

        <h2 className="fw-bold mb-4">
          Recently Viewed
        </h2>

        <div className="recent-scroll">

          {products.map((product) => (

            <div key={product.id} className="recent-card">

              <button className="wishlist-btn">
                <FaHeart />
              </button>

              <img src={product.image} alt={product.name} />

              <div className="recent-info">

                <h6>{product.name}</h6>
                <p>{product.price}</p>

                <button className="btn btn-orange btn-sm w-100">
                  Add to Cart
                </button>

              </div>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}

export default RecentlyViewed;