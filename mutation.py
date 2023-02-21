import os
import sys
import ast
import astor
import copy

if len(sys.argv) != 4:
    raise Exception("usage: python3 mutation.py mutfile.mut mutdbfile.mutdb source.py")

# map symbols to potential replacement operations
arithmetic = {
    "+"      : ast.Add(),
    "-"      : ast.Sub(),
    "*"      : ast.Mult(),
    "/"      : ast.Div(),
    "//"     : ast.FloorDiv(),
    "%"      : ast.Mod(),
    "**"     : ast.Pow(),
}

assignment = {
    "="       : ast.Assign(),
    "+="      : ast.Add(),
    "-="      : ast.Sub(),
    "*="      : ast.Mult(),
    "/="      : ast.Div(),
    "//="     : ast.FloorDiv(),
    "%="      : ast.Mod(),
    "**="     : ast.Pow(),
}

comparison = {
    "=="     : ast.Eq(),
    "!="     : ast.NotEq(),
    "<"      : ast.Lt(),
    "<="     : ast.LtE(),
    ">"      : ast.Gt(),
    ">="     : ast.GtE(),
    "is"     : ast.Is(),
    "is not" : ast.IsNot(),
    "in"     : ast.In(),
    "not in" : ast.NotIn(),
}

logical = {
    "and"    : ast.And(),
    "or"     : ast.Or()
}

listSubscript = {
    "[]"     : ast.List(),
    "[+1]"   : ast.List(),
    "[-1]"   : ast.List(),
    "[*2]"   : ast.List(),
    "[//2]"  : ast.List()
}

fileSyntax2Ops = {
    "ArithmeticOperator" : arithmetic,
    "AssignmentOperator" : assignment,
    "ComparisonOperator" : comparison,
    "LogicalOperator"    : logical,
    "ListSubscript"      : listSubscript
}

# parse CLI args:
# first arg should be the .mutdb file
# second arg should be the source code to be mutated
mutFile    = open(sys.argv[1], "r")
mutDBFile  = open(sys.argv[2], "r")
sourceFile = open(sys.argv[3], "r")

# make dir to store mutated source files:
if not os.path.isdir("mut"):
    os.mkdir("mut")

# keep nodes stored in memory
sourceStr = sourceFile.read()
rootNode  = astor.parse_file(sys.argv[3])
nodes     = [node for node in ast.walk(rootNode)]

# nodes are uniquely identified with starting and ending positions
# many-to-one relation between .mutdb entries and nodes,
# we map the 4-column composite primary key with a dict.
# If the .mutdb file does not match the source, this will fail!
nodeDict = dict() # nodeKey maps to node

# find valid keys (correspond to the operations we want to mutate)
validKeys = set() # set of nodeKeys

mutFile.readline() # first line is the source filename
for line in mutFile.readlines():
    data = line.split(" ")
    validKeys.add((int(data[0]), int(data[1]), int(data[2]), int(data[3])))

# build the dictionary mapping keys to nodes
for node in nodes:
    if hasattr(node, "lineno"): # does the node correspond to actual source code?
        key = (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)
        if key in validKeys:
            nodeDict[key] = node

# for each line in the .mutdb file
# use nodeDict to find the corresponding node
# temporarily replace the node with the mutant
# use astor to write the mutated source file
# return the node to its previous state
for dbline in mutDBFile.readlines():
    data = dbline.split(" ")
    key  = ((int(data[0]), int(data[1]), int(data[2]), int(data[3])))
    if key in validKeys and key in nodeDict.keys():
        node = nodeDict[key]
        temp = copy.deepcopy(node)

        # lookup replacement op using previously defined dicts
        replacement = fileSyntax2Ops[data[5]][data[7]]
        if hasattr(node, "op"):
            node.op = replacement
        elif hasattr(node, "ops"):
            node.ops[0] = replacement

        with open("mut" + os.path.sep + data[-1][:-1], "w") as mutant:
            # for some reason, astor likes to add newlines where they don't belong
            mutant.write(astor.to_source(rootNode).replace("\n\n", "\n"))
        
        if hasattr(node, "op"):
            node.op = temp.op
        elif hasattr(node, "ops"):
            node.ops[0] = temp.ops[0]

mutFile.close()
mutDBFile.close()
sourceFile.close()