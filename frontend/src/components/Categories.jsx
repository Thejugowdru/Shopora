import React from "react";
import "./Categories.css";

// categories section
function Categories() {

  const categories = [

    { 
        name: "Groceries", 
        image: "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Kitchen", 
        image: "https://images.unsplash.com/photo-1506368083636-6defb67639a7?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Electronics", 
        image: "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Mobiles", 
        image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Fashion", 
        image: "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Beauty", 
        image: "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Fitness", 
        image: "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Furniture", 
        image: "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Toys", 
        image: "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Books", 
        image: "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Appliances", 
        image: "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=200&q=80" 
    },

    { 
        name: "Accessories", 
        image: "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?auto=format&fit=crop&w=200&q=80" 
    }

];

  return (

    <section className="categories-section">

      <div className="container">

        <h2 className="section-header">
          Shop by Categories
        </h2>

        <div className="categories-scroll">

          {categories.map((cat, index) => (

            <div key={index} className="category-item">

              <img
                src={cat.image}
                alt={cat.name}
              />

              <p>{cat.name}</p>

            </div>

          ))}

        </div>

      </div>

    </section>

  );
}

export default Categories;