from app.models import ClinicalTrials, ClinicalTrialsFilters
from dataclasses import asdict
from typing import List


class SearchTreeNode:
    def __init__(self, node_type, value, parent=None):
        self.type = node_type
        self.value = value
        self.parent = parent
        self.children = []
        # variable to store ClinicalTrials records
        self.records = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = " " * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.value, end="")
        if self.records:
            print(f" ({len(self.records)} records)")
        else:
            print()
        if self.children:
            for child in self.children:
                child.print_tree()

    # def get_search_terms(self):
    #     search_terms = []
    #     if self.children:
    #         for child in self.children:
    #             search_terms.append(child.value)
    #             search_terms.extend(child.get_search_terms())
    #     return search_terms

    def create_search_tree(self):
        ctf = ClinicalTrialsFilters()
        ctf_dict = asdict(ctf)
        filter_queue = list(ctf_dict.keys())

        # create queue
        queue = [self]
        next_queue = queue.copy()
        while filter_queue:
            current_filter = filter_queue.pop(0)
            queue = next_queue.copy()
            next_queue = []
            while queue:
                current_node = queue.pop(0)
                # create a dictionary of filter values and empty lists
                filter_value_bins = {value: [] for value in ctf_dict[current_filter]}

                # iterate through records and add to bins
                for ct in current_node.records:
                    attrs = getattr(ct, current_filter)
                    # check attrs is a str and not None
                    if not attrs:
                        # if attrs is None, add to all bins
                        attrs = ctf_dict[current_filter]
                    # print(f'attrs: {attrs}')
                    if current_filter == 'age' or current_filter == 'phase':
                        attrs = attrs.split(',')
                    if isinstance(attrs, str):
                        attrs = [attrs]
                    for attr in attrs:
                        # filter_value_bins.get(attr, "Unknown status").append(ct)
                        if attr in filter_value_bins:
                            filter_value_bins[attr].append(ct)
                        # elif current_filter == "status":
                        #     filter_value_bins["Unknown status"].append(ct)
                    

                # create child nodes for each filter value
                for filter_value, bins in filter_value_bins.items():
                    child_node = SearchTreeNode(
                        current_filter, filter_value, current_node
                    )
                    child_node.records = bins
                    current_node.add_child(child_node)
                    next_queue.append(child_node)

                # remove records from current node
                current_node.records = []

        return self

    def get_filtered_records(self, filters: dict, num_records: int):
        filtered_records = []
        ctf = ClinicalTrialsFilters()
        ctf_dict = asdict(ctf)

        # add all filter values whose filter type is not in filters
        for filter_type, filter_values in ctf_dict.items():
            if filter_type not in filters or len(filters[filter_type]) == 0:
                filters[filter_type] = filter_values
        

        num_leaves = 0

        stack = [self]

        while stack and num_leaves <= num_records:
            current_node = stack.pop()
            if current_node.children:
                for child in current_node.children:
                    if child.type in filters:
                        if child.value in filters[child.type]:
                            stack.append(child)
                    else:
                        # in this case, the filter type is not in filters
                        # therefore, we want to add all children to the stack
                        stack.append(child)
            else:
                num_leaves += len(current_node.records)
                filtered_records.extend(current_node.records)

        return filtered_records[:num_records]
        # return filtered_records

    # serialize tree to dictionary
    def serialize(self):
        # traverse tree in pre-order and print leaves records
        stack = [self]
        tree_dict = {}
        while stack:
            current_node = stack.pop()
            if current_node.children:
                for child in current_node.children:
                    stack.append(child)
            else:
                tree_dict[current_node.value] = current_node.records

        return tree_dict



# Define a function to search for a tag in a dictionary
def find_tag(obj, tag):
    if tag in obj:
        return obj[tag]
    for key in obj:
        if isinstance(obj[key], dict):
            result = find_tag(obj[key], tag)
            if result is not None:
                return result



############## test code ################
if __name__ == "__main__":
    # create search tree of ClinicalTrials, with nodes of type ClinicalTrialsFilters

    # create root node
    root = SearchTreeNode("term", "Glioma")

    import random
    import time

    ctf = ClinicalTrialsFilters()
    ctf_dict = asdict(ctf)
    n = 10000
    print(f"creating {n} records")
    start_time = time.time()
    # randomly initialize 25 ClinicalTrials records
    for i in range(n):
        ct = ClinicalTrials()
        ct.nct_id = f"NCT{i}"
        ct.title = f"Glioma {i}"
        ct.phase = random.choice(ctf_dict["phase"])
        ct.status = random.choice(ctf_dict["status"])
        ct.age = [random.choice(ctf_dict["age"]) for i in range(2)]
        ct.gender = random.choice(ctf_dict["gender"])

        root.records.append(ct)

    print(f"created {n} records in {time.time() - start_time} seconds")
    # create queue
    # queue = [root]

    # filter_queue = list(ctf_dict.keys())
    # next_queue = queue.copy()
    # while filter_queue:
    #     current_filter = filter_queue.pop(0)
    #     queue = next_queue.copy()
    #     next_queue = []
    #     while queue:
    #         current_node = queue.pop(0)
    #         # create a dictionary of filter values and empty lists
    #         filter_value_bins = {filter_value: [] for filter_value in ctf_dict[current_filter]}

    #         # loop through records and put in a bin for each filter value
    #         for ct in current_node.records:
    #             filter_value_bins[getattr(ct, current_filter)].append(ct)

    #         # loop through bins and create children
    #         for filter_value, bin in filter_value_bins.items():
    #             child = SearchTreeNode(current_filter, filter_value)
    #             current_node.add_child(child)
    #             # add records to children
    #             child.records = bin
    #             next_queue.append(child)

    #         # free records from parent
    #         current_node.records = []

    print("creating search tree")
    start_time = time.time()
    root.create_search_tree().print_tree()
    # root.create_search_tree()
    print(f"created search tree in {time.time() - start_time} seconds")

    test_filters = {
        "phase": ["Phase 1", "Phase 2"],
        "status": ["Recruiting", "Active, not recruiting"],
    }

    # # add all filter values whose filter type is not in test_filters
    # for filter_type, filter_values in ctf_dict.items():
    #     if filter_type not in test_filters:
    #         test_filters[filter_type] = filter_values

    # # traverse tree and arrive at "n" leaves nodes based on test_filters

    # search_results = []

    # num_leaves = 10
    # stack = [root]

    # while num_leaves > 0 and stack:
    #     current_node = stack.pop()
    #     print(f'popped {current_node.value} from stack')
    #     if current_node.children:
    #         for child in current_node.children:
    #             if child.type in test_filters:
    #                 if child.value in test_filters[child.type]:
    #                     print(f'adding {child.value} to stack')
    #                     stack.append(child)
    #             else:
    #                 # in this case, we want to add all children to the stack
    #                 # beceause we don't have a filter for this type
    #                 print(f'ADDING {child.value} to stack')
    #                 stack.append(child)
    #     else:
    #         num_leaves -= len(current_node.records)
    #         search_results.extend(current_node.records)

    print("getting filtered records")
    start_time = time.time()
    print(len(root.get_filtered_records(test_filters, 1000)))
    print(f"got filtered records in {time.time() - start_time} seconds")


############## test code ################
