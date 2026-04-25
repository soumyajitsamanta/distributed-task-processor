# Introduction:
Distributed processing uses ESP boards, micropython and network connection to
setup the ESP boards as distributed workers nodes. These workers can perform
tasks which are given by the user and return the result back to the user. For
now the project does not have encryption and certificate management and proper
authentication so users will have to decide how to secure them.

# Goal:
Setup a cluster of inexpensive ESP boards and use that cluster to perform distributed tasks.

Components of cluster:
1. User machine                     : The machine from which user connects to the workers, assigns tasks and gets the result.
1. Orchestrator ESP Board           : A single ESP board to connect to the worker nodes and perform cluster and device management.
1. Worker nodes                     : The ESP boards which will be doing the actual tasks.
1. Network                          : The connection over wifi, usb or any other networking technology which will be used by worker and user to cluster.

# Overview of the working:

1. Finds all worker boards and ensure they have micropython firmware and the `main.py` file in them.
1. Note down the ESP Now peer name for all boards. Put this in orchestrator peers array.
1. Start all worker nodes to be connected to the cluster.
1. The workers boot up and start with ESP Now communication receiver loop.
1. Start orchestrator and connects to it (for now serial usb connection)
1. Use orchestrator to connect all workers to a wifi network.
1. Checks if all workers connected to the WIFI and fix any problems workers may face.
1. Note down the ip address of all the workers.
1. Uses orchestrator to start the socket server for all workers.
1. Dispatches task through socket requests to the IP addresses noted above. Get the result in response.

# Adding tasks capabilities to workers

In the present scenario only task supported is `get_version` which gets the version of
the file deployed.
This is used to see what version of worker is deployed. Users will need to add their
task in the `performTask` method in the handler section same as where `get_version` is
present.

The section inside `performTask` is as seen below.
```python
    # All handlers for task actions
    if action == 'get_version':
        return json.dumps({"version": VERSION})
    
    if action == 'new_task':            # Like this
        result = doUserTask(payload)    # Similar to this
        return json.dumps(result)       # Return result to be sent back in response.
```

# Making requests to worker for task

Since the workers use socket for communication anybody can send and receive
using any language and device it can be user machine, orchestrator or worker
nodes themselves. A sample way to send task using java is below.

## Using Java to send request to socket server
```java
  public static void main(String[] args) throws IOException {
    String ipOfDevice = "IP OF DEVICE YOU SEE IN ROUTER"
    Socket s = new Socket();
    SocketAddress endpoint = new InetSocketAddress(ipOfDevice, 8000);
    s.connect(endpoint, 10000);
    s.setKeepAlive(true);
    
    OutputStream outputStream = s.getOutputStream();
    outputStream.write("{\"action\":\"get_version\"}".getBytes());
    InputStream inputStream = s.getInputStream();
    byte[] bytes = inputStream.readAllBytes();

    System.err.println(new String(bytes));
  }
```

# Advantages And Disadvantages

## Advantages:

- Uses micropython and python for declaring tasks and that is accessible to most people.
- Uses socket connection so simple and easy to connect to from most devices and most languages.
- Easy setup for starting cluster and connecting to network.

## Disadvantages:

- Using micropython and python is slower than native C,C++ and other compiled outputs.
- Uses ESP Now protocol, so other boards which do not have ESP Now will not work without modification to this program.

# TODO
- Add encryption, authentication and authorization.
- Add more default tasks other than `get_version`

# Disclaimer:

User is responsible for going through the program and its capabilites to find out if it is safe for their use or not.
The developer(s) are not responsible for any damages caused by use of this project for now. This is provided as is.

It is in its initial phase of development so it will have minimal functionalities.
