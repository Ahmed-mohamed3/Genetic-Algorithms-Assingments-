        import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



fuzzy_dict = {'var_dict': [], 'sets_dict': [], 'rules_dict': []}

def Main_Menu():
    flag = 1
    while flag == 1:
        print("Main Menu")
        print("=========")
        print("1 - Add variables")
        print("2 - Add fuzzy sets to an existing variable")
        print("3 - Add rules")
        print("4 - Run the simulation on crisp values")
        print()
        user_input = input("Enter Choice: ")
        if user_input == '1':
            Add_variables()
        elif user_input == '2':
            Add_fuzzy_sets()
        elif user_input == '3':
            Add_rules()
        elif user_input == '4':
            all_in_one()
        elif user_input == 'ESC':
            print("Exiting")
            flag = 0
        else:
            print("Invalid input")

def first_message():
    first_message = "Fuzzy Logic Toolbox\n"
    delim = "=" * len(first_message)
    all_text = first_message+delim
    print(all_text)
    print("1 - Creeate a new fuzzy system")
    print("2 - Quit")
    user_input = input("Enter Choice: ") 
    return user_input

def receive_input():
    sys_name = input("Enter the system's name: ")
    sys_description = input("Enter the system's description: ")
    return sys_name, sys_description

def Add_variables():
        print("Add variables chosen")
        print("Enter the  variable's name, type (IN or OUT) and range [LOW,HIGH]")
        print ("press x to finish")
        delim = "=" * 25
        print(delim)
        list_of_vars = []
        while True:
            var = input()
            if var == 'x':
                break
            else:
                splitted_var = var.split()
                low = float(splitted_var[2].replace('[', '').replace(',', ''))
                high = float(splitted_var[3].replace(']', ''))
                list_of_vars.append([splitted_var[0], splitted_var[1], low, high])
        for var in list_of_vars:
            fuzzy_dict ['var_dict'].append(var)

def Add_fuzzy_sets():
        print("Enter the variable's name")
        delim = "=" * 25
        print(delim)
        var_name = input()
        print("Enter the fuzzy set name, type (TRI/ TRAP) and values")
        print ("press x to finish")
        print(delim)
        fuzzy_sets = []
        flag = 0
        for var in fuzzy_dict ['var_dict']:
            if var[0] == var_name:
                flag = 1
        while True and flag == 1:
            float_list = []
            fuzzy_set = input()
            if fuzzy_set == 'x':
                break
            else:
                splitted_fuzzy_set = fuzzy_set.split()
                for x in range(2, len(splitted_fuzzy_set)):
                    float_list.append(float(splitted_fuzzy_set[x]))
                fuzzy_sets.append([var_name,splitted_fuzzy_set[0], splitted_fuzzy_set[1], float_list])
        for fuzzy_set in fuzzy_sets:
            fuzzy_dict ['sets_dict'].append(fuzzy_set)

        if flag == 0:
            print("Variable does not exist")

def Add_rules():
        print("Enter the rule in this format : press x to finish")
        print("IN_variable set operator IN_variable set =>  OUT_variable set")
        rules = []
        while True:
            rule = input()
            if rule == 'x':
                break
            else:
                splitted_rule = rule.split()
                # proj_funding high or exp_level expert => risk low
                rules.append([
                    [splitted_rule[0],splitted_rule[1]], # In_Variable_1,
                    splitted_rule[2], # Operator,
                    [splitted_rule[3],splitted_rule[4]], # In_Variable_2,
                    [splitted_rule[6],splitted_rule[7]] # Out_Variable
                    ])
        for rule in rules:
            fuzzy_dict ['rules_dict'].append(rule)



def all_in_one():
    print ('Enter the crisp values:')
    delim = "=" * 25
    print(delim)
    crisp  = {}
    for value in fuzzy_dict["var_dict"]:
        if value[1] == "IN":
            crisp_value = input(value[0] + ": ")
            crisp[value[0]] = float(crisp_value)
    fuzzy_dict['crisp'] = crisp
    all_crisp_cases = fuzzification(crisp)
    after_inference = inference(all_crisp_cases)
    x = centroid(after_inference)
    output_dict = calc_weighted_mean_avg(after_inference, x)
    text = ""
    for key, value in output_dict.items():
        text += str(key) + " "
        for x in value:
            text += str(x) + " "
        text += "\n"
    print(text)
    plotting(all_crisp_cases, crisp, output_dict['risk'][0])
    return output_dict

def draw_lines():
    
    vars_equations_dict = {}

    for value in fuzzy_dict["var_dict"]:
        flag = 1
        equations_list = {}
        if value[1] == "IN":
            var_name = value[0]
            for set in fuzzy_dict["sets_dict"]:
                if set[0] == var_name:
                    if set[2] == "TRI":
                        # num_lines = 2
                        points = set[3]
                        # (y2-y1)/(x2-x1)
                        flag  = 0
                        for num_1 in range(0, len(points)):
                            for num_2 in range (num_1+1, len(points)):
                                if points[num_1] == points[num_2]:
                                    flag = 1
                        left = 0
                        right = 0
                        if flag == 1:
                            if points[0] == points[1]:
                                right = 1
                            elif points[1] == points[2]:
                                left = 1
                        if right == 1:
                            m = (0-1) / (points[2] - points[1])
                            b = 1- m * points[1]
                            equations_list[set[1]] = [None, [m, b]] 
                        elif left == 1:
                            m = (1-0) / (points[2] - points[0])
                            b = 0- m * points[0]
                            equations_list[set[1]] = [[m, b], None]
                        else :
                            m = (1-0) / (points[1] - points[0])
                            b = 0- m * points[0]
                            left_line = [m,b]
                            m = (0-1) / (points[2] - points[1])
                            b = 1- m * points[1]
                            right_line = [m,b]
                            equations_list[set[1]] = [left_line, right_line]
                        
                    elif set[2] == "TRAP":
                        points = set[3]
                        flag  = 0
                        for num_1 in range(0, len(points)):
                            for num_2 in range (num_1+1, len(points)):
                                if points[num_1] == points[num_2]:
                                    flag = 1
                        left = 0
                        right = 0
                        if flag == 1:
                                if points[0] == points[1]:
                                    right = 1
                                elif points[2] == points[3]:
                                    left = 1
                        if right == 1:
                                m = (0-1) / (points[3] - points[2])
                                b = 1- m * points[2]
                                equations_list[set[1]] = [None, [0,1] , [m, b]] 
                        elif left == 1:
                                m = (1-0) / (points[1] - points[0])
                                b = 0- m * points[0]
                                equations_list[set[1]] = [[m, b], [0,1] ,None]
                        else :
                                m = (1-0) / (points[1] - points[0])
                                b = 0- m * points[0]
                                left_line = [m,b]
                                m = (0-1) / (points[3] - points[2])
                                b = 1- m * points[2]
                                right_line = [m,b]
                                equations_list[set[1]] = [left_line, [0,1] , right_line]       
        else:
            flag = 0

        if flag == 1:
            vars_equations_dict[var_name] = equations_list
    return vars_equations_dict

def calc_crisp(vars_equations_dict, crisp_value):

    all_cases = {}
    for key, value in crisp_value.items():
        intersection_points = {}
        for set, equationn in vars_equations_dict.items():
            if key == set :
                x = value 
                points = []
                if key == 'exp_level':
                    z = 2
                for set_name, equation in equationn.items():
                    for a_list in fuzzy_dict["sets_dict"]:
                        if a_list[0] == set and a_list[1] == set_name:
                            points = a_list[-1]
                            break
                    flag_2 = 1
                    for i in range (len(points)):
                        flag = 0
                        y = 0 
                        for j in range (i+1, len (points)):
                            if (x >= points[j-1]) and (x <=  points[j]):
                                if equation[j-1] == None:
                                    continue
                                elif equation[j-1] != None:
                                    y = equation[j-1][0] * x + equation[j-1][1]
                                    intersection_points[set_name] = y
                                    flag = 1
                                    flag_2 = 0
                                    break
                        if flag == 1:
                            break
                    if (flag_2 == 1):
                        intersection_points[set_name] = y    

        all_cases[key] = intersection_points
    return all_cases
                       
def fuzzification(crisp_value):
    vars_equations_dict = draw_lines()
    all_crisp_cases = calc_crisp(vars_equations_dict, crisp_value)
    print ('Fuzzification => done')

    return all_crisp_cases

def inference(all_crisp_cases):

    accumulate = []
    for rule in fuzzy_dict["rules_dict"]:
        var_1 = rule[0][0]
        set_1 = rule[0][1]
        operator = rule[1].upper()
        var_2 = rule[2][0]
        set_2 = rule[2][1]
        var_3 = rule[3][0]
        set_3 = rule[3][1]
        key = var_3 + set_3
        if operator == "AND":
            accumulate.append([key,min(all_crisp_cases[var_1][set_1], all_crisp_cases[var_2][set_2])])
        elif operator == "OR":
            accumulate.append([key,max(all_crisp_cases[var_1][set_1], all_crisp_cases[var_2][set_2])])
        elif operator == "NOT":
            accumulate.append( [key,1 - all_crisp_cases[var_1][set_1]])
        elif operator == "AND_NOT":
            accumulate.append( [key,min(all_crisp_cases[var_1][set_1], 1 - all_crisp_cases[var_2][set_2])])
        elif operator == "OR_NOT":
            accumulate.append([key,max(all_crisp_cases[var_1][set_1], 1 - all_crisp_cases[var_2][set_2])])
    keyys = []
    for key,_ in accumulate:
        keyys.append(key)
    keyys = list(set(keyys))
    after_inference = {}
    for key in keyys:
        values = []
        for var, val in accumulate:
            if key == var:
                values.append(val)
        after_inference[key] = max(values)
    
    print ('Inference => done')
    return after_inference

def centroid(after_inference):
    final_result = {}
    for var, val in after_inference.items():
            for a_list in fuzzy_dict["sets_dict"]:
                if a_list[0]+a_list[1] == var :
                    points = a_list[-1]
                    break
            if len(points) == 2:
                final_result[var] = (points[0] + points[1]) / 2
            elif len(points) == 3:
                final_result[var] = (points[0] + points[1] + points[2]) / 3
            elif len(points) == 4:
                final_result[var] = (points[0] + points[1] + points[2] + points[3]) / 4
    return final_result
    
def calc_weighted_mean_avg(after_inference, final_result):
    output = []
    for item in fuzzy_dict["var_dict"]:
        if item[1] == "OUT":
            output.append(item[0])
    output_dict = {}
    for var in output:
        denominator = 0
        numerator = 0
        x = -1000
        y = ""

        for key,value in after_inference.items():
            if var in key:
                denominator += value
                if value > x :
                    x = value
                    y = key
        
        for key, value in after_inference.items():
            if var in key:
                numerator += value * final_result[key]
        output_dict[var] = [numerator / denominator,var + " is "+y.replace(var,"")]
    return output_dict

def CountFrequency(my_list):
 
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq

def plotting (crisp, crisp_values_for_plot, y, file_name):
    list_of_colors = [ "Blue",  "Violet", "Red","Green", 'cyan','orange']
    temp_for_sets = []
    for set in fuzzy_dict['sets_dict']:
        temp_for_sets.append(set[0])
    freq_in_sets = CountFrequency(temp_for_sets)
    visited = []
    fig, axs = plt.subplots(3)
    fig.set_size_inches(18.5, 10.5)
    shape_number = 0
    for set in fuzzy_dict['sets_dict']:
        
        if set[0] not in visited:     
            visited.append(set[0])   
            axs[shape_number].set_title(f"line graph for {set[0]}")  # add title
            
            counter = freq_in_sets[set[0]]
            if set[2] == 'TRI':
                shape = [0,1,0]
            elif set[2] == 'TRAP':
                shape = [0,2,2,0] 
            c = 0
            for item in fuzzy_dict['sets_dict']: 
                if c != counter:
                    if item[0] == set[0]:
                        c+=1
                        if item[2] == 'TRAP':
                            for fuzzy in fuzzy_dict['var_dict']:
                                if (fuzzy[0] == item[0]) and (fuzzy[1] == 'IN'):
                                    point = [[crisp_value_x, crisp_value_x], [0, crisp_value_y]],[[0,crisp_value_x ],[crisp_value_y, crisp_value_y]]
                                    crisp_value_y = float(crisp[item[0]][item[1]])
                                    crisp_value_x = float(crisp_values_for_plot[item[0]])
                                    if (crisp_value_y > 0):
                                        point = [[crisp_value_x, crisp_value_x], [0, crisp_value_y]],[[0,crisp_value_x ],[crisp_value_y, crisp_value_y]]
                                        axs[shape_number].plot(point[0][0],point[0][1], color = 'black', linestyle = 'dotted') 
                                        axs[shape_number].plot(point[1][0],point[1][1], color = 'black', linestyle = 'dotted')
                                        break
                            axs[shape_number].plot([item[3][0],item[3][1]], [0,1], color = list_of_colors[c])
                            axs[shape_number].plot([item[3][1],item[3][2]],[1,1], color = list_of_colors[c])
                            axs[shape_number].plot([item[3][2],item[3][3]], [1,0], color = list_of_colors[c], label = item[1])
                            axs[shape_number].legend(loc="upper right")
                        if item[2] == 'TRI':
                            for fuzzy in fuzzy_dict['var_dict']:
                                if (fuzzy[0] == item[0]) and (fuzzy[1] == 'IN'):
                                    crisp_value_y = float(crisp[item[0]][item[1]])
                                    crisp_value_x = float(crisp_values_for_plot[item[0]])
                                    if (crisp_value_y > 0):
                                        point = [[crisp_value_x, crisp_value_x], [0, crisp_value_y]],[[0,crisp_value_x ],[crisp_value_y, crisp_value_y]]
                                        axs[shape_number].plot(point[0][0],point[0][1], color = 'black', linestyle = 'dotted') 
                                        axs[shape_number].plot(point[1][0],point[1][1], color = 'black', linestyle = 'dotted')
                                if (fuzzy[0] == item[0]) and (fuzzy[1] == 'OUT'):
                                    crisp_value_x = float(y)
                                    axs[shape_number].plot([y,y],[0,1], color = 'black', linestyle = 'dotted') 
                            axs[shape_number].plot([item[3][0], item[3][1]], [0, 1], color = list_of_colors[c])
                            axs[shape_number].plot([item[3][1], item[3][2]], [1, 0], color = list_of_colors[c], label = item[1])
                            axs[shape_number].legend(loc="upper right")
                else :
                    break
            shape_number+=1
        else:
            continue
    file_name = file_name.split('\\')[0:-1]
    output_name_file = "\\".join(file_name)
    output_name_file = output_name_file +'\plot.png'
    plt.savefig(output_name_file , dpi=300, bbox_inches='tight')
    plt.legend()
    plt.show() 

        
def read_file(filename):
    delims = [
    "end_variables",
    "end_var_set",
    "end_all_sets",
    "end_rules",
    "end_crisp"
    ]
    delims_pos = {d: [] for d in delims}
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for i, line in enumerate(content):
        for d in delims:
            if d in line:
                delims_pos[d].append(i)
    
    
    variable_lines = content[:delims_pos["end_variables"][0]]
    sets_lines = content[delims_pos["end_variables"][0]+1:delims_pos["end_all_sets"][0]]
    rules_lines = content[delims_pos["end_all_sets"][0]+1:delims_pos["end_rules"][0]]
    crisp_lines = content[delims_pos["end_rules"][0]+1:delims_pos["end_crisp"][0]]
    fuzzy_sets = []
    a = []
    a.append(delims_pos["end_variables"][0]+1)
    a.extend(delims_pos["end_var_set"])
    for i in range(len(a)-1):
        z = content[a[i]:a[i+1]]
        if "end_var_set" in z:
            z.remove("end_var_set")
        fuzzy_sets.append(z)
    
    # adding variables to the dictionary
    list_of_vars = []
    for var in variable_lines:
        splitted_var = var.split()
        low = float(splitted_var[2].replace('[', '').replace(',', ''))
        high = float(splitted_var[3].replace(']', ''))
        list_of_vars.append([splitted_var[0], splitted_var[1], low, high])
    
    for var in list_of_vars:
        fuzzy_dict ['var_dict'].append(var)

    fuzzfuzz = []
    # adding fuzzy sets to the dictionary
    for fuzzy_set in fuzzy_sets:
        var_name = fuzzy_set[0]
        fuzzy_set.remove(var_name)
        for line in fuzzy_set:
            float_list = []
            splitted_fuzzy_set = line.split()
            for x in range(2, len(splitted_fuzzy_set)):
                float_list.append(float(splitted_fuzzy_set[x]))
            fuzzfuzz.append([var_name,splitted_fuzzy_set[0], splitted_fuzzy_set[1], float_list])
    for fuzzy_set in fuzzfuzz:
        fuzzy_dict ['sets_dict'].append(fuzzy_set)

    # adding rules to the dictionary
    rules = []
    for rule in rules_lines:
        splitted_rule = rule.split()
        rules.append([
                    [splitted_rule[0],splitted_rule[1]], # In_Variable_1,
                    splitted_rule[2], # Operator,
                    [splitted_rule[3],splitted_rule[4]], # In_Variable_2,
                    [splitted_rule[6],splitted_rule[7]] # Out_Variable
                    ])
    
    for rule in rules:
            fuzzy_dict ['rules_dict'].append(rule)
    
    # adding crisp values to the dictionary
    crisp = {}
    for crisp_value in crisp_lines:
        splitted_crisp = crisp_value.split()
        crisp[splitted_crisp[0]] = float(splitted_crisp[1])
    crisp_keys = list(crisp.keys())
    inputs = []
    for var in fuzzy_dict['var_dict']:
        if var[1] == 'IN':
            inputs.append(var[0])
    
    for val in inputs:
        if val not in crisp_keys:
            crisp[val] = 0
    fuzzy_dict ['crisp_dict'] = crisp    

def output_file(filename):
    all_crisp_cases = fuzzification(fuzzy_dict['crisp_dict'])

    after_inference = inference(all_crisp_cases)
    x = centroid(after_inference)
    output_dict = calc_weighted_mean_avg(after_inference, x)
    text = ""
    for key, value in output_dict.items():
        text += str(key) + " "
        for x in value:
            text += str(x) + " "
        text += "\n"
    with open(filename, "w") as text_file:
        text_file.write(text)
    my_output = ""
    for key , value in output_dict.items():
        my_output = value[0]
    
    plotting(all_crisp_cases, fuzzy_dict['crisp_dict'], my_output, filename)
    return output_dict


#Add_variables()
#Add_fuzzy_sets()
#Add_rules()
#crisp , crisp_values_for_plot= simulation()
#after_inference = inference(crisp)
#x = centroid(after_inference)
#output_dict = calc_weighted_mean_avg(after_inference, x)
#print(output_dict['risk'][0],output_dict['risk'][1])


# read_file(r'F:\sana 4\GA\assignments\Assignment 3\New folder\input.txt')
# output_file(r'F:\sana 4\GA\assignments\Assignment 3\New folder\output.txt')

#print("hi")
# print("Enter ESC to exit")
# Main_Menu()

# ______________________________________________________________
# Menu
from tkinter.ttk import *
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import *

#!/usr/bin/python
import tkinter, time
from subprocess import Popen
import tkinter.font as font

Freq = 2500
Dur = 150

top = tkinter.Tk()
top.title('Fuzzy logic system')
top.geometry('400x200') # Size 200, 200


file_name = ''
def start():
    import os
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    file_name = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#    os.system("python test.py")
    # function to open a new window
    read_file(file_name)
    file_name = file_name.split('/')[0:-1]
    output_name_file = "\\".join(file_name)
    output_name_file = output_name_file +'\output.txt'
    my_output = output_file(output_name_file)
    openNewWindow(my_output)




# on a button click
def openNewWindow(output_dict):
    texts = ''
    for key, value in output_dict.items():
        texts += str(key) + " "
        for x in value:
            texts += str(x) + " "
        texts += "\n"
    
    
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(top)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("400x100")
    
    # A Label widget to show in toplevel
    Label(newWindow,
          text =f"The result is: \n {texts} ", font = 15).pack()

myFont = font.Font(size=15)
startButton = tkinter.Button(top, height=4, width=50, text ="Choose the input file (.txt)", 
command = start, bg='#0052cc', fg='#ffffff', font= myFont)

quitbutton = Button(top, text="Quit", height=4, width=50 ,command=top.destroy, bg='#0052cc', fg='#ffffff', font = myFont) #button to close the window

startButton.pack()
quitbutton.pack()
top.mainloop()
