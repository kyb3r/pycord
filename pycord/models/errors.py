

class HttpError(Exception):

    def __init__(self, response, data):
        self.response = response
        self.status = response.status_code
        self.reason = response.reason_phrase
        self.method = response.method
        self.code = data.get('code', 0)
        self.message = data.get('message', '')

        fmt = '{0.reason} ({0.status}): {0.message}'

        super().__init__(fmt.format(self))



