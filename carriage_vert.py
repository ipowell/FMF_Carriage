# TODO: control sig figs & types
# TODO: connect move function
# TODO: connect emergency stop function
# TODO: connect limits to move function
# TODO: connect movement parameters to increase/decrease on focus
# TODO: [OPTIONAL] create 'home' sidebar button that moves in order of z, y, x or selected order
# TODO: [OPTIONAL] create 'set as home' sidebar button

import tkinter as tk  # allows import and use of tkinter modules
from tkinter import *  # imports all of tkinter's modules
import customtkinter  # custom, pre-made theming applied to tkinter GUI's based on Windows 11
import csv  # package for reading and writing to CSV (comma separated values) files
import warnings  # package to supress warnings that do not affect program functions
import gclib  # package by Galil Motion to view, control, and otherwise interact with the carriage motion controls
from varname import argname, UsingExecWarning  # package to use an argument's name as a reference

# suppresses warning from using argname in the move_axis and set_axis functions
warnings.filterwarnings("ignore", category=UsingExecWarning)

# default themes for the program
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

mwt_storage_reader = csv.reader(open('mwt_storage.csv', 'r'))
mwt_dict = {}
for mwt_storage_row in mwt_storage_reader:
    k, v = mwt_storage_row
    mwt_dict[k] = v
print(mwt_dict)


class MoveCarriage(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        galil = gclib.GalilCommands()
        print('gclib version:', galil.GVersion())
        # self.print_to_log(galil.GVersion())

        # try:
        #     # - galil motion controller init and connection
        #     # -- make an instance of the gclib python class
        #     galil = gclib.GalilCommands()
        #     print('gclib version:', galil.GVersion())
        #     # self.print_to_log(galil.GVersion())
        #
        #     # -- connect
        #     # galil.GOpen('192.168.0.42 -s ALL')
        #     galil.GOpen('COM1')
        #     print(galil.GInfo())
        #
        # # - Misc
        # # -- Motion Complete
        # print('Motion Complete')
        # galil_command = galil.GCommand  # alias the command callable
        # galil_command('AB')  # abort motion and program
        # galil_command('MO')  # turn off all motors
        # galil_command('SHA')  # servo A
        # galil_command('SPA=1000')  # speed, 1000 cts/sec
        # galil_command('PRA=3000')  # relative move, 3000 cts
        # print(' Starting move...')
        # galil_command('BGA')  # begin motion
        # galil.GMotionComplete('A')
        # print(' done.')
        # del galil_command  # delete the alias
        #
        # # -- exception handler
        # except gclib.GclibError as galil_error:
        # print('Unexpected GclibError:', galil_error)
        #
        # finally:
        #     galil.GClose('COM1')
        #
        # return

        # - configure gui
        # -- configure window
        self.title("carriage_vert")
        self.geometry(f"{360}x{880}")
        self.resizable(False, False)

        # -- configure grid layout (4x2)
        self.grid_columnconfigure(0, weight=5)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=7)

        # - left sidebar widgets
        # -- create frame for left sidebar widgets
        self.frame_sidebar = customtkinter.CTkFrame(self)
        self.frame_sidebar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        # self.frame_sidebar.grid_rowconfigure(4, weight=1)

        # -- left sidebar labels
        self.label_logo = customtkinter.CTkLabel(self.frame_sidebar, text="MWT Carriage Controls",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_version = customtkinter.CTkLabel(self.frame_sidebar, text="Version 20230914 ",
                                                    font=customtkinter.CTkFont(size=12, slant="italic"))
        self.label_appearance = customtkinter.CTkLabel(self.frame_sidebar, text="Appearance Mode:", anchor="w")
        # self.scaling_label = customtkinter.CTkLabel(self.frame_sidebar, text="UI Scaling:", anchor="w")

        # -- left sidebar buttons
        self.button_stop = customtkinter.CTkButton(self.frame_sidebar, text="Stop Carriage",
                                                   hover_color="dark red", fg_color="red", command=self.stop_carriage)
        # self.button_home = customtkinter.CTkButton(self.frame_sidebar, text='Move Home', command=self.move_home)
        # self.button_restore = customtkinter.CTkButton(self.frame_sidebar, text='Restore Positions',
        #                                               command=self.restore_positions)

        # -- left sidebar menus
        self.menu_appearance = customtkinter.CTkOptionMenu(self.frame_sidebar, values=["Light", "Dark", "System"],
                                                           command=self.change_appearance_mode_event)
        # self.menu_scaling = customtkinter.CTkOptionMenu(self.frame_sidebar, values=["75%", "100%", "125%"],
        #                                                 command=self.change_scaling_event)

        # -- left sidebar widget positioning
        self.label_logo.grid(row=0, column=0, columnspan=2, padx=(30, 0), pady=(10, 0))
        self.label_version.grid(row=1, column=0, columnspan=2, padx=(30, 0), sticky="n")
        self.button_stop.grid(row=3, column=0, padx=(30, 0), pady=(0, 10))
        # self.button_start.grid(row=2, column=0, padx=20, pady=10)
        # self.button_restore.grid(row=4, column=0, padx=20, pady=10)
        # self.button_home.grid(row=3, column=1, padx=(10, 0), pady=(0, 5))
        self.label_appearance.grid(row=2, column=1, padx=(11, 0), pady=(0, 0), sticky="s")
        # self.label_scaling.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.menu_appearance.grid(row=3, column=1, padx=(11, 0), pady=(0, 5), sticky="n")
        # self.menu_scaling.grid(row=9, column=0, padx=20, pady=(10, 20))

        # - carriage position controls
        # -- create frame for carriage position controls
        self.tabview_position = customtkinter.CTkTabview(self)
        self.tabview_position.grid(row=1, column=0, columnspan=2, padx=5, sticky="nsew")
        self.tabview_position.add("Positions")

        # -- controls entry defaults
        global mwt_dict
        self.entry_x_target_stored = tk.DoubleVar()
        self.entry_x_target_stored.set(mwt_dict['x_target'])
        self.entry_x_actual_stored = tk.DoubleVar()
        self.entry_x_actual_stored.set(mwt_dict['x_actual'])
        self.entry_y_target_stored = tk.DoubleVar()
        self.entry_y_target_stored.set(mwt_dict['y_target'])
        self.entry_y_actual_stored = tk.DoubleVar()
        self.entry_y_actual_stored.set(mwt_dict['y_actual'])
        self.entry_z_target_stored = tk.DoubleVar()
        self.entry_z_target_stored.set(mwt_dict['z_target'])
        self.entry_z_actual_stored = tk.DoubleVar()
        self.entry_z_actual_stored.set(mwt_dict['z_actual'])

        # -- controls labels
        self.label_carriage_position = customtkinter.CTkLabel(self.tabview_position.tab("Positions"),
                                                              text="Carriage Position", anchor="center",
                                                              font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label_target = customtkinter.CTkLabel(self.tabview_position.tab("Positions"), text="Target",
                                                   anchor="center")
        self.label_actual = customtkinter.CTkLabel(self.tabview_position.tab("Positions"), text="Actual",
                                                   anchor="center")
        self.label_x = customtkinter.CTkLabel(self.tabview_position.tab("Positions"), text="X", anchor="w")
        self.label_y = customtkinter.CTkLabel(self.tabview_position.tab("Positions"), text="Y", anchor="w")
        self.label_z = customtkinter.CTkLabel(self.tabview_position.tab("Positions"), text="Z", anchor="w")

        # -- controls entry fields
        self.entry_x_target = customtkinter.CTkEntry(self.tabview_position.tab("Positions"), width=70,
                                                     textvariable=self.entry_x_target_stored)
        self.entry_x_target.configure(justify="center")
        self.entry_x_actual = customtkinter.CTkEntry(self.tabview_position.tab("Positions"), state="disabled", width=70,
                                                     font=customtkinter.CTkFont(size=12, slant="italic"),
                                                     textvariable=self.entry_x_actual_stored)
        self.entry_x_actual.configure(justify="center")
        self.entry_x_target.bind("<Return>", lambda _: self.move_axis(self, self.entry_x_target_stored,
                                                                      self.entry_x_limit_fwd_stored,
                                                                      self.entry_x_limit_rev_stored))
        self.entry_y_target = customtkinter.CTkEntry(self.tabview_position.tab("Positions"), width=70,
                                                     textvariable=self.entry_y_target_stored)
        self.entry_y_target.configure(justify="center")
        self.entry_y_actual = customtkinter.CTkEntry(self.tabview_position.tab("Positions"), state="disabled", width=70,
                                                     font=customtkinter.CTkFont(size=12, slant="italic"),
                                                     textvariable=self.entry_y_actual_stored)
        self.entry_y_actual.configure(justify="center")
        self.entry_y_target.bind("<Return>", lambda _: self.move_axis(self, self.entry_y_target_stored,
                                                                      self.entry_y_limit_fwd_stored,
                                                                      self.entry_y_limit_rev_stored))
        self.entry_z_target = customtkinter.CTkEntry(self.tabview_position.tab("Positions"), width=70,
                                                     textvariable=self.entry_z_target_stored)
        self.entry_z_target.configure(justify="center")
        self.entry_z_actual = customtkinter.CTkEntry(self.tabview_position.tab("Positions"), state="disabled", width=70,
                                                     font=customtkinter.CTkFont(size=12, slant="italic"),
                                                     textvariable=self.entry_z_actual_stored)
        self.entry_z_actual.configure(justify="center")
        self.entry_z_target.bind("<Return>", lambda _: self.move_axis(self, self.entry_z_target_stored,
                                                                      self.entry_z_limit_fwd_stored,
                                                                      self.entry_z_limit_rev_stored))

        # -- controls buttons
        self.button_move_x = customtkinter.CTkButton(self.tabview_position.tab("Positions"), text='Move',
                                                     hover_color="dark green", fg_color="forest green", border_width=2,
                                                     width=70, text_color=("gray10", "#DCE4EE"),
                                                     command=lambda: self.move_axis(self, self.entry_x_target_stored,
                                                                                    self.entry_x_limit_fwd_stored,
                                                                                    self.entry_x_limit_rev_stored))
        self.button_set_x = customtkinter.CTkButton(self.tabview_position.tab("Positions"), text='Set Axis',
                                                    fg_color="transparent", border_width=2, width=70,
                                                    text_color=("gray10", "#DCE4EE"),
                                                    command=lambda: self.set_axis(self, self.entry_x_actual_stored,
                                                                                  self.entry_x_target_stored))
        self.button_move_y = customtkinter.CTkButton(self.tabview_position.tab("Positions"), text='Move',
                                                     hover_color="dark green", fg_color="forest green", border_width=2,
                                                     width=70, text_color=("gray10", "#DCE4EE"),
                                                     command=lambda: self.move_axis(self, self.entry_y_target_stored,
                                                                                    self.entry_y_limit_fwd_stored,
                                                                                    self.entry_y_limit_rev_stored))
        self.button_set_y = customtkinter.CTkButton(self.tabview_position.tab("Positions"), text='Set Axis',
                                                    fg_color="transparent", border_width=2, width=70,
                                                    text_color=("gray10", "#DCE4EE"),
                                                    command=lambda: self.set_axis(self, self.entry_y_actual_stored,
                                                                                  self.entry_y_target_stored))
        self.button_move_z = customtkinter.CTkButton(self.tabview_position.tab("Positions"), text='Move',
                                                     hover_color="dark green", fg_color="forest green", border_width=2,
                                                     width=70, text_color=("gray10", "#DCE4EE"),
                                                     command=lambda: self.move_axis(self, self.entry_z_target_stored,
                                                                                    self.entry_z_limit_fwd_stored,
                                                                                    self.entry_z_limit_rev_stored))
        self.button_set_z = customtkinter.CTkButton(self.tabview_position.tab("Positions"), text='Set Axis',
                                                    fg_color="transparent", border_width=2, width=70,
                                                    text_color=("gray10", "#DCE4EE"),
                                                    command=lambda: self.set_axis(self, self.entry_z_actual_stored,
                                                                                  self.entry_z_target_stored))

        # -- controls widgets positioning
        self.label_carriage_position.grid(row=0, column=0, columnspan=5, pady=(10, 0), sticky="nsew")
        self.label_target.grid(row=1, column=1, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.label_actual.grid(row=1, column=2, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.label_x.grid(row=2, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.label_y.grid(row=3, column=0, padx=(5, 0), pady=(10, 0), sticky="nsew")
        self.label_z.grid(row=4, column=0, padx=(5, 0), pady=(10, 5), sticky="nsew")
        self.entry_x_target.grid(row=2, column=1, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.entry_x_actual.grid(row=2, column=2, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.entry_y_target.grid(row=3, column=1, padx=(5, 0), pady=(10, 0), sticky="nsew")
        self.entry_y_actual.grid(row=3, column=2, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.entry_z_target.grid(row=4, column=1, padx=(5, 0), pady=(10, 5), sticky="nsew")
        self.entry_z_actual.grid(row=4, column=2, padx=(10, 0), pady=(10, 5), sticky="nsew")
        self.button_move_x.grid(row=2, column=3, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.button_set_x.grid(row=2, column=4, padx=(10, 10), pady=(5, 0), sticky="nsew")
        self.button_move_y.grid(row=3, column=3, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.button_set_y.grid(row=3, column=4, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.button_move_z.grid(row=4, column=3, padx=(10, 0), pady=(10, 5), sticky="nsew")
        self.button_set_z.grid(row=4, column=4, padx=(10, 10), pady=(10, 5), sticky="nsew")

        # - create software limits controls
        # -- create frame for software limits
        self.tabview_position.add("Limits")

        # -- limits entry defaults
        # global mwt_dict
        self.entry_x_limit_fwd_stored = tk.IntVar()
        self.entry_x_limit_fwd_stored.set(mwt_dict['x_fwd_limit'])
        self.entry_x_limit_rev_stored = tk.IntVar()
        self.entry_x_limit_rev_stored.set(mwt_dict['x_rev_limit'])
        self.entry_y_limit_fwd_stored = tk.IntVar()
        self.entry_y_limit_fwd_stored.set(mwt_dict['y_fwd_limit'])
        self.entry_y_limit_rev_stored = tk.IntVar()
        self.entry_y_limit_rev_stored.set(mwt_dict['y_rev_limit'])
        self.entry_z_limit_fwd_stored = tk.IntVar()
        self.entry_z_limit_fwd_stored.set(mwt_dict['z_fwd_limit'])
        self.entry_z_limit_rev_stored = tk.IntVar()
        self.entry_z_limit_rev_stored.set(mwt_dict['z_rev_limit'])
        self.checkbox_unlock_limits_status = IntVar()

        # -- limits labels
        self.label_software_limits = customtkinter.CTkLabel(self.tabview_position.tab("Limits"), text="Software Limits",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label_forward = customtkinter.CTkLabel(self.tabview_position.tab("Limits"), text="Forward",
                                                    anchor="center")
        self.label_reverse = customtkinter.CTkLabel(self.tabview_position.tab("Limits"), text="Reverse",
                                                    anchor="center")
        self.label_x_limits = customtkinter.CTkLabel(self.tabview_position.tab("Limits"), text="X", anchor="center")
        self.label_y_limits = customtkinter.CTkLabel(self.tabview_position.tab("Limits"), text="Y", anchor="center")
        self.label_z_limits = customtkinter.CTkLabel(self.tabview_position.tab("Limits"), text="Z", anchor="center")

        # -- limits entry fields
        self.entry_x_limit_fwd = customtkinter.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                                        textvariable=self.entry_x_limit_fwd_stored)
        self.entry_x_limit_fwd.configure(justify="center")
        self.entry_x_limit_rev = customtkinter.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                                        textvariable=self.entry_x_limit_rev_stored)
        self.entry_x_limit_rev.configure(justify="center")
        self.entry_y_limit_fwd = customtkinter.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                                        textvariable=self.entry_y_limit_fwd_stored)
        self.entry_y_limit_fwd.configure(justify="center")
        self.entry_y_limit_rev = customtkinter.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                                        textvariable=self.entry_y_limit_rev_stored)
        self.entry_y_limit_rev.configure(justify="center")
        self.entry_z_limit_fwd = customtkinter.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                                        textvariable=self.entry_z_limit_fwd_stored)
        self.entry_z_limit_fwd.configure(justify="center")
        self.entry_z_limit_rev = customtkinter.CTkEntry(self.tabview_position.tab("Limits"), width=70,
                                                        textvariable=self.entry_z_limit_rev_stored)
        self.entry_z_limit_rev.configure(justify="center")

        # -- limits buttons and checkbox
        self.checkbox_unlock_limits = customtkinter.CTkCheckBox(self.tabview_position.tab("Limits"), text="", onvalue=1,
                                                                offvalue=0, variable=self.checkbox_unlock_limits_status,
                                                                command=self.enable_button)
        self.button_set_limits = customtkinter.CTkButton(self.tabview_position.tab("Limits"), text='Set All Limits',
                                                         fg_color="transparent", border_width=2, width=90,
                                                         text_color=("gray10", "#DCE4EE"), state="disabled",
                                                         command=self.set_limits)
        self.button_check_limits = customtkinter.CTkButton(self.tabview_position.tab("Limits"), text='Check All Limits',
                                                           fg_color="transparent", border_width=2, width=20,
                                                           text_color=("gray10", "#DCE4EE"), command=self.check_limits)

        # -- limits widgets positioning
        self.label_software_limits.grid(row=0, column=0, columnspan=4, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.label_forward.grid(row=1, column=1, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.label_reverse.grid(row=1, column=2, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.label_x_limits.grid(row=2, column=0, padx=(20, 0), pady=(5, 0), sticky="nsew")
        self.label_y_limits.grid(row=3, column=0, padx=(20, 0), pady=(5, 0), sticky="nsew")
        self.label_z_limits.grid(row=4, column=0, padx=(20, 0), pady=(5, 5), sticky="nsew")
        self.entry_x_limit_fwd.grid(row=2, column=1, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.entry_x_limit_rev.grid(row=2, column=2, padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.entry_y_limit_fwd.grid(row=3, column=1, padx=(5, 0), pady=(10, 0), sticky="nsew")
        self.entry_y_limit_rev.grid(row=3, column=2, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.entry_z_limit_fwd.grid(row=4, column=1, padx=(5, 0), pady=(10, 5), sticky="nsew")
        self.entry_z_limit_rev.grid(row=4, column=2, padx=(10, 0), pady=(10, 5), sticky="nsew")
        self.checkbox_unlock_limits.grid(row=2, column=3, padx=(10, 0), pady=(5, 0), sticky="w")
        self.button_set_limits.grid(row=2, column=3, padx=(40, 0), pady=(5, 0), sticky="e")
        self.button_check_limits.grid(row=3, column=3, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="nsew")

        # - create carriage stop codes display
        self.tabview_config = customtkinter.CTkTabview(self)
        self.tabview_config.grid(row=2, column=0, padx=5, sticky="nsew")
        self.tabview_config.add("Stop Codes")
        self.tabview_config.add("Log")

        # -- stop codes entry defaults
        # global mwt_dict
        self.entry_stop_codes_stored = tk.StringVar()
        self.entry_stop_codes_stored.set("1, 1, 1")

        # -- stop codes labels
        self.label_stop_codes = customtkinter.CTkLabel(self.tabview_config.tab("Stop Codes"), text="Stop Codes",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label_stop_terms = customtkinter.CTkLabel(self.tabview_config.tab("Stop Codes"),
                                                       text="0 - motors are running\n1 - motors stopped at "
                                                            "commanded position\n7 - motors stopped after abort "
                                                            "command \n9 - motors stopped after finding home")

        # -- stop codes entry fields
        self.entry_stop_codes_input = customtkinter.CTkEntry(self.tabview_config.tab("Stop Codes"), width=70,
                                                             state="disabled",
                                                             textvariable=self.entry_stop_codes_stored)
        self.entry_stop_codes_input.configure(justify="center")

        # -- stop codes widgets positioning
        self.label_stop_codes.grid(row=0, column=0, padx=(35, 0), pady=(10, 0), sticky="nsew")
        self.entry_stop_codes_input.grid(row=1, column=0, padx=(135, 100), pady=(10, 0), sticky="nsew")
        self.label_stop_terms.grid(row=2, column=0, padx=(35, 0), pady=(10, 0), sticky="n")

        # - log events
        # -- log events label fields
        self.label_log = customtkinter.CTkLabel(self.tabview_config.tab("Log"), text="Event Log",
                                                anchor="center",
                                                font=customtkinter.CTkFont(size=16, weight="bold"))

        # -- log events text fields
        self.textbox_log = customtkinter.CTkTextbox(self.tabview_config.tab("Log"), width=250, height=100)
        self.textbox_log.insert("0.0", "Welcome!")

        # -- log events button
        self.button_clear_log = customtkinter.CTkButton(self.tabview_config.tab("Log"), text='Clear',
                                                        fg_color="transparent", border_width=2, width=90,
                                                        text_color=("gray10", "#DCE4EE"), command=self.clear_log)

        # -- log events widgets positioning
        self.label_log.grid(row=0, column=0, padx=(45, 0), pady=(10, 0), sticky="nsew")
        self.button_clear_log.grid(row=1, column=0, padx=(45, 0), pady=(10, 0), sticky="nsew")
        self.textbox_log.grid(row=2, column=0, padx=(45, 0), pady=(10, 0), sticky="nsew")

        # - create carriage movement controls frame and (SP, AC, DC) tab
        self.tabview_movement = customtkinter.CTkTabview(self)
        self.tabview_movement.grid(row=3, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="nsew")
        self.tabview_movement.add("SP, AC, DC")

        # -- movement entry defaults (SP, AC, DC)
        # global mwt_dict
        self.entry_speed_x_stored = tk.IntVar()
        self.entry_speed_x_stored.set(2000)
        self.entry_speed_y_stored = tk.IntVar()
        self.entry_speed_y_stored.set(1500)
        self.entry_speed_z_stored = tk.IntVar()
        self.entry_speed_z_stored.set(300)
        self.entry_accel_x_stored = tk.IntVar()
        self.entry_accel_x_stored.set(1024)
        self.entry_accel_y_stored = tk.IntVar()
        self.entry_accel_y_stored.set(1024)
        self.entry_accel_z_stored = tk.IntVar()
        self.entry_accel_z_stored.set(1024)
        self.entry_decel_x_stored = tk.IntVar()
        self.entry_decel_x_stored.set(1024)
        self.entry_decel_y_stored = tk.IntVar()
        self.entry_decel_y_stored.set(1024)
        self.entry_decel_z_stored = tk.IntVar()
        self.entry_decel_z_stored.set(1024)

        # -- movement labels (SP, AC, DC)
        self.label_sp_ac_dc = customtkinter.CTkLabel(self.tabview_movement.tab("SP, AC, DC"), text="Speed, Acceleration"
                                                                                                   ", Deceleration",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label_speed = customtkinter.CTkLabel(self.tabview_movement.tab("SP, AC, DC"), text="SP", anchor="center")
        self.label_accel = customtkinter.CTkLabel(self.tabview_movement.tab("SP, AC, DC"), text="AC", anchor="center")
        self.label_decel = customtkinter.CTkLabel(self.tabview_movement.tab("SP, AC, DC"), text="DC", anchor="center")
        self.label_x = customtkinter.CTkLabel(self.tabview_movement.tab("SP, AC, DC"), text="X", anchor="center")
        self.label_y = customtkinter.CTkLabel(self.tabview_movement.tab("SP, AC, DC"), text="Y", anchor="center")
        self.label_z = customtkinter.CTkLabel(self.tabview_movement.tab("SP, AC, DC"), text="Z", anchor="center")

        # -- movement entry fields (SP, AC, DC)
        self.entry_speed_x_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_speed_x_stored)
        self.entry_speed_x_input.configure(justify="center")
        self.entry_speed_x_input.bind('<FocusIn>', lambda event: self.enable_button_set)
        self.entry_speed_y_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_speed_y_stored)
        self.entry_speed_y_input.configure(justify="center")
        self.entry_speed_z_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_speed_z_stored)
        self.entry_speed_z_input.configure(justify="center")
        self.entry_accel_x_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_accel_x_stored)
        self.entry_accel_x_input.configure(justify="center")
        self.entry_accel_y_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_accel_y_stored)
        self.entry_accel_y_input.configure(justify="center")
        self.entry_accel_z_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_accel_z_stored)
        self.entry_accel_z_input.configure(justify="center")
        self.entry_decel_x_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_decel_x_stored)
        self.entry_decel_x_input.configure(justify="center")
        self.entry_decel_y_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_decel_y_stored)
        self.entry_decel_y_input.configure(justify="center")
        self.entry_decel_z_input = customtkinter.CTkEntry(self.tabview_movement.tab("SP, AC, DC"), width=50,
                                                          textvariable=self.entry_decel_z_stored)
        self.entry_decel_z_input.configure(justify="center")

        # -- movement buttons (SP, AC, DC)
        self.button_set_movement = customtkinter.CTkButton(self.tabview_movement.tab("SP, AC, DC"), text='Set',
                                                           fg_color="transparent", border_width=2, width=10,
                                                           text_color=("gray10", "#DCE4EE"), state="disabled",
                                                           command=self.enable_button_set)
        self.button_adjust_up = customtkinter.CTkButton(self.tabview_movement.tab("SP, AC, DC"), text="\u25B2",
                                                        fg_color="transparent", border_width=1, width=3,
                                                        text_color=("gray10", "#DCE4EE"),
                                                        command=self.increase_movement)
        self.button_adjust_down = customtkinter.CTkButton(self.tabview_movement.tab("SP, AC, DC"), text="\u25BC",
                                                          fg_color="transparent", border_width=1, width=3,
                                                          text_color=("gray10", "#DCE4EE"),
                                                          command=self.decrease_movement)

        # -- movement widgets positioning (SP, AC, DC)
        self.label_sp_ac_dc.grid(row=0, column=0, columnspan=6, padx=(35, 0), pady=(10, 0), sticky="nsew")
        self.label_speed.grid(row=1, column=1, padx=(0, 0), pady=(10, 0), sticky="s")
        self.label_accel.grid(row=1, column=2, padx=0, pady=(10, 0), sticky="s")
        self.label_decel.grid(row=1, column=3, padx=0, pady=(10, 0), sticky="s")
        self.label_x.grid(row=2, column=0, padx=(25, 0), pady=(5, 0), sticky="e")
        self.label_y.grid(row=3, column=0, padx=(25, 0), pady=(10, 0), sticky="e")
        self.label_z.grid(row=4, column=0, padx=(25, 0), pady=(10, 0), sticky="e")
        self.entry_speed_x_input.grid(row=2, column=1, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_accel_x_input.grid(row=2, column=2, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_decel_x_input.grid(row=2, column=3, padx=(5, 10), pady=(5, 0), sticky="nsew")
        self.entry_speed_y_input.grid(row=3, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_accel_y_input.grid(row=3, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_decel_y_input.grid(row=3, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.entry_speed_z_input.grid(row=4, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_accel_z_input.grid(row=4, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_decel_z_input.grid(row=4, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.button_set_movement.grid(row=2, column=4, columnspan=2, pady=(5, 0), sticky="nsew")
        self.button_adjust_up.grid(row=3, column=4, pady=(10, 0), sticky="nsew")
        self.button_adjust_down.grid(row=3, column=5, pady=(10, 0), sticky="nsew")

        # - create carriage movement controls tab (KP, KI, KD)
        # -- proportional control parameter, integral control parameter, derivative control parameter
        self.tabview_movement.add("KP, KI, KD")

        # -- movement entry defaults (KP, KI, KD)
        # global mwt_dict
        self.entry_kp_x_stored = tk.StringVar()
        self.entry_kp_x_stored.set("2")
        self.entry_kp_y_stored = tk.StringVar()
        self.entry_kp_y_stored.set("4")
        self.entry_kp_z_stored = tk.StringVar()
        self.entry_kp_z_stored.set("4")
        self.entry_ki_x_stored = tk.StringVar()
        self.entry_ki_x_stored.set("0.008")
        self.entry_ki_y_stored = tk.StringVar()
        self.entry_ki_y_stored.set("0.024")
        self.entry_ki_z_stored = tk.StringVar()
        self.entry_ki_z_stored.set("0.008")
        self.entry_kd_x_stored = tk.StringVar()
        self.entry_kd_x_stored.set("500")
        self.entry_kd_y_stored = tk.StringVar()
        self.entry_kd_y_stored.set("100")
        self.entry_kd_z_stored = tk.StringVar()
        self.entry_kd_z_stored.set("1000")

        # -- movement entry fields (KP, KI, KD)
        self.entry_kp_x_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_kp_x_stored)
        self.entry_kp_x_input.configure(justify="center")
        self.entry_kp_x_input.bind('<FocusIn>', lambda event: self.enable_button_set)
        self.entry_kp_y_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_kp_y_stored)
        self.entry_kp_y_input.configure(justify="center")
        self.entry_kp_z_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_kp_z_stored)
        self.entry_kp_z_input.configure(justify="center")
        self.entry_ki_x_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_ki_x_stored)
        self.entry_ki_x_input.configure(justify="center")
        self.entry_ki_y_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_ki_y_stored)
        self.entry_ki_y_input.configure(justify="center")
        self.entry_ki_z_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_ki_z_stored)
        self.entry_ki_z_input.configure(justify="center")
        self.entry_kd_x_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_kd_x_stored)
        self.entry_kd_x_input.configure(justify="center")
        self.entry_kd_y_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_kd_y_stored)
        self.entry_kd_y_input.configure(justify="center")
        self.entry_kd_z_input = customtkinter.CTkEntry(self.tabview_movement.tab("KP, KI, KD"), width=50,
                                                       textvariable=self.entry_kd_z_stored)
        self.entry_kd_z_input.configure(justify="center")

        # -- movement labels (KP, KI, KD)
        self.label_kp_ki_kd = customtkinter.CTkLabel(self.tabview_movement.tab("KP, KI, KD"), text="Proportional, "
                                                                                                   "Integral, "
                                                                                                   "Derivative",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label_kp = customtkinter.CTkLabel(self.tabview_movement.tab("KP, KI, KD"), text="KP", anchor="center")
        self.label_ki = customtkinter.CTkLabel(self.tabview_movement.tab("KP, KI, KD"), text="KI", anchor="center")
        self.label_kd = customtkinter.CTkLabel(self.tabview_movement.tab("KP, KI, KD"), text="KD", anchor="center")
        self.label_x2 = customtkinter.CTkLabel(self.tabview_movement.tab("KP, KI, KD"), text="X", anchor="center")
        self.label_y2 = customtkinter.CTkLabel(self.tabview_movement.tab("KP, KI, KD"), text="Y", anchor="center")
        self.label_z2 = customtkinter.CTkLabel(self.tabview_movement.tab("KP, KI, KD"), text="Z", anchor="center")

        # -- movement buttons (KP, KI, KD)
        self.button_set_movement2 = customtkinter.CTkButton(self.tabview_movement.tab("KP, KI, KD"), text='Set',
                                                            fg_color="transparent", border_width=2, width=10,
                                                            text_color=("gray10", "#DCE4EE"), state="disabled",
                                                            command=self.enable_button_set)
        self.button_adjust_up2 = customtkinter.CTkButton(self.tabview_movement.tab("KP, KI, KD"), text="\u25B2",
                                                         fg_color="transparent", border_width=1, width=3,
                                                         text_color=("gray10", "#DCE4EE"),
                                                         command=self.increase_movement)
        self.button_adjust_down2 = customtkinter.CTkButton(self.tabview_movement.tab("KP, KI, KD"), text="\u25BC",
                                                           fg_color="transparent", border_width=1, width=3,
                                                           text_color=("gray10", "#DCE4EE"),
                                                           command=self.decrease_movement)

        # -- movement widgets positioning (KP, KI, KD)
        self.label_kp_ki_kd.grid(row=0, column=0, columnspan=6, padx=(40, 0), pady=(10, 0), sticky="nsew")
        self.label_kp.grid(row=1, column=1, padx=(0, 0), pady=(10, 0), sticky="s")
        self.label_ki.grid(row=1, column=2, padx=0, pady=(10, 0), sticky="s")
        self.label_kd.grid(row=1, column=3, padx=0, pady=(10, 0), sticky="s")
        self.label_x2.grid(row=2, column=0, padx=(30, 0), pady=(5, 0), sticky="e")
        self.label_y2.grid(row=3, column=0, padx=(30, 0), pady=(10, 0), sticky="e")
        self.label_z2.grid(row=4, column=0, padx=(30, 0), pady=(10, 0), sticky="e")
        self.entry_kp_x_input.grid(row=2, column=1, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_ki_x_input.grid(row=2, column=2, padx=5, pady=(5, 0), sticky="nsew")
        self.entry_kd_x_input.grid(row=2, column=3, padx=(5, 10), pady=(5, 0), sticky="nsew")
        self.entry_kp_y_input.grid(row=3, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_ki_y_input.grid(row=3, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_kd_y_input.grid(row=3, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.entry_kp_z_input.grid(row=4, column=1, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_ki_z_input.grid(row=4, column=2, padx=5, pady=(10, 0), sticky="nsew")
        self.entry_kd_z_input.grid(row=4, column=3, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.button_set_movement2.grid(row=2, column=4, columnspan=2, pady=(5, 0), sticky="nsew")
        self.button_adjust_up2.grid(row=3, column=4, pady=(10, 0), sticky="nsew")
        self.button_adjust_down2.grid(row=3, column=5, pady=(10, 0), sticky="nsew")

        # - program theme default values
        self.menu_appearance.set("System")
        # self.menu_scaling.set("100%")

        # - prints current carriage status in console upon start of program
        self.print_to_log(mwt_dict)

    # - GUI functions
    # -- change overall appearance of program to light, dark, or system
    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # -- change overall scaling of program
    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # - carriage functions
    # -- stop carriage move execution and freeze actual position values
    def stop_carriage(self):
        self.print_to_log("Carriage stopped!")

    # -- move carriage to home position (default move priority: z, y, x...configurable?)
    def move_home(self):
        self.print_to_log("Moving home...")

    # -- move carriage to input position for axis
    @staticmethod
    def move_axis(self, move_target, axis_limit_fwd, axis_limit_rev):
        global mwt_dict
        if axis_limit_rev.get() > move_target.get() or move_target.get() > axis_limit_fwd.get():
            self.print_to_log("Move is beyond limits.")
        elif argname('move_target') == "entry_x_target_stored":
            self.print_to_log("Moving to...")
            self.print_to_log(self.entry_x_target.get())
            self.set_axis(self, self.entry_x_actual_stored, move_target)
        elif argname('move_target') == "entry_y_target_stored":
            self.print_to_log("Moving to...")
            self.print_to_log(self.entry_y_target.get())
            self.set_axis(self, self.entry_y_actual_stored, move_target)
        elif argname('move_target') == "entry_z_target_stored":
            self.print_to_log("Moving to...")
            self.print_to_log(self.entry_z_target.get())
            self.set_axis(self, self.entry_z_actual_stored, move_target)
        else:
            self.print_to_log("Move Error!")

    # -- set axis position target value to actual value
    @staticmethod
    def set_axis(self, axis_actual, axis_target):
        global mwt_dict
        axis_actual.set(axis_target.get())
        if argname('axis_actual') == "entry_x_actual_stored":
            mwt_dict |= {'x_actual': self.entry_x_target_stored.get()}
        elif argname('axis_actual') == "entry_y_actual_stored":
            mwt_dict |= {'y_actual': self.entry_y_target_stored.get()}
        elif argname('axis_actual') == "entry_z_actual_stored":
            mwt_dict |= {'z_actual': self.entry_z_target_stored.get()}
        else:
            self.print_to_log("Error!")
        self.csv_generate()
        self.print_to_log(mwt_dict)

    # -- ???
    def print_codes(self):
        pass

    # -- enables the set limits button if the adjacent checkbox is checked
    def enable_button(self):
        self.button_set_limits.configure(state=NORMAL if self.checkbox_unlock_limits_status.get() == 1 else DISABLED)

    # -- enables the set carriage attributes button if a prior action is performed
    def enable_button_set(self):
        self.button_set_movement.configure(state=NORMAL if self.focus_get() == self.entry_speed_x_input else DISABLED)

    # -- enables the increment up button to adjust carriage attributes if a prior action is performed
    def enable_button_up(self):
        pass

    # -- enables the increment down button to adjust carriage attributes if a prior action is performed
    def enable_button_down(self):
        pass

    # -- takes user input for all limits entries and stores those values
    def set_limits(self):
        global mwt_dict
        self.entry_x_limit_fwd_stored.set(self.entry_x_limit_fwd.get())
        self.entry_x_limit_rev_stored.set(self.entry_x_limit_rev.get())
        self.entry_y_limit_fwd_stored.set(self.entry_y_limit_fwd.get())
        self.entry_y_limit_rev_stored.set(self.entry_y_limit_rev.get())
        self.entry_z_limit_fwd_stored.set(self.entry_z_limit_fwd.get())
        self.entry_z_limit_rev_stored.set(self.entry_z_limit_rev.get())
        mwt_dict |= {'x_fwd_limit': self.entry_x_limit_fwd_stored.get()}
        mwt_dict |= {'x_rev_limit': self.entry_x_limit_rev_stored.get()}
        mwt_dict |= {'y_fwd_limit': self.entry_y_limit_fwd_stored.get()}
        mwt_dict |= {'y_rev_limit': self.entry_y_limit_rev_stored.get()}
        mwt_dict |= {'z_fwd_limit': self.entry_z_limit_fwd_stored.get()}
        mwt_dict |= {'z_rev_limit': self.entry_z_limit_rev_stored.get()}
        self.checkbox_unlock_limits_status.set(0)
        self.button_set_limits.configure(state="disabled")
        self.csv_generate()

    # -- increases carriage attribute
    def increase_movement(self):
        self.entry_speed_x_stored.set(self.entry_speed_x_stored.get() + 1)

    # -- decreases carriage attribute
    def decrease_movement(self):
        self.entry_speed_x_stored.set(self.entry_speed_x_stored.get() - 1)

    # -- used to print what GUI function is currently in focus to the program event log
    def entry_focus(self):
        self.print_to_log("focus is:")
        self.print_to_log(self.focus_get())

    # -- used to save all current carriage attributes
    def set_movement(self):
        if self.focus_get() == self.entry_speed_x_input:
            self.print_to_log("WIDGET IN FOCUS!")
            self.button_set_movement.configure(state=NORMAL)
        else:
            self.print_to_log("Not focused, focus is")
            self.print_to_log(self.focus_get())
            self.button_set_movement.configure(state="disabled")

    # - event log functions
    # -- used to print event descriptions or carriage status to the program event log
    def print_to_log(self, text):
        self.textbox_log.insert(tk.END, '\n')
        self.textbox_log.insert(tk.END, text)

    # -- clears the program event log
    def clear_log(self):
        self.textbox_log.delete("0.0", "end")
        self.textbox_log.insert("0.0", "Log cleared.")

    # - csv functions
    # -- recalls saved limits from csv and outputs them in the log
    def check_limits(self):
        global mwt_dict
        self.entry_x_limit_fwd_stored.set(mwt_dict['x_fwd_limit'])
        self.entry_x_limit_rev_stored.set(mwt_dict['x_rev_limit'])
        self.entry_y_limit_fwd_stored.set(mwt_dict['y_fwd_limit'])
        self.entry_y_limit_rev_stored.set(mwt_dict['y_rev_limit'])
        self.entry_z_limit_fwd_stored.set(mwt_dict['z_fwd_limit'])
        self.entry_z_limit_rev_stored.set(mwt_dict['z_rev_limit'])
        self.csv_recall()

    # -- csv file that stores carriage values such as current position and movement limits
    def csv_generate(self):
        with open('mwt_storage.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in mwt_dict.items():
                writer.writerow([key, value])
        self.checkbox_unlock_limits_status.set(0)
        self.button_set_limits.configure(state="disabled")

    # -- recalls saved limits from csv
    def csv_recall(self):
        global mwt_dict
        with open("mwt_storage.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(','.join(row))
        self.print_to_log(mwt_dict)

    # -- restores saved positions to program from csv
    def restore_positions(self):
        global mwt_dict
        self.entry_x_actual_stored.set(mwt_dict['x_actual'])
        self.entry_y_actual_stored.set(mwt_dict['y_actual'])
        self.entry_z_actual_stored.set(mwt_dict['z_actual'])


if __name__ == "__main__":
    app = MoveCarriage()
    app.mainloop()
