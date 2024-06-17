from Parser import ParsedFormula
from Parser import Subformula
from Parser import Until
from Parser import Proposition
from Parser import Conjunction
from Parser import Negation
from Parser import Next

class GNBA_node:
    def __init__(self, gnba, formula_set):
        self.gnba = gnba
        self.formula_set = formula_set
        self.next = set()
        self.prev = set()

    def add_next(self, node_idx):
        self.next.add(node_idx)

    def add_prev(self, node_idx):
        self.prev.add(node_idx)

    def __str__(self) -> str:
        str = "[\n"
        for formula in self.formula_set:
            str += formula.__str__() + ",\n"
        return str + "]"


class GNBA:
    def __init__(self, alphabet, parsed_formula):
        # list of nodes
        self.nodes = []
        # list of indices of nodes
        self.initial = []
        self.final = []
        self.alphabet = alphabet
        self.parsed_formula = parsed_formula
        self.build_gnba()

    def build_gnba(self):
        # build nodes from pased formula
        # for formula_set in self.parsed_formula.elementary_set:
        for index in range(len(self.parsed_formula.elementary_sets)):
            formula_set = self.parsed_formula.elementary_sets[index]
            node = GNBA_node(self, formula_set)
            self.nodes.append(node)
            if self.parsed_formula.formula in formula_set:
                self.initial.append(index)
        
        # every until formula in closure is related with a final set.
        for until in self.parsed_formula.closure:
            if until.type == 'until':
                F = []
                # for formula_set in self.parsed_formula.elementary_set:
                for index in range(len(self.parsed_formula.elementary_sets)):
                    formula_set = self.parsed_formula.elementary_sets[index]
                    # if this set satisfies the until formula
                    # if not (until.left not in formula_set and until.right not in formula_set):
                    if not (until in formula_set and until.right not in formula_set):
                        F.append(index)
                self.final.append(F)
        # for final_set in self.final:
        #     # for every pair of nodes in the same final set, add edges
        #     for i in range(len(final_set)):
        #         for j in range(len(final_set)):
        #             self.nodes[final_set[i]].add_next(final_set[j])
        #             self.nodes[final_set[j]].add_prev(final_set[i])

        # build edges
        for index in range(len(self.nodes)):
            node = self.nodes[index]
            # add self loop
            node.add_next(index)
            node.add_prev(index)
            for formula in node.formula_set:
                if formula.type == 'next':
                    for jndex in range(len(self.nodes)):
                        psb_next = self.nodes[jndex]
                        if formula.formula in psb_next.formula_set:
                            node.add_next(jndex)
                            psb_next.add_prev(index)
                elif formula.type == 'until':
                    for jndex in range(len(self.nodes)):
                        psb_next = self.nodes[jndex]
                        if formula.right in node.formula_set or (formula.left in node.formula_set and formula in psb_next.formula_set):
                            node.add_next(jndex)
                            psb_next.add_prev(index)
                elif formula.type == 'negation' and formula.formula.type == 'until':
                    for jndex in range(len(self.nodes)):
                        psb_next = self.nodes[jndex]
                        if formula.formula.right not in node.formula_set and (formula.formula.left not in node.formula_set or formula.formula not in psb_next.formula_set):
                            node.add_next(jndex)
                            psb_next.add_prev(index)

    def print_gnba(self):
        for index in range(len(self.nodes)):
            node = self.nodes[index]
            print("Node", index, ":", node)
            print("Next:", node.next)
            print("Prev:", node.prev)
            print("")