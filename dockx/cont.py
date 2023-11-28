from tkinter import LabelFrame, OptionMenu, PhotoImage, Toplevel, messagebox, ttk
from customtkinter import *
from PIL import Image, ImageTk
import os
import subprocess
import socket
import pickle
import threading
from tkinter.simpledialog import Dialog
from PIL import ImageGrab, Image, ImageTk, ImageFilter
import docker
from tkterminal import Terminal
import keyboard
import psutil

current_directory = os.getcwd()

set_appearance_mode("dark")  # Modes: system (default), light, dark
set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

def fun_yes():
    messagebox.showinfo('Return', 'All containers are closed.')
    y = messagebox.askyesno("Confirmation", "Do you want to Logout?")
    if y:
        root.destroy()
    else:
        messagebox.showinfo('Return', 'You will now return to the main screen.')


def fun_no():
    y = messagebox.askyesno("Confirmation", "Do you want to Logout?")
    if y:
        root.destroy()
    else:
        messagebox.showinfo('Return', 'You will now return to the main screen.')


def fun():
    x = messagebox.askyesno("Confirmation", "Do you want to close all containers?")
    if x:
        fun_yes()
    else:
        fun_no()

def home():
    root.destroy()
    import main

def stats():
    root.destroy()
    import launcher
#Write a function to get data from socket 47475 on localhost and store it in a list

network_snapshot = []

def get_network_snapshot(sock, recieved_flag):
    # Listen for incoming connections
    sock.listen(1)
    print("Waiting for a connection...")

    # Accept a connection from the sender
    conn, addr = sock.accept()
    print("Connection established with:", addr)
    try:
        global network_snapshot
        # Receive and process the system snapshot continuously
        while True:
            # Receive the data from the sender
            serialized_data = conn.recv(4096)

            # Deserialize the data using pickle
            network_snapshot = pickle.loads(serialized_data)
            #print(network_snapshot)
            if(recieved_flag.is_set()):
                continue
            else:
                recieved_flag.set()
            
    finally:
        # Close the connection and the socket
        conn.close()
        sock.close() # Create a socket and connect to the receiver

def is_key_combination_pressed(combination):
    # Check if all of the keys in the combination are pressed.
    for key in combination:
        if not keyboard.is_pressed(key):
            return False

    # All of the keys in the combination are pressed.
    return True

def is_alt_f4_pressed(event):
    combination = ["alt", "f4"]
    return is_key_combination_pressed(combination)

def close_application(event):
    root.destroy()
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "python.exe":
            proc.kill()

if __name__ == '__main__':
# Create a socket and bind it to a specific host and port
    host = 'localhost'
    port = 47475
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))

    recieved_flag = threading.Event()
    # Create a thread to receive the system snapshot
    recieve_thread = threading.Thread(target= get_network_snapshot, args=(sock,recieved_flag))
    recieve_thread.start()
    
    def launch_net():
        os.system("python backend/network.py")
    
    p = threading.Thread(target=launch_net)
    p.start()

    recieved_flag.wait()

    if(recieved_flag.is_set()):
        root = CTk()
        root.title("DOCK-X")
        root.attributes('-fullscreen', True)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width},{screen_height}")

        rel_path_favicon = "assets/favicon.ico"
        img_path_favicon = os.path.join(current_directory, rel_path_favicon)

        root.iconbitmap(img_path_favicon)
        #sidePaneMenu
        framemenu = CTkFrame(master=root,height=screen_height,width=screen_width/4,fg_color="#313131")

        rel_path_round = "assets/round.png"
        img_path_round = os.path.join(current_directory, rel_path_round)

        img = CTkImage(light_image=Image.open(img_path_round),dark_image=Image.open(img_path_round),size=(150,150))
        imglabel= CTkLabel(framemenu, text='', image = img, corner_radius=50).pack(side=TOP,padx=(10,10),pady=(20,10))

        label = CTkLabel(master=framemenu,text="047pegasus",font=("Montserrat SemiBold", 20), fg_color='#3E3E3E',text_color='White').pack(side=TOP,padx=0,pady=(25,25))

        rel_path_home = "assets/home.png"
        img_path_home = os.path.join(current_directory, rel_path_home)

        download_home=CTkImage(light_image=Image.open(img_path_home),dark_image=Image.open(img_path_home),size=(30,30))
        homelabel = CTkButton(master=framemenu,text="Home",font=("Montserrat SemiBold" ,20), cursor='arrow', fg_color='#3E3E3E',hover_color='#3E3E3E',text_color='White',image=download_home, command=home).pack(side=TOP,padx=(0,20),pady=(110,10))

        rel_path_stats = "assets/statistics.png"
        img_path_stats = os.path.join(current_directory, rel_path_stats)

        download_stat=CTkImage(light_image=Image.open(img_path_stats),dark_image=Image.open(img_path_stats),size=(30,30))
        cpustatslabel = CTkButton(master=framemenu,text="Statistics",font=("Montserrat SemiBold", 20), cursor='arrow',fg_color='#3E3E3E',hover_color='#3E3E3E',text_color='White',image=download_stat, command = stats).pack(side=TOP,padx=0,pady=(20,10))

        rel_path_box = "assets/box.png"
        img_path_box = os.path.join(current_directory, rel_path_box)

        download_cont=CTkImage(light_image=Image.open(img_path_box),dark_image=Image.open(img_path_box),size=(25,25))
        contlabel = CTkButton(master=framemenu,text="Containers",font=("Montserrat SemiBold", 20), cursor='arrow',fg_color='#3E3E3E',hover_color='#3E3E3E',text_color='White',image=download_cont).pack(side=TOP,padx=0,pady=(20,10))

        rel_path_dock = "assets/docker_greenjpg.jpg"
        img_path_dock = os.path.join(current_directory, rel_path_dock)

        run_img = CTkImage(light_image=Image.open(img_path_dock),dark_image=Image.open(img_path_dock),size=(200,50))
        running_label = CTkLabel(framemenu,text='', image= run_img,fg_color='green',corner_radius=0).pack(side=BOTTOM,padx=0,pady=(51,0))

        button = CTkButton(framemenu,text="Logout",font=("Montserrat", 20), fg_color="#1D0042", width=140,height=40,corner_radius=10,command=fun).pack(side=BOTTOM,padx=0,pady=(100,20))
        framemenu.pack(side=LEFT, fill=BOTH, padx=0, pady=0)

        # mainWindowFrame
        frame_main = CTkFrame(master=root, width=1000, height=800, fg_color="Black")

        frame_Top = CTkFrame(master=frame_main, width=1000, height=700, fg_color="gray10")
        frame_Left = CTkFrame(master=frame_Top, width=1000, height=600, fg_color="gray10")
        frame_Right = CTkFrame(master=frame_Top, width=800, height=600, fg_color="#071330")

        can1 = CTkCanvas(frame_Right, bg="#071330", height="600", width=680, highlightthickness=0)

        rel_path_cloud = "assets/cloud.png"
        img_path_cloud = os.path.join(current_directory, rel_path_cloud)
        cloudimg = CTkImage(light_image=Image.open(img_path_cloud), dark_image=Image.open(img_path_cloud), size=(30, 30))
        instab = CTkLabel(can1, text="Network Inspector Tab", font=("Montserrat SemiBold", 20), fg_color="#071330", text_color='White', anchor="w")

        cloud_label = CTkLabel(can1, text='', image=cloudimg, fg_color='#071330', corner_radius=0, anchor="w")
        cloud_label.pack(side=LEFT, anchor="nw", padx=(100,0), pady=5)
        instab.pack(side=LEFT, anchor="nw", padx=(20, 100), pady=5)
        
        # A text area to display recieved network information
        
        class ScrollableLabelButtonFrame(CTkScrollableFrame):
            def __init__(self, master, command=None, **kwargs):
                super().__init__(master, **kwargs)
                self.grid_columnconfigure(0, weight=1)

                self.command = command
                self.radiobutton_variable = StringVar()
                self.label_list = []
                self.button_list = []

            def add_item(self, item, image=None):
                label = CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
                button = CTkButton(self, text="Command", width=100, height=24)
                if self.command is not None:
                    button.configure(command=lambda: self.command(item))
                label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
                button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
                self.label_list.append(label)
                self.button_list.append(button)

            def remove_item(self, item):
                for label, button in zip(self.label_list, self.button_list):
                    if item == label.cget("text"):
                        label.destroy()
                        button.destroy()
                        self.label_list.remove(label)
                        self.button_list.remove(button)
                        return

        scrollnet = ScrollableLabelButtonFrame(master=can1, width=600, height = 500, corner_radius=0)
        scrollnet.pack(side=BOTTOM, anchor="n", fill = BOTH, padx=0, pady=(70,0))
        
        for i in range (len(network_snapshot)):
            scrollnet.add_item(network_snapshot[i])

        can1.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)

        frame_LeftTop=CTkFrame(master=frame_Left, width=1000, height=50, fg_color="gray10")

        frame_LeftBottom=CTkFrame(master=frame_Left, width=1000, height=500, fg_color="#1560BD")
        rel_path_eth = "assets/ethernet.png"
        img_path_eth = os.path.join(current_directory, rel_path_eth)
        ethernet_img = CTkImage(light_image=Image.open(img_path_eth), dark_image=Image.open(img_path_eth), size=(30, 30))
        activity_label = CTkLabel(frame_LeftBottom, text="Port Exposure Activity Tab", font=("Montserrat SemiBold", 20), fg_color="#1560BD", text_color='White')

        ethernet_label = CTkLabel(frame_LeftBottom, text='', image=ethernet_img, fg_color='#1560BD', corner_radius=0)
        ethernet_label.pack(side=LEFT, anchor=NW, padx=10, pady=5)

        activity_label.pack(side=TOP, anchor=NW, padx=(0,0), pady=5)


        frame_cname=CTkFrame(master=frame_LeftTop, width=850, height=50, fg_color="#1560BD")
        cname=CTkCanvas(frame_cname, bg="#1560BD", height="50", width=850,highlightthickness=0)
        contname = CTkLabel(cname, text="Container name :", font=("Montserrat SemiBold", 20), fg_color="#1560BD", text_color='White').pack(side=LEFT, padx=(10,0), pady=5)
        rel_path_refresh = "assets/refresh.png"
        img_path_refresh = os.path.join(current_directory, rel_path_refresh)
        refimg = CTkImage(light_image=Image.open(img_path_refresh), dark_image=Image.open(img_path_refresh),size=(30,30))
        ref_label = CTkLabel(cname, text='', image=refimg, fg_color='#1560BD', corner_radius=0).pack(side=RIGHT, padx=(800,0),  pady=(0,0))
        cname.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)

        frame_spin=CTkFrame(master=frame_LeftTop, width=200, height=50, fg_color="#1560BD")
        
        spin=CTkCanvas(frame_spin, bg="#1560BD", height="50", width=200,highlightthickness=0)
        
        class ComboboxDialog(Dialog):
            def body(self, master):
                self.title("Container Details")
                screen_width = master.winfo_screenwidth()
                screen_height = master.winfo_screenheight()
                x = (screen_width - 500) / 2
                y = (screen_height - 150) / 2
                self.geometry(f"500x150+{int(x)}+{int(y)}")
                self.overrideredirect(True)

                # Create the Combobox widget
                items = ["--Select a Container--", "ubuntu"]
                self.combobox = ttk.Combobox(master, values=items, width=40, background="#313131", foreground="#000000", font=("Montserrat SemiBold", 12), state="readonly")
                self.combobox.pack(pady=20, padx=20)

                # Optionally, set an initial selection
                self.combobox.set(items[0])

            def apply(self):
                selected_container = self.combobox.get()
                if selected_container == "--Select a Container--":
                    messagebox.showerror("Error", "Please select a container.")
                    self.result = None  # This prevents the dialog from closing when there's an error.
                else:
                    self.result = selected_container

        def run_selected_container(container_name):
            client = docker.from_env()
            selected_container = client.containers.run(container_name, detach=True)
            print(f"Started container '{container_name}', ID: {selected_container.id}")

        def create_combobox_window():
            dialog = ComboboxDialog(root)
            result = dialog.result  # Get the selected container (or None if canceled)
            if result:
                run_selected_container(result)
    
        sp = CTkButton(master=spin, text="Spin new", font=("Montserrat", 20), cursor='arrow', fg_color='#1560BD', hover_color='#00008B', text_color='White',command=create_combobox_window).pack(side=LEFT, padx=(10,0), pady=5)
        rel_path_hard = "assets/hard_drive.png"
        img_path_hard = os.path.join(current_directory, rel_path_hard)
        hardimg = CTkImage(light_image=Image.open(img_path_hard), dark_image=Image.open(img_path_hard),size=(30,30))
        hard_label = CTkLabel(spin, text='', image=hardimg, fg_color='#1560BD', corner_radius=0).pack(side=RIGHT, padx=(0,20),  pady=(0,0))

        spin.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
        frame_cname.pack(side=LEFT, fill=BOTH, padx=0, pady=10)
        frame_spin.pack(side=RIGHT, fill=BOTH, padx=(10,0), pady=10)


        frame_LeftBottomIn=CTkFrame(master=frame_LeftBottom, width=1000, height=500, fg_color="#0A2351")
        ins=CTkCanvas(frame_LeftBottomIn, bg="#0A2351", height="500", width=1000,highlightthickness=0)
        ins.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=0)

        frame_LeftBottomIn.pack(side=BOTTOM, fill=BOTH, padx=(0,50), pady=10)

        frame_LeftTop.pack(side=TOP, fill=BOTH, padx=0, pady=10)
        frame_LeftBottom.pack(side=BOTTOM, fill=BOTH, padx=0, pady=(0,30))
        frame_Left.pack(side=LEFT, fill=BOTH, padx=(10,0), pady=0)
        frame_Right.pack(side=RIGHT, fill=BOTH, padx=(10,10), pady=(20,30))

        frame_Top.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=(0,0))

        frame_Bottom = CTkFrame(master=frame_main, width=1000, height=1200, fg_color="gray10")

        can2 = CTkCanvas(frame_Bottom, bg="gray17", height="300", width=1000,highlightthickness=2)

        terminal = Terminal(master=can2, yscrollcommand=set(), wrap=WORD, background="black", foreground="white", pady=5, padx=5)
        terminal.shell = True
        terminal.basename = 'DOCK-X'	
        terminal.pack(expand=True, fill='both')

        can2.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=(0,10))

        frame_Bottombar = CTkFrame(master=frame_main, width=1000, height=70, fg_color="gray19", corner_radius=0) 
        CPUlabel = CTkLabel(master=frame_Bottombar,text="CPU: 65.01%",font=("Montserrat" ,15), fg_color='gray19',text_color='White').pack(side=LEFT,padx=40,pady=12)
        Memlabel = CTkLabel(master=frame_Bottombar,text="Memory: 61%",font=("Montserrat" ,15), fg_color='gray19',text_color='White').pack(side=LEFT,padx=10,pady=12)
        Disklabel = CTkLabel(master=frame_Bottombar,text="Disk: 35%",font=("Montserrat" ,15), fg_color='gray19',text_color='White').pack(side=LEFT,padx=10,pady=12)
        Conlabel = CTkLabel(master=frame_Bottombar,text="Containers: Online ✅",font=("Montserrat" ,15), fg_color='gray19',text_color='White').pack(side=RIGHT,padx=(0,40),pady=12)
        Servlabel = CTkLabel(master=frame_Bottombar,text="Service: Running ⚡",font=("Montserrat" ,15), fg_color='gray19',text_color='White').pack(side=RIGHT,padx=20,pady=12)
        frame_Bottombar.pack(side=BOTTOM,fill=BOTH,expand=True,padx=0,pady=0)

        frame_Bottom.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
        frame_main.pack(side=RIGHT, padx=0, expand=True, fill=BOTH)

        root.bind('<Alt-F4>', is_alt_f4_pressed)
        root.bind('<Destroy>', close_application)

        root.mainloop()