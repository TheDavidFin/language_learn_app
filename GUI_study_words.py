import recorder
import tkinter as tk
from tkinter import ttk
import os
from play_audio import AudioFile
import random
from settings_ import Settings
import ntpath

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Learn Hebrew")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1, minsize=400)
        container.grid_columnconfigure(0, weight=1, minsize=1200)

        self.frames = {}

        for F in (StartPage, RecordPage, LessonPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(padx=100, pady=10)

        record_button = ttk.Button(self, text="Record audio",
                           command=lambda: controller.show_frame(RecordPage))
        record_button.pack(padx=100, pady=50)


        lesson_button = ttk.Button(self, text="Start lesson",
                            command=lambda: controller.show_frame(LessonPage))
        lesson_button.pack(padx=100, pady=110)


class RecordPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.rec = recorder.Recorder(channels=2)
        self.running = None

        label = ttk.Label(self, text="Record audio", font=LARGE_FONT)
        label.place(x=300, y=10)

        Label_hebrew_name = ttk.Label(self, text='Write word in Hebrew')
        Label_hebrew_name.place(x=10, y=60)
        self.Entry_hebrew_name = tk.Entry(self, width=120)
        self.Entry_hebrew_name.place(x=10, y=90)
        Label_russian_name = ttk.Label(self, text='Write word in Russian')
        Label_russian_name.place(x=10, y=140)
        self.Entry_russian_name = tk.Entry(self, width=120)
        self.Entry_russian_name.place(x=10, y=170)
        Label_another_name = ttk.Label(self, text='Write word in another language')
        Label_another_name.place(x=10, y=210)
        self.Entry_another_name = tk.Entry(self, width=120)
        self.Entry_another_name.place(x=10, y=240)



        button_start_record = tk.Button(self, text="Start record",
                            command=self.start_record)
        button_start_record.place(x=330, y=310)

        button_stop_record = tk.Button(self, text="Stop record",
                                        command=self.stop_record)
        button_stop_record.place(x=430, y=310)

        button_save_record = tk.Button(self, text="Play record",
                                       command=self.play_record)
        button_save_record.place(x=530, y=310)

        button_start_page = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button_start_page.place(x=700, y=10)


    def play_record(self):
        a = AudioFile(self.file_path)
        a.play()
        a.close()


    def start_record(self):
        self.file_path = os.path.join(Settings().record_path, str(self.Entry_hebrew_name.get()) + '__' +
                                      str(self.Entry_russian_name.get()) +  '__' +
                                      str(self.Entry_another_name.get()) + r'.wav')
        print('record started')
        if self.running is not None:
            print('already running')
        else:
            self.running = self.rec.open(self.file_path, 'wb')
            self.running.start_recording()


    def stop_record(self):

        if self.running is not None:
            self.running.stop_recording()
            self.running.close()
            self.running = None
            print('stop record')
        else:
            print('not running')


class LessonPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start lesson", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.start_lesson()


        button_start_page = tk.Button(self, text="Back to Home",
                                      command=lambda: controller.show_frame(StartPage))
        button_start_page.place(x=700, y=10)

        button_play_record = tk.Button(self, text="Play next",
                            command=self.play_next)
        button_play_record.place(x=390, y=130)

        button_play_record = tk.Button(self, text="Play previous",
                                       command=self.play_previous)
        button_play_record.place(x=300, y=130)

        button_show_rus_word = tk.Button(self, text="Show RUS",
                                       command=self.show_rus_word)
        button_show_rus_word.place(x=330, y=190)

        button_show_leng_word = tk.Button(self, text="Show language",
                                         command=self.show_second_word)
        button_show_leng_word.place(x=330, y=230)

        button_show_leng_word = tk.Button(self, text="remove from lesson",
                                          command=self.remove_from_lesson)
        button_show_leng_word.place(x=330, y=260)


    def start_lesson(self):
        folder_path = Settings().lesson_path
        self.words_names_list = []
        aux_words_names_list = []
        for file in os.listdir(folder_path):
            if file.endswith(".wav"):
                aux_words_names_list.append(os.path.join(folder_path, file))
        while aux_words_names_list:
            file_path = random.choice(aux_words_names_list)
            self.words_names_list.append(file_path)
            aux_words_names_list.remove(file_path)
        self.word_number = -1


    def play_next(self):
        self.word_number += 1
        if self.word_number > len(self.words_names_list) - 1:
            self.word_number  = 0
        self.file_path = self.words_names_list[self.word_number]
        a = AudioFile(self.file_path)
        a.play()
        a.close()


    def play_previous(self):
        self.word_number -= 1
        if self.word_number < 0:
            self.word_number = len(self.words_names_list) - 1
        self.file_path = self.words_names_list[self.word_number]
        a = AudioFile(self.file_path)
        a.play()
        a.close()


    def remove_from_lesson(self):
        self.words_names_list.remove(self.file_path)


    def show_rus_word(self):
        root = tk.Tk()
        head, tail = ntpath.split(self.file_path)
        word = tail[:-4].split('__')[1]
        Label_finish = tk.Label(root, text=word, font="Arial 32")
        Label_finish.pack()


    def show_second_word(self):
        root = tk.Tk()
        head, tail = ntpath.split(self.file_path)
        word = tail[:-4].split('__')[0]
        Label_finish = tk.Label(root, text=word, font="Arial 32")
        Label_finish.pack()


    def show_third_word(self):
        root = tk.Tk()
        head, tail = ntpath.split(self.file_path)
        word = tail[:-4].split('__')[2]
        Label_finish = tk.Label(root, text=word, font="Arial 32")
        Label_finish.pack()


app = SeaofBTCapp()
app.mainloop()