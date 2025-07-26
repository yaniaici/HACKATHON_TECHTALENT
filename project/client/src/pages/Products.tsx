import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Header from '@/components/Header';
import ProductCard from '@/components/ProductCard';
import { categories } from '@/data/products';
import { useProducts } from '@/hooks/useProducts';
import { Product } from '@/types';

const Products: React.FC = () => {
  const [searchParams] = useSearchParams();
  const { products } = useProducts();
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  useEffect(() => {
    const category = searchParams.get('category');
    setSelectedCategory(category || '');
  }, [searchParams]);

  useEffect(() => {
    let filtered = products;

    // Filter by category
    if (selectedCategory) {
      filtered = filtered.filter(product => product.category === selectedCategory);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredProducts(filtered);
  }, [selectedCategory, searchQuery, products]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleCategoryFilter = (categoryId: string) => {
    setSelectedCategory(categoryId === selectedCategory ? '' : categoryId);
  };

  const currentCategoryName = selectedCategory 
    ? categories.find(cat => cat.id === selectedCategory)?.name 
    : 'Todos los productos';

  return (
    <div className="min-h-screen bg-market-beige">
      <Header onSearch={handleSearch} searchQuery={searchQuery} />
      
      <main className="max-w-7xl mx-auto p-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Sidebar filters */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-800">Filtros</h3>
              
              <div className="space-y-3">
                <button
                  onClick={() => handleCategoryFilter('')}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    !selectedCategory 
                      ? 'bg-market-red text-white' 
                      : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">🏪</span>
                    <span>Todos</span>
                  </div>
                </button>
                
                {categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => handleCategoryFilter(category.id)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedCategory === category.id 
                        ? 'bg-market-red text-white' 
                        : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <span className="text-lg">{category.icon}</span>
                      <span>{category.name}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Products grid */}
          <div className="lg:w-3/4">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                {currentCategoryName}
              </h2>
              <p className="text-gray-600">
                {filteredProducts.length} productos encontrados
              </p>
            </div>

            {filteredProducts.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredProducts.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <p className="text-gray-500 text-lg">
                  No se encontraron productos que coincidan con tu búsqueda
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Products;