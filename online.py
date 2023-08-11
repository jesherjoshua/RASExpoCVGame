import pyautogui
import math
import cv2
import numpy as np
import time
import mediapipe as mp
import pywinctl as gw
import pygetwindow as gw2

# Import required modules

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=True, min_detection_confidence=0.3, model_complexity=2
)
mp_drawing = mp.solutions.drawing_utils

# Initialize pose estimation model


def detectPose(image, pose, blankImage=False):
    # Function to detect pose landmarks in an image/frame

    output_image = image.copy()

    if blankImage:
        blank_image = np.zeros((720, 1920, 3), np.uint8)
        output_image = blank_image

    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = pose.process(imageRGB)

    height, width, _ = image.shape

    landmarks = []

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image=output_image,
            landmark_list=results.pose_landmarks,
            connections=mp_pose.POSE_CONNECTIONS,
        )

        for landmark in results.pose_landmarks.landmark:

            landmarks.append(
                (
                    int(landmark.x * width),
                    int(landmark.y * height),
                    (landmark.z * width),
                )
            )
    return output_image, landmarks, results


def checkHandsJoined(img, results, draw=False):
    # Function to check if hands are joined or not

    height, width, _ = img.shape

    output_img = img.copy()

    left_wrist_landmark = (
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height,
    )
    right_wrist_landmark = (
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height,
    )

    distance = int(
        math.hypot(
            left_wrist_landmark[0] - right_wrist_landmark[0],
            left_wrist_landmark[1] - right_wrist_landmark[1],
        )
    )

    if distance < 130:
        hand_status = "Hands Joined"
        color = (0, 255, 0)

    else:
        hand_status = "Hands Not Joined"
        color = (0, 0, 255)

    if draw:
        cv2.putText(
            output_img, hand_status, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 3
        )
        cv2.putText(
            output_img,
            f"Distance: {distance}",
            (10, 70),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            color,
            3,
        )

    return output_img, hand_status


def checkJumpCrouch(img, results, MID_Y=250, draw=False):
    # Function to check if the player is jumping, crouching, or standing

    height, width, _ = img.shape

    output_image = img.copy()

    left_y = int(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height
    )
    right_y = int(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height
    )

    actual_mid_y = abs(right_y + left_y) // 2

    lower_bound = MID_Y - 15
    upper_bound = MID_Y + 100

    if actual_mid_y < lower_bound:
        posture = "Jumping"

    elif actual_mid_y > upper_bound:
        posture = "Crouching"

    else:
        posture = "Standing"

    if draw:
        cv2.putText(
            output_image,
            posture,
            (5, height - 50),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 255, 255),
            3,
        )
        cv2.line(output_image, (0, MID_Y), (width, MID_Y), (255, 255, 255), 2)

    return output_image, posture


# Function to draw text on the image with background


def draw_text(
    img,
    text,
    font=cv2.FONT_HERSHEY_PLAIN,
    pos=(0, 0),
    font_scale=3,
    font_thickness=2,
    text_color=(0, 255, 0),
    text_color_bg=(0, 0, 0),
):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(
        img,
        text,
        (x, y + text_h + font_scale - 1),
        font,
        font_scale,
        text_color,
        font_thickness,
    )
    return text_size


if __name__ == "__main__":

    pose_video = mp_pose.Pose(
        static_image_mode=False, min_detection_confidence=0.5, model_complexity=1
    )

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    pTime = 0

    game_started = False
    x_pos_index = 1
    y_pos_index = 1
    MID_Y = None
    counter = 0
    num_of_frames = 10

    message = "JOIN BOTH HANDS TO START THE GAME. "
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        img = cv2.resize(img, (1280, 720))
        img, landmarks, results = detectPose(img, pose_video)
        if landmarks:
            if game_started:
                pass
            else:
                draw_text(
                    img,
                    message,
                    pos=(w // 8, h // 2),
                    text_color=(0, 0, 255),
                    font_scale=5,
                )

            if checkHandsJoined(img, results)[1] == "Hands Joined":

                counter += 1
                if counter == num_of_frames:
                    message = "STARTS IN 3.."

                elif counter == num_of_frames * 4:
                    message = "STARTS IN 2.."

                elif counter == num_of_frames * 6:
                    message = "STARTS IN 1.."

                elif counter == num_of_frames * 8:

                    if not (game_started):

                        game_started = True
                        left_y = int(
                            results.pose_landmarks.landmark[
                                mp_pose.PoseLandmark.RIGHT_SHOULDER
                            ].y
                            * h
                        )
                        right_y = int(
                            results.pose_landmarks.landmark[
                                mp_pose.PoseLandmark.LEFT_SHOULDER
                            ].y
                            * h
                        )
                        MID_Y = abs(right_y + left_y) // 2
                        try:

                            win = gw.getWindowsWithTitle(
                                "chrome://dino/ – Network error - Google Chrome (Incognito)"
                            )[0]
                            win.activate()
                        except:
                            for i in gw2.getAllTitles():
                                if i.split(" ")[0] == "Google Chrome (Incognito)":
                                    win = gw2.getWindowsWithTitle(i)[0]
                                    win.activate()
                                    print("Window Switch Successfull!!!")

                        time.sleep(3)
                        pyautogui.press("space")
                    else:

                        pyautogui.press("space")

                    counter = 0

            else:

                counter = 0

            if MID_Y:

                img, posture = checkJumpCrouch(img, results, MID_Y, draw=True)

                if posture == "Jumping" and y_pos_index == 1:

                    pyautogui.press("up")
                    y_pos_index += 1

                elif posture == "Crouching" and y_pos_index == 1:

                    pyautogui.press("down")

                    y_pos_index -= 1

                elif posture == "Standing" and y_pos_index != 1:

                    y_pos_index = 1
                print(posture)

        else:

            counter = 0

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(
            img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
        )

        cv2.imshow("Dino IRL", img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
