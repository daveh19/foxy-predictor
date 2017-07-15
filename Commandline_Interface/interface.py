from subprocess import call
import pandas as pd
import pickle
import numpy as np
import webbrowser
from urllib.request import pathname2url
from select_model import select_model
from foxy_intro import print_foxypredictor, print_foxsay
import predict_till_election
import sys
import os
from  copy import deepcopy as copy 
sys.path.append(os.path.abspath('../Visualisation'))
from Plotting_function import plot_graphs


sys.path.append(os.path.abspath('../Python_Gui'))
from vars import POLLING_FIRMS
from vars import MODELS
from vars import PARTIES


#sys.path.append(os.path.abspath('../Backend'))
#from wahlrecht_polling_firms import get_tables


sys.path.append(os.path.abspath('../Backend/.'))
from APICalls.APICalls import getPollingData


sys.path.append(os.path.abspath('../models/.'))
import preprocessing as pp 

def header():
    call(["clear"])
    #call(["figlet", "Foxy Predictor"])
    print_foxypredictor()
    print("------------------------------------------------------------------")
    print("Here we might want to put some boring information")
    print("------------------------------------------------------------------")
    #call(["cowsay", "Welcome to the Foxy Predictor. Type 'D' to check the web for new data, type 'P' to start a new prediction or 'H' for help."])
    print_foxsay()

def get_new_data(path):

    """ This function calls the get_tables function from 
    wahlrecht_polling_firms to import new data. All data is 
    coverted to pickle and saved in the directory 'data'. Therfore
   we don't need to download everytime we call the programm."""
    

    print('Downloading new data......')
    table = getPollingData(state = False)
    pickle.dump(table, open(path, 'wb'))
    all_inst = []

    for key ,values in table.items() :
        print('Collect data from:', key)
        all_inst.append(key)
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
    all_data = pickle.load(open(path, 'rb'))
    data = {ui : all_data[ui] for ui in use_inst}
    preprocessed_data = pp.average(data)
    
    return use_inst, preprocessed_data


    
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
    datapath = dir_path + '/data/all_data.p'# where to save data to/ read data from
    datafolder = dir_path+'/data/'
    if not os.path.exists(datafolder):
        os.makedirs(datafolder)
    prediction_path = os.path.abspath(os.path.join(dir_path, os.pardir)) + '/predictions/'
    if not os.path.exists(prediction_path):
        os.makedirs(prediction_path)


    x = input() # allowed_inputs = 'd', 'p', 'h'
    if x == 'd' or x == 'D':
        all_inst = get_new_data(datapath)
        use_inst, data = choose_inst(all_inst, datapath)

    if x == 'p'or x == 'P':
#        int_names = open(polling_firms_path, 'r')
#        all_inst =  [line[:len(line)-1] for line in int_names]
#        int_names.close()
        all_inst = POLLING_FIRMS
        use_inst, data = choose_inst(all_inst, datapath)

    if x == 'h' or x == 'H':
        print('There is no help for you!')
        call(["sl"])
        return None

    visualize(data, use_inst)

    model, name  = select_model()
    print(name, 'predicts:\n')

    prediction = model.predict_all(data)
    print(prediction.iloc[0])
    to_election = predict_till_election.predict_till_election(prediction)
    complete_prediction    = to_election.predict()
    histogram = to_election.histograms()

    lower = copy(complete_prediction)
    lower[PARTIES] = lower[PARTIES].applymap(lambda x : x[0])
    upper = copy(complete_prediction)
    upper[PARTIES] = upper[PARTIES].applymap(lambda x : x[2])
    mean = copy(complete_prediction)
    mean[PARTIES] = mean[PARTIES].applymap(lambda x : x[1])

    output_dict = {'mean':mean,'lower':lower,'upper':upper,'hist':histogram}

    complete_prediction.to_pickle( prediction_path + 'prediction_' + name + '.p')
    data2plot = output_dict['mean']
    plot_graphs(data2plot)
    url = 'file:{}'.format(pathname2url(os.path.abspath('Dashboard.html')))
    webbrowser.open(url)


if __name__ == "__main__":
    main()
