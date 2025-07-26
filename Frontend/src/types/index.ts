export interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
  category: string;
  provider: string;
  origin: string;
  allergens: string[];
  quantity?: number;
}

export interface User {
  id: string;
  name: string;
  firstSurname: string;
  secondSurname: string;
  email: string;
  address: string;
  phone: string;
  role: 'cliente' | 'vendedor';
}

export interface CartItem extends Product {
  quantity: number;
}

export interface Order {
  id: string;
  userId: string;
  items: CartItem[];
  total: number;
  status: 'pendiente' | 'procesando' | 'enviado' | 'entregado';
  date: Date;
}

export interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
}