-- Script para actualizar precios en productos existentes
-- Ejecutar en MySQL

USE marketplace;

-- Verificar que la columna precio existe
DESCRIBE producto;

-- Actualizar precios existentes con valores realistas según el tipo
UPDATE producto SET precio = 15.00 WHERE tipo = 'carne' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 12.00 WHERE tipo = 'pescado' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 8.00 WHERE tipo = 'verdura' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 6.00 WHERE tipo = 'fruta' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 4.50 WHERE tipo = 'lácteo' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 3.00 WHERE tipo = 'panadería' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 5.00 WHERE tipo = 'conservas' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 2.50 WHERE tipo = 'especias' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 20.00 WHERE tipo = 'aceite' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 8.00 WHERE tipo = 'huevos' AND (precio IS NULL OR precio = 0);
UPDATE producto SET precio = 25.00 WHERE tipo = 'miel' AND (precio IS NULL OR precio = 0);

-- Establecer precio por defecto para productos sin tipo específico
UPDATE producto SET precio = 10.00 WHERE precio IS NULL OR precio = 0;

-- Verificar que se actualizaron correctamente
SELECT id, nombre, precio, tipo FROM producto LIMIT 10; 