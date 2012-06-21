

class MockHttpClient(object):

    checked_heros_already = False

    def get(self, url):
        fixture = None
        if '/hero/' in url:
            if not self.checked_heros_already:
                fixture = open('tests/hero.json')
                self.checked_heros_already = True
            else:
                raise Exception('Hero endpoint checked twice')
        else:
            fixture = open('tests/career.json')
        data = fixture.read()
        fixture.close()
        return MockResponse(data)


class MockResponse(object):

    def __init__(self, data):
        self.text = data
        self.status_code = 200
