import os.path
import json

class SQLQuery:
    
    def __init__(self, cmd):
        self.cmd = " ".join(cmd.split())
        self.tables = self.getTables()
        self.tablekeys = self.getTablekeys()
        self.attrs = self.getAttrs()
        self.conds = self.getConditions()
    
    def getAttrs(self):
        # attribute list between SELECT and FROM
        attr_str = self.cmd[(self.cmd.index("SELECT") + 6):self.cmd.index("FROM")].strip()
        attrs = attr_str.split(",")
        attrs = map(lambda attr: attr.strip(),attrs)
        # rewrite attrs, ex: tname -> teacher.tname
        result = []
        for attr in attrs:
            for key in self.tablekeys:
                if attr in key:
                    result.append(key)
                    break
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
            if(os.path.exists(table.strip() + ".txt") != True):
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
        conds = cond_str.split("AND")
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
            fname = t + ".txt"
            table = json.load(open(fname))
            keys = keys + map(lambda key: t+"."+key, table[0].keys()) 
        return keys


if __name__ == '__main__':
    cmd4 = "SELECT tname FROM teacher, department WHERE location = l2 AND teacher.did = department.did"
    cmd5 = "SELECT * FROM teacher, department"
    query = SQLQuery(cmd5)
    print "cmd: " +cmd4
    print "tables:" + str(query.tables)
    print "tablekeys:" + str(query.tablekeys)
    print "attrs:" + str(query.attrs)
    print "conditions:" + str(query.conds)
    pass