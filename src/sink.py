#  Copyright (c) Meta Platforms, Inc. and affiliates.
#  All rights reserved.
#  This source code is licensed under the license found in the
#  LICENSE file in the root directory of this source tree.

import source, cv2
from moviepy.editor import VideoFileClip, AudioFileClip

class Sink():
    """
    Clase para crear un video a partir de una fuente y agregar audio si se proporciona.
    """

    TEMP_FILE = ""

    def __init__(self, source: source.Source, target_fps=60, time=15, output_video_path="sample.mp4", temp_file_path=""):
        """
        Inicializa la clase Sink con la fuente, fps objetivo, duración y ruta de salida del video.

        Parámetros:
            source (source.Source): La fuente de los frames para el video.
            target_fps (int, opcional): Los frames por segundo objetivo para el video. Por defecto es 60.
            time (int, opcional): La duración del video en segundos. Por defecto es 15.
            output_video_path (str, opcional): La ruta de salida para el video. Por defecto es "sample.mp4".
            temp_file_path (str, opcional): La ruta del archivo temporal.
        """
        self.source = source
        self.target_fps = target_fps
        self.time = time
        self.output_video_path = output_video_path
        Sink.TEMP_FILE = temp_file_path

    def _add_audio(self, audio_path):
        """
        Agrega audio al video utilizando la ruta de audio proporcionada.

        Parámetros:
            audio_path (str): La ruta al archivo de audio.
        """
        # Define dos clips, uno de video y uno de audio
        video_clip = VideoFileClip(Sink.TEMP_FILE)
        audio_clip = AudioFileClip(audio_path)

        # Combina los dos clips
        final_clip = video_clip.set_audio(audio_clip)

        # Guarda el video final con audio
        final_clip.write_videofile(self.output_video_path)

    def create_video(self, audio_path=None):
        """
        Crea un video a partir de la fuente y agrega audio si se proporciona.

        Parámetros:
            audio_path (str, opcional): La ruta al archivo de audio. Si no se proporciona, no se agregará audio.
        """
        output_video_path = Sink.TEMP_FILE if audio_path else self.output_video_path

        source = self.source
        target_fps = self.target_fps
        time = self.time

        img = source.next_frame()
        height, width = img.shape[:2]

        # Inicializa el VideoWriter de OpenCV
        vw = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), target_fps, (width, height))

        if not vw.isOpened():
            raise Exception("OpenCV no puede reconocer el códec utilizado por el video temporal.")

        # Escribe los frames en el video
        for fr in range(time * target_fps):
            vw.write(img)
            img = source.next_frame()

        vw.release()

        # Agrega el audio si se proporciona una ruta de audio
        if audio_path:
            self._add_audio(audio_path)
