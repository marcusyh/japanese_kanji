import os

def readfile(dirname):
    data = []
    for f in os.listdir(dirname):
        fpath = os.path.join(dirname, f)
        if not os.path.isfile(fpath):
            continue
        h = open(fpath, 'r')
        for i in h.readlines():
            if i.strip() == '':
                continue
            data.append(i.strip())
        h.close()
    return data

