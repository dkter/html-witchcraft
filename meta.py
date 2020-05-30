import inspect
import copy

def get_snippets(src):
    start = 0
    while start < len(src):
        start = src.find("...[", start)
        nestlevel = 1
        end = start + 4
        while nestlevel > 0:
            end += 1
            if end >= len(src):
                return
            if src[end] == "[":
                nestlevel += 1
            elif src[end] == "]":
                nestlevel -= 1
        yield slice(start, end + 1)
        start = end


def get_bracket_pairs(src):
    # TODO: this assumes brackets are formed correctly
    start = 0
    while start < len(src):
        start = src.find("[", start)
        if start == -1: return
        end = src.find("]", start)
        yield slice(start, end + 1)
        start = end


class PageMeta(type):

    @staticmethod
    def _replace(src):
        newsrc = list(src)
        for snippet in get_snippets(src):
            code = src[snippet]
            code = code.lstrip("...[").rstrip("]")
            html = ""
            args = []
            for bracketpair in get_bracket_pairs(code):
                obj = code[bracketpair]
                obj = obj.lstrip("[").rstrip("]")
                if obj[0] == '+':
                    html += f"<{obj[1:]}>"
                elif obj[0] == '-':
                    html += f"</{obj[1:]}>"
                else:
                    html += f"{{{len(args)}}}" # TODO: escape this preliminarily
                    args.append(obj)
            arglist = ''.join(["["] + [item + "," for item in args] + ["]"])
            newsrc[snippet] = f'"""{html}""".format(*{arglist})' # TODO: stuff will get moved around

        modified = ''.join(newsrc).strip()
        mod = compile(modified, "<string>", "exec")
        ns = {}
        exec(mod, ns)
        return ns["render"]

    def __new__(cls, name, bases, dct):
        if "render" in dct:
            src = inspect.getsource(dct["render"])
            dct["render"] = cls._replace(src)
        return super().__new__(cls, name, bases, dct)
