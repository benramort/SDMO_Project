print("Hello 2024")

import urllib.request
contents = urllib.request.urlopen("https://guthib.com").read()

print(contents)

with open("results/text.txt", "w") as f:
    f.write("This is a test file 3.\n")