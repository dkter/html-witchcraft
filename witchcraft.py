"""
html-witchcraft
not your typical python HTML generator

copyright (c) 2020 David Teresi

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""


import ast
import inspect
import textwrap


def exclude(func):
    "Decorator applied to methods to not run through the HTML generator."
    func.__dict__["exclude"] = True
    return func


class HTMLSyntaxError(Exception):
    pass


class HTMLTagGenerator(ast.NodeVisitor):
    """
    Parses the expression inside square brackets into an HTML tag.
    """
    def __init__(self):
        self.tag = ""
        self.args = []


    def generate(self, node):
        self.visit(node)
        return self.tag, self.args


    def visit_Index(self, node):
        self.visit(node.value)


    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            self.tag = f"</{node.operand.id}>"
        else:
            raise HTMLSyntaxError("Invalid HTML tag")


    def visit_Name(self, node):
        self.tag = f"<{node.id}>"


    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise HTMLSyntaxError("Invalid HTML tag")

        self.tag = f"<{node.func.id}"
        for kw in node.keywords:
            self.tag += f" {kw.arg}=\"{{}}\""
            self.args.append(kw.value)
        self.tag += ">"


class HTMLGenerator(ast.NodeVisitor):
    """
    Parses HTML-generating syntax into HTML.
    """
    def __init__(self):
        self.html = ""
        self.args = []


    def generate(self, node):
        self.visit(node)
        return self.html, self.args


    def visit_List(self, node):
        "A list is typically used as the first HTML tag in a document."
        element = node.elts[0]
        if (isinstance(element, ast.UnaryOp) and
            isinstance(element.op, ast.USub)):
            # the unary - operator is used for ending tags
            self.html = f"</{element.operand.id}>" + self.html
        else:
            self.html = f"<{element.id}>" + self.html


    def visit_Subscript(self, node):
        "Subscripts are used for opening and closing HTML tags."
        tag, args = HTMLTagGenerator().generate(node.slice)
        self.html = tag + self.html
        self.args = args + self.args
        self.visit(node.value)


    def visit_Call(self, node):
        "Calls are used for embedding Python expressions."
        self.html = "{}" + self.html
        if len(node.args) <= 1:
            self.args.insert(0, node.args[0])
        else:
            # There are commas in the bracketed statement, so turn it into a tuple
            # This won't work with 1-length tuples with single commas, because this
            # is being parsed as an arguments list and the comma is irrelevant
            tup = ast.Tuple(
                elts=node.args,
                ctx=ast.Load()
            )
            self.args.insert(0, tup)
        self.visit(node.func)


class RenderableFunctionTransformer(ast.NodeTransformer):
    """
    A NodeTransformer applied to a function with embedded syntax for
    generating HTML.
    """
    def visit_Subscript(self, node):
        """
        If the object being subscipted is the Ellipsis object (...), then this
        method will convert everything inside the subscript to HTML.
        """
        if isinstance(node.value, ast.Ellipsis):
            html_generator = HTMLGenerator()
            html_code, args = html_generator.generate(node.slice)
            # Generates something like the following Python code:
            # html_code.format(*args)
            # more literally: str.format(html_code, *args)
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='str', ctx=ast.Load()),
                    attr='format',
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value=html_code),
                    *args
                ],
                keywords=[]
            )
        else:
            return node


class PageMeta(type):
    def __new__(cls, name, bases, dct):
        for key, val in dct.items():
            if callable(val) and "exclude" not in val.__dict__:
                # Get function source
                src = inspect.getsource(val)
                src = textwrap.dedent(src)

                # Transform function
                tree = RenderableFunctionTransformer().visit(ast.parse(src))
                tree = ast.fix_missing_locations(tree)

                # Compile into new function
                mod = compile(tree, "<ast>", "exec")
                ns = val.__globals__
                exec(mod, ns)

                # Replace the function in the class dict
                dct[key] = ns[val.__name__]
        return super().__new__(cls, name, bases, dct)


class Page(metaclass=PageMeta):
    "Simple class to make subclassing more intuitive"
