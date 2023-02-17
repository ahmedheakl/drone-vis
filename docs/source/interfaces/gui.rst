Graphical User Interface
========================

The library is built-in with **out-of-the box** GUI to easen the use of the proposed computer vision control,
and gives the user real-time, full access over their drone. The GUI is built with
`Tkinter <https://docs.python.org/3/library/tkinter.html>`_, for its ease-of-use and fast response and render.
Moreover, it is a cross-platform library allowing smoother integrations with platforms other than Ubuntu. 


Getting Started
---------------

To get started, just run the following command on your terminal:

.. code-block:: console

    $ dronevis-gui

This will open the following window, where you can *right-click* on any button to view its functionality. 

.. image:: ../guides/gui-main.png
  :width: 500
  :align: center
  :alt: GUI Sample Button Info


Structure
---------

The GUI is shipped as a class ``DroneVisGui``. 

.. autoclass:: dronevis.gui.main.DroneVisGui


Some parts are shipped as their own custom modules such as buttons and progress bars, which 
are then integrated later to build the GUI.


.. autoclass:: dronevis.gui.main_button.MainButton

.. autoclass:: dronevis.gui.image_button.ImageButton

.. autoclass:: dronevis.gui.image_bw_button.ImageBWButton

.. autoclass:: dronevis.gui.circular_progressbar.CircularProgressbar

Run GUI from Code 
-----------------

If you are not a terminal fan, you can your python script to the GUI: 

.. code-block:: python

    from dronevis.gui.main import DroneVisGui

    gui = DroneVisGui()     # create GUI instance 
    gui.window.mainloop()   # start GUI main loop