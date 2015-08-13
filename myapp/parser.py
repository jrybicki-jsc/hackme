from xml.sax import ContentHandler


class TODOListHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.todos = list()
        self.current_date = None
        self.current_content = None
        self.chars = ''

    def startElement(self, name, attrs):
        self.chars = ''

    def endElement(self, name):
        if name == 'date':
            self.current_date = self.chars
        if name == 'content':
            self.current_content = self.chars
        if name == 'todo':
            self.todos.append([self.current_date, self.current_content])
            self.current_content = self.current_date = None

    def characters(self, content):
        self.chars += content

    def get_todos(self):
        return self.todos

if __name__ == "__main__":
    import xml.sax
    p = TODOListHandler()
    source = open('../todos2.xml')
    xml.sax.parse(source, p)
    print p.get_todos()