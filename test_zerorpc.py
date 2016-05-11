'''
import msgpack

def foo():
    json_data = '{"foo":23, "bar":5, "goop": "boop"}'
    binary_data = msgpack.packb(json_data)
    return msgpack.unpackb(binary_data)

if __name__ == '__main__':
    foo()

import zerorpc

class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()

'''

import zerorpc

class StreamingRPC(object):
    @zerorpc.stream
    def streaming_range(self, fr, to, step):
        return xrange(fr, to, step)

s = zerorpc.Server(StreamingRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
