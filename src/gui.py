"""
Interfaz gráfica para el convertidor de extensiones de imágenes.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from typing import List, Optional

from .image_converter import ImageConverter


class ImageConverterGUI:
    """
    Interfaz gráfica para el convertidor de extensiones de imágenes.
    """
    
    def __init__(self):
        """Inicializar la interfaz gráfica."""
        self.root = tk.Tk()
        self.converter = ImageConverter()
        self.selected_files = []
        self.setup_gui()
    
    def setup_gui(self):
        """Configurar la interfaz gráfica."""
        self.root.title("Convertidor de Extensiones de Imágenes")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Convertidor de Extensiones de Imágenes", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección 1: Selección de archivos
        files_frame = ttk.LabelFrame(main_frame, text="Selección de Archivos", padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        files_frame.columnconfigure(1, weight=1)
        
        # Botón para seleccionar archivos individuales
        ttk.Button(files_frame, text="Seleccionar Imágenes", 
                  command=self.select_files).grid(row=0, column=0, padx=(0, 10))
        
        # Botón para seleccionar carpeta
        ttk.Button(files_frame, text="Seleccionar Carpeta", 
                  command=self.select_folder).grid(row=0, column=1, padx=(0, 10))
        
        # Botón para limpiar selección
        ttk.Button(files_frame, text="Limpiar", 
                  command=self.clear_selection).grid(row=0, column=2)
        
        # Lista de archivos seleccionados
        self.files_listbox = tk.Listbox(files_frame, height=6)
        self.files_listbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(files_frame, orient="vertical", command=self.files_listbox.yview)
        scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Sección 2: Configuración de conversión
        config_frame = ttk.LabelFrame(main_frame, text="Configuración de Conversión", padding="10")
        config_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Selección de extensión de destino
        ttk.Label(config_frame, text="Extensión de destino:").grid(row=0, column=0, sticky=tk.W)
        
        self.target_var = tk.StringVar(value=".1")
        target_combo = ttk.Combobox(config_frame, textvariable=self.target_var, 
                                   values=ImageConverter.TARGET_EXTENSIONS, 
                                   state="readonly", width=10)
        target_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Información sobre organización automática
        info_label = ttk.Label(config_frame, 
                              text="Los archivos se organizarán automáticamente en subcarpetas", 
                              font=("Arial", 9, "italic"), foreground="gray")
        info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Sección 3: Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # Botón de conversión
        self.convert_button = ttk.Button(action_frame, text="Convertir Archivos", 
                                        command=self.start_conversion, style="Accent.TButton")
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de salir
        ttk.Button(action_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT)
        
        # Sección 4: Barra de progreso
        self.progress_var = tk.StringVar(value="Listo para convertir")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=4, column=0, columnspan=3, pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        
        # Inicializar interfaz
        self.update_file_count()
    
    def select_files(self):
        """Seleccionar archivos de imagen individuales."""
        filetypes = [
            ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
            ("Todos los archivos", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=filetypes
        )
        
        if files:
            # Filtrar solo archivos de imagen válidos
            valid_files = [f for f in files if self.converter.is_image_file(f)]
            self.selected_files.extend(valid_files)
            self.selected_files = list(set(self.selected_files))  # Eliminar duplicados
            self.update_files_list()
    
    def select_folder(self):
        """Seleccionar carpeta con imágenes."""
        folder = filedialog.askdirectory(title="Seleccionar carpeta con imágenes")
        
        if folder:
            files = self.converter.get_image_files_from_folder(folder)
            self.selected_files.extend(files)
            self.selected_files = list(set(self.selected_files))  # Eliminar duplicados
            self.update_files_list()
    
    
    def clear_selection(self):
        """Limpiar selección de archivos."""
        self.selected_files = []
        self.update_files_list()
    
    def update_files_list(self):
        """Actualizar lista de archivos seleccionados."""
        self.files_listbox.delete(0, tk.END)
        
        for file_path in self.selected_files:
            filename = Path(file_path).name
            self.files_listbox.insert(tk.END, filename)
        
        self.update_file_count()
    
    def update_file_count(self):
        """Actualizar contador de archivos."""
        count = len(self.selected_files)
        self.progress_var.set(f"Archivos seleccionados: {count}")
        
        # Habilitar/deshabilitar botón de conversión
        self.convert_button.config(state="normal" if count > 0 else "disabled")
    
    def start_conversion(self):
        """Iniciar conversión en un hilo separado."""
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados.")
            return
        
        # Deshabilitar botón durante conversión
        self.convert_button.config(state="disabled")
        
        # Limpiar resultados anteriores
        self.results_text.delete(1.0, tk.END)
        
        # Iniciar conversión en hilo separado
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
    
    def convert_files(self):
        """Convertir archivos (ejecutado en hilo separado)."""
        try:
            target_extension = self.target_var.get()
            
            total_files = len(self.selected_files)
            self.progress_bar.config(maximum=total_files)
            self.progress_bar.config(value=0)
            
            success_count = 0
            
            for i, file_path in enumerate(self.selected_files):
                # Actualizar progreso
                self.root.after(0, lambda: self.progress_var.set(f"Convirtiendo {i+1}/{total_files}"))
                self.root.after(0, lambda: self.progress_bar.config(value=i))
                
                # Convertir archivo
                if self.converter.convert_single_file(file_path, target_extension):
                    success_count += 1
            
            # Finalizar progreso
            self.root.after(0, lambda: self.progress_bar.config(value=total_files))
            self.root.after(0, lambda: self.progress_var.set(f"Conversión completada: {success_count}/{total_files} archivos"))
            
            # Mostrar mensaje final con información sobre subcarpetas
            subfolders_info = ""
            if success_count > 0:
                summary = self.converter.get_conversion_summary()
                subfolders = set(item['subfolder'] for item in summary['converted'])
                if subfolders:
                    subfolders_info = f"\n\nSubcarpetas creadas:\n" + "\n".join(f"📁 {subfolder}" for subfolder in sorted(subfolders))
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Conversión Completada", 
                f"Se convirtieron exitosamente {success_count} de {total_files} archivos.{subfolders_info}"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante la conversión: {e}"))
        
        finally:
            # Rehabilitar botón
            self.root.after(0, lambda: self.convert_button.config(state="normal"))
    
    
    def run(self):
        """Ejecutar la aplicación."""
        self.root.mainloop()


def main():
    """
    Función principal para ejecutar la GUI.
    """
    try:
        app = ImageConverterGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    main()
