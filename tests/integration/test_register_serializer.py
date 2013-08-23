import urllib2
import vcr

class MockSerializer(object):
    def __init__(self):
        self.serialize_count = 0
        self.deserialize_count = 0
        self.load_args = None

    def deserialize(self, cassette_string):
        self.serialize_count += 1
        self.cassette_string = cassette_string
        return ([], [])

    def serialize(self, cassette_dict):
        self.deserialize_count += 1
        return ""

def test_registered_serializer(tmpdir):
    ms = MockSerializer()
    my_vcr = vcr.VCR()
    my_vcr.register_serializer('mock', ms)
    tmpdir.join('test.mock').write('test_data')
    with my_vcr.use_cassette(str(tmpdir.join('test.mock')), serializer='mock'):
        urllib2.urlopen('http://httpbin.org/')
        assert ms.serialize_count == 1 # Serializer deserialized once
        assert ms.cassette_string == 'test_data' # and serialized the test data string
        assert ms.deserialize_count == 0 # and hasn't serialized yet

    assert ms.serialize_count == 1



