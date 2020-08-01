#Data Processing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
memory = pd.read_csv('data_memory.csv')
control = pd.read_csv('data_control.csv')

#remove bad subjects - found previously
excludedSubjects = [5, 21, 38, 72] #pids of bad subjects

#remove bad subjects from memory dataframe
bad_mem_indices = []
for indx in range (0, len(memory['pid'])):
    curr_pid = memory['pid'][indx]
    is_bad = False
    for subject in excludedSubjects:
        if curr_pid == subject:
            is_bad = True
    if is_bad:
        bad_mem_indices.append(indx)
memory = memory.drop(bad_mem_indices)

#remove bad subjects from control dataframe
bad_con_indices = []
for indx in range (0, len(control['pid'])):
    curr_pid = control['pid'][indx]
    is_bad = False
    for subject in excludedSubjects:
        if curr_pid == subject:
            is_bad = True
    if is_bad:
        bad_con_indices.append(indx)
control = control.drop(bad_con_indices)


#function to find the trial tyoes for the previous trial givne the pid and picid
def find_prev_trial (mem_pid, mem_picid):
    for i in range (1, len(control['pid'])):
        if control['pid'][i] == mem_pid:
            if control['picid'][i] == mem_picid:
                return (control['congruency'][i-1], control['response'][i-1])
    
    return('-','-') #if this fails for any reason


#determines ratio of "1" responses to total responses in that category
def accuracy(response_list):
    accurate = [i for i in response_list if i == 1]
    return(len(accurate)/len(response_list))


#find accuracy for the individual subject
def subject_accuracy(curr_ID, memory):
    #initialize arrays for different trial types
    congruent_go = []
    congruent_nogo = []
    incongruent_go = []
    incongruent_nogo = []
    
    #find memory accuracy in relation to previous trial type
    for i in range (1, len(memory['pid'])):
        if (memory['pid'][i] == curr_ID) and (memory['memCond'][i] == "old"):
            prev_conditions = find_prev_trial(memory['pid'][i], memory['picid'][i])
            response = memory['sbjACC'][i]
            if prev_conditions[0] != '-':
                if prev_conditions[0] == "congruent":
                    if prev_conditions[1] == "go":
                        congruent_go.append(response)
                    else:
                        congruent_nogo.append(response)
                else:
                    if prev_conditions[1] == "go":
                        incongruent_go.append(response)
                    else:
                        incongruent_nogo.append(response)
    
    accuracies = [accuracy(congruent_go), accuracy(congruent_nogo), accuracy(incongruent_go), accuracy(incongruent_nogo)]
    return accuracies

#Responses will be contained in this two dimensional list so that it is in the 
# order of congruent_go, congruent_nogo, incongruent_go, incongruent_nogo lists
all_accuracies = [[],[],[],[]]

#get accuracies for each participant and then put into all_accuracies 
'''
pid_list = np.arange(84).tolist()
pid_list = [x+1 for x in pid_list if x+1 not in excludedSubjects]
'''
pid_list = memory.pid.unique().tolist()
print(pid_list)

for ID in pid_list:
    individ_acc = subject_accuracy(ID, memory.copy())
    for i in range(4):
        all_accuracies[i].append(individ_acc[i])
        
print(all_accuracies)
     

'''
#plot the relationship

labels = ('congruent go', 'congruent nogo', 'incongruent go', 'incongruent nogo')
y_pos = np.arange(len(labels))
accuracies = [accuracy(congruent_go), accuracy(congruent_nogo), accuracy(incongruent_go), accuracy(incongruent_nogo)]

plt.figure(1)
plt.bar(y_pos, accuracies)
plt.xticks(y_pos, labels)
plt.ylabel("Memory Accuracy")
plt.xlabel("N-1 Trial Type")
plt.title("Memory Accuracy vs. N-1 Trial Type")
for i in range(len(accuracies)):
    plt.text(x=y_pos[i], y=accuracies[i] + 0.01, s=round(accuracies[i], 3), size=10)
plt.show()

plt.figure(2)
plt.bar(y_pos, accuracies)
plt.xticks(y_pos, labels)
plt.ylabel("Memory Accuracy")
plt.xlabel("N-1 Trial Type")
plt.title("Memory Accuracy vs. N-1 Trial Type")
plt.ylim(.5, .6)
plt.show()
'''
