import open3d as o3d
import open3d.visualization.gui as gui


import numpy as np
import cv2
import threading
import time


class VideoWindow:

    def __init__(self):

        self.rgb_images = []
        rgbd_data = o3d.data.SampleRedwoodRGBDImages()
        for path in rgbd_data.color_paths:
            img = o3d.io.read_image(path) 
            self.rgb_images.append(img)

        # path = 
        # img = o3d.io.read_image(path)
        # self.rgb_images.append(img)


        self.window = gui.Application.instance.create_window(
            "Open3D - Video", 1000, 500)


        em = self.window.theme.font_size
        margin = 0.5 * em
        self.panel = gui.Vert(0.5 * em, gui.Margins(margin))
        self.panel.add_child(gui.Label("Color image"))
        self.rgb_widget = gui.ImageWidget(self.rgb_images[0])
        self.panel.add_child(self.rgb_widget)
        self.window.add_child(self.panel)        
        
        self.is_done = False
        threading.Thread(target=self._update_thread).start()

    def _update_thread(self):
            # This is NOT the UI thread, need to call post_to_main_thread() to update
            # the scene or any part of the UI.
            idx = 0
            while not self.is_done:
                time.sleep(0.100)

                # Get the next frame, for instance, reading a frame from the camera.
                rgb_frame = self.rgb_images[idx]
                idx += 1
                if idx >= len(self.rgb_images):
                    idx = 0

                # Update the images. This must be done on the UI thread.
                def update():
                    self.rgb_widget.update_image(rgb_frame)

                if not self.is_done:
                    gui.Application.instance.post_to_main_thread(
                        self.window, update)






def main():
    app = gui.Application.instance
    app.initialize()

    win = VideoWindow()


    app.run()


if __name__ == "__main__":
    main()