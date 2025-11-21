import os
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

# Paths to icons (relative to project root)
ICON_HOME = os.path.join("assets", "icons", "home.png")
ICON_CALENDAR = os.path.join("assets", "icons", "calendar.png")
ICON_USERS = os.path.join("assets", "icons", "users.png")

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # CustomTkinter appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        # Main layout
        self.root.title("DIVERSIONESJERRY - Login")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # Main container
        self.main_frame = ctk.CTkFrame(master=self.root, fg_color="#ffffff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Brand/Image
        self.left_frame = ctk.CTkFrame(master=self.main_frame, fg_color="#6b2fb8", width=400)
        self.left_frame.pack(side="left", fill="y", padx=(0, 20))
        self.left_frame.pack_propagate(False)
        
        # Right side - Login form
        self.right_frame = ctk.CTkFrame(master=self.main_frame, fg_color="#ffffff", width=500)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(False)
        
        self._build_left_side()
        self._build_login_form()
    
    def _build_left_side(self):
        """Build the left brand side"""
        # Brand title
        brand_label = ctk.CTkLabel(
            master=self.left_frame, 
            text="DIVERSIONESJERRY",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        brand_label.pack(pady=(100, 20), padx=20)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            master=self.left_frame,
            text="Bienvenido de Vuelta",
            font=ctk.CTkFont(size=18),
            text_color="white"
        )
        welcome_label.pack(pady=(0, 100))
        
        # Add some decorative text
        decorative_text = ctk.CTkLabel(
            master=self.left_frame,
            text="Sistema de Gestión de Rentas\ny Reservaciones",
            font=ctk.CTkFont(size=14),
            text_color="white",
            justify="center"
        )
        decorative_text.pack(expand=True)
    
    def _build_login_form(self):
        """Build the login form"""
        # Form container
        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#ffffff")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = ctk.CTkLabel(
            master=form_frame,
            text="Iniciar Sesión",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#333333"
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            master=form_frame,
            text="Ingrese sus credenciales para acceder al panel.",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        desc_label.pack(pady=(0, 30))
        
        # Username/Email field
        user_label = ctk.CTkLabel(
            master=form_frame,
            text="Usuario / Email",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        )
        user_label.pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            master=form_frame,
            width=350,
            height=45,
            placeholder_text="ejemplo@dlivrss.com",
            corner_radius=8
        )
        self.username_entry.pack(pady=(0, 20))
        
        # Password field
        pass_label = ctk.CTkLabel(
            master=form_frame,
            text="Contraseña",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        )
        pass_label.pack(anchor="w", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            master=form_frame,
            width=350,
            height=45,
            placeholder_text="••••••••",
            show="•",
            corner_radius=8
        )
        self.password_entry.pack(pady=(0, 30))
        
        # Login button
        login_btn = ctk.CTkButton(
            master=form_frame,
            text="Iniciar Sesión",
            command=self._on_login,
            width=350,
            height=45,
            corner_radius=8,
            fg_color="#6b2fb8",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        login_btn.pack(pady=(0, 20))
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self._on_login())
        self.password_entry.bind("<Return>", lambda e: self._on_login())
        
        # Set focus to username field
        self.username_entry.focus()
    
    def _on_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.mostrar_error("Error", "Por favor complete todos los campos.")
            return
        
        # Call controller to handle login
        self.controller.iniciar_sesion(username, password)
    
    def mostrar_error(self, titulo, mensaje):
        """Show error message"""
        messagebox.showerror(titulo, mensaje)
    
    def mostrar_exito(self, titulo, mensaje):
        """Show success message"""
        messagebox.showinfo(titulo, mensaje)
    
    def limpiar_formulario(self):
        """Clear the login form"""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus()
    
    def ocultar(self):
        """Hide the login view"""
        self.main_frame.pack_forget()
    
    def mostrar(self):
        """Show the login view"""
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

class RentasView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Update window title and size
        self.root.title("Panel de Control de Rentas - DIVERSIONESJERRY")
        self.root.geometry("1200x750")

        # Create main frames: sidebar + content
        self.app_frame = ctk.CTkFrame(master=self.root)
        self.app_frame.pack(fill="both", expand=True)

        # Sidebar (left)
        self.sidebar = ctk.CTkFrame(master=self.app_frame, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.configure(fg_color="#6b2fb8")

        # Content area (right) - will contain different views
        self.content = ctk.CTkFrame(master=self.app_frame, fg_color="#f7f7f7")
        self.content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Load icons
        self.icon_home = self._load_icon(ICON_HOME, (24, 24))
        self.icon_calendar = self._load_icon(ICON_CALENDAR, (24, 24))
        self.icon_users = self._load_icon(ICON_USERS, (24, 24))

        # Build UI
        self._build_sidebar()
        
        # Initialize views
        self.current_view = None
        
        # Show dashboard by default
        self._show_dashboard()

    def _load_icon(self, path, size):
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Warning loading icon {path}: {e}")
            img = Image.new("RGBA", size, (0, 0, 0, 0))
            return ImageTk.PhotoImage(img)

    def _build_sidebar(self):
        # Top spacer
        top_spacer = ctk.CTkFrame(master=self.sidebar, fg_color="#6b2fb8")
        top_spacer.pack(pady=(20, 10))

        # Brand label in sidebar
        brand_label = ctk.CTkLabel(
            master=self.sidebar,
            text="DIVERSIONESJERRY",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        brand_label.pack(pady=(0, 20))

        # Menu buttons
        btn_opts = dict(master=self.sidebar, width=180, height=48, corner_radius=12, anchor="w")

        self.btn_inicio = ctk.CTkButton(image=self.icon_home, text="  Panel de Control", 
                                       command=self._show_dashboard,
                                       fg_color="#8f49e6", text_color="white", **btn_opts)
        self.btn_inicio.pack(pady=(10, 6), padx=16)

        self.btn_ordenes = ctk.CTkButton(image=self.icon_calendar, text="  Órdenes (Reservas)", 
                                        command=self._show_ordenes,
                                        fg_color="#6b2fb8", text_color="white", **btn_opts)
        self.btn_ordenes.pack(pady=6, padx=16)

        self.btn_clientes = ctk.CTkButton(image=self.icon_users, text="  Clientes", 
                                         command=self._show_clientes,
                                         fg_color="#6b2fb8", text_color="white", **btn_opts)
        self.btn_clientes.pack(pady=6, padx=16)

        # Spacer to push the create button to the bottom
        self.sidebar_spacer = ctk.CTkFrame(master=self.sidebar, fg_color="#6b2fb8")
        self.sidebar_spacer.pack(expand=True)

        # Create New Order button at bottom
        self.btn_crear = ctk.CTkButton(master=self.sidebar, text="Crear Nueva Orden",
                                       command=self.controller.crear_nueva_orden,
                                       width=180, height=48, corner_radius=24)
        self.btn_crear.pack(pady=10, padx=16)
        
        # Logout button
        self.btn_logout = ctk.CTkButton(master=self.sidebar, text="Cerrar Sesión",
                                       command=self.controller.cerrar_sesion,
                                       width=180, height=40, corner_radius=20,
                                       fg_color="#e74c3c", text_color="white")
        self.btn_logout.pack(pady=10, padx=16)

    def _clear_content(self):
        """Clear the content area"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def _show_dashboard(self):
        """Show dashboard view"""
        self._clear_content()
        self.current_view = "dashboard"
        
        # Update button colors
        self._update_button_colors()
        
        # Build dashboard
        self._build_topbar("Panel de Control de Rentas")
        self._build_dashboard_cards()
        self._build_orders_section()

    def _show_ordenes(self):
        """Show orders management view"""
        self._clear_content()
        self.current_view = "ordenes"
        
        # Update button colors
        self._update_button_colors()
        
        # Build orders management view
        self._build_topbar("Gestión de Órdenes y Reservaciones")
        self._build_ordenes_view()

    def _show_clientes(self):
        """Show clients view"""
        self._clear_content()
        self.current_view = "clientes"
        
        # Update button colors
        self._update_button_colors()
        
        # Build clients view (placeholder)
        self._build_topbar("Gestión de Clientes")
        lbl = ctk.CTkLabel(master=self.content, text="Vista de Clientes - En Desarrollo", 
                          font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(expand=True)

    def _update_button_colors(self):
        """Update sidebar button colors based on current view"""
        # Reset all buttons to default color
        self.btn_inicio.configure(fg_color="#6b2fb8")
        self.btn_ordenes.configure(fg_color="#6b2fb8")
        self.btn_clientes.configure(fg_color="#6b2fb8")
        
        # Highlight current view button
        if self.current_view == "dashboard":
            self.btn_inicio.configure(fg_color="#8f49e6")
        elif self.current_view == "ordenes":
            self.btn_ordenes.configure(fg_color="#8f49e6")
        elif self.current_view == "clientes":
            self.btn_clientes.configure(fg_color="#8f49e6")

    def _build_topbar(self, title_text):
        """Build top bar with title and user info"""
        topbar = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7", height=80)
        topbar.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(master=topbar, text=title_text, 
                            font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(side="left", padx=(10, 0))

        # Right side user info box
        user_box = ctk.CTkFrame(master=topbar, fg_color="#ffffff", corner_radius=10)
        user_box.pack(side="right", padx=10, pady=16)

        user_label = ctk.CTkLabel(master=user_box, 
                                 text=f"Usuario: {self.controller.get_usuario_actual()}", 
                                 text_color="#6b6b6b")
        user_label.pack(side="left", padx=(10, 8), pady=6)

        user_bubble = ctk.CTkFrame(master=user_box, width=32, height=32, 
                                  corner_radius=16, fg_color="#9b6b4f")
        user_bubble.pack(side="right", padx=(0, 10), pady=6)

    def _build_dashboard_cards(self):
        """Build dashboard cards (only for dashboard view)"""
        cards_frame = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        cards_frame.pack(fill="x", pady=(0, 20))

        card_opts = dict(master=cards_frame, width=360, height=120, 
                        corner_radius=12, fg_color="#ffffff")

        self.card_eventos = ctk.CTkFrame(**card_opts)
        self.card_eventos.pack(side="left", padx=(0, 20))
        lbl_ev_t = ctk.CTkLabel(master=self.card_eventos, text="Próximos Eventos", 
                               font=ctk.CTkFont(size=14, weight="bold"))
        lbl_ev_t.pack(anchor="nw", pady=(12, 4), padx=12)
        lbl_ev_desc = ctk.CTkLabel(master=self.card_eventos, 
                                  text="Eventos programados para esta semana.", 
                                  text_color="#7a7a7a")
        lbl_ev_desc.pack(anchor="nw", padx=12)
        btn_cal = ctk.CTkButton(master=self.card_eventos, text="Ver Calendario", 
                               width=140, height=32, corner_radius=8,
                               command=self.controller.ver_calendario)
        btn_cal.pack(anchor="sw", padx=12, pady=10)

        self.card_reservas = ctk.CTkFrame(**card_opts)
        self.card_reservas.pack(side="left", padx=(0, 20))
        lbl_res_t = ctk.CTkLabel(master=self.card_reservas, 
                                text="Reservaciones Activas", 
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

        self.card_clientes = ctk.CTkFrame(**card_opts)
        self.card_clientes.pack(side="left")
        lbl_cli_t = ctk.CTkLabel(master=self.card_clientes, 
                                text="Clientes Registrados", 
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

    def _build_orders_section(self):
        """Build orders section (only for dashboard view)"""
        orders_card = ctk.CTkFrame(master=self.content, fg_color="#ffffff", 
                                  corner_radius=12)
        orders_card.pack(fill="both", expand=True)

        lbl_title = ctk.CTkLabel(master=orders_card, text="Órdenes Recientes", 
                                font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(anchor="nw", padx=20, pady=(18, 4))

        lbl_sub = ctk.CTkLabel(master=orders_card, 
                              text="Base de datos no disponible (Falta configuración).", 
                              text_color="#9f9f9f")
        lbl_sub.pack(anchor="nw", padx=20)

        # Table area
        table_frame = ctk.CTkFrame(master=orders_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=12)

        columns = ("articulo", "cliente", "estado", "fecha", "acciones")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        for c in columns:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Message when no data
        self.lbl_sin_datos = ctk.CTkLabel(master=table_frame, 
                                         text="No hay reservaciones para mostrar.", 
                                         text_color="#7a7a7a")
        self.lbl_sin_datos.place(relx=0.5, rely=0.5, anchor="center")

    def _build_ordenes_view(self):
        """Build the complete orders management view"""
        # Main container
        main_container = ctk.CTkFrame(master=self.content, fg_color="#f7f7f7")
        main_container.pack(fill="both", expand=True)

        # Title section
        title_section = ctk.CTkFrame(master=main_container, fg_color="#f7f7f7")
        title_section.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(master=title_section, 
                            text="Gestión de Órdenes y Reservaciones",
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w")

        # Create New Order button
        crear_orden_btn = ctk.CTkButton(master=title_section, 
                                       text="Crear Nueva Orden",
                                       command=self.controller.crear_nueva_orden,
                                       width=180, height=40, corner_radius=20,
                                       fg_color="#6b2fb8", text_color="white")
        crear_orden_btn.pack(anchor="e", side="bottom")

        # Separator
        separator = ctk.CTkFrame(master=main_container, height=2, fg_color="#e0e0e0")
        separator.pack(fill="x", pady=10)

        # Orders list section
        orders_card = ctk.CTkFrame(master=main_container, fg_color="#ffffff", 
                                  corner_radius=12)
        orders_card.pack(fill="both", expand=True, pady=10)

        # Loading label
        loading_label = ctk.CTkLabel(master=orders_card, 
                                    text="Cargando datos de reservaciones...",
                                    text_color="#7a7a7a")
        loading_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Table frame
        table_frame = ctk.CTkFrame(master=orders_card, fg_color="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create table using ttk.Treeview
        columns = ("ARTÍCULO PRINCIPAL", "CLIENTE", "ESTADO", "FECHA DE ENTREGA", "ACCIONES")
        self.ordenes_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Configure columns
        for col in columns:
            self.ordenes_tree.heading(col, text=col)
            self.ordenes_tree.column(col, width=200, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", 
                                 command=self.ordenes_tree.yview)
        self.ordenes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.ordenes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # No data message
        self.ordenes_sin_datos = ctk.CTkLabel(master=table_frame, 
                                             text="No hay reservaciones para mostrar.",
                                             text_color="#7a7a7a")
        self.ordenes_sin_datos.place(relx=0.5, rely=0.5, anchor="center")

        # Bottom info
        bottom_info = ctk.CTkLabel(master=main_container, 
                                  text=f"Usuario: {self.controller.get_usuario_actual()}",
                                  text_color="#7a7a7a")
        bottom_info.pack(anchor="w", pady=10)

    # --- Public API used by controller ---
    def actualizar_eventos(self, eventos):
        pass

    def actualizar_reservaciones(self, reservaciones, total_activas):
        self.lbl_total_activas.configure(text=str(total_activas))

        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not reservaciones:
            self.lbl_sin_datos.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.lbl_sin_datos.place_forget()
            for r in reservaciones:
                self.tree.insert("", "end", values=(
                    r.get("articulo", "-"), 
                    r.get("cliente", "-"), 
                    r.get("estado", "-"), 
                    r.get("fecha_entrega", "-"), 
                    ""))

    def actualizar_ordenes_completas(self, ordenes):
        """Update the complete orders management view with data"""
        # Clear existing rows
        for row in self.ordenes_tree.get_children():
            self.ordenes_tree.delete(row)

        if not ordenes:
            self.ordenes_sin_datos.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.ordenes_sin_datos.place_forget()
            for orden in ordenes:
                self.ordenes_tree.insert("", "end", values=(
                    orden.get("articulo", "-"),
                    orden.get("cliente", "-"),
                    orden.get("estado", "-"),
                    orden.get("fecha_entrega", "-"),
                    "Editar | Eliminar"  # Placeholder for action buttons
                ))

    def actualizar_clientes(self, total_clientes):
        self.lbl_total_clientes.configure(text=str(total_clientes))

    def actualizar_usuarios(self, usuarios_conectados):
        pass

    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def mostrar_dialogo_nueva_orden(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Crear Nueva Orden")
        dialog.geometry("420x360")
        dialog.transient(self.root)
        dialog.grab_set()

        titulo_dialog = ctk.CTkLabel(master=dialog, text="Crear Nueva Orden", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        titulo_dialog.pack(pady=16)

        form_frame = ctk.CTkFrame(master=dialog)
        form_frame.pack(pady=8, padx=12, fill="x")

        labels = ["Artículo", "Cliente", "Estado", "Fecha de Entrega"]
        self._entries = {}
        for i, l in enumerate(labels):
            lbl = ctk.CTkLabel(master=form_frame, text=l+":")
            lbl.grid(row=i, column=0, sticky="w", padx=6, pady=6)
            ent = ctk.CTkEntry(master=form_frame, width=260)
            ent.grid(row=i, column=1, padx=6, pady=6)
            self._entries[l.lower()] = ent

        def guardar():
            articulo = self._entries['artículo'].get() if 'artículo' in self._entries else self._entries['articulo'].get()
            cliente = self._entries['cliente'].get()
            estado = self._entries['estado'].get()
            fecha = self._entries['fecha de entrega'].get() if 'fecha de entrega' in self._entries else self._entries['fecha de entrega'].get()

            if articulo and cliente and estado and fecha:
                self.controller.agregar_reservacion(articulo, cliente, estado, fecha)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios")

        btn_save = ctk.CTkButton(master=dialog, text="Guardar", command=guardar, width=120)
        btn_save.pack(pady=14)

        return dialog

    def ocultar(self):
        """Hide the main view"""
        self.app_frame.pack_forget()