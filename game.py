import customtkinter as ctk
from PIL import Image
import mysql.connector, random, sys, subprocess 

HOSTNAME = "sql8.freesqldatabase.com" 
USERNAME = "sql8677293"
PASSWORD = "**********"
DATABASE = "sql8677293"

ctk.set_appearance_mode("dark")

colorsArray = [("blue", "#000066"),
    ("red", "#660000"),
    ("green", "#003300"),
    ("cyan", "#006666"),
    ("magenta", "#660066"),
    ("orange", "#7f5200"),
    ("grey", "#696969")]

config = open("userconfig.txt", "r") 
lines = config.readlines()
configColor =  lines[0].strip()
for item in colorsArray: 
    if configColor in item: 
        color = item[1] 
        color2 = configColor 
configLogged = lines[3].strip()
if configLogged == "unlogged":
    import login

class BUTTON(ctk.CTkButton): 
    def __init__(MAIN, *args,
        width = 160,
        height = 60,
        text = "Loading...",
        font = ("HACKED", 22),
        image = None,
        hover_color = color,
        border_width = None,
        border_color = None,
        fg_color = "#3e3e3e",
        command = None,
        **kwargs):
        super().__init__(*args, 
            width = width, 
            height = height, 
            text = text, 
            font = font, 
            hover_color = hover_color, 
            border_width = border_width, 
            border_color = border_color, 
            image = image, 
            fg_color = fg_color, 
            command = command,
            **kwargs) 

class FRAME(ctk.CTkFrame): 
    def __init__(MAIN, *args,
        width = None,
        height = None,
        border_width = 2,
        border_color = color2,
        fg_color = "#2e2e2e",
        **kwargs):
        super().__init__(*args, 
            width = width, 
            height = height, 
            fg_color = fg_color, 
            border_width = border_width, 
            border_color = border_color, 
            **kwargs) 

class LABEL(ctk.CTkLabel):
    def __init__(MAIN, *args,
        font = ("Century Gothic", 40),
        text = "Loading...",
        wraplength = 1000,
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
        wraplength = 1000, 
        fg_color = "#2e2e2e", 
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
        font = ("Century Gothic", 16),
        border_color = color2,
        width = 200,
        height = 20,
        **kwargs):
        super().__init__(*args, 
            font = font, 
            placeholder_text = placeholder_text, 
            border_color = border_color, 
            width = width, 
            height = height, 
            **kwargs) 

def restart(): 
    python = sys.executable
    currentScript = __file__  
    subprocess.Popen([python, currentScript])
    sys.exit()

def toggleFullscreen(event = None): 
    state = not app.attributes('-fullscreen')
    app.attributes('-fullscreen', state)

def exitFullscreen(event = None):
    app.attributes('-fullscreen', False)

def logOut():
    config = open("userconfig.txt", "r") 
    lines = config.readlines()
    lines[3] = "unlogged" + "\n" 
    config = open("userconfig.txt", "w")
    config.writelines(lines)  
    sys.exit()

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

class MAIN(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}")
        self.geometry("0+0")
        self.title("Mathic")
        self.iconbitmap("appmathiclogo.ico")
        self.resizable(False, False)                   
        self.bind('<F11>', toggleFullscreen) 
        self.bind('<Escape>', exitFullscreen)  
        self.buttons = [("  Dashboard", 200, "dashboard.png", self.dashboard),
            ("  Play", 260, "play.png", self.play), 
            ("  Classroom", 320, "classroom.png", self.classroom),
            ("  Quit", 0.8, "quit.png", self.quit)]
        self.topicNames = [("Numbers", "numberstopic.jpg"),
            ("Algebra", "algebratopic.jpg"),
            ("Graphs", "graphstopic.jpg"),
            ("Ratio and Proportion", "ratiotopic.jpg"),
            ("Geometry and Shapes", "geometrytopic.jpg"),
            ("Stats and Probability", "statstopic.jpg")]
        self.EXPANDWIDTH = self.width -250
        self.CONTRACTWIDTH = self.width - 70
        self.buttonMenu = {}
        self.typeWindow = ""
        self.disabledButton = ""
        self.menuContracted = False
        self.dashboard()

    def contract(self):
        for i in range(0,4):
            self.buttonMenu[str(i)].destroy()
        self.menuContracted = True
        self.typeWindow.place(x = 70, y = 0)
        self.optionsFrame.configure(self,
            width = 70)
        self.customiseFrame.destroy()
        self.expandButton.place(x = 60, rely = 0.5)
        self.expandButton.configure(command = self.expand)

        index = 0
        for item in self.buttons:
            buttonName = str(index)
            button = ctk.CTkButton(master = self.optionsFrame,
                height = 50,
                width = 50,
                corner_radius = 5,
                text = "",
                fg_color = "#2e2e2e",
                hover_color = "#1e1e1e",
                image = ctk.CTkImage(dark_image = Image.open(item[2])),
                compound = "left",
                command = item[3])
            if "Quit" in item[0]:
                button.place(x = 10, rely = item[1])
            else:
                button.place(x = 10, y = item[1])
            self.buttonMenu[buttonName] = button
            index += 1
        self.buttonMenu[self.disabledButton].configure(state = "disabled")

    def expand(self):  
        self.menuContracted = False
        self.typeWindow.place(x = 250, y = 0) 
        self.optionsFrame = ctk.CTkFrame(self,
            width = 250,
            height = self.height,
            fg_color = "#1e1e1e")
        self.optionsFrame.place(relx = 0, rely = 0)
        self.expandButton = ctk.CTkButton(master = self.optionsFrame, 
            width = 17,
            height = 50,
            text = "",
            fg_color = "grey",
            command = self.contract) 
        self.expandButton.place(x = 240, rely = 0.5)
        self.customiseFrame = ctk.CTkFrame(master = self.optionsFrame,
            width = 210,
            height = 150)
        self.customiseFrame.place(x = 20, y = 20)
        self.customiseLabel = ctk.CTkLabel(master = self.customiseFrame,
            text = "Customise theme",
            font = ("HACKED", 26))    
        self.customiseLabel.place(x = 20, y = 20)

        index = 0
        for item in self.buttons:
            buttonName = str(index)
            button = ctk.CTkButton(master = self.optionsFrame,
            height = 50,
            width = 230,
            corner_radius = 5,
            text = item[0],
            font = ("HACKED", 20),
            fg_color = "#2e2e2e",
            anchor = "w",
            hover_color = "#1e1e1e",
            image = ctk.CTkImage(dark_image = Image.open(item[2])),
            compound = "left",
            command = item[3])
            if "Quit" in item[0]:
                button.place(x = 10, rely = item[1]) 
            else:
                button.place(x = 10, y = item[1])
            self.buttonMenu[buttonName] = button
            index += 1
        self.buttonMenu[self.disabledButton].configure(state = "disabled")

        self.customise()
        
    def customise(self):

        def changeTheme(color):

            def noRestart():
                restartWindow.destroy()

            file = open("userconfig.txt", "r") 
            lines = file.readlines()
            lines[0] = color[0] + "\n"
            lines[1] = WELCOMEUSER + "\n" 
            lines[2] = TYPEACCOUNT + "\n"
            lines[3] = "logged" + "\n"
            file = open("userconfig.txt", "w") 
            file.writelines(lines) 
            
            restartWindow = ctk.CTkToplevel(app)
            restartWindow.geometry("300x300") 
            restartWindow.geometry(f"{(self.width - 300)//2}+{(self.height - 300)//2}")
            restartWindow.title("Warning")
            restartWindow.resizable(False, False)
            label = LABEL(restartWindow, 
                text ="Please restart the app to apply changes. Do you want to restart now? Any unsaved progress will be lost", 
                font = ("Century Gothic Bold", 18),
                wraplength = 250)
            label.pack(padx = 10, pady = 50)
            yesButton = BUTTON(restartWindow, 
                text = "Yes",
                width = 100,
                height = 60,
                command = restart)
            noButton = BUTTON(restartWindow, 
                text = "No",
                width = 100,
                height = 60,
                command = noRestart)
            yesButton.pack(side="right", padx = 20, pady = 20)
            noButton.pack(side="left", padx = 20, pady = 20)
            restartWindow.grab_set() 

        x = 10.5
        for color in colorsArray:
            button = BUTTON(master = self.customiseFrame,
                text = "",
                width = 18,
                height = 18,
                corner_radius = 9,
                fg_color = color[0],
                hover_color = color[1],
                command = lambda color = color: changeTheme(color))
            button.place(x = x, rely = 0.75)
            x += (10.5 + 18)

    # Option 1
    def dashboard(self):

        def establishShortcut():
            self.shortcut = True
            self.play()

        try:
            self.typeWindow.destroy()
        except:
            pass
        self.dashboardFrame = ctk.CTkFrame(self,
            width = self.width,
            height = self.height,
            fg_color = "#2e2e2e")
        self.dashboardFrame.place(x = 250, y = 0)
        self.typeWindow = self.dashboardFrame
        self.disabledButton = "0"
        if self.menuContracted == False:
            self.expand()
        else:
            self.contract()
        lastFrame = FRAME(master = self.dashboardFrame, 
            width = 450, 
            height = 450)
        lastFrame.place(x = 100, y = 200)
        percentageFrame = FRAME(master = self.dashboardFrame, 
            width = 450, 
            height = 450)
        percentageFrame.place(x = 600, y = 200)
        welcomeLabel = ctk.CTkLabel(master = self.dashboardFrame, 
            text = "Hi, " + WELCOMEUSER,
            font = ("Century Gothic", 50))
        welcomeLabel.place(x = 100, y = 50)

        lastLabel = LABEL(master = lastFrame,
            text = "Play your first level!",
            font = ("BEBAS", 50),
            wraplength = 400,
            justify = "left")
        lastLabel.place(x = 25, y = 50)
        playButton = BUTTON(master = lastFrame,
            text = "PLAY",
            command = establishShortcut)
        playButton.place(x = 225, y = 350, anchor = ctk.CENTER)

        self.shortcut = False
        config = open("userconfig.txt", "r")
        lines = config.readlines()
        lastLevel = lines[4]
        if lastLevel != "None":   
            self.level = lastLevel
            lastLabel.configure(text = "Continue playing: " + lastLevel)
        else:
            playButton.configure(command = self.play)

        statsLabel = LABEL(master = percentageFrame,
            text = "Not applicable",
            font = ("Bebas", 30),
            wraplength = 400,
            justify = "center")
        statsLabel.place(x = 225, y = 350, anchor = ctk.CENTER)
        correctPercentage = "N/A"
        if TYPEACCOUNT == "Student":
            conn = connect()
            cursor = conn.cursor()
            query = "SELECT questionNum, rightNum FROM tblStudent WHERE username = %s"
            cursor.execute(query, (WELCOMEUSER,))
            userStats = cursor.fetchone()
            try:
                correctPercentage = f"{round(int(userStats[1]) * 100 / int(userStats[0]))}"
            except:
                pass
            if correctPercentage != "N/A":
                if int(correctPercentage) == 100:
                    statsLabel.configure(text = "of  the  questions  you  have  solved  were  correct !  That's  impossible !")
                elif int(correctPercentage) <= 99 and int(correctPercentage) > 75: 
                    statsLabel.configure(text = "of  the  questions  you  have  solved  were  correct !  Very  well  done !")
                elif int(correctPercentage) <= 75 and int(correctPercentage) > 66:
                    statsLabel.configure(text = "of  the  questions  you  have  solved  were  correct !  You're  almost  there !")
                elif int(correctPercentage) <= 66 and int(correctPercentage) > 33:
                    statsLabel.configure(text = "of  the  questions  you  have  solved  were  correct !  Keep  going !")
                elif int(correctPercentage) <= 33 and int(correctPercentage) > 0:
                    statsLabel.configure(text = "of  the  questions  you  have  solved  were  correct !  You  need  to  work  harder")
                else:
                    statsLabel.configure(text = "Start  solving  questions!")
                correctPercentage = correctPercentage + "%"
            cursor.close()
            conn.close()
        percentageLabel = LABEL(master = percentageFrame,
            text = correctPercentage,
            font = ("Bebas", 175))
        percentageLabel.place(x = 225, y = 150, anchor = ctk.CENTER)





    # Option 2
    def play(self):
        def quitLevel():
            def quitLevelYes():
                if self.count != 10:
                    if TYPEACCOUNT == "Student":
                        conn = connect()
                        cursor = conn.cursor()
                        query = "UPDATE tblStudent set questionNum = questionNum + %s" 
                        cursor.execute(query, (self.questionNum,))
                        query = "UPDATE tblStudent set rightNum = rightNum + %s" 
                        cursor.execute(query, (self.rightNum,))
                        conn.commit()
                        cursor.close()
                        conn.close()
                    quitLevel.destroy()
                self.play()

            def quitLevelNo():
                quitLevel.destroy()

            if self.count != 10:
                quitLevel = ctk.CTkToplevel(app)
                quitLevel.geometry("300x300") 
                quitLevel.geometry(f"{(self.width - 300)//2}+{(self.height - 300)//2}")                
                quitLevel.title("Warning")
                quitLevel.resizable(False, False)
                label = LABEL(quitLevel, 
                    text ="Are you sure you want to quit this level? All progress made in this level will be lost", 
                    font = ("Century Gothic Bold", 18),
                    wraplength = 250)
                label.pack(padx = 10, pady = 50)
                yesButton = BUTTON(quitLevel, 
                    text = "Yes",
                    width = 100,
                    height = 60,
                    command = quitLevelYes)
                noButton = BUTTON(quitLevel, 
                    text = "No",
                    width = 100,
                    height = 60,
                    command = quitLevelNo)
                yesButton.pack(side="right", padx = 20, pady = 20)
                noButton.pack(side="left", padx = 20, pady = 20)
                quitLevel.grab_set()
            else:
                quitLevelYes()
        
        def checkAnswer():
            myAnswer = ""
            wrongSelection = None
            if self.questionType == "e":
                myAnswer = self.questionEntry.get().replace(" ", "")
            elif self.questionType == "b":
                myAnswer = self.answerBoolean
            elif self.questionType == "s" and len(self.answersSelected) != 0:
                wrongSelection = False
                answersArray = self.answer.split("~")
                if len(answersArray) == len(self.answersSelected):
                    for answer in self.answersSelected:
                        if answer not in answersArray:
                            wrongSelection = True
                else:
                    wrongSelection = True
                if wrongSelection == False:
                    myAnswer = self.answer
                elif wrongSelection == True:
                    myAnswer = "Wrong answer"

            try:
                self.incorrectLabel.destroy()
            except:
                pass
            try:
                self.correctLabel.destroy()
            except:
                pass
            try:
                self.answerFrame.destroy()
            except:
                pass
            
            if myAnswer != "" and self.levelProgress[self.count] == "*":
                    if myAnswer == self.answer:
                        if self.incorrect == True:
                            self.levelProgress[self.count] = "ic"
                        else:
                            self.levelProgress[self.count] = "c"
                        if TYPEACCOUNT == "Student":
                            self.rightNum += 1
                            self.questionNum += 1
                    elif myAnswer != self.answer:
                        if self.incorrect == True or self.questionType == "b" or wrongSelection == True:
                            self.levelProgress[self.count] = "i"
                            if TYPEACCOUNT == "Student":
                                self.questionNum += 1
                        elif self.incorrect == False:
                            self.incorrectLabel = ERRORLABEL(master = self.playFrame3,
                                text = "Incorrect answer. One more try",
                                font = ("Century Gothic", 18))
                            self.incorrectLabel.place(x = 110, rely = 0.46)
                            self.incorrect = True 

            if self.levelProgress[self.count] != "*":
                self.whiteboard.destroy()
                self.whiteboardLabel.destroy()
                if "~" in self.answer:
                    self.answer = self.answer.replace("~", ",")
                self.nextButton = BUTTON(master = self.playFrame3,
                    text = "NEXT",
                    font = ("Bebas", 18),
                    width = 100, 
                    height = 60,
                    border_width = 2,
                    border_color = color2,
                    command = questionAfter)
                self.nextButton.place(relx = 0.7, rely = 0.8)
                self.answerFrame = FRAME(master = self.playFrame3,
                    width = (self.width - 250)/3 - 100,
                    height = self.height/2,
                    border_color = "Red")                                  
                self.answerFrame.place(x = 2*(self.width - 250)/3 + 50, y = 200)
                answerLabel = LABEL(master = self.answerFrame,
                    text = f"""Answer:
{self.answer}""",
                    font = ("Century Gothic", 20))
                answerLabel.place(x = 10, y = 10)
                if self.count != 0:
                    self.backButton = BUTTON(master = self.playFrame3,
                        text = "BACK",
                        font = ("Bebas", 18),
                        width = 100, 
                        height = 60,
                        border_width = 2,
                        border_color = color2,
                        command = questionBefore)
                    self.backButton.place(x = 110, rely = 0.8)
            if self.levelProgress[self.count] == "i":
                self.incorrectLabel = ERRORLABEL(master = self.playFrame3,
                    text = "Incorrect answer. No more tries",
                    font = ("Century Gothic", 22))
                self.incorrectLabel.place(x = 2*(self.width - 250)/3 + 50, y = 150)
                self.submitButton.configure(state = "disabled")
            elif self.levelProgress[self.count] == "c" or self.levelProgress[self.count] == "ic":
                self.answerFrame.configure(border_color = "Green")
                self.correctLabel = LABEL(master = self.playFrame3,
                    text = "Correct! Click next",
                    font = ("Century Gothic", 22),
                    text_color = "Green")
                self.correctLabel.place(x = 2*(self.width - 250)/3 + 50, y = 150)
                self.submitButton.configure(state = "disabled")

        def insertChar(char):
            currentText = self.questionEntry.get()
            char = char.replace("𝑥", "")
            self.questionEntry.insert(len(currentText), char) 

        def questionBefore():
            self.count -= 1
            levelContents()
            checkAnswer()

        def questionAfter():
            self.count += 1
            levelContents()
            if self.count < 10:
                checkAnswer()
        
        def checkAnswerBoolean(value):
            self.answerBoolean = value

        def addOption(option):
            found = False
            for item in self.answersSelected:
                if item == option:
                    self.answersSelected.remove(item)
                    found = True
            if found == False:
                self.answersSelected.append(option)

        def levelContents():
            if self.count < 10: 
                for item in self.playFrame3.winfo_children():
                    if item != self.questionLabel and item != self.infoLabel and item != self.leaveButton:
                        item.destroy()
                question = self.questions[self.count][0]
                self.answer = self.questions[self.count][1]
                difficulty = self.questions[self.count][2]
                self.questionType = self.questions[self.count][3]
                self.infoLabel.configure(text = f"{self.level} | Question difficulty: {difficulty} | {self.count + 1}/10")

                self.incorrect = None
                self.answerBoolean = ""
                self.whiteboard = ctk.CTkTextbox(master = self.playFrame3,
                    width = (self.width - 250)/3 - 100,
                    height = self.height/2,
                    fg_color = "#cccccc",
                    border_width = 3,
                    border_color = color2,
                    font = ("Consolas", 20),
                    text_color = "Black")
                self.whiteboard.place(x = 2*(self.width - 250)/3 + 50, y = 200)
                self.whiteboardLabel = LABEL(master = self.playFrame3,
                    text = "Whiteboard")
                self.whiteboardLabel.place(x = 2*(self.width - 250)/3 + 50, y = 140)
                self.submitButton = BUTTON(master = self.playFrame3,
                    text = "SUBMIT",
                    font = ("Bebas", 18),
                    width = 100, 
                    height = 60,
                    border_width = 2,
                    border_color = color2,
                    command = checkAnswer)
                if self.questionType == "e":
                    self.questionLabel.configure(text = question)
                    self.incorrect = False
                    self.submitButton.place(x = 520, rely = 0.39)
                    self.questionEntry = ENTRY(master = self.playFrame3,
                        width = 400,
                        height = 50)
                    self.questionEntry.place(x = 110, rely = 0.4)
                    charsFrame = FRAME(master = self.playFrame3,
                        width = 465,
                        height = 200)
                    charsFrame.place(x = 85, rely = 0.5) 
                    charsLabel = LABEL(master = charsFrame,
                        font = ("Bebas", 22),
                        text = "Special characters:")
                    charsLabel.place(x = 10, y = 10 )
                    chars = "√", "⁻", "𝑥⁰", "𝑥¹", "𝑥²", "𝑥³", "𝑥⁴", "𝑥⁵", "𝑥⁶", "𝑥⁷", "𝑥⁸", "𝑥⁹", "π"
                    xindex = -1
                    yindex = 0
                    for char in chars:
                        button = BUTTON(master = charsFrame,
                            text = char,
                            font = ("Century Gothic", 20),
                            width = 40,
                            height = 40,
                            command = lambda char = char: insertChar(char))
                        if xindex == 9:
                            xindex = 0
                            yindex += 1
                        else:
                            xindex += 1
                        button.place(x = 10 + 45*xindex, y = 60 + 45*yindex)
                elif self.questionType == "b":
                    self.questionLabel.configure(text = question)
                    self.submitButton.place(x = 600, rely = 0.5)
                    options = []
                    if self.answer == "Yes" or self.answer == "No":
                        options = ["Yes", "No"]
                    elif self.answer == "True" or self.answer == "False":
                        options = ["True", "False"]
                    elif self.answer == "Rational" or self.answer == "Irrational":
                        options = ["Rational", "Irrational"]
                    self.booleanButton = ctk.CTkSegmentedButton(master = self.playFrame3,
                        values = [options[0], options[1]],
                        width = (self.width - 250)/2 - 100,
                        height = 200,
                        unselected_hover_color = color,
                        selected_color = color2,
                        selected_hover_color = color2,
                        font = ("Hacked", 40),
                        command = checkAnswerBoolean)
                    self.booleanButton.place(x = 150, y = 300)
                        
                elif self.questionType == "s":
                    self.answersSelected = []
                    self.submitButton.place(x = 600, rely = 0.5)
                    splitQuestion = question.split(":")
                    question = splitQuestion[0]
                    options = splitQuestion[1]
                    options = options.split("~")
                    self.questionLabel.configure(text = question)
                    index = 0
                    for option in options:
                        optionCheckbox = ctk.CTkCheckBox(master = self.playFrame3,
                            text = option,
                            checkbox_width = 30,
                            checkbox_height = 30,
                            corner_radius = 8,
                            fg_color = color2,
                            border_width = 3,
                            border_color = color2,
                            hover_color = color,
                            font = ("Century Gothic", 18),
                            command = lambda option = option: addOption(option))
                        optionCheckbox.place(x = 150, y = 300 + 50*index)
                        index += 1
            elif self.count == 10:
                score = 0
                for item in self.levelProgress:
                    if item == "c":
                        score += 1
                    elif item == "ic":
                        score += 0.5
                for widget in self.playFrame3.winfo_children():
                    if widget != self.nextButton and widget != self.leaveButton and widget != self.infoLabel:
                        widget.destroy()
                stars = 0
                if score > 4 and score < 7:
                    stars = 1
                elif score > 6 and score < 10:
                    stars = 2
                elif score == 10:
                    stars = 3
                imageLabel = ctk.CTkLabel(master = self.playFrame3,
                    text = "",
                    image = ctk.CTkImage(dark_image = Image.open(f"{stars}stars.png"), size = (350, 150)))
                imageLabel.place(relx = 0.5, y = 150)
                self.infoLabel.configure(font = ("Bebas", 42),
                        wraplength = (self.width - 450)/2)
                self.level.replace(" ", "  ")
                levelIndex = self.subtopics.index(self.level)
                nextLevel = self.subtopics[levelIndex + 1]
                if TYPEACCOUNT ==  "Student":
                    conn = connect()
                    cursor = conn.cursor()
                    query = "UPDATE tblStudent SET questionNum = questionNum + %s"
                    cursor.execute(query, (self.questionNum,))
                    query = "UPDATE tblStudent SET rightNum = rightNum + %s"
                    cursor.execute(query, (self.rightNum,))
                    if stars == 0:
                        self.infoLabel.configure(text = f"""{self.level}
    Level  completed
    Score:  {score}/10           

    You  have  not  achieved  any  stars  in  this  level!

    Click  retry  to  play  this  level  again  and  unlock  the  next  one""")
                        self.nextButton.configure(text = "RETRY", command = lambda level = self.level: playLevel(level))
                    else:
                        self.infoLabel.configure(text = f"""{self.level}
    Level  completed
    Score:  {score}/10           

    You  have  just  unlocked  "{nextLevel}"!

    Click  next  to  play!""")
                        self.nextButton.configure(command = lambda level = nextLevel: playLevel(level))
                        newProgress = ""
                        found = False
                        i = 0
                        while found == False:
                            if self.progress[i] == "0":
                                newProgress = newProgress + str(stars) + "0"
                                found = True
                            else:
                                newProgress = newProgress + self.progress[i]
                                i += 1
                        while len(newProgress) != len(self.progress):
                            newProgress = newProgress + "L"
                        self.progress = newProgress
                        query = "UPDATE tblStudentProgress SET progress = %s WHERE username = %s AND topic = %s"
                        cursor.execute(query, (self.progress, WELCOMEUSER, self.topic))

                        config = open("userconfig.txt", "r") 
                        lines = config.readlines()
                        lines[4] = nextLevel
                        config = open("userconfig.txt", "w")
                        config.writelines(lines)  
                    conn.commit()
                    cursor.close()
                    conn.close()
                elif TYPEACCOUNT == "Teacher":
                    self.infoLabel.configure(text = f"""{self.level}
Level  completed
Score:  {score}/10           

Click  next  to  play the next level!""")
                    self.nextButton.configure(command = lambda level = nextLevel: playLevel(level))  
                    config = open("userconfig.txt", "r") 
                    lines = config.readlines()
                    lines[4] = nextLevel
                    config = open("userconfig.txt", "w")
                    config.writelines(lines)                    
                    
        def playLevel(level):
            self.shortcut = False
            self.typeWindow.destroy()
            self.playFrame3 = ctk.CTkFrame(self,
                width = self.width,
                height = self.height, 
                fg_color = "#2e2e2e")
            self.playFrame3.place(x = 250, y = 0)
            self.typeWindow = self.playFrame3
            self.disabledButton = "1"
            if self.menuContracted == False:
                self.expand()
            else:
                self.contract()   

            config = open("userconfig.txt", "r") 
            lines = config.readlines()
            lines[4] = level
            config = open("userconfig.txt", "w")
            config.writelines(lines)  

            self.level = level
            self.levelProgress = ["*","*","*","*","*","*","*","*","*","*"]
            if TYPEACCOUNT == "Student":
                self.questionNum = 0
                self.rightNum = 0
            self.leaveButton = BUTTON(master = self.playFrame3,
                text = "LEAVE",
                font = ("Bebas", 18) ,
                width = 80, 
                height = 50,
                border_width = 2,
                border_color = color2, 
                command = quitLevel)
            self.leaveButton.place(x = 10, y = 145)

            conn = connect()
            cursor = conn.cursor()
            query = f"SELECT question, answer, difficulty, questiontype FROM tblQuestion WHERE subtopic = %s"
            cursor.execute(query, (level,))
            data = cursor.fetchall()
            self.questions = []
            qs = [[],[],[]]
            challengeQs = []
            for i in range(0, len(data) - 1):
                if data[i][2] == 1:
                    qs[0].append(data[i])
                elif  data[i][2] == 2:
                    qs[1].append(data[i])
                elif  data[i][2] == 3:
                    qs[2].append(data[i])
                else:
                    challengeQs.append(data[i])
            for i in range(0, 3):
                for j in range(3):
                    selectedIndex = random.randint(0, len(qs[i]) - 1)
                    question = qs[i].pop(selectedIndex)
                    self.questions.append(question)
            selectedIndex = random.randint(0, len(challengeQs) - 1)
            self.questions.append(challengeQs[selectedIndex])
            cursor.close()
            conn.close()

            self.count = 0
            self.questionLabel = LABEL(master = self.playFrame3,
                text = "Loading...",
                font = ("Century Gothic", 36),
                wraplength = 2*(self.width - 250)/3 - 100)
            self.questionLabel.place(x = 100, y = 210)
            self.infoLabel = LABEL(master = self.playFrame3,
                text = "Loading...",
                font = ("Century Gothic", 26),
                wraplength = self.width/2 - 200)
            self.infoLabel.place(x = 100, y = 140)

            levelContents()

        def displayLevelInfo(level, index):
            try:
                self.viewLevelFrame.destroy()
            except:
                pass
            if self.currentLevel != level:
                self.currentLevel = level
                self.viewLevelFrame = FRAME(master = self.playFrame2, 
                    width = self.width/3, 
                    height = self.height - 600)
                levelLabel = LABEL(master = self.viewLevelFrame,
                    text = level, 
                    wraplength = self.width * 2/3 - 700,
                    justify = "left")
                levelInfo = LABEL(master = self.viewLevelFrame, 
                    text = "Click below to start level!",
                    font = ("Century Gothic", 26),
                    wraplength = self.width * 2/3 - 700)
                startButton = BUTTON(master = self.viewLevelFrame,
                    text = "Start", 
                    command = lambda level = level: playLevel(level))
                if self.height <= 900:
                    self.viewLevelFrame.configure(height = self.height - 300)
                    levelLabel.configure(wraplength = self.width *2/3 - 600, 
                        font = ("Century Gothic", 26))
                    levelInfo.configure(font = ("Century Gothic", 18), 
                        wraplength = self.width * 2/3 - 600)
                self.viewLevelFrame.place(x = self.width * 2/3 - 300, y = 200)
                levelLabel.place(x = 50, y = 35)
                levelInfo.place(x = 50, y = 175)
                if self.height <= 900:
                    startButton.place(x = self.width/3 - 200, y = self.height - 400)
                else:
                    startButton.place(x = self.width/3 - 200, y = self.height - 700)
            elif self.currentLevel == level:
                self.currentLevel = ""
            if TYPEACCOUNT == "Student" and self.currentLevel != "":
                if self.progress[index] == "L":
                    levelInfo.configure(text = "This level is currently blocked. Play more to unlock")
                    startButton.configure(state = "disabled")
                else:
                    if self.progress[index] == "0":
                        imageLabel = ctk.CTkLabel(master = self.viewLevelFrame,
                            text = "",
                            image = ctk.CTkImage(dark_image = Image.open("0stars.png"), size = (140, 60)))
                        if self.height <= 900:
                            imageLabel.place(x = 50, y = self.height - 400)
                        else:
                            imageLabel.place(x = 50, y = self.height - 700)
                

        def displayLevels(topic):
            self.currentLevel = ""
            self.topic = topic
            self.typeWindow.destroy()
            self.playFrame2 = ctk.CTkFrame(self,
                width = self.width,
                height = self.height, 
                fg_color = "#2e2e2e")
            self.playFrame2.place(x = 250, y = 0)
            self.typeWindow = self.playFrame2
            self.disabledButton = "1"
            if self.menuContracted == False:
                self.expand()
            else:
                self.contract()
            self.showLevelsFrame = FRAME(master = self.playFrame2,
                width = self.height - 300, 
                height = self.height - 300)
            self.showLevelsFrame.place(x = 100, y = 200)
            backButton = BUTTON(master = self.playFrame2,
                text = "BACK",
                font = ("Bebas", 18) ,
                width = 80, 
                height = 50, 
                command = self.play)
            backButton.place(x = 10, y = 145)
            showLevelsFrame2 = ctk.CTkScrollableFrame(master = self.showLevelsFrame,
                width = self.height - 330, 
                height = self.height - 320)
            showLevelsFrame2.place(x = 5, y = 5)
            self.playLabel = ctk.CTkLabel(master = self.playFrame2, 
                text = topic,
                justify = "left",
                font = ("Century Gothic", 50))
            self.playLabel.place(x = 100, y = 50)
            conn = connect()
            cursor = conn.cursor()
            query = "SELECT subtopic FROM tblSubtopics WHERE topic = %s ORDER BY indexLevel ASC"
            cursor.execute(query, (topic,))
            subtopics = cursor.fetchall()
            subtopics = str(subtopics).replace("('", "").replace("',)", "").replace("[", "").replace("]", "")
            self.subtopics = subtopics.split(", ")
            if TYPEACCOUNT == "Student":
                query = "SELECT progress FROM tblStudentProgress WHERE username = %s and topic = %s"
                cursor.execute(query,(WELCOMEUSER, topic))
                self.progress = cursor.fetchone()
                self.progress = str(self.progress).replace("('", "").replace("',)", "")
                if self.progress == "None":
                    self.progress = "0"
                    count = 1
                    for i in range(1, len(self.subtopics)):
                        self.progress = self.progress + "L"
                        count += 1
                    query = f"INSERT INTO tblStudentProgress (username, topic, progress) VALUES (%s, %s, %s)"
                    cursor.execute(query, (WELCOMEUSER, topic, self.progress))
                    conn.commit()
                cursor.close()
                conn.close()
            index = 0
            for level in self.subtopics:
                button = BUTTON(master = showLevelsFrame2,
                    height = 50,
                    width = self.width/3,
                    text = str(index +1) + ".   " + level.replace(" ", "   "),
                    anchor = "w",
                    font = ("Bebas", 16),
                    command = lambda level = level, index = index: displayLevelInfo(level, index))
                if TYPEACCOUNT == "Student":
                    if self.progress[index] == "L":
                        button.configure(image = ctk.CTkImage(dark_image = Image.open("locked.png"), 
                            size = (50, 20)), compound = "right")
                    else:
                        button.configure(image = ctk.CTkImage(dark_image = Image.open(f"{self.progress[index]}stars.png"), 
                            size = (70, 30)),
                            compound = "right")
                button.pack(pady = 5)
                index += 1

        if self.shortcut:
            level = self.level
            conn = connect()
            cursor = conn.cursor()
            query = "SELECT topic FROM tblSubtopics WHERE subtopic = %s"
            cursor.execute(query, (level,))
            topic = str(cursor.fetchone()).replace("('", "").replace("',)", "")
            cursor.close()
            conn.close()
            displayLevels(topic)
            playLevel(level)
        else:
            self.typeWindow.destroy()
            self.playFrame = ctk.CTkFrame(self,
                width = self.width,
                height = self.height, 
                fg_color = "#2e2e2e")
            self.playFrame.place(x = 250, y = 0)
            self.typeWindow = self.playFrame 
            self.disabledButton = "1"
            if self.menuContracted == False:
                self.expand()
            else:
                self.contract()
            self.levelsFrame = ctk.CTkScrollableFrame(master = self.playFrame,
                width = self.EXPANDWIDTH - 200,
                height = self.height - 200, 
                fg_color = "#2e2e2e")
            self.levelsFrame.place(x = 80, y = 150)
            self.playLabel = ctk.CTkLabel(master = self.playFrame, 
                text = "Play levels",
                font = ("Century Gothic", 50))
            self.playLabel.place(x = 100, y = 50)

            maxcolumns = (self.EXPANDWIDTH - 200) // (270)
            row = 0
            column = 0 
            for item in self.topicNames:
                image = ctk.CTkImage(dark_image = Image.open(item[1]), size = (250, 250))
                imageLabel = ctk.CTkLabel(master = self.levelsFrame, image = image, text = "")
                imageLabel.grid(row = row, column = column, padx = 20, pady = 5)
                button = BUTTON(master = self.levelsFrame, 
                    text = item[0],
                    font = ("HACKED", 20),
                    width = 250,
                    height = 50, 
                    hover_color = color,
                    command = lambda topic = item[0]: displayLevels(topic))
                button.grid(row = row + 1, column = column, padx = 20, pady=(5, 50)) 
                column += 1
                if column == maxcolumns:
                    column = 0
                    row += 2
        

    # Option 3
    def classroom(self):

        def checkClassID(classID):
            try:
                self.errorLabel.destroy()
            except:
                pass
            allowedChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            valid = True
            if len(classID) == 8:
                for char in classID:
                    if char not in allowedChars:
                        valid = False
            else:
                valid = False

            if valid == False:
                self.errorLabel = ERRORLABEL(master = self.viewclassFrame, 
                    text = "Please enter a valid class ID")
                self.errorLabel.place(x = 25, y = 120)
            else:
                return True

        def addStudent():
            classID = self.classnameEntry.get()
            valid = checkClassID(classID)
            if valid:
                conn = connect()
                cursor = conn.cursor()
                query = "SELECT className FROM tblClass WHERE classID = %s"
                cursor.execute(query, (classID,))
                classname = str(cursor.fetchone())
                classname = classname.replace('("', '').replace('",)', '').replace("('", "").replace("',)", "")
                if classname == "None":
                    self.errorLabel = ERRORLABEL(master = self.viewclassFrame, 
                        text = "Class not found. Try again")
                    self.errorLabel.place(x = 25, y = 120)
                elif classname != "None":
                    query = "INSERT INTO tblStudentClass (username, classID) VALUES (%s, %s)"
                    cursor.execute(query, (WELCOMEUSER, classID))
                    conn.commit()
                    showClass(classID, classname)
                    displayClasses()
                cursor.close()
                conn.close()

        def joinClass():
            try:
                self.errorLabel.destroy()
            except:
                pass
            try:
                self.viewclassFrame.destroy()
            except:
                pass
            try:
                self.classnameLabel.destroy()
            except:
                pass
            self.currentCode = ""
            if self.numClasses == 5:
                self.errorLabel = ERRORLABEL(master = self.classroomFrame, text = "You have reached the maximum number of classes.")
                self.errorLabel.place(x = 100, y = 255)
            else:
                self.classButton.configure(state = "disabled")
                self.viewclassFrame = FRAME(master = self.classroomFrame, 
                    width = self.width/3, 
                    height = self.height - 500)
                self.viewclassFrame.place(x = 100, y = 400)
                self.myclassLabel = LABEL(master = self.classroomFrame,
                    text = "Join new class")
                self.myclassLabel.place(x = 100, y = 345)
                classnameCodeLabel = ctk.CTkLabel(master = self.viewclassFrame, 
                    text = "Enter the 8 digit code provided by your teacher to join their class",
                    font = ("Century Gothic", 20),
                    wraplength = self.width/3 - 100,
                    justify = "left")
                classnameCodeLabel.place(x = 25,  y = 25)
                self.classnameEntry = ENTRY(master = self.viewclassFrame, 
                    placeholder_text = "Enter code...",
                    border_color = color2,
                    width = self.width/3 - 50)
                self.classnameEntry.place(x = 25, y = 75)
                classnameButton = BUTTON(master = self.viewclassFrame, 
                    width = self.width/12, 
                    text = "Enter",
                    command = addStudent)
                classnameButton.place(relx = 0.375, y = 150)
        
        def showStudent(username):
            conn = connect()
            cursor = conn.cursor()
            query = "SELECT questionNum, rightNum, email FROM tblStudent WHERE username = %s"
            cursor.execute(query, (username,))
            userStats = cursor.fetchone()
            query = "SELECT topic, progress FROM tblStudentProgress WHERE username = %s"
            cursor.execute(query, (username,))
            userProgress = cursor.fetchall()
            print(userProgress)
            for item in userProgress:
                print(item)
            cursor.close()
            conn.close()
            showStudentFrame = ctk.CTkScrollableFrame(master = self.viewclassFrame,
                width = self.width/3 - 28, 
                height = self.height - 526)
            showStudentFrame.place(x = 3, y = 3)
            studentNameLabel = LABEL(master = showStudentFrame, 
                text = username)
            studentNameLabel.pack(padx = 20, pady = 10, anchor = "w")
            try:
                correctPercentage = f"{round(int(userStats[1]) * 100 / int(userStats[0]))}%"
            except:
                correctPercentage = "N/A"
            arrayProgress = []
            for topicName in self.topicNames:
                topic = topicName[0]
                for item in userProgress:
                    if topic in item:
                        levelCount = 0
                        for i in item[1]:
                            if i != "L":
                                levelCount += 1
                    if levelCount == 1 or topic not in item:
                        arrayProgress.append("Not started")
                    else:
                        arrayProgress.append(str(levelCount))
            
            self.infoLabel = LABEL(master = showStudentFrame,
                text = 
f"""    Email: {userStats[2]}

    Level in "Numbers" topic:  {arrayProgress[0]}
    Level in "Algebra" topic:  {arrayProgress[1]}
    Level in "Graphs" topic:  {arrayProgress[2]}
    Level in "Ratio & proportion" topic:  {arrayProgress[3]}
    Level in "Geometry & trigonometry" topic:  {arrayProgress[4]}
    Level in "Stats and probability" topic:  {arrayProgress[5]}
""",
                font = ("Century Gothic", 16),
                justify = "left")
            
            if TYPEACCOUNT == "Teacher":
                self.infoLabel.configure(text = 
f"""    Email: {userStats[2]}

    Number of questions solved:  {userStats[0]}
    Number of questions right:  {userStats[1]}
    Percentage of correct answers:  {correctPercentage}
    Level in "Numbers" topic:  {arrayProgress[0]}
    Level in "Algebra" topic:  {arrayProgress[1]}
    Level in "Graphs" topic:  {arrayProgress[2]}
    Level in "Ratio & proportion" topic:  {arrayProgress[3]}
    Level in "Geometry & trigonometry" topic:  {arrayProgress[4]}
    Level in "Stats and probability" topic:  {arrayProgress[5]}
""")
            self.infoLabel.pack(padx = 10, pady = 10, anchor = "w")

        def addClass(classname):
            duplicatedID = True
            conn = connect()
            cursor = conn.cursor()
            while duplicatedID == True:
                try:
                    classID = f"{random.randint(0, 99999999):08d}"
                    query = "INSERT INTO tblClass (classID, classname, username) VALUES (%s, %s, %s)"   
                    cursor.execute(query, (classID, classname, WELCOMEUSER,))
                    conn.commit()
                    duplicatedID = False
                except:
                    pass
            if duplicatedID == False:
                self.currentCode = ""
                self.viewclassFrame.destroy()
                self.myclassLabel.destroy()
                showClass(classID, classname)
                displayClasses()
            self.classButton.configure(state = "enabled")
            cursor.close()
            conn.close()

        def assignClassname():
            classname = self.classnameEntry.get()
            try:
                self.errorLabel.destroy()
            except:
                pass
            if len(classname.replace(" ", "")) == 0 or len(classname) > 20:
                self.errorLabel = ERRORLABEL(master = self.viewclassFrame, text = "Please enter a valid class name")
                self.errorLabel.place(x = 25, y = 120)
            else:
                addClass(classname)

        def createClass():
            try:
                self.viewclassFrame.destroy()
            except:
                pass
            try:
                self.classnameLabel.destroy()
            except:
                pass
            try:
                self.errorLabel.destroy()
            except:
                pass
            self.currentCode = ""
            if self.numClasses == 10:
                self.errorLabel = ERRORLABEL(master = self.classroomFrame, text = "You have reached the maximum number of classes.")
                self.errorLabel.place(x = 100, y = 255)
            else:
                self.classButton.configure(state = "disabled")
                self.viewclassFrame = FRAME(master = self.classroomFrame, 
                    width = self.width/3, 
                    height = self.height - 450)
                self.viewclassFrame.place(x = 100, y = 400)
                self.myclassLabel = LABEL(master = self.classroomFrame,
                    text = "My new class")
                self.myclassLabel.place(x = 100, y = 345)
                assignNameLabel = ctk.CTkLabel(master = self.viewclassFrame, 
                    text = "Assign a unique name for your class",
                    font = ("Century Gothic", 20))
                assignNameLabel.place(x = 25,  y = 25)
                self.classnameEntry = ENTRY(master = self.viewclassFrame, 
                    placeholder_text = "Enter class name (max 20 characters)",
                    border_color = color2,
                    width = self.width/3 - 50)
                self.classnameEntry.place(x = 25, y = 75)
                classnameButton = BUTTON(master = self.viewclassFrame, 
                    width = self.width/12, 
                    text = "Enter", 
                    command = assignClassname)
                classnameButton.place(relx = 0.375, y = 150)

        def showClass(classID, classname):
            try:
                self.myclassLabel.destroy()
            except:
                pass      
            try:
                self.classnameLabel.destroy()
            except:
                pass
            try:
                self.viewclassFrame.destroy()
            except:
                pass
            try:
                self.errorLabel.destroy()
            except:
                pass
            if self.currentCode != classID:
                self.classButton.configure(state = "enabled")
                self.viewclassFrame = FRAME(master = self.classroomFrame, 
                    width = self.width/3, 
                    height = self.height - 400)
                self.viewclassFrame.place(x = 100, y = 350)
                self.classnameLabel = LABEL(master = self.classroomFrame,
                    text = classname + "            ")
                self.classnameLabel.place(x = 100, y = 295)
                self.viewclass2Frame = ctk.CTkScrollableFrame(master = self.viewclassFrame,
                    width = self.width/3 - 70,
                    height = self.height - 575)
                self.viewclass2Frame.place(x = 25, y = 50)
                if TYPEACCOUNT == "Teacher":
                    codeLabel = ctk.CTkLabel(master = self.viewclassFrame,
                        text = "Students can join with the code     " + classID,
                        font = ("Bebas", 20))
                    codeLabel.place(relx = 0.05, y = 20)
                conn = connect()
                cursor = conn.cursor()
                query  = "SELECT username FROM tblStudentClass WHERE classID = %s"
                cursor.execute(query, (classID,))
                usernames = cursor.fetchall()
                for username in usernames:
                    username = str(username).replace("('", "").replace("',)", "")
                    print(username)
                    button = BUTTON(master = self.viewclass2Frame,
                    height = 30,
                    width = self.width/3,
                    text = "        " + username,
                    anchor = "w",
                    font = ("Bebas", 16),
                    command = lambda username = username: showStudent(username))
                    button.pack(pady = 3)
                self.currentCode = classID
                cursor.close()
                conn.close()
            elif self.currentCode == classID:
                self.currentCode = ""

        def displayClasses():
            try:
                self.classes2Frame.destroy()
            except:
                pass
            
            self.classes2Frame = ctk.CTkScrollableFrame(master = classesFrame, 
                width = self.width/3 - 30, 
                height = self.height - 320,
                fg_color = "#2e2e2e")
            self.classes2Frame.place(x = 5, y = 5)
            classes = []
            classIDs = []
            conn = connect()
            cursor = conn.cursor()
            if TYPEACCOUNT == "Teacher":
                self.classButton.configure(text = "Create class", command = createClass)
                query = "SELECT className, classID FROM tblClass WHERE username = %s ORDER BY className ASC"
                cursor.execute(query, (WELCOMEUSER,))
                classesFetched = cursor.fetchall()
                for item in classesFetched:
                    classID = str(item[1]).replace("('", "").replace("',)", "").replace('("', '').replace('",)', '')
                    classname = str(item[0]).replace("('", "").replace("',)", "").replace('("', '').replace('",)', '')
                    classIDs.append(classID)
                    classes.append(classname)
                self.numClasses = len(classes)
                classLabel.configure(text = str(self.numClasses) + "/10 classes created")
            elif TYPEACCOUNT == "Student":
                self.classButton.configure(text = "Join class", command = joinClass)
                query = "SELECT classID FROM tblStudentClass WHERE username = %s"
                cursor.execute(query, (WELCOMEUSER,))
                classIDsFetched = cursor.fetchall()
                for classID in classIDsFetched:
                    classID = str(classID).replace("('", "").replace("',)", "").replace('("', '').replace('",)', '')
                    query = "SELECT classname FROM tblClass WHERE classID = %s"
                    cursor.execute(query, (classID,))
                    classname = cursor.fetchone()
                    classname = str(classname).replace("('", "").replace("',)", "").replace('("', '').replace('",)', '')
                    classes.append(classname)
                    classIDs.append(classID)
                self.numClasses = len(classes)
                classLabel.configure(text = str(5 - self.numClasses) + "/5 classes to join")
            index = 0
            for item in classes:
                button = BUTTON(master = self.classes2Frame,
                    height = 60,
                    width = self.width/3,
                    text = "        " + item,
                    anchor = "w",
                    font = ("Bebas", 17),
                    command = lambda classID = classIDs[index], classname = item: showClass(classID, classname))
                button.pack(pady = 5)
                index += 1
            cursor.close()
            conn.close()

        self.typeWindow.destroy()
        self.classroomFrame = ctk.CTkFrame(self,
            width = self.width,
            height = self.height, 
            fg_color = "#2e2e2e")
        self.classroomFrame.place(x = 250, y = 0)
        self.typeWindow = self.classroomFrame 
        self.disabledButton = "2"
        if self.menuContracted == False:
            self.expand()
        else:
            self.contract()
        classroomLabel = LABEL(master = self.classroomFrame, 
            text = "Classroom",
            font = ("Century Gothic", 50))
        classroomLabel.place(x = 100, y = 50)
        classesLabel = LABEL(master = self.classroomFrame, 
            text = "My classes")
        classesLabel.place(x = self.width * 2/3 - 325, y = 190) 
        classFrame = FRAME(master = self.classroomFrame, 
            width = self.width/3, 
            height = 100)
        classFrame.place(x = 100, y = 150)
        classesFrame = FRAME(master = self.classroomFrame, 
            width = self.width/3, 
            height = self.height - 300)
        classesFrame.place(x = self.width * 2/3 - 350, y = 250)
        self.classButton = BUTTON(master = classFrame,
            width = self.width/12,
            height = 60)
        self.classButton.place(relx = 0.7, y = 20)
        classLabel = ctk.CTkLabel(master = classFrame,
            font = ("HACKED", 30),
            text = "Loading...")
        classLabel.place(relx = 0.1, rely = 0.33)
        self.currentCode = ""
        displayClasses()
            
    def quit(self):
        def noQuit():
            quitWindow.destroy()

        quitWindow = ctk.CTkToplevel(self)
        quitWindow.geometry("300x300") 
        quitWindow.geometry(f"{(self.width - 300)//2}+{(self.height - 300)//2}")  
        quitWindow.title("Warning")
        quitWindow.resizable(False, False)
        label = LABEL(quitWindow, 
            text ="Are you sure you want to quit? Any unsaved progress will be lost", 
            font = ("Century Gothic Bold", 18),
            wraplength = 250)
        label.pack(padx = 10, pady = 50)
        yesButton = BUTTON(quitWindow, 
            text = "Yes",
            width = 100,
            height = 60,
            command = logOut)
        noButton = BUTTON(quitWindow, 
            text = "No",
            width = 100,
            height = 60,
            command = noQuit)
        yesButton.pack(side="right", padx = 20, pady = 20)
        noButton.pack(side="left", padx = 20, pady = 20)
        quitWindow.grab_set()

config = open("userconfig.txt", "r") 
lines = config.readlines()
WELCOMEUSER = lines[1].strip()
TYPEACCOUNT = lines[2].strip()
configLogged =  lines[3].strip()
if configLogged == "logged":
    app = MAIN()
    app.protocol("WM_DELETE_WINDOW", logOut)
    app.mainloop()