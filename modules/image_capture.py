import cv2


class ImageCapture:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)

    def capture_image(self):
        success, img = self.cap.read()
        img = cv2.flip(img, 1)
        return success, img

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
