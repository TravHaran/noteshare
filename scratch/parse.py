import json
json_file = "/Users/travisratnaharan/Documents/Work/noteshare/scratch/files.json"

def parser(file, index):
    with open(file) as f:
        dictData = json.load(f)
        print(dictData)
        print('\n')
        book = dictData[index]
        print(book)
        print('\n')
        pdf = book['content']
    return pdf
    
result = parser(json_file, 2)
print(result)