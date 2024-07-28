from rich.table import Table

from bojojo.utils.dict_mapper import object_to_dict

def get_singlerow_table(**kwargs):
    headers = []
    values = []
    for key, value in kwargs.items():
        headers.append(key)
        values.append(value)
    table = Table(*headers)
    table.add_row(*values)
    return table


def get_multirow_table(*args):
    headers = []
    values = []
    for item in args:
        values.append(object_to_dict(item))
    for key in values[0].keys():
        headers.append(key)
    table = Table(*headers)
    for item in values:
        currentRow = item.values()
        table.add_row(*currentRow)
    return table
    
