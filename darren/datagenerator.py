import json
import random
import os

data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

if __name__ == '__main__':
    ''' student table'''
    data = []
    for i in range(1, 11):
        t = {}
        t['sid'] = i
        t['sname'] = "S" + str(i)
        t['ssex'] = "male" if i % 2 == 0 else "female"
        t['did'] = i % 11 # ten department
        t['rid'] = i % 11 # ten room
        data.append(t)
    json.dump(data, open(data_dir+"/student.txt", "w"), ensure_ascii=False, indent=4)
    
    ''' course table'''
    data = []
    for i in range(1, 11):
        t = {}
        t['cid'] = i
        t['cname'] = "C" + str(i)
        t['cgrade'] = i % 4 + 1 # four year in university
        t['did'] = i % 11 # ten department
        t['rid'] = i % 11 # ten room
        t['tid'] = i % 11 # ten teacher
        data.append(t)
    json.dump(data, open(data_dir+"/course.txt", "w"), ensure_ascii=False, indent=4)
    
    ''' teacher table'''
    data = []
    for i in range(1, 11):
        t = {}
        t['tid'] = i
        t['tname'] = "T" + str(i)
        t['tsex'] = "male" if i % 2 == 0 else "female"
        t['did'] = i
        data.append(t)
    json.dump(data, open(data_dir+"/teacher.txt", "w"), ensure_ascii=False, indent=4)
    
    ''' department table'''
    data = []
    for i in range(1, 11):
        t = {}
        t['did'] = i
        t['dname'] = "D" + str(i)
        t['location'] = "L" + str(i)
        data.append(t)
    json.dump(data, open(data_dir+"/department.txt", "w"), ensure_ascii=False, indent=4)
    
    ''' room table'''
    data = []
    for i in range(1, 11):
        t = {}
        t['rid'] = i
        t['rname'] = "Room" + str(i)
        if i % 3 == 0:
            t['type'] = "classroom"
        elif i % 3 == 1:
            t['type'] = "office"
        else:
            t['type'] = "lab"
        t['did'] = i % 11 # ten department
        t['ownerid'] = i % 11 # ten teacher
        data.append(t)
    json.dump(data, open(data_dir+"/room.txt", "w"), ensure_ascii=False, indent=4)
    
    ''' enroll_in table'''
    data = []
    for i in range(1,101):
        t = {}
        t["sid"] = i % 10 + 1 # ten student
        t["cid"] = i % 10 + 1 # ten course
        t["grade"] = random.randint(0,99) 
        data.append(t)
    json.dump(data, open(data_dir+"/enroll_in.txt","w"), ensure_ascii=False, indent=4)
    
    print "Data generated!"
    pass