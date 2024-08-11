import json
import os
from datetime import datetime

class Cliente:
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion

class Empleado:
    def __init__(self, nombre, cargo):
        self.nombre = nombre
        self.cargo = cargo

class Proveedor:
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


def ingresar_datos_producto():
    productos = []
    while True:
        nombre = input("Ingrese el nombre del producto: ")
        cantidad = int(input("Ingrese la cantidad: "))
        precio = float(input("Ingrese el precio: "))
        productos.append(Producto(nombre, cantidad, precio))
        
        otra = input("¿Desea ingresar otro producto? (s/n): ")
        if otra.lower() != 's':
            break
    return productos

def registrar_venta(sistema):
    fecha = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
    nombre_cliente = input("Ingrese el nombre del cliente: ")
    direccion_cliente = input("Ingrese la dirección del cliente: ")
    cliente = Cliente(nombre_cliente, direccion_cliente)
    
    nombre_empleado = input("Ingrese el nombre del empleado que realizó la venta: ")
    cargo_empleado = input("Ingrese el cargo del empleado: ")
    empleado = Empleado(nombre_empleado, cargo_empleado)
    
    productos = ingresar_datos_producto()
    venta = Venta(fecha, cliente, empleado, productos)
    sistema.registrar_venta(venta)
    print("Venta registrada con éxito.\n")

def registrar_compra(sistema):
    fecha = input("Ingrese la fecha de la compra (YYYY-MM-DD): ")
    nombre_proveedor = input("Ingrese el nombre del proveedor: ")
    contacto_proveedor = input("Ingrese el contacto del proveedor: ")
    proveedor = Proveedor(nombre_proveedor, contacto_proveedor)
    
    productos = ingresar_datos_producto()
    compra = Compra(fecha, proveedor, productos)
    sistema.registrar_compra(compra)
    print("Compra registrada con éxito.\n")

def generar_informe_ventas(sistema):
    inicio = input("Ingrese la fecha de inicio del informe (YYYY-MM-DD): ")
    fin = input("Ingrese la fecha de fin del informe (YYYY-MM-DD): ")
    inicio_dt = datetime.strptime(inicio, '%Y-%m-%d')
    fin_dt = datetime.strptime(fin, '%Y-%m-%d')
    sistema.generar_informe_ventas(inicio_dt, fin_dt)

def generar_informe_stock(sistema):
    sistema.generar_informe_stock()

def menu():
    sistema = SistemaGestion()
    
    while True:
        print("\nSistema de Gestión de Ventas y Compras")
        print("1. Registrar Venta")
        print("2. Registrar Compra")
        print("3. Generar Informe de Ventas")
        print("4. Generar Informe de Stock")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_venta(sistema)
        elif opcion == "2":
            registrar_compra(sistema)
        elif opcion == "3":
            generar_informe_ventas(sistema)
        elif opcion == "4":
            generar_informe_stock(sistema)
        elif opcion == "5":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, seleccione nuevamente.")
if __name__ == "__main__":
    menu()
