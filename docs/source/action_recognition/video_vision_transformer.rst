Video Vision Transformer (ViViT)
================================

Four different architectures of video transformers are proposed in `here <https://arxiv.org/abs/2103.15691>`_ based on four different factorization techniques
of spatiotemporal features. In the first variation (Spatiotemporal attention), the transformer encoder accepts different spatiotemporal portions of the
video, performing joint space-time attention without factorization. In the second variation (Factorized encoder), a spatial transformer is applied first for
all frames in a video, and then a temporal transformer deals with the learned encoding of each spatial transformer. In the third variation
(Factorized self-attention), a similar approach to the first variation is applied but with factorization into spatial attention and temporal attention. In
the final variation (Factorized dot-product attention), the factorization is applied to the multi-head dot-product attention operation. The first variation
has the highest inference cost and achieves the best results on the `Kinetics-400 dataset <https://arxiv.org/abs/1705.06950>`_. On the other hand, the second 
variation has the minimal inference cost compared to the other variations, with a slight decrease in accuracy compared to the first variation.

.. image:: action_recognition.png
    :width: 80%
    :align: center
    :alt: Video Vision Transformer (ViViT) Inference

Example
-------

    .. code-block:: python

        from dronevis.models import ActionRecognizer

        model = ActionRecognizer()
        model.load_model("google")
        model.detect_webcam()
