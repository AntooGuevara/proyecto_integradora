import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
# Asegúrate de que esta línea esté descomentada si usas PIL para cargar imágenes
from PIL import Image, ImageTk, ImageDraw 
# Importamos el conector de MySQL
import mysql.connector

# --- 1. MODELO (Modelo.py) ---
# Maneja la lógica de datos y las reglas del negocio (autenticación con MySQL).
class Modelo:
    """
    Gestiona la lógica de autenticación (verificación de credenciales) interactuando 
    con la base de datos MySQL.
    """
    def __init__(self):
        # Configuración de la conexión a la base de datos (BD)
        # Basado en la configuración de tu imagen
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'bd_jerry'
        }
        self.conexion = None
        self.cursor = None
        self.credenciales_respaldo = {"admin": "password123"} # Credenciales de respaldo
        
        # Intentar conectar a la BD al iniciar el Modelo
        self._conectar_bd()

    def _conectar_bd(self):
        """Intenta establecer la conexión con la base de datos MySQL."""
        try:
            self.conexion = mysql.connector.connect(**self.db_config)
            # cursor(buffered=True) es útil para consultas.
            self.cursor = self.conexion.cursor(buffered=True)
            print("INFO: Conexión a la base de datos 'bd_jerry' establecida con éxito.")
        except mysql.connector.Error as err:
            # Captura errores de conexión (ej. BD no iniciada, credenciales incorrectas)
            print(f"ERROR: Ocurrió un error al conectar con la base de datos: {err}")
            messagebox.showerror("Error de Conexión", 
                                f"No se pudo conectar a la base de datos '{self.db_config['database']}'. Por favor, verifique el servidor MySQL y las credenciales.")
            self.conexion = None
            self.cursor = None
            print("ADVERTENCIA: Usando credenciales de respaldo 'admin/password123'.")
    # png
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos de forma segura."""
        if self.cursor:
            self.cursor.close()
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("INFO: Conexión a la base de datos cerrada.")

    def verificar_credenciales(self, usuario, contrasena):
        """
        Verifica las credenciales. Si la BD está disponible, consulta la tabla 'usuarios'.
        Si no, usa las credenciales de respaldo.
        """
        if not self.conexion or not self.cursor:
            # Usar credenciales de respaldo si la BD no está disponible
            return self.credenciales_respaldo.get(usuario) == contrasena
        
        try:
            # 1. Preparar la consulta SQL. Asume una tabla 'usuarios' con campos 'usuario' y 'contrasena'.
            sql = "SELECT password FROM usuarios WHERE nombre = %s"
            self.cursor.execute(sql, (usuario,))
            
            # 2. Obtener el resultado
            resultado = self.cursor.fetchone()
            
            if resultado:
                # Usuario encontrado: comparar la contraseña
                contrasena_bd = resultado[0]
                # NOTA: En un sistema de producción, la verificación de contraseña debería usar hashing (bcrypt, etc.).
                return contrasena_bd == contrasena
            else:
                # Usuario no encontrado
                return False

        except mysql.connector.Error as err:
            print(f"ERROR: Fallo al ejecutar la consulta SQL: {err}")
            messagebox.showerror("Error de BD", "Ocurrió un error al consultar la base de datos. Verifique la estructura de la tabla 'usuarios'.")
            return False

# --- 2. VISTA (Vista.py) ---
# Muestra la interfaz de usuario y recoge la entrada del usuario. Ahora usa CustomTkinter.
class Vista:
    """
    Crea y gestiona todos los elementos visuales de la interfaz de inicio de sesión (CustomTkinter).
    No contiene lógica de negocio, solo presenta los datos del Modelo.
    """
    def __init__(self, master, controlador):
        # Referencia al controlador para notificar eventos (e.g., clic en botón)
        self.controlador = controlador 
        self.master = master
        
        # Configuración de la ventana principal
        ancho_ventana = 1000
        alto_ventana = 600
        master.title("DIVERSIONES JERRY - Login")
        master.geometry(f"{ancho_ventana}x{alto_ventana}")
        master.resizable(False, False)
        
        # Definición de colores y estilos de CTK
        color_primario = "#5DECEE" # Turquesa/Verde Menta
        # ATENCIÓN: Estas rutas son ABSOLUTAS y podrían fallar. Se usa el fallback si no se encuentran.
        fondo_ruta = "fondo.png"
        logo_ruta = "logo.png"
        color_fondo_fallback = "#955DFD" # Morado para el fallback
        
        # ----------------------------------------------------
        # MODIFICACIÓN: Configuración de la IMAGEN de Fondo
        # ----------------------------------------------------
        
        # 1. Aseguramos que el fondo de la ventana principal nunca sea gris (usamos el color de fallback)
        master.configure(fg_color=color_fondo_fallback)
        
        # Intentar cargar la imagen de fondo y usar un CTkLabel que cubra toda la ventana
        try:
            # Cargar y redimensionar la imagen de fondo para ajustarse a la ventana
            fondo_imagen_pil = Image.open(fondo_ruta).resize((ancho_ventana, alto_ventana), Image.LANCZOS)
            self.fondo_ctk_image = ctk.CTkImage(dark_image=fondo_imagen_pil, light_image=fondo_imagen_pil, size=(ancho_ventana, alto_ventana))
            
            # Usar un CTkLabel para la imagen de fondo que ocupa toda la ventana
            self.fondo_principal = ctk.CTkLabel(master, 
                                                text="", 
                                                image=self.fondo_ctk_image)
            
        except Exception as e:
            # Fallback si la imagen no se encuentra: usar un CTkFrame de color sólido (Morado) que cubre todo
            print(f"ADVERTENCIA: Error al cargar o aplicar la imagen de fondo en: {fondo_ruta}. Usando color sólido. Error: {e}")
            self.fondo_principal = ctk.CTkFrame(master, 
                                                fg_color=color_fondo_fallback, 
                                                corner_radius=0) # corner_radius=0 para asegurar que sea un bloque sólido

        # 2. Colocamos el fondo (imagen o color) para que cubra toda la ventana (master)
        self.fondo_principal.place(x=0, y=0, relwidth=1, relheight=1)

        # Contenedor central (tarjeta de login). Siempre se coloca en 'master' para flotar sobre el fondo.
        self.contenedor_central = ctk.CTkFrame(master, # Colocado directamente en master
                                            fg_color="white", 
                                               width=350, 
                                               height=400,
                                               corner_radius=15, 
                                               border_color=color_primario, 
                                               border_width=2)
        # Usamos .place para centrarlo
        self.contenedor_central.place(relx=0.5, rely=0.5, anchor="center")
        
        # Se establece el layout dentro del contenedor central
        self.contenedor_central.grid_columnconfigure(0, weight=1)

        # --- ESPACIO PARA EL LOGO --- 
        try:
            logo_imagen = Image.open(logo_ruta)
            # 2. Crear el objeto CTkImage
            self.logo = ctk.CTkImage(light_image=logo_imagen, 
                                     dark_image=logo_imagen, 
                                     size=(200, 200))
            # 3. Mostrar el logo en la fila 0
            ctk.CTkLabel(self.contenedor_central, 
                         image=self.logo,
                         text="", # Quitar texto para que solo se vea la imagen
                         fg_color="white").grid(row=0, column=0, padx=20, pady=(20, 5))
        except FileNotFoundError:
            # Si el archivo no se encuentra, se muestra un placeholder.
            print(f"ADVERTENCIA: No se encontró la imagen del logo en {logo_ruta}. Usando un placeholder.")
            ctk.CTkLabel(self.contenedor_central, 
                         text="[LOGO]", 
                         font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                         text_color="red",
                         fg_color="white").grid(row=0, column=0, padx=20, pady=(20, 5))
            self.logo = None 
            
        # Subtítulo "Bienvenido de Vuelta" (Fila 1)
        ctk.CTkLabel(self.contenedor_central, 
                     text="Bienvenido de Vuelta", 
                     font=ctk.CTkFont(family="Arial", size=16, weight="bold"), 
                     text_color="gray20",
                     fg_color="white").grid(row=1, column=0, padx=20, pady=(5, 5))

        # Instrucción (Fila 2)
        ctk.CTkLabel(self.contenedor_central, 
                     text="Ingrese sus credenciales para acceder al panel.", 
                     font=ctk.CTkFont(family="Arial", size=11), 
                     text_color="gray50",
                     fg_color="white").grid(row=2, column=0, padx=20, pady=(0, 20))

        # --- Campo Usuario / Email --- (Fila 3 y 4)
        ctk.CTkLabel(self.contenedor_central, 
                     text="Usuario / Email", 
                     font=ctk.CTkFont(family="Arial", size=12), 
                     text_color="gray30",
                     fg_color="white",
                     anchor="w").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.entrada_usuario = ctk.CTkEntry(self.contenedor_central, 
                                            placeholder_text="admin", # Usamos el placeholder nativo de CTK
                                            width=300, 
                                            height=40,
                                            corner_radius=8,
                                            border_color="#5DECEE",
                                            font=ctk.CTkFont(family="Arial", size=14))
        self.entrada_usuario.grid(row=4, column=0, padx=20, pady=(5, 15))
        
        # --- Campo Contraseña --- (Fila 5 y 6)
        ctk.CTkLabel(self.contenedor_central, 
                     text="Contraseña", 
                     font=ctk.CTkFont(family="Arial", size=12), 
                     text_color="gray30",
                     fg_color="white",
                     anchor="w").grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")

        self.entrada_contrasena = ctk.CTkEntry(self.contenedor_central, 
                                            placeholder_text="********",
                                            show="*", 
                                            width=300, 
                                            height=40,
                                            corner_radius=8,
                                            border_color="#5DECEE",
                                            font=ctk.CTkFont(family="Arial", size=14))
        self.entrada_contrasena.grid(row=6, column=0, padx=20, pady=(5, 25))
        
        # --- Botón Iniciar Sesión --- (Fila 7)
        self.boton_login = ctk.CTkButton(self.contenedor_central, 
                                         text="Iniciar Sesión", 
                                         command=self.controlador.manejar_login, # Llama al método del controlador
                                         fg_color=color_primario, 
                                         hover_color=color_primario, 
                                         text_color="gray30",
                                         corner_radius=8,
                                         height=45,
                                         font=ctk.CTkFont(family="Arial", size=14, weight="bold"))
        self.boton_login.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")

    def obtener_credenciales(self):
        """Retorna las entradas de usuario y contraseña."""
        return self.entrada_usuario.get(), self.entrada_contrasena.get()

# --- 3. CONTROLADOR (Controlador.py) ---
# Actúa como intermediario, manejando la lógica de la interfaz.
class Controlador:
    """
    Controla el flujo de la aplicación. Recibe eventos de la Vista, 
    llama al Modelo para la lógica (verificación de BD) y actualiza la Vista.
    """
    def __init__(self, master):
        self.modelo = Modelo()
        self.vista = Vista(master, self)

    def manejar_login(self):
        """
        Método llamado cuando se hace clic en el botón 'Iniciar Sesión'.
        """
        usuario, contrasena = self.vista.obtener_credenciales()

        # Pasa los datos al Modelo para su verificación
        if self.modelo.verificar_credenciales(usuario, contrasena):
            # Usamos tk.messagebox ya que CTk no tiene su propio messagebox.
            messagebox.showinfo("Login Exitoso", f"¡Bienvenido, {usuario}! Acceso concedido.")
            # En una app real, aquí se cerraría la ventana de login y se abriría el panel principal
            # self.vista.master.destroy() 
        else:
            messagebox.showerror("Error de Login", "Usuario o Contraseña incorrectos. Inténtalo de nuevo.")

# --- Ejecución de la Aplicación (POO) ---
if __name__ == "__main__":
    # 1. Configuración global de CustomTkinter
    ctk.set_appearance_mode("light") # Puede ser "light", "dark" o "system"
    ctk.set_default_color_theme("green") # Establece el tema de color base

    # 2. Creamos la ventana principal (Root), usando ctk.CTk()
    root = ctk.CTk()
    
    # 3. Instanciamos el Controlador, que a su vez instancia el Modelo y la Vista
    # 'app' se define aquí para que sea accesible en la función on_closing
    app = Controlador(root)

    # 4. Definición de la función de cierre para asegurar la desconexión de la BD
    def on_closing():
        if app:
            # Llama al método para cerrar la conexión a la BD antes de destruir la ventana
            app.modelo.cerrar_conexion()
        root.destroy()
    
    # 5. Registrar el manejador de eventos para el cierre de la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 6. Iniciamos el bucle principal de CustomTkinter
    root.mainloop()