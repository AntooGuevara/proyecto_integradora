class RentasModel:
    def __init__(self):
        self.eventos = []
        self.reservaciones = []
        self.clientes = []
        self.usuarios_conectados = 0
        self.usuario_actual = None
        
        # Base de datos simulada de usuarios
        self.usuarios = {
            "admin": "admin123",
            "jerry": "jerry123", 
            "ejemplo@dlivrss.com": "password123"
        }
        
    def cargar_datos_iniciales(self):
        """Carga datos iniciales para la aplicación"""
        self.eventos = [
            "Reunión de coordinación - Lunes 10:00",
            "Entrega de equipo - Miércoles 14:30",
            "Mantenimiento preventivo - Viernes 09:00"
        ]
        
        self.reservaciones = [
            {"articulo": "Oficina 101", "cliente": "Juan Pérez", "estado": "Activa", "fecha_entrega": "2024-01-15"},
            {"articulo": "Sala Conferencias A", "cliente": "María García", "estado": "Pendiente", "fecha_entrega": "2024-01-20"}
        ]
        
        self.clientes = ["Juan Pérez", "María García", "Carlos López", "Ana Martínez"]
        self.usuarios_conectados = 10
    
    def validar_credenciales(self, usuario, password):
        """Valida las credenciales del usuario"""
        if usuario in self.usuarios and self.usuarios[usuario] == password:
            self.usuario_actual = usuario
            return True
        return False
    
    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual"""
        self.usuario_actual = None
    
    def obtener_usuario_actual(self):
        """Obtiene el usuario actualmente logueado"""
        return self.usuario_actual
    
    def obtener_eventos(self):
        return self.eventos
    
    def obtener_reservaciones(self):
        return self.reservaciones
    
    def obtener_clientes(self):
        return self.clientes
    
    def obtener_total_clientes(self):
        return len(self.clientes)
    
    def obtener_reservaciones_activas(self):
        return len([r for r in self.reservaciones if r["estado"] == "Activa"])
    
    def obtener_usuarios_conectados(self):
        return self.usuarios_conectados
    
    def agregar_reservacion(self, articulo, cliente, estado, fecha_entrega):
        nueva_reservacion = {
            "articulo": articulo,
            "cliente": cliente,
            "estado": estado,
            "fecha_entrega": fecha_entrega
        }
        self.reservaciones.append(nueva_reservacion)
        return nueva_reservacion