import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Save, X } from 'lucide-react';
import Header from '@/components/Header';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useAuth } from '@/context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Product } from '@/types';
import { categories } from '@/data/products';
import { useProducts } from '@/hooks/useProducts';
import { useToast } from '@/hooks/use-toast';

const Admin: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  const { products, loading, addProduct, editProduct, removeProduct } = useProducts();
  const [isEditing, setIsEditing] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    category: '',
    provider: '',
    origin: '',
    image: '',
    allergens: [] as string[]
  });

  useEffect(() => {
    if (!user || user.role !== 'vendedor') {
      navigate('/');
      return;
    }
  }, [user, navigate]);

  const handleFormChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleAddProduct = () => {
    setIsEditing(true);
    setEditingProduct(null);
    setFormData({
      name: '',
      price: '',
      category: '',
      provider: '',
      origin: '',
      image: '/api/placeholder/300/200',
      allergens: []
    });
  };

  const handleEditProduct = (product: Product) => {
    setIsEditing(true);
    setEditingProduct(product);
    setFormData({
      name: product.name,
      price: product.price.toString(),
      category: product.category,
      provider: product.provider,
      origin: product.origin,
      image: product.image,
      allergens: product.allergens
    });
  };

  const handleSaveProduct = async () => {
    if (!formData.name || !formData.price || !formData.category || !formData.provider || !formData.origin) {
      toast({
        title: "Error",
        description: "Por favor completa todos los campos obligatorios",
        variant: "destructive"
      });
      return;
    }

    setIsSaving(true);

    const productData: Omit<Product, 'id'> = {
      name: formData.name,
      price: parseFloat(formData.price),
      category: formData.category,
      provider: formData.provider,
      origin: formData.origin,
      image: formData.image || '/api/placeholder/300/200',
      allergens: formData.allergens
    };

    try {
      let success = false;
      
      if (editingProduct) {
        success = await editProduct(editingProduct.id, productData);
      } else {
        success = await addProduct(productData);
      }

      if (success) {
        setIsEditing(false);
        setEditingProduct(null);
        
        toast({
          title: "Éxito",
          description: editingProduct ? "Producto actualizado correctamente" : "Producto creado correctamente",
        });
      } else {
        toast({
          title: "Error",
          description: "No se pudo guardar el producto. Inténtalo de nuevo.",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Ocurrió un error al guardar el producto",
        variant: "destructive"
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteProduct = async (productId: string, productName: string) => {
    if (!confirm(`¿Estás seguro de que quieres eliminar el producto "${productName}"?`)) {
      return;
    }

    try {
      const success = await removeProduct(productId);
      
      if (success) {
        toast({
          title: "Producto eliminado",
          description: "El producto ha sido eliminado correctamente",
        });
      } else {
        toast({
          title: "Error",
          description: "No se pudo eliminar el producto. Inténtalo de nuevo.",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Ocurrió un error al eliminar el producto",
        variant: "destructive"
      });
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditingProduct(null);
  };

  if (!user || user.role !== 'vendedor') {
    return null;
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-market-beige">
        <Header />
        <main className="max-w-7xl mx-auto p-6">
          <div className="flex justify-center items-center h-64">
            <div className="text-lg text-gray-600">Cargando productos...</div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-market-beige">
      <Header />
      
      <main className="max-w-7xl mx-auto p-6">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Administración de Productos</h1>
          {!isEditing && (
            <Button 
              onClick={handleAddProduct}
              className="bg-market-green hover:bg-market-green-light text-white"
            >
              <Plus className="h-4 w-4 mr-2" />
              Añadir Producto
            </Button>
          )}
        </div>

        {isEditing && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-xl font-semibold mb-6">
              {editingProduct ? 'Editar Producto' : 'Nuevo Producto'}
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <Label htmlFor="name">Nombre del Producto*</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => handleFormChange('name', e.target.value)}
                  placeholder="Nombre del producto"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="price">Precio (€)*</Label>
                <Input
                  id="price"
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => handleFormChange('price', e.target.value)}
                  placeholder="0.00"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="category">Categoría*</Label>
                <Select value={formData.category} onValueChange={(value) => handleFormChange('category', value)}>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Selecciona una categoría" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((category) => (
                      <SelectItem key={category.id} value={category.id}>
                        {category.icon} {category.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="provider">Proveedor*</Label>
                <Input
                  id="provider"
                  value={formData.provider}
                  onChange={(e) => handleFormChange('provider', e.target.value)}
                  placeholder="Nombre del proveedor"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="origin">Origen*</Label>
                <Input
                  id="origin"
                  value={formData.origin}
                  onChange={(e) => handleFormChange('origin', e.target.value)}
                  placeholder="Ciudad, región o país"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="image">URL de la Imagen</Label>
                <Input
                  id="image"
                  value={formData.image}
                  onChange={(e) => handleFormChange('image', e.target.value)}
                  placeholder="https://ejemplo.com/imagen.jpg"
                  className="mt-1"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-4 mt-6">
              <Button variant="outline" onClick={handleCancel} disabled={isSaving}>
                <X className="h-4 w-4 mr-2" />
                Cancelar
              </Button>
              <Button 
                onClick={handleSaveProduct} 
                className="bg-market-green hover:bg-market-green-light" 
                disabled={isSaving}
              >
                <Save className="h-4 w-4 mr-2" />
                {isSaving ? 'Guardando...' : 'Guardar'}
              </Button>
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Producto
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Categoría
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Precio
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Proveedor
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Origen
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {products.map((product) => (
                  <tr key={product.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <img 
                          src={product.image} 
                          alt={product.name}
                          className="h-10 w-10 rounded-lg object-cover mr-3"
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {product.name}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center">
                        {categories.find(c => c.id === product.category)?.icon} 
                        <span className="ml-2">
                          {categories.find(c => c.id === product.category)?.name}
                        </span>
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      €{product.price.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {product.provider}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {product.origin}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end space-x-2">
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => handleEditProduct(product)}
                          className="h-8 w-8"
                          disabled={isEditing}
                        >
                          <Edit className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => handleDeleteProduct(product.id, product.name)}
                          className="h-8 w-8 text-red-600 hover:text-red-900"
                          disabled={isEditing}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {products.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500">No hay productos disponibles</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Admin;