import sys
import requests
import json

"""

Name: actiPyme.py

Desc: Defines the actiPyme module, which is a general purpose driver library towards the timekeeping software actiTIME. This driver is built upon URL requests (cURL) and json

Author: Alberto Lavatelli - 2019


"""

class Driver(object):
    """ 
    Name: actiPyme.Driver(Target,actitimeUserName,actitimePsw)

    Args:   Target, url of the actitime server
            actitimeUserName, account user name
            actitimePsw, account password

    Desc: This is the core driver with communication protocol API
    
    """
    def __init__(self,Target="",actitimeUserName="",actitimePsw=""):
        self.Target=Target
        self.actitimeUserName=actitimeUserName
        self.actitimePsw=actitimePsw
        self.IsStarted=False
        self.ServerHeaders= {'accept': 'application/json; charset=UTF-8'}
        self.writeDefheaders={'accept': 'application/json; charset=UTF-8', 'Content-Type': 'application/json' }
        self.IdNumber=0
        self.IdName=""
        self.IdSurname=""

    def Start(self):
        """ 
            Name: actiPyme.Driver.Start()

            Args:  Void

            Desc: This method starts up the driver. Handshake is performed by means of user self identification.
        """        
        requrl=self.Target
        requrl+="/users/me"
        try:
            MyIdReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw),timeout=3)
            MyIdReq.raise_for_status()   
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            sys.exit(1)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            sys.exit(1)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            print ("Oops: Something Else",err)
            sys.exit(1)
        
        IdData=json.loads(MyIdReq.text)
        self.IdNumber=IdData['id']
        self.IdName=IdData['firstName']
        self.IdSurname=IdData['lastName']
        self.IsStarted=True

    def Stop(self):
        """ 
            Name: actiPyme.Driver.Stop()

            Args:  Void

            Desc: This method shuts down the driver. Useful to re initialize the communication.
        """   
        self.IdNumber=""
        self.IdName=""
        self.IdSurname=""
        self.IsStarted=False


    def CustomerList(self):
        """ 
            Name: actiPyme.Driver.CustomerList()

            Args:  Void

            Desc: Simply get the info about the customers. The output is a JSON object
        """
        if  self.IsStarted:   
            requrl=self.Target
            requrl+="/customers"
            CustReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            Clients=json.loads(CustReq.text)
        else:
            Clients={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')
        
        return Clients

    def LeaveTypesList(self):
        """ 
            Name: actiPyme.Driver.LeaveTypesList()

            Args:  Void

            Desc: Simply get the info about the leave types. The output is a JSON object
        """
        if  self.IsStarted:   
            requrl=self.Target
            requrl+="/leaveTypes"
            CustReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            Leaves=json.loads(CustReq.text)
        else:
            Leaves={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')
        
        return Leaves

    def SearchTasks(self,SearchMethod: int,SearchArgument: str):
        """ 
            Name: actiPyme.Driver.SearchTasks(SearchMethod: str, SearchArgument: str)

            Args:   SearchMethod, specify how you want to search: 1 - By Name; 2 - By task id; 3 - By customer id; 4 - By project id
                    SearchArgument, what you want to search as string

            Desc: This function lets you search for a task inside the actitime database. The output is a JSON object
        """

        MethodDict={1: "ByName", 2: "ByIds", 3: "ByCustomerIds", 4: "ByProjectIds"}
        if self.IsStarted:
            #switch on the dictionary   
            SrcMethTok=MethodDict.get(SearchMethod,"err")
            if SrcMethTok=="err":
                SrcResult={}
                raise Exception('Inappropriate or bad search method')
            elif SrcMethTok=="ByName":
                #Here we look for a name
                requrl=self.Target+"/tasks?offset=0&words="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByIds":
                #Here we look for a task ID
                requrl=self.Target+"/tasks?offset=0&ids="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByCustomerIds":
                #Here we look for a customer ID
                requrl=self.Target+"/tasks?offset=0&customerIds="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByProjectIds":
                #Here we look for a project ID
                requrl=self.Target+"/tasks?offset=0&projectIds="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            else:
                SrcResult={}
                raise Exception('Inappropriate or bad search method')    
        else:
            SrcResult={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return SrcResult

    def SearchProjects(self, SearchMethod: int,SearchArgument: str):
        """ 
            Name: actiPyme.Driver.SearchProjects(SearchMethod: str, SearchArgument: str)

            Args:   SearchMethod, specify how you want to search: 1 - By Name; 2 - By task id; 3 - By customer id; 
                    SearchArgument, what you want to search as string

            Desc: This function lets you search for a task inside the actitime database. The output is a JSON object
        """
        MethodDict={1: "ByName", 2: "ByIds", 3: "ByCustomerIds"}
        if self.IsStarted:
            #switch on the dictionary   
            SrcMethTok=MethodDict.get(SearchMethod,"err")
            if SrcMethTok=="err":
                SrcResult={}
                raise Exception('Inappropriate or bad search method')
            elif SrcMethTok=="ByName":
                #Here we look for a name
                requrl=self.Target+"/projects?offset=0&words="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByIds":
                #Here we look for a project ID
                requrl=self.Target+"/projects?offset=0&ids="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByCustomerIds":
                #Here we look for a customer ID
                requrl=self.Target+"/projects?offset=0&customerIds="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            else:
                SrcResult={}
                raise Exception('Inappropriate or bad search method')    
        else:
            SrcResult={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return SrcResult



    def GetDayTimeTrack(self,usrIds: int, Year: int,Month: int,Day: int,TaskId:int):
        """ 
            Name: actiPyme.Driver.GetDayTimeTrack(self,usrIds: int, Year: int,Month: int,Day: int,TaskId:int)

            Args:   usrIds, user number for which you want to read the time sheet
                    Year, when you want to query timesheet data
                    Month, when you want to query timesheet data
                    Day, when you want to query timesheet data
                    TaskId, the identifier of the task (check actitime website)

            Desc: This function lets you query the data from actitime time sheet. The output is a JSON object

        """
        if  self.IsStarted: 
            assembler="-"
            dateQuery=assembler.join([str(Year),str(Month).zfill(2),str(Day).zfill(2)])
            requrl=self.Target+"/timetrack/"+str(usrIds)+"/"+dateQuery+"/"+str(TaskId)
            TtrackReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            TtrackData=json.loads(TtrackReq.text)   
        else:
            TtrackData={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return TtrackData

    def WriteDayTimeTrack(self,usrIds: int, Year: int,Month: int,Day: int,TaskId:int,TimeAsMinute: int,Comment: str):
        """ 
            Name: actiPyme.Driver.WriteDayTimeTrack(self,usrIds: int, Year: int,Month: int,Day: int,TaskId:int,TimeAsMinute: int,Comment: str)

            Args:   usrIds, user number for which you want to write the time sheet
                    Year, when you want to query timesheet data
                    Month, when you want to query timesheet data
                    Day, when you want to query timesheet data
                    TaskId, the identifier of the task (check actitime website)
                    TimeAsMinute, time spent on the task in minutes
                    Comment, comment to the task (empty string if no comment should be posted)

            Desc: This function lets you query the data from actitime time sheet. The output is a JSON object 

        """
        if  self.IsStarted:
            assembler="-"
            dateQuery=assembler.join([str(Year),str(Month).zfill(2),str(Day).zfill(2)])
            requrl=self.Target+"/timetrack/"+str(usrIds)+"/"+dateQuery+"/"+str(TaskId)
            #assemble data in json format
            dataToWrite= '{"time":' + str(TimeAsMinute) + ',"comment":"' + Comment + '"}'
            #finally write
            WtReq=requests.patch(requrl,headers=self.writeDefheaders,data=dataToWrite,auth=(self.actitimeUserName,self.actitimePsw))
            TtrackData=json.loads(WtReq.text)    
        else:
            TtrackData={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return TtrackData

    def GetTaskInfo(self, TaskId:int):
        """ 
            Name: actiPyme.Driver.GetTaskInfo(self, TaskId:int)

            Args:   TaskId, the ID number of the task 

            Desc: This function returns the info and the properties of a task. The output is a JSON object
        """
        if  self.IsStarted: 
            requrl=self.Target+"/tasks/"+str(TaskId)
            TaskInfoReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            TaskInfo=json.loads(TaskInfoReq.text)   
        else:
            TaskInfo={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return TaskInfo

    def GetActiTimeInfo(self):
        """ 
            Name: actiPyme.Driver.GetActiTimeInfo()

            Args:  Void

            Desc: Simply get the info about the actitime installation. The output is a JSON object
        """
        if  self.IsStarted: 
            requrl=self.Target+"/info/"
            ActiInfoReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            ActiInfo=json.loads(ActiInfoReq.text)   
        else:
            ActiInfo={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')
        return ActiInfo
    
    def DepartmentList(self):
        """ 
            Name: actiPyme.Driver.DepartmentList()

            Args:  Void

            Desc: Simply get the list of all departments. The output is a JSON object
        """
        if  self.IsStarted: 
            requrl=self.Target+"/departments/"
            DepInfoReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            DepInfo=json.loads(DepInfoReq.text)   
        else:
            DepInfo={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return DepInfo

    def GetDepartmentInfo(self,DepartmentId: int):
        """ 
            Name: actiPyme.Driver.GetDepartmentInfo(self,DepartmentId: int)

            Args:  DepartmentId, identification number of department

            Desc: get the info of one department. The output is a JSON object
        """
        if  self.IsStarted: 
            requrl=self.Target+"/departments/"+str(DepartmentId)
            DepInfoReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            DepInfo=json.loads(DepInfoReq.text)   
        else:
            DepInfo={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return DepInfo

    def GetProjectInfo(self, ProjectId: int):
        """ 
            Name: actiPyme.Driver.GetProjectInfo(self, ProjectId: int)

            Args:  ProjectId, identification number of the project

            Desc: get the info of one project. The output is a JSON object
        """
        if  self.IsStarted: 
            requrl=self.Target+"/projects/"+str(ProjectId)
            ProjInfoReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            ProjInfo=json.loads(ProjInfoReq.text)   
        else:
            ProjInfo={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return ProjInfo

    def SearchUsers(self, SearchMethod: int,SearchArgument: str):
        """ 
            Name: actiPyme.Driver.SearchUsers(SearchMethod: str, SearchArgument: str)

            Args:   SearchMethod, specify how you want to search: 1 - By Full Name; 2 - By user Id; 3 - By department; 4 - By email; 
                    SearchArgument, what you want to search as string

            Desc: This function lets you search for a task inside the actitime database. The output is a JSON object
        """
        MethodDict={1: "ByFullName", 2: "ByIds", 3: "ByDepartment", 4: "ByEmail"}
        if self.IsStarted:
            #switch on the dictionary   
            SrcMethTok=MethodDict.get(SearchMethod,"err")
            if SrcMethTok=="err":
                SrcResult={}
                raise Exception('Inappropriate or bad search method')
            elif SrcMethTok=="ByFullName":
                #Here we look for a full name
                requrl=self.Target+"/users?offset=0&name="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByIds":
                #Here we look for a user ID
                requrl=self.Target+"/users?offset=0&ids="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByDepartment":
                #Here we look for a department
                requrl=self.Target+"/users?offset=0&department="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            elif SrcMethTok=="ByEmail":
                #Here we look for an email addresss
                requrl=self.Target+"/users?offset=0&email="+SearchArgument
                SrcReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
                SrcResult=json.loads(SrcReq.text)
            else:
                SrcResult={}
                raise Exception('Inappropriate or bad search method')    
        else:
            SrcResult={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return SrcResult
    
    def GetLeaveTime(self, UserId: int,YearFrom: int,MonthFrom: int,DayFrom: int,YearTo: int,MonthTo: int, DayTo: int):
        """ 
            Name: actiPyme.Driver.GetLeaveTime(self, UserId: int,YearFrom: int,MonthFrom: int,DayFrom: int,YearTo: int,MonthTo: int, DayTo: int)

            Args:   userId, user number for which you want to read the time sheet
                    YearFrom, start date you want to query timesheet data
                    MonthFrom, start date want to query timesheet data
                    DayFrom, start date want to query timesheet data
                    YearTo, end date want to query timesheet data
                    MonthTo, end date want to query timesheet data
                    DayTo, end date want to query timesheet data

            Desc: This function lets you query the leave time from actitime time sheet. The output is a JSON object

        """

        if  self.IsStarted: 
            assembler="-"
            dateFrom=assembler.join([str(YearFrom),str(MonthFrom).zfill(2),str(DayFrom).zfill(2)])
            dateTo=assembler.join([str(YearTo),str(MonthTo).zfill(2),str(DayTo).zfill(2)])
            requrl=self.Target+"/leavetime?userIds="+str(self.IdNumber)+"&dateFrom="+dateFrom+"&dateTo="+dateTo
            LeaveReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            LeaveData=json.loads(LeaveReq.text)   
        else:
            LeaveData={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return LeaveData

    def GetTimeSheetDateInterval(self,  UserId: int,YearFrom: int,MonthFrom: int,DayFrom: int,YearTo: int,MonthTo: int, DayTo: int):
        """ 
            Name: actiPyme.Driver.GetTimeSheetDateInterval(self, UserId: int,YearFrom: int,MonthFrom: int,DayFrom: int,YearTo: int,MonthTo: int, DayTo: int)

            Args:   userId, user number for which you want to read the time sheet
                    YearFrom, start date you want to query timesheet data
                    MonthFrom, start date want to query timesheet data
                    DayFrom, start date want to query timesheet data
                    YearTo, end date want to query timesheet data
                    MonthTo, end date want to query timesheet data
                    DayTo, end date want to query timesheet data

            Desc: This function lets you query the time sheet of a user within a date interval. The output is a JSON object

        """
        if  self.IsStarted: 
            assembler="-"
            dateFrom=assembler.join([str(YearFrom),str(MonthFrom).zfill(2),str(DayFrom).zfill(2)])
            dateTo=assembler.join([str(YearTo),str(MonthTo).zfill(2),str(DayTo).zfill(2)])
            requrl=self.Target+"/timetrack?userIds="+str(self.IdNumber)+"&dateFrom="+dateFrom+"&dateTo="+dateTo
            TimesheetReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            TimesheetData=json.loads(TimesheetReq.text)   
        else:
            TimesheetData={}
            raise Exception('Communication not initialized. Run the Start() command on the driver instance')

        return TimesheetData


class AbfParser(object):
    """ 
    Name: actiPyme.AbfParser(FileName)

    Args:   FileName, actitime batch format (.abf) file to be read

    Desc:   This class implements the routines to load actitime time track data using a batch file.
            The batch file should be formatted as described below (comments are with % at the start of line)

                % actitime batch format file (.abf)
                % comments are with the percentage charachter
                % A. Lavatelli - 2019
                %First entry
                START ENTRY;
                USERNAME;john.doe;
                PASSWORD;FooBar18;
                START TIMESHEET;
                % format the timesheet as follows: year;month;day;task;hours;
                2019;8;19;558;1;
                2019;8;19;13619;7;
                END TIMESHEET;
                END ENTRY;
                %Here another entry
                START ENTRY;
                USERNAME;pippo.balera;
                PASSWORD;ggghhhh;
                START TIMESHEET;
                2019;7;12;108;1;
                2019;7;13;16509;7;
                2019;8;1;21;4;
                2019;8;3;009;3;
                END TIMESHEET;
                END ENTRY;
    
    """
    def __init__ (self,FileName):
        self.FileName=FileName
        # try to open file
        try:
            self.InputFile=open(self.FileName,"r")
        except:
            raise Exception('Impossible to open file')

        self.TimeSheetRowLimit=1000
    
    def Read(self):
        # remove comment lines
        ParsedRow=[]
        for InpLine in self.InputFile:
            if InpLine[0]!="%":
                # remove \n
                JustInp=InpLine.split("\n")[0]
                ParsedRow.append(JustInp)

        #initialize the data structure
        timeSheetTemplate={'year': 0,'month':0,'day': 0,'task':0,'hours':0}
        actiItem={'user':'','psw':'','timesheet': []}
        actiData=[]
        timeSheetList=[]
        Nrows=len(ParsedRow)
        WorkRow=0
        EntryCounter=0
        #here you parse the input file
        while WorkRow<Nrows:
            Command=ParsedRow[WorkRow].split(';')
            if Command[0]=="START ENTRY":
                actiData.append(actiItem)
                # get username
                WorkRow+=1
                Command=ParsedRow[WorkRow].split(';')
                if Command[0]=="USERNAME":
                    actiItem['user']=Command[1]
                else:
                    raise ValueError("Input file formatted in the wrong manner. Expected USERNAME after START ENTRY")
                #get psw
                WorkRow+=1
                Command=ParsedRow[WorkRow].split(';')
                if Command[0]=="PASSWORD":
                    actiItem['psw']=Command[1]
                else:
                    raise ValueError("Input file formatted in the wrong manner. Expected PASSWORD after USERNAME")
                # retrieve time sheet
                WorkRow+=1
                Command=ParsedRow[WorkRow].split(';')
                if Command[0]=="START TIMESHEET":
                    TimeSheetRowCounter=0
                    while Command[0]!="END TIMESHEET":
                        WorkRow+=1
                        
                        # put a limit to the while cycle
                        if TimeSheetRowCounter>self.TimeSheetRowLimit:
                            raise  ValueError("Too many time sheet rows or maybe something wrong in the formatting of input file. Check the existance of the END TIMESHEET tag")
                        Command=ParsedRow[WorkRow].split(';')
                        # dump the time sheet data into the output array
                        if Command[0]!="END TIMESHEET":
                            timeSheetList.append(timeSheetTemplate)
                            timeSheetTemplate["year"]=int(Command[0])
                            timeSheetTemplate["month"]=int(Command[1])
                            timeSheetTemplate["day"]=int(Command[2])
                            timeSheetTemplate["task"]=int(Command[3])
                            timeSheetTemplate["hours"]=int(Command[4])
                            TimeSheetLineAsJsonStr=json.dumps(timeSheetTemplate)
                            timeSheetList[TimeSheetRowCounter]=json.loads(TimeSheetLineAsJsonStr)
                            TimeSheetRowCounter+=1
                    
                    actiItem["timesheet"]=timeSheetList                  
                else:
                    raise ValueError("Input file formatted in the wrong manner. Expected START TIMESHEET after PASSWORD")
                #update counters
                WorkRow+=1
                Command=ParsedRow[WorkRow].split(';')
                if Command[0]=="END ENTRY":
                    # dump the acti time entry in the output structure (JSON format)
                    actiDataAsJsonStr=json.dumps(actiItem)
                    actiData[EntryCounter]=json.loads(actiDataAsJsonStr)
                    EntryCounter+=1

            WorkRow+=1

        return(actiData)

    def Close(self):
        self.InputFile.close()