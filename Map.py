from Robot import Robot
from copy import copy, deepcopy
from Destination import Destination


class Map:

    m = 0
    n = 0
    destinations = {}
    obstaclesPosition = []
    robotsPosition = {}
    mapMaze = [[]]

    OBSTACLE_ID = -1
    EMPTY_SPACE = 0


    def start(self, m, n, robotsPosition, destinations, obstaclesPosition):
        self.m = m
        self.n = n
        self.mapMaze = [[0 for x in range(m)] for y in range(n)]
        self.destinations = destinations
        self.obstaclesPosition = obstaclesPosition

        for obstacle in obstaclesPosition:
            self.mapMaze[obstacle[0]][obstacle[1]] = self.OBSTACLE_ID

        for key, value in robotsPosition.items():
            self.robotsPosition[key] = Robot(key, value)

        # for position in robotsPosition:
        #     # testRobot = Robot('testing', position)
        #     # self.mapMaze[position[0]][position[1]] = testRobot
        #     print testRobot.initialPosition

        # for dest in destinations:
        #     destination = Destination(dest[0], dest[1])
        #     map[destination.position[0]][destination.position[1]] = destination.identifier
        #     # print destination.identifier

        # print self.mapMaze[0][0]

    def moveRobot(self, destinationId, robotId):
        destinationPosition = self.destinations.get(destinationId)
        robotPosition = self.robotsPosition.get(robotId).currentPosition
        self.lookForPath(destinationPosition, robotPosition, robotId)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def lookForPath(self, destinationPoint, robotPosition, robotId):
        print "looking for " , destinationPoint[0] ," ",destinationPoint[1]
        print "robot in " , robotPosition[0] ," ",robotPosition[1]
        self.mapMaze[robotPosition[0]][robotPosition[1]] = 0
        tempMap = deepcopy(self.mapMaze)
        foundAPath = False

        count = 0
        self.findPath(tempMap, destinationPoint, robotPosition)
        #self.printMap(tempMap, self.m, self.n)
        self.movingThroughPath(tempMap, self.mapMaze, robotPosition, destinationPoint, robotId)
        print "new robot position", self.robotsPosition.get(robotId).currentPosition

    def findPath(self, matrix, destinationPoint, robotPosition):
        heap = []
        newHeap = []
        lastWave = 3
        matrix[destinationPoint[0]][destinationPoint[1]] = -2
        for dir in self.directions:
            newR = destinationPoint[0] + dir[0]
            newC = destinationPoint[1] + dir[1]
            if newR >= 0 and newR < self.m and newC >= 0 and newC < self.n and matrix[newR][newC] == self.EMPTY_SPACE:
                matrix[newR][newC] = 3
                heap.append((newR, newC))

        for currentWave in range(4, 100):
            lastWave = lastWave + 1
            while heap:
                position = heap.pop()
                for dir in self.directions:
                    newR = position[0] + dir[0]
                    newC = position[1] + dir[1]
                    if newR >= 0 and newR < self.m and newC >= 0 and newC < self.n and matrix[newR][newC] != self.OBSTACLE_ID:
                        if matrix[newR][newC] == self.EMPTY_SPACE and matrix[position[0]][position[1]] == currentWave-1:
                            matrix[newR][newC] = currentWave
                            newHeap.append((newR, newC))
                        if (newR, newC) == robotPosition:
                            print "found a robot at ", position
                            return

            if not newHeap:
                print "unreachable"
                return
            heap = newHeap
            newHeap = []

    def movingThroughPath(self, pathMap, map, robotPosition, destination, robotId):
        robotLevel = pathMap[robotPosition[0]][robotPosition[1]]
        print "this is the robot level ", robotLevel
        while (robotPosition != destination):
            map[robotPosition[0]][robotPosition[1]] = 0
            for dir in self.directions:
                if (pathMap[robotPosition[0]][robotPosition[1]] == 3):
                    robotPosition = destination
                else:
                    newR = dir[0] + robotPosition[0]
                    newC = dir[1] + robotPosition[1]
                    if self.isValidPoint(newR, newC, self.m, self.n) and pathMap[newR][newC] == (robotLevel - 1):
                        robotPosition = (newR, newC)
                        robotLevel = pathMap[newR][newC]
                        break
            self.robotsPosition.get(robotId).moveToPosition(robotPosition)
            self.robotsPosition.get(robotId).currentPosition = robotPosition
            print "move robot to position ", robotPosition
            map[robotPosition[0]][robotPosition[1]] = "   R"
            # print "====="
            #self.printMap(map, self.m, self.n)

        # self.printMap(map, self.m, self.n)

    def isValidPoint(self, newR, newC, m, n):
        return newR >= 0 and newR < m and newC >= 0 and newC < n

    def printMap(self, map, m, n):
        for i in range(m):
            for j in range(n):
                print '{:4}'.format(map[i][j]),
            print

if __name__ == '__main__':
    m = 6
    n = 6
    robotsPosition = {"R1": (5, 0)}
    obstaclesPosition = [(3,2), (2,3), (3,3)]
    destinations = {"A": (5,0), "C": (0,0), "D": (0,5), "B": (5,5), "E": (2,2)}
    map = Map()
    map.start(m, n, robotsPosition, destinations, obstaclesPosition)
    map.moveRobot("C", "R1")
    map.moveRobot("D", "R1")
    map.moveRobot("E", "R1")
    map.moveRobot("A", "R1")
    map.moveRobot("B", "R1")
    map.moveRobot("D", "R1")
