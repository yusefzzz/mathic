import customtkinter as ctk 
import mysql.connector, ssl, smtplib, random, hashlib 
from email.message import EmailMessage 
from PIL import Image

emailSender = "*************@gmail.com" 
emailPassword = "**** **** **** ****"

HOSTNAME = "sql8.freesqldatabase.com"
USERNAME = "sql8677293"
PASSWORD = "**********"         
DATABASE = "sql8677293"

ctk.set_appearance_mode("dark")

config = open("userconfig.txt", "r") 
lines = config.readlines()
configLogged = lines[3].strip()
if configLogged == "unlogged":
    LOGGEDIN = False
elif configLogged == "logged":
    LOGGEDIN = True

class BUTTON(ctk.CTkButton):
    def __init__(MAIN, *args,
        width = 300,
        height = 50,
        text = "Loading...",
        font = ("HACKED", 25),
        corner_radius = 50,
        image = None,
        hover_color = "#7f5200",
        fg_color = "#3e3e3e",
        bg_color = "transparent",
        command = None,
        **kwargs):
        super().__init__(*args, 
            width = width, 
            height = height, 
            text = text, 
            font = font, 
            corner_radius = corner_radius,
            hover_color = hover_color, 
            image = image, 
            fg_color = fg_color, 
            bg_color = bg_color,
            command = command,
            **kwargs)
        
class LABEL(ctk.CTkLabel):
    def __init__(MAIN, *args,
        font = ("Century Gothic", 15),
        text = "Loading...",
        wraplength = 500,
        justify = "left",
        text_color = "White",
        fg_color = "transparent",
        **kwargs):
        super().__init__(*args, 
            font = font, 
            text_color = text_color, 
            text = text, 
            wraplength = wraplength, 
            justify = justify, 
            fg_color = fg_color, 
            **kwargs) 
        
class ERRORLABEL(LABEL): 
    def __init__(MAIN, *args,
        text = "Error",
        text_color = "Red",
        font = ("Century Gothic", 12),
        wraplength = 400,
        fg_color = "transparent",
        **kwargs):
        super().__init__(*args, 
            text = text, 
            text_color = text_color, 
            wraplength = wraplength, 
            font = font, 
            fg_color = fg_color, 
            **kwargs) 

class ENTRY(ctk.CTkEntry):
    def __init__(MAIN, *args,
        placeholder_text = "...",
        font = ("Century Gothic", 15),
        width = 500,
        height = 30,
        border_color = "Grey",
        **kwargs):
        super().__init__(*args, 
            font = font, 
            placeholder_text = placeholder_text, 
            width = width, 
            height = height, 
            border_color = border_color, 
            **kwargs) 


def connect():
    try:
        conn = mysql.connector.connect(
        host=HOSTNAME,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE)
        return conn
    except:
        print("Error - couldn't connect to database")

class APP(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.resizable(False, False)
        self.title("Mathic: Log in")
        self.iconbitmap("appmathiclogo.ico")
        
        imageLabel = ctk.CTkLabel(self,
            text = "",
            image = ctk.CTkImage(dark_image = Image.open("mathicloading.png"), 
                size = (800, 800)))
        imageLabel.place(x = 0, y = 0)  

        loginButton = BUTTON(self,
            text = "LOG IN",
            corner_radius = 0,
            command = self.logIn)
        loginButton.place(relx = 0.5,
            rely = 0.75,
            anchor = ctk.CENTER)

        createButton = BUTTON(self,
            text = "CREATE ACCOUNT",
            corner_radius = 0,
            command = self.createAccount)
        createButton.place(relx = 0.5,
            rely = 0.85,
            anchor = ctk.CENTER)

    def logIn(self):
        APP.destroy(self) 
        app = LOGIN() 
        app.mainloop(self) 

    def createAccount(self):
        APP.destroy(self) 
        app = CREATEACCOUNT() 
        app.mainloop(self) 
    
class LOGIN(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.resizable(False, False)
        self.geometry(f'+{x}+{y}')

        def login():
            LOGIN.destroy(self) 
            app = LOGIN() 
            app.mainloop(self) 

        def hidePassword():
            self.passwordEntry.configure(show = "*")
            self.showButton.configure(image = ctk.CTkImage(dark_image = Image.open("closedeye.png")),
                command = showPassword)

        def showPassword():
            self.passwordEntry.configure(show = "")
            self.showButton.configure(image = ctk.CTkImage(dark_image = Image.open("openeye.png")),
                command = hidePassword)

        def checkPassword():
            password = self.passwordEntry.get()
            confirmPassword = self.confirmEntry.get()
            try:
                self.errorLabel1.destroy()
            except: 
                pass
            try:
                self.errorLabel2.destroy()
            except: 
                pass

            if len(password) < 8 or len(password) > 24:
                self.passwordEntry.configure(border_color = "Red")
                self.errorLabel1 = ERRORLABEL(self,
                    text = "Please enter a valid password")
                self.errorLabel1.place(relx = 0.18, rely = 0.55)
            else:
                self.passwordEntry.configure(border_color = "Grey")           
                if password != confirmPassword:
                    self.errorLabel2 = ERRORLABEL(self,
                        text = "Passwords don't match")
                    self.errorLabel2.place(relx = 0.18, rely = 0.55)
                else:
                    hashedNewpassword = hashlib.sha256(password.encode()).hexdigest()
                    conn = connect()
                    cursor = conn.cursor() 
                    try:
                        query = "UPDATE tblStudent SET password = %s WHERE email = %s"
                        cursor.execute(query, (hashedNewpassword, self.email,))        
                        conn.commit()
                    except:
                        query = "UPDATE tblTeacher SET password = %s WHERE email = %s"
                        cursor.execute(query, (hashedNewpassword, self.email,))        
                        conn.commit()                        
                    cursor.close()
                    conn.close()
                    for item in self.winfo_children():
                        item.destroy()
                    successLabel = LABEL(self,
                        text = "PASSWORD  CHANGED  SUCCESSFULLY.  YOU  MAY  NOW  LOG  IN",
                        font = ("HACKED", 30),
                        justify = "center")
                    successLabel.place(relx = 0.5, rely = 0.45, anchor = ctk.CENTER)
                    self.enterButton = BUTTON(self,
                        text = "LOG IN",
                        command = login)
                    self.enterButton.place(relx = 0.5, rely = 0.70, anchor = ctk.CENTER)

        def resetPassword():
            for item in self.winfo_children():
                item.destroy()
            newPasswordLabel = LABEL(self,
                text = "Create your new password")
            newPasswordLabel.place(relx = 0.15, rely = 0.33)
            self.passwordEntry =  ENTRY(self,
                placeholder_text = "Password - between 8 and 24 characters ",
                show = "*")
            self.passwordEntry.place(relx = 0.18, rely = 0.45) 
            self.confirmEntry =  ENTRY(self,
                placeholder_text = "Confirm password",
                show = "*")
            self.confirmEntry.place(relx = 0.18, rely = 0.50) 
            enterButton = BUTTON(self,
                text = "ENTER",
                command = checkPassword)
            enterButton.place(relx = 0.50,
                rely = 0.80,
                anchor = ctk.CENTER)
            self.showButton = BUTTON(self,
                width = 20,
                height = 20,
                text = "",
                image = ctk.CTkImage(dark_image = Image.open("closedeye.png")),
                fg_color = "#3e3e3e",
                command = showPassword)
            self.showButton.place(x = 670, rely = 0.55) 

        def checkCode(sixcode):
            code = self.confirmationEntry.get()
            if str(sixcode) == str(code):
                self.confirmationEntry.configure(border_color = "Grey")
                resetPassword()
            else:
                self.confirmationEntry.configure(border_color = "Red")
                self.errorLabel = ERRORLABEL(self,
                    text = "Wrong code")
                self.errorLabel.place(relx = 0.18, rely = 0.50)            

        def sendEmail(email):
            self.email = email
            sixcode = f"{random.randint(0, 999999):06d}" 
            for item in self.winfo_children():
                item.destroy()
            confirmationLabel = LABEL(self,
                    text = "Please check your emails for a 6-digit confirmation code that we have just sent. You may also check spam.")
            confirmationLabel.place(relx = 0.18, rely = 0.33)
            self.confirmationEntry =  ENTRY(self,
                placeholder_text = "Enter 6-digit code")
            self.confirmationEntry.place(relx = 0.18, rely = 0.46)
            enterButton = BUTTON(self,
                text = "ENTER",
                command = lambda sixcode = sixcode: checkCode(sixcode))
            enterButton.place(relx = 0.50,
                rely = 0.80,
                anchor = ctk.CENTER)
            
            emailReceiver = email 
            subject = "Reset password - Do not reply to this email"
            body = """
            It seems that you have requested to change your password 
            Enter the following 6 digit code in the Mathic app:

            {}
            """.format(sixcode)
                    
            em = EmailMessage() 
            em["From"] = emailSender
            em["To"] = emailReceiver
            em["Subject"] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
                smtp.login(emailSender, emailPassword)
                smtp.sendmail(emailSender, emailReceiver, em.as_string()) # # #
        
        def checkEmail():
            validEmail = False
            foundEmail = False
            try:
                self.errorLabel1.destroy()
            except:
                pass
            try:
                self.errorLabel2.destroy()
            except:
                pass
            email = self.emailEntry.get()

            if "@gmail.com" not in email and "@outlook.org.uk" not in email and "@beauchamp.org.uk" not in email:                #if "@" not in email or "." not in email or "@." in email:  ## CHANGE TO HAVE MORE POSSIBLE EMAIL DOMAINS/NEW CLIENTS
                self.emailEntry.configure(border_color = "Red")
            else:
                if email[0] == "@":
                    self.emailEntry.configure(border_color = "Red")
                else:             
                    self.emailEntry.configure(border_color = "Grey")
                    validEmail = True
     
            if validEmail == True:
                conn = connect()
                cursor = conn.cursor()        
                cursor.execute("SELECT email FROM tblStudent")
                emails = cursor.fetchall()
                for item in emails:
                    item = str(item).replace("('", "").replace("',)", "")
                    if item == email:
                        foundEmail = True
                        break
                if foundEmail == False:
                    cursor.execute("SELECT email FROM tblTeacher")
                    emails = cursor.fetchall()
                    for item in emails:
                        item = str(item).replace("('", "").replace("',)", "")
                        if item == email:
                            foundEmail = True
                            break
                cursor.close()
                conn.close()
                if foundEmail == True:
                    sendEmail(email)
                else:
                    self.errorLabel2 = ERRORLABEL(self,
                        text = "Email not found")
                    self.errorLabel2.place(relx = 0.18, rely = 0.5)    
            else:
                self.errorLabel1 = ERRORLABEL(self,
                    text = "Please enter a valid set of variables")
                self.errorLabel1.place(relx = 0.18, rely = 0.5)                                

        def forgotPassword():
            for item in self.winfo_children():
                item.destroy()
            emailLabel = LABEL(self,
                    text = "Please enter your email in order to send a verification code")
            emailLabel.place(relx = 0.18, rely = 0.33)
            self.emailEntry =  ENTRY(self, 
                placeholder_text = "Email")
            self.emailEntry.place(relx = 0.18, rely = 0.46)
            enterButton = BUTTON(self,
                text = "ENTER",
                command = checkEmail)
            enterButton.place(relx = 0.50,
                rely = 0.80,
                anchor = ctk.CENTER)

        def checkLogin():
            username = usernameEntry.get()
            password = self.passwordEntry.get()
            hashedPassword = hashlib.sha256(password.encode()).hexdigest()
            foundMatch = False
            type = ""

            try:
                self.errorLabel.destroy()
            except:
                pass

            if len(username) == 0 or len(password) == 0:
                self.errorLabel = ERRORLABEL(self,
                    text = "Invalid entries")
                self.errorLabel.place(relx = 0.203, rely = 0.63)
            else:
                conn = connect()
                cursor = conn.cursor()     
                query  = "SELECT username FROM tblStudent WHERE username = %s and password = %s"
                cursor.execute(query, (username, hashedPassword))
                result = cursor.fetchone()
                if result is not None:
                    foundMatch = True 
                    type = "Student"
                else:
                    query  = "SELECT username FROM tblTeacher WHERE username = %s and password = %s"
                    cursor.execute(query, (username, hashedPassword))
                    result = cursor.fetchone()
                    if result is not None:
                        foundMatch = True 
                        type = "Teacher"
                cursor.close()
                conn.close()
                               
                if foundMatch == True:
                    for item in self.winfo_children():
                        item.destroy()
                    successLabel = LABEL(self,
                        text = "LOGGED  IN  SUCCESSFULLY.  LOADING . . .",
                        font = ("HACKED", 30),
                        justify = "center")
                    successLabel.place(relx = 0.5, rely = 0.45, anchor = ctk.CENTER)
                    with open("userconfig.txt", "r") as file: 
                        lines = file.readlines()
                        if lines[1] != username + "\n":
                            lines[4] = "None"
                        lines[1] = username + "\n" 
                        lines[2] = type + "\n"
                        lines[3] = "logged" + "\n"
                    with open("userconfig.txt", "w") as file: 
                        file.writelines(lines)
                    LOGIN.destroy(self)
                else:
                    self.errorLabel = ERRORLABEL(self,
                        text = "Username and password don't match")
                    self.errorLabel.place(relx = 0.203, rely = 0.63)
                cursor.close()
                conn.close() 

        bigLabel = LABEL(self,
            text = "LOG IN",
            font = ("HACKED", 70),
            justify = "center")
        bigLabel.place(relx = 0.5, rely = 0.3, anchor = ctk.CENTER)
        usernameEntry = ENTRY(self,
            placeholder_text = "Username")
        usernameEntry.place(x = 160, rely = 0.50)
        self.passwordEntry = ENTRY(self,
            placeholder_text = "Password",
            show = "*")
        self.passwordEntry.place(x = 160, rely = 0.55)
        self.showButton = BUTTON(self,
            width = 20,
            height = 20,
            text = "",
            image = ctk.CTkImage(dark_image = Image.open("closedeye.png")),
            fg_color = "#3e3e3e",
            command = showPassword)
        self.showButton.place(x = 670, rely = 0.55) 
        forgotButton = ctk.CTkButton(self,
            height = 5,
            width = 5,
            font = ("Century Gothic", 12),
            fg_color = "transparent",
            text="Forgot Password?",
            hover_color = "#7f5200",
            command = forgotPassword)
        forgotButton.place(x = 160, rely = 0.60)
        logInButton = BUTTON(self, 
            text = "LOG IN",
            command = checkLogin)
        logInButton.place(relx = 0.5,
            rely = 0.70,
            anchor = ctk.CENTER)

class CREATEACCOUNT(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.resizable(False, False)
        self.title("Mathic: Create Account")
        self.geometry(f'+{x}+{y}')

        def hidePassword():
            passwordEntry.configure(show = "*")
            showButton.configure(image = ctk.CTkImage(dark_image = Image.open("closedeye.png")),
                command = showPassword)

        def showPassword():
            passwordEntry.configure(show = "")
            showButton.configure(image = ctk.CTkImage(dark_image = Image.open("openeye.png")),
                command = hidePassword)

        def options(option):
            if option == "Teacher":
                self.teacherNameEntry = ENTRY(self,
                    placeholder_text = "Teacher Name")
                self.teacherNameEntry.place(relx = 0.2, rely = 0.40)
            else:
                try:
                    self.teacherNameEntry.destroy()
                except:
                    pass        

        def checkCode(sixcode):
            username = self.username
            email = self.email
            password = self.password
            choice = self.choice
            name = self.name
            createNew = False
            hashedPassword = hashlib.sha256(password.encode()).hexdigest()
            try:
                self.errorLabel.destroy()
            except:
                pass
            code = self.confirmationEntry.get()
            if sixcode == code:
                self.confirmationEntry.configure(border_color = "Grey")
                createNew = True
            else:
                self.confirmationEntry.configure(border_color = "Red")
                self.errorLabel = ERRORLABEL(self,
                    text = "Wrong code")
                self.errorLabel.place(relx = 0.18, rely = 0.50)

            if createNew == True:
                conn = connect()                                                                                                # Try except connection
                cursor = conn.cursor() 
                if choice == "Student":
                    insertQuery = "INSERT INTO tblStudent (username, email, password) VALUES (%s, %s, %s)"   
                    cursor.execute(insertQuery, (username, email, hashedPassword))   
                elif choice == "Teacher":
                    insertQuery = "INSERT INTO tblTeacher (username, email, password, teachername) VALUES (%s, %s, %s, %s)"   
                    cursor.execute(insertQuery, (username, email, hashedPassword, name))   
                conn.commit()
                cursor.close()
                conn.close()
                for item in self.winfo_children():
                    item.destroy()
                successLabel = LABEL(self,
                    text = "ACCOUNT  CREATED  SUCCESSFULLY.  YOU  MAY  NOW  LOG  IN",
                    font = ("HACKED", 30),
                    justify = "center")
                successLabel.place(relx = 0.5, rely = 0.45, anchor = ctk.CENTER)
                enterButton = BUTTON(self,
                    text = "LOG IN",
                    command = login)
                enterButton.place(relx = 0.5, rely = 0.70, anchor = ctk.CENTER)


        def sendEmail(sixcode):
            confirmationLabel = LABEL(self,
                    text = "Please check your emails for a 6-digit confirmation code that we have just sent. You may also check spam.")
            confirmationLabel.place(relx = 0.18, rely = 0.33)
            self.confirmationEntry = ENTRY(self,
                placeholder_text = "Enter 6-digit code")
            self.confirmationEntry.place(relx = 0.18, rely = 0.46)
            enterButton = BUTTON(self,
                text = "ENTER",
                command = lambda sixcode = sixcode: checkCode(sixcode))
            enterButton.place(relx = 0.50,
                rely = 0.80,
                anchor = ctk.CENTER)
            
            emailReceiver = self.email
            subject = "Confirmation code - Do not reply to this email"
            body = """
            Thank you for creating your account in Mathic! 
            You are one step away from starting your journey with us.
            Enter the following 6 digit code in the Mathic app:

            {}
            """.format(sixcode)
            
            em = EmailMessage()
            em["From"] = emailSender
            em["To"] = emailReceiver
            em["Subject"] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
                smtp.login(emailSender, emailPassword)
                smtp.sendmail(emailSender, emailReceiver, em.as_string())

        def checkEntries():
            self.choice = typeOption.get()
            username = usernameEntry.get()
            password = passwordEntry.get()
            email = emailEntry.get()
            self.name = ""
            error = False
            foundEmail = False
            foundUsername = False
            validUsername = True
            validEmail = True
            self.username = username
            self.email = email
            self.password = password

            try:
                self.errorLabel1.destroy()
            except:
                pass
            try:
                self.errorLabel2.destroy()
            except:
                pass
            try:
                self.errorLabel3.destroy()
            except:
                pass

            if self.choice == "Teacher":
                self.name = self.teacherNameEntry.get()
                if len(self.name) == 0:
                    error = True
                    self.teacherNameEntry.configure(border_color = "Red")
                    validUsername = False
                else:
                    self.teacherNameEntry.configure(border_color = "Grey")

            if len(username) < 6 or len(username) > 16:
                error = True
                usernameEntry.configure(border_color = "Red")
                validUsername = False
            else:
                usernameEntry.configure(border_color = "Grey")

            if len(password) < 8 or len(password) > 24:
                error = True
                passwordEntry.configure(border_color = "Red")
            else:
                passwordEntry.configure(border_color = "Grey")

            if "@gmail.com" not in email and "@outlook.org.uk" not in email and "@beauchamp.org.uk" not in email:                #if "@" not in email or "." not in email or "@." in email:  ## CHANGE TO HAVE MORE POSSIBLE EMAIL DOMAINS/NEW CLIENTS
                error = True
                emailEntry.configure(border_color = "Red")
                validEmail = False
            else:
                if email[0] == "@":
                    error = True
                    emailEntry.configure(border_color = "Red")
                    validEmail = False       
                else:             
                    emailEntry.configure(border_color = "Grey")

            if error == True:
                self.errorLabel1 = ERRORLABEL(self,
                    text = "Please enter a valid set of variables")
                self.errorLabel1.place(relx = 0.2, rely = 0.6)
            
            if validEmail == True:
                conn = connect()
                cursor = conn.cursor()    
                while foundEmail == False:       
                    cursor.execute("SELECT email FROM tblStudent")
                    emails = cursor.fetchall()
                    for item in emails:
                        item = str(item).replace("('", "").replace("',)", "")
                        if item == email:
                            foundEmail = True
                            break
                    cursor.execute("SELECT email FROM tblTeacher")
                    emails = cursor.fetchall()
                    for item in emails:
                        item = str(item).replace("('", "").replace("',)", "")
                        if item == email:
                            foundEmail = True
                            break
                    break
                cursor.close()
                conn.close()
                if foundEmail == True:
                    validEmail = False
                    self.errorLabel2 = ERRORLABEL(self,
                        text = "Email address already in use")
                    emailEntry.configure(border_color = "Red")
                    if error == True:
                        self.errorLabel2.place(relx = 0.2, rely = 0.63)
                    elif error == False:
                        self.errorLabel2.place(relx = 0.2, rely = 0.60)
                else:
                    emailEntry.configure(border_color = "Grey")

            if validUsername == True:
                conn = connect()
                cursor = conn.cursor() 
                while foundUsername == False:       
                    cursor.execute("SELECT username FROM tblStudent")
                    usernames = cursor.fetchall()
                    for item in usernames:
                        item = str(item).replace("('", "").replace("',)", "")
                        if item == username:
                            foundUsername = True
                            break
                    cursor.execute("SELECT username FROM tblTeacher")
                    usernames = cursor.fetchall()
                    for item in usernames:
                        item = str(item).replace("('", "").replace("',)", "")
                        if item == username:
                            foundUsername = True
                            break
                    break
                cursor.close()
                conn.close()
                if foundUsername == True:
                    validUsername = False
                    self.errorLabel3 = ERRORLABEL(self,
                        text = "Username already in use")
                    usernameEntry.configure(border_color = "Red")
                    if error == True:
                        if foundEmail == True:
                            self.errorLabel3.place(relx = 0.2, rely = 0.66)
                        else:
                            self.errorLabel3.place(relx = 0.2, rely = 0.63)
                    elif error == False:
                        if foundEmail == True:
                            self.errorLabel3.place(relx = 0.2, rely = 0.63)
                        else:
                            self.errorLabel3.place(relx = 0.2, rely = 0.60)
                else:
                    usernameEntry.configure(border_color = "Grey")

            if validEmail == True and validUsername == True and error == False:
                sixcode = f"{random.randint(0, 999999):06d}" 
                for item in self.winfo_children():
                    item.destroy()
                sendEmail(sixcode)
        
        def login():
            CREATEACCOUNT.destroy(self) 
            app = LOGIN() 
            app.mainloop(self) 

        bigLabel = LABEL(self,
            text = "CREATE ACCOUNT",
            font = ("HACKED", 70),
            justify = "center")
        bigLabel.place(relx = 0.5, 
            rely = 0.3, 
            anchor = ctk.CENTER)
        emailEntry = ENTRY(self,
            placeholder_text = "Email")
        emailEntry.place(relx = 0.2, 
            rely = 0.50)
        usernameEntry = ENTRY(self,
            placeholder_text = "Username - between 6 and 16 characters")
        usernameEntry.place(relx = 0.2, 
            rely = 0.45)
        passwordEntry = ENTRY(self,
            placeholder_text = "Password - between 8 and 24 characters",
            show = "*")
        passwordEntry.place(relx = 0.2, 
            rely = 0.55)
        checkCreateButton = BUTTON(self,
            text = "CREATE ACCOUNT",
            command = checkEntries)
        checkCreateButton.place(relx = 0.5,
            rely = 0.80,
            anchor = ctk.CENTER)
        typeOption = ctk.CTkOptionMenu(self,
            values = ["Student", "Teacher"],
            fg_color = "#7f5200",
            dropdown_fg_color = "#7f5200",
            button_color = "#7f5200",
            button_hover_color = "#7f5200",
            command = options)
        typeOption.set("Student")
        typeOption.place(relx = 0.65, rely = 0.6)
        showButton = BUTTON(self,
            width = 20,
            height = 20,
            text = "",
            image = ctk.CTkImage(dark_image = Image.open("closedeye.png")),
            fg_color = "#3e3e3e",
            command = showPassword)
        showButton.place(x = 670, rely = 0.55) 

if not LOGGEDIN:
    app = APP()
    width = 800
    height = 800
    x = int(app.winfo_screenwidth()/2 - width/2)
    y = int(app.winfo_screenheight()/2 - height/2)
    app.geometry(f'+{x}+{y}')

    app.mainloop()