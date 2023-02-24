.. currentmodule:: dronevis.drone_connect.command

Command Thread
==============

Thread resposible for sending control information/instructions to drone socket ``port=5556``. 

Sending Commands
----------------

Sending commands is implemented using the interface provided by the drones manufacturers. You can send as in the following example for ``land`` instruction: 

.. code-block:: python

    socket.send("AT*REF=#ID#," + "290717696" + "\r")

Refer to the `official documentation <https://www.parrot.com/en/support/documentation/ar-drone>`_ for more details.


Command Class
-------------

.. autoclass:: Command