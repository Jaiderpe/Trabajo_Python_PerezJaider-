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