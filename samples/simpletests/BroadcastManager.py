class BroadcastManager(object):
    def __init__(self):
        self.broadcasters = []
        self.receivers = []
    
    def register_broadcaster(self, broadcaster):
        if not (broadcaster in self.broadcasters):
            try:
                self.broadcasters.append(broadcaster)
            except:
                return None
        
        return self
    
    def deregister_broadcaster(self, broadcaster):
        try:
            self.broadcasters.remove(broadcaster)
        except:
            raise
    
    def register_receiver(self, receiver):
        if not (receiver in self.receivers):
            try:
                self.receivers.append(receiver)
            except:
                return None
        
        return self
    
    def deregister_receiver(self, receiver):
        try:
            self.receivers.remove(receiver)
        except:
            raise
    
    def broadcast(self, broadcaster, message):
        if broadcaster in self.broadcasters:
            for receiver in self.receivers:
                receiver.receive(message)


class Broadcaster(object):
    def __init__(self):
        self.broadcast_manager = None
    
    def request_registration(self, broadcast_manager):
        pass
    
    def request_deregistration(self):
        pass
    
    def broadcast(self, message):
        pass


class Receiver(object):
    def __init__(self):
        self.broadcast_manager = None
    
    def request_registration(self, broadcast_manager):
        pass
    
    def request_deregistration(self):
        pass
    
    def receive(self, message):
        pass