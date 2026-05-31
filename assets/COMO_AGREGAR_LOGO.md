# Cómo agregar el logo de la Universidad Señor de Sipán

La portada (`docs/portada.md`) ya está lista y **referencia el logo** en `assets/logo_uss.png`.
Solo falta depositar el archivo de imagen (no se puede guardar desde el chat).

## Pasos

1. Guarda la imagen del logo que tienes (la que pegaste) como archivo **PNG**.
2. Colócalo exactamente en:
   ```
   C:\Users\DELL\Documents\0.10.1 Tesis Francisco\assets\logo_uss.png
   ```
   (el nombre debe ser `logo_uss.png`, en minúsculas).
3. Listo: la portada y cualquier documento que use esa ruta mostrarán el logo.

## Si lo descargas del sitio oficial
La versión vectorial/oficial suele estar en la web institucional de la USS. Para impresión en
tesis, prefiere un PNG de buena resolución (≥ 300 px de ancho) o un SVG.

## Para usar el logo en LaTeX (si compilas la tesis en LaTeX)
```latex
\includegraphics[width=4cm]{assets/logo_uss.png}
```

## Para usar el logo en los notebooks (encabezado de reportes)
```python
from IPython.display import Image
Image('../assets/logo_uss.png', width=150)
```

> Nota de uso: el logo institucional es propiedad de la Universidad Señor de Sipán; empléalo solo
> conforme a las normas gráficas de la universidad para documentos académicos.
