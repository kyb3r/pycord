

string = '''Hello there "My name is bob well hi there" yo " doodle bob "
I have got a codeblock here:
```py
async with ctx.session.get(url) as resp:
    async def resp_handler(resp.json):
        perform.db.execfile(json)
```'''


class ArgLex:
    def __init__(self, string):
        self.string = string
        self.is_quoted = False
        self.args = []
        self.current = ''
        self._quote = '"'
        self.index = 0
    
    def reset(self):
        arg = self.current.strip(' "') if not self.is_quoted else self.current
        self.args.append(arg)
        self.current = ''
    
    def return_arg(self):
        x = self.current
        self.current = ''
        return x
    
    @property
    def end_of_line(self):
        return self.index == len(self.string)

    @property
    def char(self):
        return self.string[self.index]

    @property
    def on_quote(self):
        return self.char == self._quote

    @property
    def on_escape(self):
        return self.char == '\\'

    def get_arg(self):
        while not self.end_of_line:
            if self.char.isspace() or self.end_of_line:
                if self.is_quoted:
                    self.current += self.char
                else:
                    return self.return_arg()
            if self.on_escape and not self.end_of_line:
                if self.string[self.index+1] == '"':
                    self.index += 2
                    continue
            if self.on_quote:
                self.is_quoted = not self.is_quoted
            self.current += self.char
            self.index += 1
        return self.return_arg()

    
    def get_args(self):
        while not self.end_of_line:
            if self.char.isspace() or self.end_of_line:
                if self.is_quoted:
                    self.current += self.char
                else:
                    self.reset()
            if self.on_escape and not self.end_of_line:
                if self.string[self.index+1] == '"':
                    self.index += 2
                    continue
            if self.on_quote:
                self.is_quoted = not self.is_quoted
            self.current += self.char
            self.index += 1
        self.reset()
        return self.args


lex = ArgLex(string)
print(lex.get_arg())
print(lex.get_arg())
print(lex.get_arg())
print(lex.get_arg())
print(lex.get_arg())
