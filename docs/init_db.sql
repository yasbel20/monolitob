-- Crear base de datos
CREATE DATABASE IF NOT EXISTS tienda_bolsos;
USE tienda_bolsos;

-- Crear tabla bolsos
CREATE TABLE IF NOT EXISTS bolsos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    tipo ENUM('bolso_mano','bandolera','mochila','clutch','tote','riñonera') NOT NULL,
    material VARCHAR(100) NOT NULL,
    color VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    descripcion TEXT NOT NULL,
    talla ENUM('pequeño','mediano','grande','xl') NOT NULL,
    temporada ENUM('primavera_verano','otoño_invierno','todo_el_año') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo
INSERT INTO bolsos 
(nombre, marca, tipo, material, color, precio, stock, descripcion, talla, temporada)
VALUES 
('Bolso Clásico Elegante','Prada','bolso_mano','Cuero genuino','Negro',450.00,15,'Bolso de mano elegante ideal para eventos formales','mediano','todo_el_año'),
('Bandolera Urban Style','Michael Kors','bandolera','Cuero sintético','Marrón',199.99,25,'Perfecta para el día a día, cómoda y espaciosa','pequeño','primavera_verano'),
('Mochila Adventure','The North Face','mochila','Nylon resistente','Azul marino',89.50,40,'Mochila deportiva con múltiples compartimentos','grande','todo_el_año'),
('Clutch de Noche Dorado','Guess','clutch','Tejido brillante','Dorado',125.00,10,'Perfecto para fiestas y eventos nocturnos','pequeño','otoño_invierno'),
('Tote Bag Espacioso','Coach','tote','Lona y cuero','Beige',285.00,18,'Ideal para llevar todo lo necesario en tu día','grande','primavera_verano'),
('Riñonera Deportiva','Nike','riñonera','Poliéster','Negro',35.00,50,'Compacta y práctica para actividades deportivas','pequeño','todo_el_año'),
('Bolso Vintage Retro','Guess','bolso_mano','Cuero envejecido','Camel',320.00,12,'Diseño retro con estilo atemporal','mediano','otoño_invierno'),
('Bandolera Chain','Zara','bandolera','Polipiel','Rojo',69.99,30,'Bandolera con cadena dorada, muy trendy','pequeño','primavera_verano');
