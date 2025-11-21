import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'database': 'bd_integradora',
    'user': 'root',
    'password': ''
}

class GestionEstados:
    
    def __init__(self, config):
        self.conexion = None
        self.config = config
        self._conectar()
        
    def _conectar(self):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            if self.conexion.is_connected():
                print(f"✅ Conexión a MySQL exitosa, DB: {self.config['database']}")
                # Asumimos que las tablas ya existen
            
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")

    def cambiar_estado(self, entidad_id: int, nuevo_estado: str, estado_actual_requerido: str = None) -> bool:

        cursor = self.conexion.cursor()
        sql = "UPDATE Orden SET estado = %s WHERE orden_id = %s"
        params = [nuevo_estado, entidad_id]
        if estado_actual_requerido:
            sql += " AND estado = %s"
            params.append(estado_actual_requerido)

        try:
            cursor.execute(sql, tuple(params))
            self.conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"🔄 ID {entidad_id} transicionado de '{estado_actual_requerido or 'CUALQUIERA'}' a '{nuevo_estado}' con éxito.")
                return True
            else:
                print(f"⚠️ Falló la transición: ID {entidad_id} no está en el estado requerido '{estado_actual_requerido}' o no existe.")
                return False
                
        except Error as e:
            print(f"❌ Error al cambiar estado: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

