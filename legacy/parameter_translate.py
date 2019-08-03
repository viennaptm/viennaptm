# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 16:32:58 2019

@author: flab
"""

test = """NTP DPH
ANC CG
DVE CB CG
DVR CB CA
ADD NAME=OD1 TYPE=O XCOORR=0.647321 YCOORR=0.856817 ZCOORR=0.591685 TEMPF=0
ADD NAME=OD2 TYPE=O XCOORR=0.606134 YCOORR=-1.00824 ZCOORR=-0.664536 TEMPF=0
ADD NAME=HD2 TYPE=H XCOORR=1.57808 YCOORR=-0.847137 ZCOORR=-0.55007 TEMPF=0
DEL ND1
DEL CD2
DEL CE1
REP OD1 ODX
REP OD2 NPP=N
DEL NE2"""

def parameter_translate(inp):
    inp = inp.split(sep="\n")
    headerList = []
    addList = []
    axesList = []
    deleteList = []
    replaceList = []
    indent = " " * 2
    for line in inp:
        parts = line.split(sep=" ")
        if parts[0] == "ANC":
            headerList.append("<anchor>"+parts[1]+"</anchor>")
        elif parts[0] == "DVE":
            axesList.append('<axis number="1" p1="'+parts[1]+'" p2="'+parts[2]+'"/>')
        elif parts[0] == "DVR":
            axesList.append('<axis number="2" p1="'+parts[1]+'" p2="'+parts[2]+'"/>')
        elif parts[0] == "ADD":
            name = parts[1].split(sep="=")[1]
            eletype = parts[2].split(sep="=")[1]
            xcoorr = parts[3].split(sep="=")[1]
            ycoorr = parts[4].split(sep="=")[1]
            zcoorr = parts[5].split(sep="=")[1]
            tempfactor = parts[6].split(sep="=")[1]
            addList.append( '<add name="' + name + '" eletype="' + eletype + '" xcoorr="' + xcoorr + '" ycoorr="' + ycoorr + '" zcoorr="' + zcoorr + '" tempfactor="' + tempfactor + '"/>' )
        elif parts[0] == "DEL":
            deleteList.append( '<del name="' + parts[1] + '"/>' )
        elif parts[0] == "REP":
            oriName = parts[1]
            newRes = parts[2].split(sep="=")
            if len( newRes ) == 1:
                replaceList.append( '<rep name="' + oriName + '" by="' + newRes[0] + '"/>' )
            elif len( newRes ) == 2:
                replaceList.append( '<rep name="' + oriName + '" by="' + newRes[0] + '" new_eletype="' + newRes[1] + '"/>' )
    returnString = indent * 3 + "\n".join( headerList )
    if len( axesList ) > 0:
        returnString = returnString + "\n" + indent * 3 + "<axes>\n" + indent * 4 + ( indent * 4 ).join( x + "\n" for x in axesList ) + indent * 3 + "</axes>"
    if len( addList ) > 0:
        returnString = returnString + "\n" + indent * 3 + "<additions>\n" + indent * 4 + ( indent * 4 ).join( x + "\n" for x in addList ) + indent * 3 + "</additions>"
    if len( deleteList ) > 0:
        returnString = returnString + "\n" + indent * 3 + "<deletions>\n" + indent * 4 + ( indent * 4 ).join( x + "\n" for x in deleteList ) + indent * 3 + "</deletions>"
    if len( replaceList ) > 0:
        returnString = returnString + "\n" + indent * 3 + "<replacements>\n" + indent * 4 + ( indent * 4 ).join( x + "\n" for x in replaceList ) + indent * 3 + "</replacements>"
    return returnString
    
z = """NTP KAL
DVE CD CE
ANC CE
DVR CD CG
ADD NAME=HE TYPE=H XCOORR=0.539156 YCOORR=-0.0661429 ZCOORR=-0.950755 TEMPF=0
ADD NAME=OZ TYPE=O XCOORR=0.614661 YCOORR=0.103507 ZCOORR=1.04827 TEMPF=0
DEL NZ
DEL HZ1
DEL HZ2
DEL HZ3"""
print( parameter_translate( z ) )
mydoc = minidom.parse( "/home/flab/Desktop/done.xml" )