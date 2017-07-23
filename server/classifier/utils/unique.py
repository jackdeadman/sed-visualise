# Keeps order
def unique(lst):
    new_list = []
    tmp_set = set()
    for item in lst:
        if item not in tmp_set:
            new_list.append(item)
            tmp_set.add(item)
    return new_list
