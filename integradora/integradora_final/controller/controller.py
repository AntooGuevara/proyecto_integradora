from model.model import RentasModel
from view.view import LoginView, RentasView

class RentasController:
    def __init__(self, root):
        self.root = root
        self.model = RentasModel()
        
        # Mostrar login primero
        self.login_view = LoginView(root, self)
        self.rentas_view = None
        
        # Cargar datos iniciales (pero no mostrar aún)
        self.model.cargar_datos_iniciales()
    
    def iniciar_sesion(self, usuario, password):
        """Maneja el proceso de inicio de sesión"""
        if self.model.validar_credenciales(usuario, password):
            self.login_view.mostrar_exito("Éxito", "Inicio de sesión exitoso")
            self.mostrar_panel_principal()
        else:
            self.login_view.mostrar_error("Error", "Credenciales incorrectas")
            self.login_view.limpiar_formulario()
    
    def mostrar_panel_principal(self):
        """Muestra el panel principal después del login exitoso"""
        # Ocultar login
        self.login_view.ocultar()
        
        # Crear y mostrar vista principal
        self.rentas_view = RentasView(self.root, self)
        self.actualizar_vista()
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        if self.rentas_view:
            self.rentas_view.ocultar()
        self.model.cerrar_sesion()
        self.login_view.mostrar()
        self.login_view.limpiar_formulario()
    
    def actualizar_vista(self):
        """Actualiza todos los elementos de la vista con los datos del modelo"""
        if self.rentas_view:
            eventos = self.model.obtener_eventos()
            reservaciones = self.model.obtener_reservaciones()
            total_activas = self.model.obtener_reservaciones_activas()
            total_clientes = self.model.obtener_total_clientes()
            usuarios_conectados = self.model.obtener_usuarios_conectados()
            
            self.rentas_view.actualizar_eventos(eventos)
            self.rentas_view.actualizar_reservaciones(reservaciones, total_activas)
            self.rentas_view.actualizar_clientes(total_clientes)
            self.rentas_view.actualizar_usuarios(usuarios_conectados)
    
    def get_usuario_actual(self):
        """Obtiene el usuario actual para mostrar en la vista"""
        return self.model.obtener_usuario_actual() or "Invitado"
    
    def ver_calendario(self):
        if self.rentas_view:
            self.rentas_view.mostrar_mensaje("Calendario", "Funcionalidad de calendario en desarrollo")
    
    def crear_nueva_orden(self):
        if self.rentas_view:
            self.rentas_view.mostrar_dialogo_nueva_orden()
    
    def agregar_reservacion(self, articulo, cliente, estado, fecha_entrega):
        self.model.agregar_reservacion(articulo, cliente, estado, fecha_entrega)
        self.actualizar_vista()
        if self.rentas_view:
            self.rentas_view.mostrar_mensaje("Éxito", "Reservación creada correctamente")