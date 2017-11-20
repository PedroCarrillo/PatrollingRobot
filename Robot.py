class Robot:

    id = "Unknown Id"

    initialPosition = (0, 0)
    currentPosition = (0, 0)

    def __init__(self, id, initialPosition):
        self.id = id
        self.initialPosition = initialPosition
        self.currentPosition = initialPosition