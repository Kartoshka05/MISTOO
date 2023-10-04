import requests

def read_channels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

