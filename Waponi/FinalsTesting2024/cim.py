import cv2

images = ["LimelightStudio2024RawImages/Raft1/0000_new/DSC08748.JPG", "LimelightStudio2024RawImages/Raft2/0000_new/DSC08702.JPG", "LimelightStudio2024RawImages/Raft4/0000_new/ESC00452.JPG", "LimelightStudio2024RawImages/Raft5/0000_new/DSC03981.JPG"]

def combine(images):
        img1 = cv2.imread(images[0])
        img2 = cv2.imread(images[1])
        img3 = cv2.imread(images[2])
        img4 = cv2.imread(images[3])

        image_row_1 = cv2.hconcat([img1, img2])
        image_row_2 = cv2.hconcat([img3, img4])
        combined_image = cv2.vconcat([image_row_1, image_row_2])

        return cv2.imwrite("Combined.png", combined_image)

combine(images)
