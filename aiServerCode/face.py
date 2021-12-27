import json
a = [{"a":{"b":"a","c":"a"},"k":0},{"a":{"b":"a","c":"a"},"k":0}]
b = {}

b["c"] = "a"
b["k"] = "a"

del a

print(a)