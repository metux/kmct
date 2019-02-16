
def set_from(container, name):
    if name in container:
        val = container[name]
        if type(val) == str:
            return set([val])
        if val is None:
            return set([])
        return set(val)
    return set()

def dict_from(container, name):
    if name in container:
        return container[name]
    return {}

def dict_keys_from(container, name):
    if name in container:
        return set(container[name].keys())
    return set([])

def dict_keys(d):
    return set(d.keys())

def dict_merge(dest, source):
    for x in source:
        if x not in dest:
            dest[x] = source[x]
    return dest

def make_path(fn):
    import errno
    import os

    path = os.path.dirname(fn)

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def write_file(fn, text):
    make_path(fn)
    f = open(fn, "w")
    f.write(text)
    f.close()

def fmt_val(val):
    if isinstance(val, int):
        return ("%d" % val)

    # try a hex number
    try:
        x = ("%d" % int(val, 16))
        return ("%s" % val)
    except:
        pass

    return ("\"%s\"" % val)
