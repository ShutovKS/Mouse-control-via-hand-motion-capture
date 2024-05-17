import cv2

from modules.hand_tracking import HandTracking
from modules.image_capture import ImageCapture
from modules.mouse_controller import MouseController

is_draw = True
mouse_sensation_multiplier = 7

capture = ImageCapture()
tracking = HandTracking()
controller = MouseController(mouse_sensation_multiplier)

while True:
    success, img = capture.capture_image()
    if success:
        img = tracking.find_hands(img, is_draw)
        cx, cy = tracking.get_hand_coordinates(img)
        gestures = tracking.detect_hand_gestures(img)

        if cx and cy:
            controller.move_mouse(cx, cy)

        if gestures.fist:
            cv2.putText(img, "Click Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            controller.click_down()
        if gestures.palm:
            cv2.putText(img, "Click Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            controller.click_up()
        if not gestures.palm and not gestures.fist:
            cv2.putText(img, "None Track", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            controller.click_up()

        cv2.imshow("Image", img)
        cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
