

class CheckedOnceEndpoint(object):

    checked_already = False

    def __init__(self, file_name):
        fixture = open(file_name)
        self.data = fixture.read()
        fixture.close()


class MockHttpClient(object):

    def __init__(self):
        self.endpoints = {
        'career': CheckedOnceEndpoint('tests/career.json'),
        'hero': CheckedOnceEndpoint('tests/hero.json'),
        'item': CheckedOnceEndpoint('tests/item.json')
    }

    

    def get(self, url):
        endpoint_name = self.resolve_url(url)
        endpont = self.endpoints[endpoint_name]
        if endpont.checked_already:
            raise Exception(endpoint_name +' already hit in this test')
        else:   
            endpont.checked_already = True
            data = endpont.data
            return MockResponse(data)

    def resolve_url(self, url):
        url_id = None
        if '/hero/' in url:
            url_id = 'hero'
        elif 'item' in url:
            url_id = 'item'
        else:
            url_id = 'career'
        return url_id


class MockResponse(object):

    def __init__(self, data):
        self.text = data
        self.status_code = 200
