import { useState, useEffect } from 'react';
import { Product } from '@/types';
import { getProductos, createProducto, updateProducto, deleteProducto } from '@/lib/api';

export const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const normalizeCategory = (cat: string) => {
    if (!cat) return '';
    const map: Record<string, string> = {
      'lácteo': 'lacteos',
      'lácteos': 'lacteos',
      'lacteo': 'lacteos',
      'panadería': 'panaderia',
      'panaderia': 'panaderia',
      'fruta': 'fruta',
      'verdura': 'verdura',
      'carne': 'carne',
      'pescado': 'pescado',
      'conservas': 'conservas',
      'especias': 'especias',
      'aceite': 'aceite',
      'huevos': 'huevos',
      'miel': 'miel'
    };
    return map[cat.toLowerCase()] || cat.toLowerCase();
  };

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await getProductos();
      if (response.success && response.productos) {
        // Transformar datos del backend al formato del frontend
        const formattedProducts: Product[] = response.productos.map((p: any) => ({
          id: p.id.toString(),
          name: p.nombre,
          price: parseFloat(p.precio),
          category: normalizeCategory(p.tipo),
          provider: p.paradero,
          origin: p.origen,
          image: p.imagen || '/api/placeholder/300/200',
          allergens: p.alergenos ? p.alergenos.split(',') : []
        }));
        setProducts(formattedProducts);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const addProduct = async (productData: Omit<Product, 'id'>) => {
    try {
      const response = await createProducto({
        name: productData.name,
        price: productData.price,
        category: productData.category,
        provider: productData.provider,
        origin: productData.origin,
        image: productData.image,
        allergens: productData.allergens.join(',')
      });

      if (response.success) {
        await fetchProducts(); // Refrescar la lista
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error adding product:', error);
      return false;
    }
  };

  const editProduct = async (productId: string, productData: Omit<Product, 'id'>) => {
    try {
      const response = await updateProducto(parseInt(productId), {
        name: productData.name,
        price: productData.price,
        category: productData.category,
        provider: productData.provider,
        origin: productData.origin,
        image: productData.image,
        allergens: productData.allergens.join(',')
      });

      if (response.success) {
        await fetchProducts(); // Refrescar la lista
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error updating product:', error);
      return false;
    }
  };

  const removeProduct = async (productId: string) => {
    try {
      const response = await deleteProducto(parseInt(productId));

      if (response.success) {
        await fetchProducts(); // Refrescar la lista
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error deleting product:', error);
      return false;
    }
  };

  return { 
    products, 
    loading, 
    updateProducts: fetchProducts, // Mantener compatibilidad
    addProduct,
    editProduct,
    removeProduct,
    refetch: fetchProducts
  };
};