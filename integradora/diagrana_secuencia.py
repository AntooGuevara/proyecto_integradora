import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    'host': 'localhost',
    'database': 'bd_integradora',
    'user': 'root',
    'password': ''
}

class SistemaVentas:
    
    def __init__(self, config):
        self.conexion = None
        self.config = config
        self._conectar()
        self.orden_activa_id = None
        
    def _conectar(self):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            if self.conexion.is_connected():
                print(f"✅ Conexión a MySQL exitosa, DB: {self.config['database']}")

            
        except Error as e:
            print(f"❌ Error al conectar a MySQL. Asegúrate de que la base de datos y las credenciales son correctas: {e}")

    def iniciar_sesion(self, email: str):
        sql = "SELECT cliente_id FROM Cliente WHERE email = %s;"
        cursor = self.conexion.cursor(buffered=True)
        try:
            cursor.execute(sql, (email,))
            resultado = cursor.fetchone()
            if resultado:
                cliente_id = resultado[0]
                print(f"🔑 Cliente ID {cliente_id} inició sesión.")
                return cliente_id
            else:
                print("❌ Sesión fallida. Cliente no encontrado.")
                return -1
        except Error as e:
            print(f"Error en iniciar sesión: {e}")
            return -1
        finally:
            cursor.close()

    def seleccionar_producto(self, producto_id: int):
        sql = "SELECT nombre, precio, stock FROM Producto WHERE producto_id = %s;"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (producto_id,))
            producto = cursor.fetchone()
            if producto:
                print(f"🔍 Producto seleccionado: {producto[0]} (Precio: {producto[1]})")
                return {"id": producto_id, "nombre": producto[0], "precio": float(producto[1])}
            else:
                print("Producto no encontrado en el catálogo.")
                return None
        except Error as e:
            print(f"Error al seleccionar producto: {e}")
            return None
        finally:
            cursor.close()

    def agregar_al_carrito(self, producto_data: dict, cantidad: int):

        if producto_data:
            producto_data['cantidad'] = cantidad
            print(f"🛒 Agregado al carrito: {cantidad}x {producto_data['nombre']}")
            return producto_data
        return None

    def confirmar_al_carrito(self, cliente_id: int, items_carrito: list) -> int:

        cursor = self.conexion.cursor()
        
        try:
            sql_orden = "INSERT INTO Orden (cliente_id, estado) VALUES (%s, 'PENDIENTE');"
            cursor.execute(sql_orden, (cliente_id,))
            orden_id = cursor.lastrowid            
            sql_detalle = "INSERT INTO DetalleOrden (orden_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s);"
            
            total_orden = 0.0
            for item in items_carrito:
                precio = item['precio']
                cantidad = item['cantidad']
                subtotal_item = precio * cantidad
                
                cursor.execute(sql_detalle, (orden_id, item['id'], cantidad, precio))
                total_orden += subtotal_item
                
            sql_update_total = "UPDATE Orden SET subtotal = %s WHERE orden_id = %s;"
            cursor.execute(sql_update_total, (total_orden, orden_id))
            
            self.conexion.commit()
            self.orden_activa_id = orden_id
            print(f"🛍️ Orden ID {orden_id} generada con éxito. Total: {total_orden:.2f}")
            return orden_id
            
        except Error as e:
            print(f"❌ Error al confirmar el carrito y generar la orden: {e}")
            self.conexion.rollback()
            return -1
        finally:
            cursor.close()

    def pago_confirmado(self):
        if self.orden_activa_id is None:
            print("❌ No hay orden activa para confirmar pago.")
            return False

        sql = "UPDATE Orden SET estado = 'ACTIVA' WHERE orden_id = %s AND estado = 'PENDIENTE';"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (self.orden_activa_id,))
            self.conexion.commit()
            if cursor.rowcount > 0:
                print(f"💳 Pago confirmado. Orden ID {self.orden_activa_id} es ahora ACTIVA.")
                return True
            return False
        except Error as e:
            print(f"Error al confirmar pago: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def cancelar_orden(self):
        if self.orden_activa_id is None:
            print("❌ No hay orden activa para cancelar.")
            return False

        sql = "UPDATE Orden SET estado = 'CANCELADA' WHERE orden_id = %s AND estado != 'COMPLETADA';"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (self.orden_activa_id,))
            self.conexion.commit()
            if cursor.rowcount > 0:
                print(f"🛑 Orden ID {self.orden_activa_id} ha sido CANCELADA.")
                return True
            return False
        except Error as e:
            print(f"Error al cancelar la orden: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()
            
    def finalizar_orden(self):
        if self.orden_activa_id is None:
            print("❌ No hay orden activa para finalizar.")
            return False

        sql = "UPDATE Orden SET estado = 'FINALIZADA' WHERE orden_id = %s AND estado = 'ACTIVA';"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (self.orden_activa_id,))
            self.conexion.commit()
            if cursor.rowcount > 0:
                print(f"✅ Orden ID {self.orden_activa_id} ha sido FINALIZADA. Fin del periodo de venta.")
                return True
            return False
        except Error as e:
            print(f"Error al finalizar la orden: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()
            
    def cerrar_conexion(self):
        """Cierra la conexión de la base de datos."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Desconexión de MySQL.")
