#import python ,tkinter, mysql and other libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import re
import tkinter as tk

from pet import Pet
# from GIF import GIF
# from RAG import RAG


#connecting to the database
pdsdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pavan",
    database="pawfect"
)

#creating table user query userid,first_name,last_name,email,mobile,password
create_user_table = """
CREATE TABLE IF NOT EXISTS user_info (
    email VARCHAR(100) NOT NULL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
    )
"""
create_pet_table = """CREATE TABLE IF NOT EXISTS Pet (
    pet_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_name VARCHAR(50) NOT NULL,
    pet_Type VARCHAR(50) NOT NULL,
    pet_gender VARCHAR(6) NOT NULL,
    breed VARCHAR(50) NOT NULL,
    pet_color VARCHAR(50) NOT NULL,
    pet_weight DECIMAL(10, 2) NOT NULL,
    pet_age INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    FOREIGN KEY (email) REFERENCES user_info(email) ON DELETE CASCADE
)
"""

#executing the query
cursor = pdsdb.cursor()
cursor.execute(create_user_table)
cursor.execute(create_pet_table)

#class Pawfect Portions as pp
class PawfectPortions:
    #initializing the class
    def __init__(self, root):
        self.root = root
        self.root.title("Pawfect Portions")
        self.root.geometry("1200x750")
        self.root.config(bg="black")
        # self.rag = RAG()
        
        
        #self.welcomeScreen()
        self.loginScreen()
    
    #login screen
    def loginScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            
        #create a frame for the login screen
        self.login_frame = Frame(self.root, bg="black")
        self.login_frame.place(x=0, y=0, width=1200, height=750)
        
        self.show_pass_var = tk.IntVar()
        self.password_visible = False
        # adding Logindogpage1 image
        self.bg = Image.open("images/Logindogpage1.jpg")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.login_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        #adding Welcome text on the top
        self.welcome_label = Label(self.login_frame, text="Welcome", font=("calibri", 70, "bold"), bg="black", fg="WHITE")
        self.welcome_label.place(x=100, y=70)


        #adding login text on the top
        #self.login_label = Label(self.login_frame, text="Login", font=("calibri", 20, "bold"), bg="black", fg="WHITE")
        #self.login_label.place(x=850, y=200)

        self.title = Image.open("txtImages/title.png")
        self.title = self.title.resize((170, 70), Image.LANCZOS)
        self.title = ImageTk.PhotoImage(self.title)
        self.title_image = Label(self.login_frame, image=self.title, bg="white")
        self.title_image.config(highlightthickness=0, bd=0, relief="ridge")
        self.title_image.place(x=760, y=100)
        
        #adding username label
        self.username_label = Label(self.login_frame, text="__________________________", font=("calibri", 18, "bold"), bg="black", fg="WHITE") 
        self.username_label.place(x=760, y=270)
        #adding password label
        self.password_label = Label(self.login_frame, text="__________________________", font=("calibri", 18, "bold"), bg="black", fg="WHITE")
        self.password_label.place(x=760, y=340)
        
        #adding password entryc
        self.password_entry = Entry(self.login_frame,font=("calibri", 18), bg="black", width=28, bd=0,fg="white", relief="ridge",insertbackground="white")
        self.password_entry.place(x=765, y=325)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', self.removepasswordtext)
        self.password_entry.bind('<FocusOut>', self.removepasswordtext)
    
        #adding username entry
        self.username_entry = Entry(self.login_frame,font=("calibri", 18), bg="black", width= 28, bd=0,fg="white", relief="ridge",insertbackground="white")
        self.username_entry.place(x=765, y=260)
        self.username_entry.insert(0, "Email")
        #self.username_entry.bind("<Key>", self.removeusernametext)
        self.username_entry.bind('<FocusIn>', self.removeusernametext)
        self.username_entry.bind('<FocusOut>', self.removeusernametext)
        
        show_icon_image = Image.open("images/show.png")
        show_icon_resized = show_icon_image.resize((30, 30), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.show_icon = ImageTk.PhotoImage(show_icon_resized)

        #storing in user email variable
        self.user_email = self.username_entry.get()
        # Open and resize the hide icon
        hide_icon_image = Image.open("images/hide.png")
        hide_icon_resized = hide_icon_image.resize((30, 30), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS for Pillow >= 7.0.0
        self.hide_icon = ImageTk.PhotoImage(hide_icon_resized)


        # Create a button to toggle password visibility
        self.toggle_button = tk.Button(self.login_frame, image=self.show_icon, command=self.toggle_password_visibility, borderwidth=0,highlightthickness=0, bg="black", activebackground="black")
        self.toggle_button.place(x=1050, y=330)
        
        
        #adding login button
        self.login_button = Button(self.login_frame, text="Login", font=("calibri",18,"bold"), bg="midnight blue", fg="white", bd=0, cursor="hand2",activebackground="black",activeforeground="grey", command=self.login_validation)
        self.login_button.place(x=880, y=420)

        #text for signup button
        self.text = Label(self.login_frame, text="Don't have an account?", font=("calibri", 14), bg="#080808", fg="WHITE")
        self.text.place(x=780, y=500)

        #adding signup button
        self.signup_button = Button(self.login_frame, text="sign up", font=("calibri",14,"underline"), bg="black", fg="light blue", bd=0, cursor="hand2",activebackground="black",activeforeground="grey",command=self.signupScreen)
        self.signup_button.place(x=970, y=495)
        

        #adding forgot password button
        self.forgot_password_button = Button(self.login_frame, text="Forgot Password?", font=("calibri",10,"bold"), bg="black", fg="light blue", bd=0, cursor="hand2",activebackground="black")
        self.forgot_password_button.place(x=960, y=380)

    def toggle_password_visibility(self):
        if self.password_visible:
            # Hide the password and update the button icon
            self.password_entry.config(show="*")
            self.toggle_button.config(image=self.show_icon)
            self.password_visible = False
        else:
            # Show the password and update the button icon
            self.password_entry.config(show="")
            self.toggle_button.config(image=self.hide_icon)
            self.password_visible = True
    
    #creating entry lable inside the username entry
    def removeusernametext(self, event):
        if self.username_entry.get() == "Email":
            self.username_entry.delete(0, "end")
            self.username_entry.config(fg="white")
        elif self.username_entry.get() == "":
            self.username_entry.insert(0, "Email")
            self.username_entry.config(fg="white") 
    def removepasswordtext(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(fg="white")
            self.password_entry.config(show="*")
        elif self.password_entry.get() == "":
            self.password_entry.insert(0, "Password")
            self.password_entry.config(show="")
            self.password_entry.config(fg="white") 

    #creating signup screen
    def signupScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            
        #create a frame for the signup screen
        self.signup_frame = Frame(self.root, bg="black")
        self.signup_frame.place(x=0, y=0, width=1200, height=750)
        # adding Logindogpage1 image
        self.bg = Image.open("images/signtupcat.jpg")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.signup_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        self.signup_label = Label(self.signup_frame, text="Register Your Account Here", font=("calibri", 40, "bold"), bg="#080808", fg="WHITE")
        self.signup_label.place(x=300, y=50)
        
        #adding first name label
        self.first_name_label = Label(self.signup_frame, text="First Name", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.first_name_label.place(x=40, y=200)
        #addling line under the first name label
        self.first_name_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.first_name_label.place(x=158, y=206)
        #adding first name entry
        self.first_name_entry = Entry(self.signup_frame,font=("calibri", 15), bg="#080808", width=28, bd=0,fg="white", relief="ridge",insertbackground="white")
        self.first_name_entry.place(x=160, y=206)
        #adding last name label 
        self.last_name_label = Label(self.signup_frame, text="Last Name", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.last_name_label.place(x=450, y=206)
        #addling line under the last name label
        self.last_name_label = Label(self.signup_frame, text="____________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.last_name_label.place(x=565, y=205)
        #adding last name entry
        self.last_name_entry = Entry(self.signup_frame,font=("calibri",15), bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.last_name_entry.place(x=570, y=206)
        #adding email label
        self.email_label = Label(self.signup_frame, text="Email", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.email_label.place(x=50, y=275)
        #addling line under the email label
        self.email_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.email_label.place(x=158, y=280)
        #adding email entry
        self.email_entry = Entry(self.signup_frame,font=("calibri", 15), width=28, bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.email_entry.place(x=160, y=280)
        #adding mobile label
        self.mobile_label = Label(self.signup_frame, text="Mobile", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.mobile_label.place(x=50, y=350)
        #addling line under the mobile label
        self.mobile_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.mobile_label.place(x=160, y=350)
        #adding mobile entry
        self.mobile_entry = Entry(self.signup_frame,font=("calibri", 15), bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.mobile_entry.place(x=160, y=350)
        #adding password label
        self.password_label = Label(self.signup_frame, text="Password", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.password_label.place(x=50, y=425)
        #addling line under the password label
        self.password_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.password_label.place(x=160, y=425)
        #adding password entry
        self.password_entry = Entry(self.signup_frame,font=("calibri", 15), width= 28, bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white",show="*")
        self.password_entry.place(x=160, y=425)
        
         # Create a button to toggle password visibility
        self.toggle_button = tk.Button(self.signup_frame, image=self.show_icon, command=self.toggle_password_visibility, borderwidth=0,highlightthickness=0, bg="#080808", activebackground="black")
        self.toggle_button.place(x=425, y=420)
        
        #adding confirm password label
        self.confirm_password_label = Label(self.signup_frame, text="Confirm Password", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.confirm_password_label.place(x=50, y=500)
        #addling line under the confirm password label
        self.confirm_password_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.confirm_password_label.place(x=250, y=495)
        #adding confirm password entry
        self.confirm_password_entry = Entry(self.signup_frame,font=("calibri", 15), width=28, bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white",show="*")
        self.confirm_password_entry.place(x=252, y=495)
        #adding signup button
        self.signup_button = Button(self.signup_frame, text="Sign Up", font=("calibri",18,"bold"), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="#080808",activeforeground="grey")
        self.signup_button.place(x=485, y=590)
        self.signup_button.config(command=self.signup_data)
        #adding login button
        self.login_button = Button(self.signup_frame, text="Back to Login", font=("calibri",18,"bold"), bg="#080808", fg="white", bd=0, cursor="hand2",activebackground="#080808",activeforeground="grey",command=self.loginScreen)
        self.login_button.place(x=460, y=650)
        

    def welcomeScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
                       
        #dsiplay welcome image
        self.bg = Image.open("images/welcome.jpg")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        
        #display title image on left middle
        self.title = Image.open("txtImages/title.png")
        self.title = self.title.resize((570, 200), Image.LANCZOS)
        self.title = ImageTk.PhotoImage(self.title)
        self.title_image = Label(self.root, image=self.title, bg="white")
        self.title_image.config(highlightthickness=0, bd=0, relief="ridge")
        self.title_image.place(x=20, y=140)
        

        #bottom frame for buttons
        self.bottom_frame = Frame(self.root, bg="#242323")
        self.bottom_frame.place(x=0, y=690, width=1200, height=80)
        #add shadow to the bottom frame
        self.bottom_frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=0)
        
        #add logo image as a button side to home button
        self.logo = Image.open("images/logout.jpg")
        self.logo = self.logo.resize((40, 40), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_button = Button(self.bottom_frame, image=self.logo, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.logo_button.place(x=20, y=10)
        self.logo_button.config(command=self.loginScreen)
        
        #add profile image as a button
        self.profile = Image.open("images/profile.png")
        self.profile = self.profile.resize((40, 40), Image.LANCZOS)
        self.profile = ImageTk.PhotoImage(self.profile)
        self.profile_button = Button(self.bottom_frame, image=self.profile, bg="#242323", activebackground="#242323",bd=0, cursor="hand2", command=self.profile_screen)
        self.profile_button.place(x=90, y=10)
        
        
        #home button    
        self.home_button = Button(self.bottom_frame, text="Home", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.home_button.place(x=400, y=6)
        
        #dogs button
        self.dogs_button = Button(self.bottom_frame, text="Dogs", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        #command to dogs screen
        self.dogs_button.config(command=self.selectDogBreed)
        self.dogs_button.place(x=520, y=6)
        
        #cats button
        self.cats_button = Button(self.bottom_frame, text="Cats", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.cats_button.place(x=640, y=6)
        
        #Pet AI
        self.pet_ai_button = Button(self.bottom_frame, text="Pet AI", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        #command=self.petAiScreen
        self.pet_ai_button.config(command=self.petAiScreen)
        self.pet_ai_button.place(x=760, y=6)
        
        
        #place facebook icon as a button
        self.facebook_icon = Image.open("social/facebook.png")
        self.facebook_icon = self.facebook_icon.resize((25, 25), Image.LANCZOS)
        self.facebook_icon = ImageTk.PhotoImage(self.facebook_icon)
        self.facebook_button = Button(self.bottom_frame, image=self.facebook_icon, bg="#242323", bd=0, cursor="hand2")
        self.facebook_button.place(x=1000, y=13)
        
        
        #place instagram icon as a button
        self.instagram_icon = Image.open("social/insta.png")
        self.instagram_icon = self.instagram_icon.resize((25, 25), Image.LANCZOS)
        self.instagram_icon = ImageTk.PhotoImage(self.instagram_icon)
        self.instagram_button = Button(self.bottom_frame, image=self.instagram_icon, bg="#242323", bd=0, cursor="hand2")
        self.instagram_button.place(x=1050, y=15)
        
        
        #twitter  icon as a button
        self.twitter_icon = Image.open("social/twitter.png")
        self.twitter_icon = self.twitter_icon.resize((25, 25), Image.LANCZOS)
        self.twitter_icon = ImageTk.PhotoImage(self.twitter_icon)
        self.twitter_button = Button(self.bottom_frame, image=self.twitter_icon, bg="#242323", bd=0, cursor="hand2")
        self.twitter_button.place(x=1100, y=15)
        
    
    #petai screen
    def petAiScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
        
        #buttons frame on top
        self.buttons_frame = Frame(self.root, bg="#242323")
        self.buttons_frame.place(x=0, y=0, width=1200, height=60)
        
        #home button
        self.home_button = Button(self.buttons_frame, text="Home", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.home_button.config(command=self.welcomeScreen)
        self.home_button.place(x=400, y=6)
        
        #dogs button
        self.dogs_button = Button(self.buttons_frame, text="Dogs", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        #commad=self.selectDogBreed
        self.dogs_button.config(command=self.selectDogBreed)    
        self.dogs_button.place(x=520, y=6)
        
        #cats button
        self.cats_button = Button(self.buttons_frame, text="Cats", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.cats_button.place(x=640, y=6)
        
        #Pet AI
        self.pet_ai_button = Button(self.buttons_frame, text="Pet AI", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.pet_ai_button.place(x=760, y=6)
        
        #highlight the pet ai button
        self.pet_ai_button.config(bg="white", fg="#242323")
        
        #add logo image as a button
        self.logo = Image.open("images/logout.jpg")
        self.logo = self.logo.resize((40, 40), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_button = Button(self.buttons_frame, image=self.logo, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.logo_button.place(x=20, y=10)
        self.logo_button.config(command=self.loginScreen)
        
        #add profile image as a button
        self.profile = Image.open("images/profile.png")
        self.profile = self.profile.resize((40, 40), Image.LANCZOS)
        self.profile = ImageTk.PhotoImage(self.profile)
        self.profile_button = Button(self.buttons_frame, image=self.profile, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.profile_button.place(x=90, y=10)
        
        
        #facebook icon as a button
        self.facebook_icon = Image.open("social/facebook.png")
        self.facebook_icon = self.facebook_icon.resize((25, 25), Image.LANCZOS)
        self.facebook_icon = ImageTk.PhotoImage(self.facebook_icon)
        
        self.facebook_button = Button(self.buttons_frame, image=self.facebook_icon, bg="#242323", bd=0, cursor="hand2")
        self.facebook_button.place(x=1000, y=13)
        
        #instagram icon as a button
        self.instagram_icon = Image.open("social/insta.png")
        self.instagram_icon = self.instagram_icon.resize((25, 25), Image.LANCZOS)
        self.instagram_icon = ImageTk.PhotoImage(self.instagram_icon)
        
        self.instagram_button = Button(self.buttons_frame, image=self.instagram_icon, bg="#242323", bd=0, cursor="hand2")
        self.instagram_button.place(x=1050, y=15)
        
        #twitter icon as a button
        self.twitter_icon = Image.open("social/twitter.png")
        self.twitter_icon = self.twitter_icon.resize((25, 25), Image.LANCZOS)
        self.twitter_icon = ImageTk.PhotoImage(self.twitter_icon)
        
        self.twitter_button = Button(self.buttons_frame, image=self.twitter_icon, bg="#242323", bd=0, cursor="hand2")
        self.twitter_button.place(x=1100, y=15)
        
    
        #rest as frame for the rest of the screen with black background
        self.rest_frame = Frame(self.root, bg="black")
        self.rest_frame.place(x=0, y=60, width=1200, height=690)
        
        
        #i'm your pet ai label
        self.pet_ai_label = Label(self.rest_frame, text="I'm your Pet AI", font=("calibri", 30, "bold"), bg="black", fg="white")
        self.pet_ai_label.place(x=500, y=20)
        
        #you can ask me anything about your pet, ask a question label, or ask me to explain the behavior of your pet
        self.ask_label = Label(self.rest_frame, text="You can ask me anything about your pet, ask a question, or ask me to explain the behavior of your pet", font=("calibri", 18), bg="black", fg="white")
        self.ask_label.place(x=80, y=80)
         
        #Example: What are the best foods for my dog?
        self.example_label = Label(self.rest_frame, text="Example: What are the best foods for my dog?", font=("calibri", 18), bg="black", fg="white")
        self.example_label.place(x=400, y=120)
        
        
        #entry box for the question big and wide
        self.question_entry = Entry(self.rest_frame, font=("calibri", 18), bg="white", fg="black", relief="ridge")
        #center the text
        self.question_entry.config(justify="center")
        
        #rounded corners
        self.question_entry.config(highlightthickness=0, bd=0)
        self.question_entry.config(highlightbackground="black", highlightcolor="black")
        self.question_entry.place(x=80, y=180, width=1000, height=50)
        
        #ask button
        # self.ask_button = Button(self.rest_frame, text="Ask", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2",command=self.genetaeResponse)
        self.ask_button = Button(self.rest_frame, text="Ask", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.ask_button.place(x=550, y=250)
        
        
        #generate response
    # def genetaeResponse(self):
    #     #get the question from the entry box
    #     question = self.question_entry.get()
    #     #check if the question is empty
    #     if question == "":
    #         messagebox.showerror("Error", "Please enter a question")
    #         return
        
    #     response = self.rag.query(question)
        
    #     # print(response)
        
    #     #frame for the response
    #     self.response_frame = Frame(self.rest_frame, bg="black")
    #     self.response_frame.place(x=80, y=320, width=1000, height=300)
        
    #     #with borders
    #     self.response_frame.config(highlightbackground="white", highlightcolor="white", highlightthickness=1)
        
    #     #response label
    #     self.response_label = Label(self.response_frame, text=response, font=("calibri", 18), bg="black", fg="white")
    #     #if text is long, wrap it
    #     self.response_label.config(wraplength=950)
    #     self.response_label.place(x=10, y=10)
        
        
    #dogs screen
    def selectDogBreed(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            
            
        #display selectbreed image full screen
        self.bg = Image.open("images/selectbreed.jpg")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        
        
        
        #buttons frame on top
        self.buttons_frame = Frame(self.root, bg="#242323")
        self.buttons_frame.place(x=0, y=0, width=1200, height=60)
        
        #home button
        self.home_button = Button(self.buttons_frame, text="Home", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.home_button.config(command=self.welcomeScreen)
        self.home_button.place(x=400, y=6)
        
        #dogs button
        self.dogs_button = Button(self.buttons_frame, text="Dogs", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.dogs_button.place(x=520, y=6)
        
        #dogs button white
        self.dogs_button.config(bg="white", fg="#242323")
        
        
        #cats button
        self.cats_button = Button(self.buttons_frame, text="Cats", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.cats_button.place(x=640, y=6)
        
        #Pet AI
        self.pet_ai_button = Button(self.buttons_frame, text="Pet AI", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.pet_ai_button.config(command=self.petAiScreen)
        self.pet_ai_button.place(x=760, y=6)
        
        #facebook icon as a button
        self.facebook_icon = Image.open("social/facebook.png")
        self.facebook_icon = self.facebook_icon.resize((25, 25), Image.LANCZOS)
        self.facebook_icon = ImageTk.PhotoImage(self.facebook_icon)
        
        self.facebook_button = Button(self.buttons_frame, image=self.facebook_icon, bg="#242323", bd=0, cursor="hand2")
        self.facebook_button.place(x=1000, y=13)
        
        #instagram icon as a button
        self.instagram_icon = Image.open("social/insta.png")
        self.instagram_icon = self.instagram_icon.resize((25, 25), Image.LANCZOS)
        self.instagram_icon = ImageTk.PhotoImage(self.instagram_icon)
        
        self.instagram_button = Button(self.buttons_frame, image=self.instagram_icon, bg="#242323", bd=0, cursor="hand2")
        self.instagram_button.place(x=1050, y=15)
        
        #twitter icon as a button
        self.twitter_icon = Image.open("social/twitter.png")
        self.twitter_icon = self.twitter_icon.resize((25, 25), Image.LANCZOS)
        self.twitter_icon = ImageTk.PhotoImage(self.twitter_icon)
        
        self.twitter_button = Button(self.buttons_frame, image=self.twitter_icon, bg="#242323", bd=0, cursor="hand2")
        self.twitter_button.place(x=1100, y=15)
        
        #add logo image as a button 
        self.logo = Image.open("images/logout.jpg")
        self.logo = self.logo.resize((40, 40), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_button = Button(self.buttons_frame, image=self.logo, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.logo_button.place(x=20, y=10)
        self.logo_button.config(command=self.loginScreen)
        
        #add profile image as a button
        self.profile = Image.open("images/profile.png")
        self.profile = self.profile.resize((40, 40), Image.LANCZOS)
        self.profile = ImageTk.PhotoImage(self.profile)
        self.profile_button = Button(self.buttons_frame, image=self.profile, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.profile_button.place(x=90, y=10)
        
        
        #select dog breed label bg #272727
        self.select_dog_breed_label = Label(self.root, text="Select Dog Breed", font=("calibri", 30, ), bg="#272727", fg="white")
        self.select_dog_breed_label.place(x=250, y=120)
        
        #dog breeds buttons as text
        #labrador button
        self.labrador_button = Button(self.root, text="Labrador", font=("calibri", 18, "bold"), bg="#272727", fg="white", bd=0, cursor="hand2")
        self.labrador_button.place(x=320, y=250)
        
        #german shepherd button
        self.german_shepherd_button = Button(self.root, text="German Shepherd", font=("calibri", 18, "bold"), bg="#272727", fg="white", bd=0, cursor="hand2")
        self.german_shepherd_button.place(x=280, y=320)
        
        
        #golden retriever button
        self.golden_retriever_button = Button(self.root, text="Golden Retriever", font=("calibri", 18, "bold"), bg="#272727", fg="white", bd=0, cursor="hand2")
        self.golden_retriever_button.place(x=290, y=390)
        
        #french bulldog button
        self.french_bulldog_button = Button(self.root, text="French Bulldog", font=("calibri", 18, "bold"), bg="#272727", fg="white", bd=0, cursor="hand2")
        self.french_bulldog_button.place(x=300, y=460)
        
        #siberian husky button
        self.siberian_husky_button = Button(self.root, text="Siberian Husky", font=("calibri", 18, "bold"), bg="#272727", fg="white", bd=0, cursor="hand2")
        self.siberian_husky_button.place(x=300, y=530)
        
        #config command for the buttons
        # self.labrador_button.config(command=self.dogScreen("Labrador"))
        # self.german_shepherd_button.config(command=self.dogScreen("German Shepherd"))
        # self.golden_retriever_button.config(command=self.dogScreen("Golden Retriever"))
        # self.french_bulldog_button.config(command=self.dogScreen("French Bulldog"))
        # self.siberian_husky_button.config(command=self.dogScreen("Siberian Husky"))
        
    #dog screen
    # def dogScreen(self, breed):
    #     #clear the window
    #     for i in self.root.winfo_children():
    #         i.destroy()
            
    #     #display dog breed image full screen
    #     self.bg = Image.open(f"images/{breed}.jpg")
    #     self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
    #     self.bg = ImageTk.PhotoImage(self.bg)
    #     self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        
        
        
        
        
    #     #buttons frame on top
    #     self.buttons_frame = Frame(self.root, bg="#242323")
    #     self.buttons_frame.place(x=0, y=0, width=1200, height=60)
        
        
    #     #home button
    #     self.home_button = Button(self.buttons_frame, text="Home", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
    #     self.home_button.config(command=self.welcomeScreen)
    #     self.home_button.place(x=400, y=6)
        
    #     #dogs button
    #     self.dogs_button = Button(self.buttons_frame, text="Dogs", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
    #     self.dogs_button.config(command=self.selectDogBreed)
    #     self.dogs_button.place(x=520, y=6)
        
    #     #dogs button white
    #     self.dogs_button.config(bg="white", fg="#242323")
        
    #     #cats button
    #     self.cats_button = Button(self.buttons_frame, text="Cats", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
    #     self.cats_button.place(x=640, y=6)
        
    #     #Pet AI
    #     self.pet_ai_button = Button(self.buttons_frame, text="Pet AI", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
    #     self.pet_ai_button.config(command=self.petAiScreen)
    #     self.pet_ai_button.place(x=760, y=6)
        
    #     #facebook icon as a button
    #     self.facebook_icon = Image.open("social/facebook.png")
    #     self.facebook_icon = self.facebook_icon.resize((25, 25), Image.LANCZOS)
    #     self.facebook_icon = ImageTk.PhotoImage(self.facebook_icon)
        
    #     self.facebook_button = Button(self.buttons_frame, image=self.facebook_icon, bg="#242323", bd=0, cursor="hand2")
    #     self.facebook_button.place(x=1000, y=13)
        
    #     #instagram icon as a button
    #     self.instagram_icon = Image.open("social/insta.png")
    #     self.instagram_icon = self.instagram_icon.resize((25, 25), Image.LANCZOS)
    #     self.instagram_icon = ImageTk.PhotoImage(self.instagram_icon)
        
    #     self.instagram_button = Button(self.buttons_frame, image=self.instagram_icon, bg="#242323", bd=0, cursor="hand2")
    #     self.instagram_button.place(x=1050, y=15)
        
    #     #twitter icon as a button
    #     self.twitter_icon = Image.open("social/twitter.png")
    #     self.twitter_icon = self.twitter_icon.resize((25, 25), Image.LANCZOS)
    #     self.twitter_icon = ImageTk.PhotoImage(self.twitter_icon)

    #     self.twitter_button = Button(self.buttons_frame, image=self.twitter_icon, bg="#242323", bd=0, cursor="hand2")
    #     self.twitter_button.place(x=1100, y=15)
        
        
        
    #     #display breed name label
    #     self.breed_label = Label(self.root, text=breed, font=("calibri", 30, "bold"), bg="#272727", fg="white")
    #     self.breed_label.place(x=500, y=120)
        
    # adding signup page entry boxes data to the database
    def signup_data(self):
    #get the data from the entry boxes
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        mobile = self.mobile_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
         #check if the data is empty
        if first_name == "" or last_name == "" or email == "" or mobile == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "All fields are required")
            return
        #email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid Email")
            return
        #mobile validation
        if not re.fullmatch(r"^[0-9]{10}$", mobile):
            messagebox.showerror("Error", "Invalid Mobile Number")
            return
        #password validation
        if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            messagebox.showerror("Error", "Password must contain at least 8 characters, including letters and numbers")
            return
        #check if the password and confirm password are the same
        if password != confirm_password:
            messagebox.showerror("Error", "Password and Confirm Password should be the same")
            return
        # inserting the data to the database
        cursor = pdsdb.cursor()
        insert_data = f"INSERT INTO user_info (email,first_name,last_name, mobile, password) VALUES ('{email}', '{first_name}', '{last_name}',  '{mobile}', '{password}')"
        cursor.execute(insert_data)
        pdsdb.commit()
        messagebox.showinfo("Success", "You have successfully registered")
        self.loginScreen()
        
    #login page validation with the database
    def login_validation(self):
        #get the data from the entry boxes
        self.email = self.username_entry.get()
        password = self.password_entry.get()
        
        # print("Email:", email)s
        
        # print("Password:", password)
        
        # if email == "" or password == "":
        #     messagebox.showerror("Error", "All fields are required")
        
        # checking the email and password with the database
        cursor = pdsdb.cursor()
        select_data = f"SELECT * FROM user_info WHERE email = '{self.email}' AND password = '{password}'"
        cursor.execute(select_data)
        user = cursor.fetchone()

        if user:
            self.welcomeScreen()
        else:
            messagebox.showerror("Error", "Invalid Email or Password")
            return


    def profile_screen(self):
        for i in self.root.winfo_children():
            i.destroy()
        
        #create a frame for the signup screen
        self.profile_frame = Frame(self.root, bg="black")
        self.profile_frame.place(x=0, y=0, width=1200, height=750)

        #adding pet name label
        self.pet_name_label = Label(self.profile_frame, text="What is your pet Name?", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.pet_name_label.grid(row=0, column=0)

        #adding pet name entry
        self.pet_name_entry = Entry(self.profile_frame,font=("calibri", 15, "bold"), width=28, bg="grey34", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.pet_name_entry.grid(row=0, column=1)

        #adding pet type label
        self.pet_type_label = Label(self.profile_frame, text="Is it dog or cat ?", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.pet_type_label.grid(row=1, column=0)

        self.pet_choice = tk.IntVar()

        # Create radio buttons for Dog or Cat
        self.dog_radio = tk.Radiobutton(self.profile_frame, text="Dog", variable=self.pet_choice, value=1,  font=("calibri", 18, "bold"), bg="#080808", fg="white", activebackground="#080808", activeforeground="white", selectcolor="#080808").grid(row=1, column=1)
        self.cat_radio = tk.Radiobutton(self.profile_frame, text="Cat", variable=self.pet_choice, value=2,  font=("calibri", 18, "bold"), bg="#080808", fg="white", activebackground="#080808", activeforeground="white", selectcolor="#080808").grid(row=1, column=2)
        

        #adding breed entry
        self.pet_name_label = Label(self.profile_frame, text="Enter your pet's breed:?", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.pet_name_label.grid(row=2, column=0)
        self.breed_entry = Entry(self.profile_frame,font=("calibri", 15, "bold"), width=28, bg="grey34", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.breed_entry.grid(row=2, column=1)

        #adding gender label
        self.pet_type_label = Label(self.profile_frame, text="Gender : ", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.pet_type_label.grid(row=3, column=0)

        self.gender_choice = tk.IntVar()

        # Create radio buttons for Male or Female
        self.dog_radio = tk.Radiobutton(self.profile_frame, text="Male", variable=self.gender_choice, value=1,  font=("calibri", 18, "bold"), bg="#080808", fg="white", activebackground="#080808", activeforeground="white", selectcolor="#080808").grid(row=3, column=1)
        self.cat_radio = tk.Radiobutton(self.profile_frame, text="Female", variable=self.gender_choice, value=2,  font=("calibri", 18, "bold"), bg="#080808", fg="white", activebackground="#080808", activeforeground="white", selectcolor="#080808").grid(row=3, column=2)
        

        #Create spinbox widget to get age input
        self.pet_age_label = Label(self.profile_frame, text="How old is your pet ? (in years)", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.pet_age_label.grid(row=4, column=0)
        self.pet_age = tk.Spinbox(self.profile_frame, from_=1, to=40, width=10, font=("calibri", 18, "bold"), bg="#080808", fg="grey50")
        self.pet_age.grid(row=4, column=1)

        scale_var = tk.DoubleVar() 
        self.weight_label = Label(self.profile_frame, text="What is your pet weight ? (in lbs)", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.weight_label.grid(row=5, column=0)
        self.scale_weight = tk.Scale(self.profile_frame, from_=0, to=100, variable=scale_var, resolution=0.1, orient=tk.HORIZONTAL)
        self.scale_weight.grid(row=5, column=1)

        # adding pet_color label & entry
        self.pet_color_label = Label(self.profile_frame, text="what is your pet's color?", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.pet_color_label.grid(row=6, column=0)
        self.pet_color_entry = Entry(self.profile_frame,font=("calibri", 15, "bold"), width=28, bg="grey34", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.pet_color_entry.grid(row=6, column=1)


        #print(self.pet_name_entry.get(), self.pet_selected, self.breed_entry.get(), self.pet_color_entry.get(), self.scale_weight.get(), self.pet_age.get())


        #print(my_pet.name, my_pet.pet_type, my_pet.gender, my_pet.breed, my_pet.color, my_pet.weight, my_pet.age)
        #my_pet = Pet(, self.pet_choice.get(), self.breed_entry.get(), self.gender_choice.get(), , self.pet_color_entry.get(), )
        

        self.insert_pet_button = Button(self.profile_frame, text="Click to Insert Pet Data", font=("calibri", 18, "bold"), bg="grey50", fg="white", bd=0, cursor="hand2", command= self.validate_pet_data)
        self.insert_pet_button.grid(row=8, column=2)

        self.insert_pet_button = Button(self.profile_frame, text="View my Pet Data", font=("calibri", 18, "bold"), bg="grey50", fg="white", bd=0, cursor="hand2", command= self.display_pet_data)
        self.insert_pet_button.grid(row=10, column=2)

        self.insert_pet_button = Button(self.profile_frame, text="Back to Home", font=("calibri", 18, "bold"), bg="grey50", fg="white", bd=0, cursor="hand2", command= self.welcomeScreen)
        self.insert_pet_button.grid(row=16, column=2)

    def insert_pet_data(self, my_pet):
            insert_pet_data = f"INSERT INTO Pet (pet_name, pet_type, pet_gender, breed, pet_color, pet_weight, pet_age, email) VALUES ('{my_pet.name}', '{my_pet.pet_type}', '{my_pet.gender}','{my_pet.breed}', '{my_pet.color}', {my_pet.weight}, {my_pet.age}, 'pavan@gmail.com')"
            cursor.execute(insert_pet_data)
            pdsdb.commit()
            messagebox.showinfo("Success", "You have successfully inserted pet data")

    def validate_pet_data(self):
        self.pet_selected=""
        if self.pet_choice.get()==1:
            self.pet_selected = "Dog"
        elif self.pet_choice.get()==2:
            self.pet_selected = "Cat"

        
        self.gender_selected=""
        if self.gender_choice.get()==1:
            self.gender_selected = "Male"
        elif self.gender_choice.get()==2:
            self.gender_selected = "Female"

        my_pet = Pet()
        my_pet.name = self.pet_name_entry.get()
        my_pet.pet_type = self.pet_selected
        my_pet.gender = self.gender_selected
        my_pet.age = self.pet_age.get()
        my_pet.color = self.pet_color_entry.get()
        my_pet.weight = self.scale_weight.get()
        my_pet.breed =self.breed_entry.get()


        print(my_pet.name, my_pet.pet_type, my_pet.gender, my_pet.breed, my_pet.color, my_pet.weight, my_pet.age)

        #check pet name exists or not for the user to avoid duplicate entry
        get_pet_data = f"SELECT pet_name FROM pet WHERE email = 'pavan@gmail.com'"
        cursor.execute(get_pet_data)
        pet_data = cursor.fetchall()

        # Storing the fetched pet name
        for pet in pet_data:
             self.pet_name = pet[0]
        
        if my_pet.name=="" or my_pet.pet_type=="" or my_pet.gender=="" or my_pet.breed=="" or my_pet.color=="" or my_pet.weight==0 or my_pet.age==0:    
            messagebox.showerror("Failed", "All fields are mandatory")
        elif self.pet_name == my_pet.name:
            messagebox.showerror("Failed", "You have a pet already with this name")
        else:
            self.insert_pet_data(my_pet)
    
    def display_pet_data(self):
        for i in self.root.winfo_children():
            i.destroy()
        
        #create a frame to display pet data
        self.pet_data_frame = Frame(self.root, bg="black")
        self.pet_data_frame.place(x=0, y=0, width=1200, height=750)

        # Create a Treeview widget for the table
        tree = ttk.Treeview(self.pet_data_frame, columns=("Name", "Type", "Gender", "Breed", "Color", "Weight", "Age"))

        # Define column headings
        tree.heading("#0", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Type", text="Type")
        tree.heading("Gender", text="Gender")
        tree.heading("Breed", text="Breed")
        tree.heading("Color", text="Color")
        tree.heading("Weight", text="Weight")
        tree.heading("Age", text="Age")

        # Set the column widths
        tree.column("#0",  width=100)  # Id column
        tree.column("Name",  width=100) # Name column
        tree.column("Age",  width=100)  # Age column
        tree.column("Gender",  width=100)  # Gender column
        tree.column("Weight",  width=100)  # Weight column
        tree.column("Color",  width=100)  # Color column
        tree.column("Breed",  width=100)  # Breed column
        tree.column("Type",  width=100) 

        # Insert data into the table
        pet_array = self.get_pet_data()

        print(pet_array)

        for idx, pet in enumerate(pet_array, start=1):
            tree.insert("", "end", text=str(idx), values=(
                pet.name,  pet.pet_type, pet.gender, pet.breed, pet.color, pet.weight, pet.age
            ))
        # Change foreground and background colors
        tree.tag_configure('oddrow', background='grey50', foreground='white')
        tree.tag_configure('evenrow', background='white', foreground='black')

        # Apply colors to rows
        for idx, item in enumerate(tree.get_children()):
            if idx % 2 == 0:
                tree.item(item, tags=('evenrow',))
            else:
                tree.item(item, tags=('oddrow',))

        # Pack the Treeview widget and expand it
        tree.place(x=100, y=30)

         #adding login button
        self.login_button = Button(self.pet_data_frame, text="Back to Profile", font=("calibri",18,"bold"), bg="#080808", fg="white", bd=0, cursor="hand2",activebackground="#080808",activeforeground="grey",command=self.profile_screen)
        self.login_button.place(x=460, y=650)



    def get_pet_data(self):
        print(self.email)
        get_pet_data = f"SELECT * FROM pet WHERE email = '{self.email}'"
        cursor.execute(get_pet_data)
        pet_data = []
        for row in cursor.fetchall():
                 my_pet = Pet()
                 my_pet.name = row[1]
                 my_pet.pet_type = row[2] 
                 my_pet.gender = row[3]
                 my_pet.breed = row[4]  
                 my_pet.color = row[5]  
                 my_pet.weight = row[6]  
                 my_pet.age = row[7]  
                 pet_data.append(my_pet)
                 print(my_pet.display_info())

        messagebox.showinfo("Success", "You have successfully retrieved pet data")

        return pet_data

        
        
    
        

        
        
    
        
        
        
            
        
        
        
        
        
        
        
        
        
        
        





#starter code
if __name__ == "__main__":
    root = Tk()
    app = PawfectPortions(root)
    root.mainloop()