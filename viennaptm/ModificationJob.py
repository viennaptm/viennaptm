# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:27:26 2019

@author: CMargreitter
"""
class ResdiueMod:
    """Holds information on a particular modification of a given residue"""
    def __init__(self, resNum=None, oriResType=None, modID=None, chainID):
        self.resNum = resNum
        self.oriResType = oriResType
        self.modID = modID
        self.chainID = chainID
        
class ModificationJob:
    """Stores all the information necessary to execute a modification job on a given structure"""
    def __init__(self, structure, database="default"):
        # if default database is to be used, load it now
        if type(database) == str and database == "default":
            print("TODO: implement default database")
        self.database = database
        
        # if a string has been fed, try to parse it
        if type(structure) == str and os.path.exists(structure):
            if 