import json5


def read_conf():
    conf_file = open("conf.json5", "r")
    conf = json5.loads(conf_file.read())
    conf_file.close()

    return conf
