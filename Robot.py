# Imports need for the movement of the robot
import time
import create2api
# Imports needed for image processing
import threading
import numpy as np
import cv2
# import time
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera


class Robot:
    # Variables for the robotics lab, this will change every new scenario
    rotationVelocity = 50
    movementVelocity = 100
    ninetyRotationSleep = 3.25
    movementSpeedSleep = 2.65

    bot = None

    ids = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    id = "Unknown Id"

    initialPosition = (0, 0)
    currentPosition = (0, 0)
    direction = "U"
    cameraThread = None

    def __init__(self, id, initialPosition):
        self.id = id
        self.initialPosition = initialPosition
        self.currentPosition = initialPosition
        self.bot = create2api.Create2()
        self.bot.start()
        self.bot.safe()
        cameraThread = CameraThread(self.bot)
        cameraThread.start()

    def moveToPosition(self, newPosition):
        r = newPosition[0] - self.currentPosition[0]
        c = newPosition[1] - self.currentPosition[1]
        newDirectionIndex = self.directions.index((r, c))
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
            self.turnRight()
            self.turnRight()
            print "rotate two times to any side"
        elif degreeRotation == 90:
            if self.direction == "U":
                self.direction = "R"
            elif self.direction == "D":
                self.direction = "L"
            elif self.direction == "R":
                self.direction = "D"
            elif self.direction == "L":
                self.direction = "U"
            self.turnRight()
            print "rotate right"
        elif degreeRotation == -90:
            self.turnLeft()
            if self.direction == "U":
                self.direction = "L"
            elif self.direction == "D":
                self.direction = "R"
            elif self.direction == "R":
                self.direction = "U"
            elif self.direction == "L":
                self.direction = "D"
            print "rotate left"
        self.moveForward()
        print "move forward"

    def turnRight(self):
        self.rotation(self.rotationVelocity, self.ninetyRotationSleep)

    def turnLeft(self):
        self.rotation(self.rotationVelocity * -1, self.ninetyRotationSleep)

    def moveForward(self):
        self.move(self.movementVelocity)

    def moveBackwards(self):
        self.move(self.movementVelocity * -1)

    def stop(self):
        self.bot.drive_straight(0)

    def move(self, velocity):
        self.bot.drive_straight(velocity)
        time.sleep(self.movementSpeedSleep)
        self.stop()

    def rotation(self, rotationVelocity, ninetyRotationSleep):
        self.bot.turn_clockwise(rotationVelocity)
        time.sleep(ninetyRotationSleep)
        self.stop()

    def endConnection(self):
        self.bot.stop()
        self.bot.destroy()


class CameraThread(threading.Thread):
    marker_path = 'intruder.jpg'
    marker_intruder = cv2.resize(cv2.imread(marker_path), (0, 0), fx=0.5, fy=0.5)
    marker_intruder = cv2.cvtColor(marker_intruder, cv2.COLOR_BGR2GRAY)
    threshold = .7
    storedMarkers = {}
    scales = [0.4, 0.7, 1]
    robot = None

    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self):
        # First we will scale the marker once so we don't resize them each time
        self.storingMarkerScale(self.marker_intruder)
        self.startCamera()

    # this method is for reference only. This only works with an image no scalation
    def template_matching(self, image, marker):
        w, h = marker.shape[::-1]
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        res = cv2.matchTemplate(image_gray, marker, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    def storingMarkerScale(self, marker):
        for scale in self.scales:
            resized = imutils.resize(marker, width=int(marker.shape[1] * scale))
            self.storedMarkers[str(scale)] = resized

    # This method takes in consideration 3 resized images for the marker
    # It will apply template matching for the scale you consider helpful
    # Remember that it will run template matching so it will be heavy for the camera frames
    def multiScaleTemplateMatching(self, image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        found = []
        w = 0
        h = 0
        for scale in self.scales:
            marker = self.storedMarkers[str(scale)]
            w, h = marker.shape[::-1]
            res = cv2.matchTemplate(image_gray, marker, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.threshold)
            if zip(*loc[::-1]):
                found = zip(*loc[::-1])
                break
        if found:
            self.robot.play_note("G5", 20)
        for pt in found:
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    # initializing the camera
    def startCamera(self):
        print("Warming up camera")
        resolution = (640, 480)

        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = 16

        rawCapture = PiRGBArray(self.camera, size=resolution)

        time.sleep(0.1)
        print "Starting to patrol"
        for f in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame = f.array
            self.multiScaleTemplateMatching(frame)
            cv2.imshow("Security", frame)
            key = cv2.waitKey(1) & 0xFF

            rawCapture.truncate(0)

            if key == ord("q"):
                break




