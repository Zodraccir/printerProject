import win32print

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
    for job in printJob:
        for key,values in job.items():
            if str(key)=="Status" & str(values)=="None":
                print(str(key)+"  ==> value ==> "+str(values))
            pass
        return job

    


def main():
    printer_name = "HP LaserJet 2420 PCL6 Class Driver" # or get_printer_names()[0]
    prn = win32print.OpenPrinter(printer_name)
    error = printer_errorneous_state(prn)
    if error:
        print("ERROR occurred: ", error)
    else:
        print("Printer OK...")
        #  Do the real workS
        previusStatus=0
        counter=0
        previusJob={}
        while True:
            jobs=[]
            print_jobs = win32print.EnumJobs(prn, 0, 1, 2)
            if print_jobs:
                jobs.extend(list(print_jobs))
            
            if(len(jobs)>0):
                if(previusStatus==0):
                    print("Starting printing")
                counter=counter+1
                previusStatus=1
                previusJob=printCatching(jobs)
            else:
                if(previusStatus==1):
                    print("User " + previusJob["pUserName"] + " have printed " + str(previusJob["PagesPrinted"]) + " Pages")
                    print("Finish printing")
                    print (counter)
                    counter=0

                previusStatus=0
            
            


    win32print.ClosePrinter(prn)


if __name__ == "__main__":
    main()
