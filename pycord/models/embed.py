class Embed:
    '''Class that formats an embed'''
    __slots__ = (
        'color','title','url','author',
        'description','fields','image',
        'thumbnail','footer','timestamp',
        )
    
    def __init__(self, **kwargs):
        '''Initialises an Embed object'''
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.url = kwargs.get('title_url')
        self.description = kwargs.get('description')
        self.timestamp = kwargs.get('timestamp')
        self.fields = []
          
    def del_field(self, index):
        '''Deletes a field by index'''
        self.fields.pop(index)
        return self
      
    def add_field(self, name, value, inline=True):
        '''Adds a field'''
        field = {
            'name': name, 
            'value': value, 
            'inline': inline
            }
        self.fields.append(field)
        return self
    
    def set_author(self, name, icon_url=None, url=None):
        '''Sets the author of the embed'''
        self.author = {
            'name': name,
            'icon_url' : icon_url,
            'url' : url
            }
        return self
    
    def set_thumbnail(self, url):
        '''Sets the thumbnail of the embed'''
        self.thumbnail = {'url': url}
        return self
    
    def set_image(self, url):
        '''Sets the image of the embed'''
        self.image = {'url': url}
        return self
        
    def set_footer(self, text, icon_url=None):
        '''Sets the footer of the embed'''
        self.footer = {
            'text': text,
            'icon_url': icon_url
            }
        return self
    
    def to_dict(self):
        '''Turns the object into a dictionary'''
        return {
            key: getattr(self, key)
            for key in self.__slots__
            if hasattr(self, key) and getattr(self, key)
            }