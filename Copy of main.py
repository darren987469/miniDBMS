import json
from sqlparser import SQLQuery 

def readCommand():
    while True:
        cmd = raw_input(">>> command:")
        if(cmd == 'q' or cmd =='quit'):
            break
        print cmd
        


# join two tables
def join(table1, table2):
    result = []
    for t1 in table1:
        for t2 in table2:
                result.append(dict(t1.items() + t2.items()))
    return result

# join two tables
def equalJoin(table1, table2, cond):
    result = []
    for t1 in table1:
        for t2 in table2:
                result.append(dict(t1.items() + t2.items()))
    return result

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

# get first matched condition
def condFilter(cond,keys):
    # case: department.did = teacher.did
    if cond['para1'] in keys and cond['para2'] in keys:
        return True
    # case: location = 1
    elif cond['para1'] in keys:
        return True
    else:
        return False    

# tables: a list of table name, ex: teacher
# return: a dict of table data
def loadTables(tables):
    data = {}
    for t in tables:
        fname = t + ".txt"
        table = json.load(open(fname))
        newTable = []
        for row in table:
            newRow = {}
            for key in row:
                newRow[t+"."+key] = row[key]
            newTable.append(newRow)
        data[t] = newTable
        #data[t] = json.load(open(fname))
    return data

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
            return filter(lambda row: str(row[cond['para1']]) >= cond['para2'], table)
        elif cond['logic'] == "!=":
            return filter(lambda row: str(row[cond['para1']]) != cond['para2'], table)
        else: 
            print "tableFilter() else"
            return []
    else:
        print "Error in tableFilter()"
        print table
        print cond  

def getJoinConditions(conds, keys):

if __name__ == '__main__':
    cmd1 = "SELECT * FROM teacher"
    cmd2 = "SELECT tid, tname FROM teacher"
    cmd3 = "SELECT tname FROM teacher WHERE tid = 1"
    cmd4 = "SELECT tname FROM teacher, department WHERE location = L2 AND teacher.did = department.did"
    cmd5 = "SELECT * FROM teacher, department"
    cmd = cmd1
    query = SQLQuery(cmd)
    conds = [cond for cond in query.conds]
    print "cmd: " +cmd
    print "tables:" + str(query.tables)
    print "tablekeys:" + str(query.tablekeys)
    print "attrs:" + str(query.attrs)
    print "conditions:" + str(conds) + "\n"

    data = loadTables(query.tables)
    
    result = []
    # read all the tables
    while len(result) == 0 or len(data) != 0:
        if len(result) == 0:
            result = data.pop(data.keys()[0])
        else:
            # pop another table to join with result table
            jointable = data.pop(data.keys()[0])
            result = join(result, jointable)
            # get executable condition and filter result table
            keys = result[0].keys()
            
            conditions = filter(lambda c: condFilter(c, keys), conds)
            print conditions
            for cond in conditions:
                # remove conditions from conds
                conds.remove(cond)
                result = tableFilter(result, cond)
    
    print "result:" + str(result) 
    # read all conditions
    if len(conds) != 0:
        for cond in conds:
            print "cond:" + str(cond)
            result = tableFilter(result, cond)
    # TODO
    # select attrs    
    
    printTable(result)
    
    pass
