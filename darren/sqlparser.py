import os.path
import json
import re
from datagenerator import data_dir

class SQLQuery:
    
    def __init__(self, cmd):
        self.cmd = " ".join(cmd.split())
        self.tables = self.getTables()
        self.tablekeys = self.getTablekeys()
        self.attrs = self.getAttrs()
        self.conds = self.getConditions()
    
    # cmd8 = "SELECT MAX(Grade), MIN(Grade), AVG(Grade) FROM enroll_in"
    def getAttrs(self):
        # attribute list between SELECT and FROM
        attr_str = self.cmd[(self.cmd.index("SELECT") + 6):self.cmd.index("FROM")].strip()
        if "*" in attr_str and "COUNT(*)" not in attr_str:
            return ["*"]
        attrs = attr_str.split(",")
        attrs = map(lambda attr: attr.strip(),attrs)
        # rewrite attrs, ex: tname -> teacher.tname
        result = []
        for attr in attrs:
            for key in self.tablekeys:
                if attr in key:
                    result.append(key)
                    break
        # aggregate function attrs, ex: MAX(Grade), MIN(Grade), AVG(Grade)
        for attr in attrs:
            if "(" in attr and ")":
                attribute = attr[attr.index("(")+1:attr.index(")")]
                for key in self.tablekeys:
                    if attribute in key:
                        attribute = key
                        break
                s = ""
                if "COUNT" in attr:
                    s = "COUNT(" + attribute + ")"
                elif "MAX" in attr:
                    s = "MAX(" + attribute + ")"
                elif "MIN" in attr:
                    s = "MIN(" + attribute + ")"
                elif "SUM" in attr:
                    s = "SUM(" + attribute + ")"
                elif "AVG" in attr:
                    s = "AVG(" + attribute + ")"
#                 else:
#                     print "\nError: sqlparser getAttr() error."
                result.append(s)
        return result
    
    def getTables(self):
        # table list between FROM and WHERE
        #attr_str = cmd[(cmd.index("select") + 6):cmd.index("from")].strip()
        if(self.cmd.find("WHERE") == -1):
            table_str = self.cmd[self.cmd.index("FROM") + 4:].strip()
        else:
            table_str = self.cmd[self.cmd.index("FROM") + 4:self.cmd.index("WHERE")].strip()
        tables = table_str.split(",")
    
        return_tables = []
        for table in tables:
            fpath = os.path.join(data_dir, table.strip() + ".txt")
            if(os.path.exists(fpath) != True):
                print "There is no \"" + str(table.strip()) + "\" in system."
                return 
            return_tables.append(table.strip())
        return return_tables
    
    # cmd4 = "SELECT TNAME FROM Teacher, Department WHERE DID = 2 AND Location = L1"
    # condition data structure: {"para1":para1, "para2":para2, "logic":logic}
    def getConditions(self):
        if(self.cmd.find("WHERE") == -1):
            return []
        cond_str = self.cmd[self.cmd.index("WHERE")+5:].strip()
        if "IN" in cond_str or "NOT IN" in cond_str:
            nestedquery = cond_str[cond_str.index("(")+1:cond_str.index(")")]
            para1 = cond_str.split(" ")[0].strip()
            if "NOT IN" in cond_str:
                logic = "NOT IN"
            else:
                logic = "IN"
            para2 = nestedquery
            # rewrite conditions, ex: location -> department.location
            if para1.find(".") == -1:
                for key in self.tablekeys:
                    if para1 in key:
                        para1 = key
                        break
            return [{"para1":para1, "para2":para2, "logic":logic}] 
        
        #conds = re.split("AND | OR", cond_str)
        conds = re.split("AND", cond_str)
        return_conds = []
        
        for cond in conds:
            tokens = cond.strip().split(" ")
            para1 = tokens[0]
            logic = tokens[1]
            para2 = tokens[2]
            # rewrite conditions, ex: location -> department.location
            if para1.find(".") == -1:
                for key in self.tablekeys:
                    if para1 in key:
                        para1 = key
                        break
            return_conds.append({"para1":para1, "para2":para2, "logic":logic})
        return return_conds

    def getTablekeys(self):
        keys = []
        for t in self.tables:
            fpath = os.path.join(data_dir, t + ".txt")
            table = json.load(open(fpath))
            keys = keys + map(lambda key: t+"."+key, table[0].keys()) 
        return keys

def parseQuery(cmd):
    query = SQLQuery(cmd)
    print "cmd: " +cmd
    print "tables:" + str(query.tables)
    #print "tablekeys:" + str(query.tablekeys)
    print "attrs:" + str(query.attrs)
    print "conditions:" + str(query.conds)
    
if __name__ == '__main__':
    cmd4 = "SELECT tname FROM teacher, department WHERE location = l2 AND teacher.did = department.did"
    cmd5 = "SELECT * FROM teacher, department WHERE location = L2 AND location = L3"
    cmd6 = "SELECT * FROM teacher WHERE did IN (SELECT did FROM department WHERE location = L3)"
    cmd7 = "SELECT * FROM teacher WHERE did NOT IN (SELECT did FROM department WHERE location = L3)"
    cmd8 = "SELECT MAX(grade), MIN(grade), AVG(grade) FROM enroll_in" 
    cmd = cmd7
    parseQuery(cmd)
    pass