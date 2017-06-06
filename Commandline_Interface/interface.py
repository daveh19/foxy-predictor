from subprocess import call
import pandas as pd
import os
from wahlrecht_polling_firms import get_tables
from select_model import select_model
#from Plotting_function import plot_graphs
import numpy as np




def header():
    call(["clear"])
    call(["figlet", "Foxy Predictor"])
    print("------------------------------------------------------------------")
    print("Here we might want to put some boring information")
    print("------------------------------------------------------------------")
    call(["cowsay", "Welcome to the Foxy Predictor. Type 'D' to check the web for new data, type 'P' to start a new  or 'H' for help."])

#def header():
#    print("Welcome to the Foxy Predictor. Type 'D' to check the web for new data, type 'P' to start a new  or 'H' for help.")

def get_new_data(path):
    """ This function calls the get_tables function from 
    wahlrecht_polling_firms to import new data"""
    
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
        #return None

    model, name  = select_model()
    print(name, 'predicts:\n')
    
    prediction = model.predict(data)
    print(prediction)
    


if __name__ == "__main__":
    main()
