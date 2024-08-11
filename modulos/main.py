import json
import os
from datetime import datetime

class cliente:
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion
class Empleado:
    def __init__(self, nombre,cargo):
        self.nombre = nombre
        self.cargo = cargo 
class proveedor:
    def __init__(self, nombre, contacto):
        self.nombre = nombre
        self.contacto = contacto
class Producto:
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

class Venta:
    def __init__(self, fecha, cliente, empleado, productos):
        self.fecha = fecha
        self.cliente = cliente
        self.empleado = empleado
        self.productos = productos

class Compra:
    def __init__(self, fecha, proveedor, productos):
        self.fecha = fecha
        self.proveedor = proveedor
        self.productos = productos    
class SistemaGestion:
    def __init__(self, archivo_json="datos/datos.json"):
        self.archivo_json = archivo_json
        os.makedirs(os.path.dirname(self.archivo_json), exist_ok=True)
        self.cargar_datos()
    def cargar_datos(self):
        try:
            with open(self.archivo_json, 'r') as archivo:
                datos = json.load(archivo)
                self.ventas = datos.get('ventas', [])
                self.compras = datos.get('compras', [])
                self.stock = datos.get('stock', {})
        except FileNotFoundError:
            self.ventas = []
            self.compras = []
            self.stock = {}
    def guardar_datos(self):
        datos = {
            'ventas': self.ventas,
            'compras': self.compras,
            'stock': self.stock
        }
        with open(self.archivo_json, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
