import os
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from pygame import mixer
import time
from mutagen.mp3 import MP3
import threading
from tkinter import ttk
from ttkthemes import themed_tk as themes

root = themes.ThemedTk()
root.get_themes()
root.set_theme("radiance")
mixer.init()  # initializing the mixer

muted = False
# creating menu option at the top of window
menu_bar = Menu(root)
root.config(menu=menu_bar)


def open_browser():
    global filename_w_path
    filename_w_path = filedialog.askopenfilename()
    add_to_playlist(filename_w_path)


playlist = []


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlist_box.insert(index, filename)
    playlist.insert(index, filename_w_path)
    playlist_box.pack()
    index += 1


# creating submenu options

sub_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=sub_menu)
sub_menu.add_cascade(label="Open", command=open_browser)
sub_menu.add_cascade(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo("About Melody",
                                "Hello Dear User!!"
                                " This music player is developed using python by Vedant Achtani. "
                                "Hope you enjoy it. Cheers!")


sub_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=sub_menu)
sub_menu.add_cascade(label="About Us", command=about_us)

root.title("GoodMusic")
root.geometry('')
root.iconbitmap(r"images/boombox.ico")


def show_detail(playing_song):
    global total_time
    file_label['text'] = "Now Playing-- " + os.path.basename(playing_song)
    file_data = os.path.splitext(playing_song)

    if file_data[1] == '.mp3':
        audio = MP3(playing_song)
        total_length = audio.info.length
    else:
        audio = mixer.Sound(playing_song)
        total_length = audio.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = "{:02d}:{:02d}".format(mins, secs)
    total_time = time_format
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global total_time
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            time_format = "{:02d}:{:02d}".format(mins, secs)
            seek_time_label['text'] = "Seek Time -- " + time_format + " / " + total_time
            time.sleep(1)
            current_time += 1


def play_music():
    global now_playing
    global paused
    if paused:
        mixer.music.unpause()
        status_bar['text'] = 'Music Resumed'
        paused = False
    else:

        try:
            stop_music()
            time.sleep(1)
            selected_song = playlist_box.curselection()
            selected_song = int(selected_song[0])
            now_playing = playlist[selected_song]
            mixer.music.load(now_playing)
            mixer.music.play()
            show_detail(now_playing)
            status_bar['text'] = "playing " + os.path.basename(now_playing)
        except:
            tkinter.messagebox.showinfo("ERROR - NO AUDIO FILE FOUND.",
                                        "Melody could not find the file to play. "
                                        "please make sure to load a file before playing")


paused = False


def pause_music():
    global paused
    if not paused:
        mixer.music.pause()
        status_bar['text'] = "music paused... "
        paused = True


def stop_music():
    mixer.music.stop()
    status_bar['text'] = "Stopped playing... "


def rewind_music():
    mixer.music.rewind()
    status_bar['text'] = "Rewinding... "


def mute_music():
    global muted
    if not muted:
        mute_button.configure(image=mute_photo)
        mixer.music.set_volume(0)
        scale.set(0)
        status_bar['text'] = "Muted... "
        muted = True
    else:
        mute_button.configure(image=volume_photo)
        mixer.music.set_volume(0.7)
        scale.set(70)
        muted = False
        status_bar['text'] = "un-muted... "


def set_vol(val):
    global score
    score = float(val) / 100
    mixer.music.set_volume(score)


def delete_music():
    selected_song = playlist_box.curselection()
    selected_song = int(selected_song[0])
    playlist_box.delete(selected_song)
    playlist.pop(selected_song)


play_photo = PhotoImage(file='images/play-button.png')
pause_photo = PhotoImage(file='images/pause-button.png')
stop_photo = PhotoImage(file='images/stop.png')
rewind_photo = PhotoImage(file='images/rewind.png')
mute_photo = PhotoImage(file='images/no-sound.png')
volume_photo = PhotoImage(file='images/volume-button.png')

# root - status bar, left frame and right frame
# left frame - playlist box , add and delete button
# right frame - top frame,middle frame and bottom frame

status_bar = Label(root, text="Welcome to GoodMusic!!", anchor=W, relief=SUNKEN, font='Arial 10 italic')
status_bar.pack(side=BOTTOM, fill=X)

left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=30)

playlist_box = Listbox(left_frame)
playlist_box.pack()

right_frame = Frame(root)
right_frame.pack(side=RIGHT, padx=30)

add_button = ttk.Button(left_frame, text="add", command=open_browser)
add_button.pack(side=LEFT)

del_button = ttk.Button(left_frame, text="delete", command=delete_music)
del_button.pack()

top_frame = Frame(right_frame)
top_frame.pack()

file_label = ttk.Label(top_frame, text="Let's Make Some Noise!", relief=SUNKEN)
file_label.pack(pady=15)

seek_time_label = ttk.Label(top_frame, text=" Seek Time --/--", relief=GROOVE)
seek_time_label.pack()

middle_frame = Frame(right_frame)
middle_frame.pack(pady=35)

play_button = ttk.Button(middle_frame, image=play_photo, command=play_music)  # all the buttons packed here for display
play_button.grid(row=0, column=0, padx=10)
pause_button = ttk.Button(middle_frame, image=pause_photo, command=pause_music)
pause_button.grid(row=0, column=1, padx=10)
stop_button = ttk.Button(middle_frame, image=stop_photo, command=stop_music)
stop_button.grid(row=0, column=2, padx=10)

bottom_frame = Frame(right_frame)
bottom_frame.pack()

mute_button = ttk.Button(bottom_frame, image=volume_photo, command=mute_music)
mute_button.grid(row=0, column=1, padx=10)

rewind_button = ttk.Button(bottom_frame, image=rewind_photo, command=rewind_music)
rewind_button.grid(row=0, column=0, padx=10)

scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(30)
mixer.music.set_volume(0.3)
scale.grid(row=0, column=2)


def closing_window():
    try:
        stop_music()
        root.destroy()
    except NameError:
        root.destroy()


root.protocol('WM_DELETE_WINDOW', closing_window)
root.mainloop()
