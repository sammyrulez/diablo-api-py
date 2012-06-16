

class MockHttpClient(object):
    def get(self, url):
        fixture = None
        if '/hero/' in url:
            fixture = open('tests/hero.json')
        else:
            fixture = open('tests/career.json')
        data = fixture.read()
        fixture.close()
        return MockResponse(data)


class MockResponse(object):

    def __init__(self, data):
        self.text = data
        self.status_code = 200
