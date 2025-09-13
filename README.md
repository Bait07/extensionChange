# Convertidor de Extensiones de Imágenes

Un programa en Python que convierte las extensiones de imágenes a formatos personalizados (.1, .2, .3, .4, .5, .6) con una interfaz gráfica intuitiva.

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Configuración del ambiente

1. **Crear y activar el ambiente virtual:**
   ```bash
   # Crear ambiente virtual
   python -m venv venv
   
   # Activar ambiente virtual
   # En Windows:
   venv\Scripts\activate
   
   # En Linux/Mac:
   source venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Interfaz Gráfica (Recomendado)
```bash
# Ejecutar el programa principal con interfaz gráfica
python main.py
```

### Modo Consola
```bash
# Ejecutar en modo consola
python main.py --console
```

### Funcionalidades
- **Selección de archivos**: Selecciona imágenes individuales o carpetas completas
- **Formatos soportados**: JPG, PNG, BMP, GIF, TIFF, WEBP
- **Extensiones de destino**: .1, .2, .3, .4, .5, .6
- **Conversión masiva**: Procesa múltiples archivos simultáneamente
- **Organización automática**: Crea subcarpetas organizadas por extensión
- **Interfaz intuitiva**: GUI fácil de usar con barra de progreso avanzada
- **Manejo de archivos grandes**: Optimizado para carpetas de 200MB+ 
- **Progreso detallado**: Muestra porcentaje, tiempo estimado y archivo actual
- **Cancelación**: Opción para cancelar la conversión en cualquier momento
- **Mensajes de éxito**: Reportes detallados con estadísticas completas

## Estructura del proyecto

```
ExtensionChange/
├── main.py              # Punto de entrada principal
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Este archivo
├── venv/               # Ambiente virtual (no incluir en git)
├── src/                # Código fuente principal
│   ├── __init__.py
│   ├── app.py          # Aplicación principal
│   ├── image_converter.py  # Lógica de conversión
│   └── gui.py          # Interfaz gráfica
├── tests/              # Pruebas unitarias
├── docs/               # Documentación
└── data/               # Archivos de datos
```

## Desarrollo

### Ejecutar pruebas
```bash
pytest tests/
```

### Formatear código
```bash
black src/ tests/
```

### Verificar estilo de código
```bash
flake8 src/ tests/
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
