# TODO: [CLEANUP] change all ints to doubles/floats? (e.g. limits entries)
# TODO: [CLEANUP] use loops to make multiple widgets
# TODO: enforce carriage movement/limit physical maximum of x=-5000, +5000?

import tkinter as tk  # package: allows import and use of tkinter GUI modules
from tkinter import *  # imports all of tkinter's modules
import customtkinter as ctk  # package: custom, pre-made theming applied to tkinter's GUI based on Windows 11
import csv  # package: reading and writing to CSV (comma separated values) files
import gclib  # imports gclib.py file, must be in same directory
from threading import *  # package: allows tkinter to have multiple threads to run simultaneously
# import traceback  # module: provides traceback object associated with an exception
# import logging  # module: allows the program to output errors and exceptions to the log file
import os  # package: used to access user's OS for files and machine time
import sys  # package: used to access user's OS for files

# default themes for the program
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# gets absolute path to resource (icon), works for dev and for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# alternate between filepaths for executable vs dev
filepath = os.path.dirname(sys.executable) + "\\_internal\\mwt_storage.csv"
# filepath = os.path.dirname(sys.executable) + "\\mwt_storage.csv"
mwt_storage_reader = csv.reader(open(filepath, 'r'))
# mwt_storage_reader = csv.reader(open('mwt_storage.csv', 'r'))
mwt_dict = {}
for mwt_storage_row in mwt_storage_reader:
    k, v = mwt_storage_row
    mwt_dict[k] = v
print(mwt_dict)

galil = gclib.py()
status = "Disconnected"


class MoveCarriage(ctk.CTk):

    def __init__(self):
        super().__init__()

        global mwt_dict
        global status

        # - program attempts to connect to carriage, COM port must match what cpu sees/has assigned
        try:
            print('gclib version:', galil.GVersion())  # prints installed gclib version
            galil.GOpen('COM2 --baud 19200')  # change to COM port used by carriage
            print(galil.GInfo())  # prints connection information for carriage

        # - exception handler if program cannot connect to carriage
        except gclib.GclibError as e:
            print('Unexpected GclibError:', e)

        # - code runs only if program connects to carriage successfully
        else:
            c = galil.GCommand
            status = "Connected"

            # -- "A"/x axis default settings
            c('SHA')  # sets servo motor "A" to x-axis
            c('DPA=' + str(float(mwt_dict['x_actual']) * 40))  # x-axis last stored position
            c('FLA=' + str(float(mwt_dict['x_fwd_limit']) * 40))  # x-axis last stored fwd limit
            c('BLA=' + str(float(mwt_dict['x_rev_limit']) * 40))  # x-axis last stored rev limit
            c('SPA=' + mwt_dict['sp_x'])  # x-axis speed, 2000 cts/sec
            c('ACA=' + mwt_dict['ac_x'])  # x-axis acceleration, 1024 cts/sec
            c('DCA=' + mwt_dict['dc_x'])  # x-axis deceleration, 1024 cts/sec
            c('KPA=' + mwt_dict['kp_x'])  # x-axis proportional Kp, 4
            c('KIA=' + mwt_dict['ki_x'])  # x-axis integral Ki, 0.008
            c('KDA=' + mwt_dict['kd_x'])  # x-axis derivative Kd, 500

            # -- "B"/y axis default settings
            c('SHB')  # sets servo motor "B" to y-axis
            c('DPB=' + str(float(mwt_dict['y_actual']) * 40))  # y-axis last stored position
            c('FLB=' + str(float(mwt_dict['y_fwd_limit']) * 40))  # y-axis last stored fwd limit
            c('BLB=' + str(float(mwt_dict['y_rev_limit']) * 40))  # y-axis last stored rev limit
            c('SPB=' + mwt_dict['sp_y'])  # y-axis speed, 1500 cts/sec
            c('ACB=' + mwt_dict['ac_y'])  # y-axis acceleration, 1024 cts/sec
            c('DCB=' + mwt_dict['dc_y'])  # y-axis deceleration, 1024 cts/sec
            c('KPB=' + mwt_dict['kp_y'])  # y-axis proportional Kp, 4
            c('KIB=' + mwt_dict['ki_y'])  # y-axis integral Ki, 0.024
            c('KDB=' + mwt_dict['kd_y'])  # y-axis derivative Kd, 100

            # -- "C"/z axis default settings
            c('SHC')  # sets servo motor "C" to z-axis
            c('DPC=' + str(float(mwt_dict['z_actual']) * 40))  # z-axis last stored position
            c('FLC=' + str(float(mwt_dict['z_fwd_limit']) * 40))  # z-axis last stored fwd limit
            c('BLC=' + str(float(mwt_dict['z_rev_limit']) * 40))  # z-axis last stored rev limit
            c('SPC=' + mwt_dict['sp_z'])  # z-axis speed, 300 cts/sec
            c('ACC=' + mwt_dict['ac_z'])  # z-axis acceleration, 1024 cts/sec
            c('DCC=' + mwt_dict['dc_z'])  # z-axis deceleration, 1024 cts/sec
            c('KPC=' + mwt_dict['kp_z'])  # z-axis proportional Kp, 4
            c('KIC=' + mwt_dict['ki_z'])  # z-axis integral Ki, 0.008
            c('KDC=' + mwt_dict['kd_z'])  # z-axis derivative Kd, 1000

        # - configure gui
        # -- configure window
        self.title("FMF MWT Carriage")
        self.screen_width = self.winfo_screenwidth()  # or _width?
        self.screen_height = self.winfo_screenheight()  # or _height?
        print(f"Screen Width: {self.screen_width}, Screen Height: {self.screen_height}")
        self.app_width = 360.0
        self.app_height = 900.0
        self.open_at_x = (self.screen_width/2) - (self.app_width/2)
        self.open_at_y = (self.screen_height/2) - (self.app_height/2)
        self.geometry(f"{self.app_width}x{self.app_height}+{self.open_at_x}+{self.open_at_y}")
        print(f"Geometry: {self.app_width}x{self.app_height}+{self.open_at_x}+{self.open_at_y}")
        self.resizable(True, True)

        # -- configure grid layout (1x4)
        self.grid_columnconfigure(0, weight=5)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=7)
        self.grid_rowconfigure(3, weight=1)

        # - dock widgets
        # -- create frame for dock widgets
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.grid(row=0, column=0, sticky="nsew")

        # -- dock labels
        self.label_title = ctk.CTkLabel(self.frame_top, text="MWT Carriage Controls",
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.label_version = ctk.CTkLabel(self.frame_top, text="Version 20250129 ",
                                          font=ctk.CTkFont(size=12, slant="italic"))

        # TODO: [OPTIONAL] create 'home' dock button that moves in order of z, y, x or selected order
        # TODO: [OPTIONAL] create 'set as home' dock button
        # -- dock buttons
        self.button_connect = ctk.CTkButton(self.frame_top, text='Disconnected', state="disabled",
                                            hover_color="dark red", fg_color="red",
                                            command=self.connect_carriage)
        self.button_stop = ctk.CTkButton(self.frame_top, text="Stop Carriage", hover_color="dark red", fg_color="red",
                                         command=self.stop_carriage)
        if status == "Connected":
            self.button_connect.configure(text="Connected", hover_color="dark green",
                                          fg_color="forest green")
        else:
            self.button_connect.configure(text="Disconnected", hover_color="dark red", fg_color="red")
        self.button_quit = ctk.CTkButton(self.frame_top, text='Quit Program', hover_color="grey40", fg_color="grey50",
                                         command=self.quit_carriage)

        # -- dock widget positioning
        self.label_title.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.label_version.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=0, sticky="n")
        self.button_connect.grid(row=2, column=0, padx=(30, 0), pady=(10, 0))
        self.button_quit.grid(row=2, column=1, padx=(15, 0), pady=(10, 0))
        self.button_stop.grid(row=3, column=0, columnspan=2, padx=(30, 0), pady=(10, 10), sticky="nsew")

        # - CARRIAGE POSITION AND LIMITS CONTROLS
        # -- create frame for carriage position and limits controls
        self.tabview_position = ctk.CTkTabview(self)
        self.tabview_position.grid(row=1, column=0, columnspan=2, padx=5, sticky="nsew")

        # - CARRIAGE POSITION CONTROLS
        # -- create frame for carriage position controls
        self.tabview_position.add("Positions")

        # -- controls database values entry defaults
        self.x_target = tk.StringVar()
        self.x_target.set(mwt_dict['x_actual'])
        self.y_target = tk.StringVar()
        self.y_target.set(mwt_dict['y_actual'])
        self.z_target = tk.StringVar()
        self.z_target.set(mwt_dict['z_actual'])
        self.x_actual = tk.StringVar()
        self.x_actual.set(mwt_dict['x_actual'])
        self.y_actual = tk.StringVar()
        self.y_actual.set(mwt_dict['y_actual'])
        self.z_actual = tk.StringVar()
        self.z_actual.set(mwt_dict['z_actual'])

        # -- controls labels
        self.label_position = ctk.CTkLabel(self.tabview_position.tab("Positions"), text="Carriage Position",
                                           anchor="center", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_target = ctk.CTkLabel(self.tabview_position.tab("Positions"), text="Target", anchor="center")
        self.label_actual = ctk.CTkLabel(self.tabview_position.tab("Positions"), text="Actual", anchor="center")
        self.label_x = ctk.CTkLabel(self.tabview_position.tab("Positions"), text="X", anchor="w")
        self.label_y = ctk.CTkLabel(self.tabview_position.tab("Positions"), text="Y", anchor="w")
        self.label_z = ctk.CTkLabel(self.tabview_position.tab("Positions"), text="Z", anchor="w")

        # -- controls entry fields
        self.entry_x_target = ctk.CTkEntry(self.tabview_position.tab("Positions"), width=70, height=50,
                                           font=ctk.CTkFont(size=20, weight="bold"), textvariable=self.x_target)
        self.entry_x_target.configure(justify="center")
        self.entry_y_target = ctk.CTkEntry(self.tabview_position.tab("Positions"), width=70, height=50,
                                           font=ctk.CTkFont(size=20, weight="bold"), textvariable=self.y_target)
        self.entry_y_target.configure(justify="center")
        self.entry_z_target = ctk.CTkEntry(self.tabview_position.tab("Positions"), width=70, height=50,
                                           font=ctk.CTkFont(size=20, weight="bold"), textvariable=self.z_target)
        self.entry_z_target.configure(justify="center")
        self.entry_x_actual = ctk.CTkEntry(self.tabview_position.tab("Positions"), width=70, state="disabled",
                                           font=ctk.CTkFont(size=20), fg_color="transparent",
                                           textvariable=self.x_actual)
        self.entry_x_actual.configure(justify="center")
        self.entry_y_actual = ctk.CTkEntry(self.tabview_position.tab("Positions"), width=70, state="disabled",
                                           font=ctk.CTkFont(size=20), fg_color="transparent",
                                           textvariable=self.y_actual)
        self.entry_y_actual.configure(justify="center")
        self.entry_z_actual = ctk.CTkEntry(self.tabview_position.tab("Positions"), width=70, state="disabled",
                                           font=ctk.CTkFont(size=20), fg_color="transparent",
                                           textvariable=self.z_actual)
        self.entry_z_actual.configure(justify="center")

        # -- controls buttons
        self.button_move_x = ctk.CTkButton(self.tabview_position.tab("Positions"), text='Move', width=70,
                                           border_width=2, hover_color="dark green", fg_color="forest green",
                                           text_color=("gray10", "#DCE4EE"), font=ctk.CTkFont(size=18),
                                           command=lambda: self.move_axis("X", self.entry_x_target.get(),
                                                                          self.x_limit_fwd, self.x_limit_rev))
        self.button_set_x = ctk.CTkButton(self.tabview_position.tab("Positions"), text='Set', width=70,
                                          border_width=2, text_color=("gray10", "#DCE4EE"),
                                          font=ctk.CTkFont(size=18),
                                          command=lambda: self.set_axis("X", self.entry_x_target.get()))
        self.button_move_y = ctk.CTkButton(self.tabview_position.tab("Positions"), text='Move', width=70,
                                           border_width=2, hover_color="dark green", fg_color="forest green",
                                           text_color=("gray10", "#DCE4EE"), font=ctk.CTkFont(size=18),
                                           command=lambda: self.move_axis("Y", self.entry_y_target.get(),
                                                                          self.y_limit_fwd, self.y_limit_rev))
        self.button_set_y = ctk.CTkButton(self.tabview_position.tab("Positions"), text='Set', width=70,
                                          border_width=2, text_color=("gray10", "#DCE4EE"),
                                          font=ctk.CTkFont(size=18),
                                          command=lambda: self.set_axis("Y", self.entry_y_target.get()))
        self.button_move_z = ctk.CTkButton(self.tabview_position.tab("Positions"), text='Move', width=70,
                                           border_width=2, hover_color="dark green", fg_color="forest green",
                                           text_color=("gray10", "#DCE4EE"), font=ctk.CTkFont(size=18),
                                           command=lambda: self.move_axis("Z", self.entry_z_target.get(),
                                                                          self.z_limit_fwd, self.z_limit_rev))
        self.button_set_z = ctk.CTkButton(self.tabview_position.tab("Positions"), text='Set', width=70,
                                          border_width=2, text_color=("gray10", "#DCE4EE"),
                                          font=ctk.CTkFont(size=18),
                                          command=lambda: self.set_axis("Z", self.entry_z_target.get()))

        # -- controls widgets positioning
        self.label_position.grid(row=0, column=0, columnspan=5, pady=(10, 0), sticky="nsew")
        self.label_target.grid(row=1, column=1, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.label_actual.grid(row=1, column=2, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.label_x.grid(row=2, column=0, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.entry_x_target.grid(row=2, column=1, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.entry_x_actual.grid(row=2, column=2, padx=(4, 0), pady=(5, 0), sticky="nsew")
        self.button_move_x.grid(row=2, column=3, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.button_set_x.grid(row=2, column=4, padx=(5, 10), pady=(5, 0), sticky="nsew")
        self.label_y.grid(row=3, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.entry_y_target.grid(row=3, column=1, padx=(5, 0), pady=(10, 0), sticky="nsew")
        self.entry_y_actual.grid(row=3, column=2, padx=(4, 0), pady=(10, 0), sticky="nsew")
        self.button_move_y.grid(row=3, column=3, padx=(5, 0), pady=(10, 0), sticky="nsew")
        self.button_set_y.grid(row=3, column=4, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.label_z.grid(row=4, column=0, padx=(10, 0), pady=(10, 5), sticky="nsew")
        self.entry_z_target.grid(row=4, column=1, padx=(5, 0), pady=(10, 5), sticky="nsew")
        self.entry_z_actual.grid(row=4, column=2, padx=(4, 0), pady=(10, 5), sticky="nsew")
        self.button_move_z.grid(row=4, column=3, padx=(5, 0), pady=(10, 5), sticky="nsew")
        self.button_set_z.grid(row=4, column=4, padx=(5, 10), pady=(10, 5), sticky="nsew")

        # - SOFTWARE LIMITS CONTROLS
        # -- create frame for software limits
        self.tabview_position.add("Limits")

        # -- limits database values entry defaults
        self.x_limit_fwd = tk.IntVar()
        self.x_limit_fwd.set(mwt_dict['x_fwd_limit'])
        self.x_limit_rev = tk.IntVar()
        self.x_limit_rev.set(mwt_dict['x_rev_limit'])
        self.y_limit_fwd = tk.IntVar()
        self.y_limit_fwd.set(mwt_dict['y_fwd_limit'])
        self.y_limit_rev = tk.IntVar()
        self.y_limit_rev.set(mwt_dict['y_rev_limit'])
        self.z_limit_fwd = tk.IntVar()
        self.z_limit_fwd.set(mwt_dict['z_fwd_limit'])
        self.z_limit_rev = tk.IntVar()
        self.z_limit_rev.set(mwt_dict['z_rev_limit'])
        self.checkbox_unlock_limits_status = IntVar()

        # -- limits labels
        self.label_limits = ctk.CTkLabel(self.tabview_position.tab("Limits"), text="Software Limits", anchor="center",
                                         font=ctk.CTkFont(size=16, weight="bold"))
        self.label_fwd = ctk.CTkLabel(self.tabview_position.tab("Limits"), text="Forward", anchor="center")
        self.label_rev = ctk.CTkLabel(self.tabview_position.tab("Limits"), text="Reverse", anchor="center")
        self.label_x_limits = ctk.CTkLabel(self.tabview_position.tab("Limits"), text="X", anchor="center")
        self.label_y_limits = ctk.CTkLabel(self.tabview_position.tab("Limits"), text="Y", anchor="center")
        self.label_z_limits = ctk.CTkLabel(self.tabview_position.tab("Limits"), text="Z", anchor="center")

        # -- limits entry fields
        self.entry_x_limit_fwd = ctk.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                              textvariable=self.x_limit_fwd)
        self.entry_x_limit_fwd.configure(justify="center")
        self.entry_x_limit_rev = ctk.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                              textvariable=self.x_limit_rev)
        self.entry_x_limit_rev.configure(justify="center")
        self.entry_y_limit_fwd = ctk.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                              textvariable=self.y_limit_fwd)
        self.entry_y_limit_fwd.configure(justify="center")
        self.entry_y_limit_rev = ctk.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                              textvariable=self.y_limit_rev)
        self.entry_y_limit_rev.configure(justify="center")
        self.entry_z_limit_fwd = ctk.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                              textvariable=self.z_limit_fwd)
        self.entry_z_limit_fwd.configure(justify="center")
        self.entry_z_limit_rev = ctk.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                              textvariable=self.z_limit_rev)
        self.entry_z_limit_rev.configure(justify="center")

        # -- limits buttons and checkbox
        self.checkbox_unlock_limits = ctk.CTkCheckBox(self.tabview_position.tab("Limits"), text="", onvalue=1,
                                                      offvalue=0, variable=self.checkbox_unlock_limits_status,
                                                      command=self.enable_button_set_limits)
        self.button_set_limits = ctk.CTkButton(self.tabview_position.tab("Limits"), text='Set All', width=15,
                                               border_width=2, fg_color="transparent", text_color=("gray10", "#DCE4EE"),
                                               state="disabled", command=self.set_limits)
        self.button_recall_limits = ctk.CTkButton(self.tabview_position.tab("Limits"), text='Recall LMT', width=20,
                                                  border_width=2, fg_color="transparent",
                                                  text_color=("gray10", "#DCE4EE"), command=self.recall_limits)

        # -- limits widgets positioning
        self.label_limits.grid(row=0, column=0, columnspan=4, padx=0, pady=(10, 0), sticky="nsew")
        self.label_fwd.grid(row=1, column=1, padx=0, pady=(10, 0), sticky="nsew")
        self.label_rev.grid(row=1, column=2, padx=0, pady=(10, 0), sticky="nsew")
        self.label_x_limits.grid(row=2, column=0, padx=(33, 0), pady=(5, 0), sticky="e")
        self.label_y_limits.grid(row=3, column=0, padx=(33, 0), pady=(10, 0), sticky="e")
        self.label_z_limits.grid(row=4, column=0, padx=(33, 0), pady=(10, 5), sticky="e")
        self.entry_x_limit_fwd.grid(row=2, column=1, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_x_limit_rev.grid(row=2, column=2, padx=(5, 10), pady=(5, 0), sticky="nsew")
        self.entry_y_limit_fwd.grid(row=3, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_y_limit_rev.grid(row=3, column=2, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.entry_z_limit_fwd.grid(row=4, column=1, padx=5, pady=(10, 5), sticky="nsew")
        self.entry_z_limit_rev.grid(row=4, column=2, padx=(5, 10), pady=(10, 5), sticky="nsew")
        self.checkbox_unlock_limits.grid(row=2, column=3, padx=(10, 0), pady=(5, 0), sticky="w")
        self.button_set_limits.grid(row=2, column=3, padx=(0, 26), pady=(5, 0), sticky="e")
        self.button_recall_limits.grid(row=3, column=3, columnspan=2, padx=(10, 33.5), pady=(10, 0), sticky="nsew")

        # CARRIAGE ATTRIBUTES
        # - CARRIAGE ATTRIBUTES (SP, AC, DC)
        # -- create tab/frame for attribute controls (SP: speed, AC: acceleration, DC: deceleration)
        self.tabview_position.add("SP, AC, DC")

        # -- attribute entry defaults (SP, AC, DC)
        self.speed_x = tk.IntVar()
        self.speed_x.set(mwt_dict['sp_x'])
        self.speed_y = tk.IntVar()
        self.speed_y.set(mwt_dict['sp_y'])
        self.speed_z = tk.IntVar()
        self.speed_z.set(mwt_dict['sp_z'])
        self.accel_x = tk.IntVar()
        self.accel_x.set(mwt_dict['ac_x'])
        self.accel_y = tk.IntVar()
        self.accel_y.set(mwt_dict['ac_y'])
        self.accel_z = tk.IntVar()
        self.accel_z.set(mwt_dict['ac_z'])
        self.decel_x = tk.IntVar()
        self.decel_x.set(mwt_dict['dc_x'])
        self.decel_y = tk.IntVar()
        self.decel_y.set(mwt_dict['dc_y'])
        self.decel_z = tk.IntVar()
        self.decel_z.set(mwt_dict['dc_z'])
        self.checkbox_unlock_SAD_status = IntVar()

        # -- attribute labels (SP, AC, DC)
        self.label_sp_ac_dc = ctk.CTkLabel(self.tabview_position.tab("SP, AC, DC"), anchor="center",
                                           text="Speed, Acceleration, Deceleration",
                                           font=ctk.CTkFont(size=16, weight="bold"))
        self.label_speed = ctk.CTkLabel(self.tabview_position.tab("SP, AC, DC"), text="SP", anchor="center")
        self.label_accel = ctk.CTkLabel(self.tabview_position.tab("SP, AC, DC"), text="AC", anchor="center")
        self.label_decel = ctk.CTkLabel(self.tabview_position.tab("SP, AC, DC"), text="DC", anchor="center")
        self.label_SAD_x = ctk.CTkLabel(self.tabview_position.tab("SP, AC, DC"), text="X", anchor="center")
        self.label_SAD_y = ctk.CTkLabel(self.tabview_position.tab("SP, AC, DC"), text="Y", anchor="center")
        self.label_SAD_z = ctk.CTkLabel(self.tabview_position.tab("SP, AC, DC"), text="Z", anchor="center")

        # -- attribute entry fields (SP, AC, DC)
        self.entry_speed_x = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.speed_x)
        self.entry_speed_x.configure(justify="center")
        self.entry_speed_y = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.speed_y)
        self.entry_speed_y.configure(justify="center")
        self.entry_speed_z = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.speed_z)
        self.entry_speed_z.configure(justify="center")
        self.entry_accel_x = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.accel_x)
        self.entry_accel_x.configure(justify="center")
        self.entry_accel_y = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.accel_y)
        self.entry_accel_y.configure(justify="center")
        self.entry_accel_z = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.accel_z)
        self.entry_accel_z.configure(justify="center")
        self.entry_decel_x = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.decel_x)
        self.entry_decel_x.configure(justify="center")
        self.entry_decel_y = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.decel_y)
        self.entry_decel_y.configure(justify="center")
        self.entry_decel_z = ctk.CTkEntry(self.tabview_position.tab("SP, AC, DC"), width=50,
                                          textvariable=self.decel_z)
        self.entry_decel_z.configure(justify="center")

        # -- attribute buttons and checkboxes (SP, AC, DC)
        self.checkbox_unlock_SAD = ctk.CTkCheckBox(self.tabview_position.tab("SP, AC, DC"), onvalue=1, offvalue=0,
                                                   text="", variable=self.checkbox_unlock_SAD_status,
                                                   command=self.enable_button_set_SAD)
        self.button_set_SAD = ctk.CTkButton(self.tabview_position.tab("SP, AC, DC"), width=10, border_width=2,
                                            text='Set All', fg_color="transparent", text_color=("gray10", "#DCE4EE"),
                                            state="disabled", command=self.set_SAD)
        self.button_recall_SAD = ctk.CTkButton(self.tabview_position.tab("SP, AC, DC"),  width=20, border_width=2,
                                               text='Recall SAD', fg_color="transparent",
                                               text_color=("gray10", "#DCE4EE"), command=self.recall_SAD)

        # -- attribute widgets positioning (SP, AC, DC)
        self.label_sp_ac_dc.grid(row=0, column=0, columnspan=6, padx=0, pady=(10, 0), sticky="nsew")
        self.label_speed.grid(row=1, column=1, padx=0, pady=(10, 0), sticky="nsew")
        self.label_accel.grid(row=1, column=2, padx=0, pady=(10, 0), sticky="nsew")
        self.label_decel.grid(row=1, column=3, padx=0, pady=(10, 0), sticky="nsew")
        self.label_SAD_x.grid(row=2, column=0, padx=(25, 0), pady=(5, 0), sticky="e")
        self.label_SAD_y.grid(row=3, column=0, padx=(25, 0), pady=(10, 0), sticky="e")
        self.label_SAD_z.grid(row=4, column=0, padx=(25, 0), pady=(10, 0), sticky="e")
        self.entry_speed_x.grid(row=2, column=1, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_accel_x.grid(row=2, column=2, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_decel_x.grid(row=2, column=3, padx=(5, 10), pady=(5, 0), sticky="nsew")
        self.entry_speed_y.grid(row=3, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_accel_y.grid(row=3, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_decel_y.grid(row=3, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.entry_speed_z.grid(row=4, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_accel_z.grid(row=4, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_decel_z.grid(row=4, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.checkbox_unlock_SAD.grid(row=2, column=4, padx=(10, 0), pady=(5, 0), sticky="w")
        self.button_set_SAD.grid(row=2, column=4, padx=(0, 20), pady=(5, 0), sticky="e")
        self.button_recall_SAD.grid(row=3, column=4, columnspan=2, padx=(10, 20), pady=(10, 0), sticky="nsew")

        # - CARRIAGE ATTRIBUTES (KP, KI, KD)
        # -- create tab/frame for attribute controls (KP: proportional, KI: integral, KD: derivative)
        self.tabview_position.add("KP, KI, KD")

        # -- attribute entry defaults (KP, KI, KD)
        self.kp_x = tk.IntVar()
        self.kp_x.set(mwt_dict['kp_x'])
        self.kp_y = tk.IntVar()
        self.kp_y.set(mwt_dict['kp_y'])
        self.kp_z = tk.IntVar()
        self.kp_z.set(mwt_dict['kp_z'])
        self.ki_x = tk.DoubleVar()
        self.ki_x.set(mwt_dict['ki_x'])
        self.ki_y = tk.DoubleVar()
        self.ki_y.set(mwt_dict['ki_y'])
        self.ki_z = tk.DoubleVar()
        self.ki_z.set(mwt_dict['ki_z'])
        self.kd_x = tk.IntVar()
        self.kd_x.set(mwt_dict['kd_x'])
        self.kd_y = tk.IntVar()
        self.kd_y.set(mwt_dict['kd_y'])
        self.kd_z = tk.IntVar()
        self.kd_z.set(mwt_dict['kd_z'])
        self.checkbox_unlock_PID_status = IntVar()

        # -- attribute labels (KP, KI, KD)
        self.label_kp_ki_kd = ctk.CTkLabel(self.tabview_position.tab("KP, KI, KD"), anchor="center",
                                           text="Proportional, Integral, Derivative",
                                           font=ctk.CTkFont(size=16, weight="bold"))
        self.label_kp = ctk.CTkLabel(self.tabview_position.tab("KP, KI, KD"), text="KP", anchor="center")
        self.label_ki = ctk.CTkLabel(self.tabview_position.tab("KP, KI, KD"), text="KI", anchor="center")
        self.label_kd = ctk.CTkLabel(self.tabview_position.tab("KP, KI, KD"), text="KD", anchor="center")
        self.label_PID_x = ctk.CTkLabel(self.tabview_position.tab("KP, KI, KD"), text="X", anchor="center")
        self.label_PID_y = ctk.CTkLabel(self.tabview_position.tab("KP, KI, KD"), text="Y", anchor="center")
        self.label_PID_z = ctk.CTkLabel(self.tabview_position.tab("KP, KI, KD"), text="Z", anchor="center")

        # -- attribute entry fields (KP, KI, KD)
        self.entry_kp_x = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.kp_x)
        self.entry_kp_x.configure(justify="center")
        self.entry_kp_y = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.kp_y)
        self.entry_kp_y.configure(justify="center")
        self.entry_kp_z = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.kp_z)
        self.entry_kp_z.configure(justify="center")
        self.entry_ki_x = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.ki_x)
        self.entry_ki_x.configure(justify="center")
        self.entry_ki_y = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.ki_y)
        self.entry_ki_y.configure(justify="center")
        self.entry_ki_z = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.ki_z)
        self.entry_ki_z.configure(justify="center")
        self.entry_kd_x = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.kd_x)
        self.entry_kd_x.configure(justify="center")
        self.entry_kd_y = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.kd_y)
        self.entry_kd_y.configure(justify="center")
        self.entry_kd_z = ctk.CTkEntry(self.tabview_position.tab("KP, KI, KD"), width=50, textvariable=self.kd_z)
        self.entry_kd_z.configure(justify="center")

        # -- attribute buttons (KP, KI, KD)
        self.checkbox_unlock_PID = ctk.CTkCheckBox(self.tabview_position.tab("KP, KI, KD"), onvalue=1, offvalue=0,
                                                   text="", variable=self.checkbox_unlock_PID_status,
                                                   command=self.enable_button_set_PID)
        self.button_set_PID = ctk.CTkButton(self.tabview_position.tab("KP, KI, KD"), width=10, border_width=2,
                                            text='Set All', fg_color="transparent", text_color=("gray10", "#DCE4EE"),
                                            state="disabled", command=self.set_PID)
        self.button_recall_PID = ctk.CTkButton(self.tabview_position.tab("KP, KI, KD"), width=20, border_width=2,
                                               text='Recall PID', fg_color="transparent",
                                               text_color=("gray10", "#DCE4EE"), command=self.recall_PID)

        # -- attribute widgets positioning (KP, KI, KD)
        self.label_kp_ki_kd.grid(row=0, column=0, columnspan=6, padx=0, pady=(10, 0), sticky="nsew")
        self.label_kp.grid(row=1, column=1, padx=0, pady=(10, 0), sticky="nsew")
        self.label_ki.grid(row=1, column=2, padx=0, pady=(10, 0), sticky="nsew")
        self.label_kd.grid(row=1, column=3, padx=0, pady=(10, 0), sticky="nsew")
        self.label_PID_x.grid(row=2, column=0, padx=(25, 0), pady=(5, 0), sticky="e")
        self.label_PID_y.grid(row=3, column=0, padx=(25, 0), pady=(10, 0), sticky="e")
        self.label_PID_z.grid(row=4, column=0, padx=(25, 0), pady=(10, 0), sticky="e")
        self.entry_kp_x.grid(row=2, column=1, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_ki_x.grid(row=2, column=2, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_kd_x.grid(row=2, column=3, padx=(5, 10), pady=(5, 0), sticky="nsew")
        self.entry_kp_y.grid(row=3, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_ki_y.grid(row=3, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_kd_y.grid(row=3, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.entry_kp_z.grid(row=4, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_ki_z.grid(row=4, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_kd_z.grid(row=4, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.checkbox_unlock_PID.grid(row=2, column=4, padx=(10, 0), pady=(5, 0), sticky="w")
        self.button_set_PID.grid(row=2, column=4, padx=(0, 20), pady=(5, 0), sticky="e")
        self.button_recall_PID.grid(row=3, column=4, columnspan=2, padx=(10, 20), pady=(10, 0), sticky="nsew")

        # CARRIAGE STATUS CODES AND APPEARANCE CONFIG
        # -- create frame for status codes and GUI appearance config
        self.tabview_config = ctk.CTkTabview(self)
        self.tabview_config.grid(row=2, column=0, padx=5, sticky="nsew")

        # - CARRIAGE STATUS CODES
        # -- create tab/frame for status codes
        self.tabview_config.add("Status")

        # -- status codes database values entry defaults
        self.x_status_code = tk.IntVar()
        self.x_status_code.set(mwt_dict['x_stop_code'])
        self.y_status_code = tk.IntVar()
        self.y_status_code.set(mwt_dict['y_stop_code'])
        self.z_status_code = tk.IntVar()
        self.z_status_code.set(mwt_dict['z_stop_code'])
        self.status_codes = tk.StringVar()
        self.status_codes.set(f"{self.x_status_code.get()}, {self.y_status_code.get()}, {self.z_status_code.get()}")

        # -- status codes entries
        self.entry_status_codes = ctk.CTkEntry(self.tabview_config.tab("Status"), width=50, state="disabled",
                                               font=ctk.CTkFont(size=12), fg_color="transparent",
                                               textvariable=self.status_codes)
        self.entry_status_codes.configure(justify="center")

        # -- status codes labels
        self.label_status_title = ctk.CTkLabel(self.tabview_config.tab("Status"), anchor="center", text="Status",
                                               font=ctk.CTkFont(size=16, weight="bold"))
        self.label_status_terms = ctk.CTkLabel(self.tabview_config.tab("Status"),
                                               text="0 - motors are running\n1 - motors stopped at commanded position\n"
                                                    "2 - motors stopped by forward hard/software limit\n3 - motors "
                                                    "stopped by reverse hard/software limit\n7 - motors stopped after "
                                                    "abort command")
        # 0 - Motors are running, independent mode
        # 1 - Motors decelerating or stopped at commanded independent position
        # 2 - Decelerating or stopped by FWD limit switch or soft limit FL
        # 3 - Decelerating or stopped by REV limit switch or soft limit BL
        # 4 - Decelerating or stopped by Stop Command (ST)
        # 6 - Stopped by Abort input
        # 7 - Stopped by Abort command (AB)
        # 8 - Decelerating or stopped by Off-on-Error (OE1)
        # 9 - Stopped after Finding Edge (FE)
        # 10 - Stopped after Homing (HM)
        # 11 - Stopped by Selective Abort Input
        # 16 - Stepper Position Maintenance Mode Error
        # 50 - Contour running
        # 51 - Contour Stop
        # 99 - MC timeout
        # 100 - Motors are running, vector sequence
        # 101 - Motors stopped at commanded vector

        # -- status codes widgets positioning
        self.label_status_title.grid(row=0, column=0, padx=(25, 0), pady=(10, 0), sticky="nsew")
        self.entry_status_codes.grid(row=1, column=0, padx=(25, 0), pady=(10, 0), sticky="nsew")
        self.label_status_terms.grid(row=2, column=0, padx=(25, 0), pady=(10, 0), sticky="n")

        # - GUI APPEARANCE CONFIG
        # -- create tab/frame for GUI appearance config
        self.tabview_config.add("UI")

        # -- UI label fields
        self.label_appearance = ctk.CTkLabel(self.tabview_config.tab("UI"), text="Appearance Mode:", anchor="center")
        self.label_scaling = ctk.CTkLabel(self.tabview_config.tab("UI"), text="UI Scaling:", anchor="center")

        # -- UI menus
        self.menu_appearance = ctk.CTkOptionMenu(self.tabview_config.tab("UI"), values=["Light", "Dark", "System"],
                                                 command=self.change_appearance_mode_event)
        self.menu_scaling = ctk.CTkOptionMenu(self.tabview_config.tab("UI"),
                                              values=["80%", "90%", "100%", "110%", "120%"],
                                              command=self.change_scaling_event)

        # -- UI theme default values
        self.menu_appearance.set("System")
        self.menu_scaling.set("100%")

        # -- UI widgets positioning
        self.label_appearance.grid(row=0, column=0, padx=(15, 0), pady=(0, 0))
        self.label_scaling.grid(row=0, column=1, padx=(15, 0), pady=(0, 0))
        self.menu_appearance.grid(row=1, column=0, padx=(15, 0), pady=(0, 0))
        self.menu_scaling.grid(row=1, column=1, padx=(15, 0), pady=(0, 0))

        # -- set buttons default values
        self.checkbox_unlock_limits_status.set(0)
        self.checkbox_unlock_SAD_status.set(0)
        self.checkbox_unlock_PID_status.set(0)
        self.button_set_limits.configure(state="disabled")
        self.button_set_SAD.configure(state="disabled")
        self.button_set_PID.configure(state="disabled")

        self.carriage_threading()

    # - GUI functions
    # -- change overall appearance of program to light, dark, or system
    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    # - carriage functions
    # -- stop carriage move execution and freeze actual position values
    def stop_carriage(self):
        c = galil.GCommand
        c('AB')
        del c
        self.write_log("Carriage stopped!")

    # -- close carriage connection and exit program window
    def quit_carriage(self):
        self.stop_carriage()
        print("Connection closing, goodbye!")
        galil.GClose()
        self.destroy()

    @staticmethod
    def connect_carriage():
        global status
        if status == "Connected":
            print(galil.GInfo())  # COM2, DMC2132 Rev 1.0n, 10483
        else:
            status = "Connected"
            print('gclib version:', galil.GVersion())  # prints installed gclib version
            galil.GOpen('COM2 --baud 19200')  # change to COM port used by carriage
            print(galil.GInfo())  # prints connection information for carriage

    # TODO: motion complete after target - position = 0?
    # -- update carriage positions and stop codes
    # noinspection PyTypeChecker
    def update_carriage(self):
        global mwt_dict
        c = galil.GCommand
        x_pos = float(c('TPA')) / 40
        x_pos_str = str(x_pos)
        x_pos_round_str = str("%.1f" % x_pos)
        y_pos = float(c('TPB')) / 40
        y_pos_str = str(y_pos)
        y_pos_round_str = str("%.1f" % y_pos)
        z_pos = float(c('TPC')) / 40
        z_pos_str = str(z_pos)
        z_pos_round_str = str("%.1f" % z_pos)
        x_sc = str(c('SCA'))
        y_sc = str(c('SCB'))
        z_sc = str(c('SCC'))
        self.x_actual.set(x_pos_round_str)
        self.y_actual.set(y_pos_round_str)
        self.z_actual.set(z_pos_round_str)
        self.status_codes.set(f"{x_sc}, {y_sc}, {z_sc}")
        mwt_dict |= {'x_actual': x_pos_str}
        mwt_dict |= {'y_actual': y_pos_str}
        mwt_dict |= {'z_actual': z_pos_str}
        mwt_dict |= {'x_stop_code': x_sc}
        mwt_dict |= {'y_stop_code': y_sc}
        mwt_dict |= {'z_stop_code': z_sc}
        self.csv_generate()
        self.after(10, self.update_carriage)
        # self.after(10, self.write_log("Carriage updated"))

    # -- create thread to constantly update carriage position and stop codes
    def carriage_threading(self):
        position_thread = Thread(target=self.update_carriage)
        position_thread.start()

    # -- move carriage to input position for axis
    # noinspection PyTypeChecker
    def move_axis(self, axis, move_target, axis_limit_fwd, axis_limit_rev):
        app.bind_all("<1>", lambda event: event.widget.focus_set())
        move_encoder = str(float(move_target) * 40)
        c = galil.GCommand
        if (float(axis_limit_rev.get()) > float(move_target) or
                float(move_target) > float(axis_limit_fwd.get())):
            self.write_log("Move is beyond limits!")
        elif axis == "X":
            self.x_target.set(float(move_target))
            self.write_log("Move initiated, target is X=" + move_target)
            c('PAA=' + str(move_encoder))
            c('BGA')
        elif axis == "Y":
            self.y_target.set(float(move_target))
            self.write_log("Move initiated, target is Y=" + move_target)
            c('PAB=' + str(move_encoder))
            c('BGB')
        elif axis == "Z":
            self.z_target.set(float(move_target))
            self.write_log("Move initiated, target is Z=" + move_target)
            c('PAC=' + str(move_encoder))
            c('BGC')
        else:
            self.write_log("Moving error!")
        del c

    # -- set axis position target value to actual value
    # noinspection PyTypeChecker
    def set_axis(self, axis, set_target):
        global mwt_dict
        c = galil.GCommand
        value_encoder = str(float(set_target) * 40)  # e.g. 40 encoder counts per mm (230*40=9200)
        if axis == "X":
            c('DPA=' + str(value_encoder))
            self.x_target.set(float(set_target))
            mwt_dict |= {'x_actual': set_target}
            self.write_log("X position is now: " + set_target)
        elif axis == "Y":
            c('DPB=' + str(value_encoder))
            self.y_target.set(float(set_target))
            mwt_dict |= {'y_actual': set_target}
            self.write_log("Y position is now: " + set_target)
        elif axis == "Z":
            c('DPC=' + str(value_encoder))
            self.z_target.set(float(set_target))
            mwt_dict |= {'z_actual': set_target}
            self.write_log("Z position is now: " + set_target)
        else:
            self.write_log("Set axis error!")
        del c
        self.csv_generate()

    # -- enables the set limits button if the adjacent checkbox is checked
    def enable_button_set_limits(self):
        self.button_set_limits.configure(state=NORMAL if self.checkbox_unlock_limits_status.get() == 1 else DISABLED)

    # -- takes user input for all limits entries and stores those values
    def set_limits(self):
        global mwt_dict
        c = galil.GCommand
        c('FLA=' + str(float(self.entry_x_limit_fwd.get()) * 40))
        c('BLA=' + str(float(self.entry_x_limit_rev.get()) * 40))
        c('FLB=' + str(float(self.entry_y_limit_fwd.get()) * 40))
        c('BLB=' + str(float(self.entry_y_limit_rev.get()) * 40))
        c('FLC=' + str(float(self.entry_z_limit_fwd.get()) * 40))
        c('BLC=' + str(float(self.entry_z_limit_rev.get()) * 40))
        self.x_limit_fwd.set(self.entry_x_limit_fwd.get())
        self.x_limit_fwd.set(self.entry_x_limit_fwd.get())
        self.x_limit_rev.set(self.entry_x_limit_rev.get())
        self.y_limit_fwd.set(self.entry_y_limit_fwd.get())
        self.y_limit_rev.set(self.entry_y_limit_rev.get())
        self.z_limit_fwd.set(self.entry_z_limit_fwd.get())
        self.z_limit_rev.set(self.entry_z_limit_rev.get())
        mwt_dict |= {'x_fwd_limit': self.x_limit_fwd.get()}
        mwt_dict |= {'x_rev_limit': self.x_limit_rev.get()}
        mwt_dict |= {'y_fwd_limit': self.y_limit_fwd.get()}
        mwt_dict |= {'y_rev_limit': self.y_limit_rev.get()}
        mwt_dict |= {'z_fwd_limit': self.z_limit_fwd.get()}
        mwt_dict |= {'z_rev_limit': self.z_limit_rev.get()}
        self.checkbox_unlock_limits_status.set(0)
        self.button_set_limits.configure(state="disabled")
        self.csv_generate()
        del c

    # -- enables the set SAD button if the adjacent checkbox is checked
    def enable_button_set_SAD(self):
        self.button_set_SAD.configure(state=NORMAL if self.checkbox_unlock_SAD_status.get() == 1 else DISABLED)

    # -- used to save all current speed, accel, decel carriage attributes
    def set_SAD(self):
        global mwt_dict
        c = galil.GCommand
        c('SPA=' + str(int(self.entry_speed_x.get())))
        c('SPB=' + str(int(self.entry_speed_y.get())))
        c('SPC=' + str(int(self.entry_speed_z.get())))
        c('ACA=' + str(int(self.entry_speed_x.get())))
        c('ACB=' + str(int(self.entry_speed_y.get())))
        c('ACC=' + str(int(self.entry_speed_z.get())))
        c('DCA=' + str(int(self.entry_speed_x.get())))
        c('DCB=' + str(int(self.entry_speed_y.get())))
        c('DCC=' + str(int(self.entry_speed_z.get())))
        self.speed_x.set(self.entry_speed_x.get())
        self.speed_y.set(self.entry_speed_y.get())
        self.speed_z.set(self.entry_speed_z.get())
        self.accel_x.set(self.entry_accel_x.get())
        self.accel_y.set(self.entry_accel_y.get())
        self.accel_z.set(self.entry_accel_z.get())
        self.decel_x.set(self.entry_decel_x.get())
        self.decel_y.set(self.entry_decel_y.get())
        self.decel_z.set(self.entry_decel_z.get())
        mwt_dict |= {'sp_x': self.speed_x.get()}
        mwt_dict |= {'sp_y': self.speed_y.get()}
        mwt_dict |= {'sp_z': self.speed_z.get()}
        mwt_dict |= {'ac_x': self.accel_x.get()}
        mwt_dict |= {'ac_y': self.accel_y.get()}
        mwt_dict |= {'ac_z': self.accel_z.get()}
        mwt_dict |= {'dc_x': self.decel_x.get()}
        mwt_dict |= {'dc_y': self.decel_y.get()}
        mwt_dict |= {'dc_z': self.decel_z.get()}
        self.checkbox_unlock_SAD_status.set(0)
        self.button_set_SAD.configure(state="disabled")
        self.csv_generate()
        del c

    # -- enables the set PID button if the adjacent checkbox is checked
    def enable_button_set_PID(self):
        self.button_set_PID.configure(state=NORMAL if self.checkbox_unlock_PID_status.get() == 1 else DISABLED)

    # -- used to save all current proportional, integral, derivative carriage attributes
    def set_PID(self):
        global mwt_dict
        c = galil.GCommand
        c('KPA=' + str(int(self.entry_kp_x.get())))
        c('KPB=' + str(float(self.entry_kp_y.get())))
        c('KPC=' + str(int(self.entry_kp_z.get())))
        c('KIA=' + str(int(self.entry_ki_x.get())))
        c('KIB=' + str(float(self.entry_ki_y.get())))
        c('KIC=' + str(int(self.entry_ki_z.get())))
        c('KDA=' + str(int(self.entry_kd_x.get())))
        c('KDB=' + str(float(self.entry_kd_y.get())))
        c('KDC=' + str(int(self.entry_kd_z.get())))
        self.kp_x.set(self.entry_kp_x.get())
        self.kp_y.set(self.entry_kp_y.get())
        self.kp_z.set(self.entry_kp_z.get())
        self.ki_x.set(self.entry_ki_x.get())
        self.ki_y.set(self.entry_ki_y.get())
        self.ki_z.set(self.entry_ki_z.get())
        self.kd_x.set(self.entry_kd_x.get())
        self.kd_y.set(self.entry_kd_y.get())
        self.kd_z.set(self.entry_kd_z.get())
        mwt_dict |= {'kp_x': self.kp_x.get()}
        mwt_dict |= {'kp_y': self.kp_y.get()}
        mwt_dict |= {'kp_z': self.kp_z.get()}
        mwt_dict |= {'ki_x': self.ki_x.get()}
        mwt_dict |= {'ki_y': self.ki_y.get()}
        mwt_dict |= {'ki_z': self.ki_z.get()}
        mwt_dict |= {'kd_x': self.kd_x.get()}
        mwt_dict |= {'kd_y': self.kd_y.get()}
        mwt_dict |= {'kd_z': self.kd_z.get()}
        self.checkbox_unlock_PID_status.set(0)
        self.button_set_PID.configure(state="disabled")
        self.csv_generate()
        del c

    # - csv functions
    # -- recalls saved limits from csv and outputs them in the log
    # noinspection PyTypeChecker
    def recall_limits(self):
        c = galil.GCommand
        x_fwd = (float(c('FLA=?')) / 40)
        x_rev = (float(c('BLA=?')) / 40)
        y_fwd = (float(c('FLB=?')) / 40)
        y_rev = (float(c('BLB=?')) / 40)
        z_fwd = (float(c('FLC=?')) / 40)
        z_rev = (float(c('BLC=?')) / 40)
        self.x_limit_fwd.set(x_fwd)
        self.x_limit_rev.set(x_rev)
        self.y_limit_fwd.set(y_fwd)
        self.y_limit_rev.set(y_rev)
        self.z_limit_fwd.set(z_fwd)
        self.z_limit_rev.set(z_rev)
        del c
        self.write_log("Limits recalled!")

    # -- recalls saved SAD values from csv and outputs them in the log
    # noinspection PyTypeChecker
    def recall_SAD(self):
        c = galil.GCommand
        x_sp = (int(c('SPA=?')))
        x_ac = (int(c('ACA=?')))
        x_dc = (int(c('DCA=?')))
        y_sp = (int(c('SPB=?')))
        y_ac = (int(c('ACB=?')))
        y_dc = (int(c('DCB=?')))
        z_sp = (int(c('SPC=?')))
        z_ac = (int(c('ACC=?')))
        z_dc = (int(c('DCC=?')))
        self.speed_x.set(x_sp)
        self.accel_x.set(x_ac)
        self.decel_x.set(x_dc)
        self.speed_y.set(y_sp)
        self.accel_y.set(y_ac)
        self.decel_y.set(y_dc)
        self.speed_z.set(z_sp)
        self.accel_z.set(z_ac)
        self.decel_z.set(z_dc)
        self.csv_recall()
        del c
        self.write_log("SAD attributes recalled!")

    # -- recalls saved PID values from csv and outputs them in the log
    # noinspection PyTypeChecker
    def recall_PID(self):
        c = galil.GCommand
        x_kp = (int(float(c('KPA=?'))))
        x_ki = (float(c('KIA=?')))
        x_kd = (int(float(c('KDA=?'))))
        y_kp = (int(float(c('KPB=?'))))
        y_ki = (float(c('KIB=?')))
        y_kd = (int(float(c('KDB=?'))))
        z_kp = (int(float(c('KPC=?'))))
        z_ki = (float(c('KIC=?')))
        z_kd = (int(float(c('KDC=?'))))
        self.kp_x.set(x_kp)
        self.ki_x.set(x_ki)
        self.kd_x.set(x_kd)
        self.kp_y.set(y_kp)
        self.ki_y.set(y_ki)
        self.kd_y.set(y_kd)
        self.kp_z.set(z_kp)
        self.ki_z.set(z_ki)
        self.kd_z.set(z_kd)
        self.csv_recall()
        del c
        self.write_log("PID attributes recalled!")

    # -- csv file that stores carriage values such as current position and movement limits
    @staticmethod
    def csv_generate():
        # with open('mwt_storage.csv', 'w', newline='') as csv_file:
        with open(filepath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in mwt_dict.items():
                writer.writerow([key, value])
        # self.checkbox_unlock_limits_status.set(0)
        # self.checkbox_unlock_SAD_status.set(0)
        # self.checkbox_unlock_PID_status.set(0)
        # self.button_set_limits.configure(state="disabled")
        # self.button_set_SAD.configure(state="disabled")
        # self.button_set_PID.configure(state="disabled")

    # TODO: is this necessary?
    # -- recalls saved limits from csv
    def csv_recall(self):
        global mwt_dict
        # with open("mwt_storage.csv", "r") as file:
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(','.join(row))
        self.write_log(mwt_dict)

    # - event log functions
    # -- used to print event descriptions or carriage status to the event log file
    @staticmethod
    def write_log(user_action):
        print(user_action)
        # with open('mwt_log.txt', 'w', newline='') as txt_file:
        #     txt_file.write(user_action)

    # [DEPRECATED FOR LOG FILE]
    # -- used to print event descriptions or carriage status to the GUI event log
    # def print_log(self, text):
    #     self.textbox_log.insert(tk.END, '\n')
    #     self.textbox_log.insert(tk.END, text)

    # [DEPRECATED FOR LOG FILE]
    # -- clears the program event log
    # def clear_log(self):
    #     self.textbox_log.delete("0.0", "end")
    #     self.textbox_log.insert("0.0", "Log cleared.")


if __name__ == "__main__":
    app = MoveCarriage()
    app.mainloop()
