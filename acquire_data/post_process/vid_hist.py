import cv2
import matplotlib.pyplot as plt

# Iterate through image indices
for i in range(0, 759):  # Replace with the actual range
    # Read the image in grayscale
    img_name = f"/Users/pratiksha/test-scripts/camera2/trk/tracked_batch_1699306772.2372239_2_item_{i}.png"
    img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)

    # Compute histogram
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    # Plot histogram
    plt.figure()
    plt.title(f"Histogram for image {i}")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.ylim([0, 25000])
    plt.grid()
    plt.savefig(f"Histogram_{i}.png")
    plt.close()

