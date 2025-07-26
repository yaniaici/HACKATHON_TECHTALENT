import React, { useState } from 'react';
import { CreditCard, Smartphone } from 'lucide-react';
import Header from '@/components/Header';
import CartItem from '@/components/CartItem';
import Receipt from '@/components/Receipt';
import { Button } from '@/components/ui/button';
import { useCart } from '@/context/CartContext';
import { useAuth } from '@/context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Cart: React.FC = () => {
  const { items, total, clearCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [selectedPayment, setSelectedPayment] = useState('card');
  const [showReceipt, setShowReceipt] = useState(false);

  const subtotal = total;
  const discount = 0; // You can implement discount logic here
  const shipping = total > 50 ? 0 : 3.99;
  const tax = total * 0.21;
  const finalTotal = subtotal - discount + shipping + tax;

  const handlePurchase = () => {
    if (!user) {
      navigate('/login');
      return;
    }

    if (items.length === 0) {
      return;
    }

    // Save order to localStorage
    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const newOrder = {
      id: Date.now().toString(),
      userId: user.id,
      items: [...items],
      total: finalTotal,
      status: 'pendiente',
      date: new Date()
    };
    orders.push(newOrder);
    localStorage.setItem('orders', JSON.stringify(orders));

    // Show receipt and clear cart
    setShowReceipt(true);
  };

  const handleCloseReceipt = () => {
    setShowReceipt(false);
    clearCart();
    navigate('/');
  };

  if (items.length === 0 && !showReceipt) {
    return (
      <div className="min-h-screen bg-market-beige">
        <Header />
        <main className="max-w-7xl mx-auto p-6">
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Tu carrito está vacío</h2>
            <p className="text-gray-600 mb-6">¡Agrega algunos productos deliciosos!</p>
            <Button onClick={() => navigate('/')} className="bg-market-red hover:bg-market-red-light">
              Ir a comprar
            </Button>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-market-beige">
      <Header />
      
      <main className="max-w-7xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Tu carrito</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart items */}
          <div className="lg:col-span-2">
            {items.map((item) => (
              <CartItem key={item.id} item={item} />
            ))}
          </div>

          {/* Payment sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 sticky top-6">
              <h3 className="text-xl font-semibold mb-6 text-gray-800">Cómo pagarás</h3>
              
              {/* Payment methods */}
              <div className="space-y-3 mb-6">
                <div 
                  className={`p-3 rounded-lg border-2 cursor-pointer transition-colors ${
                    selectedPayment === 'card' 
                      ? 'border-market-red bg-market-red/5' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedPayment('card')}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded-full border-2 ${
                      selectedPayment === 'card' 
                        ? 'border-market-red bg-market-red' 
                        : 'border-gray-300'
                    }`} />
                    <CreditCard className="h-5 w-5 text-gray-600" />
                    <span className="font-medium">Tarjeta de crédito/débito</span>
                  </div>
                </div>
                
                <div 
                  className={`p-3 rounded-lg border-2 cursor-pointer transition-colors ${
                    selectedPayment === 'paypal' 
                      ? 'border-market-red bg-market-red/5' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedPayment('paypal')}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded-full border-2 ${
                      selectedPayment === 'paypal' 
                        ? 'border-market-red bg-market-red' 
                        : 'border-gray-300'
                    }`} />
                    <span className="font-bold text-blue-600">PayPal</span>
                  </div>
                </div>
                
                <div 
                  className={`p-3 rounded-lg border-2 cursor-pointer transition-colors ${
                    selectedPayment === 'mobile' 
                      ? 'border-market-red bg-market-red/5' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedPayment('mobile')}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded-full border-2 ${
                      selectedPayment === 'mobile' 
                        ? 'border-market-red bg-market-red' 
                        : 'border-gray-300'
                    }`} />
                    <Smartphone className="h-5 w-5 text-gray-600" />
                    <span className="font-medium">Pago móvil</span>
                  </div>
                </div>
              </div>

              {/* Order summary */}
              <div className="border-t pt-6 space-y-3">
                <div className="flex justify-between text-sm">
                  <span>Artículos ({items.reduce((sum, item) => sum + item.quantity, 0)}):</span>
                  <span>€{subtotal.toFixed(2)}</span>
                </div>
                
                {discount > 0 && (
                  <div className="flex justify-between text-sm text-green-600">
                    <span>Descuento:</span>
                    <span>-€{discount.toFixed(2)}</span>
                  </div>
                )}
                
                <div className="flex justify-between text-sm">
                  <span>Envío:</span>
                  <span>{shipping === 0 ? 'GRATIS' : `€${shipping.toFixed(2)}`}</span>
                </div>
                
                <div className="flex justify-between text-sm">
                  <span>IVA:</span>
                  <span>€{tax.toFixed(2)}</span>
                </div>
                
                <div className="border-t pt-3">
                  <div className="flex justify-between font-bold text-lg">
                    <span>Total ({items.reduce((sum, item) => sum + item.quantity, 0)} artículos):</span>
                    <span className="text-market-red">€{finalTotal.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              <Button
                onClick={handlePurchase}
                className="w-full mt-6 bg-gray-800 hover:bg-gray-900 text-white py-3 text-lg"
                disabled={items.length === 0}
              >
                Proceder al checkout
              </Button>
            </div>
          </div>
        </div>
      </main>

      {showReceipt && (
        <Receipt 
          items={items} 
          total={finalTotal} 
          onClose={handleCloseReceipt} 
        />
      )}
    </div>
  );
};

export default Cart;