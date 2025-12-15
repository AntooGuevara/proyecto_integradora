import os
import sys
import customtkinter as ctk
from PIL import Image
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkinter import StringVar, Toplevel, Entry
from tkcalendar import DateEntry 
from datetime import datetime
import tkinter as tk


# mostrar_dialogo_nueva_orden

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
#show_ordenes
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
#actualizar_dashboard 

class RentasView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # ... (código existente)

        # Inicialización de diccionarios para diálogos (Añadir o asegurar que existan)
        self.campos_orden = {}
        self.cliente_entries = {}
        self.lbl_sin_datos_ordenes = None

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
#guardar_cliente
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
#RentasView
    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
#_build_ordenes_view 
    def _show_dashboard(self):
        self._clear_content()
        self.current_view = "dashboard"
        self._update_button_colors()
        self._build_topbar("Panel de Control de Rentas")
        self._build_dashboard_cards()
        self._build_orders_section()
        
        # Forzar actualización después de crear los widgets
        self.root.after(200, self.controller.actualizar_vista)
#_build_sidebar 
    def _show_ordenes(self):
        self._clear_content()
        self.current_view = "ordenes"
        self._update_button_colors()
        self._build_ordenes_view()
        self.controller.actualizar_vista_ordenes()
        
        # Forzar actualización
        print("=== CAMBIANDO A VISTA ÓRDENES ===")
        self.root.after(100, self.controller.actualizar_vista_ordenes)  # eso espera 100ms y lo actualiza

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
####
    def _build_dashboard_cards(self):
        cards_frame = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        cards_frame.pack(fill="x", pady=(0, 20))

        # Frame para título y botón de actualizar
        header_frame = ctk.CTkFrame(master=cards_frame, fg_color="#f7f7f7")
        header_frame.pack(fill="x", pady=(0, 10))
        
        title = ctk.CTkLabel(master=header_frame, text="Panel de Control", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(side="left", padx=20)
        
        # Botón de actualizar
        btn_actualizar = ctk.CTkButton(master=header_frame, text="↻ Actualizar", 
                                    command=self.controller.actualizar_vista,
                                    width=100, height=30, fg_color="#3498db")
        btn_actualizar.pack(side="right", padx=20)
        
        # Contenedor para las tarjetas
        cards_container = ctk.CTkFrame(master=cards_frame, fg_color="#f7f7f7")
        cards_container.pack(fill="x")
        
        card_opts = dict(width=360, height=120, corner_radius=12, fg_color="#ffffff")
        
        # Tarjeta de eventos
        self.card_eventos = ctk.CTkFrame(master=cards_container, **card_opts)
        self.card_eventos.pack(side="left", padx=(0, 20))
        
        lbl_ev_t = ctk.CTkLabel(master=self.card_eventos, text="Próximos Eventos", 
                            font=ctk.CTkFont(size=14, weight="bold"))
        lbl_ev_t.pack(anchor="nw", pady=(12, 4), padx=12)
        
        self.card_eventos_desc = ctk.CTkLabel(master=self.card_eventos, 
                                            text="Cargando eventos...", 
                                            text_color="#7a7a7a")
        self.card_eventos_desc.pack(anchor="nw", padx=12)
        
        btn_cal = ctk.CTkButton(master=self.card_eventos, text="Ver Calendario", 
                            width=140, height=32, corner_radius=8, 
                            command=self.controller.ver_calendario)
        btn_cal.pack(anchor="sw", padx=12, pady=10)

        # Tarjeta de reservaciones
        self.card_reservas = ctk.CTkFrame(master=cards_container, **card_opts)
        self.card_reservas.pack(side="left", padx=(0, 20))
        
        lbl_res_t = ctk.CTkLabel(master=self.card_reservas, text="Reservaciones Activas", 
                                font=ctk.CTkFont(size=14, weight="bold"))
        lbl_res_t.pack(anchor="nw", pady=(12, 4), padx=12)
        
        self.lbl_total_activas = ctk.CTkLabel(master=self.card_reservas, text="0", 
                                            font=ctk.CTkFont(size=30, weight="bold"), 
                                            text_color="#6b2fb8")
        self.lbl_total_activas.pack(anchor="nw", padx=12)
        
        lbl_res_desc = ctk.CTkLabel(master=self.card_reservas, 
                                text="Reservaciones activas este mes.", 
                                text_color="#7a7a7a")
        lbl_res_desc.pack(anchor="nw", padx=12)

        # Tarjeta de clientes
        self.card_clientes = ctk.CTkFrame(master=cards_container, **card_opts)
        self.card_clientes.pack(side="left")
        
        lbl_cli_t = ctk.CTkLabel(master=self.card_clientes, text="Clientes Registrados", 
                                font=ctk.CTkFont(size=14, weight="bold"))
        lbl_cli_t.pack(anchor="nw", pady=(12, 4), padx=12)
        
        self.lbl_total_clientes = ctk.CTkLabel(master=self.card_clientes, text="0", 
                                            font=ctk.CTkFont(size=30, weight="bold"), 
                                            text_color="#6b2fb8")
        self.lbl_total_clientes.pack(anchor="nw", padx=12)
        
        lbl_cli_desc = ctk.CTkLabel(master=self.card_clientes, 
                                text="Total de clientes en BD.", 
                                text_color="#7a7a7a")
        lbl_cli_desc.pack(anchor="nw", padx=12)


######
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

# view/view.py (Dentro de la clase RentasView)
#actualizar_ordenes_simples
    # ------------------------------------------------------------------
    # [REEMPLAZO COMPLETO] VISTA DE ÓRDENES (Ahora usa la estructura simple del Dashboard)
    # ------------------------------------------------------------------
    def _build_ordenes_view(self):
        main_container = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        main_container.pack(fill="both", expand=True)

        title_section = ctk.CTkFrame(master=main_container, fg_color="#f7f7f7")
        title_section.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(master=title_section, text="Gestión de Órdenes y Reservaciones", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", padx=20, pady=10, side="left")

        # Frame para botones
        btn_frame = ctk.CTkFrame(master=title_section, fg_color="#f7f7f7")
        btn_frame.pack(anchor="e", side="right", padx=20, pady=10)
        
        # Botón de actualizar
        actualizar_btn = ctk.CTkButton(
            master=btn_frame, 
            text="↻ Actualizar", 
            command=lambda: self.controller.actualizar_vista_ordenes(),
            width=120, 
            height=35,
            fg_color="#3498db",
            text_color="white"
        )
        actualizar_btn.pack(side="left", padx=(0, 10))
        
        # Botón de crear orden
        crear_orden_btn = ctk.CTkButton(
            master=btn_frame, 
            text="+ Crear Nueva Orden", 
            command=self.controller.crear_nueva_orden, 
            width=180, 
            height=35,
            fg_color="#6b2fb8", 
            text_color="white"
        )
        crear_orden_btn.pack(side="left")
        
        # Tabla de órdenes
        orders_card = ctk.CTkFrame(master=main_container, fg_color="#ffffff", corner_radius=12)
        orders_card.pack(fill="both", expand=True, padx=20, pady=10)

        # Configuración del estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                    font=("Arial", 11), 
                    rowheight=35, 
                    background="#ffffff", 
                    fieldbackground="#ffffff", 
                    foreground="#333333",
                    borderwidth=0)
        style.map("Treeview", 
                background=[('selected', '#8f49e6')],
                foreground=[('selected', 'white')])
        
        style.configure("Treeview.Heading", 
                    font=("Arial", 12, "bold"), 
                    background="#6b2fb8", 
                    foreground="white",
                    relief="flat",
                    borderwidth=0,
                    padding=(10, 5))
        style.map("Treeview.Heading",
                background=[('active', '#8f49e6')])

        # Frame para tabla y scrollbar
        table_frame = ctk.CTkFrame(master=orders_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Columnas - NOTA: La primera columna debe ser 'ID' para almacenar el ID real
        columns = ('ID', 'Artículo / Evento', 'Cliente', 'Estado', 'Fecha Entrega', 'Acciones')
        self.ordenes_tree = ttk.Treeview(
            master=table_frame, 
            columns=columns, 
            show='headings', 
            height=15,
            selectmode='browse'
        )
        
        # Configurar anchos y alineaciones de columnas
        config_columnas = {
            'ID': {'width': 60, 'anchor': 'center', 'stretch': False},
            'Artículo / Evento': {'width': 250, 'anchor': 'w', 'stretch': True},
            'Cliente': {'width': 150, 'anchor': 'w', 'stretch': False},
            'Estado': {'width': 120, 'anchor': 'center', 'stretch': False},
            'Fecha Entrega': {'width': 120, 'anchor': 'center', 'stretch': False},
            'Acciones': {'width': 100, 'anchor': 'center', 'stretch': False}
        }
        
        for col in columns:
            self.ordenes_tree.heading(col, text=col)
            if col in config_columnas:
                cfg = config_columnas[col]
                self.ordenes_tree.column(col, 
                                    width=cfg['width'], 
                                    anchor=cfg['anchor'],
                                    stretch=cfg.get('stretch', False))
            else:
                self.ordenes_tree.column(col, width=100, anchor='center')

        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.ordenes_tree.yview)
        self.ordenes_tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Scrollbar horizontal (opcional, si los datos son muy anchos)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.ordenes_tree.xview)
        self.ordenes_tree.configure(xscrollcommand=scrollbar_x.set)
        
        # Organizar en grid para mejor control
        self.ordenes_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # Configurar el grid para que se expanda
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Etiqueta de "No hay datos"
        self.lbl_sin_datos_ordenes = ctk.CTkLabel(master=table_frame, 
                                                text="Cargando reservaciones...", 
                                                text_color="#7a7a7a",
                                                font=ctk.CTkFont(size=12))
        self.lbl_sin_datos_ordenes.place(relx=0.5, rely=0.5, anchor="center")
#_mostrar_menu_contextual_clientes
#####_show_ordenes
    def _build_clientes_view(self):
        main_container = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        main_container.pack(fill="both", expand=True)

        title_section = ctk.CTkFrame(master=main_container, fg_color="#f7f7f7")
        title_section.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(master=title_section, text="Gestión de Clientes", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", side="left")

        crear_cliente_btn = ctk.CTkButton(master=title_section, text="Agregar Cliente", 
                                        command=self._mostrar_dialogo_nuevo_cliente, 
                                        width=150, height=40, corner_radius=20, 
                                        fg_color="#27ae60", text_color="white")
        crear_cliente_btn.pack(anchor="e", side="right", padx=(0, 10))

        brand_header = ctk.CTkFrame(master=main_container, fg_color="#6b2fb8", height=60)
        brand_header.pack(fill="x", pady=(0, 20))

        brand_label = ctk.CTkLabel(master=brand_header, text="DIVERSIONESJERRY", 
                                font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        brand_label.pack(pady=18)

        table_card = ctk.CTkFrame(master=main_container, fg_color="#ffffff", corner_radius=12)
        table_card.pack(fill="both", expand=True, pady=10)

        table_title = ctk.CTkLabel(master=table_card, text="Tabla de Clientes", 
                                font=ctk.CTkFont(size=18, weight="bold"))
        table_title.pack(anchor="w", padx=20, pady=(20, 10))

        # Cambiar este mensaje a uno más útil
        info_label = ctk.CTkLabel(master=table_card, 
                                text="Haga clic derecho en un cliente para ver opciones.", 
                                text_color="#7a7a7a")
        info_label.pack(anchor="w", padx=20, pady=(0, 15))

        table_frame = ctk.CTkFrame(master=table_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Configurar estilo del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 11), rowheight=35,
                    background="#ffffff", fieldbackground="#ffffff", 
                    foreground="#333333")
        style.map("Treeview", background=[('selected', '#8f49e6')])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                    background="#6b2fb8", foreground="white")

        columns = ("NOMBRE", "TELEFONO", "CORREO", "DIRECCIÓN", "ID_OCULTO")
        self.clientes_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # Ocultar la columna ID_OCULTO
        self.clientes_tree.heading("NOMBRE", text="NOMBRE")
        self.clientes_tree.heading("TELEFONO", text="TELEFONO")
        self.clientes_tree.heading("CORREO", text="CORREO")
        self.clientes_tree.heading("DIRECCIÓN", text="DIRECCIÓN")
        self.clientes_tree.heading("ID_OCULTO", text="")
        
        # Configurar anchos
        self.clientes_tree.column("NOMBRE", width=200, anchor="w")
        self.clientes_tree.column("TELEFONO", width=120, anchor="center")
        self.clientes_tree.column("CORREO", width=200, anchor="w")
        self.clientes_tree.column("DIRECCIÓN", width=200, anchor="w")
        self.clientes_tree.column("ID_OCULTO", width=0, stretch=False)  # Ocultar columna

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        self.clientes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.clientes_sin_datos = ctk.CTkLabel(master=table_frame, 
                                            text="No hay clientes para mostrar.", 
                                            text_color="#7a7a7a")
        self.clientes_sin_datos.place(relx=0.5, rely=0.5, anchor="center")

        bottom_info = ctk.CTkLabel(master=main_container, 
                                text=f"ID de Usuario: {self.controller.get_usuario_actual()}", 
                                text_color="#7a7a7a")
        bottom_info.pack(anchor="w", pady=10)

        # Crear menú contextual
        self.menu_contextual_clientes = tk.Menu(self.root, tearoff=0)
        self.menu_contextual_clientes.add_command(label="📝 Editar Cliente", 
                                                command=self._editar_cliente_desde_menu)
        self.menu_contextual_clientes.add_command(label="🗑️ Eliminar Cliente", 
                                                command=self._eliminar_cliente_desde_menu)
        self.menu_contextual_clientes.add_separator()
        self.menu_contextual_clientes.add_command(label="📋 Ver Detalles", 
                                                command=self._ver_detalles_cliente)
#_mostrar_dialogo_nuevo_cliente
        # Vincular eventos
        self.clientes_tree.bind("<Button-3>", self._mostrar_menu_contextual_clientes)  # Clic derecho
        self.clientes_tree.bind("<Double-1>", self._editar_cliente_doble_clic)  # Doble clic

        # Cargar clientes
        self.controller.actualizar_vista_clientes()

    def _mostrar_dialogo_nuevo_cliente(self):
        """Muestra diálogo para agregar un nuevo cliente - VERSIÓN CORREGIDA CON BOTONES"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Agregar Nuevo Cliente")
        dialog.geometry("500x550")  # Aumenté la altura para que quepan los botones
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # Título principal
        titulo = ctk.CTkLabel(
            master=dialog, 
            text="Agregar Nuevo Cliente", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=20)

        # Frame principal para el formulario
        main_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        main_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Frame para los campos del formulario
        form_frame = ctk.CTkFrame(master=main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Diccionario para almacenar las entradas
        self.cliente_entries = {}

        # Campos del formulario
        campos = [
            ("Nombre Completo *", "nombre", "Ej: Juan Pérez"),
            ("Teléfono", "telefono", "Ej: 1234567890"),
            ("Correo Electrónico", "correo", "Ej: cliente@email.com"),
            ("Dirección", "direccion", "Ej: Calle Principal #123")
        ]

        for i, (label, key, placeholder) in enumerate(campos):
            # Frame para cada campo
            field_frame = ctk.CTkFrame(master=form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)

            # Etiqueta
            lbl = ctk.CTkLabel(
                master=field_frame, 
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#333333"
            )
            lbl.pack(anchor="w", padx=5, pady=(0, 5))

            # Campo de entrada
            ent = ctk.CTkEntry(
                master=field_frame, 
                width=400, 
                height=40,
                placeholder_text=placeholder,
                corner_radius=8,
                font=ctk.CTkFont(size=12)
            )
            
            if key == "telefono":
                # Validar solo números para teléfono
                ent.bind('<KeyRelease>', lambda e: self._validar_telefono(e.widget))
            
            ent.pack(fill="x", padx=5)
            
            # Almacenar referencia
            self.cliente_entries[key] = ent

        # Frame para los botones (¡IMPORTANTE: SEPARADO!)
        button_frame = ctk.CTkFrame(master=main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")

        def guardar_cliente():
            """Recupera datos y guarda el cliente."""
            try:
                nombre = self.cliente_entries['nombre'].get().strip()
                telefono = self.cliente_entries['telefono'].get().strip()
                correo = self.cliente_entries['correo'].get().strip()
                direccion = self.cliente_entries['direccion'].get().strip()

                if not nombre:
                    messagebox.showerror("Error", "El nombre es obligatorio")
                    self.cliente_entries['nombre'].focus()
                    return

                # Validar formato de correo (opcional)
                if correo and "@" not in correo:
                    if not messagebox.askyesno("Advertencia", 
                        "El formato del correo parece incorrecto. ¿Desea continuar?"):
                        self.cliente_entries['correo'].focus()
                        return

                # Cerrar diálogo primero
                dialog.destroy()
                
                # Luego procesar en el controller
                self.controller.agregar_cliente(nombre, telefono, correo, direccion)

            except KeyError as e:
                messagebox.showerror("Error", f"Falta el campo: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")

        def cancelar():
            dialog.destroy()

        # Botón CANCELAR (Izquierda)
        btn_cancelar = ctk.CTkButton(
            master=button_frame,
            text="Cancelar",
            command=cancelar,
            width=120,
            height=45,
            corner_radius=10,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_cancelar.pack(side="left", padx=(0, 10))

        # Botón GUARDAR (Derecha)
        btn_guardar = ctk.CTkButton(
            master=button_frame,
            text="Guardar Cliente",
            command=guardar_cliente,
            width=140,
            height=45,
            corner_radius=10,
            fg_color="#27ae60",
            hover_color="#219653",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_guardar.pack(side="right", padx=(10, 0))

        # Asegurar que los botones estén centrados
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=1)

        # Espaciador para separar los botones
        spacer = ctk.CTkLabel(master=button_frame, text="", width=50)
        spacer.pack(side="left", expand=True)

        # Enfocar en el primer campo
        self.cliente_entries['nombre'].focus()

        # Manejar tecla ESC para cancelar
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        
        # Manejar tecla Enter para guardar
        dialog.bind('<Return>', lambda e: guardar_cliente())

        # Centrar la ventana en la pantalla
        dialog.update_idletasks()
        ancho = dialog.winfo_width()
        alto = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (ancho // 2)
        y = (dialog.winfo_screenheight() // 2) - (alto // 2)
        dialog.geometry(f'{ancho}x{alto}+{x}+{y}')

        # Forzar a que se muestren todos los widgets
        dialog.update()

    def _validar_telefono(self, entry_widget):
        """Valida que solo se ingresen números en el teléfono."""
        texto = entry_widget.get()
        # Remover caracteres no numéricos
        solo_numeros = ''.join(filter(str.isdigit, texto))
        if texto != solo_numeros:
            # Actualizar texto sin caracteres no numéricos
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, solo_numeros)

    def guardar_cliente(self, dialog: ctk.CTkToplevel):
        """Recupera los datos del diálogo de Registro de Cliente."""
        try:
            # CORRECCIÓN: Solo usar las claves que realmente existen
            nombre = self.cliente_entries["nombre"].get().strip()
            telefono = self.cliente_entries["telefono"].get().strip()
            correo = self.cliente_entries["correo"].get().strip()
            direccion = self.cliente_entries["direccion"].get().strip()

            # La clave "apellidos" no existe en el diccionario actual
            # Si necesitas apellidos, debes agregarlo a los campos
            #_build_clientes_view
        except KeyError as e:
            messagebox.showerror("Error de Formulario", f"Falta el campo: {e}")
            return
        
        if not nombre:
            messagebox.showerror("Validación", "El nombre del cliente es obligatorio.")
            return

        id_cliente = self.controller.agregar_cliente(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            direccion=direccion
        )
        
        if id_cliente:
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' guardado con ID: {id_cliente}")
            dialog.destroy()
            if self.current_view == "clientes":
                self.controller.actualizar_vista_clientes()
        else:
            messagebox.showerror("Error de BD", "No se pudo guardar el cliente.")

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

            # Verificar que el treeview existe
            if not hasattr(self, 'tree') or not self.tree.winfo_exists():
                print("DEBUG: Treeview no disponible para actualizar")
                return
                
            # Limpiar tabla
            for row in self.tree.get_children():
                 self.tree.delete(row)
#_build_dashboard_cards
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
                        "Ver"  # Acción
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

    def actualizar_ordenes_simples(self, reservaciones):
        """Versión simplificada para depuración."""
        print(f"DEBUG: actualizar_ordenes_simples con {len(reservaciones)} reservaciones")
        
        # Limpiar tabla
        for item in self.ordenes_tree.get_children():
            self.ordenes_tree.delete(item)
        
        if not reservaciones:
            print("DEBUG: No hay datos")
            return
        
        # Mostrar primeros datos para depuración
        for i, r in enumerate(reservaciones[:5]):  # Solo 5 para depurar
            print(f"DEBUG: Reservación {i+1}: {r}")
            
            valores = (
                str(r.get('id', i+1)),
                str(r.get('articulo', 'N/A'))[:30],
                str(r.get('cliente', 'N/A')),
                str(r.get('estado', 'N/A')).replace('_', ' ').title(),
                str(r.get('fecha_entrega', 'N/A')),
                "Ver"
            )
            
            print(f"DEBUG: Valores a insertar: {valores}")
            self.ordenes_tree.insert("", "end", values=valores)
        
        print("DEBUG: Tabla actualizada")

    def _aplicar_formato_estado(self, item_id, estado):
        """Aplica formato de color según el estado de la orden."""
        try:
            colores_estado = {
                'pendiente': ('#f39c12', '#000000'),  # Naranja
                'confirmada': ('#3498db', '#ffffff'),  # Azul
                'en_proceso': ('#2ecc71', '#ffffff'),  # Verde
                'completada': ('#27ae60', '#ffffff'),  # Verde oscuro
                'cancelada': ('#e74c3c', '#ffffff')   # Rojo
            }
            
            if estado in colores_estado:
                color_fondo, color_texto = colores_estado[estado]
                self.ordenes_tree.tag_configure(estado, background=color_fondo, foreground=color_texto)
                self.ordenes_tree.item(item_id, tags=(estado,))
                
        except Exception as e:
            print(f"Error aplicando formato de estado: {e}")
#actualizar_ordenes_simples
    def _ajustar_ancho_columnas(self):
        """Ajusta automáticamente el ancho de las columnas según el contenido."""
        try:
            for col in self.ordenes_tree['columns']:
                # Obtener el ancho máximo del contenido
                max_width = 0
                for item in self.ordenes_tree.get_children():
                    valor = self.ordenes_tree.set(item, col)
                    if valor:
                        # Estimar ancho basado en longitud del texto
                        ancho_estimado = len(str(valor)) * 8
                        max_width = max(max_width, ancho_estimado)
                
                # Establecer un ancho mínimo y máximo
                ancho_final = max(50, min(max_width + 20, 300))
                self.ordenes_tree.column(col, width=ancho_final)
                
        except Exception as e:
            print(f"Error ajustando ancho de columnas: {e}")
####
#_mostrar_dialogo_nuevo_cliente
    def actualizar_clientes_completos(self, clientes):
        """Actualización segura de la tabla de clientes con ID oculto."""
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
                    # Insertar con ID en columna oculta
                    self.clientes_tree.insert("", "end", values=(
                        cliente.get('nombre', ''),
                        cliente.get('telefono', ''),
                        cliente.get('correo', ''),
                        cliente.get('direccion', ''),
                        cliente.get('id', '')  # ID en columna oculta
                    ))
            else:
                if hasattr(self, 'clientes_sin_datos') and self.clientes_sin_datos.winfo_exists():
                    self.clientes_sin_datos.place(relx=0.5, rely=0.5, anchor="center")
                    
        except Exception as e:
            print(f"Error actualizando clientes completos: {e}")

    def mostrar_dialogo_nueva_orden(self):
        # 1. Configuración Básica del Diálogo
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Crear Nueva Orden")
        dialog.geometry("450x400")  # Aumenté el tamaño para más campos
        dialog.grab_set()
        
        # Título
        titulo_dialog = ctk.CTkLabel(master=dialog, text="Crear Nueva Orden", 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        titulo_dialog.pack(pady=(15, 10))

        # 2. Obtener y Preparar Datos
        cliente_map = {item['nombre']: item['id'] for item in self.controller.obtener_lista_clientes()}
        articulo_map = {item['nombre']: item['id'] for item in self.controller.obtener_lista_articulos()}

        lista_clientes = list(cliente_map.keys()) or ["(No hay clientes)"]
        lista_articulos = list(articulo_map.keys()) or ["(No hay artículos)"]
        
        # 3. Frame para organizar los campos
        form_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        form_frame.pack(pady=5, padx=20, fill="x", expand=True)

        form_frame.grid_columnconfigure(0, weight=1) 
        form_frame.grid_columnconfigure(1, weight=1)
        
        fila = 0

        # 4. Campo ARTÍCULO
        lbl_articulo = ctk.CTkLabel(master=form_frame, text="Artículo:", text_color="#555555")
        lbl_articulo.grid(row=fila, column=0, sticky="e", padx=(6, 15), pady=8) 
        
        combo_articulo = ctk.CTkComboBox(
            master=form_frame, 
            values=lista_articulos, 
            state="readonly" if "(No hay artículos)" not in lista_articulos else "disabled",
            width=200
        )
        combo_articulo.grid(row=fila, column=1, padx=(5, 20), pady=8, sticky="w")
        fila += 1
        
        # 5. Campo CLIENTES
        lbl_cliente = ctk.CTkLabel(master=form_frame, text="Cliente:", text_color="#555555")
        lbl_cliente.grid(row=fila, column=0, sticky="e", padx=(6, 15), pady=8) 
        
        combo_cliente = ctk.CTkComboBox(
            master=form_frame, 
            values=lista_clientes, 
            state="readonly" if "(No hay clientes)" not in lista_clientes else "disabled",
            width=200
        )
        combo_cliente.grid(row=fila, column=1, padx=(5, 20), pady=8, sticky="w")
        fila += 1
        #guardar_orden
        # Botón para registrar nuevo cliente
        btn_registro = ctk.CTkButton(
            master=form_frame,
            text="Registrar nuevo cliente...",
            command=self.mostrar_dialogo_registro_cliente, 
            fg_color="transparent", 
            hover_color="#f0f0f0",
            text_color="#007bff",
            font=ctk.CTkFont(size=11, underline=True),
            width=260,
            anchor="w"
        )
        btn_registro.grid(row=fila, column=1, padx=(5, 20), pady=(0, 8), sticky="w")
        fila += 1 
        
        # 6. Campo ESTADO
        estados = ["Programado", "En Curso", "Entregado", "Cancelado"]
        var_estado = StringVar(value=estados[0])
        
        lbl_estado = ctk.CTkLabel(master=form_frame, text="Estado:", text_color="#555555")
        lbl_estado.grid(row=fila, column=0, sticky="e", padx=(6, 15), pady=8) 
        
        option_estado = ctk.CTkOptionMenu(
            master=form_frame, 
            values=estados, 
            variable=var_estado,
            width=200
        )
        option_estado.grid(row=fila, column=1, padx=(5, 20), pady=8, sticky="w")
        fila += 1
        
        # 7. Campo FECHA DE ENTREGA
        lbl_fecha_entrega = ctk.CTkLabel(master=form_frame, text="Fecha de Entrega:", text_color="#555555")
        lbl_fecha_entrega.grid(row=fila, column=0, sticky="e", padx=(6, 15), pady=8) 
        
        date_entrega = DateEntry(
            master=form_frame, 
            width=20, 
            background='darkblue', 
            foreground='white', 
            borderwidth=2, 
            date_pattern='dd/MM/yy'
        )
        date_entrega.grid(row=fila, column=1, padx=(5, 20), pady=8, sticky="w")
        fila += 1
        
        # 8. Campo FECHA DE DEVOLUCIÓN (CORRECCIÓN: variable diferente)
        lbl_fecha_devolucion = ctk.CTkLabel(master=form_frame, text="Fecha de Devolución:", text_color="#555555")
        lbl_fecha_devolucion.grid(row=fila, column=0, sticky="e", padx=(6, 15), pady=8) 
        
        # CORRECCIÓN: Usa una variable diferente para la fecha de devolución
        date_devolucion = DateEntry(
            master=form_frame, 
            width=20, 
            background='darkblue', 
            foreground='white', 
            borderwidth=2, 
            date_pattern='dd/MM/yy'
        )
        date_devolucion.grid(row=fila, column=1, padx=(5, 20), pady=8, sticky="w")
        fila += 1
        
        # 9. Frame de Botones
        button_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        button_frame.pack(pady=(15, 20), padx=20, fill="x") 

        button_frame.grid_columnconfigure(0, weight=1) 
        button_frame.grid_columnconfigure(1, weight=1)
        
        btn_cancelar = ctk.CTkButton(
            master=button_frame, 
            text="Cancelar", 
            command=dialog.destroy, 
            fg_color="#a0a0a0", 
            hover_color="#888888", 
            width=100
        )
        btn_cancelar.grid(row=0, column=0, padx=10, sticky="e")
#mostrar_dialogo_registro_cliente
        btn_guardar = ctk.CTkButton(
            master=button_frame, 
            text="Guardar", 
            command=lambda: self.guardar_orden(dialog), 
            fg_color="#5DECEE", 
            hover_color="#1e6c7e", 
            width=100
        )
        btn_guardar.grid(row=0, column=1, padx=10, sticky="w")

        # CORRECCIÓN: Guardar referencias como atributos (incluyendo fecha de devolución)
        self.campos_orden = {
            "articulo": combo_articulo,
            "clientes": combo_cliente,
            "estado": var_estado,
            "fecha de entrega": date_entrega,
            "fecha de devolución": date_devolucion  # ← ¡IMPORTANTE! Agregar este campo
        }
        #guardar_orden
        # Guardar mapeos
        dialog.cliente_map = cliente_map
        dialog.articulo_map = articulo_map
        dialog.campos_orden = {
                "articulo": combo_articulo,
                "clientes": combo_cliente,
                "estado": var_estado,
                "fecha de entrega": date_entrega,
                "fecha de devolución": date_devolucion
            }
######
    def mostrar_dialogo_registro_cliente(self):
        """Crea y muestra la ventana para Registrar Cliente, según la estructura de la BD."""
        
        # Usar self.root en lugar de 'root' global
        dialog = ctk.CTkToplevel(self.root, fg_color="#ffffff") 
        dialog.title("Registrar Cliente")
        dialog.geometry("500x500") 
        dialog.grab_set()

        titulo_dialog = ctk.CTkLabel(master=dialog, text="Registro de Cliente Nuevo", 
                                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#333333")
        titulo_dialog.pack(pady=(16, 10))

        form_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        form_frame.pack(pady=5, padx=20, fill="x")
        
        # Los campos que se usan en guardar_cliente
        campos = [("Nombre", "nombre"), ("Teléfono", "telefono"), ("Correo", "correo"), ("Dirección", "direccion")]
        #guardar_cliente
        form_frame.grid_columnconfigure(0, weight=1) 
        form_frame.grid_columnconfigure(1, weight=1)
        
        self.cliente_entries = {} # Reinicia el diccionario para este diálogo

        for i, (l, key) in enumerate(campos):
            
            lbl = ctk.CTkLabel(master=form_frame, text=l+":", text_color="#555555")
            lbl.grid(row=i, column=0, sticky="e", padx=(6, 15), pady=8) 
            
            placeholder_text = f"Ingresa el {l.lower()}"
            ent = ctk.CTkEntry(master=form_frame, width=200, placeholder_text=placeholder_text)
            ent.grid(row=i, column=1, padx=(5, 20), pady=8, sticky="w")
            
            self.cliente_entries[key] = ent # <--- Almacena el Entry con la key correcta

        # FRAME DE BOTONES
        button_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        button_frame.pack(pady=(15, 20), padx=20, fill="x") 

        button_frame.grid_columnconfigure(0, weight=1) 
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Botones
        btn_cancelar = ctk.CTkButton(master=button_frame, text="Cancelar", command=dialog.destroy, 
                                    fg_color="#a0a0a0", hover_color="#888888", text_color="#000000", width=100)
        btn_cancelar.grid(row=0, column=0, padx=10, sticky="e")

        # Configura el comando para guardar
        btn_registrar = ctk.CTkButton(master=button_frame, text="Registrar", 
                                    command=lambda: self.guardar_cliente(dialog), # <--- ¡CORRECCIÓN!
                                    fg_color="#5DECEE", hover_color="#1e6c7e", width=100,text_color="#000")
        btn_registrar.grid(row=0, column=1, padx=10, sticky="w")
        
    def guardar_cliente(self, dialog: ctk.CTkToplevel):
        """
        Recupera los datos del diálogo de Registro de Cliente y los guarda 
        usando el controlador (self.controller.agregar_cliente).
        """
        
        # Las claves 'nombre', 'telefono', 'correo', 'direccion' coinciden
        # con las entradas guardadas en self.cliente_entries
        try:
            nombre = self.cliente_entries["nombre"].get().strip()
            apellidos = self.cliente_entries["apellidos"].get().strip()
            telefono = self.cliente_entries["telefono"].get().strip()
            correo = self.cliente_entries["correo"].get().strip()
            direccion = self.cliente_entries["direccion"].get().strip()
            
        except KeyError as e:
            messagebox.showerror("Error de Formulario", f"Falta el campo clave: {e}")
            return
        
        if not nombre:
            messagebox.showerror("Validación", "El nombre del cliente es obligatorio.")
            return

        # Llama a la función del controlador que usa RentasModel.agregar_cliente
        id_cliente = self.controller.agregar_cliente(
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            correo=correo,
            direccion=direccion
        )
        
        if id_cliente:
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' guardado con ID: {id_cliente}")
            dialog.destroy() 
            # Actualiza la vista de clientes inmediatamente (si es la vista actual)
            if self.current_view == "clientes":
                self.controller.actualizar_vista_clientes()
        else:
            messagebox.showerror("Error de BD", "No se pudo guardar el cliente. Revisa la consola.")

    # En view.py, dentro del método guardar_orden, justo después de obtener los valores:
    def guardar_orden(self, dialog: ctk.CTkToplevel):
        """Recupera los datos del diálogo de Nueva Orden y los guarda como Reservación."""
        try:
            # Usar los atributos del diálogo, no de self
            articulo_nombre = dialog.campos_orden["articulo"].get()
            cliente_nombre = dialog.campos_orden["clientes"].get()
            estado = dialog.campos_orden["estado"].get()
            
            # Fecha de entrega
            fecha_entrega_widget = dialog.campos_orden["fecha de entrega"]
            fecha_entrega_date = fecha_entrega_widget.get_date()
            fecha_entrega_str = fecha_entrega_date.strftime("%Y-%m-%d")
            
            # Fecha de devolución
            fecha_devolucion_widget = dialog.campos_orden["fecha de devolución"]
            fecha_devolucion_date = fecha_devolucion_widget.get_date()
            fecha_devolucion_str = fecha_devolucion_date.strftime("%Y-%m-%d")
            
        except KeyError as e:
            messagebox.showerror("Error de Formulario", f"Falta el campo clave: {e}")
            return
        except AttributeError:
            messagebox.showerror("Error", "Campos del formulario no encontrados.")
            return
        
        # ----- AQUÍ VA EL MAPEO DE ESTADOS -----
        # Mapear estados del diálogo a estados de la BD
        estado_map = {
            "Programado": "pendiente",
            "En Curso": "en_proceso",
            "Entregado": "completada",
            "Cancelado": "cancelada"
        }
        
        estado_bd = estado_map.get(estado, "pendiente")
        # ---------------------------------------
        
        # OBTENER IDs REALES USANDO LOS MAPEOS DEL DIÁLOGO
        cliente_id_fk = dialog.cliente_map.get(cliente_nombre)
        articulo_id = dialog.articulo_map.get(articulo_nombre)

        if not cliente_id_fk or not articulo_id:
            messagebox.showerror("Validación", "Debes seleccionar un cliente y un artículo válidos.")
            return

        usuario_id_logueado = self.controller.get_usuario_id()
        if not usuario_id_logueado:
            messagebox.showerror("Error", "No se pudo obtener ID de usuario.")
            return

        costo_total = 100.00  # Esto debería venir del precio del artículo

        datos_orden = {
            'cliente_id': cliente_id_fk,
            'estado': estado_bd,  # ← Usar estado_bd aquí en lugar del estado original
            'fecha_evento': fecha_entrega_str,
            'fecha_entrega': fecha_entrega_str,
            'total': costo_total,
            'observaciones': f"Alquiler: {articulo_nombre} | Cliente: {cliente_nombre}",
            'articulos': [
                {
                    'articulo_id': articulo_id,
                    'cantidad': 1,
                    'precio_unitario': costo_total
                }
            ],
        }
        
        try:
            id_reservacion = self.controller.agregar_reservacion_completa(datos_orden)
            #actualizar_ordenes_simples
            if id_reservacion:
                messagebox.showinfo("Éxito", f"Reservación para '{articulo_nombre}' guardada con ID: {id_reservacion}")
                dialog.destroy()
                # Actualizar la vista
                self.controller.actualizar_vista()
            else:
                messagebox.showerror("Error de BD", "No se pudo guardar la reservación/orden.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
 

# ========== MÉTODOS PARA CRUD DE ÓRDENES ==========
#_show_dashboard
    def _configurar_treeview_ordenes(self):
        """Configura eventos del Treeview de órdenes para CRUD."""
        try:
            # Configurar doble clic para editar
            self.ordenes_tree.bind('<Double-1>', self._editar_orden_doble_clic)
            
            # Configurar menú contextual
            self.menu_contextual_ordenes = tk.Menu(self.root, tearoff=0)
            self.menu_contextual_ordenes.add_command(label="📋 Ver Detalles", command=self._ver_detalles_orden)
            self.menu_contextual_ordenes.add_command(label="📝 Editar Orden", command=self._editar_orden)
            self.menu_contextual_ordenes.add_command(label="🔄 Cambiar Estado", command=self._cambiar_estado_orden)
            self.menu_contextual_ordenes.add_separator()
            self.menu_contextual_ordenes.add_command(label="🗑️ Eliminar Orden", command=self._eliminar_orden)
            
            # Vincular menú contextual
            self.ordenes_tree.bind('<Button-3>', self._mostrar_menu_contextual_ordenes)
            
        except Exception as e:
            print(f"Error configurando treeview de órdenes: {e}")

    def _editar_orden_doble_clic(self, event):
        """Maneja doble clic para editar orden."""
        self._editar_orden()
#_show_ordenes
    def _mostrar_menu_contextual_ordenes(self, event):
        """Muestra el menú contextual para órdenes."""
        try:
            # Seleccionar el item bajo el cursor
            item = self.ordenes_tree.identify_row(event.y)
            if item:
                self.ordenes_tree.selection_set(item)
                self.menu_contextual_ordenes.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error mostrando menú contextual de órdenes: {e}")

    def _ver_detalles_orden(self):
        """Muestra los detalles de la orden seleccionada."""
        seleccionado = self.ordenes_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una orden para ver detalles.")
            return
        
        item = seleccionado[0]
        valores = self.ordenes_tree.item(item, 'values')
        orden_id = self._obtener_id_orden_desde_tree(item)
        
        if not orden_id:
            messagebox.showerror("Error", "No se pudo obtener el ID de la orden.")
            return
        
        # Obtener detalles completos de la BD
        orden = self.controller.model.obtener_detalles_orden_completa(orden_id)
        if not orden:
            messagebox.showerror("Error", "No se encontró la orden en la base de datos.")
            return
        
        # Mostrar diálogo con detalles
        self._mostrar_dialogo_detalles_orden(orden)

    def _editar_orden(self):
        """Abre diálogo para editar una orden seleccionada."""
        seleccionado = self.ordenes_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una orden para editar.")
            return
        
        item = seleccionado[0]
        orden_id = self._obtener_id_orden_desde_tree(item)
        
        if not orden_id:
            messagebox.showerror("Error", "No se pudo obtener el ID de la orden.")
            return
        
        # Obtener datos de la orden desde la BD
        orden = self.controller.model.obtener_detalles_orden_completa(orden_id)
        if not orden:
            messagebox.showerror("Error", "No se encontró la orden en la base de datos.")
            return
        
        # Mostrar diálogo de edición
        self._mostrar_dialogo_editar_orden(orden)

    def _cambiar_estado_orden(self):
        """Cambia el estado de la orden seleccionada."""
        seleccionado = self.ordenes_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una orden para cambiar estado.")
            return
        
        item = seleccionado[0]
        valores = self.ordenes_tree.item(item, 'values')
        orden_id = self._obtener_id_orden_desde_tree(item)
        estado_actual = valores[2] if len(valores) > 2 else ""
        
        if not orden_id:
            messagebox.showerror("Error", "No se pudo obtener el ID de la orden.")
            return
        
        # Mostrar diálogo para seleccionar nuevo estado
        self._mostrar_dialogo_cambiar_estado(orden_id, estado_actual)

    def _eliminar_orden(self):
        """Elimina la orden seleccionada."""
        seleccionado = self.ordenes_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una orden para eliminar.")
            return
        
        item = seleccionado[0]
        valores = self.ordenes_tree.item(item, 'values')
        orden_id = self._obtener_id_orden_desde_tree(item)
        cliente_nombre = valores[1] if len(valores) > 1 else "Orden"
        
        if not orden_id:
            messagebox.showerror("Error", "No se pudo obtener el ID de la orden.")
            return
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar la orden #{orden_id} para '{cliente_nombre}'?\n\n"
            f"Esta acción no se puede deshacer y eliminará todos los detalles relacionados."
        )
        
        if confirmacion:
            if self.controller.eliminar_orden(orden_id):
                messagebox.showinfo("Éxito", f"Orden #{orden_id} eliminada correctamente.")
                # Actualizar vista
                self.controller.actualizar_vista_ordenes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la orden.")

    def _obtener_id_orden_desde_tree(self, item):
        """Obtiene el ID de la orden desde el item del treeview."""
        try:
            valores = self.ordenes_tree.item(item, 'values')
            if valores and len(valores) > 0:
                # El ID debería estar en algún campo oculto o en la primera columna
                # Depende de cómo estés almacenando los datos
                orden_id = valores[0] if valores[0] and valores[0].isdigit() else None
                return orden_id
        except Exception as e:
            print(f"Error obteniendo ID de orden: {e}")
        return None

    def _mostrar_dialogo_detalles_orden(self, orden):
        """Muestra un diálogo con los detalles completos de una orden."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Detalles de Orden #{orden.get('id', 'N/A')}")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()

        # Título
        titulo = ctk.CTkLabel(master=dialog, 
                            text=f"📄 Detalles de Orden #{orden.get('id', 'N/A')}", 
                            font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=15)

        # Frame para contenido
        content_frame = ctk.CTkFrame(master=dialog)
        content_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Información básica
        info_text = f"""
        👤 Cliente: {orden.get('cliente_nombre', 'N/A')}
        📅 Fecha Evento: {orden.get('fecha_evento', 'N/A')}
        📅 Fecha Entrega: {orden.get('fecha_entrega', 'N/A')}
        📅 Fecha Devolución: {orden.get('fecha_devolucion', 'N/A')}
        📊 Estado: {orden.get('estado', 'N/A')}
        💰 Total: ${orden.get('total', 0):.2f}
        
        📝 Observaciones:
        {orden.get('observaciones', 'Sin observaciones')}
        
        👤 Creado por: {orden.get('usuario_nombre', 'N/A')}
        📅 Fecha Reservación: {orden.get('fecha_reservacion', 'N/A')}
        """
        
        info_label = ctk.CTkLabel(master=content_frame, text=info_text,
                                font=ctk.CTkFont(size=12), justify="left")
        info_label.pack(pady=10, padx=10, anchor="w")

        # Botón para cerrar
        btn_cerrar = ctk.CTkButton(master=dialog, text="Cerrar", 
                                command=dialog.destroy,
                                width=100, height=35)
        btn_cerrar.pack(pady=15)

    def _mostrar_dialogo_editar_orden(self, orden):
        """Muestra diálogo para editar una orden existente."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Editar Orden #{orden.get('id', 'N/A')}")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Implementar formulario de edición similar a crear nueva orden
        # pero con los valores precargados

    def _mostrar_dialogo_cambiar_estado(self, orden_id, estado_actual):
        """Muestra diálogo para cambiar el estado de una orden."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Cambiar Estado - Orden #{orden_id}")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        titulo = ctk.CTkLabel(master=dialog, 
                            text=f"🔄 Cambiar Estado de Orden #{orden_id}", 
                            font=ctk.CTkFont(size=16, weight="bold"))
        titulo.pack(pady=15)

        content_frame = ctk.CTkFrame(master=dialog)
        content_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Estado actual
        lbl_actual = ctk.CTkLabel(master=content_frame, 
                                text=f"Estado actual: {estado_actual}",
                                font=ctk.CTkFont(size=14))
        lbl_actual.pack(pady=(0, 20))

        # Opciones de estado
        lbl_nuevo = ctk.CTkLabel(master=content_frame, text="Nuevo estado:")
        lbl_nuevo.pack(pady=(0, 10))

        estados = ["pendiente", "confirmada", "en_proceso", "completada", "cancelada"]
        var_estado = StringVar(value=estado_actual)
        
        for estado in estados:
            rb = ctk.CTkRadioButton(master=content_frame, 
                                text=estado.replace('_', ' ').title(),
                                variable=var_estado, 
                                value=estado)
            rb.pack(anchor="w", padx=30, pady=5)

        def aplicar_cambio():
            nuevo_estado = var_estado.get()
            if nuevo_estado == estado_actual:
                messagebox.showinfo("Info", "El estado es el mismo. No se realizaron cambios.")
                dialog.destroy()
                return
            
            if self.controller.actualizar_estado_orden(orden_id, nuevo_estado):
                messagebox.showinfo("Éxito", f"Estado cambiado a '{nuevo_estado}'")
                dialog.destroy()
                self.controller.actualizar_vista_ordenes()
            else:
                messagebox.showerror("Error", "No se pudo cambiar el estado.")

        # Botones
        btn_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        btn_aplicar = ctk.CTkButton(master=btn_frame, text="Aplicar Cambio",
                                command=aplicar_cambio,
                                width=120, height=35,
                                fg_color="#3498db")
        btn_aplicar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(master=btn_frame, text="Cancelar",
                                    command=dialog.destroy,
                                    width=100, height=35,
                                    fg_color="#95a5a6")
        btn_cancelar.pack(side="left", padx=10)


    def _build_ordenes_view(self):
        main_container = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        main_container.pack(fill="both", expand=True)

        title_section = ctk.CTkFrame(master=main_container, fg_color="#f7f7f7")
        title_section.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(master=title_section, text="Gestión de Órdenes y Reservaciones", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", padx=20, pady=10, side="left")

        # Frame para botones
        btn_frame = ctk.CTkFrame(master=title_section, fg_color="#f7f7f7")
        btn_frame.pack(anchor="e", side="right", padx=20, pady=10)
        
        # Botón de actualizar
        actualizar_btn = ctk.CTkButton(
            master=btn_frame, 
            text="↻ Actualizar", 
            command=lambda: self.controller.actualizar_vista_ordenes(),
            width=120, 
            height=35,
            fg_color="#3498db",
            text_color="white"
        )
        actualizar_btn.pack(side="left", padx=(0, 10))
        
        # Botón de crear orden
        crear_orden_btn = ctk.CTkButton(
            master=btn_frame, 
            text="+ Crear Nueva Orden", 
            command=self.controller.crear_nueva_orden, 
            width=180, 
            height=35,
            fg_color="#6b2fb8", 
            text_color="white"
        )
        crear_orden_btn.pack(side="left")
        
        # Tabla de órdenes
        orders_card = ctk.CTkFrame(master=main_container, fg_color="#ffffff", corner_radius=12)
        orders_card.pack(fill="both", expand=True, padx=20, pady=10)

        # Configuración del estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 12), rowheight=30, 
                    background="#ffffff", fieldbackground="#ffffff", foreground="#333333")
        style.map("Treeview", background=[('selected', '#8f49e6')])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), 
                    background="#6b2fb8", foreground="white")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Frame para tabla y scrollbar
        table_frame = ctk.CTkFrame(master=orders_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Columnas
        columns = ('ID', 'Articulo', 'Cliente', 'Estado', 'Fecha Entrega', 'Acciones')
        self.ordenes_tree = ttk.Treeview(
            master=table_frame, columns=columns, show='headings', height=15
        )
        
        # Configurar columnas
        column_widths = {'ID': 60, 'Articulo': 200, 'Cliente': 150, 
                        'Estado': 120, 'Fecha Entrega': 120, 'Acciones': 100}
        
        for col in columns:
            self.ordenes_tree.heading(col, text=col)
            self.ordenes_tree.column(col, width=column_widths.get(col, 100), 
                                anchor="center" if col in ['ID', 'Estado', 'Fecha Entrega'] else "w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.ordenes_tree.yview)
        self.ordenes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.ordenes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Etiqueta de "No hay datos"
        self.lbl_sin_datos_ordenes = ctk.CTkLabel(master=table_frame, 
                                                text="Cargando reservaciones...", 
                                                text_color="#7a7a7a")
        self.lbl_sin_datos_ordenes.place(relx=0.5, rely=0.5, anchor="center")
 
#actualizar_reservaciones 
    def actualizar_dashboard(self, eventos, reservaciones, total_activas, total_clientes):
        """Actualiza solo el dashboard sin recrear widgets."""
        try:
            # Actualizar eventos
            if hasattr(self, 'card_eventos_desc') and self.card_eventos_desc.winfo_exists():
                eventos_str = [f"{e['titulo']} - {e['fecha_evento']}" for e in eventos[:3]]
                texto_eventos = "\n".join(eventos_str) if eventos_str else "Sin eventos programados."
                self.card_eventos_desc.configure(text=texto_eventos)
            
            # Actualizar contador de reservaciones activas
            if hasattr(self, 'lbl_total_activas') and self.lbl_total_activas.winfo_exists():
                self.lbl_total_activas.configure(text=str(total_activas))
            
            # Actualizar contador de clientes
            if hasattr(self, 'lbl_total_clientes') and self.lbl_total_clientes.winfo_exists():
                self.lbl_total_clientes.configure(text=str(total_clientes))
            
            # Actualizar tabla
            if hasattr(self, 'tree') and self.tree.winfo_exists():
                self.actualizar_reservaciones(reservaciones, total_activas)
                
        except Exception as e:
            print(f"Error actualizando dashboard: {e}")

    def ocultar(self):
        if hasattr(self, 'app_frame'):
            self.app_frame.pack_forget()

    def mostrar(self):
        if hasattr(self, 'app_frame'):
            self.app_frame.pack(fill="both", expand=True)
#_mostrar_dialogo_editar_reservacion


    # -------------------------
    # VISTA DE USUARIOS
    # -------------------------
    def _show_usuarios(self):
        """Muestra la vista de gestión de usuarios."""
        self._clear_content()
        self.current_view = "usuarios"
        self._update_button_colors()
        self._build_usuarios_view()

    def _build_usuarios_view(self):
        """Construye la vista de usuarios."""
        main_container = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        main_container.pack(fill="both", expand=True)

        # Cabecera
        header_frame = ctk.CTkFrame(master=main_container, fg_color="#f7f7f7")
        header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(master=header_frame, text="Gestión de Usuarios", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", padx=20, pady=10, side="left")

        # Botones de acción
        btn_frame = ctk.CTkFrame(master=header_frame, fg_color="#f7f7f7")
        btn_frame.pack(anchor="e", side="right", padx=20, pady=10)

        actualizar_btn = ctk.CTkButton(
            master=btn_frame,
            text="↻ Actualizar",
            command=self._actualizar_usuarios,
            width=120,
            height=35,
            fg_color="#3498db"
        )
        actualizar_btn.pack(side="left", padx=(0, 10))

        nuevo_usuario_btn = ctk.CTkButton(
            master=btn_frame,
            text="+ Nuevo Usuario",
            command=self._mostrar_dialogo_nuevo_usuario,
            width=150,
            height=35,
            fg_color="#27ae60"
        )
        nuevo_usuario_btn.pack(side="left")

        # Tabla de usuarios
        table_card = ctk.CTkFrame(master=main_container, fg_color="#ffffff", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=20, pady=10)

        # Configurar estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 11), rowheight=35)
        style.map("Treeview", background=[('selected', '#8f49e6')])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), 
                    background="#6b2fb8", foreground="white")

        # Frame para tabla
        table_frame = ctk.CTkFrame(master=table_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Columnas
        columns = ('ID', 'Usuario', 'Nombre', 'Email', 'Rol', 'Último Login', 'Acciones')
        self.usuarios_tree = ttk.Treeview(
            master=table_frame,
            columns=columns,
            show='headings',
            height=12
        )

        # Configurar columnas
        for col in columns:
            self.usuarios_tree.heading(col, text=col)
            self.usuarios_tree.column(col, width=120, anchor="center" 
                                    if col in ['ID', 'Rol', 'Acciones'] else "w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscrollcommand=scrollbar.set)

        self.usuarios_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Etiqueta de "No hay datos"
        self.lbl_sin_datos_usuarios = ctk.CTkLabel(master=table_frame,
                                                text="Cargando usuarios...",
                                                text_color="#7a7a7a")
        self.lbl_sin_datos_usuarios.place(relx=0.5, rely=0.5, anchor="center")

        # Configurar eventos
        self._configurar_treeview_usuarios()

        # Cargar datos iniciales
        self._actualizar_usuarios()

    def _configurar_treeview_usuarios(self):
        """Configura eventos del Treeview de usuarios."""
        try:
            # Menú contextual
            self.menu_contextual_usuarios = tk.Menu(self.root, tearoff=0)
            self.menu_contextual_usuarios.add_command(label="📝 Editar Usuario", 
                                                    command=self._editar_usuario)
            self.menu_contextual_usuarios.add_command(label="🗑️ Eliminar Usuario", 
                                                    command=self._eliminar_usuario)
            
            # Vincular eventos
            self.usuarios_tree.bind('<Button-3>', self._mostrar_menu_contextual_usuarios)
            self.usuarios_tree.bind('<Double-1>', lambda e: self._editar_usuario())
            
        except Exception as e:
            print(f"Error configurando treeview de usuarios: {e}")

    def _mostrar_menu_contextual_usuarios(self, event):
        """Muestra el menú contextual para usuarios."""
        try:
            item = self.usuarios_tree.identify_row(event.y)
            if item:
                self.usuarios_tree.selection_set(item)
                self.menu_contextual_usuarios.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error mostrando menú contextual de usuarios: {e}")

    def _actualizar_usuarios(self):
        """Actualiza la lista de usuarios."""
        try:
            # Obtener usuarios del controlador
            usuarios = self.controller.obtener_usuarios()
            
            # Limpiar tabla
            for item in self.usuarios_tree.get_children():
                self.usuarios_tree.delete(item)
            
            if usuarios:
                self.lbl_sin_datos_usuarios.place_forget()
                
                for usuario in usuarios:
                    ultimo_login = usuario.get('ultimo_login')
                    if ultimo_login:
                        ultimo_login_str = ultimo_login.strftime("%Y-%m-%d %H:%M")
                    else:
                        ultimo_login_str = "Nunca"
                    
                    self.usuarios_tree.insert("", "end", values=(
                        usuario.get('id'),
                        usuario.get('usuario'),
                        usuario.get('nombre_completo', ''),
                        usuario.get('email', ''),
                        usuario.get('rol', 'empleado').title(),
                        ultimo_login_str,
                        "Editar | Eliminar"
                    ))
            else:
                self.lbl_sin_datos_usuarios.configure(text="No hay usuarios registrados")
                self.lbl_sin_datos_usuarios.place(relx=0.5, rely=0.5, anchor="center")
                
        except Exception as e:
            print(f"Error actualizando usuarios: {e}")
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")

    def _mostrar_dialogo_nuevo_usuario(self):
        """Muestra diálogo para crear nuevo usuario."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Nuevo Usuario")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()

        # Título
        titulo = ctk.CTkLabel(master=dialog, text="Crear Nuevo Usuario",
                            font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=15)

        # Frame del formulario
        form_frame = ctk.CTkFrame(master=dialog)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Campos
        campos = []
        row = 0

        # Usuario
        lbl_usuario = ctk.CTkLabel(master=form_frame, text="Usuario *:")
        lbl_usuario.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 5))
        entry_usuario = ctk.CTkEntry(master=form_frame, width=250)
        entry_usuario.grid(row=row, column=1, padx=10, pady=(10, 5))
        campos.append(('usuario', entry_usuario))
        row += 1

        # Contraseña
        lbl_password = ctk.CTkLabel(master=form_frame, text="Contraseña *:")
        lbl_password.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry_password = ctk.CTkEntry(master=form_frame, width=250, show="•")
        entry_password.grid(row=row, column=1, padx=10, pady=5)
        campos.append(('password', entry_password))
        row += 1

        # Confirmar contraseña
        lbl_confirm_password = ctk.CTkLabel(master=form_frame, text="Confirmar Contraseña *:")
        lbl_confirm_password.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry_confirm_password = ctk.CTkEntry(master=form_frame, width=250, show="•")
        entry_confirm_password.grid(row=row, column=1, padx=10, pady=5)
        campos.append(('confirm_password', entry_confirm_password))
        row += 1

        # Nombre completo
        lbl_nombre = ctk.CTkLabel(master=form_frame, text="Nombre Completo:")
        lbl_nombre.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry_nombre = ctk.CTkEntry(master=form_frame, width=250)
        entry_nombre.grid(row=row, column=1, padx=10, pady=5)
        campos.append(('nombre_completo', entry_nombre))
        row += 1

        # Email
        lbl_email = ctk.CTkLabel(master=form_frame, text="Email:")
        lbl_email.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry_email = ctk.CTkEntry(master=form_frame, width=250)
        entry_email.grid(row=row, column=1, padx=10, pady=5)
        campos.append(('email', entry_email))
        row += 1

        # Rol
        lbl_rol = ctk.CTkLabel(master=form_frame, text="Rol:")
        lbl_rol.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        combo_rol = ctk.CTkComboBox(
            master=form_frame,
            values=["admin", "empleado"],
            width=250,
            state="readonly"
        )
        combo_rol.set("empleado")
        combo_rol.grid(row=row, column=1, padx=10, pady=5)
        campos.append(('rol', combo_rol))
        row += 1

        # Botones
        btn_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        def guardar_usuario():
            # Obtener valores
            datos = {}
            for key, widget in campos:
                if isinstance(widget, ctk.CTkEntry):
                    datos[key] = widget.get().strip()
                elif isinstance(widget, ctk.CTkComboBox):
                    datos[key] = widget.get()

            # Validaciones
            if not datos.get('usuario'):
                messagebox.showerror("Error", "El usuario es obligatorio")
                return

            if not datos.get('password'):
                messagebox.showerror("Error", "La contraseña es obligatoria")
                return

            if datos['password'] != datos.get('confirm_password', ''):
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

            # Remover confirm_password
            del datos['confirm_password']

            # Guardar
            if self.controller.agregar_usuario(datos):
                dialog.destroy()

        def cancelar():
            dialog.destroy()

        btn_guardar = ctk.CTkButton(master=btn_frame, text="Guardar",
                                command=guardar_usuario,
                                width=120, height=35,
                                fg_color="#27ae60")
        btn_guardar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(master=btn_frame, text="Cancelar",
                                    command=cancelar,
                                    width=120, height=35,
                                    fg_color="#95a5a6")
        btn_cancelar.pack(side="left", padx=10)

    def _editar_usuario(self):
        """Edita el usuario seleccionado."""
        seleccionado = self.usuarios_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para editar")
            return

        item = seleccionado[0]
        valores = self.usuarios_tree.item(item, 'values')
        usuario_id = valores[0]

        # Obtener datos del usuario
        usuario = self.controller.obtener_usuario(usuario_id)
        if not usuario:
            messagebox.showerror("Error", "No se pudo obtener los datos del usuario")
            return

        # Mostrar diálogo de edición (similar al de nuevo usuario)
        self._mostrar_dialogo_editar_usuario(usuario)

    def _mostrar_dialogo_editar_usuario(self, usuario):
        """Muestra diálogo para editar usuario."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Editar Usuario: {usuario.get('usuario')}")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        # Título
        titulo = ctk.CTkLabel(master=dialog, text=f"Editar Usuario: {usuario.get('usuario')}",
                            font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=15)

        # Frame del formulario
        form_frame = ctk.CTkFrame(master=dialog)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Campos
        row = 0

        # Usuario
        lbl_usuario = ctk.CTkLabel(master=form_frame, text="Usuario *:")
        lbl_usuario.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 5))
        entry_usuario = ctk.CTkEntry(master=form_frame, width=250)
        entry_usuario.insert(0, usuario.get('usuario', ''))
        entry_usuario.grid(row=row, column=1, padx=10, pady=(10, 5))
        row += 1

        # Nueva contraseña (opcional)
        lbl_password = ctk.CTkLabel(master=form_frame, text="Nueva Contraseña:")
        lbl_password.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry_password = ctk.CTkEntry(master=form_frame, width=250, show="•", 
                                    placeholder_text="Dejar vacío para no cambiar")
        entry_password.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Nombre completo
        lbl_nombre = ctk.CTkLabel(master=form_frame, text="Nombre Completo:")
        lbl_nombre.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry_nombre = ctk.CTkEntry(master=form_frame, width=250)
        entry_nombre.insert(0, usuario.get('nombre_completo', ''))
        entry_nombre.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Email
        lbl_email = ctk.CTkLabel(master=form_frame, text="Email:")
        lbl_email.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry_email = ctk.CTkEntry(master=form_frame, width=250)
        entry_email.insert(0, usuario.get('email', ''))
        entry_email.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Rol
        lbl_rol = ctk.CTkLabel(master=form_frame, text="Rol:")
        lbl_rol.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        combo_rol = ctk.CTkComboBox(
            master=form_frame,
            values=["admin", "empleado"],
            width=250,
            state="readonly"
        )
        combo_rol.set(usuario.get('rol', 'empleado'))
        combo_rol.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Estado
        lbl_activo = ctk.CTkLabel(master=form_frame, text="Activo:")
        lbl_activo.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        combo_activo = ctk.CTkComboBox(
            master=form_frame,
            values=["Sí", "No"],
            width=250,
            state="readonly"
        )
        combo_activo.set("Sí" if usuario.get('activo', 1) else "No")
        combo_activo.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Botones
        btn_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        def guardar_cambios():
            datos = {
                'usuario': entry_usuario.get().strip(),
                'password': entry_password.get().strip() if entry_password.get().strip() else None,
                'nombre_completo': entry_nombre.get().strip(),
                'email': entry_email.get().strip(),
                'rol': combo_rol.get(),
                'activo': 1 if combo_activo.get() == "Sí" else 0
            }
            
            if not datos['usuario']:
                messagebox.showerror("Error", "El usuario es obligatorio")
                return

            if self.controller.actualizar_usuario(usuario['id'], datos):
                dialog.destroy()
                # Actualizar vista
                self._actualizar_usuarios()

        def cancelar():
            dialog.destroy()

        btn_guardar = ctk.CTkButton(master=btn_frame, text="Guardar",
                                command=guardar_cambios,
                                width=120, height=35,
                                fg_color="#27ae60")
        btn_guardar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(master=btn_frame, text="Cancelar",
                                    command=cancelar,
                                    width=120, height=35,
                                    fg_color="#95a5a6")
        btn_cancelar.pack(side="left", padx=10)

    def _eliminar_usuario(self):
        """Elimina el usuario seleccionado."""
        seleccionado = self.usuarios_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para eliminar")
            return

        item = seleccionado[0]
        valores = self.usuarios_tree.item(item, 'values')
        usuario_id = valores[0]
        nombre_usuario = valores[1]

        # Confirmar eliminación
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al usuario '{nombre_usuario}'?\n\n"
            f"Esta acción no se puede deshacer. El usuario será desactivado."
        )

        if confirmacion:
            if self.controller.eliminar_usuario(usuario_id):
                # Actualizar vista
                self._actualizar_usuarios()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario")

    # -------------------------
    # DIÁLOGOS MEJORADOS PARA RESERVACIONES
    # -------------------------
    def _mostrar_dialogo_editar_reservacion(self, reservacion):
        """Muestra diálogo para editar una reservación existente."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Editar Reservación #{reservacion.get('id')}")
        dialog.geometry("600x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Título
        titulo = ctk.CTkLabel(master=dialog, 
                            text=f"✏️ Editar Reservación #{reservacion.get('id')}",
                            font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=15)

        # Frame para contenido con scrollbar
        main_frame = ctk.CTkFrame(master=dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame interno para el formulario
        form_frame = ctk.CTkFrame(master=main_frame)
        form_frame.pack(fill="both", expand=True)

        # Obtener listas para combobox
        cliente_map = {item['nombre']: item['id'] for item in self.controller.obtener_lista_clientes()}
        articulo_map = {item['nombre']: item['id'] for item in self.controller.obtener_lista_articulos()}

        lista_clientes = list(cliente_map.keys())
        
        # Variables para almacenar widgets
        combo_cliente = None
        combo_estado = None
        date_widgets = {}
        entry_total = None
        text_obs = None

        # Campos del formulario
        row = 0

        # Cliente
        lbl_cliente = ctk.CTkLabel(master=form_frame, text="Cliente *:")
        lbl_cliente.grid(row=row, column=0, sticky="w", padx=10, pady=10)
        
        cliente_actual = reservacion.get('cliente_nombre', '')
        combo_cliente = ctk.CTkComboBox(
            master=form_frame,
            values=lista_clientes,
            width=300,
            state="readonly"
        )
        combo_cliente.set(cliente_actual if cliente_actual in lista_clientes else "")
        combo_cliente.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # Estado
        lbl_estado = ctk.CTkLabel(master=form_frame, text="Estado:")
        lbl_estado.grid(row=row, column=0, sticky="w", padx=10, pady=10)
        
        estados = ['pendiente', 'confirmada', 'en_proceso', 'completada', 'cancelada']
        combo_estado = ctk.CTkComboBox(
            master=form_frame,
            values=estados,
            width=300,
            state="readonly"
        )
        combo_estado.set(reservacion.get('estado', 'pendiente'))
        combo_estado.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # Fechas
        fecha_campos = ['fecha_evento', 'fecha_entrega', 'fecha_devolucion']
        fecha_labels = ['Fecha Evento', 'Fecha Entrega', 'Fecha Devolución']
        
        for i, (campo, label) in enumerate(zip(fecha_campos, fecha_labels)):
            lbl = ctk.CTkLabel(master=form_frame, text=f"{label}:")
            lbl.grid(row=row, column=0, sticky="w", padx=10, pady=10)
            
            # Obtener fecha de la reservación
            fecha_valor = reservacion.get(campo)
            if fecha_valor:
                if hasattr(fecha_valor, 'strftime'):
                    fecha_default = fecha_valor
                else:
                    try:
                        fecha_default = datetime.strptime(str(fecha_valor), "%Y-%m-%d")
                    except:
                        fecha_default = datetime.now()
            else:
                fecha_default = datetime.now()
            
            date_widget = DateEntry(
                master=form_frame,
                width=20,
                date_pattern='dd/MM/yyyy'
            )
            date_widget.set_date(fecha_default)
            date_widget.grid(row=row, column=1, padx=10, pady=10)
            
            date_widgets[campo] = date_widget
            row += 1

        # Total
        lbl_total = ctk.CTkLabel(master=form_frame, text="Total:")
        lbl_total.grid(row=row, column=0, sticky="w", padx=10, pady=10)
        
        entry_total = ctk.CTkEntry(master=form_frame, width=300)
        entry_total.insert(0, str(reservacion.get('total', 0)))
        entry_total.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # Observaciones
        lbl_obs = ctk.CTkLabel(master=form_frame, text="Observaciones:")
        lbl_obs.grid(row=row, column=0, sticky="w", padx=10, pady=10)
        
        text_obs = ctk.CTkTextbox(master=form_frame, width=300, height=80)
        text_obs.insert("1.0", reservacion.get('observaciones', ''))
        text_obs.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # Frame para botones
        button_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        button_frame.pack(pady=15, padx=20, fill="x")

        def guardar_cambios():
            """Guarda los cambios realizados en la reservación."""
            try:
                datos = {
                    'cliente_id': cliente_map.get(combo_cliente.get()),
                    'estado': combo_estado.get(),
                    'fecha_evento': date_widgets['fecha_evento'].get_date().strftime("%Y-%m-%d"),
                    'fecha_entrega': date_widgets['fecha_entrega'].get_date().strftime("%Y-%m-%d"),
                    'fecha_devolucion': date_widgets['fecha_devolucion'].get_date().strftime("%Y-%m-%d"),
                    'total': float(entry_total.get() or 0),
                    'observaciones': text_obs.get("1.0", "end-1c").strip(),
                    'articulos': []
                }
                
                if not datos['cliente_id']:
                    messagebox.showerror("Error", "Debe seleccionar un cliente válido")
                    return
                
                if self.controller.actualizar_reservacion_completa(reservacion['id'], datos):
                    messagebox.showinfo("Éxito", "Reservación actualizada correctamente")
                    dialog.destroy()
                    self.controller.actualizar_vista_ordenes()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la reservación")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")

        def cancelar():
            dialog.destroy()

        # Botones
        btn_guardar = ctk.CTkButton(
            master=button_frame,
            text="Guardar Cambios",
            command=guardar_cambios,
            width=140,
            height=35,
            fg_color="#27ae60"
        )
        btn_guardar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(
            master=button_frame,
            text="Cancelar",
            command=cancelar,
            width=120,
            height=35,
            fg_color="#95a5a6"
        )
        btn_cancelar.pack(side="left", padx=10)
#actualizar_clientes_completos
    def _mostrar_menu_contextual_clientes(self, event):
        """Muestra el menú contextual al hacer clic derecho en un cliente."""
        try:
            item = self.clientes_tree.identify_row(event.y)
            if item:
                self.clientes_tree.selection_set(item)
                self.menu_contextual_clientes.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error mostrando menú contextual: {e}")

    def _editar_cliente_doble_clic(self, event):
        """Abre edición al hacer doble clic en un cliente."""
        self._editar_cliente_desde_menu()

    def _editar_cliente_desde_menu(self):
        """Edita el cliente seleccionado."""
        seleccionado = self.clientes_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para editar.")
            return
        
        item = seleccionado[0]
        valores = self.clientes_tree.item(item, 'values')
        
        if len(valores) >= 5:  # Asegurarse de que tenemos el ID
            cliente_id = valores[4]  # ID está en la columna oculta
            cliente_nombre = valores[0]
            self._mostrar_dialogo_editar_cliente(cliente_id, cliente_nombre, valores)

    def _eliminar_cliente_desde_menu(self):
        """Elimina el cliente seleccionado."""
        seleccionado = self.clientes_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para eliminar.")
            return
        
        item = seleccionado[0]
        valores = self.clientes_tree.item(item, 'values')
        
        if len(valores) >= 5:
            cliente_id = valores[4]
            cliente_nombre = valores[0]
            
            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar al cliente '{cliente_nombre}'?\n\n"
                f"Esta acción marcará al cliente como inactivo en el sistema."
            )
            
            if confirmacion:
                if self.controller.eliminar_cliente(cliente_id):
                    messagebox.showinfo("Éxito", f"Cliente '{cliente_nombre}' eliminado correctamente.")
                    self.controller.actualizar_vista_clientes()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el cliente.")

    def _ver_detalles_cliente(self):
        """Muestra detalles del cliente seleccionado."""
        seleccionado = self.clientes_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para ver detalles.")
            return
        
        item = seleccionado[0]
        valores = self.clientes_tree.item(item, 'values')
        
        if len(valores) >= 5:
            cliente_id = valores[4]
            cliente_nombre = valores[0]
            
            # Obtener detalles completos del modelo
            cliente = self.controller.model.buscar_cliente_por_id(cliente_id)
            
            if cliente:
                detalles = f"""
                📋 Detalles del Cliente
                
                👤 Nombre: {cliente.get('nombre', 'N/A')}
                📞 Teléfono: {cliente.get('telefono', 'N/A')}
                📧 Correo: {cliente.get('correo', 'N/A')}
                📍 Dirección: {cliente.get('direccion', 'N/A')}
                📅 Fecha Registro: {cliente.get('fecha_registro', 'N/A')}
                """
                
                messagebox.showinfo(f"Detalles - {cliente_nombre}", detalles)
            else:
                messagebox.showerror("Error", "No se encontraron detalles del cliente.")

    def _mostrar_dialogo_editar_cliente(self, cliente_id, cliente_nombre, valores_actuales):
        """Muestra diálogo para editar cliente existente."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Editar Cliente: {cliente_nombre}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        titulo = ctk.CTkLabel(master=dialog, text=f"Editar Cliente: {cliente_nombre}",
                            font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=15)

        form_frame = ctk.CTkFrame(master=dialog)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Campos de edición (mismos que en agregar cliente)
        campos = [
            ("Nombre", "nombre", valores_actuales[0] if len(valores_actuales) > 0 else ""),
            ("Teléfono", "telefono", valores_actuales[1] if len(valores_actuales) > 1 else ""),
            ("Correo", "correo", valores_actuales[2] if len(valores_actuales) > 2 else ""),
            ("Dirección", "direccion", valores_actuales[3] if len(valores_actuales) > 3 else "")
        ]
        
        entries = {}
        for i, (label, key, valor_default) in enumerate(campos):
            lbl = ctk.CTkLabel(master=form_frame, text=f"{label}:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=i, column=0, sticky="w", padx=10, pady=10)
            
            ent = ctk.CTkEntry(master=form_frame, width=300)
            ent.insert(0, valor_default)
            ent.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = ent

        def guardar_cambios():
            nombre = entries['nombre'].get().strip()
            telefono = entries['telefono'].get().strip()
            correo = entries['correo'].get().strip()
            direccion = entries['direccion'].get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio.")
                return
            
            if self.controller.actualizar_cliente(cliente_id, nombre, telefono, correo, direccion):
                dialog.destroy()
                # Actualizar la vista
                self.controller.actualizar_vista_clientes()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el cliente.")

        def cancelar():
            dialog.destroy()

        # Botones
        btn_frame = ctk.CTkFrame(master=dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        btn_guardar = ctk.CTkButton(master=btn_frame, text="Guardar Cambios", 
                                command=guardar_cambios, width=140, height=35,
                                fg_color="#27ae60")
        btn_guardar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(master=btn_frame, text="Cancelar", 
                                    command=cancelar, width=120, height=35,
                                    fg_color="#95a5a6")
        btn_cancelar.pack(side="left", padx=10)