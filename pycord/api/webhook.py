







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

        if not hasattr(embeds, '__iter__'): # supports a list/tuple of embeds 
            embeds = [embeds]               # or a single embed

        payload['embeds'] = [em.to_dict() for em in embeds] 

        payload = json.dumps(payload, indent=4)

        return self.client.api.post(self.url, data=payload)
