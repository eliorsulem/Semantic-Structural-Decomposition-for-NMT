


import re

from ucca import layer0, layer1, convert, core
from xml.etree.ElementTree import ElementTree, tostring, fromstring
import sys
import operator




def get_Hscenes(P):
    """
    P is a ucca passage. Return all the Hscenes in each passage
    """
    nodes = [x for x in P.layer("1").all if x.tag == "FN"]
    H = []
    for n in nodes:
        Hscenes = [e.child for e in n.outgoing if e.tag == 'H' and e.child.is_scene()]
        if Hscenes != []:
            H.append(Hscenes)
    H = sum(H,[])
    y = P.layer("0")
    output = []
    for sc in H:
        p = []
        d = sc.get_terminals(False,True)
        for i in list(range(0,len(d))):
            p.append(d[i].position)
        output2 = []
        for k in p:
            if(len(output2)) == 0:
                output2.append(str(y.by_position(k)))
            elif str(y.by_position(k)) != output2[-1]:
                output2.append(str(y.by_position(k)))

        output.append(output2)

    return(output)


def get_passage(P):
    """
   P is a ucca passage. Return the passage as a string.
    """
    root = [x for x in P.layer("1").all if x.tag == "FN" and x.fparent == None]
    #R = []
    #for n in nodes:
    #    root = [e.child for e in n.incoming if e.parent == None]
    #    if root !=[]:
    #       R.append(root[0])
    y = P.layer("0")
    p = []
    d = root[0].get_terminals(False,True)
    for i in list(range(0,len(d))):
        p.append(d[i].position)
    output = []
    for k in p:
        if(len(output)) == 0:
            output.append(str(y.by_position(k)))
        elif str(y.by_position(k)) != output[-1]:
            output.append(str(y.by_position(k)))
    return(output)

def to_word_text(P):
    """Converts from a Passage object to tokenized strings.
    """

    tokens = [x.text for x in sorted(P.layer(layer0.LAYER_ID).words, key=operator.attrgetter('position'))]

    starts = [0, len(tokens)]
    return [' '.join(tokens[starts[i]:starts[i + 1]])
            for i in range(len(starts) - 1)]


index = list(range(0,3003))


for t in index:
    f1 = open('newstest2014-fren-src_tupa.parsed/newstest2014-fren-src.en-skipline_%s.xml' %t) 
    xml_string1 = f1.read()
    f1.close()
    xml_object1 = fromstring(xml_string1)
    P1 = convert.from_standard(xml_object1)     #Fully automatic: from_standard, Semi-automatic: from_site
    L1 = get_Hscenes(P1)
    if L1 == []:
        L1 = get_passage(P1)
        L1 = [L1]
        if L1 ==[[]]:
            L1 = to_word_text(P1)
            L1 = [L1]
    s = open('1r%s.txt' %t, 'w')
    s.write('%s\n' %L1)
    s.close()

