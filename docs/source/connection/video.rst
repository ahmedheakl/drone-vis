.. currentmodule:: dronevis.drone_connect.video

Video Thread
==============

Thread resposible for retrieving video stream from drone socket ``port=5555``. 

Video Specs
-----------

The video can run on **25 fps** (frame per second) with a latency of **~2ms**. The video stream is acquired using ``tcp`` protocol, for integral data transmission. The video is then decoded using ``opencv``, and viewed in real-time fashion. You can close the view window by pressing ``q``. 
See the following example for retrieving a video stream from a drone connection instance:

.. code-block:: python
    
    drone = Drone() # create drone instance
    drone.connect_video() # initialize video stream 

Refer to the `official documentation <https://www.parrot.com/en/support/documentation/ar-drone>`_ for more details.


Command Class
-------------

.. autoclass:: VideoThread