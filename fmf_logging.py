import time
_ERROR_LOG_FILE = "mwt_error_log.txt"

def set_error_log_file(path: str):
    global _ERROR_LOG_FILE
    _ERROR_LOG_FILE = path

# - event log functions
# -- used to print event descriptions or carriage status to the event log file
def write_log(user_action: str):
    print(user_action)
    # with open('mwt_log.txt', 'w', newline='') as txt_file:
    #     txt_file.write(user_action)

def log_error(error_message: str):
    print(error_message)
    with open(_ERROR_LOG_FILE, 'a') as txt_file:
        txt_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} {error_message}\n')

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

