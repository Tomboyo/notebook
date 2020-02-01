#!/usr/bin/ptython3
#
# Consumes a list of pairs of arguments indcating that the first document makes
# a reference to the second, then appends a References section to the end of any
# document that was referenced indicating what referenced it.
#
# Also accumulates those references into target/reference-graph.adoc, which is
# compiled into a directed graph of the notebook.
#
# See bin/precompile

import sys

# Get everything after the script name
args = sys.argv[1::]

# Each key of the map is a document that has been referenced by another.
# Each value is a set of those referencing documents.
mapping = {}
for src, ref in zip(args[::2], args[1::2]):
    mapping.setdefault(ref, set([])).add(src)

# Append a "References" section, which contains links back to those external
# documents making reference to the document we are modifying.
for k, v in mapping.items():
    filename = "target/pre/" + k + ".adoc"
    with open(filename, 'a') as f:
        f.write("\n== References\n")
        for el in v:
            f.write(f"Referenced by <<{el}#{el},{el}>>\n\n")

# A very dumb way to generate a directed graph: we compile the list of
# references into a directed graph dot markup, replying on the asciidcotr plugin
# for diagrams to create the finished product.
#
# There is a graphviz lib for python. We should probably go that route later.
graphfile = "target/pre/reference-graph.adoc"
with open(graphfile, 'w') as f:
    f.write("[graphviz,reference-graph,png]\n"
            "----\n"
            "digraph {\n")
    
    for fromnode, v in mapping.items():
        for tonode in v:
            f.write(f"    \"{fromnode}\" -> \"{tonode}\";\n")
    
    f.write("}\n"
            "----")
