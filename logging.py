import os
import sys

# - event log functions
# -- used to print event descriptions or carriage status to the event log file
def write_log(user_action: str):
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

