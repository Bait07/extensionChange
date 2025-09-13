"""
Módulo principal de la aplicación.
Contiene la lógica principal del programa.
"""

import sys
import os
from .gui import ImageConverterGUI


def main():
    """
    Función principal del programa.
    """
    print("¡Bienvenido al Convertidor de Extensiones de Imágenes!")
    print("Iniciando interfaz gráfica...")
    
    try:
        # Inicializar y ejecutar la interfaz gráfica
        app = ImageConverterGUI()
        app.run()
        
        print("Aplicación cerrada correctamente.")
        return 0
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrate de que todas las dependencias estén instaladas.")
        return 1
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 1


def run_console_mode():
    """
    Modo consola para el convertidor (alternativo).
    """
    print("\n=== MODO CONSOLA ===")
    print("Convertidor de Extensiones de Imágenes")
    print("Extensiones disponibles: .1, .2, .3, .4, .5, .6")
    
    from .image_converter import ImageConverter
    
    converter = ImageConverter()
    
    # Obtener carpeta de entrada
    folder = input("\nIngresa la ruta de la carpeta con imágenes: ").strip()
    if not folder or not os.path.exists(folder):
        print("Carpeta no válida.")
        return 1
    
    # Obtener archivos
    files = converter.get_image_files_from_folder(folder)
    if not files:
        print("No se encontraron imágenes en la carpeta.")
        return 1
    
    print(f"\nEncontradas {len(files)} imágenes:")
    for i, file_path in enumerate(files, 1):
        print(f"{i}. {os.path.basename(file_path)}")
    
    # Seleccionar extensión
    print(f"\nExtensiones disponibles: {', '.join(converter.TARGET_EXTENSIONS)}")
    target_ext = input("Ingresa la extensión de destino (ej: .1): ").strip()
    
    if target_ext not in converter.TARGET_EXTENSIONS:
        print("Extensión no válida.")
        return 1
    
    # Convertir archivos
    success, failed = converter.convert_multiple_files(files, target_ext)
    
    print(f"\n=== RESULTADOS ===")
    print(f"Archivos convertidos exitosamente: {success}")
    print(f"Archivos fallidos: {failed}")
    
    return 0


if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        exit(run_console_mode())
    else:
        exit(main())
