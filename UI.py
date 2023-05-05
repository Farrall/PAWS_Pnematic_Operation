from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import serial
import time
import webbrowser


windowWidth = 1158
windowHeight = 740

ser = serial.Serial('COM3')
ser.flushInput()

# Main menu window
root = Tk()
root.geometry("1158x740+150+50")
root.resizable(False, False)

# global variables which need to get updated while running
maxTime = StringVar(root)
currentTime = StringVar(root)
maxSeconds = IntVar(root, value=0)
elapsedS = IntVar(root, value=0)
running = BooleanVar(root, value=False)
ballSize = 60
growing = IntVar(root, 0)
breath = IntVar(root, 0)
pressure = IntVar(root, 0)
solenoids = IntVar(root, 0)
globalMode = StringVar(root, "")

# Styles to change fonts / sizes
style = Style()
style.configure("TLabel", font=("Arial", 22, "bold"))
style.configure("TButton", font=("Arial", 17, "bold"))
style.configure("Small.TLabel", font=("Arial", 17))
style.configure("SmallBold.TLabel", font=("Arial", 17, "bold"))
style.configure("ExtraSmall.TLabel", font=("Arial", 13, "bold"))

# Images for the screens
chestImg = ImageTk.PhotoImage(Image.open(
    "assets/chest.png"))
biopacIcon = ImageTk.PhotoImage(Image.open(
    "assets/plugBlack.png"))
airIcon = ImageTk.PhotoImage(Image.open(
    "assets/plugGrey.png"))
airIconOn = ImageTk.PhotoImage(Image.open(
    "assets/plugBlack.png"
))
strapIcon = ImageTk.PhotoImage(Image.open(
    "assets/blutoothBlack.png"))
cogwheelIcon = ImageTk.PhotoImage(Image.open(
    "assets/cogwheel.png"))
pauseIcon = ImageTk.PhotoImage(Image.open(
    "assets/pause.png"))
playIcon = ImageTk.PhotoImage(Image.open(
    "assets/play.png"))


def makeMenuScreen(root):
    mainMenu = Frame(root, width=windowWidth, height=windowHeight)
    mainMenu.place(x=0, y=0)

    # Main menu label
    menuText = Label(mainMenu, text="MENU")
    menuText.place(x=535, y=106)

    # Main menu buttons
    startButton = Button(mainMenu, text="START",
                         command=lambda: goToSetupScreen(root, mainMenu))
    startButton.place(x=466, y=247, width=227, height=65)

    manualButton = Button(mainMenu, text="MANUAL", command=lambda: webbrowser.open_new(r'PAWS_Manual.pdf'))
    manualButton.place(x=466, y=353, width=227, height=65)

    exitButton = Button(mainMenu, text="EXIT", command=lambda: root.destroy())
    exitButton.place(x=466, y=459, width=227, height=65)


def makeSetupScreen(root):
    setupScreen = Frame(root, width=windowWidth, height=windowHeight)
    setupScreen.place(x=0, y=0)
    canvas = Canvas(setupScreen, width=windowWidth, height=windowHeight)
    canvas.place(x=0, y=0)

    setupLabel = Label(setupScreen, text="Setup PAWS")
    setupLabel.place(x=464, y=31)

    # Device status column - RED: #D9001B | GREEN: #95F204
    deviceStatusLabel = Label(setupScreen, text="Device Status")
    deviceStatusLabel.place(x=42, y=81)

    biopacLabel = Label(setupScreen, text="Biopac", style="Small.TLabel")
    biopacLabel.place(x=42, y=159)
    biopacIconContainer = Label(setupScreen, image=biopacIcon)
    biopacIconContainer.place(x=250, y=156)
    canvas.create_oval(307, 159, 337, 189, outline="#797979",
                       fill="#95F204", width=1)

    airLabel = Label(setupScreen, text="Air Compressor", style="Small.TLabel")
    airLabel.place(x=42, y=214)
    airIconContainer = Label(setupScreen, image=airIconOn)
    airIconContainer.place(x=250, y=211)
    canvas.create_oval(307, 214, 337, 244, outline="#797979",
                       fill="#95F204", width=1)

    strapLabel = Label(setupScreen, text="Biofeedback Strap",
                       style="Small.TLabel")
    strapLabel.place(x=42, y=269)
    strapIconContainer = Label(setupScreen, image=strapIcon)
    strapIconContainer.place(x=255, y=266)
    canvas.create_oval(307, 269, 337, 299, outline="#797979",
                       fill="#95F204", width=1)

    # Operating mode area
    operatingModeLabel = Label(setupScreen, text="Operating Mode")
    operatingModeLabel.place(x=42, y=430)
    cogwheelIconContainer = Label(setupScreen, image=cogwheelIcon)
    cogwheelIconContainer.place(x=336, y=430)

    modeBox = Combobox(setupScreen, values=[
                       "Standard", "Manual"], state="readonly")
    modeBox.place(x=42, y=491)
    modeBox.current(0)

    durationBox = Combobox(setupScreen, state="readonly", values=[
        "5 minutes",
        "10 minutes",
        "15 minutes",
        "20 minutes",
        "25 minutes",
        "30 minutes"
    ])
    durationBox.place(x=42, y=540)
    durationBox.current(0)

    returnButton = Button(setupScreen, text="RETURN",
                          command=lambda: returnToMenu(root, setupScreen, canvas))
    returnButton.place(x=42, y=653, width=227, height=65)

    # Instructions column
    instructionsLabel = Label(setupScreen, text="Instructions")
    instructionsLabel.place(x=680, y=81)

    instructionsText = Label(setupScreen, style="Small.TLabel", text="""
1. Check that the Biopac power switch is ON

2. Close the drain valve under the compressor
    and turn the power switch to ON

3. Ensure biofeedback strap is charged and
    switched ON

4. Ensure participant has the biofeedback strap
    equipped around their chest



5. Choose an operating mode:
        - Standard (timed experiment)
        - Manual (manually control ball inflation -
            advanced users)

6. Select experiment duration
    """)
    instructionsText.place(x=569, y=137)

    chestContainer = Label(setupScreen, image=chestImg)
    chestContainer.place(x=927, y=404)

    nextButton = Button(setupScreen, text="NEXT",
                        command=lambda: goToActivityScreen(root, setupScreen, canvas, modeBox.get(), durationBox.current()))
    nextButton.place(x=889, y=653, width=227, height=65)


def makeActivityScreen(root, mode, duration):
    if mode == "Standard":
        globalMode.set("Standard")
        ser.write(b"1")
        print("Biofeedback mode: ", duration, " minutes")
    elif mode == "Manual":
        globalMode.set("Manual")
        ser.write(b"2")
        print("Manual mode: ", duration, " minutes")
    running.set(True)
    readBreathData()

    activityScreen = Frame(root, width=windowWidth, height=windowHeight)
    activityScreen.place(x=0, y=0)
    canvas = Canvas(activityScreen, width=windowWidth, height=windowHeight)
    canvas.place(x=0, y=0)

    statusLabel = Label(activityScreen, text="Status - Device Running")
    statusLabel.place(x=31, y=53)
    canvas.create_oval(379, 55, 409, 85, outline="#797979",
                       fill="#95F204", width=1, tags="status")

    # Ball visualisation section
    ballVisLabel = Label(activityScreen, text="Ball Visualisation")
    ballVisLabel.place(x=465, y=109)

    canvas.create_rectangle(
        389, 151, 770, 532, fill="white", outline="#797979", width=1)
    canvas.create_oval(501, 263, 660, 422, fill="blue", tags="ball")
    animateCircle(canvas)
    canvas.create_oval(432, 194, 727, 489, fill="",
                       outline="#D9001B", width=4, dash="_")

    maxM, maxS = divmod(duration*60, 60)
    maxTime.set(f'{maxM:02d}:{maxS:02d}')
    maxSeconds.set(duration*60)
    elapsedS.set(0)

    currentM, currentS = divmod(elapsedS.get(), 60)
    currentTime.set(f'{currentM:02d}:{currentS:02d}')
    

    timeBar = Progressbar(activityScreen, length=661, mode="determinate",
                          variable=elapsedS, maximum=maxSeconds.get())
    timeBar.place(x=250, y=631)

    currentTimeLabel = Label(
        activityScreen, textvariable=currentTime, style="ExtraSmall.TLabel")
    currentTimeLabel.place(x=249, y=658)
    maxTimeLabel = Label(activityScreen, textvariable=maxTime,
                         style="ExtraSmall.TLabel")
    maxTimeLabel.place(x=870, y=658)

    pauseButton = Button(activityScreen, image=pauseIcon, command=lambda: pauseFunction(
        pauseButton, canvas, statusLabel))
    pauseButton.place(x=548, y=553, width=62, height=54)

    root.after(1000, incrementTime, canvas, statusLabel, pauseButton)

    # Pressure bar section
    canvas.create_rectangle(83, 125, 83+64, 125+545,
                            fill="white", outline="#797979", width=1)
    pressureLabel = Label(
        activityScreen, text="Pressure -          (mbar)", style="SmallBold.TLabel")
    pressureLabel.place(x=21, y=690)
    pressureValueLabel = Label(
        activityScreen, textvariable=pressure, style="SmallBold.TLabel")
    pressureValueLabel.place(x=145, y=690)
    createBarLines(canvas, activityScreen)

    canvas.create_line(84, 170, 84+63, 170, fill="#D9001B", width=3, dash="_")
    highPressureLabel = Label(
        activityScreen, text="Too high", style="ExtraSmall.TLabel", foreground="#D9001B")
    highPressureLabel.place(x=151, y=160)

    # Grey bar representing pressure
    canvas.create_rectangle(83, 100, 83+64, 100+199,
                            outline="#797979", width=1, fill="#D7D7D7", tags="pressureBar")
    updatePressureBar(canvas)

    stopButton = Button(activityScreen, text="""STOP &
RETURN""",
                        command=lambda: returnToSetupScreen(root, activityScreen, canvas))
    stopButton.place(x=1005, y=650, width=130, height=65)


def goToSetupScreen(root, mainMenu):
    mainMenu.place_forget()
    makeSetupScreen(root)


def goToActivityScreen(root, setupScreen, canvas, mode, duration):
    duration = (duration+1) * 5
    setupScreen.place_forget()
    canvas.destroy()
    makeActivityScreen(root, mode, duration)


def returnToMenu(root, setupScreen, canvas):
    setupScreen.place_forget()
    canvas.destroy()
    makeMenuScreen(root)


def returnToSetupScreen(root, activityScreen, canvas):
    elapsedS.set(-1)
    running.set(False)
    ser.write(b"-1")
    activityScreen.place_forget()
    canvas.destroy()
    makeSetupScreen(root)


def createBarLines(canvas, screen):
    start = 670
    for i in range(9):
        canvas.create_line(151, start-i*68.125, 151+10,
                           start-i*68, fill="#797979", width=2)
        x = Label(screen, text=str(30*i), style="ExtraSmall.TLabel")
        x.place(x=164, y=start-11-i*68.125)


def incrementTime(canvas, statusLabel, button):
    timer = None
    if elapsedS.get() < maxSeconds.get() and running.get():
        elapsedS.set(elapsedS.get() + 1)
        currentM, currentS = divmod(elapsedS.get(), 60)
        currentTime.set(f'{currentM:02d}:{currentS:02d}')
        timer = root.after(1000, incrementTime, canvas, statusLabel, button)
    elif elapsedS.get() >= maxSeconds.get() and running.get():
        running.set(False)
        ser.write(b"1")
        canvas.itemconfigure("status", fill="#95F204")
        statusLabel.configure(text="Status - Session Done")
        button.place_forget()


def pauseFunction(button, canvas, statusLabel):
    if running.get():
        running.set(False)
        ser.write(b"1")
        button.configure(image=playIcon)
        canvas.itemconfigure("status", fill="#D9001B")
        statusLabel.configure(text="Status - Device Paused")
    else:
        running.set(True)
        ser.write(b"0")
        button.configure(image=pauseIcon)
        canvas.itemconfigure("status", fill="#95F204")
        statusLabel.configure(text="Status - Device Running")
        incrementTime()
        animateCircle(canvas)
        readBreathData()


def animateCircle(canvas):
    if running.get():
        global ballSize
        canvas.delete("ball")
        canvas.create_oval(580-ballSize, 340-ballSize, 580 +
                           ballSize, 340+ballSize, fill="blue", tags=("ball"))
        if growing.get() == 1:
            ballSize = ballSize + 0.4

        elif growing.get() == -1:
            ballSize = ballSize - 0.4

        canvas.after(50, lambda: animateCircle(canvas))


def updatePressureBar(canvas):
    diff = pressure.get() - 195
    if running.get():
        canvas.delete("pressureBar")
        canvas.create_rectangle(83, 220-diff, 83+64, 471+199,
                                outline="#797979", width=1, fill="#D7D7D7", tags="pressureBar")

        canvas.after(50, lambda: updatePressureBar(canvas))


def readBreathData():
    if running.get() and globalMode.get() == "Standard":
        try:
            serial_data = ser.readline()
            try:
                decoded_string_data = str(
                    serial_data[0:len(serial_data) - 2].decode("utf-8"))
                string_array = decoded_string_data.split(' ')
                number_array = [int(numeric_string)
                                for numeric_string in string_array]

                breath.set(number_array[0])
                pressure.set(number_array[1])
                solenoids.set(number_array[2])

                if solenoids.get() == 1:
                    growing.set(1)
                elif solenoids.get() == -1:
                    growing.set(-1)
                elif solenoids.get() == 0:
                    growing.set(0)

                print(breath.get(), pressure.get(), solenoids.get())
            except:
                print("Error")
        except:
            print("Error")
        root.after(50, lambda: readBreathData())
    elif running.get() and globalMode.get() == "Manual":
        try:
            serial_data = ser.readline()
            try:
                decoded_string_data = str(
                    serial_data[0:len(serial_data) - 2].decode("utf-8"))
                string_array = decoded_string_data.split(' ')
                number_array = [int(numeric_string)
                                for numeric_string in string_array]

                breath.set(number_array[0])
                pressure.set(number_array[1])
                solenoids.set(number_array[2])

                print(breath.get(), pressure.get(), solenoids.get())
            except:
                print("Error")
        except:
            print("Error")
        root.after(50, lambda: readBreathData())


def terminatePAWS():
    ser.write(b"-1")
    root.quit()


def upKeyPress(event):
    if globalMode.get() == "Manual" and growing.get() == 0:
        ser.write(b"5")
        print("UP")
        growing.set(1)


def upKeyRelease(event):
    if globalMode.get() == "Manual" and growing.get() == 1:
        ser.write(b"6")
        print("UP released")
        growing.set(0)


def downKeyPress(event):
    if globalMode.get() == "Manual" and growing.get() == 0:
        ser.write(b"7")
        print("DOWN")
        growing.set(-1)

def downKeyRelease(event):
    if globalMode.get() == "Manual" and growing.get() == -1:
        ser.write(b"6")
        print("DOWN released")
        growing.set(0)


root.title("PAWS")
root.protocol("WM_DELETE_WINDOW", terminatePAWS)
root.bind("<KeyPress-Up>", upKeyPress)
root.bind("<KeyRelease-Up>", upKeyRelease)
root.bind("<KeyPress-Down>", downKeyPress)
root.bind("<KeyRelease-Down>", downKeyRelease)
root.focus_set()

makeMenuScreen(root)
root.mainloop()
