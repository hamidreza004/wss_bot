# coding: utf-8
import os.path

TOKEN = None
try:
    token_file_path = os.path.join(os.path.dirname(__file__), "TOKEN.txt")
    print()
    with open(token_file_path, 'r') as token_file:
        TOKEN = token_file.readline().strip()
except Exception as e:
    print(e)


