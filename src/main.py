#  Copyright (c) Meta Platforms, Inc. and affiliates.
#  All rights reserved.
#  This source code is licensed under the license found in the
#  LICENSE file in the root directory of this source tree.

from source import *      # Importa los módulos necesarios para la fuente de medios
from combinator import *  # Importa los módulos necesarios para combinar medios
from sink import *        # Importa los módulos necesarios para guardar el video
import os, requests, shutil  # Importa módulos estándar de Python para manejo de archivos y solicitudes HTTP

# Función para descargar archivos de internet y guardarlos localmente
def download(url, file_name_no_ext):
    response = requests.get(url, stream=True)  # Hace una solicitud HTTP GET al URL
    file_ext = response.headers['Content-Type'].split('/')[1]  # Obtiene la extensión del archivo del encabezado HTTP
    if response.status_code == 200:  # Verifica si la solicitud fue exitosa
        file_name = os.path.join(f"{file_name_no_ext}.{file_ext}")  # Construye el nombre del archivo con la extensión
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)  # Guarda el contenido del archivo en el sistema local
        return file_name  # Devuelve la ruta del archivo guardado
    del response  # Elimina la respuesta para liberar recursos

# URLs de imágenes para descargar
fb_logo = "https://raw.githubusercontent.com/Valentinol0/Imagenes/main/zapatilla2.png"
ig_logo = "https://github.com/Valentinol0/Imagenes/blob/main/zapatilla1.png?raw=true"
tw_logo = "https://github.com/Valentinol0/Imagenes/blob/main/remera.png?raw=true"
cd_logo = "https://github.com/Valentinol0/Imagenes/blob/main/underArmor.png?raw=true"
fd_logo=  "https://github.com/Valentinol0/Imagenes/blob/main/botin1.png?raw=true"


image_urls = [fb_logo, ig_logo, tw_logo, cd_logo, fd_logo]  # Lista de URLs de imágenes
image_paths = []  # Lista para almacenar las rutas de las imágenes descargadas

# Define el directorio temporal dependiendo del sistema operativo
temp_path = "/tmp" if os.name == 'posix' else f"{os.path.expanduser('~')}/AppData/Local/Temp"

# Descarga las imágenes y almacena las rutas en image_paths
for i, url in enumerate(image_urls):
    file_name = download(url, f"{temp_path}/{i}")
    image_paths.append(file_name)

# Crea una fuente de presentación de diapositivas con las imágenes 
slideshow_source = ImageSlideshowSource(
    image_paths,                # Lista de rutas de imágenes locales
    dimensions=(500, 500),      # Dimensiones de las imágenes combinadas
    standby_time=4,             # Tiempo que se muestra una imagen completa
    transition_time=0.5,          # Tiempo de transición entre imágenes
    target_fps=60,              # Fotogramas por segundo objetivo
    left_bound_white=True,      # Inicia con una imagen blanca
    right_bound_white=False,    # No termina con una imagen blanca
    min_time=35                 # Repite las imágenes hasta alcanzar los 15 segundos
)

# URL de una imagen de fondo
wa_logo = "https://github.com/Valentinol0/Imagenes/blob/main/Dise%C3%B1o%20sin%20t%C3%ADtulo%20(1).jpg?raw=true"
wa_image_path = download(wa_logo, f"{temp_path}/bg")

# Crea una fuente de imagen única para la imagen de fondo
bg_source = SingleMediaSource(
    wa_image_path,
    resolution=(720, 720)
)

# Combina la imagen de fondo con la presentación de diapositivas
combinator_source = MarginCombinator(
    bg_source=bg_source,
    front_source=slideshow_source,
    margin_top=100,
    margin_left=115
)

# URL de un archivo de audio
audio_url = "https://github.com/Valentinol0/Audios1/raw/main/running-it-down-everet-almond_1O7eGw6H%20(1).mp3"
audio_path = download(audio_url, f"{temp_path}/audio")

# Configura el sink para crear el video
sink = Sink(
    source=combinator_source,
    target_fps=60,
    time=20,
    output_video_path="sample.mp4",
    temp_file_path=f"{temp_path}/tmp.mp4"
)

# Crea el video con el audio incorporado
sink.create_video(audio_path)
