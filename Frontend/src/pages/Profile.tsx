import React, { useState, useEffect } from 'react';
import { Package, Calendar, MapPin } from 'lucide-react';
import Header from '@/components/Header';
import Receipt from '@/components/Receipt';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Order } from '@/types';
import { getPedidos } from '@/lib/api';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [orders, setOrders] = useState<Order[]>([]);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [showReceipt, setShowReceipt] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    fetchUserOrders();
  }, [user, navigate]);

  const fetchUserOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await getPedidos();
      
      if (response.success && response.pedidos) {
        // Filtrar pedidos del usuario actual y transformar formato
        const userOrders = response.pedidos
          .filter((pedido: any) => pedido.id_usuario === parseInt(user!.id))
          .map((pedido: any) => ({
            id: pedido.id.toString(),
            userId: pedido.id_usuario.toString(),
            items: pedido.productos ? JSON.parse(pedido.productos) : [],
            total: parseFloat(pedido.total || '0'),
            status: pedido.estado || 'pendiente',
            date: pedido.fecha_creacion || new Date().toISOString(),
            address: pedido.destino || user!.address
          }));
        
        setOrders(userOrders);
      } else {
        setError('No se pudieron cargar los pedidos');
      }
    } catch (error) {
      console.error('Error fetching orders:', error);
      setError('Error al cargar los pedidos');
    } finally {
      setLoading(false);
    }
  };

  const handleViewOrder = (order: Order) => {
    setSelectedOrder(order);
    setShowReceipt(true);
  };

  const handleCloseReceipt = () => {
    setShowReceipt(false);
    setSelectedOrder(null);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pendiente':
        return 'bg-yellow-100 text-yellow-800';
      case 'procesando':
        return 'bg-blue-100 text-blue-800';
      case 'enviado':
        return 'bg-purple-100 text-purple-800';
      case 'entregado':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pendiente':
        return 'Pendiente';
      case 'procesando':
        return 'Procesando';
      case 'enviado':
        return 'Enviado';
      case 'entregado':
        return 'Entregado';
      default:
        return status;
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-market-beige">
      <Header />
      
      <main className="max-w-7xl mx-auto p-6">
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">Mi Perfil</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Información Personal</h3>
              <p className="text-gray-600 mb-1">
                <strong>Nombre:</strong> {user.name} {user.firstSurname} {user.secondSurname}
              </p>
              <p className="text-gray-600 mb-1">
                <strong>Email:</strong> {user.email}
              </p>
              <p className="text-gray-600 mb-1">
                <strong>Teléfono:</strong> {user.phone}
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Dirección</h3>
              <p className="text-gray-600 flex items-center">
                <MapPin className="h-4 w-4 mr-2" />
                {user.address}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Historial de Pedidos</h2>
          
          {loading ? (
            <div className="text-center py-8">
              <div className="text-lg text-gray-600">Cargando pedidos...</div>
            </div>
          ) : error ? (
            <div className="text-center py-8">
              <Package className="h-16 w-16 text-red-300 mx-auto mb-4" />
              <p className="text-red-500 text-lg mb-4">{error}</p>
              <Button 
                onClick={fetchUserOrders}
                className="bg-market-red hover:bg-market-red-light"
              >
                Reintentar
              </Button>
            </div>
          ) : orders.length === 0 ? (
            <div className="text-center py-8">
              <Package className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-lg">No tienes pedidos aún</p>
              <Button 
                onClick={() => navigate('/')}
                className="mt-4 bg-market-red hover:bg-market-red-light"
              >
                Hacer mi primer pedido
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              {orders.map((order) => (
                <div 
                  key={order.id}
                  className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => handleViewOrder(order)}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <Package className="h-5 w-5 text-gray-400" />
                      <span className="font-semibold text-gray-800">
                        Pedido #{order.id}
                      </span>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                      {getStatusText(order.status)}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2" />
                      {new Date(order.date).toLocaleDateString('es-ES')}
                    </div>
                    <div>
                      {order.items.length} artículo{order.items.length !== 1 ? 's' : ''}
                    </div>
                    <div className="font-semibold text-market-red">
                      €{order.total.toFixed(2)}
                    </div>
                  </div>
                  
                  <div className="mt-3 text-sm text-gray-500">
                    <span>Productos: </span>
                    {order.items.slice(0, 3).map((item, index) => (
                      <span key={item.id}>
                        {item.name}
                        {index < Math.min(order.items.length, 3) - 1 ? ', ' : ''}
                      </span>
                    ))}
                    {order.items.length > 3 && <span> y {order.items.length - 3} más...</span>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {showReceipt && selectedOrder && (
        <Receipt 
          items={selectedOrder.items} 
          total={selectedOrder.total} 
          onClose={handleCloseReceipt} 
        />
      )}
    </div>
  );
};

export default Profile;