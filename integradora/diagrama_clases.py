import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                port='3307',
                user='root',      
                password='',      
                database='db_integradora'
            )
            print("Conexión a db_integradora establecida exitosamente!")
            return True
        except Error as e:
            print(f"Error de conexión: {e}")
            return False
    
    def registrar_cliente(self, correo, password):
        """Registra un nuevo cliente"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Cliente (correoElectronico, password) VALUES (%s, %s)",
                (correo, password)
            )
            self.connection.commit()
            print(f"Cliente {correo} registrado exitosamente!")
            return cursor.lastrowid
        except Error as e:
            print(f"Error al registrar cliente: {e}")
            return None
    
    def iniciar_sesion(self, correo, password):
        """Inicia sesión de un cliente"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Cliente WHERE correoElectronico = %s AND password = %s",
                (correo, password)
            )
            cliente = cursor.fetchone()
            return cliente
        except Error as e:
            print(f"Error al iniciar sesión: {e}")
            return None
    
    def mostrar_productos(self, disponibles=True):
        """Muestra todos los productos"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if disponibles:
                cursor.execute("SELECT * FROM Producto WHERE disponibilidad = TRUE")
            else:
                cursor.execute("SELECT * FROM Producto")
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener productos: {e}")
            return []
    
    def actualizar_estado_producto(self, id_producto, disponibilidad):
        """Actualiza la disponibilidad de un producto"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE Producto SET disponibilidad = %s WHERE idProducto = %s",
                (disponibilidad, id_producto)
            )
            self.connection.commit()
            print(f"Estado del producto {id_producto} actualizado a {disponibilidad}")
            return True
        except Error as e:
            print(f"Error al actualizar producto: {e}")
            return False
    
    def crear_orden(self, id_cliente, fecha_inicio, total=0):
        """Crea una nueva orden"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Orden (idCliente, fechaInicio, total) VALUES (%s, %s, %s)",
                (id_cliente, fecha_inicio, total)
            )
            self.connection.commit()
            orden_id = cursor.lastrowid
            print(f"Orden {orden_id} creada exitosamente!")
            return orden_id
        except Error as e:
            print(f"Error al crear orden: {e}")
            return None
    
    def agregar_detalle_orden(self, id_orden, id_producto, cantidad):
        """Agrega un producto a la orden"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO DetalleOrden (idOrden, idProducto, cantidad) VALUES (%s, %s, %s)",
                (id_orden, id_producto, cantidad)
            )
            self.connection.commit()
            print(f"Producto {id_producto} agregado a la orden {id_orden}")
            return True
        except Error as e:
            print(f"Error al agregar detalle: {e}")
            return False
    
    def calcular_total_orden(self, id_orden):
        """Calcula el total de una orden"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT SUM(p.precio * d.cantidad) as total
                FROM DetalleOrden d
                JOIN Producto p ON d.idProducto = p.idProducto
                WHERE d.idOrden = %s
            ''', (id_orden,))
            resultado = cursor.fetchone()
            total = resultado[0] if resultado[0] else 0
            
            # Actualizar el total en la orden
            cursor.execute(
                "UPDATE Orden SET total = %s WHERE idOrden = %s",
                (total, id_orden)
            )
            self.connection.commit()
            return total
        except Error as e:
            print(f"Error al calcular total: {e}")
            return 0
    
    def cancelar_orden(self, id_orden):
        """Cancela una orden"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE Orden SET estado = 'cancelada' WHERE idOrden = %s",
                (id_orden,)
            )
            self.connection.commit()
            print(f"Orden {id_orden} cancelada")
            return True
        except Error as e:
            print(f"Error al cancelar orden: {e}")
            return False
    
    def obtener_ordenes_cliente(self, id_cliente):
        """Obtiene todas las órdenes de un cliente"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Orden WHERE idCliente = %s ORDER BY fechaInicio DESC",
                (id_cliente,)
            )
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener órdenes: {e}")
            return []
    
    def mostrar_todas_tablas(self):
        """Muestra el contenido de todas las tablas"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            print("\n" + "="*50)
            print("CLIENTES")
            print("="*50)
            cursor.execute("SELECT * FROM Cliente")
            for cliente in cursor.fetchall():
                print(cliente)
            
            print("\n" + "="*50)
            print("PRODUCTOS")
            print("="*50)
            cursor.execute("SELECT * FROM Producto")
            for producto in cursor.fetchall():
                print(producto)
            
            print("\n" + "="*50)
            print("ÓRDENES")
            print("="*50)
            cursor.execute("SELECT * FROM Orden")
            for orden in cursor.fetchall():
                print(orden)
            
            print("\n" + "="*50)
            print("DETALLES DE ÓRDENES")
            print("="*50)
            cursor.execute("SELECT * FROM DetalleOrden")
            for detalle in cursor.fetchall():
                print(detalle)
                
        except Error as e:
            print(f"Error al mostrar datos: {e}")
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")

def ejemplo_uso_completo():
    db = DatabaseManager()
    
    if not db.connection:
        print("No se pudo conectar a la base de datos")
        return
    
    try:
        # 1. Registrar un nuevo cliente
        print("\n1. REGISTRANDO NUEVO CLIENTE")
        nuevo_id = db.registrar_cliente("ana.garcia@example.com", "ana123")
        
        # 2. Iniciar sesión
        print("\n2. INICIANDO SESIÓN")
        cliente = db.iniciar_sesion("ana.garcia@example.com", "ana123")
        if cliente:
            print(f"Bienvenido: {cliente['correoElectronico']}")
        
        # 3. Mostrar productos disponibles
        print("\n3. PRODUCTOS DISPONIBLES")
        productos = db.mostrar_productos()
        for producto in productos:
            print(f"- {producto['idProducto']}: {producto['nombre']} - ${producto['precio']}")
        
        # 4. Crear una nueva orden
        print("\n4. CREANDO NUEVA ORDEN")
        if cliente and productos:
            orden_id = db.crear_orden(cliente['idCliente'], '2024-01-20')
            
            # 5. Agregar productos a la orden
            if orden_id:
                # Agregar algunos productos de ejemplo
                db.agregar_detalle_orden(orden_id, productos[0]['idProducto'], 1)  # Laptop
                db.agregar_detalle_orden(orden_id, productos[1]['idProducto'], 2)  # Mouse
                
                # 6. Calcular total
                total = db.calcular_total_orden(orden_id)
                print(f"Total de la orden: ${total}")
        
        # 7. Mostrar todas las órdenes del cliente
        print("\n5. ÓRDENES DEL CLIENTE")
        if cliente:
            ordenes = db.obtener_ordenes_cliente(cliente['idCliente'])
            for orden in ordenes:
                print(f"Orden {orden['idOrden']}: {orden['estado']} - ${orden['total']}")
        
        # 8. Mostrar todo el contenido de las tablas
        print("\n6. CONTENIDO COMPLETO DE LA BASE DE DATOS")
        db.mostrar_todas_tablas()
        
    except Exception as e:
        print(f"Error en el ejemplo: {e}")
    finally:
        db.close()



if __name__ == "__main__":
    ejemplo_uso_completo()
    
