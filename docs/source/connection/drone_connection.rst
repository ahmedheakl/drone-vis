
Drone Connection
================

The library is built with abstraction schemes in mind. You can have full control over your drone by specifying the exact desired commands as methods on a :doc:`drone` instance. 

Main Structure
--------------

Each connection type either command, video, or navigation data is implemented as itsown `thread <https://docs.python.org/3/library/threading.html>`_ for faster and more real-time feel. Each thread initializes a connection with a port specific to that thread:

- **Commands    Port** = 5556
- **Video       Port** = 5555
- **Navigation  Port** = 5554

For each thread to start the communication - sends commands or receive data, it must ``acquire`` the *socket_lock*.
After the desired are executed, the thread must ``release`` the socket_lock back.

Command Connection
------------------

You can create a drone instace, and initiate a connection with the drone with a two lines of code. 

.. code-block:: python

    from dronevis import Drone

    drone = Drone() # create drone instance
    drone.connect() # initiate drone connection on IP 192.168.1.1

This will print ``Connected successfully`` or ``Could not connect to drone``. You can see that the code is minimal if you want abstraction. 

Here is a small test with multiple control instructions: 

.. code-block:: python
    :emphasize-lines: 5, 6, 8, 10, 11
    
    from dronevis import Drone

    drone = Drone()
    drone.connect()
    drone.set_config(max_altitude=50) # set maximum height to 50m
    drone.takeoff() # drone takeoff
    sleep(1)      # wait for one second
    drone.hover()   # drone hover still inplace
    sleep(1)      
    drone.land()    # drone lands smoothly
    drone.stop()    # stop drone connection

Video Connection
----------------

You can acquire the video stream as follows: 

.. code-block:: python
    :emphasize-lines: 4

    from dronevis import Drone
    
    drone = Drone()
    drone.connect_video() # initialize video stream 

It initializes the video stream, and creates an ``opencv`` window with video stream. You can exit the stream by pressing ``q``.

Navigation Data Connection
--------------------------

You can retrieve the navigation data such as elevation, vx, vy, ... etc, by providing a callbacks for handling incomining. 
For example, you can create a callback ``print_navdata``, and bind it to the incoming navdata. The function simply prints after each pre-defined period: 

.. code-block:: python
    :emphasize-lines: 3, 4, 8, 9

    from dronevis import Drone

    def print_navdata(navdata) -> None:
        print(navdata)

    drone = Drone()
    drone.connect()
    drone.set_config(activate_gps=True, activate_navdata=True) # activate navdata
    drone.set_callback(print_navdata) # bind callback
    sleep(5)      # wait for 5 seconds
    drone.stop()

