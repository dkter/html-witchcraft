from meta import PageMeta
import datetime

class Page(metaclass=PageMeta):
    def render(self):
        return ...[
            [html]
                [head]
                    [title] ("website page") [-title]
                [-head]
                [body]
                    [h1]
                        ("Current date")
                    [-h1]
                    [p] (datetime.datetime.now()) [-p]
                [-body]
            [-html]
        ]

p = Page()
print(p.render())
