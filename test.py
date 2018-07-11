
import json


if __name__ == '__main__':
  with open('tree.json', 'r') as f:
    subjectdata = json.load(f)

  for sd in subjectdata:
    print (sd.get('id'))
