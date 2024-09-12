import cv2
import os

# Check the current working directory
print(f"Current working directory: {os.getcwd()}")

# Replace 'image.png' with your actual image file name
image_path = 'data/Raw Data/New Format/7-23 part 1/0/dart/frame_2_1721743905.206404.png'

# Read the image
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Image not found at path {image_path}. Please check the file name and extension.")
else:
    # Create a window and set the mouse callback function
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', lambda event, x, y, flags, param: print(f"Mouse Position: X: {x}, Y: {y}") if event == cv2.EVENT_MOUSEMOVE else None)

    # Display the image and wait for a key press
    while True:
        cv2.imshow('Image', image)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Press 'Esc' to exit
            break

    # Destroy all windows
    cv2.destroyAllWindows()
