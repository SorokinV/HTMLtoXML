import unittest
from wellHTML import wellHTML

class TestWellHTML(unittest.TestCase):

    def setUp(self):
        """
        ufl = "<html></html>"
        
        p=wellHTML();
        p.setPathFile(xmlFile);
        p.openFile();

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
        p.writeXMLtext('<?xml version="1.0" encoding="windows-1251" ?>');
        p.writeXMLtext("<bulletin>");

        # 1. head/details/title common description

        p.writeXMLtext("<header>");
        tagsTop = [('head',[],[])];
        p.setTagsTop(tagsTop);

        tagsXML = [('meta',[('name','description')],[])]
        p.setTagsXML(tagsXML);

        p.feed(ufl)

        p.writeXMLtext("</header>");
    
        # 2. bulletin body common

        p.writeXMLtext("<bodycommon>");
        tagsTop = [('div',[('id','content')],[])];
        p.setTagsTop(tagsTop);
        tagsXML = [('meta',[],[]),
                   ('span',[],[]),
                   ('div',[('class','text fieldset')],[])];
        p.setTagsXML(tagsXML);
        p.feed(ufl)
        p.writeXMLtext("</bodycommon>");

        # 3. brief owner information
        
        p.writeXMLtext("<userinfo>");
        tagsTop = [('div',[('class','ownerInfoInner')],[])];
        p.setTagsTop(tagsTop);
        tagsXML = [('div',[('class','ownerInfoInner')],[]),
                   ('a',[('class','bigbutton viewAjaxContacts')],[]),
                   ('span',[],[])];
        p.setTagsXML(tagsXML);
        p.feed(ufl)
        p.writeXMLtext("</userinfo>");
        p.writeXMLtext("</bulletin>");
        p.closeFile();
        """
        
    def test_empty(self):

        ufl = ""
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,ufl)

    def test_simple0(self):

        ufl = ""
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,ufl)

    def test_simple1(self):

        ufl = "<html></html>"
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,ufl)

    def test_simple2(self):

        ufl = "<html><html><html></html></html><html></html><html></html></html>"
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,ufl)

    def test_simple3(self):

        ufl = "<html><html><html></html></html>"
        uflr= "<html><html><html></html></html></html>"
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_simple4(self):

        ufl = "</html>"
        uflr= ""
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_simple5(self):

        ufl = "</html></html>"
        uflr= ""
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_simple6(self):

        ufl = "<html></html></html></html></html><html></html>"
        uflr= "<html></html><html></html>"
        p=wellHTML(); p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_Data1(self):

        ufl = "<html>a1<html>a2</html></html>"
        uflr= "<html><html>a2</html>a1</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_Data2(self):

        ufl = "<html>a1<html>a2</html>a3<html1>a7</html1>a5</html>"
        uflr= "<html><html>a2</html><html1>a7</html1>a1 a3 a5</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_ATTR1(self):

        ufl = "<html>a1<html xx=25>a2</html></html>"
        uflr= "<html><html xx=\"25\">a2</html>a1</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_ATTR2(self):

        ufl = "<html>a1<html1 xx>a2</html1></html>"
        uflr= "<html><html1>a2</html1>a1</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_ATTR3(self):

        ufl = "<html>a1<html1 xx>a2<h2 xx=5></html1></html>"
        uflr= "<html><html1><h2 xx=\"5\"></h2>a2</html1>a1</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_ATTR4(self):

        ufl = "<html a='&a&&'>&&&\"'</html>"
        uflr= "<html a=\"&amp;a&amp;&amp;\">&amp; &amp; &amp; &qout;&apos;</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_ATTR5(self):

        ufl = "<html>a1<html1 xx=1 xx=2 xx=3>a2<h2 xx=5></html1></html>"
        uflr= "<html><html1 xx=1><h2 xx=\"5\"></h2>a2</html1>a1</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_ATTR6(self):

        ufl = "<html>a1<html1 xx=1 xx=2 xx='3' /></html>"
        uflr= "<html><html1 xx=1/>a1</html>"
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_Top1(self):

        ufl = "<html><html></html></html>"
        uflr= ufl
        p=wellHTML();
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_Top2(self):

        ufl = "<html></html></html>"
        uflr= "<html></html>"
        p=wellHTML(convert_charrefs=True);
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_Top3(self):

        ufl = "<html></html><top><html></html><top1/></top>"
        uflr= "<html></html><html></html>"
        p=wellHTML(convert_charrefs=True);
        p.tagsTop = [('html',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    def test_Skip1(self):

        ufl = "<html></html><top><html><skip a=1></skip><skip b=4>123456789</skip></html><top1/></top>"
        uflr= "<html></html><html></html>"
        p=wellHTML(convert_charrefs=True);
        p.tagsTop = [('html',[],[])];
        p.tagsSkip = [('skip',[],[])];
#        p.writeXMLtext("<userinfo>");
#        p.writeXMLtext("</userinfo>");
        p.feed(ufl); p.close();
        
        result = p.getResult();
        self.assertEqual(result,uflr)

    """
        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)
    """

if __name__ == '__main__':
    unittest.main()
