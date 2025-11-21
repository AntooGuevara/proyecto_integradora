import mysql.connector
from datetime import datetime
from abc import ABC, abstractmethod

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='bd_integradora'
            )
        except mysql.connector.Error as e:
            print(f"Error al conectar: {e}")
    
    # def disconnect(self):
    #     if self.connection:
    #         self.connection.close()

class Usuario(ABC):
    def __init__(self, id_usuario=None, correo_electronico=None, password=None, tipo=None):
        self.id_usuario = id_usuario
        self.correo_electronico = correo_electronico
        self.password = password
        self.tipo = tipo
        self.db = Database()
    
    def registrar_usuario(self):
        """Caso de uso: Registrar usuario"""
        try:
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO usuario (correoElectronico, password, tipo) 
                     VALUES (%s, %s, %s)"""
            valores = (self.correo_electronico, self.password, self.tipo)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_usuario = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al registrar usuario: {e}")
            return False
    
    def iniciar_sesion(self):
        """Caso de uso: Iniciar sesión"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            sql = "SELECT * FROM usuario WHERE correoElectronico = %s AND password = %s"
            cursor.execute(sql, (self.correo_electronico, self.password))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                self.id_usuario = resultado['idUsuario']
                self.tipo = resultado['tipo']
                return True
            return False
        except mysql.connector.Error as e:
            print(f"Error al iniciar sesión: {e}")
            return False
    
    @abstractmethod
    def registrar_cliente(self):
        """Caso de uso: Registrar cliente"""
        pass

class Cliente(Usuario):
    def __init__(self, id_cliente=None, nombre=None, telefono=None, direccion=None, correo=None):
        super().__init__()
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
        self.tipo = 'cliente'
    def registrar_cliente(self):
        """Caso de uso: Registrar cliente (completo)"""
        if not self.registrar_usuario():
            return False
        try:
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO cliente (idUsuario, nombre, telefono, direccion, correo) 
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (self.id_usuario, self.nombre, self.telefono, self.direccion, self.correo)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_cliente = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al registrar cliente: {e}")
            return False
    def generar_orden(self, productos):
        """Caso de uso: Generar orden"""
        try:
            orden = Orden(id_cliente=self.id_cliente)
            if not orden.crear():
                return None
            
            for producto in productos:
                subtotal = producto['precio'] * producto['cantidad']
                orden.agregar_detalle(producto['id_producto'], producto['cantidad'], subtotal)
            
            orden.actualizar_total()
            return orden
        except Exception as e:
            print(f"Error al generar orden: {e}")
            return None
    def cancelar_orden(self, id_orden):
        """Caso de uso: Cancelar orden"""
        try:
            cursor = self.db.connection.cursor()
            sql = "UPDATE orden SET estado = 'cancelada' WHERE idOrden = %s AND idCliente = %s"
            cursor.execute(sql, (id_orden, self.id_cliente))
            self.db.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al cancelar orden: {e}")
            return False

class Empleado(Usuario):
    def __init__(self, id_empleado=None, nombre=None, puesto=None):
        super().__init__()
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.puesto = puesto
        self.tipo = 'empleado'
    
    def registrar_cliente(self, cliente_data):
        """Caso de uso: Registrar cliente (como empleado)"""
        cliente = Cliente(**cliente_data)
        return cliente.registrar_cliente()
    
    def actualizar_productos(self, id_producto, nuevos_datos):
        """Caso de uso: Actualizar productos"""
        try:
            cursor = self.db.connection.cursor()
            
            # Construir la consulta dinámicamente
            campos = []
            valores = []
            for campo, valor in nuevos_datos.items():
                campos.append(f"{campo} = %s")
                valores.append(valor)
            
            valores.append(id_producto)
            sql = f"UPDATE producto SET {', '.join(campos)} WHERE idProducto = %s"
            
            cursor.execute(sql, valores)
            self.db.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al actualizar producto: {e}")
            return False
    
    def calcular_subtotal(self, id_orden):
        """Caso de uso: Calcular subtotal"""
        try:
            cursor = self.db.connection.cursor()
            sql = "SELECT SUM(subtotal) as total FROM detalleOrden WHERE idOrden = %s"
            cursor.execute(sql, (id_orden,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado[0] if resultado[0] else 0.0
        except mysql.connector.Error as e:
            print(f"Error al calcular subtotal: {e}")
            return 0.0

class Orden:
    def __init__(self, id_orden=None, fecha=None, total=0.0, estado='pendiente', id_cliente=None, id_empleado=None):
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
    
    def actualizar_total(self):
        """Actualiza el total de la orden en la base de datos"""
        try:
            total = sum(detalle.subtotal for detalle in self.detalles)
            cursor = self.db.connection.cursor()
            sql = "UPDATE orden SET total = %s WHERE idOrden = %s"
            cursor.execute(sql, (total, self.id_orden))
            self.db.connection.commit()
            cursor.close()
            self.total = total
            return True
        except mysql.connector.Error as e:
            print(f"Error al actualizar total: {e}")
            return False

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

class Producto:
    def __init__(self, id_producto=None, nombre=None, descripcion=None, precio=None, stock=0, disponibilidad=True):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.disponibilidad = disponibilidad
        self.db = Database()
    
    def crear(self):
        try:
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO producto (nombre, descripcion, precio, stock, disponibilidad) 
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (self.nombre, self.descripcion, self.precio, self.stock, self.disponibilidad)
            cursor.execute(sql, valores)
            self.db.connection.commit()
            self.id_producto = cursor.lastrowid
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error al crear producto: {e}")
            return False

# # Ejemplo de uso de los casos de uso
# if __name__ == "__main__":
#     # Caso de uso: Registrar cliente
#     cliente = Cliente(
#         correo_electronico="cliente@email.com",
#         password="123456",
#         nombre="Ana García",
#         telefono="555-1234",
#         direccion="Calle Principal 123"
#     )
    
#     if cliente.registrar_cliente():
#         print("Cliente registrado exitosamente")
    
#     # Caso de uso: Iniciar sesión
#     if cliente.iniciar_sesion():
#         print("Sesión iniciada como cliente")
    
#     # Caso de uso: Generar orden
#     productos_orden = [
#         {'id_producto': 1, 'cantidad': 2, 'precio': 25.50},
#         {'id_producto': 2, 'cantidad': 1, 'precio': 100.00}
#     ]
    
#     orden = cliente.generar_orden(productos_orden)
#     if orden:
#         print(f"Orden generada con ID: {orden.id_orden}")
    
#     # Caso de uso: Calcular subtotal (empleado)
#     empleado = Empleado()
#     subtotal = empleado.calcular_subtotal(orden.id_orden)
#     print(f"Subtotal de la orden: {subtotal}")