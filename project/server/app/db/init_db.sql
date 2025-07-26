-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS marketplace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE marketplace;

-- Tabla usuario
CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido1 VARCHAR(100) NOT NULL,
    apellido2 VARCHAR(100),
    correo VARCHAR(255) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    rol ENUM('cliente', 'vendedor') NOT NULL
);

-- Tabla producto
CREATE TABLE IF NOT EXISTS producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    alergenos VARCHAR(255),
    paradero VARCHAR(255) NOT NULL,
    origen VARCHAR(255) NOT NULL,
    id_vendedor INT NOT NULL,
    FOREIGN KEY (id_vendedor) REFERENCES usuario(id) ON DELETE CASCADE
);

-- Tabla pedido
CREATE TABLE IF NOT EXISTS pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    contenido TEXT NOT NULL,
    destino VARCHAR(255) NOT NULL,
    estado ENUM('pendiente', 'enviado', 'entregado', 'cancelado') NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id) ON DELETE CASCADE
);

-- Insertar 10 usuarios de ejemplo (contraseña: '123456' en hash bcrypt)
INSERT INTO usuario (nombre, apellido1, apellido2, correo, contraseña, direccion, telefono, rol) VALUES
('Juan', 'Pérez', 'García', 'juan1@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Mayor 1', '600000001', 'cliente'),
('Ana', 'López', 'Martínez', 'ana2@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Sol 2', '600000002', 'cliente'),
('Luis', 'Sánchez', 'Ruiz', 'luis3@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Luna 3', '600000003', 'cliente'),
('Marta', 'Gómez', 'Díaz', 'marta4@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Mar 4', '600000004', 'cliente'),
('Pedro', 'Fernández', 'Moreno', 'pedro5@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Río 5', '600000005', 'cliente'),
('Lucía', 'Jiménez', 'Navarro', 'lucia6@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Viento 6', '600000006', 'vendedor'),
('Carlos', 'Romero', 'Serrano', 'carlos7@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Fuego 7', '600000007', 'vendedor'),
('Elena', 'Torres', 'Ramos', 'elena8@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Tierra 8', '600000008', 'vendedor'),
('David', 'Vega', 'Castro', 'david9@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Nube 9', '600000009', 'vendedor'),
('Sara', 'Molina', 'Ortega', 'sara10@correo.com', '$2b$12$eImiTXuWVxfM37uY4JANjQ==', 'Calle Flor 10', '600000010', 'vendedor');

-- Insertar 10 productos de ejemplo
INSERT INTO producto (nombre, tipo, alergenos, paradero, origen, id_vendedor) VALUES
('Manzanas', 'fruta', 'A1', 'Mercado Central', 'Tarragona', 6),
('Naranjas', 'fruta', 'A2', 'Mercado Central', 'Valencia', 7),
('Leche', 'lácteo', 'B3', 'Tienda Bio', 'Tarragona', 8),
('Pan', 'panadería', 'A1,B3', 'Panadería Sol', 'Tarragona', 9),
('Queso', 'lácteo', 'A2', 'Mercado Central', 'Reus', 10),
('Tomates', 'verdura', '', 'Mercado Central', 'Tarragona', 6),
('Aceite', 'aceite', '', 'Tienda Bio', 'Siurana', 7),
('Huevos', 'huevos', '', 'Mercado Central', 'Tarragona', 8),
('Miel', 'miel', '', 'Tienda Bio', 'Prades', 9),
('Pera', 'fruta', 'A1', 'Mercado Central', 'Lleida', 10);

-- Insertar 10 pedidos de ejemplo
INSERT INTO pedido (id_usuario, id_producto, contenido, destino, estado) VALUES
(1, 1, '2kg de manzanas', 'Calle Mayor 1', 'pendiente'),
(2, 2, '1kg de naranjas', 'Calle Sol 2', 'enviado'),
(3, 3, '3L de leche', 'Calle Luna 3', 'entregado'),
(4, 4, '2 barras de pan', 'Calle Mar 4', 'cancelado'),
(5, 5, '500g de queso', 'Calle Río 5', 'pendiente'),
(1, 6, '1kg de tomates', 'Calle Mayor 1', 'pendiente'),
(2, 7, '1L de aceite', 'Calle Sol 2', 'enviado'),
(3, 8, '12 huevos', 'Calle Luna 3', 'entregado'),
(4, 9, '1 tarro de miel', 'Calle Mar 4', 'pendiente'),
(5, 10, '2kg de peras', 'Calle Río 5', 'pendiente'); 