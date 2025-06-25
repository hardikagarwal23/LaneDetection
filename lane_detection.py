import cv2
import numpy as np
cap = cv2.VideoCapture('Video3 (1).mp4')
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break
    width = int(cap.get(3))
    height = int(cap.get(4))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(7,7), 0)
    edges = cv2.Canny(blur,175,255)
    polygon_points = np.array([[
           (int(0.05 * width), height),
    (int(0.95 * width), height),
    (int(0.64 * width), int(0.64 * height)),
    (int(0.42 * width), int(0.64 * height))
    ]], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask,polygon_points,255)
    roi = cv2.bitwise_and(edges,mask)
    lines = cv2.HoughLinesP(roi,rho=1,theta=np.pi / 180,threshold=60,minLineLength=50,maxLineGap=200)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 == 0:
             continue
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < 0.3:
             continue        
            cv2.line(frame,(x1, y1),(x2, y2),(0,255,0),10)
    cv2.imshow('mask',mask)
    cv2.imshow('Lane Detection',frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


