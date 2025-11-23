# model/model.py
import mysql.connector
from datetime import datetime
from mysql.connector import Error

class RentasModel:
    def __init__(self, host='localhost', user='root', password='', database='bd_integradora', port=3306):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
        }
        self.conexion = None
        self.current_user = None  # dict con info del usuario tras login
        self.conectar_bd()

    def conectar_bd(self):
        """Establece conexión con la base de datos MySQL"""
        try:
            self.conexion = mysql.connector.connect(**self.db_config)
            if self.conexion.is_connected():
                print("✅ Conexión a la base de datos establecida correctamente")
        except Error as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            self.conexion = None

    def obtener_cursor(self):
        """Devuelve un cursor dictionary, reintentando la conexión si es necesario"""
        try:
            if not self.conexion or not self.conexion.is_connected():
                self.conectar_bd()
            if self.conexion and self.conexion.is_connected():
                return self.conexion.cursor(dictionary=True)
            return None
        except Error:
            # Intentar reconectar una vez
            self.conectar_bd()
            if self.conexion and self.conexion.is_connected():
                return self.conexion.cursor(dictionary=True)
            return None

    # -------------------------
    # Autenticación / usuarios
    # -------------------------
    def validar_credenciales(self, usuario, password):
        """Valida credenciales contra la tabla usuarios (nota: passwords en dump están en texto plano)."""
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = "SELECT * FROM usuarios WHERE usuario = %s AND password = %s AND activo = 1 LIMIT 1"
            cursor.execute(query, (usuario, password))
            row = cursor.fetchone()
            if row:
                # Guardar usuario actual para mostrar en la vista
                self.current_user = row
                # Actualizar ultimo_login
                try:
                    upd = "UPDATE usuarios SET ultimo_login = %s WHERE id = %s"
                    cursor2 = self.obtener_cursor()
                    if cursor2:
                        cursor2.execute(upd, (datetime.now(), row['id']))
                        self.conexion.commit()
                        cursor2.close()
                except Exception:
                    pass
                return True
            return False
        except Error as e:
            print(f"Error validando credenciales: {e}")
            return False
        finally:
            cursor.close()

    def obtener_usuario_actual(self):
        """Devuelve un nombre legible del usuario actual (o 'Invitado')"""
        if self.current_user:
            return self.current_user.get('usuario') or self.current_user.get('nombre_completo') or "Usuario"
        # fallback: intentar obtener admin si existe
        cursor = self.obtener_cursor()
        if not cursor:
            return "Usuario"
        try:
            cursor.execute("SELECT usuario FROM usuarios WHERE activo = 1 LIMIT 1")
            row = cursor.fetchone()
            return row['usuario'] if row else "Usuario"
        finally:
            cursor.close()

    def cerrar_sesion(self):
        self.current_user = None

    # -------------------------
    # Eventos
    # -------------------------
    def obtener_eventos(self, limit=5):
        """Devuelve próximos eventos (fecha_evento >= ahora)"""
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            query = """
                SELECT id, titulo, descripcion, fecha_evento, tipo
                FROM eventos
                WHERE fecha_evento >= NOW()
                ORDER BY fecha_evento ASC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            eventos = []
            for r in rows:
                fecha = r['fecha_evento'].strftime("%Y-%m-%d %H:%M") if r['fecha_evento'] else ""
                eventos.append({
                    "id": r['id'],
                    "titulo": r['titulo'],
                    "descripcion": r['descripcion'],
                    "fecha_evento": fecha,
                    "tipo": r['tipo']
                })
            return eventos
        except Error as e:
            print(f"Error obteniendo eventos: {e}")
            return []
        finally:
            cursor.close()

    def obtener_eventos_por_fecha(self, año, mes, dia):
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            fecha = f"{int(año):04d}-{int(mes):02d}-{int(dia):02d}"
            query = """
                SELECT id, titulo, descripcion, hora_inicio, hora_fin
                FROM eventos
                WHERE DATE(fecha_evento) = %s
                ORDER BY fecha_evento
            """
            cursor.execute(query, (fecha,))
            rows = cursor.fetchall()
            eventos = []
            for r in rows:
                eventos.append({
                    "id": r.get('id'),
                    "titulo": r.get('titulo'),
                    "descripcion": r.get('descripcion'),
                    # hora_inicio/fin pueden venir como None
                    "hora_inicio": r.get('hora_inicio').strftime("%H:%M") if r.get('hora_inicio') else "",
                    "hora_fin": r.get('hora_fin').strftime("%H:%M") if r.get('hora_fin') else ""
                })
            return eventos
        except Error as e:
            print(f"Error obteniendo eventos por fecha: {e}")
            return []
        finally:
            cursor.close()

    def agregar_evento(self, titulo, descripcion, fecha_evento, tipo='entrega'):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = """
                INSERT INTO eventos (titulo, descripcion, fecha_evento, tipo, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (titulo, descripcion, fecha_evento, tipo, datetime.now()))
            self.conexion.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error agregando evento: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    # -------------------------
    # Reservaciones
    # -------------------------
    def obtener_reservaciones(self, limit=10):
        """Devuelve reservaciones (para la vista dashboard), mapeando:
           - 'articulo' <- observaciones (en Opción A guardamos el evento en observaciones)
           - 'cliente'  <- nombre cliente
           - 'estado'
           - 'fecha_entrega' <- fecha_entrega si existe, si no usa fecha_evento
        """
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            query = """
                SELECT r.id, r.cliente_id, c.nombre AS cliente, r.estado, r.fecha_evento, r.fecha_entrega, r.total, r.observaciones
                FROM reservaciones r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                ORDER BY r.fecha_reservacion DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            reservaciones = []
            for r in rows:
                fecha_entrega = r.get('fecha_entrega') or r.get('fecha_evento')
                fecha_str = fecha_entrega.strftime("%Y-%m-%d") if fecha_entrega else ""
                reservaciones.append({
                    "id": r.get('id'),
                    "articulo": r.get('observaciones') or "",  # usamos observaciones para guardar 'evento' según Opción A
                    "cliente": r.get('cliente') or "",
                    "estado": r.get('estado') or "",
                    "fecha_entrega": fecha_str,
                    "total": float(r.get('total')) if r.get('total') is not None else 0.0
                })
            return reservaciones
        except Error as e:
            print(f"Error obteniendo reservaciones: {e}")
            return []
        finally:
            cursor.close()

    def obtener_reservaciones_activas(self):
        cursor = self.obtener_cursor()
        if not cursor:
            return 0
        try:
            query = "SELECT COUNT(*) AS total FROM reservaciones WHERE estado IN ('confirmada','en_proceso')"
            cursor.execute(query)
            row = cursor.fetchone()
            return int(row['total']) if row and 'total' in row else 0
        except Error as e:
            print(f"Error contando reservaciones activas: {e}")
            return 0
        finally:
            cursor.close()

    def agregar_reservacion_completa(self, datos_orden):
        """
        Inserta una reservación en la tabla reservaciones.
        Se espera datos_orden con al menos:
          - cliente_id (int)
          - fecha_evento (date string 'YYYY-MM-DD' o datetime compatible)
          - estado (opcional)
          - observaciones (string)   <- aquí guardaremos el 'evento' según Opción A
          - total (decimal)          <- aquí guardaremos el costo
          - articulos (opcional)     <- lista de dicts con articulo_id, cantidad, precio_unitario
        """
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query_res = """
                INSERT INTO reservaciones (cliente_id, usuario_id, estado, fecha_reservacion, fecha_evento, fecha_entrega, total, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            usuario_id = self.current_user['id'] if self.current_user else 1  # fallback a 1
            estado = datos_orden.get('estado', 'pendiente')
            fecha_evento = datos_orden.get('fecha_evento')
            fecha_entrega = datos_orden.get('fecha_entrega', None)
            total = datos_orden.get('total', datos_orden.get('costo', None))
            observaciones = datos_orden.get('observaciones', datos_orden.get('evento', ''))

            cursor.execute(query_res, (
                datos_orden.get('cliente_id'),
                usuario_id,
                estado,
                datetime.now(),
                fecha_evento,
                fecha_entrega,
                total,
                observaciones
            ))
            reservacion_id = cursor.lastrowid

            # si hay items para detalle_reservacion, insertarlos
            articulos = datos_orden.get('articulos', [])
            if articulos and isinstance(articulos, list):
                query_det = """
                    INSERT INTO detalle_reservacion (reservacion_id, articulo_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                for item in articulos:
                    articulo_id = item.get('articulo_id')
                    cantidad = item.get('cantidad', 1)
                    precio_unitario = item.get('precio_unitario', 0.0)
                    subtotal = cantidad * precio_unitario
                    cursor.execute(query_det, (reservacion_id, articulo_id, cantidad, precio_unitario, subtotal))

            self.conexion.commit()
            return reservacion_id
        except Error as e:
            print(f"Error agregando reservación: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def obtener_ordenes_completas(self):
        """Devuelve órdenes con info legible para la vista de órdenes."""
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            query = """
                SELECT r.id, c.nombre AS cliente_nombre, r.fecha_evento, r.estado,
                       r.fecha_reservacion, r.observaciones, r.total
                FROM reservaciones r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                ORDER BY r.fecha_reservacion DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            ordenes = []
            for r in rows:
                fecha_evento = r.get('fecha_evento')
                fecha_str = fecha_evento.strftime("%Y-%m-%d") if fecha_evento else ""
                ordenes.append({
                    "id": r.get('id'),
                    "cliente_nombre": r.get('cliente_nombre'),
                    "fecha_evento": fecha_str,
                    "estado": r.get('estado'),
                    "fecha_reservacion": r.get('fecha_reservacion').strftime("%Y-%m-%d %H:%M") if r.get('fecha_reservacion') else "",
                    "notas": r.get('observaciones') or "",
                    "total": float(r.get('total')) if r.get('total') is not None else 0.0
                })
            return ordenes
        except Error as e:
            print(f"Error obteniendo órdenes completas: {e}")
            return []
        finally:
            cursor.close()

    def actualizar_estado_orden(self, orden_id, nuevo_estado):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = "UPDATE reservaciones SET estado = %s WHERE id = %s"
            cursor.execute(query, (nuevo_estado, orden_id))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error actualizando estado de orden: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def eliminar_orden(self, orden_id):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            # eliminar detalle_reservacion por cascade si existiera, pero en dump hay ON DELETE CASCADE en FK
            # Si no hubiera cascade, eliminar manualmente:
            try:
                qd = "DELETE FROM detalle_reservacion WHERE reservacion_id = %s"
                cursor.execute(qd, (orden_id,))
            except Exception:
                pass
            qr = "DELETE FROM reservaciones WHERE id = %s"
            cursor.execute(qr, (orden_id,))
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error eliminando orden: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    # -------------------------
    # Clientes
    # -------------------------
    def obtener_clientes_db(self):
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            cursor.execute("SELECT id, nombre, telefono, correo, direccion, fecha_registro FROM clientes WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo clientes: {e}")
            return []
        finally:
            cursor.close()

    def obtener_total_clientes(self):
        cursor = self.obtener_cursor()
        if not cursor:
            return 0
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM clientes WHERE activo = 1")
            row = cursor.fetchone()
            return int(row['total']) if row and 'total' in row else 0
        except Error as e:
            print(f"Error contando clientes: {e}")
            return 0
        finally:
            cursor.close()

    def agregar_cliente(self, nombre, telefono=None, correo=None, direccion=None):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = "INSERT INTO clientes (nombre, telefono, correo, direccion, fecha_registro, activo) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (nombre, telefono, correo, direccion, datetime.now(), 1))
            self.conexion.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error agregando cliente: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def actualizar_cliente(self, cliente_id, nombre, telefono=None, correo=None, direccion=None):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = "UPDATE clientes SET nombre = %s, telefono = %s, correo = %s, direccion = %s WHERE id = %s"
            cursor.execute(query, (nombre, telefono, correo, direccion, cliente_id))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error actualizando cliente: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def eliminar_cliente(self, cliente_id):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = "UPDATE clientes SET activo = 0 WHERE id = %s"
            cursor.execute(query, (cliente_id,))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error eliminando cliente: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def buscar_cliente_por_id(self, cliente_id):
        cursor = self.obtener_cursor()
        if not cursor:
            return None
        try:
            query = "SELECT * FROM clientes WHERE id = %s AND activo = 1"
            cursor.execute(query, (cliente_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error buscando cliente: {e}")
            return None
        finally:
            cursor.close()

    def cliente_existe(self, nombre, telefono=None, correo=None):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = """
                SELECT COUNT(*) AS total FROM clientes
                WHERE activo = 1 AND (nombre = %s OR telefono = %s OR correo = %s)
            """
            cursor.execute(query, (nombre, telefono, correo))
            row = cursor.fetchone()
            return int(row['total']) > 0 if row and 'total' in row else False
        except Error as e:
            print(f"Error verificando cliente existente: {e}")
            return False
        finally:
            cursor.close()

    # -------------------------
    # Artículos
    # -------------------------
    def obtener_articulos_db(self):
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            cursor.execute("SELECT id, nombre, precio_renta as precio FROM articulos WHERE estado = 'disponible' ORDER BY nombre")
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo artículos: {e}")
            return []
        finally:
            cursor.close()

    def obtener_articulo_por_id(self, articulo_id):
        cursor = self.obtener_cursor()
        if not cursor:
            return None
        try:
            cursor.execute("SELECT * FROM articulos WHERE id = %s", (articulo_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error obteniendo artículo: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_stock_articulo(self, articulo_id, cantidad):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = "UPDATE articulos SET stock = stock - %s WHERE id = %s"
            cursor.execute(query, (cantidad, articulo_id))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error actualizando stock: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    # -------------------------
    # Pagos
    # -------------------------
    def registrar_pago(self, reservacion_id, monto, metodo_pago, referencia=None):
        cursor = self.obtener_cursor()
        if not cursor:
            return False
        try:
            query = """
                INSERT INTO pagos (reservacion_id, monto, metodo_pago, referencia, fecha_pago)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (reservacion_id, monto, metodo_pago, referencia, datetime.now()))
            self.conexion.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error registrando pago: {e}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def obtener_pagos_por_reservacion(self, reservacion_id):
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            cursor.execute("SELECT * FROM pagos WHERE reservacion_id = %s ORDER BY fecha_pago DESC", (reservacion_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo pagos: {e}")
            return []
        finally:
            cursor.close()

    # -------------------------
    # Reportes y estadísticas
    # -------------------------
    def obtener_estadisticas_generales(self):
        cursor = self.obtener_cursor()
        if not cursor:
            return {}
        try:
            stats = {}
            
            # Total reservaciones este mes
            cursor.execute("""
                SELECT COUNT(*) as total 
                FROM reservaciones 
                WHERE MONTH(fecha_reservacion) = MONTH(CURRENT_DATE()) 
                AND YEAR(fecha_reservacion) = YEAR(CURRENT_DATE())
            """)
            stats['reservaciones_mes'] = cursor.fetchone()['total']
            
            # Ingresos este mes
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) as ingresos 
                FROM reservaciones 
                WHERE MONTH(fecha_reservacion) = MONTH(CURRENT_DATE()) 
                AND YEAR(fecha_reservacion) = YEAR(CURRENT_DATE())
                AND estado != 'cancelada'
            """)
            stats['ingresos_mes'] = float(cursor.fetchone()['ingresos'])
            
            # Clientes nuevos este mes
            cursor.execute("""
                SELECT COUNT(*) as nuevos 
                FROM clientes 
                WHERE MONTH(fecha_registro) = MONTH(CURRENT_DATE()) 
                AND YEAR(fecha_registro) = YEAR(CURRENT_DATE())
            """)
            stats['clientes_nuevos'] = cursor.fetchone()['nuevos']
            
            # Artículos más rentados
            cursor.execute("""
                SELECT a.nombre, COUNT(dr.id) as veces_rentado
                FROM detalle_reservacion dr
                JOIN articulos a ON dr.articulo_id = a.id
                GROUP BY a.id, a.nombre
                ORDER BY veces_rentado DESC
                LIMIT 5
            """)
            stats['articulos_populares'] = cursor.fetchall()
            
            return stats
        except Error as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
        finally:
            cursor.close()

    def obtener_reporte_ventas(self, fecha_inicio, fecha_fin):
        cursor = self.obtener_cursor()
        if not cursor:
            return []
        try:
            query = """
                SELECT r.id, c.nombre as cliente, r.fecha_reservacion, r.total, r.estado,
                       GROUP_CONCAT(a.nombre SEPARATOR ', ') as articulos
                FROM reservaciones r
                LEFT JOIN clientes c ON r.cliente_id = c.id
                LEFT JOIN detalle_reservacion dr ON r.id = dr.reservacion_id
                LEFT JOIN articulos a ON dr.articulo_id = a.id
                WHERE r.fecha_reservacion BETWEEN %s AND %s
                GROUP BY r.id
                ORDER BY r.fecha_reservacion DESC
            """
            cursor.execute(query, (fecha_inicio, fecha_fin))
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo reporte de ventas: {e}")
            return []
        finally:
            cursor.close()

    # -------------------------
    # Utilidades
    # -------------------------
    def obtener_usuarios_conectados(self):
        # Placeholder sencillo - en un sistema real esto sería más complejo
        return 1

    def backup_database(self, filepath):
        """Realiza un backup de la base de datos (concepto)"""
        # Esta es una implementación conceptual
        # En producción se usaría mysqldump o herramientas específicas
        try:
            print(f"Backup conceptual realizado en: {filepath}")
            return True
        except Exception as e:
            print(f"Error en backup: {e}")
            return False

    def __del__(self):
        if self.conexion and self.conexion.is_connected():
            try:
                self.conexion.close()
                print("🔌 Conexión a la base de datos cerrada")
            except Exception:
                pass