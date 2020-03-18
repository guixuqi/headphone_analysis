import re

s = "255"
# if re.search("万", s):
#     sr = int(s.replace("万", ""))*10000
#     print(sr)

s = int(s.replace("万", ""))*10000 if re.search("万", s) else s
print(s)