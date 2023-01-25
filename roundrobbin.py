from prettytable import PrettyTable
from tkinter import *
class RoundRobin:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x500" )
        promt_frame = Frame(self.window)
        label = Label(promt_frame , text = "enter number of processes " , font = ("bold" , 15))
        self.entry = Entry(promt_frame , width = 20)
        label.pack(side='left')
        self.entry.pack(side='left')
        promt_frame.pack()
        button = Button(self.window , command = self.processData , text = "enter" , font = ("bold" , 17) , fg='white' , bg='gray')
        button.pack()
        self.list = []
        self.process_data = []
        self.time_slice = ""
        mainloop()
    def processData(self):
        input_frame = Frame(self.window)
        n= self.entry.get()
        temp = []
        h_label =  Label(input_frame , text = "enter data of processes" , font = ("bold" , 15))
        h_label.pack()
        head_frame = Frame(input_frame )
        l =Label(head_frame , text = "ID" , width = 10)
        l.pack(side = "left")
        l =Label(head_frame , text = "AT" , width = 10)
        l.pack(side = "left")
        l =Label(head_frame , text = "BT" , width = 10)
        l.pack(side = "left")
        head_frame.pack()
        for i in range(int(n)):
            frame = Frame(input_frame)
            for j in range(3):
                entry = Entry(frame , width = 10)
                entry.pack(side = "left")
                temp.append(entry)
            self.list.append(temp)
            temp=[]
            frame.pack(side = "top")
        t_s_frame = Frame(input_frame)
        t_s_label = Label(t_s_frame , text = "enter time slice" , font = ("bold" , 15))
        t_s_label.pack(side = "left")
        self.time_slice = Entry(t_s_frame)
        self.time_slice.pack(side="left")
        t_s_frame.pack()
        button = Button(input_frame  ,  command = self.initialize , text = "apply algorithm" , font = ("bold" , 17), fg='white' , bg='gray')
        button.pack()
        input_frame.pack()
    def initialize(self):
        temp = []
        for i in range(int(self.entry.get())):
            for j in range(len(self.list[i])):
                value = int(self.list[i][j].get())
                temp.append(value)
                if j == 2:
                    temp.extend([0 , value])
            self.process_data.append(temp)
            temp = []
            print(self.process_data)
        RoundRobin.schedulingProcess(self, self.process_data, self.time_slice)

    def schedulingProcess(self, process_data, time_slice):
        start_time = []
        exit_time = []
        executed_process = []
        ready_queue = []
        process_data.sort(key=lambda x: x[1]) #sort processes according to arrival time
        s_time= process_data[0][1]
        while 1:
            temp = []
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    present = 0
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if process_data[i][0] == ready_queue[k][0]:
                                present = 1
                    '''
                    The above if loop checks that the next process is not a part of ready_queue
                    '''
                    if present == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                        ready_queue.append(temp)
                        temp = []
                    '''
                    The above if loop adds a process to the ready_queue only if it is not already present in it
                    '''
                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                    '''
                    The above if loop makes sure that the recently executed process is appended at the end of ready_queue
                    '''
            if len(ready_queue) == 0:
                break
            if len(ready_queue) != 0:
                if ready_queue[0][2] > int(time_slice.get()):
                    #If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                    start_time.append(s_time)
                    #s_time = s_time + int(time_slice.get())
                    #e_time = s_time
                    #exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    if process_data[j][2]==process_data[j][4]:
                        process_data[j].append(s_time-process_data[j][1])
                    process_data[j][2] = process_data[j][2] - int(time_slice.get())
                    ready_queue.pop(0)
                    s_time = s_time + int(time_slice.get())
                    e_time = s_time
                    exit_time.append(e_time)
                elif ready_queue[0][2] <= int(time_slice.get()):
                    #If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                    start_time.append(s_time)
                    #s_time = s_time + ready_queue[0][2]
                    #e_time = s_time
                    #exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    if process_data[j][2]==process_data[j][4]:
                        process_data[j].append(s_time-process_data[j][1])
                    s_time = s_time + ready_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
                    ready_queue.pop(0)
            
        for i in range(len(process_data)):
            turnaround_time = process_data[i][6] - process_data[i][1] #turnaround_time = completion_time - arrival_time
            process_data[i].append(turnaround_time)
        for i in range(len(process_data)):
            waiting_time = process_data[i][7] - process_data[i][4] #waiting_time = turnaround_time - burst_time
            process_data[i].append(waiting_time)
        RoundRobin.printData(self, process_data, executed_process)
    def printData(self, process_data, executed_process):
        hd = ["P_ID ","Arival_time","BTime","RT"," CTime","TATime","WT"]
        frame = Frame(self.window)
        hd_frame = Frame(frame)
        for x in range(len(hd)):
            label = Label(hd_frame , text = hd[x] , width = 10)
            label.pack(side = "left")
        hd_frame.pack(side = "top")
        for i in range(len(process_data)):
            frame2 = Frame(frame)
            for j in range(len(process_data[i])):
                if j == 2 or j ==3:
                     continue
                label = Label(frame2 , text = process_data[i][j] , width = 10)
                label.pack(side = "left")
            frame2.pack(side = "top")
        frame.pack()
if __name__ == "__main__":
    rr = RoundRobin()
