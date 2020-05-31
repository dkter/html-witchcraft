from witchcraft import Page
import datetime

class ExamplePage(Page):
    def render_list(self):
        ul = ...[ [ul] ]
        for i in range(10):
            ul += ...[ [li] (i) [-li] ]
        ul += ...[ [-ul] ]
        return ul

    def render(self):
        return ...[
            [html]
                [head]
                    [title] ("website page") [-title]
                [-head]
                [body]
                    [img (src="https://www.python.org/static/community_logos/python-logo-generic.svg", alt="Python logo")]
                    [h1]
                        ("Current date")
                    [-h1]
                    [p] (datetime.datetime.now()) [-p]
                    (self.render_list())
                [-body]
            [-html]
        ]

p = ExamplePage()
print(p.render())
