import React from 'react'
import Hero from '../components/Hero'
import FeaturedProducts from '../components/FeaturedProducts'
import RecommendedProducts from '../components/RecommendedProducts'
import Categories from '../components/Categories'
import TrendingProducts from '../components/TrendingProducts'
import RecentlyViewed from '../components/RecentlyViewed'

function HomePage() {
  return (
    <>
        <Hero />
        <RecommendedProducts />
        <Categories />
        <TrendingProducts />
        <RecentlyViewed />
        <FeaturedProducts />
    </>
  )
}

export default HomePage