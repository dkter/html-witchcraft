## html-witchcraft

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
