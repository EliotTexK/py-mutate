# py-mutate
A utility that generates mutated python code. Used to generate logical and runtime errors.

mutation-candidates.py parses a python source file and generates a list of mutation points, suffixed with '.mut'. Mutation points uniquely represent nodes within the syntax tree (for example: assignment operator +=, at line 16, column 8). The generated file can be edited to remove undesired mutation points.

mutator.py takes a .mut file and expands it: outputing a .mutdb file, which contains possible code mutations for all mutation points specified. This file can also be edited to remove unwanted mutations.

Finally, mutation.py applies the .mutdb file to the original source code, dumping each variation to a 'mut' subdirectory.

# installation
You will need to install the astor module. This can be done easily with pip. Once you have, clone the repository and run the scripts in your terminal of choice.

# usage
To mutation-candidates.py, pass one argument: the name of python source file you would like to mess with. Edit the generated .mut file if desired.
To mutator.py, pass one argument: the name of the .mut file. Edit the resuting .mutdb file if desired.
To mutation.py, pass three arguments: the .mut file, the .mutdb file, and the name of the source file.
