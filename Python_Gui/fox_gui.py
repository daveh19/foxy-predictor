#from tkinter import *
#import tkinter.messagebox Can nor use tkinter on the server
import pandas as pd
import sys
import os
import numpy as np
from  copy import deepcopy as copy
from subprocess import call

# imports for data
sys.path.append(os.path.abspath('../Commandline_Interface'))
from foxy_intro import print_fox_gui, print_foxypredictor, print_foxsay

# imports for data
# sys.path.append(os.path.abspath('../Backend'))
# from wahlrecht_polling_firms import get_tables

#imports for data

sys.path.append(os.path.abspath('../Backend/.'))
from APICalls.APICalls import getPollingData

#imports for prediction
sys.path.append(os.path.abspath('../models'))
import predict_till_election
import model_classes

import preprocessing as pp


#imports for visualization
from urllib.request import pathname2url
import webbrowser
sys.path.append(os.path.abspath('../Visualisation'))
from Plotting_function import plot_graphs



#### some global vars
from vars import DATA_PATH
from vars import POLLING_FIRMS
from vars import MODELS
from vars import HELP_TEXT
from vars import PARTIES
from vars import MODELS_classes

class modelName():
    def __init__(self):
        self.modelName = None

    def get(self):
        return self.modelName

    def set(self, name):
        self.modelName=name


class var():
    def __init__(self):
        self.var = None

    def get(self):
        return self.var

    def set(self, val):
        self.var=val

class interface:

    def __init__(self, master,graphical = False):

        self.printer = self.gui_print if graphical else self.terminal_print
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) #current directory
        self.datapath = self.dir_path + '/data/all_data.p'# where to save data to/ read data from
        self.datafolder = self.dir_path+'/data/'
        self.graphical = graphical
        self.selected_data = dict() # empty dict that will be filled with pandas dataframes for all selected firms

        self.prediction = dict()
        self.prediction2display = dict()


        self.whichPollingFirms = [1 for i in range(len(POLLING_FIRMS))] #default is to select all firms
        #-----------------------------------------------------------------
        ########################## TEXT OUTPUT ###########################
        #-----------------------------------------------------------------

        if self.graphical:

            self.init_frame(master)

        else:
            for i in range(len(POLLING_FIRMS)):
                self.whichPollingFirms[i] = var()
                self.whichPollingFirms[i].set(0)

            header()
            ########################################################################
            # Locations of files containing the model / firm names and the subfolder
            # where we save intermediate polling results
            ########################################################################

            self.modelName = modelName()
            if not os.path.exists(self.datafolder):
                os.makedirs(self.datafolder)
            self.prediction_path = os.path.abspath(os.path.join(self.dir_path, os.pardir)) + '/predictions/'
            if not os.path.exists(self.prediction_path):
                os.makedirs(self.prediction_path)


            x = input() # allowed_inputs = 'd', 'p', 'h'
            if x == 'd' or x == 'D':
                self.dataUpdate()
                self.choose_inst()
                self.saveSelection()

            if x == 'p'or x == 'P':
                #int_names = open(polling_firms_path, 'r')
                #all_inst =  [line[:len(line)-1] for line in int_names]
                #int_names.close()
                self.choose_inst()
                self.saveSelection()
            if x == 'h' or x == 'H':
                self.printer(msg='There is no help for you!')
                call(["sl"])
                return None

            self.performPrediction()
            self.displayData()
            #print(name, 'predicts:\n')






    def gui_print(self, **kwargs):
        '''
        if used as system info box, pass msg_box = True to printer function
            then also pass kwargs 'title' and 'msg'
        else just pass 'msg'
        '''
        if 'msg_box' in kwargs and kwargs['msg_box']=='info':
            tkinter.messagebox.showinfo(kwargs['title'], kwargs['msg'])

        elif 'msg_box' in kwargs and kwargs['msg_box']=='question':
            return tkinter.messagebox.askquestion(kwargs['title'], kwargs['msg'])

        else:
            self.callback(self.Output, kwargs['msg'])

        return None

    def terminal_print(self, **kwargs):
        '''
        just pass the message as 'msg' argument in kwargs
        '''
        print(kwargs['msg'])


    def init_frame(self,master):
            self.framewidth = 75
            #self.textwidth = 75


            self.outputFrame = Frame(master, width = self.framewidth, bg = 'plum2')
            self.outputFrame.pack(side = RIGHT, anchor = N)

            self.outputTitle = Label(self.outputFrame, text = 'Results', bg = 'purple', \
                                     width = self.framewidth, font = ("ComicSans", 12))
            self.outputTitle.pack(side = TOP)

            self.Output = Text(self.outputFrame, width = self.framewidth)
            self.Output.pack()

            self.clearButton = Button(self.outputFrame, text = 'Clear', command = self.deleteText(self.Output))
            self.clearButton.pack(side = RIGHT)

            self.textVar = StringVar()
            self.textVar.set('Hello\n')

            self.printButton = Button(self.outputFrame, text = 'Print', \
                                      command = self.printText(self.Output,  self.textVar.get()))
            self.printButton.pack(side = RIGHT)

            self.helpButton = Button(self.outputFrame, text = 'Help', command = self.printText(self.Output,  HELP_TEXT))
            self.helpButton.pack(side = RIGHT)

            self.foxButton = Button(self.outputFrame, text = 'Fox', command= self.printFoxy(self.Output))
            self.foxButton.pack(side = RIGHT)

            #-----------------------------------------------------------------
            ############################# DATA ###############################
            #-----------------------------------------------------------------

            self.dataFrame = Frame(master, width = self.framewidth, bg = 'light yellow')
            self.dataFrame.pack(side = TOP)

            self.dataTitle = Label(self.dataFrame, text = 'Data', bg = 'yellow', width = self.framewidth, font=("ComicSans", 12))
            self.dataTitle.pack(side = TOP)


            #-----------------------------------------------------------------
            ########################  data selection #########################
            #-----------------------------------------------------------------
            self.leftTopFrame = Frame(self.dataFrame, bg = 'light yellow')
            self.leftTopFrame.pack(side= TOP)

            self.dataHelp = Label(self.leftTopFrame, text = 'Select the polling firms you want to use:', bg = 'light yellow')
            self.dataHelp.grid(row = 1, sticky = W)



            for i in range(len(POLLING_FIRMS)):
                self.whichPollingFirms[i] = Variable()
                self.whichPollingFirms[i].set(0)
                check = Checkbutton(self.leftTopFrame, text = POLLING_FIRMS[i], \
                                    variable = self.whichPollingFirms[i], bg = 'light yellow')
                if i < 6:
                    check.grid(row = i+2, column = 0,  sticky = W)
                else: check.grid(row = i-6+2, column = 1, sticky = W)

            #-----------------------------------------------------------------
            #-----------------------------------------------------------------

            self.dataOK_button = Button(self.dataFrame, text = 'Save Selection', command = self.saveSelection)
            self.dataOK_button.pack(side = LEFT)

            self.dataStatus_button = Button(  self.dataFrame, text = 'Status',  command = self.dataStatus)
            self.dataStatus_button.pack(side = LEFT)

            self.dataUpdate_button = Button(self.dataFrame, text = 'Update',  command = self.dataUpdate)
            self.dataUpdate_button.pack(side = LEFT)



            #-----------------------------------------------------------------
            ######################## PREDICTION ##############################
            #-----------------------------------------------------------------

            self.predictionFrame = Frame(master, width = self.framewidth, bg = 'PaleGreen3')
            self.predictionFrame.pack(side = TOP)

            self.predictionTitle = Label(self.predictionFrame, text = 'Predict', \
                                         bg = 'sea green', width = self.framewidth, font=("ComicSans", 12))
            self.predictionTitle.pack(side = TOP)

            self.modelName = StringVar(master)
            self.modelName.set("----")

            self.modelSelect = OptionMenu(self.predictionFrame, self.modelName, *MODELS)
            self.modelSelect.pack()

            #self.paramSelect = Button(self.predictionFrame, text = 'Adjust Parameters', command = self.notPossible)
            #self.paramSelect.pack(side = LEFT)

            self.predict = Button(self.predictionFrame, text = 'Predict', command = self.performPrediction)
            self.predict.pack(side = LEFT)



            #-----------------------------------------------------------------
            ########################### VISUALIZATION ########################
            #-----------------------------------------------------------------


            self.visualizationFrame = Frame(master, width = self.framewidth, bg = 'light cyan')
            self.visualizationFrame.pack(side =TOP)

            self.visualizationTitle = Label(self.visualizationFrame, \
                                            text = 'Display', bg = 'SkyBlue', width = self.framewidth, font=("ComicSans", 12))
            self.visualizationTitle.pack(side = TOP)

            #self.dispPred_Button = Button(self.visualizationFrame, text = 'Display Prediction', command = self.notPossible)
            #self.dispPred_Button.pack(side = LEFT)

            #self.dispPolls_Button = Button(self.visualizationFrame, text = 'Display Polls', command = self.notPossible)
            #self.dispPolls_Button.pack(side = LEFT)



            self.selectWeeks = Label(self.visualizationFrame, text = 'How many weeks should be displayed? ', bg = 'light cyan')
            self.selectWeeks.pack(side = TOP)

            self.weeks = IntVar()
            self.weeks.set(10)
            self.selectWeeks = Entry(self.visualizationFrame, text = self.weeks)
            self.selectWeeks.pack(side = TOP)

            self.displayOK_button = Button(self.visualizationFrame, text = 'Show Figures', command = self.displayData)
            self.displayOK_button.pack(side = BOTTOM)



#------------------------------------------------------------------------
########### FUNCTIONS CHECKING DATA ###################################
#------------------------------------------------------------------------


    def valid_selection(self):
        #check if data is selected_data
        if not isinstance(self.selected_data,pd.core.frame.DataFrame) or len(self.selected_data.index)==0  :
            self.printer(title= 'Error', msg='Please select data first' ,msg_box='info')


    def choose_inst(self):
        """ This function prints the names of all polling firms and lets the user
        choose which one to use by keyboard input (y/n). return value is a dictionary
        with the keys being the names of the chosen polling firms and values are
        dataframes with the respective polling data."""

        print('choose which firms to use (y/n): \n')
        for k in range(len(POLLING_FIRMS)):
            ans = input("%s: " % POLLING_FIRMS[k] )
            if ans == 'y':
                self.whichPollingFirms[k].set(1)
            else :
                self.whichPollingFirms[k].set(0)


#------------------------------------------------------------------------
########### FUNCTIONS FOR TEXT OUTPUT ###################################
#------------------------------------------------------------------------

    def generateOutput(self, textString):
        self.textVar.set(textString)

    def printText(self, textbox, text):
        return lambda : self.callback(textbox, text)

    def callback(self, textbox, text):
        s = text
        textbox.insert(END, s)
        textbox.see(END)

    def kill(self, textbox):
        textbox.delete(1.0, END)

    def deleteText(self, textbox):
        return lambda: self.kill(textbox)

    def printFoxy(self, textbox):
        fox = print_fox_gui()
        return lambda : self.callback(textbox, fox)
#------------------------------------------------------------------------
########### FUNCTIONS FOR DATA ##########################################
#------------------------------------------------------------------------
    def saveSelection(self):

        pollsters = np.array([self.whichPollingFirms[i].get() for i in range(len(self.whichPollingFirms))],dtype=bool)
        #self.printer( msg= self.all_data)
        #self.printer(msg=  np.array(POLLING_FIRMS)[pollsters])

        self.selected_data = pp.average({k: self.all_data[k] for k in np.array(POLLING_FIRMS)[pollsters]})
        #self.printer(msg=self.selected_data)
        #for i in range(len(self.whichPollingFirms)):
            #self.callback(self.Output, str(self.whichPollingFirms[i].get()))
        #   if self.whichPollingFirms[i].get():

                #self.selected_data[POLLING_FIRMS[i]] = pd.read_pickle(DATA_PATH + '/' + POLLING_FIRMS[i] + '.p')
        #self.callback(self.Output, str(self.selected_data.keys()))

    def dataStatus(self):
        max_dates = []
        self.valid_selection()
        #for key, df in self.selected_data.items():
        #        max_dates.append(df.index.max())
        maxdate = self.selected_data['Datum'][0]#max(max_dates)
        tkinter.messagebox.showinfo('Latest Polls', 'Latest Poll is from ' + maxdate.strftime('%Y-%m-%d'))

    def dataUpdate(self):
        if self.graphical:

            answer = self.printer(title= 'Confirm Update', msg='Do you want to update your database?',msg_box='question')
        else:
            while True:
                self.printer(msg='Do you want to update your database? (yes/no)')
                answer = input()
                if answer == 'yes' or answer  == 'no':
                    break
                else:
                    self.printer(msg='This was not a valid answer...')



        if  answer == 'yes':
            #table = get_tables() # deprecated
            self.all_data = getPollingData(state = False)

            #for key ,values in table.items() :
            #    print('Collect data from:', key)
            #    table[key].to_pickle(DATA_PATH + '/' + key+ '.p')

            self.printer(title='', msg='Update Completed', msg_box='info')




#------------------------------------------------------------------------
########### FUNCTIONS FOR PREDICTION ####################################
#------------------------------------------------------------------------


    def selectModel(self):

        if self.graphical:
            modelName = self.modelName.get()
        else:
            self.printer(msg='This is a list of all the available models:\n\n')
            for i, mn in enumerate(MODELS):
                self.printer(msg='{0:d} {1:s}'.format(i,mn))

            self.printer(msg='Please enter the number of the model you want to select:')
            while True:
                try:
                    model_nr = int(input())
                    if model_nr < 0 or model_nr > len(MODELS_classes):
                        raise ValueError('invalid input')
                    break
                except ValueError:
                    self.printer(msg='try again')

            modelName = MODELS[model_nr]
            self.modelName.set(modelName)

        predictionModel = MODELS_classes[MODELS.index(modelName)]

        #self.printer(msg=predictionModel)

        if modelName == "----":
            self.printer(title='', msg='No Model Selected!',msg_box='info')

        return predictionModel



    def performPrediction(self):

        self.valid_selection()

        model_class = self.selectModel()
        model    = model_class()
        if model is not None:
            modelOutput = model.predict_all(self.selected_data)

            if not model.predicts():
                to_election = predict_till_election.predict_till_election(modelOutput)
                self.complete_prediction    = to_election.predict()
                histogram = to_election.histograms()
            else:
                self.complete_prediction = modelOutput
                histogram = model.histogram()

            self.prediction[self.modelName.get()] = modelOutput
            lower = copy(self.complete_prediction)
            lower[PARTIES] = lower[PARTIES].applymap(lambda x : x[0])
            upper = copy(self.complete_prediction)
            upper[PARTIES] = upper[PARTIES].applymap(lambda x : x[2])
            mean = copy(self.complete_prediction)
            mean[PARTIES] = mean[PARTIES].applymap(lambda x : x[1])

            self.output_dict = {'mean':mean,'lower':lower,'upper':upper,'hist':histogram,'original': self.selected_data}

            #self.prediction2display[self.modelName.get()] = str(modelOutput[1]) + "(" #+ str(modelOutput[1] - modelOutput[0]) + ")"
            #self.callback(self.Output, str(self.prediction[self.modelName.get()].T))

            self.printer(msg= '' + str(self.modelName.get()) +  ': \n\n')
            for p in PARTIES:
                self.prediction2display[p] = str(modelOutput[p][0][1]) + "\t\t( +/- " + str(modelOutput[p][0][1] - modelOutput[p][0][0]) + ")"
                self.printer(msg='' + p + '\t\t')
                self.printer(msg=''+ str(self.prediction2display[p]) + '\n')
            self.printer(msg= '\n\n')

        else:
            self.printer(title='Error', msg='Please select a model first',msg_box='info')

#    prediction.to_pickle( prediction_path + 'prediction_' + name + '.p')


#------------------------------------------------------------------------
########### FUNCTIONS FOR VISUALIZATION #################################
#------------------------------------------------------------------------
    def notPossible(self):
        tkinter.messagebox.showinfo('Error', 'Not yet implemented!' )

    #def displayPolls(self):


    def displayData(self):


        data2plot = self.output_dict
        plot_graphs(data2plot)
        url = 'file:{}'.format(pathname2url(os.path.abspath('Dashboard.html')))
        webbrowser.open(url)



#------------------------------------------------------------------------
########### FUNCTIONS FOR TERMINAL USE  #################################
#------------------------------------------------------------------------

def header():
    call(["clear"])
    #call(["figlet", "Foxy Predictor"])
    print_foxypredictor()
    print("------------------------------------------------------------------")
    print("Welcome to the Foxy Predictor - an engine that will predict the German 2017 Elections")
    print("------------------------------------------------------------------")
    #call(["cowsay", "Welcome to the Foxy Predictor. Type 'D' to check the web for new data, type 'P' to start a new prediction or 'H' for help."])
    print_foxsay()
#------------------------------------------------------------------------
##########################      MAIN      ###############################
#------------------------------------------------------------------------

def main():


    if '-GUI' in sys.argv:

            root = Tk()
            root.title("Foxy Predictor")
            b = interface(root,graphical =True)
            root.mainloop()
    else:
        header()
        print('Running the normal mode now.')
        print('If you want to run the GUI, run with option -GUI.')

        b= interface(None)



if __name__ == "__main__":
    main()
