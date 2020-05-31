## html-witchcraft

### FAQ

#### What does it do?

See for yourself -

```python
from witchcraft import Page
class ExamplePage(Page):
    def render(self):
        return ...[
            [html]
                [head]
                    [title] ("My Cool Website") [-title]
                [-head]
                [body]
                    [marquee][h1] ("Wheeeeeeeeee") [-h1][-marquee]
                [-body]
            [-html]
        ]

page = ExamplePage()
print(page.render())
```

```
$ python test.py
<html><head><title>My Cool Website</title></head><body><marquee><h1>Wheeeeeeeeee</h1></marquee></body></html>
```

(see another example at [example.py](https://github.com/dkter/html-witchcraft/blob/master/example.py)!)

#### what the heck

I'm glad you enjoyed it.

#### Should I use this?

Probably not. This was mainly intended as a fun project and proof of concept to see the extent of what I could do with metaprogramming in Python. Most people probably don't know this is possible!
Obviously this doesn't have as many features as, say, [jinja2](https://palletsprojects.com/p/jinja/) or [dominate](https://github.com/Knio/dominate) and I haven't tried to break it at all so there may be vulnerabilities somewhere. It's just cool.

#### But how does it work?

I might post a full technical explanation later. In the meantime, have a look at [witchcraft.py](https://github.com/dkter/html-witchcraft/blob/master/witchcraft.py). It's pretty well documented.
