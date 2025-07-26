import React from 'react';
import { Minus, Plus, X } from 'lucide-react';
import { CartItem as CartItemType } from '@/types';
import { Button } from '@/components/ui/button';
import { useCart } from '@/context/CartContext';
import { allergenIcons } from '@/data/products';

interface CartItemProps {
  item: CartItemType;
}

const CartItem: React.FC<CartItemProps> = ({ item }) => {
  const { removeItem, updateQuantity } = useCart();

  const handleQuantityChange = (newQuantity: number) => {
    updateQuantity(item.id, newQuantity);
  };

  const handleRemove = () => {
    removeItem(item.id);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <div className="flex items-start space-x-4">
        {/* Product image */}
        <img
          src={item.image}
          alt={item.name}
          className="w-24 h-24 object-cover rounded-lg"
        />

        {/* Product details */}
        <div className="flex-1">
          <div className="flex justify-between items-start mb-2">
            <h3 className="font-semibold text-gray-800 text-lg">{item.name}</h3>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleRemove}
              className="text-gray-400 hover:text-red-500"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          <div className="space-y-2 mb-3">
            <p className="text-sm text-gray-600">
              <span className="font-medium">Proveedor:</span> {item.provider}
            </p>
            <p className="text-sm text-gray-600">
              <span className="font-medium">Origen:</span> {item.origin}
            </p>
            {item.allergens.length > 0 && (
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-600">Alérgenos:</span>
                <div className="flex space-x-1">
                  {item.allergens.map((allergen) => (
                    <span
                      key={allergen}
                      className="text-lg"
                      title={allergen}
                    >
                      {allergenIcons[allergen] || '⚠️'}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Quantity controls and price */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="icon"
                onClick={() => handleQuantityChange(item.quantity - 1)}
                className="h-8 w-8"
              >
                <Minus className="h-3 w-3" />
              </Button>
              <span className="font-medium text-gray-800 min-w-[2rem] text-center">
                {item.quantity}
              </span>
              <Button
                variant="outline"
                size="icon"
                onClick={() => handleQuantityChange(item.quantity + 1)}
                className="h-8 w-8"
              >
                <Plus className="h-3 w-3" />
              </Button>
            </div>
            
            <div className="text-right">
              <p className="text-lg font-semibold text-market-red">
                {(item.price * item.quantity).toFixed(2)}€
              </p>
              <p className="text-sm text-gray-500">
                {item.price.toFixed(2)}€ / unidad
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartItem;