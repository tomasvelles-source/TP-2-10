from libro import Libro
from socio import Socio

class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = {}  # Diccionario para búsqueda rápida por ISBN (isbn: Libro)
        self.socios = {}    # Diccionario para búsqueda rápida por DNI (dni: Socio)

    def agregar_libro(self, libro):
        if libro.isbn in self.catalogo:
            raise ValueError(f"Ya existe un libro registrado con el ISBN {libro.isbn}.")
        self.catalogo[libro.isbn] = libro

    def registrar_socio(self, socio):
        if socio.dni in self.socios:
            raise ValueError(f"Ya existe un socio registrado con el DNI {socio.dni}.")
        self.socios[socio.dni] = socio

    def prestar(self, isbn, dni):
        if isbn not in self.catalogo:
            raise ValueError("El libro no existe en la biblioteca.")
        if dni not in self.socios:
            raise ValueError("El socio no existe en la biblioteca.")
        
        libro = self.catalogo[isbn]
        socio = self.socios[dni]

        if not libro.disponible:
            raise ValueError("El libro no está disponible para ser prestado.")
        if not socio.puede_pedir():
            raise ValueError("El socio alcanzó el límite de libros permitidos.")
            
        # Modificamos los estados
        libro.prestar()
        try:
            socio.agregar_libro(libro)
        except ValueError as e:
            # Revertimos el estado del libro si falla al agregarlo al socio
            libro.devolver()
            raise e

    def devolver(self, isbn, dni):
        if isbn not in self.catalogo:
            raise ValueError("El libro no existe en la biblioteca.")
        if dni not in self.socios:
            raise ValueError("El socio no existe en la biblioteca.")
        
        libro = self.catalogo[isbn]
        socio = self.socios[dni]

        if libro not in socio.libros:
            raise ValueError("Este socio no tiene prestado el libro indicado.")

        # Modificamos los estados
        socio.quitar_libro(libro)
        libro.devolver()

    def libros_disponibles(self):
        return [libro for libro in self.catalogo.values() if libro.disponible]