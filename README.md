
# Cuy traductor

Un traductor de documentos Word minimalista elaborado con Python y GTK 3 (PyGObject)


## Captura
![](https://i.ibb.co/C5MhpRW/cuytrad-mainview.png)


## Características

### Servicios de traducción
- Papago
- Kakao
- Google

### Lenguages soportados
- Koreano
- Español
- Inglés

## Instalación

### Requisitos previos

Descargar e instalar [**MSYS2**](https://www.msys2.org/), sigue las instrucciones de su página.

Abrir la consola `MSYS2 MinGW 32-bit` y ejecutar la siguiente línea.

```bash
pacman -S mingw-w64-i686-gtk3 mingw-w64-i686-glade mingw-w64-i686-python3-gobject mingw-w64-i686-python3-pip mingw-w64-i686-python-lxml
```

Luego las librerías Python necesarias para este proyecto

```bash
pip install python-docx googletrans kakaotrans
```

Descargar este repositorio o clonarlo con Git.

```bash
git clone https://github.com/sirdeniel/CuyTraductor.git
```

### Ejecución

#### Método 1:
- Abrir la carpeta de este proyecto con la consola `MSYS2 MinGW 32-bit`.

- Ejecutar esta línea.
  ```bash
  python cuytraductor.py
  ```

#### Método 2:
- Abrir la carpeta con Visual Studio Code y aprobar la confianza.
- `F1` en el teclado, escribir Python y entrar en `Python: Run Python file in terminal`.

