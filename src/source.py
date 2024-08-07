#  Copyright (c) Meta Platforms, Inc. and affiliates.
#  All rights reserved.
#  This source code is licensed under the license found in the
#  LICENSE file in the root directory of this source tree.

import cv2
import numpy as np

class Source:
    """
    Clase base para representar una fuente de medios. Define un método abstracto next_frame que debe ser 
    implementado por las subclases para devolver el siguiente cuadro de la fuente.
    """

    def next_frame():
        """
        Calcula según sea necesario y devuelve el siguiente cuadro de la fuente.

        Returns:
            np.ndarray: El siguiente cuadro de la fuente como un array con forma (altura, ancho, canal de color).
        """
        pass


class SingleMediaSource(Source):
    """
    Clase utilizada para representar un único recurso creativo, sin modificaciones ni efectos añadidos.
    Esta clase maneja tanto entradas de imágenes como de videos y permite saltar cuadros para alcanzar una 
    tasa de fotogramas deseada para los videos. También proporciona una opción para repetir el video desde 
    el principio o congelarlo en el último cuadro cuando termina.
    """

    def __init__(self, video_path, resolution=(720, 720), target_fps=None, on_end_loop=True):
        """
        Constructor para la clase SingleMediaSource.

        Parameters:
            video_path (str): Ruta del archivo de video o imagen.
            resolution (tuple): La resolución deseada a la que se redimensiona el recurso. Predeterminado es (720, 720).
            target_fps (int): La tasa de fotogramas deseada para los recursos de video. Predeterminado es 60.
            on_end_loop (bool): Si es True, repite el video desde el principio cuando termina. Si es False, se congela en el último cuadro. 
                                Predeterminado es True.
        """
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)
        self.source_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.target_fps = target_fps
        self.fps_factor = 1 if target_fps is None else int(self.target_fps / self.source_fps)
        self.resolution = resolution
        self.count = 0
        self.last_frame = None
        self.ret = True
        self.on_end_loop = on_end_loop

    def next_frame(self):
        """
        Ajusta la tasa de fotogramas del video a la deseada y devuelve el siguiente cuadro de la fuente.
        """

        if self.count % self.fps_factor != 0:
            self.count += 1
            return self.last_frame

        ret, frame = self.cap.read()

        if ret:
            self.last_frame = frame
        elif self.cap.get(cv2.CAP_PROP_FRAME_COUNT) > 1 and self.on_end_loop:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, self.last_frame = self.cap.read()

        self.count += 1
        self.last_frame = cv2.resize(self.last_frame, self.resolution)
        return self.last_frame


class ImageSlideshowSource(Source):
    """
    Clase utilizada para producir una presentación de diapositivas en movimiento entre imágenes.
    Esta clase maneja una lista de rutas de imágenes locales y crea la presentación de diapositivas.
    Permite configurar el tiempo de espera para cada imagen, el tiempo de transición entre imágenes y 
    los fotogramas por segundo objetivo.
    """

    def __init__(self, img_paths, dimensions=(550, 550), standby_time=3, transition_time=1, target_fps=60, left_bound_white=True, right_bound_white=False, min_time=23):
        """
        Constructor para la clase ImageSlideshowSource.

        Parameters:
            img_paths (list): Lista de rutas de archivos de imágenes locales.
            dimensions (tuple): Las dimensiones deseadas a las que se redimensionan las imágenes. Predeterminado es (550, 550).
            standby_time (int): El tiempo que cada imagen se muestra completamente en segundos. Predeterminado es 3.
            transition_time (int): El tiempo para la transición entre imágenes en segundos. Predeterminado es 1.
            target_fps (int): Los fotogramas por segundo deseados para la presentación de diapositivas. Predeterminado es 60.
            left_bound_white (bool): Si es True, inicia la presentación de diapositivas con una imagen blanca. Predeterminado es True.
            right_bound_white (bool): Si es True, termina la presentación de diapositivas con una imagen blanca. Predeterminado es False.
            min_time (int): El tiempo mínimo para la presentación de diapositivas en segundos. Predeterminado es 15.
        """
        super().__init__()
        self.imgs = [cv2.imread(path) for path in img_paths]
        self.imgs = [cv2.resize(img, dimensions) for img in self.imgs]

        expected_imgs = 1 + int(min_time / (standby_time + transition_time))
        self.imgs = [self.imgs[i % len(self.imgs)] for i in range(expected_imgs)]

        self.standby_time = standby_time
        self.transition_time = transition_time
        self.target_fps = target_fps
        self.count = 0
        self.next_img_idx = 0

        white_img = np.ones_like(self.imgs[0]) * 255

        if left_bound_white:
            self.imgs = [white_img] + self.imgs

        if right_bound_white:
            self.imgs = self.imgs + [white_img]

        self.is_transitioning = True
        self.state_count = 0

    def _left_transition(img1, img2, alpha):
        """
        Realiza una transición hacia la izquierda entre dos imágenes.

        Parameters:
            img1 (numpy array): La primera imagen.
            img2 (numpy array): La segunda imagen.
            alpha (float): El factor de transición, un float entre 0 y 1. Cuanto mayor sea el valor, más visible será la segunda imagen.

        Returns:
            numpy array: La imagen resultante después de realizar la transición hacia la izquierda. Mismo tamaño que las imágenes de entrada.
        """

        if img1.shape != img2.shape:
            raise ValueError("Las imágenes de entrada deben tener el mismo tamaño.")

        cut = int(alpha * img1.shape[1])
        res = np.zeros_like(img1)
        res[:, :img1.shape[1] - cut] = img1[:, cut:]
        res[:, img1.shape[1] - cut:] = img2[:, :cut]
        return res

    def next_frame(self):
        """
        Devuelve el siguiente cuadro en la presentación de diapositivas.
        Este método maneja las transiciones entre imágenes y el tiempo de espera para cada imagen.
        """

        # Máquina de estados simple para controlar la transición entre imágenes
        if self.is_transitioning and self.state_count == self.transition_time * self.target_fps:
            self.state_count = 0
            self.is_transitioning = False
            self.next_img_idx = min(self.next_img_idx + 1, len(self.imgs) - 1)

        if not self.is_transitioning and self.state_count == self.standby_time * self.target_fps:
            self.state_count = 0
            self.is_transitioning = True

        self.count += 1
        self.state_count += 1

        if self.is_transitioning and self.next_img_idx < len(self.imgs) - 1:
            alpha = self.state_count / (self.transition_time * self.target_fps)
            return ImageSlideshowSource._left_transition(self.imgs[self.next_img_idx], self.imgs[self.next_img_idx + 1], alpha)
        else:
            return self.imgs[self.next_img_idx]
