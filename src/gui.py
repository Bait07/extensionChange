"""
Interfaz gráfica para el convertidor de extensiones de imágenes.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import os
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
        self.conversion_cancelled = False
        self.start_time = None
        self.setup_gui()
    
    def setup_gui(self):
        """Configurar la interfaz gráfica."""
        self.root.title("Convertidor de Extensiones de Imágenes")
        self.root.geometry("700x450")
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
        
        # Sección 4: Barra de progreso mejorada
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        progress_frame.columnconfigure(0, weight=1)
        
        # Información principal de progreso
        self.progress_var = tk.StringVar(value="Listo para convertir")
        ttk.Label(progress_frame, textvariable=self.progress_var).grid(row=0, column=0, sticky=tk.W)
        
        # Información secundaria (porcentaje, tiempo, etc.)
        self.progress_detail_var = tk.StringVar(value="")
        ttk.Label(progress_frame, textvariable=self.progress_detail_var, 
                 font=("Arial", 8), foreground="gray").grid(row=1, column=0, sticky=tk.W)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botón de cancelar (inicialmente oculto)
        self.cancel_button = ttk.Button(progress_frame, text="Cancelar", 
                                       command=self.cancel_conversion, state="disabled")
        self.cancel_button.grid(row=0, column=1, padx=(10, 0))
        
        
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
        
        # Verificar tamaño total de archivos
        total_size = self.calculate_total_size()
        if total_size > 500 * 1024 * 1024:  # 500MB
            result = messagebox.askyesno(
                "Archivos Grandes Detectados", 
                f"Se detectaron archivos grandes ({self.format_size(total_size)}). "
                f"La conversión puede tardar varios minutos.\n\n¿Deseas continuar?"
            )
            if not result:
                return
        
        # Preparar para conversión
        self.conversion_cancelled = False
        self.start_time = None
        
        # Deshabilitar botón y habilitar cancelar
        self.convert_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        
        # Iniciar conversión en hilo separado
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
    
    def cancel_conversion(self):
        """Cancelar la conversión en curso."""
        self.conversion_cancelled = True
        self.progress_var.set("Cancelando conversión...")
    
    def calculate_total_size(self):
        """Calcular el tamaño total de los archivos seleccionados."""
        total_size = 0
        for file_path in self.selected_files:
            try:
                total_size += os.path.getsize(file_path)
            except:
                pass
        return total_size
    
    def format_size(self, size_bytes):
        """Formatear tamaño en bytes a formato legible."""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def convert_files(self):
        """Convertir archivos (ejecutado en hilo separado)."""
        import time
        
        try:
            target_extension = self.target_var.get()
            total_files = len(self.selected_files)
            
            # Configurar barra de progreso
            self.root.after(0, lambda: self.progress_bar.config(maximum=total_files, value=0))
            self.root.after(0, lambda: self.progress_var.set(f"Preparando conversión de {total_files} archivos..."))
            
            # Registrar tiempo de inicio
            self.start_time = time.time()
            success_count = 0
            failed_count = 0
            
            for i, file_path in enumerate(self.selected_files):
                # Verificar si se canceló la conversión
                if self.conversion_cancelled:
                    self.root.after(0, lambda: self.progress_var.set("Conversión cancelada por el usuario"))
                    break
                
                # Calcular progreso y tiempo estimado
                current_progress = i + 1
                percentage = (current_progress / total_files) * 100
                
                # Calcular tiempo estimado
                elapsed_time = time.time() - self.start_time
                if i > 0:
                    avg_time_per_file = elapsed_time / i
                    remaining_files = total_files - i
                    estimated_remaining = avg_time_per_file * remaining_files
                    time_str = self.format_time(estimated_remaining)
                else:
                    time_str = "Calculando..."
                
                # Actualizar interfaz
                filename = os.path.basename(file_path)
                self.root.after(0, lambda p=percentage, f=filename, t=time_str, curr=current_progress, total=total_files: 
                    self.update_progress_display(p, f, t, curr, total))
                
                # Convertir archivo
                try:
                    if self.converter.convert_single_file(file_path, target_extension):
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
                    print(f"Error al convertir {file_path}: {e}")
                
                # Pequeña pausa para mantener la interfaz responsiva
                time.sleep(0.01)
            
            # Finalizar
            if not self.conversion_cancelled:
                # Actualizar barra al 100%
                self.root.after(0, lambda: self.progress_bar.config(value=total_files))
                
                # Calcular tiempo total
                total_time = time.time() - self.start_time
                time_str = self.format_time(total_time)
                
                # Mostrar mensaje de éxito
                self.root.after(0, lambda: self.show_success_message(success_count, failed_count, total_files, time_str))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante la conversión: {e}"))
        
        finally:
            # Restaurar interfaz
            self.root.after(0, lambda: self.convert_button.config(state="normal"))
            self.root.after(0, lambda: self.cancel_button.config(state="disabled"))
    
    def update_progress_display(self, percentage, filename, time_str, current, total):
        """Actualizar la visualización de progreso."""
        self.progress_var.set(f"Convirtiendo: {filename}")
        self.progress_detail_var.set(f"Progreso: {current}/{total} ({percentage:.1f}%) - Tiempo restante: {time_str}")
        self.progress_bar.config(value=current-1)
    
    def format_time(self, seconds):
        """Formatear tiempo en segundos a formato legible."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}min"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def show_success_message(self, success_count, failed_count, total_files, time_str):
        """Mostrar mensaje de éxito detallado."""
        # Información sobre subcarpetas
        subfolders_info = ""
        if success_count > 0:
            summary = self.converter.get_conversion_summary()
            subfolders = set(item['subfolder'] for item in summary['converted'])
            if subfolders:
                subfolders_info = f"\n\n📁 Subcarpetas creadas:\n" + "\n".join(f"   • {subfolder}" for subfolder in sorted(subfolders))
        
        # Mensaje principal
        if failed_count == 0:
            title = "✅ ¡Conversión Completada Exitosamente!"
            message = f"""🎉 ¡Perfecto! Todos los archivos se convirtieron correctamente.

📊 Resumen:
   • Archivos convertidos: {success_count}/{total_files}
   • Tiempo total: {time_str}
   • Sin errores{subfolders_info}

✨ Los archivos están listos para usar."""
        else:
            title = "⚠️ Conversión Completada con Advertencias"
            message = f"""📋 Conversión finalizada con algunos problemas.

📊 Resumen:
   • Archivos convertidos: {success_count}/{total_files}
   • Archivos fallidos: {failed_count}
   • Tiempo total: {time_str}{subfolders_info}

⚠️ Revisa los archivos fallidos e intenta nuevamente si es necesario."""
        
        messagebox.showinfo(title, message)
    
    
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
