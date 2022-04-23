import cv2
import mediapipe as mp
import message

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

while True:
  cap = cv2.VideoCapture(1)
  with mp_pose.Pose(
      min_detection_confidence=0.8,
      min_tracking_confidence=0.8) as pose:
    
    while cap.isOpened():
      success, image = cap.read()
      image_hight, image_width, _ = image.shape
      
      if not success:
        print("Ignoring empty camera frame.")
        continue

      image.flags.writeable = False
      
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = pose.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      
      # mp_drawing.draw_landmarks(
      #     image,
      #     results.pose_landmarks,
      #     mp_pose.POSE_CONNECTIONS,
      #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

      if results.pose_landmarks:
        
        x_cordinate = list()
        y_cordinate = list()
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            x_cordinate.append(cx)
            y_cordinate.append(cy)
            
        cv2.rectangle(img= image,
                      pt1= (min(x_cordinate), max(y_cordinate)),
                      pt2 = (max(x_cordinate), min(y_cordinate)-20),
                      color= (0,0,255),
                      thickness= 1)
        
        cv2.imwrite('image.png', image)
        cap.release()
        
        try:
          message.telegram()
        except Exception:
          message.messenger()
        else:
          continue
      
      
  #     cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
  #     if cv2.waitKey(5) & 0xFF == 27:
  #       break
      
  # cap.release()
      
    
    
    
    
    
    
    
    
    