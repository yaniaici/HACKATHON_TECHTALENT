import React from 'react';
import { CartItem } from '@/types';

interface ReceiptProps {
  items: CartItem[];
  total: number;
  onClose: () => void;
}

const Receipt: React.FC<ReceiptProps> = ({ items, total, onClose }) => {
  const currentDate = new Date().toLocaleDateString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div 
        className="bg-white rounded-lg shadow-2xl max-w-md w-full max-h-[80vh] flex flex-col animate-in slide-in-from-bottom-4 duration-300"
        style={{ fontFamily: 'monospace' }}
      >
        {/* Receipt header */}
        <div className="p-6 border-b border-dashed border-gray-300">
          <div className="text-center">
            <h2 className="text-xl font-bold mb-2">MERCADO TARRAGONA</h2>
            <p className="text-sm text-gray-600">Carrer Major, 15</p>
            <p className="text-sm text-gray-600">43003 Tarragona</p>
            <p className="text-sm text-gray-600">Tel: 977 123 456</p>
            <div className="mt-4 pt-2 border-t border-dashed border-gray-300">
              <p className="text-sm">Fecha: {currentDate}</p>
            </div>
          </div>
        </div>

        {/* Receipt items */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="space-y-2">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between items-start">
                <div className="flex-1 pr-2">
                  <p className="text-sm font-medium">{item.name}</p>
                  <p className="text-xs text-gray-600">
                    {item.quantity} x {item.price.toFixed(2)}€
                  </p>
                </div>
                <p className="text-sm font-medium">
                  {(item.price * item.quantity).toFixed(2)}€
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Receipt footer */}
        <div className="p-6 border-t border-dashed border-gray-300">
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Subtotal:</span>
              <span>{total.toFixed(2)}€</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>IVA (21%):</span>
              <span>{(total * 0.21).toFixed(2)}€</span>
            </div>
            <div className="border-t border-dashed border-gray-300 pt-2">
              <div className="flex justify-between font-bold text-lg">
                <span>Total:</span>
                <span>{(total * 1.21).toFixed(2)}€</span>
              </div>
            </div>
          </div>
          
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600 mb-4">
              ¡Gracias por tu compra!
            </p>
            <p className="text-xs text-gray-500 mb-4">
              Tu pedido será procesado en breve
            </p>
            <button
              onClick={onClose}
              className="bg-market-red text-white px-6 py-2 rounded-lg hover:bg-market-red-light transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Receipt;