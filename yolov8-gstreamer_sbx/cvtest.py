import numpy as np
import cv2 as cv


# Try different indices
for i in range(10):
    cap = cv.VideoCapture(i)
    if not cap.isOpened():
        print(f"Camera at index {i} not available")
        continue
    else:
        print(f"Camera found at index {i}")
        break

if not cap.isOpened():
    print("No camera available. Exiting...")
    exit()

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here



    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()