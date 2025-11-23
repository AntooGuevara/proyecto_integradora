import os
import sys
import customtkinter as ctk
from PIL import Image
from tkinter import ttk, messagebox

# --- Helpers -----------------------------------------------------------------

def get_resource_path(relative_path: str) -> str:
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para ejecutables."""
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# --- Rutas de recursos ------------------------------------------------------
ICONS_DIR = os.path.join("assets", "icons")
ICON_HOME = get_resource_path(os.path.join(ICONS_DIR, "home.png"))
ICON_CALENDAR = get_resource_path(os.path.join(ICONS_DIR, "calendar.png"))
ICON_USERS = get_resource_path(os.path.join(ICONS_DIR, "users.png"))
LOGO_PATH = get_resource_path(os.path.join(ICONS_DIR, "logo.png"))


# --- View classes -----------------------------------------------------------
class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Apariencia
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Ventana
        self.root.title("DIVERSIONESJERRY - Login")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        # Contenedor principal
        self.main_frame = ctk.CTkFrame(master=self.root, fg_color="#ffffff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left (brand) / Right (form)
        self.left_frame = ctk.CTkFrame(master=self.main_frame, fg_color="#6b2fb8", width=400)
        self.left_frame.pack(side="left", fill="y", padx=(0, 20))
        self.left_frame.pack_propagate(False)

        self.right_frame = ctk.CTkFrame(master=self.main_frame, fg_color="#ffffff", width=500)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(False)

        self._build_left_side()
        self._build_login_form()

    def _build_left_side(self):
        # Logo (fallback a texto si no existe)
        try:
            if os.path.exists(LOGO_PATH):
                img = Image.open(LOGO_PATH)
                self.logo_login = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                logo_label = ctk.CTkLabel(master=self.left_frame, image=self.logo_login, text="", fg_color="#6b2fb8")
                logo_label.pack(pady=(80, 20))
            else:
                raise FileNotFoundError(LOGO_PATH)
        except Exception:
            brand_label = ctk.CTkLabel(master=self.left_frame, text="DIVERSIONESJERRY",
                                       font=ctk.CTkFont(size=32, weight="bold"), text_color="white")
            brand_label.pack(pady=(100, 20), padx=20)

        # Mensajes de bienvenida
        welcome_label = ctk.CTkLabel(master=self.left_frame, text="Bienvenido de Vuelta",
                                     font=ctk.CTkFont(size=18), text_color="white")
        welcome_label.pack(pady=(0, 100))

        decorative_text = ctk.CTkLabel(master=self.left_frame,
                                       text="Sistema de Gestión de Rentas\ny Reservaciones",
                                       font=ctk.CTkFont(size=14), text_color="white", justify="center")
        decorative_text.pack(expand=True)

    def _build_login_form(self):
        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#ffffff")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(master=form_frame, text="Iniciar Sesión",
                                   font=ctk.CTkFont(size=28, weight="bold"), text_color="#333333")
        title_label.pack(pady=(0, 10))

        desc_label = ctk.CTkLabel(master=form_frame,
                                  text="Ingrese sus credenciales para acceder al panel.",
                                  font=ctk.CTkFont(size=14), text_color="#666666")
        desc_label.pack(pady=(0, 30))

        # Usuario
        user_label = ctk.CTkLabel(master=form_frame, text="Usuario / Email",
                                  font=ctk.CTkFont(size=12, weight="bold"), text_color="#333333")
        user_label.pack(anchor="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(master=form_frame, width=350, height=45, placeholder_text="ejemplo@dlivrss.com", corner_radius=8)
        self.username_entry.pack(pady=(0, 20))

        # Contraseña
        pass_label = ctk.CTkLabel(master=form_frame, text="Contraseña",
                                  font=ctk.CTkFont(size=12, weight="bold"), text_color="#333333")
        pass_label.pack(anchor="w", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(master=form_frame, width=350, height=45, placeholder_text="••••••••",
                                           show="•", corner_radius=8)
        self.password_entry.pack(pady=(0, 30))

        login_btn = ctk.CTkButton(master=form_frame, text="Iniciar Sesión", command=self._on_login,
                                  width=350, height=45, corner_radius=8, fg_color="#6b2fb8",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        login_btn.pack(pady=(0, 20))

        # Bind Enter
        self.username_entry.bind("<Return>", lambda e: self._on_login())
        self.password_entry.bind("<Return>", lambda e: self._on_login())
        self.username_entry.focus()

    def _on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.mostrar_error("Error", "Por favor complete todos los campos.")
            return
        self.controller.iniciar_sesion(username, password)

    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)

    def mostrar_exito(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def limpiar_formulario(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus()

    def ocultar(self):
        self.main_frame.pack_forget()

    def mostrar(self):
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)


class RentasView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Ventana
        self.root.title("Panel de Control de Rentas - DIVERSIONESJERRY")
        self.root.geometry("1200x750")

        # Layout principal
        self.app_frame = ctk.CTkFrame(master=self.root)
        self.app_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(master=self.app_frame, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.configure(fg_color="#6b2fb8")

        # Content
        self.content = ctk.CTkFrame(master=self.app_frame, fg_color="#f7f7f7")
        self.content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Cargar íconos (fallback image transparente si falla)
        self.icon_home = self._load_icon(ICON_HOME, (24, 24))
        self.icon_calendar = self._load_icon(ICON_CALENDAR, (24, 24))
        self.icon_users = self._load_icon(ICON_USERS, (24, 24))

        # Construir UI
        self._build_sidebar()

        # Estado
        self.current_view = None
        self._show_dashboard()

    def _load_icon(self, path, size):
        try:
            if os.path.exists(path):
                img = Image.open(path)
            else:
                # Crear un ícono simple de color sólido como fallback
                img = Image.new('RGBA', size, (107, 47, 184, 255))
            icon = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            return icon
        except Exception:
            # Imagen transparente de fallback
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    def _build_sidebar(self):
        # Spacer
        top_spacer = ctk.CTkFrame(master=self.sidebar, fg_color="#6b2fb8")
        top_spacer.pack(pady=(20, 10))

        # Logo
        try:
            if os.path.exists(LOGO_PATH):
                logo_imagen = Image.open(LOGO_PATH)
                self.logo = ctk.CTkImage(light_image=logo_imagen, dark_image=logo_imagen, size=(120, 120))
                logo_label = ctk.CTkLabel(master=self.sidebar, image=self.logo, text="", fg_color="#6b2fb8")
                logo_label.pack(pady=(10, 20))
            else:
                raise FileNotFoundError(LOGO_PATH)
        except Exception:
            brand_label = ctk.CTkLabel(master=self.sidebar, text="DIVERSIONESJERRY",
                                       font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
            brand_label.pack(pady=(0, 20))

        # Botones del menú
        btn_opts = dict(master=self.sidebar, width=180, height=48, corner_radius=12, anchor="w")

        self.btn_inicio = ctk.CTkButton(image=self.icon_home, text="  Panel de Control",
                                        command=self._show_dashboard, fg_color="#8f49e6", text_color="white", **btn_opts)
        self.btn_inicio.pack(pady=(10, 6), padx=16)

        self.btn_ordenes = ctk.CTkButton(image=self.icon_calendar, text="  Órdenes (Reservas)",
                                         command=self._show_ordenes, fg_color="#6b2fb8", text_color="white", **btn_opts)
        self.btn_ordenes.pack(pady=6, padx=16)

        self.btn_clientes = ctk.CTkButton(image=self.icon_users, text="  Clientes",
                                          command=self._show_clientes, fg_color="#6b2fb8", text_color="white", **btn_opts)
        self.btn_clientes.pack(pady=6, padx=16)

        # Spacer expandible
        self.sidebar_spacer = ctk.CTkFrame(master=self.sidebar, fg_color="#6b2fb8")
        self.sidebar_spacer.pack(expand=True)

        # Botones inferiores
        self.btn_crear = ctk.CTkButton(master=self.sidebar, text="Crear Nueva Orden",
                                       command=self.controller.crear_nueva_orden, width=180, height=48, corner_radius=24)
        self.btn_crear.pack(pady=10, padx=16)

        self.btn_logout = ctk.CTkButton(master=self.sidebar, text="Cerrar Sesión",
                                        command=self.controller.cerrar_sesion, width=180, height=40, corner_radius=20,
                                        fg_color="#e74c3c", text_color="white")
        self.btn_logout.pack(pady=10, padx=16)

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _show_dashboard(self):
        self._clear_content()
        self.current_view = "dashboard"
        self._update_button_colors()
        self._build_topbar("Panel de Control de Rentas")
        self._build_dashboard_cards()
        self._build_orders_section()

    def _show_ordenes(self):
        self._clear_content()
        self.current_view = "ordenes"
        self._update_button_colors()
        self._build_topbar("Gestión de Órdenes y Reservaciones")
        self._build_ordenes_view()

    def _show_clientes(self):
        self._clear_content()
        self.current_view = "clientes"
        self._update_button_colors()
        self._build_topbar("Gestión de Clientes")
        self._build_clientes_view()

    def _update_button_colors(self):
        # reset
        self.btn_inicio.configure(fg_color="#6b2fb8")
        self.btn_ordenes.configure(fg_color="#6b2fb8")
        self.btn_clientes.configure(fg_color="#6b2fb8")
        # highlight
        if self.current_view == "dashboard":
            self.btn_inicio.configure(fg_color="#8f49e6")
        elif self.current_view == "ordenes":
            self.btn_ordenes.configure(fg_color="#8f49e6")
        elif self.current_view == "clientes":
            self.btn_clientes.configure(fg_color="#8f49e6")

    def _build_topbar(self, title_text):
        topbar = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7", height=80)
        topbar.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(master=topbar, text=title_text, font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(side="left", padx=(10, 0))

        user_box = ctk.CTkFrame(master=topbar, fg_color="#ffffff", corner_radius=10)
        user_box.pack(side="right", padx=10, pady=16)

        user_label = ctk.CTkLabel(master=user_box, text=f"Usuario: {self.controller.get_usuario_actual()}", text_color="#6b6b6b")
        user_label.pack(side="left", padx=(10, 8), pady=6)

        user_bubble = ctk.CTkFrame(master=user_box, width=32, height=32, corner_radius=16, fg_color="#9b6b4f")
        user_bubble.pack(side="right", padx=(0, 10), pady=6)

    def _build_dashboard_cards(self):
        cards_frame = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        cards_frame.pack(fill="x", pady=(0, 20))

        card_opts = dict(master=cards_frame, width=360, height=120, corner_radius=12, fg_color="#ffffff")

        self.card_eventos = ctk.CTkFrame(**card_opts)
        self.card_eventos.pack(side="left", padx=(0, 20))
        lbl_ev_t = ctk.CTkLabel(master=self.card_eventos, text="Próximos Eventos", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_ev_t.pack(anchor="nw", pady=(12, 4), padx=12)
        # description label stored so we can update safely
        self.card_eventos_desc = ctk.CTkLabel(master=self.card_eventos, text="Eventos programados para esta semana.", text_color="#7a7a7a")
        self.card_eventos_desc.pack(anchor="nw", padx=12)
        btn_cal = ctk.CTkButton(master=self.card_eventos, text="Ver Calendario", width=140, height=32, corner_radius=8, command=self.controller.ver_calendario)
        btn_cal.pack(anchor="sw", padx=12, pady=10)

        self.card_reservas = ctk.CTkFrame(**card_opts)
        self.card_reservas.pack(side="left", padx=(0, 20))
        lbl_res_t = ctk.CTkLabel(master=self.card_reservas, text="Reservaciones Activas", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_res_t.pack(anchor="nw", pady=(12, 4), padx=12)
        self.lbl_total_activas = ctk.CTkLabel(master=self.card_reservas, text="0", font=ctk.CTkFont(size=30, weight="bold"), text_color="#6b2fb8")
        self.lbl_total_activas.pack(anchor="nw", padx=12)
        lbl_res_desc = ctk.CTkLabel(master=self.card_reservas, text="Reservaciones activas este mes.", text_color="#7a7a7a")
        lbl_res_desc.pack(anchor="nw", padx=12)

        self.card_clientes = ctk.CTkFrame(**card_opts)
        self.card_clientes.pack(side="left")
        lbl_cli_t = ctk.CTkLabel(master=self.card_clientes, text="Clientes Registrados", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_cli_t.pack(anchor="nw", pady=(12, 4), padx=12)
        self.lbl_total_clientes = ctk.CTkLabel(master=self.card_clientes, text="0", font=ctk.CTkFont(size=30, weight="bold"), text_color="#6b2fb8")
        self.lbl_total_clientes.pack(anchor="nw", padx=12)
        lbl_cli_desc = ctk.CTkLabel(master=self.card_clientes, text="Total de clientes en BD.", text_color="#7a7a7a")
        lbl_cli_desc.pack(anchor="nw", padx=12)

    def _build_orders_section(self):
        orders_card = ctk.CTkFrame(master=self.content, fg_color="#ffffff", corner_radius=12)
        orders_card.pack(fill="both", expand=True)

        lbl_title = ctk.CTkLabel(master=orders_card, text="Órdenes Recientes", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(anchor="nw", padx=20, pady=(18, 4))

        # Table area
        table_frame = ctk.CTkFrame(master=orders_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=12)

        columns = ("articulo", "cliente", "estado", "fecha", "acciones")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        for c in columns:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.lbl_sin_datos = ctk.CTkLabel(master=table_frame, text="No hay reservaciones para mostrar.", text_color="#7a7a7a")
        self.lbl_sin_datos.place(relx=0.5, rely=0.5, anchor="center")

    def _build_ordenes_view(self):
        main_container = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        main_container.pack(fill="both", expand=True)

        title_section = ctk.CTkFrame(master=main_container, fg_color="#f7f7f7")
        title_section.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(master=title_section, text="Gestión de Órdenes y Reservaciones", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w")

        crear_orden_btn = ctk.CTkButton(master=title_section, text="Crear Nueva Orden", command=self.controller.crear_nueva_orden, width=180, height=40, corner_radius=20, fg_color="#6b2fb8", text_color="white")
        crear_orden_btn.pack(anchor="e", side="bottom")

        orders_card = ctk.CTkFrame(master=main_container, fg_color="#ffffff", corner_radius=12)
        orders_card.pack(fill="both", expand=True, pady=10)

        loading_label = ctk.CTkLabel(master=orders_card, text="Cargando datos de reservaciones...", text_color="#7a7a7a")
        loading_label.pack(anchor="w", padx=20, pady=(20, 10))

        table_frame = ctk.CTkFrame(master=orders_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ARTÍCULO PRINCIPAL", "CLIENTE", "ESTADO", "FECHA DE ENTREGA", "ACCIONES")
        self.ordenes_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.ordenes_tree.heading(col, text=col)
            self.ordenes_tree.column(col, width=200, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.ordenes_tree.yview)
        self.ordenes_tree.configure(yscrollcommand=scrollbar.set)
        self.ordenes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.ordenes_sin_datos = ctk.CTkLabel(master=table_frame, text="No hay reservaciones para mostrar.", text_color="#7a7a7a")
        self.ordenes_sin_datos.place(relx=0.5, rely=0.5, anchor="center")

        bottom_info = ctk.CTkLabel(master=main_container, text=f"Usuario: {self.controller.get_usuario_actual()}", text_color="#7a7a7a")
        bottom_info.pack(anchor="w", pady=10)

    def _build_clientes_view(self):
        main_container = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        main_container.pack(fill="both", expand=True)

        title_section = ctk.CTkFrame(master=main_container, fg_color="#f7f7f7")
        title_section.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(master=title_section, text="Gestión de Clientes", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", side="left")

        crear_cliente_btn = ctk.CTkButton(master=title_section, text="Agregar Cliente", command=self._mostrar_dialogo_nuevo_cliente, width=150, height=40, corner_radius=20, fg_color="#27ae60", text_color="white")
        crear_cliente_btn.pack(anchor="e", side="right", padx=(0, 10))

        brand_header = ctk.CTkFrame(master=main_container, fg_color="#6b2fb8", height=60)
        brand_header.pack(fill="x", pady=(0, 20))

        brand_label = ctk.CTkLabel(master=brand_header, text="DIVERSIONESJERRY", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        brand_label.pack(pady=18)

        table_card = ctk.CTkFrame(master=main_container, fg_color="#ffffff", corner_radius=12)
        table_card.pack(fill="both", expand=True, pady=10)

        table_title = ctk.CTkLabel(master=table_card, text="Tabla de Clientes", font=ctk.CTkFont(size=18, weight="bold"))
        table_title.pack(anchor="w", padx=20, pady=(20, 10))

        info_label = ctk.CTkLabel(master=table_card, text="Base de datos no disponible (Falta configuración).", text_color="#7a7a7a")
        info_label.pack(anchor="w", padx=20, pady=(0, 15))

        table_frame = ctk.CTkFrame(master=table_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("NOMBRE", "TELEFONO", "CORREO", "DIRECCIÓN", "ACCIONES")
        self.clientes_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        column_widths = {"NOMBRE": 200, "TELEFONO": 120, "CORREO": 200, "DIRECCIÓN": 200, "ACCIONES": 150}
        for col in columns:
            self.clientes_tree.heading(col, text=col)
            self.clientes_tree.column(col, width=column_widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        self.clientes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.clientes_sin_datos = ctk.CTkLabel(master=table_frame, text="No hay clientes para mostrar.", text_color="#7a7a7a")
        self.clientes_sin_datos.place(relx=0.5, rely=0.5, anchor="center")

        bottom_info = ctk.CTkLabel(master=main_container, text=f"ID de Usuario: {self.controller.get_usuario_actual()}", text_color="#7a7a7a")
        bottom_info.pack(anchor="w", pady=10)

        # Cargar clientes
        self.controller.actualizar_vista_clientes()

    def _mostrar_dialogo_nuevo_cliente(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Agregar Nuevo Cliente")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        titulo = ctk.CTkLabel(master=dialog, text="Agregar Nuevo Cliente", font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=20)

        form_frame = ctk.CTkFrame(master=dialog)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        campos = [("Nombre Completo", "nombre"), ("Teléfono", "telefono"), ("Correo Electrónico", "correo"), ("Dirección", "direccion")]
        self.cliente_entries = {}
        for i, (label, key) in enumerate(campos):
            lbl = ctk.CTkLabel(master=form_frame, text=label + ":", font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=i*2, column=0, sticky="w", padx=10, pady=(10, 5))
            ent = ctk.CTkEntry(master=form_frame, width=300, height=35)
            ent.grid(row=i*2+1, column=0, sticky="ew", padx=10, pady=(0, 10))
            self.cliente_entries[key] = ent

        btn_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        def guardar_cliente():
            nombre = self.cliente_entries['nombre'].get().strip()
            telefono = self.cliente_entries['telefono'].get().strip()
            correo = self.cliente_entries['correo'].get().strip()
            direccion = self.cliente_entries['direccion'].get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            # Cerrar el diálogo primero
            dialog.destroy()
            
            # Luego procesar en el controller
            self.controller.agregar_cliente(nombre, telefono, correo, direccion)

        def cancelar():
            dialog.destroy()

        btn_guardar = ctk.CTkButton(master=btn_frame, text="Guardar Cliente", command=guardar_cliente, width=120, height=40, fg_color="#27ae60")
        btn_guardar.pack(side="left", padx=10)
        btn_cancelar = ctk.CTkButton(master=btn_frame, text="Cancelar", command=cancelar, width=120, height=40, fg_color="#95a5a6")
        btn_cancelar.pack(side="left", padx=10)

    # ---------------- Métodos públicos que usa el controller -----------------
    def actualizar_eventos(self, eventos):
        """Actualiza la lista de eventos dentro de la tarjeta de eventos."""
        try:
            if not hasattr(self, 'card_eventos_desc') or not self.card_eventos_desc.winfo_exists():
                return
                
            texto = "Sin eventos programados."
            if eventos:
                texto = "\n".join(eventos[:5])
            self.card_eventos_desc.configure(text=texto)
        except Exception as e:
            print(f"Error actualizando eventos: {e}")

    def actualizar_reservaciones(self, reservaciones, total_activas):
        """Rellena la tabla de reservaciones del dashboard."""
        try:
            # Actualizar contador
            if hasattr(self, 'lbl_total_activas') and self.lbl_total_activas.winfo_exists():
                self.lbl_total_activas.configure(text=str(total_activas))

            # Limpiar tabla
            if hasattr(self, 'tree') and self.tree.winfo_exists():
                for row in self.tree.get_children():
                    self.tree.delete(row)

                if not reservaciones:
                    if hasattr(self, 'lbl_sin_datos') and self.lbl_sin_datos.winfo_exists():
                        self.lbl_sin_datos.place(relx=0.5, rely=0.5, anchor="center")
                else:
                    if hasattr(self, 'lbl_sin_datos') and self.lbl_sin_datos.winfo_exists():
                        self.lbl_sin_datos.place_forget()
                    for r in reservaciones:
                        self.tree.insert("", "end", values=(
                            r.get('articulo', ''),
                            r.get('cliente', ''),
                            r.get('estado', ''),
                            r.get('fecha_entrega', ''),
                            ""
                        ))
        except Exception as e:
            print(f"Error actualizando reservaciones: {e}")

    def actualizar_clientes(self, total_clientes):
        try:
            if hasattr(self, 'lbl_total_clientes') and self.lbl_total_clientes.winfo_exists():
                self.lbl_total_clientes.configure(text=str(total_clientes))
        except Exception as e:
            print(f"Error actualizando clientes: {e}")

    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def actualizar_usuarios(self, usuarios_conectados):
        # placeholder por ahora
        pass

    def actualizar_clientes_completos(self, clientes):
        """Actualización segura de la tabla de clientes"""
        try:
            if not hasattr(self, 'clientes_tree') or not self.clientes_tree.winfo_exists():
                return
                
            # Limpiar tabla
            for row in self.clientes_tree.get_children():
                self.clientes_tree.delete(row)
                
            if clientes:
                if hasattr(self, 'clientes_sin_datos') and self.clientes_sin_datos.winfo_exists():
                    self.clientes_sin_datos.place_forget()
                    
                for cliente in clientes:
                    self.clientes_tree.insert("", "end", values=(
                        cliente.get('nombre', ''),
                        cliente.get('telefono', ''),
                        cliente.get('correo', ''),
                        cliente.get('direccion', ''),
                        "Editar | Eliminar"
                    ))
            else:
                if hasattr(self, 'clientes_sin_datos') and self.clientes_sin_datos.winfo_exists():
                    self.clientes_sin_datos.place(relx=0.5, rely=0.5, anchor="center")
                    
        except Exception as e:
            print(f"Error actualizando clientes completos: {e}")

    def mostrar_dialogo_nueva_orden(self):
        self.mostrar_mensaje("Nueva Orden", "Funcionalidad para crear nueva orden en desarrollo")

    def ocultar(self):
        if hasattr(self, 'app_frame'):
            self.app_frame.pack_forget()

    def mostrar(self):
        if hasattr(self, 'app_frame'):
            self.app_frame.pack(fill="both", expand=True)