#!/usr/bin/env python

import sys


class Tree(object):
    def __init__(self):
        self.label = None
        self.children = []

    def __str__(self):
        children_str = ""
        if len(self.children) > 0:
            children_str = "("
            for idx, child in enumerate(self.children):
                if idx > 0:
                    children_str += ","
                children_str += str(child)
            children_str += ")"
        return self.label + children_str


def parse_tree(tree):
    # print("Parsing: " + tree)
    root = Tree()
    root.label = tree

    if '(' in root.label:
        root.label = root.label[:root.label.index('(')]
    if "(" not in tree:
        return root

    tree = tree[tree.index('('):]
    # print("Next: " + tree)
    parenthesis = 0

    element = ""
    for l in tree:
        if l == '(':
            if parenthesis > 0:
                element += l
            parenthesis += 1
        elif l == ')':
            parenthesis -= 1
            if parenthesis == 0:
                root.children.append(parse_tree(element))
                element = ""
            else:
                element += l
        else:
            if l == ',' and parenthesis == 1:
                root.children.append(parse_tree(element))
                element = ""
            else:
                element += l

    return root


def parse_rule(rule):
    parts = rule.split("->")
    left_non_terminal = parts[0].strip()
    if '(' in left_non_terminal:
        left_non_terminal = left_non_terminal[:left_non_terminal.index('(')].strip()
    right_tree = parse_tree(parts[1].strip())
    return left_non_terminal, right_tree


def gorn_address(p, idx):
    if p == "e":
        return str(idx + 1)
    else:
        return p + "." + str(idx + 1)


def get_all_x_pairs(p, right):
    if right.label[0] == 'x':
        return [[p, int(right.label[1])-1]]  # here we suppose that maximum x index is 9

    pairs = []
    for idx, child in enumerate(right.children):
        pairs.extend(get_all_x_pairs(gorn_address(p, idx), child))

    return pairs


def find_terminals(i, p, left, right, rules):
    new_rules = []
    common_left = "(" + str(i + 1) + "," + p + ")[] -> "
    is_term = not right.label.istitle()
    x_term = right.label[0] == 'x'
    if len(right.children) > 0:
        this_rule = ""
        for idx, child in enumerate(right.children):
            new_rules.extend(find_terminals(i, gorn_address(p, idx), left, child, rules))
            this_rule += "(" + str(i + 1) + "," + gorn_address(p, idx) + ")[]"

        if is_term and not x_term:
            new_rules.append(common_left + this_rule)

    elif is_term and not x_term:
        new_rules.append("(" + str(i + 1) + "," + p + ")[] -> " + right.label)

    if not is_term:
        for j, pair in enumerate(rules):
            if pair[0] == right.label:
                new_rules.append(common_left + "(" + str(j + 1) + ",e)[(" + str(i + 1) + "," + p + ")]")
                x_pairs = get_all_x_pairs("e", pair[1])
                for x_pair in x_pairs:
                    new_rules.append(
                        "(" + str(j + 1) + "," + x_pair[0] + ")[("+ str(i+1)+ "," + p + ")] -> (" + str(i + 1) + "," + gorn_address(p, x_pair[1]) + ")[]")

    return new_rules


def transform(i, left, right, rules):
    new_rules = []
    if left == "S":
        new_rules.append("S[] -> (" + str(i + 1) + ",e)[]")

    new_rules.extend(find_terminals(i, "e", left, right, rules))

    return new_rules


# Read contents of the input file
rules = [line.rstrip('\n') for line in open(sys.argv[1])]

transformed_rules = []
parsed_rules = []

# parse each line as a rule
for idx, rule in enumerate(rules):
    left, right = parse_rule(rule)
    print(str(idx + 1) + ". " + left + " -> " + str(right))
    parsed_rules.append([left, right])

for idx, pair in enumerate(parsed_rules):
    transformed_rules.extend(transform(idx, pair[0], pair[1], parsed_rules))

print("Transformed:")

for idx, transformed_rule in enumerate(transformed_rules):
    print(str(idx + 1) + ". " + transformed_rule)
