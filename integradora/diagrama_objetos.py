import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                port='3307',
                password='',
                database='bd_integradora'
            )
            print("Conexión exitosa a la base de datos")
        except mysql.connector.Error as e:
            print(f"Error al conectar: {e}")
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

class Empleado:
    def __init__(self, id_empleado=None, nombre=None, puesto=None):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.puesto = puesto
        self.db = Database()
    
    def crear(self):
        try:
            cursor = self.db.connection.cursor()
            sql = "INSERT INTO empleado (nombre, puesto) VALUES (%s, %s)"
            valores = (self.nombre, self.puesto)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_empleado = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al crear empleado: {e}")
            return False
    
    def leer(self, id_empleado):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            sql = "SELECT * FROM empleado WHERE idEmpleado = %s"
            cursor.execute(sql, (id_empleado,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                self.id_empleado = resultado['idEmpleado']
                self.nombre = resultado['nombre']
                self.puesto = resultado['puesto']
                return True
            return False
        except mysql.connector.Error as e:
            print(f"Error al leer empleado: {e}")
            return False

class Cliente:
    def __init__(self, id_cliente=None, nombre=None, telefono=None, direccion=None, correo=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.db = Database()
    
    def crear(self):
        try:
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO cliente (nombre, telefono, direccion, correo) 
                     VALUES (%s, %s, %s, %s)"""
            valores = (self.nombre, self.telefono, self.direccion, self.correo)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_cliente = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al crear cliente: {e}")
            return False
    
    def leer(self, id_cliente):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            sql = "SELECT * FROM cliente WHERE idCliente = %s"
            cursor.execute(sql, (id_cliente,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                self.id_cliente = resultado['idCliente']
                self.nombre = resultado['nombre']
                self.telefono = resultado['telefono']
                self.direccion = resultado['direccion']
                self.correo = resultado['correo']
                return True
            return False
        except mysql.connector.Error as e:
            print(f"Error al leer cliente: {e}")
            return False

class Usuario:
    def __init__(self, correo_electronico=None, password=None):
        self.correo_electronico = correo_electronico
        self.password = password
        self.db = Database()
    
    def crear(self):
        try:
            cursor = self.db.connection.cursor()
            sql = "INSERT INTO usuario (correoElectronico, password) VALUES (%s, %s)"
            valores = (self.correo_electronico, self.password)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al crear usuario: {e}")
            return False
    
    def iniciar_sesion(self):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            sql = "SELECT * FROM usuario WHERE correoElectronico = %s AND password = %s"
            cursor.execute(sql, (self.correo_electronico, self.password))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado is not None
        except mysql.connector.Error as e:
            print(f"Error al iniciar sesión: {e}")
            return False

class Producto:
    def __init__(self, id_producto=None, nombre=None, descripcion=None, precio=None, disponibilidad=True):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.disponibilidad = disponibilidad
        self.db = Database()
    
    def crear(self):
        try:
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO producto (nombre, descripcion, precio, disponibilidad) 
                     VALUES (%s, %s, %s, %s)"""
            valores = (self.nombre, self.descripcion, self.precio, self.disponibilidad)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_producto = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al crear producto: {e}")
            return False
    
    def leer(self, id_producto):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            sql = "SELECT * FROM producto WHERE idProducto = %s"
            cursor.execute(sql, (id_producto,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                self.id_producto = resultado['idProducto']
                self.nombre = resultado['nombre']
                self.descripcion = resultado['descripcion']
                self.precio = resultado['precio']
                self.disponibilidad = resultado['disponibilidad']
                return True
            return False
        except mysql.connector.Error as e:
            print(f"Error al leer producto: {e}")
            return False

class Orden:
    def __init__(self, id_orden=None, fecha=None, total=0.0, estado=1, id_cliente=None, id_empleado=None):
        self.id_orden = id_orden
        self.fecha = fecha or datetime.now()
        self.total = total
        self.estado = estado
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
        self.detalles = []
        self.db = Database()
    
    def crear(self):
        try:
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO orden (fecha, total, estado, idCliente, idEmpleado) 
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (self.fecha, self.total, self.estado, self.id_cliente, self.id_empleado)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_orden = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al crear orden: {e}")
            return False
    
    def agregar_detalle(self, id_producto, cantidad, subtotal):
        detalle = DetalleOrden(id_orden=self.id_orden, id_producto=id_producto, 
                              cantidad=cantidad, subtotal=subtotal)
        self.detalles.append(detalle)
        self.total += subtotal

class DetalleOrden:
    def __init__(self, id_detalle=None, cantidad=0, subtotal=0.0, id_orden=None, id_producto=None):
        self.id_detalle = id_detalle
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.id_orden = id_orden
        self.id_producto = id_producto
        self.db = Database()
    
    def crear(self):
        try:
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO detalleOrden (cantidad, subtotal, idOrden, idProducto) 
                     VALUES (%s, %s, %s, %s)"""
            valores = (self.cantidad, self.subtotal, self.id_orden, self.id_producto)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_detalle = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al crear detalle: {e}")
            return False




# if __name__ == "__main__":
#     # Crear un cliente
#     cliente = Cliente(nombre="Juan Pérez", telefono="123456789", 
#                      direccion="Calle 123", correo="juan@email.com")
#     if cliente.crear():
#         print(f"Cliente creado con ID: {cliente.id_cliente}")
    
#     # Crear un producto
#     producto = Producto(nombre="Laptop", descripcion="Laptop gaming", 
#                        precio=1500.00, disponibilidad=True)
#     if producto.crear():
#         print(f"Producto creado con ID: {producto.id_producto}")
    
#     # Crear una orden
#     orden = Orden(id_cliente=cliente.id_cliente, id_empleado=1)
#     orden.agregar_detalle(producto.id_producto, 1, 1500.00)
    
#     if orden.crear():
#         print(f"Orden creada con ID: {orden.id_orden}")
        
#         # Guardar los detalles
#         for detalle in orden.detalles:
#             detalle.id_orden = orden.id_orden
#             detalle.crear()