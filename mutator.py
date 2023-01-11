import sys

if len(sys.argv) != 2:
    raise Exception("usage: python3 mutator.py mutfile.mut")

# which symbols are interchangeable without generating an error message?
arithmetic = {"+","-","*","/","%","**","//"}
assignment = {"=","+=","-=","*=","/=","%=","//=","**="}
comparison = {"==", "!=", ">", "<", ">=", "<=", "is", "is not"}
logical    = {"and", "or"}
unary      = {"+", "-", "not"}

# what are each of these operator classes called in the file itself?
fileSyntax2Symbols = {
    "ArithmeticOperator" : arithmetic,
    "AssignmentOperator" : assignment,
    "ComparisonOperator" : comparison,
    "LogicalOperator"    : logical,
}

# parse CLI args, setup files

withExtension = sys.argv[1].split(".")
if len(withExtension) != 2:
    raise Exception("file extension should be .mut")

mutFileName   = sys.argv[1]
mutDBFileName = sys.argv[1] + "db"

mutFile   = open(mutFileName, "r")
mutDBFile = open(mutDBFileName, "w")

# generate .mutdb file from .mut file

sourceFileName = mutFile.readline() # first line is source file name
i1 = 0 # first unique identifier for mutated filename
for line in mutFile.readlines():
    data    = line.split(" ")
    symbol  = data[-1][:-1] # remove trailing newline character
    opClass = data[-2]
    # get valid replacement symbols
    replacementSymbols = fileSyntax2Symbols[opClass].copy()
    replacementSymbols.remove(symbol)
    i2 = 0 # second unique identifier for mutated filename
    for replacement in replacementSymbols:
        line  = " ".join(data[:-1]) + " " + symbol + " " + replacement + " "
        line += str(i1) + "-" + str(i2) + "-" + sourceFileName
        mutDBFile.write(line)
        i2 += 1
    i1 += 1

mutFile.close()
mutDBFile.close()