res = {"data": {"choices": [{"message": {"content": "Hello world"}}]}}

#Safety net
if res["data"]["choices"]:
    #get the Hello world
    print(res["data"]["choices"][0]["message"]["content"])
    