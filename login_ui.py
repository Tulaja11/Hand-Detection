import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

class ModernLoginUI:
    def __init__(self, database):
        self.database = database
        self.user_id = None
        

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        

        self.root = ctk.CTk()
        self.root.title("AWS Quiz")
        self.root.geometry("1100x600")
        

        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        

        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(20, 10))
        
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 20))
        
        self.setup_left_panel()
        self.create_login_frame()

    def setup_left_panel(self):

        ctk.CTkLabel(
            self.left_frame,
            text="Welcome to\nAWS Quiz",
            font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"),
            text_color="#1f538d"
        ).pack(pady=(100, 20))
        
        ctk.CTkLabel(
            self.left_frame,
            text="Test your AWS knowledge with\nour interactive quiz system",
            font=ctk.CTkFont(size=16),
            text_color="#666666"
        ).pack(pady=20)

    def create_login_frame(self):

        self.login_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color="#ffffff",
            corner_radius=15,
            border_width=2,
            border_color="#1f538d"
        )
        self.login_frame.pack(pady=50, padx=30, fill="both", expand=True)
        

        ctk.CTkLabel(
            self.login_frame,
            text="Login to Your Account",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        ).pack(pady=(40, 20))
        

        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            width=300,
            height=50,
            placeholder_text="Username",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.username_entry.pack(pady=10, padx=30)
        

        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            width=300,
            height=50,
            placeholder_text="Password",
            show="●",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.password_entry.pack(pady=10, padx=30)
        

        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=300,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=8,
            command=self.handle_login,
            fg_color="#1f538d",
            hover_color="#163d6a"
        )
        self.login_button.pack(pady=20)
        

        self.register_link = ctk.CTkButton(
            self.login_frame,
            text="Don't have an account? Register",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#f0f0f0",
            text_color="#1f538d",
            command=self.show_register_frame
        )
        self.register_link.pack(pady=(0, 40))

    def create_register_frame(self):
        self.register_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color="#ffffff",
            corner_radius=15,
            border_width=2,
            border_color="#1f538d"
        )
        self.register_frame.pack(pady=50, padx=30, fill="both", expand=True)
        
        ctk.CTkLabel(
            self.register_frame,
            text="Create New Account",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        ).pack(pady=(40, 20))
        

        self.reg_username = ctk.CTkEntry(
            self.register_frame,
            width=300,
            height=50,
            placeholder_text="Username",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.reg_username.pack(pady=10)
        
        self.reg_email = ctk.CTkEntry(
            self.register_frame,
            width=300,
            height=50,
            placeholder_text="Email",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.reg_email.pack(pady=10)
        
        self.reg_password = ctk.CTkEntry(
            self.register_frame,
            width=300,
            height=50,
            placeholder_text="Password",
            show="●",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.reg_password.pack(pady=10)
        
        self.reg_confirm = ctk.CTkEntry(
            self.register_frame,
            width=300,
            height=50,
            placeholder_text="Confirm Password",
            show="●",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.reg_confirm.pack(pady=10)
        

        self.register_button = ctk.CTkButton(
            self.register_frame,
            text="Register",
            width=300,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=8,
            command=self.handle_register,
            fg_color="#1f538d",
            hover_color="#163d6a"
        )
        self.register_button.pack(pady=20)
        

        self.login_link = ctk.CTkButton(
            self.register_frame,
            text="Already have an account? Login",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#f0f0f0",
            text_color="#1f538d",
            command=self.show_login_frame
        )
        self.login_link.pack(pady=(0, 40))

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.create_register_frame()

    def show_login_frame(self):
        if hasattr(self, 'register_frame'):
            self.register_frame.pack_forget()
        self.login_frame.pack(pady=50, padx=30, fill="both", expand=True)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.show_error("Please enter both username and password!")
            return
            
        user_id = self.database.verify_user(username, password)
        if user_id:
            self.user_id = user_id
            self.root.quit()
        else:
            self.show_error("Invalid username or password!")

    def handle_register(self):
        username = self.reg_username.get()
        email = self.reg_email.get()
        password = self.reg_password.get()
        confirm_password = self.reg_confirm.get()

        if not username or not email or not password or not confirm_password:
            self.show_error("Please fill in all fields!")
            return

        if password != confirm_password:
            self.show_error("Passwords do not match!")
            return

        if len(password) < 8:
            self.show_error("Password must be at least 8 characters long!")
            return

        success = self.database.register_user(username, password, email)
        if success:
            self.show_success("Registration successful! Please login.")
            self.show_login_frame()
        else:
            self.show_error("Username or email already exists!")

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Error")
        error_window.geometry("400x200")
        error_window.transient(self.root)
        
        ctk.CTkLabel(
            error_window,
            text="⚠️ Error",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ff3333"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            error_window,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=300
        ).pack(pady=10)
        
        ctk.CTkButton(
            error_window,
            text="OK",
            width=100,
            command=error_window.destroy
        ).pack(pady=20)

    def show_success(self, message):
        success_window = ctk.CTkToplevel(self.root)
        success_window.title("Success")
        success_window.geometry("400x200")
        success_window.transient(self.root)
        
        ctk.CTkLabel(
            success_window,
            text="✔️ Success",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#33cc33"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            success_window,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=300
        ).pack(pady=10)
        
        ctk.CTkButton(
            success_window,
            text="OK",
            width=100,
            command=success_window.destroy
        ).pack(pady=20)

    def run(self):
        self.root.mainloop()
        user_id = self.user_id
        if hasattr(self, 'root') and self.root:
            self.root.destroy()
        return user_id
