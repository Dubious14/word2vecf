import json
from anytree import RenderTree
from anytree.importer import JsonImporter
from graphviz import Digraph


def load_trees_from_json(json_file):
    """
    Load dependency trees from a JSON file.
    """
    with open(json_file, "r") as f:
        return json.load(f)


def display_tree_from_json(tree_data):
    """
    Reconstruct and display a tree using anytree from JSON data.
    """
    importer = JsonImporter()
    root = importer.import_(json.dumps(tree_data))

    print("Tree Structure:")
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")


def export_tree_to_graphviz(tree_data, output_file):
    """
    Export the tree to a Graphviz DOT format and save as an image.
    """
    dot = Digraph(comment="Dependency Tree")

    def add_nodes_edges(node, parent=None):
        dot.node(node.name, node.name)  # Add the current node
        if parent:
            dot.edge(parent.name, node.name)  # Add an edge to the parent
        for child in node.children:
            add_nodes_edges(child, node)

    importer = JsonImporter()
    root = importer.import_(json.dumps(tree_data))
    add_nodes_edges(root)

    # Build and save the graph as PNG
    dot.render(output_file, format="png", cleanup=True)
    print(f"Tree saved as '{output_file}.png'")


if __name__ == "__main__":
    # Input JSON file
    json_file = input("Enter the JSON file name to visualize (e.g., dependency_trees.json): ").strip()
    if not json_file:
        json_file = "dependency_trees.json"

    # Ensure the file ends with .json
    if not json_file.endswith(".json"):
        json_file += ".json"

    # Load all trees from the JSON file
    trees = load_trees_from_json(json_file)
    print(f"Loaded {len(trees)} trees from '{json_file}'\n")

    # Ask user for a global choice
    print("Choose an option:")
    print("1. Save all trees as images")
    print("2. Skip saving all trees")
    print("3. Decide for each tree")
    choice = input("Enter your choice (1/2/3): ").strip()

    # Process trees based on user choice
    for i, tree_data in enumerate(trees):
        print(f"\nSentence {i + 1} Tree:")
        display_tree_from_json(tree_data)

        if choice == "1":  # Save all trees
            output_file = f"tree_sentence_{i + 1}"
            export_tree_to_graphviz(tree_data, output_file)
        elif choice == "2":  # Skip all trees
            print("Tree visualization skipped.")
        elif choice == "3":  # Ask for each tree
            save_image = input("Do you want to save this tree as an image? (yes/no): ").strip().lower()
            if save_image in ("yes", "y"):
                output_file = f"tree_sentence_{i + 1}"
                export_tree_to_graphviz(tree_data, output_file)
            else:
                print("Tree visualization skipped.")
        else:
            print("Invalid choice. Skipping tree.")
