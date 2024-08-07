# Creador de plantillas de vídeo


Este marco le permite crear plantillas de video personalizadas utilizando imágenes estáticas y metadatos, lo que hace que sea más fácil y eficiente producir contenido de video a mayor escala.

## Diseño

Este marco utiliza un enfoque basado en extracción para recopilar fotogramas de diversas fuentes y combinarlos según lo previsto. El modelo es sencillo: implica el uso de implementaciones de la clase "Fuente". Como usuario final, usted es responsable de crear versiones personalizadas de estas clases (si aún no se proporcionan) y administrar su uso.


## Implementación

Este repositorio contiene archivos que se pueden ampliar para implementaciones personalizadas.

- `source.py` contiene la definición básica de la clase `Source` y ejemplos de implementaciones de `ImageSlideshowSource` y `SingleMediaSource`.

- `combinator.py` contiene una subclase `Source` de ejemplo que combina otras dos fuentes para formar una sola. Es importante tener en cuenta que los "Combinadores" también son "Fuentes" en sí mismos y pueden combinarse aún más con otras "Fuentes". Se colocan en un archivo diferente por razones de segregación de responsabilidades.

- `sink.py` extrae fotogramas de una única fuente final para crear un archivo de salida `.mp4`. También admite la adición de archivos de audio.


## Requisitos

Para garantizar un espacio de trabajo limpio y evitar posibles conflictos entre dependencias, se recomienda encarecidamente utilizar un entorno virtual. También puedes saltar directamente al paso 3.

1. El siguiente comando crea un nuevo entorno virtual llamado `myenv`.

```golpecito
python -m venv myenv
```

2. Una vez creado el entorno, puedes activarlo usando:

```golpecito
myenv\Scripts\activate
```

3. Situarnos en el directorio para instalar las dependencias:

```golpecito
cd C:\Users\pc\Downloads\Script\video-template-builder-main
```

```golpecito
python -m pip install -r requirements.txt
```

Este comando instala todos los paquetes enumerados en el archivo `requirements.txt` en su entorno activo.

4 Nos colocamos en el src y ejecutamos el main:

```golpecito
cd src
```

```golpecito
python main.py
```

## Cosas a tener en cuenta:
Las imagenes principales, de fondo o audios deben ser precargados anteriormente en un repositorio o sitio web.
Formato:

Imagenes: PNG.

Imagenes de fondo: JPG.

Audios: MP3.

Al agregar una mayor cantidad de imagenes principales debe ser menor el tiempo de transicion de las mismas(transicion time).


## Caso de prueba:
Se obtiene como salida un sample.mp4 el cual contiene imagenes ya precargadas con su fondo y audio referidas en este caso a productos de la marca new sport.

## Licencia
Este proyecto tiene licencia MIT, como se encuentra en el archivo LICENCIA.
