#  Copyright (c) Meta Platforms, Inc. and affiliates.
#  All rights reserved.
#  This source code is licensed under the license found in the
#  LICENSE file in the root directory of this source tree.

from source import Source


class MarginCombinator(Source):
    """
    Esta clase maneja la combinación de dos fuentes (fondo y producto) con márgenes especificados.
    """

    def __init__(self, bg_source, front_source, margin_top=0, margin_left=0):
        """
        El constructor para la clase MarginCombinator.

        Parámetros:
            bg_source (Source): La fuente de la cual se obtiene la imagen de fondo.
            front_source (Source): La fuente de la cual se obtiene la imagen del producto.
            margin_top (int): El margen superior. El valor por defecto es 0.
            margin_left (int): El margen izquierdo. El valor por defecto es 0.

        Excepciones:
            ValueError: Si el margen excede el tamaño de la imagen de fondo.
        """
        self.bg_source = bg_source
        self.front_source = front_source
        self.margin_top = margin_top
        self.margin_left = margin_left

    def combine(self, bg_image, front_image):
        """
        Combina las imágenes de fondo y de producto con los márgenes especificados.

        Parámetros:
            bg_image (numpy array): La imagen de fondo.
            front_image (numpy array): La imagen del producto.

        Retorna:
            numpy array: La imagen combinada.
        """
        bg_shape = bg_image.shape
        front_shape = front_image.shape

        i = self.margin_left
        j = self.margin_top

        if bg_shape[0] < front_shape[0] + j or bg_shape[1] < front_shape[1] + i:
            raise ValueError("El margen excedería el tamaño de la imagen de fondo.")

        bg_image[j:j + front_image.shape[0], i:i + front_image.shape[1]] = front_image
        return bg_image

    def next_frame(self):
        """
        Genera el siguiente frame combinando las imágenes de fondo y de producto.

        Retorna:
            numpy array: El siguiente frame combinado.
        """
        bg_image = self.bg_source.next_frame()
        front_image = self.front_source.next_frame()
        return self.combine(bg_image, front_image)
