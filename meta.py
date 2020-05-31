import ast
import inspect
import textwrap


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
        element = node.elts[0]
        if (isinstance(element, ast.UnaryOp) and
            isinstance(element.op, ast.USub)):      # the unary - operator, used for ending tags
            self.html = f"</{element.operand.id}>" + self.html
        else:
            self.html = f"<{element.id}>" + self.html


    def visit_Subscript(self, node):
        if (isinstance(node.slice, ast.UnaryOp) and
            isinstance(node.slice.op, ast.USub)):     # the unary - operator, used for ending tags
            self.html = f"</{node.slice.operand.id}>" + self.html
        elif isinstance(node.slice, ast.Name):
            self.html = f"<{node.slice.id}>" + self.html            
        elif (isinstance(node.slice.value, ast.UnaryOp) and
            isinstance(node.slice.value.op, ast.USub)):     # compatibility between <=3.8 and 3.9
            self.html = f"</{node.slice.value.operand.id}>" + self.html
        else:
            self.html = f"<{node.slice.value.id}>" + self.html
        self.visit(node.value)


    def visit_Call(self, node):
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
            # generates something like the following Python code:
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
        if "render" in dct:
            src = inspect.getsource(dct["render"])
            src = textwrap.dedent(src)
            tree = RenderableFunctionTransformer().visit(ast.parse(src))
            tree = ast.fix_missing_locations(tree)
            #print(ast.unparse(tree))
            mod = compile(tree, "<ast>", "exec")
            ns = dct["render"].__globals__
            exec(mod, ns)
            dct["render"] = ns["render"]
        return super().__new__(cls, name, bases, dct)
