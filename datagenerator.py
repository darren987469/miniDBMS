import json
if __name__ == '__main__':
    data = []
    for i in range(1, 4):
        t = {}
        t['tid'] = i
        t['tname'] = "T" + str(i)
        t['tsex'] = "male" if i % 2 == 0 else "female"
        t['did'] = i
        data.append(t)
    json.dump(data, open("teacher.txt", "w"))
    
    data = []
    for i in range(1, 4):
        t = {}
        t['did'] = i
        t['dname'] = "D" + str(i)
        t['location'] = "L" + str(i)
        data.append(t)
    json.dump(data, open("department.txt", "w"))
    # load data
    # d = json.load(open("teacher.txt"))
#     print d[0].keys()
#     print d[0]['name']
    pass