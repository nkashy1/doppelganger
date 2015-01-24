import unittest
import doppelganger

import BroadcastManager


class BroadcastManagerTest(unittest.TestCase):
    
    class FakeBroadcaster(BroadcastManager.Broadcaster):
        __metaclass__ = doppelganger.Doppel
    
    
    class FakeReceiver(BroadcastManager.Receiver):
        __metaclass__ = doppelganger.Doppel
    
    
    def setUp(self):
        self.broadcast_manager = BroadcastManager.BroadcastManager()
        self.message = 'lol'
    
    
    def test_single_broadcaster_single_receiver(self):
        fake_broadcaster = self.make_fake_broadcaster()
        self.add_fake_broadcaster_broadcast(fake_broadcaster)
        self.add_fake_broadcaster_register(fake_broadcaster)
        
        fake_receiver = self.make_fake_receiver()
        self.add_fake_receiver_receive(fake_receiver)
        self.add_fake_receiver_register(fake_receiver)
        
        fake_broadcaster.register(self.broadcast_manager)
        fake_receiver.register(self.broadcast_manager)
        
        fake_broadcaster.broadcast(self.message)
    
    
    def perform_test_m_broadcasters_n_receivers(self, m, n):
        broadcasters = map(lambda j: self.make_fake_broadcaster(), range(m))
        receivers = map(lambda j: self.make_fake_receiver(), range(n))
        
        map(self.add_fake_broadcaster_register, broadcasters)
        map(self.add_fake_broadcaster_broadcast, broadcasters)
        map(lambda broadcaster: broadcaster.register(self.broadcast_manager), broadcasters)
        
        map(self.add_fake_receiver_register, receivers)
        map(self.add_fake_receiver_receive, receivers)
        map(lambda receiver: receiver.register(self.broadcast_manager), receivers)
        
        for j in range(m):
            self.message = str(j)
            broadcasters[j].broadcast(self.message)
    
    
    def test_1_broadcaster_2_receivers(self):
        self.perform_test_m_broadcasters_n_receivers(1, 2)
    
    
    def test_10_broadcasters_100_receivers(self):
        self.perform_test_m_broadcasters_n_receivers(10, 100)
    
    
    def test_register_broadcaster(self):
        fake_broadcaster = self.make_fake_broadcaster()
        self.add_fake_broadcaster_register(fake_broadcaster)
        fake_broadcaster.register(self.broadcast_manager)
    
    
    def test_register_broadcaster_twice(self):
        fake_broadcaster = self.make_fake_broadcaster()
        self.add_fake_broadcaster_register(fake_broadcaster)
        fake_broadcaster.register(self.broadcast_manager)
        fake_broadcaster.register(self.broadcast_manager)
        self.assertEqual(len(self.broadcast_manager.broadcasters), 1)
    
    
    def test_deregister_unregistered_broadcaster(self):
        fake_broadcaster = self.make_fake_broadcaster()
        self.assertRaises(Exception, self.broadcast_manager.deregister_broadcaster, fake_broadcaster)
    
    
    def test_deregister_registered_broadcaster(self):
        fake_broadcaster = self.make_fake_broadcaster()
        self.add_fake_broadcaster_register(fake_broadcaster)
        fake_broadcaster.register(self.broadcast_manager)
        self.broadcast_manager.deregister_broadcaster(fake_broadcaster)
        self.assertEqual(self.broadcast_manager.broadcasters, [])
    
    
    def test_register_receiver(self):
        fake_receiver = self.make_fake_receiver()
        self.add_fake_receiver_register(fake_receiver)
        fake_receiver.register(self.broadcast_manager)
    
    
    def test_register_receiver_twice(self):
        fake_receiver = self.make_fake_receiver()
        self.add_fake_receiver_register(fake_receiver)
        fake_receiver.register(self.broadcast_manager)
        fake_receiver.register(self.broadcast_manager)
        self.assertEqual(len(self.broadcast_manager.receivers), 1)
    
    
    def test_deregister_unregistered_receiver(self):
        fake_receiver = self.make_fake_receiver()
        self.assertRaises(Exception, self.broadcast_manager.deregister_receiver, fake_receiver)
    
    
    def test_deregister_registered_receiver(self):
        fake_receiver = self.make_fake_receiver()
        self.add_fake_receiver_register(fake_receiver)
        fake_receiver.register(self.broadcast_manager)
        self.broadcast_manager.deregister_receiver(fake_receiver)
        self.assertEqual(self.broadcast_manager.receivers, [])
    
        
    def make_fake_broadcaster(self):
        fake_broadcaster = self.FakeBroadcaster()
        return fake_broadcaster
    
    
    def add_fake_broadcaster_broadcast(self, fake_broadcaster):
        def fake_broadcast(obj, message):
            obj.broadcast_manager.broadcast(obj, message)
        
        doppelganger.tools.monkey_patch(fake_broadcaster, 'broadcast', fake_broadcast)
    
    
    def add_fake_broadcaster_register(self, fake_broadcaster):
        def fake_register(obj, broadcast_manager):
            registration_result = broadcast_manager.register_broadcaster(obj)
            self.assertEqual(registration_result, broadcast_manager)
            obj.broadcast_manager = self.broadcast_manager
        
        doppelganger.tools.monkey_patch(fake_broadcaster, 'register', fake_register)
    
    
    def make_fake_receiver(self):
        fake_receiver = self.FakeReceiver()
        return fake_receiver
    
    
    def add_fake_receiver_receive(self, fake_receiver):
        def fake_receive(obj, message):
            self.assertEqual(message, self.message)
        
        doppelganger.tools.monkey_patch(fake_receiver, 'receive', fake_receive)
    
    
    def add_fake_receiver_register(self, fake_receiver):
        def fake_register(obj, broadcast_manager):
            registration_result = broadcast_manager.register_receiver(obj)
            self.assertEqual(registration_result, broadcast_manager)
            obj.broadcast_manager = self.broadcast_manager
        
        doppelganger.tools.monkey_patch(fake_receiver, 'register', fake_register)



# TEST RUNNER

if __name__ == '__main__':
    cases = (BroadcastManagerTest,)
    
    suite = unittest.TestSuite()
    
    for test_case in cases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
    
    unittest.TextTestRunner(verbosity = 2).run(suite)