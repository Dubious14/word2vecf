from conllu import parse
from anytree import Node
from anytree.exporter import JsonExporter
import json


def build_tree(sentence):
    """
    Build a dependency tree from a parsed CoNLL sentence.
    """
    nodes = {0: Node("ROOT")}  # Virtual root node

    # First pass: Create all nodes
    for token in sentence:
        word = token["form"]
        relation = token["deprel"]
        nodes[token["id"]] = Node(f"{word} ({relation})")

    # Second pass: Attach nodes to their parents
    for token in sentence:
        head = token["head"]
        if head in nodes:  # Ensure the parent exists
            nodes[token["id"]].parent = nodes[head]
        else:
            print(f"Warning: Parent with ID {head} not found for token {token['form']}")

    return nodes[0]  # Return the root node


def save_trees_to_json(conll_file, output_file):
    """
    Parse a CoNLL file and save the dependency trees to a JSON file.
    """
    # Parse the CoNLL file
    with open(conll_file, "r") as f:
        sentences = parse(f.read())

    # Export each tree to JSON
    exporter = JsonExporter(indent=2, sort_keys=True)
    all_trees = []
    for sentence in sentences:
        root = build_tree(sentence)
        tree_json = exporter.export(root)  # Export to JSON string
        all_trees.append(json.loads(tree_json))  # Convert to dictionary for storage

    # Save the trees to a JSON file
    with open(output_file, "w") as out_file:
        json.dump(all_trees, out_file, indent=2)
    print(f"Dependency trees saved to '{output_file}'.")


if __name__ == "__main__":
    conll_input = "parsed.conll"
    json_output = input("Enter the name for the output JSON file (e.g., output.json): ").strip()

    if not json_output:
        json_output = "dependency_trees.json"

    if not json_output.endswith(".json"):
        json_output += ".json"

    save_trees_to_json(conll_input, json_output)

    print(f"Dependency trees saved to '{json_output}'.")

