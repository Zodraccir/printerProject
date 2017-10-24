from ctypes import *
from ctypes.wintypes import HANDLE, LPSTR

def add_job_callback():
    print('A job has just been sent to the printer this script is monitoring')

spl = windll.LoadLibrary('winspool.drv')

printer_name = 'KONICA MINOLTA PS Color Laser Class Driver'
# Put the name of your printer here - can be networked or any installed on your computer.  Alternatively, set it to None to use the local printer server
#printer_name = None

hPrinter = HANDLE()

if printer_name:
    spl.OpenPrinterA(c_char_p(printer_name), byref(hPrinter),None)
else:
    spl.OpenPrinterA(None, byref(hPrinter),None)

print(hPrinter)


hjob = spl.FindFirstPrinterChangeNotification(hPrinter,0x00000100,0, None)
# 0x00000100 is a flags setting to set watch for only PRINTER_CHANGE_ADD_JOB
while True:
    windll.kernel32.WaitForSingleObject(hjob,-1)
    #When this function returns, the change that you're monitoring for has been observed, trigger the function
    add_job_callback()
    spl.FindNextPrinterChangeNotification(hjob, None, None, None)