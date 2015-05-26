from sqlparser import SQLQuery 
from db import AVG, COUNT, MAX, MIN, SUM
from db import join, hasJoinCondition, getJoinCondition, equalJoin
from db import loadTables

def readCommand():
    while True:
        cmd = raw_input(">>> command:")
        if(cmd == 'q' or cmd =='quit'):
            break
        print cmd

def printTable(table):
    print "****************************"
    line1 = ""
    line2 = ""
    for key in table[0].keys():
        line1 += key + "  |  "
        line2 += "----------"
    print line1
    print line2
    for row in table:
        row_str = ""
        for key in row.keys():
            row_str += str(row[key]) + "  |  "
        print row_str

def tableFilter(table, cond):
    print "tableFilter(), table:" + str(table)
    keys = table[0].keys()
    # case: department.did = teacher.did
    if cond['para1'] in keys and cond['para2'] in keys:
        return filter(lambda row: row[cond['para1']] == row[cond['para2']], table)
    # case: location = 1, or age > 2
    elif cond['para2'] not in keys:
        if cond['logic'] == "=":
            return filter(lambda row: str(row[cond['para1']]) == cond['para2'], table)
        elif cond["logic"] == ">":
            return filter(lambda row: str(row[cond['para1']]) > cond['para2'], table)
        elif cond['logic'] == "<":
            return filter(lambda row: str(row[cond['para1']]) < cond['para2'], table)
        elif cond['logic'] == ">=":
            return filter(lambda row: str(row[cond['para1']]) >= cond['para2'], table)
        elif cond['logic'] == "<=":
            return filter(lambda row: str(row[cond['para1']]) <= cond['para2'], table)
        elif cond['logic'] == "!=":
            return filter(lambda row: str(row[cond['para1']]) != cond['para2'], table)
        elif cond['logic'] == "IN":
            result = executeCmd(cond["para2"])
            para2list = map(lambda row: row[row.keys()[0]], result)
            return filter(lambda row: row[cond['para1']] in para2list, table)
        elif cond['logic'] == "NOT IN":
            result = executeCmd(cond["para2"])
            para2list = map(lambda row: row[row.keys()[0]], result)
            return filter(lambda row: row[cond['para1']] not in para2list, table)
        else: 
            print "tableFilter() else"
            return []
    else:
        print "Error in tableFilter()"
        print table
        print cond  

def attrFilter(table, attrs):
    # SELECT *
    if len(attrs) == 1 and "*" in attrs:
        return table
    # aggregate function, ex: MAX(enroll_in.grade)
    elif "(" in attrs[0]:
        result = {}
        for attr in attrs:
            if "COUNT" in attr:
                result.update(COUNT(table,attr))
            elif "MAX" in attr:
                result.update(MAX(table,attr))
            elif "MIN" in attr:
                result.update(MIN(table,attr))
            elif "SUM" in attr:
                result.update(SUM(table,attr))
            elif "AVG" in attr:
                result.update(AVG(table,attr))
        return [result]
    # SELECT tid, tname FROM teacher
    else:
        result = []
        for row in table:
            newRow = {}
            for rowkey in row.keys():
                if rowkey in attrs:
                    newRow[rowkey] = row[rowkey]
            result.append(newRow)
        return result



def executeCmd(cmd):
    query = SQLQuery(cmd)
    conds = [cond for cond in query.conds]
    #print "cmd: " +cmd
    #print "tables:" + str(query.tables)
    #print "tablekeys:" + str(query.tablekeys)
    #print "attrs:" + str(query.attrs)
    #print "conditions:" + str(conds) + "\n"

    data = loadTables(query.tables)
    
    result = []
    # read all the tables
    while len(result) == 0 or len(data) != 0:
        if len(result) == 0:
            result = data.pop(data.keys()[0])
        else:
            # pop another table to join with result table
            nextTable = data.pop(data.keys()[0])
            keys = result[0].keys() + nextTable[0].keys()
            
            # get join condition and join two tables
            if hasJoinCondition(conds, keys):
                joinCond = getJoinCondition(conds, keys)
                # remove join condition from condition list
                conds.remove(joinCond)
                result = equalJoin(result, nextTable, joinCond)
            else:
                result = join(result, nextTable)
     
    # read all conditions to filter result table
    if len(conds) != 0:
        for cond in conds:
            result = tableFilter(result, cond)       
    # select attrs
    result = attrFilter(result, query.attrs)    
    return result
    

    
if __name__ == '__main__':
    cmd1 = "SELECT * FROM department"
    cmd2 = "SELECT tid, tname FROM teacher"
    cmd3 = "SELECT tname, tid FROM teacher WHERE tid = 1"
    cmd4 = "SELECT tname FROM teacher, department WHERE location = L2 AND teacher.did = department.did"
    cmd5 = "SELECT * FROM teacher, department WHERE location = L2 AND teacher.did = department.did"
    cmd6 = "SELECT * FROM teacher WHERE did IN (SELECT did FROM department WHERE location = L3)"
    cmd7 = "SELECT * FROM teacher WHERE did NOT IN (SELECT did FROM department WHERE location = L3)"
    cmd8 = "SELECT MAX(grade), MIN(grade), SUM(grade), COUNT(*), AVG(grade) FROM enroll_in"
    
    result = executeCmd(cmd5)
    printTable(result)
    pass
