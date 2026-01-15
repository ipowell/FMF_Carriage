import time
_ERROR_LOG_FILE = "_internal/mwt_error_log.txt"
_EVENT_LOG_FILE = "_internal/mwt_event_log.txt"

_ERROR_LOG_TYPE = "ERR"
_EVENT_LOG_TYPE = "DBG"

def set_error_log_file(path: str):
    global _ERROR_LOG_FILE
    _ERROR_LOG_FILE = path

def set_event_log_file(path: str):
    global _EVENT_LOG_FILE
    _EVENT_LOG_FILE = path
    
def _get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def _write_log(path: str, timestamp: str, log_type: str, message: str):
    print(message)
    with open(path, 'a') as txt_file:
        txt_file.write(f'{timestamp} [{log_type}]: {message}\n')

# - event log functions
# -- used to print event descriptions or carriage status to the event log file
def log_event(message: str):
    _write_log(_EVENT_LOG_FILE, _get_timestamp(), _EVENT_LOG_TYPE, message')

def log_error(error_message: str):
    timestamp = _get_timestamp()
    for path in (_ERROR_LOG_FILE, _EVENT_LOG_FILE):
        _write_log(path, timestamp, _ERROR_LOG_TYPE, error_message')

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

