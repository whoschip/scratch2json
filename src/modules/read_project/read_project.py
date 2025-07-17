import ijson

class ReadProject:
    def __init__(self):
        pass
    
    def read(self, project_json):
        with open(project_json, 'r') as f:
            targets = ijson.items(f, 'targets.item')  
            sprites = sum(1 for _ in targets) 
            
            print("By default, there is 1 Stage")
            print(f"There are {sprites} sprites")