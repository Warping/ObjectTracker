import cv2
import numpy as np

class TargetViewer:
    def __init__(self, windowSize=(640, 480), xRange=(-4.0, 4.0), yRange=(0, 8.0)):
        self.targetPositions = []
        self.windowSize = windowSize
        self.yRange = yRange
        self.xRange = xRange
    
    def addPosition(self, position):
        self.targetPositions.append(position)

    def clearPositions(self):
        self.targetPositions = []
    
    def posToPixel(self, pos):
        x = int((pos[0] - self.xRange[0]) / (self.xRange[1] - self.xRange[0]) * self.windowSize[0])
        y = int((pos[1] - self.yRange[0]) / (self.yRange[1] - self.yRange[0]) * self.windowSize[1])
        return x, y
    
    def draw(self):
        img = np.zeros((self.windowSize[1], self.windowSize[0], 3), np.uint8)
        x0, y0 = self.posToPixel((0, 0))
        for pos in self.targetPositions:
            temp_pos = (pos[0], pos[2])
            x, y = self.posToPixel(temp_pos)
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
            cv2.line(img, (x0, y0), (x, y), (255, 255, 0), 1)
        # Draw turret position at 0, 0
        x, y = self.posToPixel((0, 0))
        cv2.circle(img, (x, y), 4, (255, 255, 255), -1)
        return img