from pygame import mixer
from tkinter import Tk, Toplevel, Label, Button, Frame, Entry
import time
import os
import sys
from PIL import Image, ImageTk
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class StopWatch:
    def __init__(self, bgclr, acbgclr) -> None:
        # Init Things
        os.system('cls')
        os.system('title Stop Watch')
        os.system('mode con:cols=40 lines=5')

        # Init Variables
        # 3, 123, 252 for win bluish color
        self.bg_color = self._rgb((3, 123, 252))
        self.activebgclr = self._rgb((3, 123, 252))  # Default one 87, 87, 87
        self.lap_spt = ""
        self.count, self.lp, self.spt, self.avg = 0, 0, 0, 0
        self.stp_strt, self.timer, self.tkn, self.music_started = False, False, False, False
        self.initial = None
        self.timeroff = False

        # Init Functions
        mixer.init()
        mixer.music.load(self.res_path('./chime.mp3'))
        self.defWindow()

    def defWindow(self):

        # Root Window
        self.root = Tk()

        self.rootw = 190
        self.rooth = 70

        self.root.bind('<Button-1>', self.clickwin)
        self.root.bind('<B1-Motion>', self.dragwin)

        self.root.overrideredirect(True)
        self.root.geometry(f"{self.rootw}x{self.rooth}")
        self.root.configure(background=self.bg_color)
        self.root.attributes("-topmost", True)
        self.root.attributes('-alpha', 0.9)
        self.root.eval('tk::PlaceWindow . center')

        # Widgets
        MainFrame = Frame(self.root, bg=self.bg_color)
        MainFrame.place(x=0, y=0, width=self.rootw, height=self.rooth)

        frame1 = Frame(MainFrame, bg=self.bg_color)

        self.logoname = Label(frame1, text="Stop Watch", font=(
            "Arial", 12), bg=self.bg_color, fg="white")
        self.logoname.pack(pady=(7, 0))

        self.timeWidget = Label(frame1, text="00:00:00", bg=self.bg_color, fg="white",
                                bd=2, font="ds-digital 14 bold")
        frame2 = Frame(MainFrame, bg=self.bg_color)
        frm1 = Frame(frame2, bg=self.bg_color)
        frm2 = Frame(frame2, bg=self.bg_color)

        # Packed
        frame1.grid(row=0, column=0, padx=(5, 10))
        self.timeWidget.pack(pady=(3, 0))
        frame2.grid(row=0, column=1)
        frm1.pack(pady=(10, 0))
        frm2.pack(pady=(10, 0))

        # Images
        image = Image.open(self.res_path("Images/stopwatch.png"))
        image = image.resize((18, 18), Image.ANTIALIAS)
        self.Stopwatch = ImageTk.PhotoImage(image)

        image = Image.open(self.res_path("Images/lap.png"))
        image = image.resize((18, 18), Image.ANTIALIAS)
        self.Lap = ImageTk.PhotoImage(image)

        image = Image.open(self.res_path("Images/split.png"))
        image = image.resize((18, 18), Image.ANTIALIAS)
        self.Split = ImageTk.PhotoImage(image)

        image = Image.open(self.res_path("Images/reset.png"))
        image = image.resize((18, 18), Image.ANTIALIAS)
        self.Reset = ImageTk.PhotoImage(image)

        image = Image.open(self.res_path("Images/play.png"))
        image = image.resize((18, 18), Image.ANTIALIAS)
        self.Start = ImageTk.PhotoImage(image)

        image = Image.open(self.res_path("Images/pause.png"))
        image = image.resize((18, 18), Image.ANTIALIAS)
        self.Pause = ImageTk.PhotoImage(image)

        image = Image.open(self.res_path("Images/stop.png"))
        image = image.resize((18, 18), Image.ANTIALIAS)
        self.Stop = ImageTk.PhotoImage(image)

        # Buttons
        self.lap_btn = Button(frm1, text="Lap - Ctrl+L", image=self.Lap, command=self.lap, bg=self.bg_color,
                              fg="white", activebackground=self.activebgclr, relief="flat", bd=0)
        self.lap_btn.grid(row=0, column=0, padx=(0, 5))
        self.stopwatch_btn = Button(frm1, text="Transition - Ctrl+T", image=self.Stopwatch, command=self.transition,
                                    fg="white", bg=self.bg_color, activebackground=self.activebgclr, relief="flat", bd=0)
        self.stopwatch_btn.grid(row=0, column=1, padx=(5, 5))
        self.split_btn = Button(frm1, text="Split - Ctrl+S", image=self.Split, command=self.split,
                                bg=self.bg_color, fg="white", activebackground=self.activebgclr, relief="flat", bd=0)
        self.split_btn.grid(row=0, column=2, padx=(5, 0))
        self.reset_btn = Button(frm2, text="Reset Clock - Ctrl+R", image=self.Reset, command=self.reset,
                                bg=self.bg_color, fg="white", activebackground=self.activebgclr, relief="flat", bd=0)
        self.reset_btn.grid(row=0, column=0, padx=(0, 5))
        self.stp = Button(frm2, text="Pause/Play - Ctrl+P", image=self.Start, command=self.stop, bg=self.bg_color,
                          fg="white", activebackground=self.activebgclr, relief="flat", bd=0)
        self.stp.grid(row=0, column=1, padx=(5, 5))
        self.stop_btn = Button(frm2, text="End - Ctrl+X", image=self.Stop, command=self.end, bg=self.bg_color,
                               fg="white", activebackground=self.activebgclr, relief="flat", bd=0)
        self.stop_btn.grid(row=0, column=2, padx=(5, 0))

        self.AllButtons = [self.lap_btn, self.stopwatch_btn,
                           self.split_btn, self.reset_btn, self.stp, self.stop_btn]

        # Button Bindings
        self.root.bind("<Control-l>", lambda e: self.lap_btn.invoke())
        self.root.bind("<Control-s>", lambda e: self.split_btn.invoke())
        self.root.bind("<Control-r>", lambda e: self.reset_btn.invoke())
        self.root.bind("<Control-p>", lambda e: self.stp.invoke())
        self.root.bind("<Control-x>", lambda e: self.stop_btn.invoke())
        self.root.bind("<Control-t>", lambda e: self.stopwatch_btn.invoke())

        # root.bind("<Motion>", getxy)

        # Hover and Leave Bindings
        for i in self.AllButtons:
            i.bind("<Enter>", self.OnHover)
            i.bind("<Leave>", self.OnLeave)

        self.root.mainloop()

    def res_path(self, rel):
        try:
            base = sys._MEIPASS  # Path where pyinstaller stores media
        except Exception:
            base = os.path.abspath(".")  # When testing program
        return os.path.join(base, rel)

    @staticmethod
    def _rgb(rgb):
        """Enables to use rgb format of color in tkinter
            rgb: tuple containing color value in range of 0 to 255"""
        return '#%02x%02x%02x' % rgb

    def dragwin(self, event):
        x = self.root.winfo_pointerx() - _offsetx
        y = self.root.winfo_pointery() - _offsety
        self.root.geometry(f"{self.rootw}x{self.rooth}+{x}+{y}")
        event.x = 20

    def clickwin(self, event):
        global _offsetx, _offsety
        _offsetx = event.x
        _offsety = event.y

    def dragwid(self, event):
        x = self.wid.winfo_pointerx() - _offsetx
        y = self.wid.winfo_pointery() - _offsety
        self.wid.geometry(f"+{x}+{y}")

    def music(self):
        global timeroff
        mixer.music.play(-1)
        self.timeroff = True

    def stop(self):
        if self.stp_strt:
            self.stp_strt = False
            try:
                self.root.after_cancel(self.wth)
            except:
                pass
            if self.timeroff:
                if not self.count:
                    self.count = self.countdown  # Pauses timer in between when commented
                self.hrs, self.mins, self.secs = self.returntime(self.count)
                wthtxt = '{:02d}:{:02d}:{:02d}'.format(
                    self.hrs, self.mins, self.secs)
                self.timeWidget.configure(text=wthtxt)
                mixer.music.stop()
            self.stp.configure(image=self.Start)
        else:
            self.stp_strt = True
            self.stp.configure(image=self.Pause)
            self.watch()

    def lap(self):
        if self.stp_strt == True:
            self.tkn = True
            self.spt = 0
            self.avg += self.count-1
            self.count = 0
            self.lp += 1
            self.lap_spt += f'Lap{self.lp}: ' + \
                '{:02d}:{:02d}:{:02d}\n'.format(self.hrs, self.mins, self.secs)

    def split(self):
        global spt, lap_spt
        if self.stp_strt == True:
            self.spt += 1
            self.lap_spt += f'Split{self.spt}: ' + \
                '{:02d}:{:02d}:{:02d}\n'.format(self.hrs, self.mins, self.secs)

    def transition(self):
        try:
            self.stp_strt = False
            self.root.after_cancel(self.wth)
            self.stp.configure(image=self.Start)
        except:
            pass
        if self.timer:
            self.timer = False
            self.lap_btn.configure(state="active")
            self.split_btn.configure(state="active")
            self.count = 0
            self.hrs, self.mins, self.secs = self.returntime(self.count)
            wthtxt = '{:02d}:{:02d}:{:02d}'.format(
                self.hrs, self.mins, self.secs)
            self.timeWidget.configure(text=wthtxt)
            self.logoname.configure(text="Stop Watch")

            time.sleep(.5)
            self.lap_btn.focus_set()
            self.split_btn.focus_set()
            self.tkn = False
            os.system('title Stop Watch')
        else:
            self.timer = True
            self.lap_btn.configure(state="disabled")
            self.split_btn.configure(state="disabled")
            self.logoname.configure(text="Timer")
            self.tkn = True
            self.end()

    def reset(self):
        if self.timer:
            mixer.music.stop()
            self.count = self.countdown
            self.hrs, self.mins, self.secs = self.returntime(self.count)
            self.timeWidget.configure(
                text='{:02d}:{:02d}:{:02d}'.format(self.hrs, self.mins, self.secs))
        else:
            self.count = 0
            self.timeWidget.configure(text="00:00:00")

    def returntime(self, count):
        mins, secs = divmod(self.count, 60)
        hrs, mins = divmod(mins, 60)
        return hrs, mins, secs

    def watch(self):
        self.hrs, self.mins, self.secs = self.returntime(self.count)
        wthtxt = '{:02d}:{:02d}:{:02d}'.format(self.hrs, self.mins, self.secs)
        self.timeWidget.configure(text=wthtxt)
        self.wth = self.root.after(1000, self.watch)

        if self.timer and self.count == 0:
            self.root.after_cancel(self.wth)
            initial = time.time()
            self.music()
        elif self.timer:
            self.count -= 1
        else:
            self.count += 1

    def end(self):

        if self.tkn:
            self.tkn = False
            self.wid = Toplevel(self.root)
            self.wid.overrideredirect(True)
            self.wid.configure(background=self.bg_color)

            screenw = int(self.root.winfo_screenwidth()/2 - self.rootw/4)
            screenh = int(self.root.winfo_screenheight()/2 - self.rooth/4)

            self.wid.geometry(f"+{screenw}+{screenh}")
            self.wid.attributes("-topmost", True)
            self.wid.attributes('-alpha', 0.8)
            self.wid.bind('<Button-1>', self.clickwin)
            self.wid.bind('<B1-Motion>', self.dragwid)
            self.wid.grab_set()

            if not self.timer:
                os.system('title Exit Menu')
                self.root.after_cancel(self.wth)

                if self.avg < 0:
                    self.avg = 0

                self.tmins, self.tsecs = divmod(self.avg, 60)
                self.thrs, self.tmins = divmod(self.tmins, 60)

                self.avg = round(self.avg/self.lp)

                self.amins, self.asecs = divmod(self.avg, 60)
                self.ahrs, self.amins = divmod(self.amins, 60)

                image = Image.open(self.res_path("Images/stop.png"))
                image = image.resize((18, 18), Image.ANTIALIAS)
                Stop2 = ImageTk.PhotoImage(image, master=self.wid)

                Label(self.wid, text=self.lap_spt+'Total Time Taken:\n{:02d}:{:02d}:{:02d}\nYour Average Time is:\n{:02d}:{:02d}:{:02d}'.format(
                    self.thrs, self.tmins, self.tsecs, self.ahrs, self.amins, self.asecs), bg=self.bg_color, fg="white").pack(padx=5, pady=(10, 0))

                end2 = Button(self.wid, image=Stop2, command=lambda: self.exitfunc(self.lap_spt+'\nTotal Time Taken:{:02d}:{:02d}:{:02d}\nYour Average Time is:{:02d}:{:02d}:{:02d}\n\n\n'.format(
                    self.thrs, self.tmins, self.tsecs, self.ahrs, self.amins, self.asecs)), bg=self.bg_color,
                              fg="white", activebackground=self.activebgclr, relief="flat", bd=0)

                end2.image = Stop2
                end2.pack(pady=(5, 10))
                self.root.bind("e", lambda e: self.end.invoke())
                self.root.bind("<Control-x>", lambda e: self.exitfunc(self.lap_spt+'\nTotal Time Taken:{:02d}:{:02d}:{:02d}\nYour Average Time is:{:02d}:{:02d}:{:02d}\n\n\n'.format(
                    self.thrs, self.tmins, self.tsecs, self.ahrs, self.amins, self.asecs)))


            else:
                os.system('title Set Timer')
                inpt=Frame(self.wid, bg=self.bg_color)

                enter=Label(self.wid, text="Enter Time:\n(in seconds)",
                              fg="white", bg=self.bg_color)
                enter.grid(row=0, column=0)

                self.entry=Entry(inpt, fg="white", bg=self.bg_color,
                                   insertbackground='white', width=15)
                self.entry.pack(pady=(8, 0), padx=(0, 8))

                entered=Button(inpt, text="Submit", command=self.done, fg="white", bg=self.bg_color,
                                 activebackground=self.activebgclr, font=("Arial", 8), pady=0, bd=0)
                entered.pack()

                self.entry.focus_set()
                self.entry.bind("<Return>", lambda e: entered.invoke())
                inpt.grid(row=0, column=1, padx=5)
                self.wid.mainloop()

        else:
            os.system("cls")
            sys.exit()

    def done(self):
        os.system('title Timer')
        if self.entry.get() == "":
            self.countdown=10
        else:
            self.countdown=int(self.entry.get())
        self.count=self.countdown
        self.wid.destroy()
        hrs, mins, secs=self.returntime(self.count)
        wthtxt='{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs)
        self.timeWidget.configure(text=wthtxt)
        self.root.update()

    def exitfunc(self, label):
        with open("Logs.txt", "a") as f:
            f.write(label)
        self.wid.destroy()
        os.system("cls")
        sys.exit()

    def OnHover(self, event):
        # global frm
        # frm = Frame(root, bg=bg_color)
        if event.widget['state'] != "disabled":
            print(event.widget["text"])

        # info = Label(frm, text=event.widget["text"], bg=bg_color, foreground="white")
        # info.pack()
        # frm.place(x=x, y=y, width=100, height=10)

    def OnLeave(self, event):
        pass
        os.system('cls')
        # frm.place_forget()


if __name__ == "__main__":
    clr=StopWatch._rgb((3, 123, 252))
    stopwatch=StopWatch(clr, clr)
