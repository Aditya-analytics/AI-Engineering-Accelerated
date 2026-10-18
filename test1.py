class GetMaxScore:
    def __init__(self,record):
        self.records = record
    
    def get_highest_score(self):
        return max(self.records,key=lambda x:x['score'])
    

test = GetMaxScore([{'id': 1, 'score': 85}, {'id': 2, 'score': 92}, {'id': 3, 'score': 78}])
print(f"Highest score : {test.get_highest_score()}")



    