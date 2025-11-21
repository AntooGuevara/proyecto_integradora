import mysql.connector
from mysql.connector import Error

class GestionTransaccionMySQL:
    """Clase que gestiona la lógica del diagrama de actividades usando MySQL."""
    
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conexion = None
        self._conectar()

    def _conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conexion.is_connected():
                print(f"✅ Conexión a MySQL exitosa, DB: {self.database}")
                self._crear_tablas_si_necesario() 
            
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")

   


    def registrar_cliente(self, nombre: str, email: str) -> int:
        sql = "INSERT INTO Cliente (nombre, email) VALUES (%s, %s);"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (nombre, email))
            self.conexion.commit()
            cliente_id = cursor.lastrowid
            print(f"👤 Cliente '{nombre}' registrado con ID: {cliente_id}")
            return cliente_id
        except Error as e:
            print(f"❌ Error al registrar cliente: {e}")
            self.conexion.rollback()
            return -1
        finally:
            cursor.close()
            
    def generar_orden(self, cliente_id: int) -> int:
        sql = "INSERT INTO Orden (cliente_id) VALUES (%s);"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (cliente_id,))
            self.conexion.commit()
            orden_id = cursor.lastrowid
            print(f"🛒 Orden generada para cliente {cliente_id} con ID: {orden_id}")
            return orden_id
        except Error as e:
            print(f"❌ Error al generar orden: {e}")
            self.conexion.rollback()
            return -1
        finally:
            cursor.close()
    
    def calcular_subtotal(self, orden_id: int) -> float:

        cursor = self.conexion.cursor()
        subtotal = 0.0
        
        try:
            # 1. Calcular el subtotal 
            sql_subtotal = """
                SELECT SUM(DO.cantidad * DO.precio_unitario)
                FROM DetalleOrden DO
                WHERE DO.orden_id = %s;
            """
            cursor.execute(sql_subtotal, (orden_id,))
            resultado = cursor.fetchone()
            
            subtotal = resultado[0] if resultado and resultado[0] is not None else 0.0
            
            # 2. Actualizar el campo subtotal en "orden"
            sql_update = "UPDATE Orden SET subtotal = %s WHERE orden_id = %s;"
            cursor.execute(sql_update, (subtotal, orden_id))
            self.conexion.commit()
            
            print(f"🧮 Subtotal calculado y actualizado para la orden {orden_id}: {subtotal:.2f}")
            return subtotal
        
        except Error as e:
            print(f"❌ Error al calcular subtotal: {e}")
            self.conexion.rollback()
            return 0.0
        finally:
            cursor.close()

    def cerrar_conexion(self):
        """Cierra la conexión de la base de datos."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Desconexión de MySQL.")

if __name__ == '__main__':
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'bd_integradora',
        'user': 'root', 
        'password': '' 
    }
    
    gestion = GestionTransaccionMySQL(**DB_CONFIG)
    