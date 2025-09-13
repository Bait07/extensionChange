"""
Módulo para conversión de extensiones de imágenes.
Convierte imágenes a extensiones personalizadas (.1, .2, .3, .4, .5, .6)
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple
from PIL import Image


class ImageConverter:
    """
    Clase para convertir extensiones de imágenes.
    """
    
    # Extensiones de imagen soportadas
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    # Extensiones de destino disponibles
    TARGET_EXTENSIONS = ['.1', '.2', '.3', '.4', '.5', '.6']
    
    def __init__(self):
        """Inicializar el convertidor."""
        self.converted_files = []
        self.failed_files = []
    
    def is_image_file(self, file_path: str) -> bool:
        """
        Verificar si un archivo es una imagen válida.
        
        Args:
            file_path: Ruta del archivo a verificar
            
        Returns:
            bool: True si es una imagen válida, False en caso contrario
        """
        try:
            path = Path(file_path)
            return path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        except Exception:
            return False
    
    def get_image_files_from_folder(self, folder_path: str) -> List[str]:
        """
        Obtener lista de archivos de imagen de una carpeta.
        
        Args:
            folder_path: Ruta de la carpeta
            
        Returns:
            List[str]: Lista de rutas de archivos de imagen
        """
        image_files = []
        try:
            folder = Path(folder_path)
            if not folder.exists():
                return image_files
            
            for file_path in folder.iterdir():
                if file_path.is_file() and self.is_image_file(str(file_path)):
                    image_files.append(str(file_path))
        except Exception as e:
            print(f"Error al leer carpeta: {e}")
        
        return sorted(image_files)
    
    def convert_single_file(self, source_path: str, target_extension: str) -> bool:
        """
        Convertir un solo archivo a la nueva extensión.
        Crea automáticamente una subcarpeta con el nombre de la extensión.
        
        Args:
            source_path: Ruta del archivo original
            target_extension: Nueva extensión (ej: '.1', '.2', etc.)
            
        Returns:
            bool: True si la conversión fue exitosa, False en caso contrario
        """
        try:
            source = Path(source_path)
            
            if not source.exists():
                print(f"Archivo no encontrado: {source_path}")
                return False
            
            if not self.is_image_file(source_path):
                print(f"No es un archivo de imagen válido: {source_path}")
                return False
            
            # Verificar que la nueva extensión sea válida
            if target_extension not in self.TARGET_EXTENSIONS:
                print(f"Extensión de destino no válida: {target_extension}")
                return False
            
            # Crear subcarpeta con el nombre de la extensión
            subfolder_name = target_extension[1:]  # Quitar el punto inicial (.1 -> 1)
            output_dir = source.parent / subfolder_name
            output_dir.mkdir(exist_ok=True)
            
            # Crear ruta del archivo de destino
            target_path = output_dir / f"{source.stem}{target_extension}"
            
            # Copiar el archivo con la nueva extensión
            shutil.copy2(source_path, target_path)
            
            self.converted_files.append({
                'original': source_path,
                'converted': str(target_path),
                'extension': target_extension,
                'subfolder': str(output_dir)
            })
            
            print(f"✓ Convertido: {source.name} -> {subfolder_name}/{target_path.name}")
            return True
            
        except Exception as e:
            print(f"Error al convertir {source_path}: {e}")
            self.failed_files.append({
                'file': source_path,
                'error': str(e)
            })
            return False
    
    def convert_multiple_files(self, file_paths: List[str], target_extension: str) -> Tuple[int, int]:
        """
        Convertir múltiples archivos a la nueva extensión.
        Crea automáticamente subcarpetas organizadas por extensión.
        
        Args:
            file_paths: Lista de rutas de archivos
            target_extension: Nueva extensión
            
        Returns:
            Tuple[int, int]: (archivos convertidos exitosamente, archivos fallidos)
        """
        self.converted_files = []
        self.failed_files = []
        
        success_count = 0
        total_files = len(file_paths)
        
        print(f"\nIniciando conversión de {total_files} archivos...")
        print(f"Extensión de destino: {target_extension}")
        print(f"Los archivos se guardarán en subcarpetas organizadas por extensión.")
        print("-" * 60)
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"[{i}/{total_files}] Procesando: {Path(file_path).name}")
            
            if self.convert_single_file(file_path, target_extension):
                success_count += 1
        
        failed_count = total_files - success_count
        
        print("-" * 60)
        print(f"Conversión completada:")
        print(f"✓ Exitosos: {success_count}")
        print(f"✗ Fallidos: {failed_count}")
        
        # Mostrar información sobre las subcarpetas creadas
        if self.converted_files:
            subfolders = set(item['subfolder'] for item in self.converted_files)
            print(f"\nSubcarpetas creadas:")
            for subfolder in sorted(subfolders):
                print(f"  📁 {subfolder}")
        
        return success_count, failed_count
    
    def get_conversion_summary(self) -> dict:
        """
        Obtener resumen de la última conversión.
        
        Returns:
            dict: Resumen con archivos convertidos y fallidos
        """
        return {
            'converted': self.converted_files,
            'failed': self.failed_files,
            'total_converted': len(self.converted_files),
            'total_failed': len(self.failed_files)
        }


def main():
    """
    Función principal para pruebas del módulo.
    """
    converter = ImageConverter()
    
    # Ejemplo de uso
    print("Convertidor de Extensiones de Imágenes")
    print("Extensiones soportadas:", ", ".join(converter.SUPPORTED_EXTENSIONS))
    print("Extensiones de destino:", ", ".join(converter.TARGET_EXTENSIONS))


if __name__ == "__main__":
    main()
