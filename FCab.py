import json
# - - - - - - - - - - - - - - - - 
# - - -  JSON DUMP CLASS  - - - -
# - - - - - - - - - - - - - - - -
class JsonDump:
    def __init__(self):
        print 'init'
    
    def dump(self, obj, filename):
        f = open(filename, 'w')
        json.dump(obj, f)
        f.close()

    def load(self, filename):
        f = open(filename)
        return json.load(f)

# - - - - - - - - - - - - - - - - 
# - - - - - __________  - - - - -
# - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - 
# - - - - - __________  - - - - -
# - - - - - - - - - - - - - - - -


