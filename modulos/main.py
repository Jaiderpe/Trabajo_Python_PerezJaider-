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
    
    def registrar_venta(self, venta):
        venta_dict = {
            'fecha': venta.fecha,
            'cliente': {'nombre': venta.cliente.nombre, 'direccion': venta.cliente.direccion},
            'empleado': {'nombre': venta.empleado.nombre, 'cargo': venta.empleado.cargo},
            'productos': [{'nombre': p.nombre, 'cantidad': p.cantidad, 'precio': p.precio} for p in venta.productos]
        }
        self.ventas.append(venta_dict)
        for producto in venta.productos:
            if producto.nombre in self.stock:
                self.stock[producto.nombre] -= producto.cantidad
            else:
                self.stock[producto.nombre] = -producto.cantidad
        self.guardar_datos()
    def registrar_compra(self, compra):
        compra_dict = {
            'fecha': compra.fecha,
            'proveedor': {'nombre': compra.proveedor.nombre, 'contacto': compra.proveedor.contacto},
            'productos': [{'nombre': p.nombre, 'cantidad': p.cantidad, 'precio': p.precio} for p in compra.productos]
        }
        self.compras.append(compra_dict)
        for producto in compra.productos:
            if producto.nombre in self.stock:
                self.stock[producto.nombre] += producto.cantidad
            else:
                self.stock[producto.nombre] = producto.cantidad
        self.guardar_datos()
    def generar_informe_ventas(self, inicio, fin):
        print(f"\nInforme de Ventas desde {inicio} hasta {fin}")
        total_ingresos = 0
        for venta in self.ventas:
            fecha_venta = datetime.strptime(venta['fecha'], '%Y-%m-%d')
            if inicio <= fecha_venta <= fin:
                print(f"Fecha: {venta['fecha']}, Cliente: {venta['cliente']['nombre']}, Dirección: {venta['cliente']['direccion']}")
                print(f"Empleado: {venta['empleado']['nombre']}, Cargo: {venta['empleado']['cargo']}")
                for producto in venta['productos']:
                    print(f"  Producto: {producto['nombre']}, Cantidad: {producto['cantidad']}, Precio: {producto['precio']}")
                    total_ingresos += producto['cantidad'] * producto['precio']
        print(f"Total de ingresos: {total_ingresos}\n")

    def generar_informe_stock(self):
        print("\nInforme de Stock")
        for nombre, cantidad in self.stock.items():
            print(f"Producto: {nombre}, Cantidad en stock: {cantidad}\n")
