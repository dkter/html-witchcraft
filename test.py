from meta import PageMeta

class Page(metaclass=PageMeta):
    def render(self):
        a = "hello\n" + "world"
        return ...[
            [+html]
                [+head]
                    [+title] ["lol test"] [-title]
                [-head]
                [+body]
                    [+h1]
                        ["Value of a"]
                    [-h1]
                    [+p] [a] [-p]
                [-body]
            [-html]
        ]

p = Page()
print(p.render())
