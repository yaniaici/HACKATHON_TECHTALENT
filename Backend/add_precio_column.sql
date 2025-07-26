-- Script para agregar columna precio a la tabla producto
-- Ejecutar en MySQL

USE marketplace;

-- Agregar columna precio a la tabla producto
ALTER TABLE producto ADD COLUMN precio DECIMAL(10,2) DEFAULT 10.00 AFTER nombre;

-- Actualizar precios existentes con valores realistas según el tipo
UPDATE producto SET precio = 15.00 WHERE tipo = 'carne';
UPDATE producto SET precio = 12.00 WHERE tipo = 'pescado';
UPDATE producto SET precio = 8.00 WHERE tipo = 'verdura';
UPDATE producto SET precio = 6.00 WHERE tipo = 'fruta';
UPDATE producto SET precio = 4.50 WHERE tipo = 'lácteo';
UPDATE producto SET precio = 3.00 WHERE tipo = 'panadería';
UPDATE producto SET precio = 5.00 WHERE tipo = 'conservas';
UPDATE producto SET precio = 2.50 WHERE tipo = 'especias';
UPDATE producto SET precio = 20.00 WHERE tipo = 'aceite';
UPDATE producto SET precio = 8.00 WHERE tipo = 'huevos';
UPDATE producto SET precio = 25.00 WHERE tipo = 'miel';

-- Verificar que se agregó correctamente
SELECT id, nombre, precio, tipo FROM producto LIMIT 10; 