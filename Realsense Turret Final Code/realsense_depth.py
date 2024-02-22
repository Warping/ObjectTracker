import pyrealsense2 as rs
import numpy as np

exposure = 31000

class DepthCamera:
    def __init__(self, colorRes, depthRes, colorFPS, depthFPS):
        # Configure depth and color streams
        self.colorRes = colorRes
        self.depthRes = depthRes
        colorX = colorRes[0]
        colorY = colorRes[1]
        depthX = depthRes[0]
        depthY = depthRes[1]
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get profile of depth stream
        self.profile = config.resolve(rs.pipeline_wrapper(self.pipeline))

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # Configure depth and color streams

        # config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.depth, depthX, depthY, rs.format.z16, depthFPS)
        # config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.color, colorX, colorY, rs.format.bgr8, colorFPS)
        # config.enable_stream(rs.stream.infrared, 848, 480, rs.format.y8, 30)

        # Align depth to color
        align_to = rs.stream.color
        self.align = rs.align(align_to)

        # Adjust gain and exposure of depth stream
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_sensor.set_option(rs.option.gain, 16)
        depth_sensor.set_option(rs.option.exposure, exposure)

        # Change depth step to 1mm
        depth_sensor.set_option(rs.option.depth_units, 0.001)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        self.depth_frame = frames.get_depth_frame()
        self.color_frame = frames.get_color_frame()
        # self.infrared_frame = frames.get_infrared_frame()

        depth_image = np.asanyarray(self.depth_frame.get_data())
        color_image = np.asanyarray(self.color_frame.get_data())
        # infrared_image = np.asanyarray(self.infrared_frame.get_data())
        if not self.depth_frame or not self.color_frame:
            return False, None, None, None
        return True, None, depth_image, color_image
    
    def get3d(self, x, y, distance):
        depth_frame = self.depth_frame
        if not depth_frame:
            return None
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        depth_pixel = [x, y]
        # Get depth scale
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        depth_point = rs.rs2_deproject_pixel_to_point(depth_intrin, depth_pixel, distance * depth_scale)
        return depth_point

    def release(self):
        self.pipeline.stop()

class CamToPoint:
    def __init__(self):
        self.service = rs.ser