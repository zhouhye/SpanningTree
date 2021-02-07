import unittest
from Topology import Topology
    
numPassed = 0
total = 0

class TopoTestCase(unittest.TestCase):
    global numPassed
    global total
    def setUp(self):
        numPassed=0
        total = 0
        # add new topographies here
        self.topos = [ 
        'Sample',
        'SimpleLoopTopo',
        'Test3Topo',
        'ComplexLoopTopo',
        'NoLoopTopo',
        'PptExampleTopo',
        '4dHyperCubeTopo',
        '6dHyperCubeTopo',
        'ComplexNonSequentialTopo',
        'DoubleInterconnectedTailTopo',
        'InterconnectionTopo',
        'NorthStarTopo',
        'OverlapRingTopo',
        'ShortTailTopo',
        'SnowflakeLoopTopo',
        'SnowflakeTopo',
        'StarHangerTopo',
        'VihnKhoaTon1Topo',
        'VihnKhoaTon2Topo',
        'VihnKhoaTon3Topo',
        'VihnKhoaTon4Topo',
        'TailTopo',
        'StarTopo'
        ]

    def tearDown(self):
        print("Passed = " + str(numPassed) + "/" + str(total))


    # assert_topology_spanning_tree() copied from run_spanning_tree.py
    def assert_topology_spanning_tree(self, inputFileName, expectedLog):
        #print("assert_topology_spanning_tree")
        actualFileName = 'TestOutput/'+inputFileName+'.log'
        print(actualFileName)
        topo = Topology(inputFileName)
        topo.run_spanning_tree()
        topo.log_spanning_tree(actualFileName)
        actualRead = open(actualFileName, "r")
        actualLog = actualRead.read()
        actualRead.close()
        # self.assertEquals(expectedLog, actualLog)
        self.silent_assert(self.assertEquals, expectedLog, actualLog)

    def each_topo_test(self, this_topo):
        #print("each_topo_test")
        expectedLogFileName = 'ExpectedOutput/'+this_topo+'.log'
        logRead = open(expectedLogFileName, "r")
        expectedLog = logRead.read()
        logRead.close()
        self.assert_topology_spanning_tree(this_topo, expectedLog)

    def test_all_topos(self):
        #print("test_all_topos")
        for testTopo in self.topos:
            self.each_topo_test(testTopo)

    def silent_assert(self, func, *args, **kwargs):
        global numPassed
        global total
        try:
            total = total + 1
            func(*args, **kwargs)
            numPassed = numPassed + 1
        except Exception as exc:
            print(exc)

unittest.main()
