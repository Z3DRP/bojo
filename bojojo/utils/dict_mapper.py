
from sqlalchemy import inspect


def object_to_dict(instance):
    if hasattr(instance, '__mapper__'):
        return {c.key: getattr(instance, c.key) for c in inspect(instance.__class__).column_attrs}
    else:
        return {k: v for k, v in vars(instance).items() if not callable(v) and not k.startswith('_')}
    

def proxy_to_dict(prxy_rsult):
    if prxy_rsult is None:
        return {}
    return {column: getattr(prxy_rsult, column) for column in prxy_rsult.keys()}