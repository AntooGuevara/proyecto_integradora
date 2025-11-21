import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'database': 'bd_integradora',
    'user': 'root',
    'password': ''
}

class GestorTransacciones:
    
    def __init__(self, config):
        self.conexion = None
        self.config = config
        self._conectar()

    def _conectar(self):
        """Establece la conexión con la base de datos MySQL."""
        try:
            self.conexion = mysql.connector.connect(**self.config)
            if self.conexion.is_connected():
                print(f"✅ Conexión a MySQL exitosa, DB: {self.config['database']}")
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")

    def procesar_orden(self, id_orden: int, id_usuario_procesa: int) -> bool:

        if not self.conexion or not self.conexion.is_connected():
            print("❌ No hay conexión activa a la base de datos.")
            return False

        cursor = self.conexion.cursor()
        
        try:
            self.conexion.start_transaction()
            print(f"🔒 Iniciando transacción para Orden ID {id_orden}...")

            sql_detalles = """
                SELECT 
                    DO.id_producto, DO.cantidad, I.cantidad_disponible
                FROM 
                    DetalleOrden DO
                JOIN 
                    Inventario I ON DO.id_producto = I.id_producto
                WHERE 
                    DO.id_orden = %s;
            """
            cursor.execute(sql_detalles, (id_orden,))
            detalles = cursor.fetchall()
            
            if not detalles:
                raise Exception(f"La orden ID {id_orden} no tiene detalles o los productos no están en inventario.")

            productos_vendidos = []
            
            for id_producto, cantidad_orden, stock_disponible in detalles:
                if cantidad_orden > stock_disponible:
                    raise Exception(f"Stock insuficiente para Producto ID {id_producto}. Necesario: {cantidad_orden}, Disponible: {stock_disponible}.")

                sql_inventario = """
                    UPDATE Inventario 
                    SET cantidad_disponible = cantidad_disponible - %s 
                    WHERE id_producto = %s;
                """
                cursor.execute(sql_inventario, (cantidad_orden, id_producto))
                
                sql_ventas = """
                    INSERT INTO Ventas (cantidad, fecha, id_usuario, id_producto)
                    VALUES (%s, NOW(), %s, %s);
                """
                cursor.execute(sql_ventas, (cantidad_orden, id_usuario_procesa, id_producto))
                productos_vendidos.append(id_producto)
            
            sql_orden = "UPDATE Órdenes SET estado = 'CONFIRMADA' WHERE id_orden = %s AND estado = 'PENDIENTE';"
            cursor.execute(sql_orden, (id_orden,))
            
            if cursor.rowcount == 0:
                raise Exception(f"No se pudo actualizar el estado de la orden {id_orden} (Quizás ya fue procesada).")

            self.conexion.commit()
            print(f"✅ Transacción completada y confirmada. {len(productos_vendidos)} producto(s) vendidos.")
            return True

        except Exception as e:
            self.conexion.rollback()
            print(f"❌ Transacción fallida. Se realizó ROLLBACK. Motivo: {e}")
            return False
            
        finally:
            cursor.close()


if __name__ == '__main__':
    gestor = GestorTransacciones(DB_CONFIG)
    
   