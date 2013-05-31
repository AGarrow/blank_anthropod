import pdb


class DebugMiddleWare:

    def process_request(self, request):
        pdb.set_trace()
