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


    def Start(self):
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

    def CustomerList(self):
        """ 
            Just get the customers list.
            Json object as output
        """
        if  self.IsStarted:   
            requrl=self.Target
            requrl+="/customers"
            CustReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            Clients=json.loads(CustReq.text)
        else:
            Clients="Communication not initialized. Execute the Start command"
        
        return Clients

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
                raise ValueError('Inappropriate or bad search method')
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
                raise ValueError('Inappropriate or bad search method')    
        else:
            SrcResult=False

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
                raise ValueError('Inappropriate or bad search method')
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
                raise ValueError('Inappropriate or bad search method')    
        else:
            SrcResult=False

        return SrcResult



    def GetDayTimeTrack(self, Year: int,Month: int,Day: int,TaskId:int):
        """ 
            Name: actiPyme.Driver.GetDayTimeTrack(Year: int,Month: int,Day: int,TaskId:int)

            Args:   Year, when you want to query timesheet data
                    Month, when you want to query timesheet data
                    Day, when you want to query timesheet data
                    TaskId, the identifier of the task (check actitime website)

            Desc: This function lets you query the data from actitime time sheet. The output is a JSON object

        """
        if  self.IsStarted: 
            assembler="-"
            dateQuery=assembler.join([str(Year),str(Month).zfill(2),str(Day).zfill(2)])
            requrl=self.Target+"/timetrack/"+str(self.IdNumber)+"/"+dateQuery+"/"+str(TaskId)
            TtrackReq=requests.get(requrl,headers=self.ServerHeaders,auth=(self.actitimeUserName,self.actitimePsw))
            TtrackData=json.loads(TtrackReq.text)   
        else:
            TtrackData=False

        return TtrackData

    def WriteDayTimeTrack(self, Year: int,Month: int,Day: int,TaskId:int,TimeAsMinute: int,Comment: str):
        """ 
            Name: actiPyme.Driver.WriteDayTimeTrack(Year: int,Month: int,Day: int,TaskId:int,TimeAsMinute: int,Comment: str)

            Args:   Year, when you want to query timesheet data
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
            requrl=self.Target+"/timetrack/"+str(self.IdNumber)+"/"+dateQuery+"/"+str(TaskId)
            #assemble data in json format
            dataToWrite= '{"time":' + str(TimeAsMinute) + ',"comment":"' + Comment + '"}'
            #finally write
            WtReq=requests.patch(requrl,headers=self.writeDefheaders,data=dataToWrite,auth=(self.actitimeUserName,self.actitimePsw))
            TtrackData=json.loads(WtReq.text)    
        else:
            TtrackData=False

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
            TaskInfo=False

        return TaskInfo