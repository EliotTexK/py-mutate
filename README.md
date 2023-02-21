# py-mutate
A utility that generates mutated python code. Used to generate logical and runtime errors.

mutation-candidates.py parses a python source file and generates a list of mutation points, suffixed with '.mut'. Mutation points uniquely represent nodes within the syntax tree (for example: assignment operator +=, at line 16, column 8). The generated file can be edited to remove undesired mutation points.

mutator.py takes a .mut file and expands it: outputing a .mutdb file, which contains possible code mutations for all mutation points specified. This file can also be edited to remove unwanted mutations.

Finally, mutation.py applies the .mutdb file to the original source code, dumping each variation to a 'mut' subdirectory.
