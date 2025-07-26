import React, { useState } from 'react';
import { Search, User, ShoppingCart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuth } from '@/context/AuthContext';
import { useCart } from '@/context/CartContext';
import { useNavigate } from 'react-router-dom';

interface HeaderProps {
  onSearch?: (query: string) => void;
  searchQuery?: string;
}

const Header: React.FC<HeaderProps> = ({ onSearch, searchQuery = '' }) => {
  const { user, logout } = useAuth();
  const { itemCount } = useCart();
  const navigate = useNavigate();
  const [search, setSearch] = useState(searchQuery);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearch(value);
    onSearch?.(value);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (search.trim()) {
      navigate(`/products?search=${encodeURIComponent(search)}`);
    }
  };

  const handleUserClick = () => {
    if (user) {
      navigate('/profile');
    } else {
      navigate('/login');
    }
  };

  const handleCartClick = () => {
    navigate('/cart');
  };

  const handleLogoClick = () => {
    navigate('/');
  };

  return (
    <header className="bg-market-red text-white p-4 shadow-lg">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Logo */}
        <div 
          className="text-lg md:text-xl font-bold cursor-pointer hover:text-gray-200 transition-colors flex-shrink-0"
          onClick={handleLogoClick}
        >
          Mercado Tarragona
        </div>

        {/* Search bar */}
        <div className="flex-1 max-w-2xl mx-2 md:mx-8">
          <form onSubmit={handleSearchSubmit} className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              type="text"
              placeholder="Buscar productos..."
              value={search}
              onChange={handleSearchChange}
              className="pl-10 bg-white text-gray-900 border-0 focus:ring-2 focus:ring-market-red-light w-full"
            />
          </form>
        </div>

        {/* User actions */}
        <div className="flex items-center space-x-2 md:space-x-4 flex-shrink-0">
          {user && user.role === 'vendedor' && (
            <Button
              variant="outline"
              onClick={() => navigate('/admin')}
              className="text-market-red border-white hover:bg-white hover:text-market-red hidden md:flex"
            >
              Admin
            </Button>
          )}
          
          <Button
            variant="ghost"
            size="icon"
            onClick={handleUserClick}
            className="hover:bg-market-red-light text-white"
          >
            <User className="h-5 w-5" />
          </Button>

          <Button
            variant="ghost"
            size="icon"
            onClick={handleCartClick}
            className="hover:bg-market-red-light text-white relative"
          >
            <ShoppingCart className="h-5 w-5" />
            {itemCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-market-green text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {itemCount}
              </span>
            )}
          </Button>

          {user && (
            <Button
              variant="outline"
              onClick={logout}
              className="text-market-red border-white hover:bg-white hover:text-market-red hidden md:flex"
            >
              Cerrar Sesión
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;