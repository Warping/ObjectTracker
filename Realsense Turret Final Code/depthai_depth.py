# Write a class that gets the depth and RGB frames from an OAK-D camera and processes them to get the depth of a target.
import depthai as dai
import numpy as np

class OakDepthCam:
    def __init__(self, res=(1280, 720), colorFps=30, depthFps=30):
        self.depthRes = res
        self.colorRes = res
        fps = max(colorFps, depthFps)
        self.pipeline = dai.Pipeline()
        self.device = dai.Device()
        self.queueNames = []
        # self.depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
        # self.colorQueue = device.getOutputQueue(name="color", maxSize=4, blocking=False)
        self.camRgb = self.pipeline.create(dai.node.Camera)
        left = self.pipeline.create(dai.node.MonoCamera)
        self.right = self.pipeline.create(dai.node.MonoCamera)
        self.stereo = self.pipeline.create(dai.node.StereoDepth)

        rgbOut = self.pipeline.create(dai.node.XLinkOut)
        dispOut = self.pipeline.createXLinkOut()

        rgbOut.setStreamName("rgb")
        dispOut.setStreamName("disp")
        self.queueNames.append("rgb")
        self.queueNames.append("disp")

        self.camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        self.camRgb.setSize(res[0], res[1])
        self.camRgb.setFps(fps)

        left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        left.setCamera("left")
        left.setFps(fps)

        self.right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.right.setCamera("right")
        self.right.setFps(fps)

        self.stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        self.stereo.setLeftRightCheck(True)
        self.stereo.setConfidenceThreshold(200)
        self.stereo.setDepthAlign(dai.CameraBoardSocket.RGB)

        # Linking
        self.camRgb.video.link(rgbOut.input)
        left.out.link(self.stereo.left)
        self.right.out.link(self.stereo.right)
        self.stereo.disparity.link(dispOut.input)

        self.camRgb.setMeshSource(dai.CameraProperties.WarpMeshSource.CALIBRATION)

        # Connect to device and start pipeline
        self.device.startPipeline(self.pipeline)

    def get_frame(self):
        latestPacket = {}
        latestPacket["rgb"] = None
        latestPacket["disp"] = None
        frameRgb = None
        frameDisp = None

        queueEvents = self.device.getQueueEvents(("rgb", "disp"))
        for queueName in queueEvents:
            packets = self.device.getOutputQueue(queueName).tryGetAll()
            if len(packets) > 0:
                latestPacket[queueName] = packets[-1]

        if latestPacket["rgb"] is not None:
            frameRgb = latestPacket["rgb"].getCvFrame()
            frameRgb = np.ascontiguousarray(frameRgb)

        if latestPacket["disp"] is not None:
            frameDisp = latestPacket["disp"].getCvFrame()
            maxDisparity = self.stereo.initialConfig.getMaxDisparity()
            # Optional, extend range 0..95 -> 0..255, for a better visualisation
            frameDisp = (frameDisp * 255. / maxDisparity).astype(np.uint8)
            frameDisp = np.ascontiguousarray(frameDisp)
        
        return True, None, frameDisp, frameRgb
    
    # Write a function that gets the 3D point of a pixel in the depth frame
    def get3d(self, x, y, distance):
        return (0, 0, 0)
        

