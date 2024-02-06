import json

name = 'Bữa ăn ấm lòng với ngườ'
chapter_test = 1

with open('mangas.json', 'r', encoding='utf-8') as f:
    for data in json.load(f):
        if data['name'] != None and name in data['name']:
            print(data['chapter'])
                