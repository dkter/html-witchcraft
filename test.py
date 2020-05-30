from meta import PageMeta

class Page(metaclass=PageMeta):
    def render(self):
        return ...[
            [html]
                [head]
                    [title] ["lol test"] [-title]
                [-head]
                [body]
                    [h1]
                        ["Simple math"]
                    [-h1]
                    [p] [0.1 + 0.2] [-p]
                [-body]
            [-html]
        ]

p = Page()
print(p.render())
