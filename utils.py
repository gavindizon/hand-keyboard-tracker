def none_in_dict(d):
    for _, value in d.items():
        if value is None:
            return True
    return False