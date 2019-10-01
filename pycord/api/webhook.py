"""
MIT License

Copyright (c) 2017 Kyb3r

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class Webhook:
    '''Simple webhook client.'''

    def __init__(self, client, **options):
        self.client = client
        self.url = options.get('url')
        self.username = options.get('username')
        self.avatar_url = options.get('avatar_url')

    def send(self, content=None, embeds=[], tts=False):
        '''Sends a message to the payload url'''

        if self.url is None:
            raise RuntimeError("url is not set!")

        payload = {
            'content': content,
            'username': self.username,
            'avatar_url': self.avatar_url,
            'tts': tts
        }
        
        if not hasattr(embeds, '__iter__'):  # supports a list/tuple of embeds
            embeds = [embeds]  # or a single embed

        payload['embeds'] = [em.to_dict() for em in embeds]

        payload = json.dumps(payload, indent=4)

        return self.client.api.post(self.url, data=payload)
