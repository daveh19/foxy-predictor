from subprocess import call
import pandas as pd
import os
from wahlrecht_polling_firms import get_tables
from model_class import model
from Plotting_function import plot_graphs
import numpy as np
#from very_simple_predictor import simple_model
#from very_simple_predictor import make_smart_panda


def header():
    call(["clear"])
    call(["figlet", "Foxy Predictor"])
    print("------------------------------------------------------------------")
    print("Here we might want to put some boring information")
    print("------------------------------------------------------------------")
    call(["cowsay", "Welcome to the Foxy Predictor. Type 'D' to check the web for new data, type 'P' to start a new  or 'H' for help."])

def get_new_data(path):
    print('Downloading new data......')
    table = get_tables()
    all_inst = []

    for key ,values in table.items() :
        print('Collect data from:', key)
        all_inst.append(key)
        table[key].to_csv(path_or_buf = path + '/' + key+ '.csv')
    print('done')

    return all_inst

def choose_inst(all_inst, path):
    use_inst = []
    print('choose which firms to use (y/n): \n')
    for k in range(len(all_inst)):
        ans = input("%s: " % all_inst[k] )
        if ans == 'y':
            use_inst.append(all_inst[k])
    data = {}
    for ui in use_inst:
        survey_data = pd.read_csv(path + '/' + ui + '.csv')
        data[ui] = survey_data
    return use_inst, data


def choose_model(model_list_path):
    ml = open(model_list_path, 'r')
    models = []
    print('\n\nAvailable models: ')

    for i, line in enumerate(ml):
        print(i+1, line)
        models.append(line.split()[0])
    ml.close()

    print('Please enter the number of the model you want to use:')
    nb = input()
    counter = 0

    while counter < 3:
        if int(nb) > 0 and int(nb) < len(models)+1:
            return models[int(nb)-1]
        else:
            print('Cannot understand input, please try again:')
            nb = input()
            counter += 1

    print('You are too stupid to type,I`m out of here!')
    return None

def callMethod(o, name, arg):
    '''o is the object containing the models, name is the name of the model, arg is a list of additional arguments'''
    pred = getattr(o, name)(arg)
    return pred

def main():

    #header()

    ########################################################################
    # Locations of files containing the model / firm names and the subfolder
    # where we save intermediate polling results
    ########################################################################
    dir_path = os.path.dirname(os.path.realpath(__file__)) #current directory
    model_path = dir_path + '/model_list.txt' # list of models
    polling_firms_path = dir_path + '/polling_firms.txt' # list of polling firms
    datapath = dir_path + '/data'# where to save data to/ read data from


    x = input() # allowed_inputs = 'd', 'p', 'h'
    if x == 'd' or x == 'D':
        all_inst = get_new_data(datapath)
        use_inst, data = choose_inst(all_inst, datapath)
        plot_graphs(data['forsa'])

    if x == 'p'or x == 'P':
        int_names = open(polling_firms_path, 'r')
        all_inst =  [line[:len(line)-1] for line in int_names]
        int_names.close()
        use_inst, data = choose_inst(all_inst, datapath)


    if x == 'h' or x == 'H':
        print('There is no help for you!')
        #return None


#    modelname = choose_model(model_path)
#
#
#    f = model()
#    pred = callMethod(f, modelname, data)
#    print(pred)
#
#    #p = simple_model(data)
#    labels = ["CDU/CSU", "SPD", "GRÜNE", "FDP", "LINKE", "AfD", "Sonstige"]
#    print('\n\n Predictions from simple model:\n')
#
#
#    for i in range(len(labels)):
#        print(labels[i], ':  ', pred[i])
#
#


if __name__ == "__main__":
    main()
