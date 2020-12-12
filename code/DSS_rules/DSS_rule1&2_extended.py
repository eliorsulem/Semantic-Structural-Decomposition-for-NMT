
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
        #Hscenes = [e.child for e in n.outgoing if e.tag == 'H']
        if Hscenes != []:
            H.append(Hscenes)
    H = sum(H,[])
    #print(H)
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

def get_EAscenes(P):
    """
    P is a ucca passage. Return all the Escenes and Ascenes in each passage and their corresponding minimal center
    """
    nodes = [x for x in P.layer("1").all if x.tag == "FN"]
    E = []
    C = []
    for n in nodes:
        EAscenes = [e.child for e in n.outgoing if (e.tag == 'E' or e.tag == 'A') and e.child.is_scene()]
        Escenes = [e.child for e in n.outgoing if e.tag == 'E' and e.child.is_scene()]
        Ascenes = [e.child for e in n.outgoing if e.tag == 'A' and e.child.is_scene()]
        if EAscenes != []:
            E.append(EAscenes)
            for pa in EAscenes:
                if pa in Escenes:
                    centers = [e.child for e in n.outgoing if e.tag == 'C' ]# find the minimal center
                    if centers != []:
                        while centers != []:
                            for c in centers:
                                ccenters = [e.child for e in c.outgoing if e.tag == 'C']
                            lcenters = centers
                            centers = ccenters
                        C.append(lcenters)
                    else:
                        C.append(['*'])
                elif pa in Ascenes:
                    scenters = [e.child for e in pa.outgoing if e.tag == 'P' or e.tag == 'S']
                    for scc in scenters:
                        centers = [e.child for e in scc.outgoing if e.tag == 'C']
                        if centers != []:
                            while centers != []:
                                for c in centers:
                                    ccenters = [e.child for e in c.outgoing if e.tag == 'C']
                                lcenters = centers
                                centers = ccenters
                            C.append(lcenters)
                        else:
                            C.append(scenters)





    E = sum(E,[])
    C = sum(C,[])
    y = P.layer("0")
    output1 = []
    center = []

    for sc in E:
        p = []
        d = sc.get_terminals(False,True)
        for i in list(range(0,len(d))):
            p.append(d[i].position)
        output2 = []
        for k in p:
            if(len(output2)) == 0 or str(y.by_position(k)) != output2[-1]:
                output2.append(str(y.by_position(k)))

        output1.append(output2)

        #W = ['who','which','that']
        #for v in output1:
        #   u = [ z for z in v if z not in W ]
        #  output.append(u)

    for c in C:
        if c!= '*':
            p = []
            d = c.get_terminals(False,True)
            for i in list(range(0,len(d))):
                p.append(d[i].position)
            output3 = []
            for k in p:
                if(len(output3)) == 0 or str(y.by_position(k)) != output3[-1]:
                    output3.append(str(y.by_position(k)))
            center.append(output3)
        else:
            center.append(c)

    return([output1,center])




def get_difference(h1,L2,C2):
    """
    h1 is the parallel Scene (string), L2 is the list of embedded Scenes (string), C2 is the list of string centers.
    For each (l2,c2) in (L2,C2), recursively return L1+c2 without l2 and then l2.
    """
    E2 = []

    for c2 in C2:
        if c2 == '*':
            c2 = [['#']]*len(h1)
    #print(C2)

    for l2 in L2:
        j = L2.index(l2)
        #print(j)
        #print(l2)

        f = []

        if l2 != []:
            for m in range(0,len(h1)):
                if h1[m:m+len(l2)] == l2:
                    f.append([m,len(l2)])

        diff = []
        for i in f:
            d = list(range(i[0],i[0]+i[1]))
            diff.append(d)
        #print(h1)
        #print(diff)

        if diff != []:
            split2 = [element for i, element in enumerate(h1) if i not in diff[0] or element in C2[j]]
            h1 = split2


        else:
            split2 = h1


        m2 = []


        W = ['who','which','that']
        u = [ z for z in L2[j] if z not in W ]
        m2.append(u)
        if  m2 != [] and diff!=[]:
            E2.append(m2)

        asplit2 =[]
        asplit2.append(split2)


    if L2 != []:
        E2 = sum(E2,[])
        for e in E2:
            asplit2.append(e)

    else:
        asplit2 = [h1]

    return(asplit2)

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


index = list(range(0,1500))

for t in index:
    f1 = open('test.en.tupa_parsed/newsdiscusstest2015-enfr-src_%s.xml' %t)
    xml_string1 = f1.read()
    f1.close()
    xml_object1 = fromstring(xml_string1)
    P1 = convert.from_standard(xml_object1)
    L1 = get_Hscenes(P1)
    L2 = get_EAscenes(P1)[0]
    C2 = get_EAscenes(P1)[1]
    T = get_passage(P1)
    D = to_word_text(P1)

    split12 = []
    for h in L1:
        D1 = get_difference(h,L2,C2)
        split12.append(D1)

    S1 = sum(split12,[])
    s = open('12r%s.txt' %t, 'w')
    if S1!=[]:
       s.write('%s\n' %S1)
    elif T!= []:
         s.write('%s\n' %[T])
    else:
        s.write('%s\n' %[D])
    #s.write(str(L1))
    #s.write(str(L2))
    s.close()