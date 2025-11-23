# controller/controller.py
from model.model import RentasModel
from view.view import LoginView, RentasView
from tkinter import messagebox

class RentasController:
    def __init__(self, root):
        self.root = root
        self.model = RentasModel()   # usa la conexión a bd que proveíste
        self.login_view = LoginView(root, self)
        self.rentas_view = None

    # --------------------------
    # Login / navegación
    # --------------------------
    def iniciar_sesion(self, usuario, password):
        if self.model.validar_credenciales(usuario, password):
            self.login_view.mostrar_exito("Éxito", "Inicio de sesión exitoso")
            self.mostrar_panel_principal()
        else:
            self.login_view.mostrar_error("Error", "Credenciales incorrectas")
            self.login_view.limpiar_formulario()

    def mostrar_panel_principal(self):
        # ocultar login
        self.login_view.ocultar()
        # crear vista principal
        self.rentas_view = RentasView(self.root, self)
        # actualizar datos en la vista
        self.actualizar_vista()

    def cerrar_sesion(self):
        if self.rentas_view:
            self.rentas_view.ocultar()
        self.model.cerrar_sesion()
        self.login_view.mostrar()
        self.login_view.limpiar_formulario()

    # --------------------------
    # Actualizar vista (dashboard)
    # --------------------------
# En controller/controller.py - modificar el método actualizar_vista
    def actualizar_vista(self):
        if not self.rentas_view:
            return
        
        # Verificar si la vista principal todavía existe
        try:
            # Test simple para verificar si el widget raíz todavía existe
            self.root.winfo_exists()
        except Exception:
            return
        
        try:
            eventos = self.model.obtener_eventos()
            reservaciones = self.model.obtener_reservaciones()
            total_activas = self.model.obtener_reservaciones_activas()
            total_clientes = self.model.obtener_total_clientes()
            usuarios_conectados = self.model.obtener_usuarios_conectados()

            # Verificar que los métodos de la vista todavía existen antes de llamarlos
            if (hasattr(self.rentas_view, 'actualizar_eventos') and 
                hasattr(self.rentas_view, 'card_eventos_desc') and 
                self.rentas_view.card_eventos_desc.winfo_exists()):
                
                eventos_str = [f"{e['titulo']} - {e['fecha_evento']}" for e in eventos]
                self.rentas_view.actualizar_eventos(eventos_str)

            if (hasattr(self.rentas_view, 'actualizar_reservaciones') and 
                hasattr(self.rentas_view, 'tree') and 
                self.rentas_view.tree.winfo_exists()):
                
                self.rentas_view.actualizar_reservaciones(reservaciones, total_activas)

            if (hasattr(self.rentas_view, 'actualizar_clientes') and 
                hasattr(self.rentas_view, 'lbl_total_clientes') and 
                self.rentas_view.lbl_total_clientes.winfo_exists()):
                
                self.rentas_view.actualizar_clientes(total_clientes)

            # Para la lista completa de clientes
            if (hasattr(self.rentas_view, 'actualizar_clientes_completos') and 
                hasattr(self.rentas_view, 'clientes_tree')):
                
                clientes = self.model.obtener_clientes_db()
                self.rentas_view.actualizar_clientes_completos(clientes)

        except Exception as e:
            print(f"Error actualizando vista: {e}")
            # No mostrar messagebox aquí para evitar problemas
    # --------------------------
    # Calendario / Eventos
    # --------------------------
    def ver_calendario(self):
        if self.rentas_view:
            self.rentas_view.mostrar_mensaje("Calendario", "Funcionalidad de calendario en desarrollo")

    def obtener_eventos_fecha(self, año, mes, dia):
        return self.model.obtener_eventos_por_fecha(año, mes, dia)

    def agregar_evento_calendario(self, titulo, descripcion, fecha_evento, tipo='entrega'):
        return self.model.agregar_evento(titulo, descripcion, fecha_evento, tipo)

    # --------------------------
    # ORDENES / RESERVACIONES
    # --------------------------
    def crear_nueva_orden(self):
        if self.rentas_view:
            self.rentas_view.mostrar_dialogo_nueva_orden()

    def agregar_reservacion(self, datos_orden):
        """Wrapper para agregar reservación. datos_orden debe cumplir con lo esperado en el model."""
        try:
            resultado = self.model.agregar_reservacion_completa(datos_orden)
            if resultado:
                # actualizar la vista
                self.actualizar_vista()
                if self.rentas_view:
                    self.rentas_view.mostrar_mensaje("Éxito", "Orden creada correctamente")
                return True
            else:
                if self.rentas_view:
                    self.rentas_view.mostrar_mensaje("Error", "Error al crear la orden")
                return False
        except Exception as e:
            if self.rentas_view:
                self.rentas_view.mostrar_mensaje("Error", f"Error al crear orden: {str(e)}")
            return False

    def obtener_ordenes(self):
        return self.model.obtener_ordenes_completas()

    def actualizar_estado_orden(self, orden_id, nuevo_estado):
        ok = self.model.actualizar_estado_orden(orden_id, nuevo_estado)
        if ok:
            self.actualizar_vista()
        return ok

    def eliminar_orden(self, orden_id):
        ok = self.model.eliminar_orden(orden_id)
        if ok:
            self.actualizar_vista()
        return ok

    # --------------------------
    # CLIENTES
    # --------------------------
    def actualizar_vista_clientes(self):
        if self.rentas_view and hasattr(self.rentas_view, 'clientes_tree'):
            clientes = self.model.obtener_clientes_db()
            if hasattr(self.rentas_view, 'actualizar_clientes_completos'):
                self.rentas_view.actualizar_clientes_completos(clientes)

    def agregar_cliente(self, nombre, telefono, correo, direccion=""):
        if not nombre or not nombre.strip():
            # Usar messagebox directamente en lugar de través de la vista
            messagebox.showerror("Error", "El nombre del cliente es obligatorio")
            return False

        if self.model.cliente_existe(nombre, telefono, correo):
            messagebox.showwarning("Advertencia", "El cliente ya existe en la base de datos")
            return False

        cliente_id = self.model.agregar_cliente(nombre, telefono, correo, direccion)
        if cliente_id:
            # Usar after para asegurar que la actualización sea segura
            self.root.after(100, self.actualizar_vista_segura)
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' agregado correctamente (ID: {cliente_id})")
            return True
        else:
            messagebox.showerror("Error", "Error al agregar el cliente")
            return False

    def actualizar_vista_segura(self):
        """Método seguro para actualizar la vista usando after()"""
        try:
            if (hasattr(self, 'rentas_view') and self.rentas_view and 
                hasattr(self.rentas_view, 'app_frame') and 
                self.rentas_view.app_frame.winfo_exists()):
                
                self.actualizar_vista()
        except Exception as e:
            print(f"Error en actualización segura: {e}")



    def actualizar_cliente(self, cliente_id, nombre, telefono, correo, direccion=""):
        if not nombre or not nombre.strip():
            if self.rentas_view:
                self.rentas_view.mostrar_mensaje("Error", "El nombre del cliente es obligatorio")
            return False

        ok = self.model.actualizar_cliente(cliente_id, nombre, telefono, correo, direccion)
        if ok:
            self.actualizar_vista()
            self.actualizar_vista_clientes()
            if self.rentas_view:
                self.rentas_view.mostrar_mensaje("Éxito", f"Cliente '{nombre}' actualizado correctamente")
            return True
        else:
            if self.rentas_view:
                self.rentas_view.mostrar_mensaje("Error", "No se pudo actualizar el cliente")
            return False

    def eliminar_cliente(self, cliente_id):
        cliente = self.model.buscar_cliente_por_id(cliente_id)
        nombre = cliente.get('nombre') if cliente else "Cliente"
        ok = self.model.eliminar_cliente(cliente_id)
        if ok:
            self.actualizar_vista()
            self.actualizar_vista_clientes()
            if self.rentas_view:
                self.rentas_view.mostrar_mensaje("Éxito", f"Cliente '{nombre}' eliminado correctamente")
            return True
        else:
            if self.rentas_view:
                self.rentas_view.mostrar_mensaje("Error", "No se pudo eliminar el cliente")
            return False

    # --------------------------
    # Complementos
    # --------------------------
    def get_usuario_actual(self):
        return self.model.obtener_usuario_actual()

    def obtener_clientes_para_combobox(self):
        clientes = self.model.obtener_clientes_db()
        return [(c['id'], c['nombre']) for c in clientes] if clientes else []

    def obtener_articulos_para_combobox(self):
        return self.model.obtener_articulos_db()
