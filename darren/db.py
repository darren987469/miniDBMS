import json
from datagenerator import data_dir
'''
    Join related funcrtions
'''
# join two tables
def join(table1, table2):
    result = []
    for t1 in table1:
        for t2 in table2:
            result.append(dict(t1.items() + t2.items()))
    return result

def hasJoinCondition(conds, keys):
    for cond in conds:
        if cond["para1"] in keys and cond["para2"] in keys:
            return True
    return False

# get join condition with specified table keys
def getJoinCondition(conds, keys):
    joinConds = filter(lambda cond: cond["para1"] in keys and cond["para2"] in keys, conds)
    return joinConds[0]

def equalJoin(table1, table2, cond):
    result = []
    if cond["para1"] in table1[0].keys():
        joinTable1 = table1
        joinTable2 = table2
    else:
        joinTable1 = table2
        joinTable2 = table1
    for t1 in joinTable1:
        for t2 in joinTable2:
            if t1[cond["para1"]] == t2[cond["para2"]]:
                result.append(dict(t1.items() + t2.items()))
    return result

import os
'''
    Load data function
'''
# tables: a list of table name, ex: teacher
# return: a dict of table data
def loadTables(tables):
    data = {}
    for t in tables:
        fpath = os.path.join(data_dir, t + ".txt")
        table = json.load(open(fpath))
        # rewrite table, ex: tid -> teacher.tid
        newTable = []
        for row in table:
            newRow = {}
            for key in row:
                newRow[t+"."+key] = row[key]
            newTable.append(newRow)
        data[t] = newTable
        #data[t] = json.load(open(fname))
    return data

'''
    Aggregation functions: COUNT, MAX, MIN, SUM, AVG
'''
def COUNT(table, attr):
    return {"COUNT(*)":len(table)}

def MAX(table, attr):
    key = attr[attr.index("(")+1:attr.index(")")]
    maximum = 0
    for row in table:
        if row[key] > maximum:
            maximum = row[key]
    return {attr:maximum}

def MIN(table, attr):
    key = attr[attr.index("(")+1:attr.index(")")]
    minimum = None
    for row in table:
        if minimum == None:
            minimum = row[key]
        if row[key] < minimum:
            minimum = row[key]
    return {attr:minimum}    

def SUM(table, attr):
    key = attr[attr.index("(")+1:attr.index(")")]
    summation = 0
    for row in table:
        summation += row[key]
    return {attr:summation}

def AVG(table, attr):
    key = attr[attr.index("(")+1:attr.index(")")]
    summation = 0
    for row in table:
        summation += row[key]
    average = summation / len(table)
    return {attr:average}
