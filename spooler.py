import win32print
import time

#constants

wp = win32print

# lists and dicitonaries of constants
ptypelist =[(wp.PRINTER_ENUM_SHARED,'shared'),(wp.PRINTER_ENUM_LOCAL,'local'),(wp.PRINTER_ENUM_CONNECTIONS,'network')]
cmds = {'Pause':wp.JOB_CONTROL_PAUSE, 'cancel':wp.JOB_CONTROL_CANCEL,'resume':wp.JOB_CONTROL_RESUME,'prior_low':wp.MIN_PRIORITY,'prior_high':wp.MAX_PRIORITY,'prior_normal':wp.DEF_PRIORITY}
statuscodes = {'deleting':wp.JOB_STATUS_DELETING,'error':wp.JOB_STATUS_ERROR,'offline':wp.JOB_STATUS_OFFLINE,'paperout':wp.JOB_STATUS_PAPEROUT,'paused':wp.JOB_STATUS_PAUSED,'printed':wp.JOB_STATUS_PRINTED,'printing':wp.JOB_STATUS_PRINTING,'spooling':wp.JOB_STATUS_SPOOLING}

class PMFuncs:

     def __init__(self):

         # initialise the list of printers
         self.PList =[]

     def PrinterList(self):

         # returns a list of dicts.
         # this gets the default printer
         tmpdic ={}
         DefPName = win32print.GetDefaultPrinter()

         # Get the default printer firstso we can add this to the list of printers

         for pt in ptypelist:

             try:

                 for (Flags,pDescription,pName,pComment) in list(win32print.EnumPrinters(pt[0],None,1)):
                     tmpdic ={}
                     tmpdic['PType'] = pt[1]
                     tmpdic['Flags'] = Flags
                     tmpdic['Description'] = pDescription
                     #test for if this is the default printer
                     if pName == DefPName:
                         tmpdic['DefPrinter':True]
                     else:
                         tmpdic['DefPrinter':False]
                     tmpdic['Name'] = pName
                     tmpdic['Comment'] = pComment
                     self.PList.append(tmpdic)
             except:
                 pass    #no printers of this type so don't add anything

         return self.PList   #list of installed printers

     def GetJobList(self,printer):

         phandle = win32print.OpenPrinter(printer)
         #now get all the print jobs (start at job 0 and -1 for all jobs)
         jlist = win32print.EnumJobs(phandle,0,-1,1)
         win32print.ClosePrinter(phandle)
         return jlist    # this lists all jobs on all printers

     def GetJobInfo(self,printer,jobID):

         phandle = win32print.OpenPrinter(printer)
         ilist = win32print.GetJob(phandle,jobID,1)
         win32print.ClosePrinter(phandle)
         return ilist    #this lists all info available at level 1 for selected job.

     def SetJobCmd(self, printer, jobID , JobInfo , RCmd ):

         phandle = win32print.OpenPrinter(printer)
         win32print.SetJob(phandle,jobID,1,JobInfo,Cmds[RCmd])
         win32print.ClosePrinter(phandle)

# test functions
e = PMFuncs()
while 1:

     time.sleep(1)
     e = PMFuncs()
     for i in e.PrinterList():

         try:
             p = e.GetJobList(i['Name'])
             for w in p:
                 print (e.GetJobInfo(i['Name'],w['JobID']))

         except:
             pass
