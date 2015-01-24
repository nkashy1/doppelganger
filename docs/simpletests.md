# Simple Unit Tests
*Author: Neeraj Kashyap (nkashy1@gmail.com)*

In this guide, I will show you how to use doppelganger with Python's [unittest](https://docs.python.org/2/library/unittest.html) module to test a simple broadcasting system.


### The broadcasting system

Our [broadcasting system](../samples/simpletests/BroadcastManager.py) consists of three classes -- `BroadcastManager`, `Broadcaster`, and `Receiver`.

Each `BroadcastManager` object is responsible for:

1. registering `Broadcaster` and `Receiver` objects in their respective roles,

2. handling the communications from its registered `Broadcaster` objects to its registered `Receiver` objects,

3. deregistering each of its registered objects when requested to do so.

Each `Broadcaster` and `Receiver` object has the ability to:

1. request registration to a single `BroadcastManager` object,

2. send or receive messages to the `BroadcastManager` object it is registered to, depending on whether it is a `Broadcaster` or a `Receiver` respectively,

3. request deregistration from the `BroadcastManager` object it is registered to.



- - -

[Back to README](../README.md)