import ast
import sys

if len(sys.argv) != 2:
    raise Exception("usage: python3 mutation-candidates.py file_to_mutate.py")

# map operation nodes to their symbols
opText = {
    ast.Add      : "+",
    ast.Sub      : "-",
    ast.Mult     : "*",
    ast.Div      : "/",
    ast.FloorDiv : "//",
    ast.Mod      : "%",
    ast.Pow      : "**",
    ast.Eq       : "==",
    ast.NotEq    : "!=",
    ast.Lt       : "<",
    ast.LtE      : "<=",
    ast.Gt       : ">",
    ast.GtE      : ">=",
    ast.Is       : "is",
    ast.IsNot    : "is not",
    ast.In       : "in",
    ast.NotIn    : "not in",
    ast.UAdd     : "+",
    ast.USub     : "-",
    ast.Not      : "not",
    ast.And      : "and",
    ast.Or       : "or"
}

class CustomNodeVisitor(ast.NodeVisitor):
    currentFunction = ""    # name of current function is used in output
    nestedLevel = 0         # ignore functions not in module scope
    
    # begin output line with source line number, column number,
    # and module-scope function name (if it exists)
    def beginLine(self,node):
        line  = ""
        # add line and column number
        line += str(node.lineno) + " " + str(node.col_offset) + " "
        # end line and end column number are also required to uniquely
        # identify operators for when we re-parse the source tree!
        line += str(node.end_lineno) + " " + str(node.end_col_offset) + " "
        # add current (module-level) function
        if self.currentFunction == "":
            line += "<module> "
        else:
            line += self.currentFunction + "() "
        return line

    def visit_FunctionDef(self, node):
        functionName = ast.FunctionDef(node).name.name
        # are we in module scope?
        if self.nestedLevel == 0:
            self.currentFunction = functionName
        self.nestedLevel += 1
        self.generic_visit(node)
        self.nestedLevel -= 1
        # reset current function, but not when nested
        if self.nestedLevel == 0:
            self.currentFunction = ""
    
    def visit_BinOp(self, node):
        line = self.beginLine(node)
        # specify type of operation
        line += "ArithmeticOperator "   
        # add the operation in question
        line += opText[type(node.op)]
        mutFile.write(line)
        mutFile.write("\n")
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        line = self.beginLine(node)
        # specify type of operation
        line += "AssignmentOperator "  
        # add the operation in question
        line += opText[type(node.op)] + "="
        mutFile.write(line)
        mutFile.write("\n")
        self.generic_visit(node)

    # we can't change = to something like +=,
    # but we can change something like += to =
    
    def visit_Compare(self, node):
        line = self.beginLine(node)
        # don't allow in or not in due to potential errors
        if type(node.ops[0]) == ast.In or type(node.ops[0]) == ast.NotIn:
            pass # we may decide to mutate these separately later
        else:
            # specify type of operation
            line += "ComparisonOperator "
            # add the operation in question
            line += opText[type(node.ops[0])]
            mutFile.write(line)
            mutFile.write("\n")
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        line = self.beginLine(node)
        # specify type of operation
        line += "LogicalOperator "
        # add the operation in question
        line += opText[type(node.op)]
        mutFile.write(line)
        mutFile.write("\n")
        self.generic_visit(node)

# find output filenames
withExtension = sys.argv[1].split(".")
if len(withExtension) != 2:
    raise Exception("file extension should be .py")

noFileExtension = withExtension[0]

# record mutation candidates in this file:
mutFile = open(noFileExtension + ".mut",   "w")

mutFile.write(sys.argv[1] + "\n")
sourceFile = ast.parse(open(sys.argv[1]).read())

# recursively visit nodes in the AST
visitor = CustomNodeVisitor()
visitor.visit(sourceFile)

mutFile.close()