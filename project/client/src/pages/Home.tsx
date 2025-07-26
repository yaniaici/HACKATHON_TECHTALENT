import React from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '@/components/Header';
import { categories } from '@/data/products';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/context/AuthContext';
import AdminDashboard from '@/components/AdminDashboard';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleShowAllProducts = () => {
    navigate('/products');
  };

  const handleCategoryClick = (categoryId: string) => {
    navigate(`/products?category=${categoryId}`);
  };

  const handleSearch = (query: string) => {
    if (query.trim()) {
      navigate(`/products?search=${encodeURIComponent(query)}`);
    }
  };

  // Si es vendedor/administrador, mostrar dashboard
  if (user && user.role === 'vendedor') {
    return (
      <div className="min-h-screen bg-market-beige">
        <Header onSearch={handleSearch} />
        
        <main className="max-w-7xl mx-auto p-6">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-market-red mb-2">Dashboard Administrativo</h1>
            <p className="text-gray-600">Panel de control del Mercado de Tarragona</p>
          </div>
          
          <AdminDashboard />
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-market-beige">
      <Header onSearch={handleSearch} />
      
      <main className="max-w-7xl mx-auto p-6">
        {/* Main featured block */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-market-red to-market-red-light rounded-lg overflow-hidden shadow-lg">
            <div className="flex items-center justify-between p-8 md:p-12">
              <div className="flex-1">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                  Descubre todos nuestros productos
                </h2>
                <p className="text-white/90 text-lg mb-6">
                  Productos frescos del mercado tradicional de Tarragona
                </p>
                <Button 
                  onClick={handleShowAllProducts}
                  className="bg-white text-market-red hover:bg-gray-100 font-semibold px-8 py-3 text-lg"
                >
                  Ver todos los productos
                </Button>
              </div>
              <div className="hidden md:block ml-8">
                <div className="w-32 h-32 bg-white/20 rounded-full flex items-center justify-center">
                  <span className="text-6xl">🛒</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Category blocks */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {categories.map((category) => (
            <div
              key={category.id}
              onClick={() => handleCategoryClick(category.id)}
              className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer transform transition-all duration-200 hover:scale-105 hover:shadow-lg"
            >
              <div className={`${category.color} h-32 flex items-center justify-center`}>
                <span className="text-4xl">{category.icon}</span>
              </div>
              <div className="p-4">
                <h3 className="text-lg font-semibold text-center text-gray-800">
                  {category.name}
                </h3>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Home;