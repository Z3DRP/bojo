from rich.table import Table

from bojojo.utils.dict_mapper import object_to_dict, stringify_dict

def get_singlerow_table(**kwargs):
    headers = []
    values = []
    for key, value in kwargs.items():
        headers.append(key)
        values.append(value)
    table = Table(*headers)
    table.add_row(*values)
    return table


def get_multirow_table(arglist):
    headers = []
    values = []
    for indx, entity in enumerate(arglist):
        strentity = stringify_dict(entity)
        if indx == 0:
           ks = strentity.keys()
           for k in ks:
               headers.append(k)
        values.append(list(strentity.values()))
    table = Table(*headers)
    for val in values:
        table.add_row(*val)
    return table


            

    
