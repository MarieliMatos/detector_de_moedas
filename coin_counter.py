import cv2
import numpy as np
import funcs


def main():
    frame = cv2.imread("./images/1.jpg")

    image_resized = funcs.resize_image(frame, 80)
    detected_circles = funcs.find_circles(image_resized)
    if detected_circles is not None:
        funcs.one_cent_radius_in_pixels = 141.7
        total, coins = funcs.coins_counter(detected_circles)
        funcs.draw_circles(image_resized, np.uint16(detected_circles), total, coins)
        print("Detected: ", detected_circles)
    else:
        print("No circles detected")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
