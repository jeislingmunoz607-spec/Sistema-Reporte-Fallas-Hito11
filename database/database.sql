CREATE DATABASE IF NOT EXISTS reporte_fallas;

USE reporte_fallas;

CREATE TABLE laboratorios (
    id_laboratorio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edificio VARCHAR(100)
);

CREATE TABLE equipos (
    id_equipo INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(30) NOT NULL UNIQUE,
    id_laboratorio INT NOT NULL,
    FOREIGN KEY (id_laboratorio)
    REFERENCES laboratorios(id_laboratorio)
);

CREATE TABLE reportes (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL UNIQUE,
    id_equipo INT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    fecha DATE NOT NULL,
    solucion TEXT,
    FOREIGN KEY (id_equipo)
    REFERENCES equipos(id_equipo)
);

INSERT INTO laboratorios (nombre, edificio)
VALUES ('Laboratorio 1', 'Edificio A');

INSERT INTO equipos (codigo, id_laboratorio)
VALUES ('PC-LAB01-01', 1);

INSERT INTO reportes
(numero, id_equipo, categoria, descripcion, estado, fecha, solucion)
VALUES
('REP-001', 1, 'Hardware',
 'Prueba de funcionamiento del equipo',
 'Pendiente', '2026-11-06', NULL
