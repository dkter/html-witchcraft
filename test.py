from witchcraft import Page
import datetime

class ExamplePage(Page):
    def render(self):
        return ...[
            [html]
                [body]
                    [a (href="#")] ("hi") [-a]
                [-body]
            [-html]
        ]

p = ExamplePage()
print(p.render())
