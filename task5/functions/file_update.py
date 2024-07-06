import json
def openfile(path):
    f = open(path, "r")
    result = json.load(f)
    f.close()
    return result

def updatefile(path, content):
    with open(path,"w") as users:
        json.dump(content, users)
        users.close()
    return
