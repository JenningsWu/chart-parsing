import copy
import pydot


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Arc:
    __index = 0

    def __init__(self, left, right, pos):
        self.left = left
        self.right = right
        self.pos = pos
        self.refs = []
        self.index = self.__index
        self.__index += 1

    def __eq__(self, other):
        def listEq(l1, l2):
            return (len(l1) == len(l2) and
                    all(l1[i] == l2[i] for i in xrange(len(l1))))

        return (self.left == other.left and
                listEq(self.right, other.right) and
                self.pos == other.pos and self.pos == 0)

    def __hash__(self):
        return hash(str(self.index))

    def addRef(self, ref):
        self.refs.append(ref)

    def setRange(self, i, j):
        self.i = i
        self.j = j

    def incPos(self):
        self.pos += 1

    def isEnd(self):
        return self.pos == len(self.right)

    def nextName(self):
        return self.right[self.pos]


class ChartEle:

    def __init__(self, name, i, j):
        self.name = name
        self.i = i
        self.j = j
        self.refs = []

    def setIndex(self, index):
        self.index = index

    def setRefs(self, refs):
        self.refs = list(refs)

    def getName(self):
        return self.name + "(" + str(self.index) + ")"


Agend0 = [ChartEle("N", 0, 1),
          ChartEle("N", 1, 2),
          ChartEle("V", 1, 2),
          ChartEle("Poss", 2, 3),
          ChartEle("N", 3, 4),
          ChartEle("V", 3, 4),
          ChartEle("P", 4, 5),
          ChartEle("Inf", 4, 5),
          ChartEle("N", 5, 6),
          ChartEle("V", 5, 6),
          ChartEle("P", 6, 7),
          ChartEle("Inf", 6, 7),
          ChartEle("N", 7, 8)
          ]

Agend1 = [ChartEle("N", 0, 1),
          ChartEle("N", 1, 2),
          ChartEle("V", 1, 2),
          ChartEle("P", 2, 3),
          ChartEle("N", 3, 4),
          ChartEle("V", 3, 4)
          ]

Agend2 = [ChartEle("N", 0, 1),
          ChartEle("N", 1, 2),
          ChartEle("V", 1, 2),
          ChartEle("Poss", 2, 3),
          ChartEle("N", 3, 4),
          ChartEle("P", 4, 5),
          ChartEle("N", 5, 6),
          ChartEle("V", 5, 6)
          ]

Agend3 = [ChartEle("N", 0, 1),
          ChartEle("N", 1, 2),
          ChartEle("V", 1, 2),
          ChartEle("N", 2, 3),
          ChartEle("V", 2, 3),
          ]

Agend4 = [ChartEle("N", 0, 1),
          ChartEle("N", 1, 2),
          ChartEle("V", 1, 2),
          ChartEle("N", 2, 3),
          ChartEle("V", 2, 3),
          ChartEle("P", 3, 4),
          ChartEle("N", 4, 5)
          ]


Agenda = [ChartEle("N", 0, 1),
          ChartEle("V", 1, 2),
          ChartEle("N", 2, 3),
          ChartEle("P", 3, 4),
          ChartEle("N", 4, 5)
          ]

Agenda.reverse()

Rule2 = {"S": [["NP", "VP"]],
         "NP": [["N"], ["Poss", "N"], ["N", "PP"], ["Poss", "N", "PP"],
                ["N", "IP"], ["Poss", "N", "IP"], ["N", "PP", "IP"],
                ["Poss", "N", "PP", "IP"]],
         "VP": [["V"], ["V", "NP"], ["V", "PP"], ["V", "NP", "PP"]],
         "PP": [["P", "N"]],
         "IP": [["Inf", "VP"]]}

Rules = {"S": [["NP", "VP"]],
         "NP": [["N"], ["N", "PP"]],
         "VP": [["V", "NP"], ["V", "NP", "PP"]],
         "PP": [["P", "NP"]]}

res = []
chart = []
ArcsCache = []
Arcs = [[set() for _ in xrange(9)] for _ in xrange(9)]

tmp = set()
for right in Rules["S"]:
    Arcs[0][0].add(Arc("S", right, 0))
    tmp.add(right[0])
for left in tmp:
    for right in Rules[left]:
        Arcs[0][0].add(Arc(left, right, 0))

index = 0
while Agenda:
    c = Agenda.pop()
    index += 1
    c.setIndex(index)
    chart.append(c)
    if c.name is "S" and c.i == 0 and c.j == 5:
        res.append(c)
        continue
    stepA = set()
    for k in xrange(c.i + 1):
        for arc in Arcs[k][c.i]:
            if not arc.isEnd() and arc.right[arc.pos] is c.name:
                tmp = copy.deepcopy(arc)
                tmp.addRef(c)
                tmp.incPos()
                tmp.setRange(k, c.j)
                Arcs[k][c.j].add(tmp)
                stepA.add(tmp)
    for arc in stepA:
        if not arc.isEnd():
            if arc.nextName() in Rules:
                for right in Rules[arc.nextName()]:
                    Arcs[arc.j][arc.j].add(
                        Arc(arc.nextName(), right, 0))
        else:
            ele = ChartEle(arc.left, arc.i, arc.j)
            ele.setRefs(arc.refs)
            Agenda.append(ele)

index = 0
for x in res:
    graph = pydot.Dot(graph_type='graph')
    print ("========= " +
           str(index + 1) +
           " parse trees!" +
           "==========")
    stack = [x]
    nextS = []
    ret = []
    layer = 0
    while stack:
        layer += 1
        while stack:
            now = stack.pop(0)
            ret.append(now.name)
            nextS += now.refs
            for ref in now.refs:
                graph.add_edge(pydot.Edge(now.getName(),
                                          ref.getName()))
        stack = nextS
        nextS = []
        print ret
        ret = []
    graph.write_png("p1-" + str(index) + ".png")
    index += 1
