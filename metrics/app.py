from .operations import Operations


class App:
    def __init__(self):
        self.register = {}

    def run(self):
        pass

    def subscribe(self, service, operations):
        for o in operations:
            if o not in self.register:
                self.register[o] = [service]
            else:
                self.register[o].append(service)

    def event(self, operation):
        if operation in self.register and len(self.register[operation]):
            for service in self.register[operation]:
                service.event(operation)


class BaseService:
    def event(self, op):
        try:
            getattr(self, "_%s" % op.name)()
        except AttributeError:
            raise Exception("Handler for {op} not implemented".format(op=op.name))


class Metrics(BaseService):
    def __init__(self):
        pass

    def _withdraw(self):
        pass


class AccountService(BaseService):
    def __init__(self):
        pass

    def _transfer(self):
        pass


def test_app():
    class DummyService:
        events = []

        def event(self, op):
            self.events.append(op)

    dummy = DummyService()

    app = App()
    app.subscribe(dummy, [Operations.transfer_operation])
    app.event(Operations.transfer_operation)

    assert Operations.transfer_operation == dummy.events[0]


def test_operation_handler_call():
    class DummyService(BaseService):
        call = False

        def _transfer_operation(self):
            self.call = True

    dummy = DummyService()

    app = App()
    app.subscribe(dummy, [Operations.transfer_operation])
    app.event(Operations.transfer_operation)

    assert True if dummy.call else False
