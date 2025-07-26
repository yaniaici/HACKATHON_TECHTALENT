-- Script para asignar categorías a productos que no las tienen
-- Ejecutar en MySQL

USE marketplace;

-- Asignar categorías específicas para productos conocidos usando IDs
UPDATE producto SET tipo = 'lácteo' WHERE id = 14 AND (tipo IS NULL OR tipo = ''); -- Leche
UPDATE producto SET tipo = 'panadería' WHERE id = 15 AND (tipo IS NULL OR tipo = ''); -- Pan
UPDATE producto SET tipo = 'lácteo' WHERE id = 16 AND (tipo IS NULL OR tipo = ''); -- Queso
UPDATE producto SET tipo = 'aceite' WHERE id = 18 AND (tipo IS NULL OR tipo = ''); -- Aceite
UPDATE producto SET tipo = 'huevos' WHERE id = 19 AND (tipo IS NULL OR tipo = ''); -- Huevos
UPDATE producto SET tipo = 'miel' WHERE id = 20 AND (tipo IS NULL OR tipo = ''); -- Miel

-- Verificar que se asignaron correctamente
SELECT id, nombre, tipo, precio FROM producto ORDER BY nombre; 