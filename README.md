# Creador de plantillas de vídeo


Este marco le permite crear plantillas de video personalizadas utilizando imágenes estáticas y metadatos, lo que hace que sea más fácil y eficiente producir contenido de video a mayor escala.

## Diseño

Este marco utiliza un enfoque basado en extracción para recopilar fotogramas de diversas fuentes y combinarlos según lo previsto. El modelo es sencillo: implica el uso de implementaciones de la clase "Fuente". Como usuario final, usted es responsable de crear versiones personalizadas de estas clases (si aún no se proporcionan) y administrar su uso.

![Diseño de muestra](diseño-de muestra.png)

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

## Muestra

`main.py` contiene un ejemplo de uso simple para estas clases. Este caso de uso de muestra extrae tres imágenes de la web y crea una presentación de diapositivas con una imagen de fondo.

- Los logotipos de Instagram y Facebook se utilizan para crear una presentación de diapositivas en bucle.
- El logo de WhatsApp se utiliza como imagen de fondo.

El componente de presentación de diapositivas tiene unas dimensiones de 550x550, mientras que el fondo (y el vídeo final) tiene unas dimensiones de 700x700. El componente de presentación de diapositivas se centra mediante un combinador de márgenes.

El fondo también podría ser un vídeo sin cambiar la API, pero en este ejemplo estamos usando una imagen estática.

Este caso de uso de muestra podría enriquecerse con creatividades personalizadas y crear un guión que cree presentaciones de diapositivas de productos y marcos personalizados que mejoren la identidad de la marca.

## Licencia
Este proyecto tiene licencia MIT, como se encuentra en el archivo LICENCIA.
