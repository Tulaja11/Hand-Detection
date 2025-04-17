import customtkinter as ctk
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import time
from threading import Lock
import queue

class MCQApp:
    def __init__(self, root, user_id, database):
        self.root = root
        self.user_id = user_id
        self.database = database
        self.root.title("AWS Certification Quiz - Hand Gesture Recognition")
        self.root.geometry("1400x900")
        self.questions = [
            {"question": "Which AWS service is used for storing and distributing large amounts of data with low latency worldwide?",
             "options": ["Amazon CloudFront", "Amazon S3", "Amazon EBS", "Amazon EFS"],
             "correct": 0,
             "explanation": "Amazon CloudFront is a content delivery network (CDN) service that delivers data, videos, applications, and APIs securely with low latency and high transfer speeds."},
            {"question": "What is the primary purpose of AWS Identity and Access Management (IAM)?",
             "options": ["Managing AWS costs", "Controlling access to AWS services", "Monitoring AWS performance", "Managing DNS records"],
             "correct": 1,
             "explanation": "IAM is used to securely control access to AWS services and resources for users and applications."},
            {"question": "Which AWS service would you use for running containerized applications?",
             "options": ["AWS Lambda", "Amazon ECS", "Amazon S3", "Amazon RDS"],
             "correct": 1,
             "explanation": "Amazon Elastic Container Service (ECS) is a fully managed container orchestration service for running containerized applications."},
            {"question": "What is the purpose of Amazon RDS?",
             "options": ["File storage", "Content delivery", "Relational database management", "Server virtualization"],
             "correct": 2,
             "explanation": "Amazon RDS (Relational Database Service) makes it easy to set up, operate, and scale relational databases in the cloud."},
            {"question": "Which service provides serverless computing in AWS?",
             "options": ["Amazon EC2", "AWS Lambda", "Amazon EBS", "Amazon VPC"],
             "correct": 1,
             "explanation": "AWS Lambda lets you run code without provisioning or managing servers, making it a serverless compute service."},
            {"question": "What is the maximum size limit for an object in Amazon S3?",
             "options": ["1 TB", "5 TB", "10 TB", "Unlimited"],
             "correct": 1,
             "explanation": "The maximum size of an object in Amazon S3 is 5 TB."},
            {"question": "Which AWS service is used for creating virtual networks?",
             "options": ["Amazon VPC", "Amazon Route 53", "AWS Direct Connect", "AWS CloudFormation"],
             "correct": 0,
             "explanation": "Amazon Virtual Private Cloud (VPC) lets you provision a logically isolated section of the AWS Cloud."},
            {"question": "What is the purpose of Amazon CloudWatch?",
             "options": ["DNS management", "Content delivery", "Monitoring and observability", "Load balancing"],
             "correct": 2,
             "explanation": "Amazon CloudWatch is a monitoring and observability service for AWS cloud resources and applications."},
            {"question": "Which storage class in S3 is designed for long-term archival storage?",
             "options": ["S3 Standard", "S3 Intelligent-Tiering", "S3 Glacier", "S3 One Zone-IA"],
             "correct": 2,
             "explanation": "S3 Glacier is designed for data archiving and long-term backup with retrieval times ranging from minutes to hours."},
            {"question": "What AWS service would you use for automated infrastructure deployment?",
             "options": ["AWS Systems Manager", "AWS CloudFormation", "AWS Config", "AWS Organizations"],
             "correct": 1,
             "explanation": "AWS CloudFormation provides a way to create and manage AWS resources through templates."}
        ]
        self.setup_styles()
        self.setup_ui()
        self.setup_video()
        self.setup_game_state()

    def setup_styles(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self.root, fg_color=("gray90", "gray16"))
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.quiz_frame = ctk.CTkFrame(self.main_container, fg_color=("gray85", "gray17"))
        self.quiz_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.header_frame = ctk.CTkFrame(self.quiz_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        self.title_label = ctk.CTkLabel(self.header_frame, text="AWS Certification Quiz", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=10)

        self.progress_label = ctk.CTkLabel(self.header_frame, text="Question 1/10", font=ctk.CTkFont(size=16))
        self.progress_label.pack(pady=5)

        self.question_frame = ctk.CTkFrame(self.quiz_frame, corner_radius=15, border_width=2, border_color="#2a6f97", fg_color=("gray80", "gray20"))
        self.question_frame.pack(fill="x", pady=10, padx=20)

        self.question_label = ctk.CTkLabel(self.question_frame, text="", wraplength=600, font=ctk.CTkFont(size=18))
        self.question_label.pack(pady=20, padx=20)

        self.options_frame = ctk.CTkFrame(self.quiz_frame, corner_radius=15, border_width=2, border_color="#2a6f97", fg_color=("gray80", "gray20"))
        self.options_frame.pack(fill="x", pady=10, padx=20)

        self.option_labels = []
        for i in range(4):
            option_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
            option_frame.pack(fill="x", pady=5, padx=20)
            finger_label = ctk.CTkLabel(option_frame, text=f"✋ {i+1}", font=ctk.CTkFont(size=16, weight="bold"), width=40)
            finger_label.pack(side="left", padx=(0, 10))
            label = ctk.CTkLabel(option_frame, text="", wraplength=500, font=ctk.CTkFont(size=16), anchor="w")
            label.pack(side="left", fill="x", expand=True)
            self.option_labels.append(label)

        self.explanation_frame = ctk.CTkFrame(self.quiz_frame, corner_radius=15, border_width=2, border_color="#2a6f97", fg_color=("gray80", "gray20"))
        self.explanation_frame.pack(fill="x", pady=10, padx=20)

        self.explanation_label = ctk.CTkLabel(self.explanation_frame, text="", wraplength=600, font=ctk.CTkFont(size=14), text_color="gray70")
        self.explanation_label.pack(pady=10, padx=20)

        self.feedback_frame = ctk.CTkFrame(self.quiz_frame, fg_color="transparent")
        self.feedback_frame.pack(fill="x", pady=10)

        self.feedback_label = ctk.CTkLabel(self.feedback_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.feedback_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(self.feedback_frame, text="Score: 0", font=ctk.CTkFont(size=16, weight="bold"))
        self.score_label.pack(pady=5)

        self.video_frame = ctk.CTkFrame(self.main_container, corner_radius=15, border_width=2, border_color="#2a6f97")
        self.video_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.instruction_label = ctk.CTkLabel(self.video_frame, text="Show fingers 1-4 to select your answer:\n\n1 - Index finger\n2 - Index + Middle fingers\n3 - Index + Middle + Ring fingers\n4 - All fingers except thumb", font=ctk.CTkFont(size=14))
        self.instruction_label.pack(pady=10)

        self.video_label = ctk.CTkLabel(self.video_frame)
        self.video_label.pack(pady=10)

    def setup_video(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise ValueError("Error: Camera not detected.")
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1)
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            self.queue = queue.Queue()
            self.running = True
            self.lock = Lock()
            self.camera_active = True
            self.update_video_frame()
        except Exception as e:
            print(f"Camera initialization error: {str(e)}")
            self.camera_active = False
            self.instruction_label.configure(text="Camera not available.\nPlease check your camera connection.", text_color="red")

    def setup_game_state(self):
        self.score = 0
        self.current_question = 0
        self.last_gesture_time = 0
        self.gesture_cooldown = 2.0
        self.answer_submitted = False
        self.show_question()

    def update_video_frame(self):
        if not self.running or not self.camera_active:
            return
        try:
            ret, frame = self.cap.read()
            if not ret:
                raise ValueError("Failed to read frame from camera.")
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            gesture = 0  # Initialize gesture as 0 (no gesture)
            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS,
                                                   self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                                   self.mp_drawing_styles.get_default_hand_connections_style())
                    fingers = self.get_fingers_up(landmarks)
                    gesture = self.get_gesture(fingers)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk
            if gesture > 0 and not self.answer_submitted:
                self.detect_gesture(gesture)
            if self.running:
                self.root.after(10, self.update_video_frame)
        except Exception as e:
            print(f"Error in video frame update: {str(e)}")
            self.camera_active = False
            self.instruction_label.configure(text="Camera error occurred.\nPlease restart the application.", text_color="red")

    def get_fingers_up(self, landmarks):
        tips = [4, 8, 12, 16, 20]
        fingers = []
        if landmarks.landmark[tips[0]].x < landmarks.landmark[tips[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        for tip in tips[1:]:
            if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def get_gesture(self, fingers):
        if fingers[1:] == [1, 0, 0, 0]:
            return 1
        elif fingers[1:] == [1, 1, 0, 0]:
            return 2
        elif fingers[1:] == [1, 1, 1, 0]:
            return 3
        elif fingers[1:] == [1, 1, 1, 1]:
            return 4
        return 0

    def detect_gesture(self, gesture):
        current_time = time.time()
        if gesture > 0 and (current_time - self.last_gesture_time) >= self.gesture_cooldown:
            self.last_gesture_time = current_time
            self.check_answer(gesture - 1)

    def check_answer(self, answer_index):
        question = self.questions[self.current_question]
        correct_answer = question["correct"]
        if answer_index == correct_answer:
            self.score += 10
            self.feedback_label.configure(text="Correct!", text_color="green")
        else:
            self.feedback_label.configure(text="Incorrect!", text_color="red")
        self.score_label.configure(text=f"Score: {self.score}")
        self.explanation_label.configure(text=question["explanation"])
        self.answer_submitted = True
        self.root.after(4000, self.next_question)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.answer_submitted = False
            self.show_question()
        else:
            self.finish_game()

    def show_question(self):
        question = self.questions[self.current_question]
        self.question_label.configure(text=question["question"])
        for i, option in enumerate(question["options"]):
            self.option_labels[i].configure(text=option)
        self.progress_label.configure(text=f"Question {self.current_question + 1}/{len(self.questions)}")
        self.explanation_label.configure(text="")
        self.feedback_label.configure(text="")

    def finish_game(self):
        self.feedback_label.configure(text="Game Over!")
        self.explanation_label.configure(text=f"Your final score is {self.score}.\nThanks for playing!")
        if self.camera_active:
            self.cap.release()
        self.running = False
        self.database.save_score(self.user_id, self.score, len(self.questions))
        self.root.after(2000, self.return_to_dashboard)

    def return_to_dashboard(self):
        self.root.destroy()
        from dashboard import Dashboard
        dashboard = Dashboard(self.user_id, self.database)
        dashboard.run()

if __name__ == "__main__":
    root = ctk.CTk()
    app = MCQApp(root, user_id=1, database={})
    root.mainloop()
