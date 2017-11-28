class Robot:
    ids = {"U": (-1,0), "R": (0, 1), "D": (1,0), "L": (0, -1)}
    directions = [(-1,0), (0,1), (1,0), (0, -1)]

    id = "Unknown Id"

    initialPosition = (0, 0)
    currentPosition = (0, 0)
    direction = "R"

    def __init__(self, id, initialPosition):
        self.id = id
        self.initialPosition = initialPosition
        self.currentPosition = initialPosition

    def moveToPosition(self, newPosition):
        r = newPosition[0] - self.currentPosition[0]
        c = newPosition[1] - self.currentPosition[1]
        newDirectionIndex = self.directions.index((r,c))
        currentDirectionIndex = self.directions.index(self.ids[self.direction])
        degreeRotation = (newDirectionIndex - currentDirectionIndex) * 90
        print degreeRotation
        print degreeRotation == 180 or degreeRotation == -180
        if degreeRotation == 180 or degreeRotation == -180:
            if self.direction == "U":
                self.direction = "D"
            elif self.direction == "D":
                self.direction = "U"
            elif self.direction == "R":
                self.direction = "L"
            elif self.direction == "L":
                self.direction = "R"
            print "rotate two times to any side"
        elif degreeRotation == 90:
            self.direction = "R"
            print "rotate right"
        elif degreeRotation == -90:
            self.direction = "L"
            print "rotate left"
        else:
            print "Asdasda"
        print "move forward"
