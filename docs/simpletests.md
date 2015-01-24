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

As this suggests, `Broadcaster` and `Receiver` objects store the broadcaster they are registered to as a member variable and `Broadcaster` objects call the `broadcast` method of the `BroadcastManager` object they are registered to in order to broadcast their messages.


### First Test

For our first test, we will instantiate a `BroadcastManager`, register within it a fake `Broadcaster` instance and a fake `Receiver` instance, have the registered `Broadcaster` instance broadcast a message through the `BroadcastManager` instance, and check whether the message was correctly received by the registered `Receiver` instance. The test will pass if and only if the `Receiver` instance received the same message that the `Broadcaster` instance sent.

We begin by making our imports:
```
import unittest
import doppelganger

import BroadcastManager
```

We can now define and set up our test case:
```
class ExampleTest1(unittest.TestCase):
    def setUp(self):
        self.broadcast_manager = BroadcastManager.BroadcastManager()
        
        class FakeBroadcaster(BroadcastManager.Broadcaster):
            __metaclass__ = doppelganger.Doppel
        
        self.fake_broadcaster_class = FakeBroadcaster
        
        class FakeReceiver(BroadcastManager.Receiver):
            __metaclass__ = doppelganger.Doppel
        
        self.fake_receiver_class = FakeReceiver
        
        self.message = 'lol'
	self.message_received = 'lol'
```

`self.broadcast_manager` is the `BroadcastManager` instance that will be the target of the test. `self.message` is the message that will be transmitted. The real work here is being done to define the `self.fake_broadcaster_class` and `self.fake_receiver_class` classes. Let us consider the `self.fake_broadcaster_class` definition. It starts by defining the `FakeBroadcaster` class:
```
class FakeBroadcaster(BroadcastManager.Broadcaster):
    __metaclass__ = doppelganger.Doppel
```

This is the basic pattern of use for the doppelganger module. If you want to create fake objects which emulate instances of a given Class, you have to instantiate them as instances of the class:
```
class FakeClass(Class):
    __metaclass__ = doppelganger.Doppel
```

Once this is done, you can instantiate a `FakeClass` object which doubles a `Class` object with the same signatures you would employ when creating the `Class` object. Observe the exact same pattern was repeated in the definition of `FakeReceiver`.

We bind these classes to the `fake_broadcaster_class` and `fake_receiver_class` attributes so that we can easily create fake broadcasters and receivers in our tests.

With the `setUp` complete, let us consider what our test should look like. Ideally, we would like to insert our assertion into the `receive` method of our fake receiver without having to worry about the fake receiver's internal state. But this is easily done by monkey patching a callback to `self.assertEqual` into the receiver's `receive` attribute:
```
def test_broadcast(self):
    def fake_broadcast(obj, message):
	    self.broadcast_manager.broadcast(obj, message)
	
	broadcaster = self.fake_broadcaster_class()
    doppelganger.tools.monkey_patch(broadcaster, 'broadcast', fake_broadcast)
    
	def fake_receive(obj, message):
		self.assertEqual(message, self.message_received)
    
	receiver = self.fake_receiver_class()
	doppelganger.tools.monkey_patch(receiver, 'receive', fake_receive)
	
	self.broadcast_manager.broadcasters.append(broadcaster)
	self.broadcast_manager.receivers.append(receiver)
	broadcaster.broadcast(self.message)
```

The real test is in these four lines of code:
```
def fake_receive(obj, message):
	self.assertEqual(message, self.message_received)

receiver = self.fake_receiver_class()
doppelganger.tools.monkey_patch(receiver, 'receive', fake_receive)
```

Incidentally, this could have been even more easily achieved in two lines using the `patch_caller` function in `doppelganger.tools`:
```
receiver = self.fake_receive_class()
doppelganger.tools.patch_caller(receiver, 'receive', lambda message: self.assertEqual(message, self.message_received))
```

That's it! This test broadcasts the message `'lol'` across the broadcast manager and passes if and only if `'lol'` is received by the registered receiver.


### Second Test

The above test could have been conducted almost as easily without using doppelganger. The nice thing about doppelganger is that it allows you to selectively preserve some of the state of the object you are mocking, and to do so easily. Consider the `NamedBroadcaster` and `AdvancedBroadcastManager` classes in [BroadcastManager.py](../samples/simpletests/BroadcastManager.py). `NamedBroadcaster` adds a `handle` attribute to the `Broadcaster` class, and `AdvancedBroadcastManager` prepends a broadcaster's handle to its message before sending it to its registered receivers.

```
def NamedBroadcaster(Broadcaster):
    def __init__(self, handle):
        self.handle = handle


def AdvancedBroadcastManager(BroadcastManager):
    def broadcast(self, obj, message):
        new_message = obj.handle + ': ' + message
        super(AdvancedBroadcastManager, self).broadcast(obj, message)
```

We can perform the same test using these classes as we did above with only minor changes to the `setUp`:
```
class ExampleTest2(ExampleTest1):
    def setUp(self):
        self.broadcast_manager = BroadcastManager.AdvancedBroadcastManager()
        
        class FakeBroadcaster(BroadcastManager.NamedBroadcaster):
            __metaclass__ = doppelganger.Doppel
        
        self.fake_broadcaster_class = FakeBroadcaster
        self.fake_broadcaster_class.declare_untouchable('handle')
        
        class FakeReceiver(BroadcastManager.Receiver):
            __metaclass__ = doppelganger.Doppel
        
        self.fake_receiver_class = FakeReceiver
        
        self.message = 'lol'
        self.message_received = 'bob: lol'
```

The key difference, besides the explicit addition of the default handle, is the following line of code:
```
self.fake_broadcaster_class.declare_untouchable('handle')
```
This line specifies that, when instantiating a fake `NamedBroadcaster` instance, the `handle` attribute should be preserved.

This example is meant to give a taste of how doppelganger can be used to rigorously test systems with very complicated chains of dependency. I will elaborate on this in future guides.

- - -

[Back to README](../README.md)
