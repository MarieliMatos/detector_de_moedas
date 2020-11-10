"""
Detector de Moedas utilizando webcam

Teclas:
    s - Faz a contagem das moedas.
    q - Finaliza o programa.
    d - Entra no modo de debug.
        c - Configura um novo raio minimo.
"""

import cv2
import numpy as np
import funcs


def main():
    webcam_number = 1
    key = cv2.waitKey(1)
    webcam = funcs.set_webcam(webcam_number)
    while True:
        try:
            frame = funcs.get_image(webcam)
            img_resized = funcs.resize_image(frame, 60)
            cv2.imshow("Capturing", img_resized)
            key = cv2.waitKey(1)
            if key == ord('d'):  # debug mode
                debug_mode = not funcs.debug_mode
                if debug_mode:
                    print("Entered debug mode")
                else:
                    print("Out of debug mode")
            if key == ord('c'):  # configure parameters
                print("Current one_cent_radius_in_pixels: ", funcs.one_cent_radius_in_pixels)
                try:
                    funcs.one_cent_radius_in_pixels = int(input("Enter new value: "))
                except ValueError:
                    print("Not a number")
            if key == ord('s'):
                webcam.release()
                cv2.imshow("Captured Image", img_resized)
                # cv2.imwrite('frame_coins.jpg', img_resized)
                print("Processing image...")
                circles_detected = funcs.find_circles(img_resized)
                if circles_detected is not None:
                    total, coins = funcs.coins_counter(circles_detected)
                    funcs.draw_circles(img_resized, np.uint16(circles_detected), total, coins)
                    print("Detected:", circles_detected)
                else:
                    print("No circle detected")
                cv2.waitKey(1650)
                print("Image processed")
                cv2.destroyAllWindows()
                webcam = funcs.set_webcam(webcam_number)
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break

        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break


main()
