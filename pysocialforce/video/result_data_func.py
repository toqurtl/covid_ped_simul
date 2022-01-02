from pysocialforce.data.parameters import DataIndex as Index


def distance(data, p_idx_1, p_idx_2):
    px_1, py_1 = data[p_idx_1][Index.px.index], data[p_idx_1][Index.py.index]
    px_2, py_2 = data[p_idx_2][Index.px.index], data[p_idx_2][Index.py.index]
    return ((px_1-px_2)**2 + (py_1-py_2)**2)**0.5