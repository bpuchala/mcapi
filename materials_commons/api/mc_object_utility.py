from .make_objects import make_object

# Note: these utilities are currently used by dataset.py in
# materials_commons_extras/test


def make_mc_file(data):
    if '_type' in data.keys():
        data['otype'] = data['_type']
    if data['otype'] != 'datafile':
        return None
    return make_object(data)


def make_mc_process(data):
    if '_type' in data.keys():
        data['otype'] = data['_type']
    if data['otype'] != 'process':
        return None
    return make_object(data)


def make_mc_sample(data):
    if '_type' in data.keys():
        data['otype'] = data['_type']
    if data['otype'] != 'sample':
        return None
    return make_object(data)