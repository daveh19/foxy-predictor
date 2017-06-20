from subprocess import call
import pandas as pd
import numpy as np
import webbrowser
from urllib.request import pathname2url
from select_model import select_model

import sys
import os

sys.path.append(os.path.abspath('../Visualisation'))
#from Plotting_function import plot_graphs


sys.path.append(os.path.abspath('../Backend'))
from wahlrecht_polling_firms import get_tables




def header():
    #call(["clear"])
    #call(["figlet", "Foxy Predictor"])
    print("------------------------------------------------------------------")
    print("Here we might want to put some boring information")
    print("------------------------------------------------------------------")
    #call(["cowsay", "Welcome to the Foxy Predictor. Type 'D' to check the web for new data, type 'P' to start a new prediction or 'H' for help."])


def get_new_data(path):

    """ This function calls the get_tables function from 
    wahlrecht_polling_firms to import new data. All data is 
    coverted to csv and saved in the directory 'data'. Therfore
   we don't need to download everytime we call the programm."""
    

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
    """ This function prints the names of all polling firms and lets the user
    choose which one to use by keyboard input (y/n). return value is a dictionary
    with the keys being the names of the chosen polling firms and values are
    dataframes with the respective polling data."""

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


    
def visualize(data, use_inst): 
    """ This function allows to visualize data from selected polling firms. The user will be 
    asked how many weeks should be displayed"""

    print('Do you want to visualize the data? (y/n)')
    inp = input()
    vv =  0
    if inp == 'y':
        while vv < 1:
            print('please type the number of the dataset you want to visualize:')
            for k, inst in enumerate(use_inst):
                print(k, inst)
            nr = input()
            print('how many weeks do you want to display?')
            weeks = int(input())
            data2plot = data[use_inst[int(nr)]][: weeks]
            plot_graphs(data2plot)

            url = 'file:{}'.format(pathname2url(os.path.abspath('Dashboard.html')))
            webbrowser.open(url)

            print('do you want to visualize a different dataset? (y/n)')
            inp = input()
            if inp == 'n':
                vv = 1


def main():

    header()

    ########################################################################
    # Locations of files containing the model / firm names and the subfolder
    # where we save intermediate polling results
    ########################################################################
    dir_path = os.path.dirname(os.path.realpath(__file__)) #current directory
    model_path = dir_path + '/model_list.txt' # list of models
    polling_firms_path = dir_path + '/polling_firms.txt' # list of polling firms
    datapath = dir_path + '/data'# where to save data to/ read data from
    prediction_path = os.path.abspath(os.path.join(dir_path, os.pardir)) + '/predictions/'
    if not os.path.exists(prediction_path):
        os.makedirs(prediction_path)


    x = input() # allowed_inputs = 'd', 'p', 'h'
    if x == 'd' or x == 'D':
        all_inst = get_new_data(datapath)
        use_inst, data = choose_inst(all_inst, datapath)

    if x == 'p'or x == 'P':
        int_names = open(polling_firms_path, 'r')
        all_inst =  [line[:len(line)-1] for line in int_names]
        int_names.close()
        use_inst, data = choose_inst(all_inst, datapath)

    if x == 'h' or x == 'H':
        print('There is no help for you!')
        call(["sl"])
        return None

    visualize(data, use_inst)

    model, name  = select_model()
    print(name, 'predicts:\n')

    prediction = model.predict(data)
    print(prediction)
    prediction.to_pickle( prediction_path + 'prediction_' + name + '.p')



if __name__ == "__main__":
    main()
