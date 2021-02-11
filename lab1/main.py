from tree import Leaf, build_tree
from data import data


print("\tThis is an awesome Luna City tourist detector:")
print("\tPossible answers to questions: 'yes' & 'no'")
print("------------------------------------------------")


def process_tree(node, spacing=""):
    """World's most elegant tree printing function."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print("The most suitable tourist is -->", node.predictions)
        return

    # Print the question at this node
    print(str(node.question))
    # get input
    val = input(">\t")

    if val == "yes":
        process_tree(node.true_branch, spacing)
    elif val == "no":
        process_tree(node.false_branch, spacing)
    else:
        print("Not a valid command. Try again")
        process_tree(node)


tree = build_tree(data)
process_tree(tree)
