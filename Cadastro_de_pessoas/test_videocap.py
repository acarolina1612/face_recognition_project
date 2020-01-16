import cv2
from win32api import GetSystemMetrics

img = cv2.imread("test.JPG")
winname = "Test"
cv2.moveWindow(winname, 40, 30)  # Move it to (40,30)
cv2.imshow(winname, img)
cv2.waitKey()
cv2.destroyAllWindows()