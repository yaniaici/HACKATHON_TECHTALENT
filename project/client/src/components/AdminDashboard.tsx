import React from 'react';
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

// Datos simulados para los gráficos
const salesData = [
  { name: 'Costillas', ventas: 45 },
  { name: 'Salmón', ventas: 38 },
  { name: 'Tomates', ventas: 32 },
  { name: 'Manzanas', ventas: 28 },
  { name: 'Pollo', ventas: 25 },
];

const originData = [
  { name: 'Local', ventas: 65 },
  { name: 'Nacional', ventas: 45 },
  { name: 'Mediterráneo', ventas: 35 },
  { name: 'Internacional', ventas: 20 },
];

const dailyRevenueData = [
  { dia: 'Lun', ingresos: 1200 },
  { dia: 'Mar', ingresos: 1500 },
  { dia: 'Mié', ingresos: 1800 },
  { dia: 'Jue', ingresos: 1600 },
  { dia: 'Vie', ingresos: 2200 },
  { dia: 'Sáb', ingresos: 2800 },
  { dia: 'Dom', ingresos: 2500 },
];

const stockData = [
  { name: 'Costillas', stock: 25 },
  { name: 'Salmón', stock: 18 },
  { name: 'Tomates', stock: 45 },
  { name: 'Manzanas', stock: 52 },
  { name: 'Pollo', stock: 30 },
];

const categoryData = [
  { name: 'Carne', value: 35, color: '#8884d8' },
  { name: 'Pescado', value: 25, color: '#82ca9d' },
  { name: 'Verdura', value: 20, color: '#ffc658' },
  { name: 'Fruta', value: 15, color: '#ff7300' },
  { name: 'Otros', value: 5, color: '#00ff88' },
];

const AdminDashboard: React.FC = () => {
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
          <LineChart data={dailyRevenueData}>
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