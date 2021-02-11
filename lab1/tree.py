from utils import class_counts, is_numeric, partition, calculate_gini, distinct_attributes, info_gain
from data import characteristics


class Leaf:
    """ end node, no other child nodes """

    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    """ this holds a reference to the question, and to the two child nodes."""

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            characteristics[self.column], condition, str(self.value))


def find_best_split(rows):
    """ calculate the gain of a question and what question is best to ask"""
    best_gain = 0
    best_question = None
    current_uncertainty = calculate_gini(rows)
    n_features = len(rows[0]) - 1

    for col in range(n_features):

        values = distinct_attributes(rows, col)

        for val in values:

            question = Question(col, val)

            true_rows, false_rows = partition(rows, question)

            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


def build_tree(rows):
    gain, question = find_best_split(rows)

    if gain == 0:
        return Leaf(rows)

    true_rows, false_rows = partition(rows, question)

    true_branch = build_tree(true_rows)

    false_branch = build_tree(false_rows)

    return Decision_Node(question, true_branch, false_branch)


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions

    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)
