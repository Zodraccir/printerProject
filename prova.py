import win32print
import time

PRINTER_ERROR_STATES = (
    win32print.PRINTER_STATUS_NO_TONER,
    win32print.PRINTER_STATUS_NOT_AVAILABLE,
    win32print.PRINTER_STATUS_OFFLINE,
    win32print.PRINTER_STATUS_OUT_OF_MEMORY,
    win32print.PRINTER_STATUS_OUTPUT_BIN_FULL,
    win32print.PRINTER_STATUS_PAGE_PUNT,
    win32print.PRINTER_STATUS_PAPER_JAM,
    win32print.PRINTER_STATUS_PAPER_OUT,
    win32print.PRINTER_STATUS_PAPER_PROBLEM,
)


def printer_errorneous_state(printer, error_states=PRINTER_ERROR_STATES):
    prn_opts = win32print.GetPrinter(printer)
    status_opts = prn_opts[18]
    for error_state in error_states:
        if status_opts & error_state:
            return error_state
    return 0

def printCatching(printJob):
    for key,values in printJob.items():
        if str(key)=="Status" & str(values)=="None":
            print(str(key)+"  ==> value ==> "+str(values))
            pass

def main():
    printer_name=win32print.GetDefaultPrinter()
    while 1:
        time.sleep(1)
        prn = win32print.OpenPrinter(printer_name)
        error = printer_errorneous_state(prn)
        if error:
            print("ERROR occurred: ", error)
        else:
            print("Printer OK... Name of Printer :" + prn)
            ilist = win32print.GetJob(prn, jobID, 1)
            print_jobs = win32print.EnumJobs(prn, 0, 1, 2)
            currentJob={}
            for job in print_jobs:
                while(win32print.GetJob(job["JobId"])>0):
                    currentJob=job
            printCatching(currentJob)





if __name__ == "__main__":
    main()