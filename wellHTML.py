import sys
import os
import xml.parsers.expat
import html.parser
import json
import datetime
import random

from html.parser import HTMLParser

printDebug  = False; #True;
printDebug1 = False

#--------------------------------------------------------------------
def getInt (source) :
        dictTran = "".maketrans("0123456789","0123456789",
                                "qwertyuiop[]asdfghjkl;'zxcvbnm,./"+
                                "QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./"+
                                "Р№С†СѓРєРµРЅРіС€С‰Р·С…СЉС„С‹РІР°РїСЂРѕР»РґР¶СЌСЏС‡СЃРјРёС‚СЊР±СЋС‘"+
                                "Р™Р¦РЈРљР•РќР“РЁР©Р—РҐРЄР¤Р«Р’РђРџР РћР›Р”Р–Р­РЇР§РЎРњР�РўР¬Р‘Р®РЃ"+
                                "`!@#$%^&*()_+-=|\\/");
        result = source.translate(dictTran);
        if (len(result)==0) : result = '0';
        return int(result)


#--------------------------------------------------------------------
#
#   Build well-down XML from HTML     
#   
#     get string from feed with all HTML structure
#     and build well-down XML in string result (function getResult()) 
#     
#     
#   Common startup function:
#     
#     setTagsTop     - where begin work with HTML (from <top> to </top>)
#     setTagsNoWork  - this tags without work (skipping <nowork> and <nowork>,
#                      but text inside and inner tags is working) 
#     setTagsSkip    - this tags without work with its inner text and inner tags
#                      (without working from <skip> ... </skip>, for example: <script>)
#     setTagsXML     - only this tags writing in result 
#     
#     all this function have list parameter  
#     
#     
#     
#     
#     
#     
#     
#     07/06/2015 - updating and testing
#     
#--------------------------------------------------------------------

class wellHTML (HTMLParser):

    nCells = 0
    
    tagTable = 0
    indent = 0
    indentStep = 2;
    
    tagTop = ""

    tagStack = [];
    tagAttrs = [];
    tagDatas = [];
    tagSkip  = [];

    OkSkip       = False;

    tagsTop      = [];
    tagsNoWork   = [];
    tagsSkip     = [];
    tagsDataJoin = [];
    
    tagsXML      = [];

    result       = "";
    OkCRLF       = False;
    OkCRLFIndent = False;

    dictXMLwell  = { '>':"&gt;", '<':"&lt;", '&':'&amp;', '"':"&qout;", "'":"&apos;"}

    def getXMLW (self, data)     :
        new = (((((data.replace('>',"&gt;")).
                  replace('<',"&lt;")).
                 replace('&','&amp;')).
                replace('"',"&qout;")).
               replace("'","&apos;"));
        return new;
        
    def getResult (self)         : return self.result;
    def setResult (self,result ) : self.result = result;
    def setCRLF (self,CRLF)      : self.OkCRLF = CRLF;
    def getCRLF (self)           : return(self.OkCRLF);
    def setIndent (self,OkIndent): self.OkCRLFIndent = OkIndent and self.OkCRLF;
    def getIndent (self)         : return(self.OkCRLFIndent);

# 
# updates 2016-03-05 : don't regenerate dublicate attributes in function writeXML1 and writeXMLb
#

    def writeXML1(self,tag,attrs=[]) :
        if self.OkCRLFIndent : self.result += "".rjust(self.indentStep*self.tagTable," ")
        self.result += '<?'+self.getXMLW(tag);
        aLast = [] 
        for a in attrs :
            if (a[1]!=None) and (a[0] not in aLast) : 
                self.result += " "+self.getXMLW(a[0])+'="'+self.getXMLW(a[1])+'"';
                aLast.append(a[0])
        self.result += "?>";
        if self.OkCRLF : self.result += "\n"

    def writeXMLb(self,tag,attrs=[]) :
        if self.OkCRLFIndent : self.result += "".rjust(self.indentStep*self.tagTable," ")
        self.result += '<'+self.getXMLW(tag); 
        aLast = [] 
        for a in attrs :
            if (a[1]!=None) and (a[0] not in aLast) : 
                self.result += " "+self.getXMLW(a[0])+'="'+self.getXMLW(a[1])+'"';
                aLast.append(a[0])
#######     if a[1]==None : self.result += " "+a[0]; # Defining that this is not weel-known 07/06/2015
        self.result += ">";
        if self.OkCRLF : self.result += "\n"

    def writeXMLe(self,tag,attrs=[],data="") :
        if self.OkCRLFIndent : self.result += "".rjust(self.indentStep*(self.tagTable+1)," ")
        self.result += "</"+self.getXMLW(tag)+">";
        if self.OkCRLF : self.result += "\n"

    def writeXMLtext(self,text)  :
        if self.OkCRLFIndent : self.result += "".rjust(self.indentStep*(self.tagTable+1)," ")
        self.result += self.getXMLW(text);
        if self.OkCRLF : self.result += "\n"

    def writeFile(self,data)     : self.writeXMLtext(data)

    def setTagsTop (self,tags):
        self.tagsTop = tags;
    def setTagsNoWork (self,tags):
        self.tagsNoWork = tags;
    def setTagsSkip (self,tags):
        self.tagsSkip = tags;
    def setTagsDataJoin (self,tags):
        self.tagsDataJoin = tags
    def setTagsXML (self,tags):
        self.tagsXML = tags
        
    def OkTagTop (self,tag,attrs):
        OK = False;
        if (self.tagsTop==[]) : OK = True; return OK;
        for (t,a,join) in self.tagsTop :
            if (t==tag) :
                if (a==[]) : OK = True; break;
                for (cIn,vIn) in attrs:
                    for (cT,vT) in a:
                        if (cIn==cT) and ((vIn==vT)) : OK = True; return OK
        return OK
    
    def OkTagNoWork (self,tag,attrs):
        OK = False;
        if (self.tagsNoWork==[]) : OK = False; return OK;
        for (t,a,join) in self.tagsNoWork :
            if (t==tag) : OK = True; break;
#                if (a==[]) : OK = True; return OK;
#                for (cIn,vIn) in attrs:
#                    for (cT,vT) in a:
#                        if (cIn==cT) and ((vIn==vT)) : OK = True; return OK
        return OK
    
    def OkTagDataJoin (self,tag,attrs):
        OK = False;
        if (self.tagsDataJoin==[]) : OK = False; return OK;
        for (t,a,join) in self.tagsDataJoin :
            if (t==tag) :
                if (a==[]) : OK = True; break;
                for (cIn,vIn) in attrs:
                    for (cT,vT) in a:
                        if (cIn==cT) and ((vIn==vT)) : OK = True; return OK
        return OK
    
    def OkTagSkip (self,tag,attrs):
        OK = False;
        if (self.tagsSkip==[]) : OK = False; return OK;
        for (t,a,join) in self.tagsSkip :
            if (t==tag) :
                if (a==[]) : OK = True; break;
                for (cIn,vIn) in attrs:
                    for (cT,vT) in a:
                        if (cIn==cT) and ((vIn==vT)) : OK = True; return OK
        return OK
    
    def OkTagXML (self,tag,attrs):
        OK = False;
        if (self.tagsXML==[]) : OK = True; return OK;
        for (t,a,join) in self.tagsXML :
            if (t==tag) :
                if (a==[]) : OK = True; break;
                for (cIn,vIn) in attrs:
                    for (cT,vT) in a:
                        if (cIn==cT) and ((vIn==vT)) : OK = True; return OK
        return OK
    
    def handle_starttag (self, tag, attrs):
        if printDebug : print ("starttag:",tag,attrs)
        if (self.OkTagNoWork(tag,attrs)) : return;
        if (self.tagTable>0) :
            self.tagTable +=1;
            self.tagStack.append(tag);
            self.tagAttrs.append(attrs);
            self.tagDatas.append("");
#            print(self.tagSkips,self.tagTable)
            self.tagSkips.append(self.OkTagSkip(tag,attrs) or self.tagSkips[self.tagTable-2]) 
            
        if (self.OkTagTop(tag,attrs))&(len(self.tagStack)==0) :
            self.tagTable=1; self.tagTop=tag; self.nCells+=1
            self.tagStack = [tag];
            self.tagAttrs = [attrs];
            self.tagDatas = [""];
            self.tagSkips = [False];
            self.indent   = 0;
        if (len(self.tagStack)>=1) :
            self.indent = self.indentStep*self.tagTable;
            OkSkip      = self.tagSkips[self.tagTable-1]
            if  self.OkTagXML(tag,attrs) and not OkSkip:
                self.writeXMLb(tag,attrs);
            
        return
    
    def handle_endtag (self, tag) :
        if printDebug : print ("endtag :",tag)
        if (self.OkTagNoWork(tag,[])) : return;
        if (self.tagTable>0) :
            pTag = self.tagStack.pop();
            while not (pTag==tag) :
                if printDebug1 : print("ending1",tag,pTag,self.tagTable)
                if (len(self.tagStack)==0) : break;
                self.indent = self.indentStep*len(self.tagStack);
                rData       = self.tagDatas.pop();
                rAttr       = self.tagAttrs.pop()
                OkSkip      = self.tagSkips.pop()
                if (len(rData)>0) and not OkSkip:
                    self.writeFile(rData);
#                    print (" ".ljust(self.indent+self.indentStep), tag, "-", rData)

                if printDebug1 : print("ending1.5",tag,pTag,self.tagTable,self.tagAttrs)
                if  self.OkTagXML(pTag,rAttr) and not OkSkip : self.writeXMLe(pTag,rAttr,rData);
                self.tagTable = len(self.tagStack);    
                if (len(self.tagStack)==0) : pTag = ""; break;
                pTag = self.tagStack.pop();
                
            if printDebug1 : print("ending2",tag,pTag,self.tagTable)
            self.tagTable = len(self.tagStack);
            self.indent = self.indentStep*self.tagTable;
            rData       = self.tagDatas[self.tagTable];
            OkSkip      = self.tagSkips[self.tagTable];
            if printDebug1 : print("ending3",tag,pTag,self.tagTable,OkSkip,rData)
            if (len(rData)>0) and not OkSkip:
                self.writeFile(rData);
#                print (" ".ljust(self.indent+self.indentStep), tag, "-", rData)
            if printDebug1 : print("ending4",tag,pTag,self.tagTable,self.OkTagXML(tag,self.tagAttrs[self.tagTable]))
            if  self.OkTagXML(tag,self.tagAttrs[self.tagTable]) and not OkSkip :
                if printDebug1 : print("ending5",tag,pTag,self.tagTable)
                self.writeXMLe(tag,self.tagAttrs[self.tagTable],rData);
            del self.tagAttrs[(self.tagTable):len(self.tagAttrs)]
            del self.tagDatas[(self.tagTable):len(self.tagDatas)]
            del self.tagSkips[(self.tagTable):len(self.tagSkips)]
            
        if self.tagTable>0 :
#            print (" ".ljust(self.indent), tag, " ----", self.tagTable)
            self.indent = self.indentStep*self.tagTable;
            
        if self.tagTable==0 : self.indent=0; self.OkSkip=False;
        
        return
    
    def handle_data (self, data) :
        if self.tagTable>0 :
            rData = data.strip()
            if len(rData)>0:
                self.tagDatas[self.tagTable-1]=(self.tagDatas[self.tagTable-1] + " " + rData).strip();
        return

    def close (self) :
        while (self.tagTable>0) : self.handle_endtag(self.tagStack[self.tagTable-1]);




#--------------------------------------------------------------------
#--------------------------------------------------------------------

def HTMLtoXML (htmlFile, xmlFile, OkCRLF=False, OkIndent=False):

    uFile = os.path.abspath(htmlFile);
    uf=open(uFile,'r'); ufl=uf.read(); uf.close()
        
    p=wellHTML(); p.setCRLF(OkCRLF); p.setIndent(OkIndent);

    tagsNoWork = [("p",[],[]),
                  ("br",[],[]),
                  ("small",[],[]),
                  ("strong",[],[]),
                  ("nobr",[],[])];

    tagsSkip = [("script",[],[]),
                ("style",[],[]),
                ("div",[('id','menu')],[]),
                ("link",[],[])];

    p.setTagsNoWork(tagsNoWork);
    p.setTagsSkip(tagsSkip);
    
    p.writeXML1('xml',[['version',"1.0"],['encoding',"windows-1251"]]);

    p.writeXMLb("bulletin",[]);

    p.feed(ufl)
        
    p.writeXMLe("bulletin");
    p.close();
    
    if (xmlFile!="") : uFile = os.path.abspath(xmlFile); uf=open(uFile,'w'); ufl=uf.write(p.getResult()); uf.close()

    return p.getResult() ;

import xml.etree.ElementTree as ET

def XMLDetail (xmlStr) :

    pA1 = pA2 = pA3 = pA4 = "";

    try :
            root = ET.fromstring(xmlStr);                           #print(rf1);
            pAddress = root.find(".//div[@itemprop='address']");    #ET.dump(pAddress);
            pa1 = root.find(".//meta[@itemprop='addressCountry']"); #ET.dump(pa1)
            pa2 = root.find(".//meta[@itemprop='addressRegion']");
            pa3 = root.find(".//meta[@itemprop='addressLocality']");
            pa4 = root.find(".//meta[@itemprop='streetAddress']");

            pA1 = pa1.get("content");
            pA2 = pa2.get("content");
            pA3 = pa3.get("content");
            pA4 = pa4.get("content");

    except :
            address = [pA1,pA2,pA3,pA4]
    finally :
            address = [pA1,pA2,pA3,pA4]
    
    return [address]

if  (__name__ == "__main__") :
        
    rf1='c://boba//programs//pyton//Far//Datas/BulletinX/10-5-sot-sobstvennost-na-saharnom-kljuche-35785502.html'
    rf1='c://boba//programs//pyton//Far//Datas/Bulletin/10-5-sot-sobstvennost-na-saharnom-kljuche-35785502.html'

    xml = HTMLtoXML("./Datas/Temp/x.html","./Datas/Temp/xml.html",True,True);
    xml = HTMLtoXML(rf1,"./Datas/Temp/xml1.html",True,True);
#    print(xml)
    adr = XMLDetail(xml);
    print(adr)
