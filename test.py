#!/usr/bin/python
import os

print("hello world")
try:
    print(os.environ['DRONE_COMMIT_MESSAGE'])
except Exception as e:
    print(str(e))
