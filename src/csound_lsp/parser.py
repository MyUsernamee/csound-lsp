# This is meant to be a wrapper around csound's Tree object.
# It should take some file parse it then return the Tree object as something
# More universally parseable like json

import ctcsound

cs = ctcsound.Csound()

def parse_orc(orc_text):
    cs.compile_orc(orc_text)
    return cs.host_data()

def cli():
    import argparse

    parser = argparse.ArgumentParser("csound-parser")

    _ = parser.add_argument("filename")

    args = parser.parse_args()

    with open(args.filename, "r") as f:
        print(parse_orc(f.read()))
