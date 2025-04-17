import customtkinter as ctk
from quiz_app import MCQApp

class Dashboard:
    def __init__(self, user_id, database):
        self.root = ctk.CTk()
        self.root.title("AWS Quiz Dashboard")
        self.root.geometry("800x600")
        self.user_id = user_id
        self.database = database
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.main_frame, text="Welcome to AWS Quiz", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        scores_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, border_width=2, border_color="#1f538d")
        scores_frame.pack(fill="both", expand=True, pady=20)

        scores = self.database.get_user_scores(self.user_id)
        if scores:
            for score, total, date in scores:
                score_text = f"Score: {score} - Date: {date}"
                card = ctk.CTkFrame(scores_frame, corner_radius=10, border_width=1, border_color="#1f538d")
                card.pack(fill="x", pady=5, padx=5)
                ctk.CTkLabel(card, text=score_text, font=ctk.CTkFont(size=12)).pack(pady=5)
        else:
            ctk.CTkLabel(scores_frame, text="No previous attempts", font=ctk.CTkFont(size=12)).pack(pady=5)

        ctk.CTkButton(self.main_frame, text="Start New Quiz", font=ctk.CTkFont(size=15, weight="bold"), command=self.start_quiz).pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Quit", font=ctk.CTkFont(size=15, weight="bold"), command=self.root.destroy).pack(pady=10)

    def start_quiz(self):
        self.root.destroy()
        quiz_root = ctk.CTk()
        quiz_app = MCQApp(quiz_root, self.user_id, self.database)
        quiz_root.mainloop()

    def run(self):
        self.root.mainloop()
