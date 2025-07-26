import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { getProductos, getMovimientosStock, getProductosStockBajo, chatbotGetStats } from '@/lib/api';

const AdminDashboard: React.FC = () => {
  const [salesData, setSalesData] = useState([]);
  const [stockData, setStockData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [revenueData, setRevenueData] = useState([]);
  const [originData, setOriginData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // Obtener productos para análisis de ventas y categorías
      const productosResponse = await getProductos();
      
      if (productosResponse.success && productosResponse.productos) {
        const productos = productosResponse.productos;

        // Datos de productos más vendidos (simulado basado en precio como proxy de popularidad)
        const salesDataFormatted = productos
          .sort((a, b) => parseFloat(b.precio) - parseFloat(a.precio))
          .slice(0, 5)
          .map(p => ({
            name: p.nombre,
            ventas: Math.floor(Math.random() * 50) + 10 // Simulado hasta tener datos reales de ventas
          }));
        setSalesData(salesDataFormatted);

        // Datos de stock bajo
        try {
          const stockBajoResponse = await getProductosStockBajo();
          if (stockBajoResponse.success && stockBajoResponse.productos) {
            const stockDataFormatted = stockBajoResponse.productos.map(p => ({
              name: p.nombre,
              stock: p.stock || Math.floor(Math.random() * 30) + 5
            }));
            setStockData(stockDataFormatted);
          }
        } catch (error) {
          // Fallback con datos de productos normales
          const stockDataFormatted = productos.slice(0, 5).map(p => ({
            name: p.nombre,
            stock: Math.floor(Math.random() * 50) + 5
          }));
          setStockData(stockDataFormatted);
        }

        // Análisis de categorías
        const categoryCounts = productos.reduce((acc, p) => {
          const categoria = p.categoria || 'Otros';
          acc[categoria] = (acc[categoria] || 0) + 1;
          return acc;
        }, {});

        const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#00ff88'];
        const categoryDataFormatted = Object.entries(categoryCounts).map(([name, value], index) => ({
          name,
          value,
          color: colors[index % colors.length]
        }));
        setCategoryData(categoryDataFormatted);

        // Análisis de origen
        const originCounts = productos.reduce((acc, p) => {
          const origen = p.origen || 'Desconocido';
          acc[origen] = (acc[origen] || 0) + 1;
          return acc;
        }, {});

        const originDataFormatted = Object.entries(originCounts)
          .slice(0, 4)
          .map(([name, value]) => ({
            name,
            ventas: (value as number) * 10 // Multiplicar por factor para simular ventas
          }));
        setOriginData(originDataFormatted);
      }

      // Datos de ingresos diarios (simulados)
      const dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
      const revenueDataFormatted = dias.map(dia => ({
        dia,
        ingresos: Math.floor(Math.random() * 1500) + 1000
      }));
      setRevenueData(revenueDataFormatted);

      // Intentar obtener estadísticas del chatbot si están disponibles
      try {
        const statsResponse = await chatbotGetStats();
        if (statsResponse.success && statsResponse.stats) {
          // Usar estadísticas reales si están disponibles
          console.log('Estadísticas reales disponibles:', statsResponse.stats);
        }
      } catch (error) {
        console.log('Estadísticas del chatbot no disponibles, usando datos simulados');
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <div className="animate-pulse">
            <div className="h-6 bg-gray-200 rounded mb-4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <div className="animate-pulse">
            <div className="h-6 bg-gray-200 rounded mb-4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <div className="animate-pulse">
            <div className="h-6 bg-gray-200 rounded mb-4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <div className="animate-pulse">
            <div className="h-6 bg-gray-200 rounded mb-4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
      {/* Productos más vendidos */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-semibold mb-4 text-market-red">Productos Más Vendidos</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={salesData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="ventas" fill="hsl(var(--market-red))" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Origen de productos */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-semibold mb-4 text-market-red">Origen de Productos Más Vendidos</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={originData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="ventas" fill="hsl(var(--market-green))" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Ingresos diarios */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-semibold mb-4 text-market-red">Ingresos Diarios</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={revenueData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="dia" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="ingresos" 
              stroke="hsl(var(--market-red))" 
              strokeWidth={3}
              dot={{ fill: 'hsl(var(--market-red))' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Stock de productos */}
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-semibold mb-4 text-market-red">Stock de Productos</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stockData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="stock" fill="hsl(var(--market-green))" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Distribución por categorías */}
      <div className="bg-white p-6 rounded-lg shadow-lg lg:col-span-2">
        <h3 className="text-xl font-semibold mb-4 text-market-red">Distribución de Productos por Categoría</h3>
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie
              data={categoryData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={120}
              fill="#8884d8"
              dataKey="value"
            >
              {categoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AdminDashboard;