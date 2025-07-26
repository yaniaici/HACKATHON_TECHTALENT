import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '@/types';
import { login as apiLogin, createUsuario } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (userData: Omit<User, 'id'> & { password: string }) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedUser = sessionStorage.getItem('currentUser');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const register = async (userData: Omit<User, 'id'> & { password: string }): Promise<boolean> => {
    try {
      const response = await createUsuario({
        nombre: userData.name,
        primer_apellido: userData.firstSurname,
        segundo_apellido: userData.secondSurname,
        email: userData.email,
        direccion: userData.address,
        telefono: userData.phone,
        password: userData.password,
        role: userData.role || 'cliente'
      });

      if (response.success) {
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error registering user:', error);
      return false;
    }
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await apiLogin({ correo: email, contraseña: password });
      
      if (response.success && response.user) {
        const userWithCorrectFormat: User = {
          id: response.user.id.toString(),
          name: response.user.nombre,
          firstSurname: response.user.primer_apellido,
          secondSurname: response.user.segundo_apellido,
          email: response.user.email,
          address: response.user.direccion,
          phone: response.user.telefono,
          role: response.user.role
        };
        
        setUser(userWithCorrectFormat);
        sessionStorage.setItem('currentUser', JSON.stringify(userWithCorrectFormat));
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error logging in:', error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    sessionStorage.removeItem('currentUser');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};