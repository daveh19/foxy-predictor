from tkinter import *
import tkinter.messagebox
import pandas as pd
import sys
import os
import numpy as np

# imports for data 
sys.path.append(os.path.abspath('../Commandline_Interface'))
from foxy_intro import print_fox_gui

# imports for data 
# sys.path.append(os.path.abspath('../Backend'))
# from wahlrecht_polling_firms import get_tables

#imports for data

sys.path.append(os.path.abspath('../Backend/.'))
from APICalls.APICalls import getPollingData

#imports for prediction
sys.path.append(os.path.abspath('../models'))
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


class MyClass: 

    def __init__(self, master):
    
        self.framewidth = 75
        #self.textwidth = 75

        self.plot_test_data = pd.read_pickle(DATA_PATH + '/forsa.p')
        
        self.selected_data = dict() # empty dict that will be filled with pandas dataframes for all selected firms 
        
        self.prediction = dict()
        
        #-----------------------------------------------------------------
        ########################## TEXT OUTPUT ###########################
        #-----------------------------------------------------------------

        self.outputFrame = Frame(master, width = self.framewidth, bg = 'plum2')
        self.outputFrame.pack(side = RIGHT, anchor = N)
        
        self.outputTitle = Label(self.outputFrame, text = 'Results', bg = 'purple',  width = self.framewidth, font = ("ComicSans", 12))
        self.outputTitle.pack(side = TOP)
        
        self.Output = Text(self.outputFrame, width = self.framewidth) 
        self.Output.pack()
        
        self.clearButton = Button(self.outputFrame, text = 'Clear', command = self.deleteText(self.Output))
        self.clearButton.pack(side = RIGHT)
        
        self.textVar = StringVar()
        self.textVar.set('Hello\n')
        
        self.printButton = Button(self.outputFrame, text = 'Print', command = self.printText(self.Output,  self.textVar.get()))
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
        
        self.whichPollingFirms = [1 for i in range(len(POLLING_FIRMS))] #default is to select all firms
        
        for i in range(len(POLLING_FIRMS)):
            self.whichPollingFirms[i] = Variable()
            self.whichPollingFirms[i].set(0)
            check = Checkbutton(self.leftTopFrame, text = POLLING_FIRMS[i], variable = self.whichPollingFirms[i], bg = 'light yellow')
            if i < 6: 
                check.grid(row = i+2, column = 0,  sticky = W)
            else: check.grid(row = i-6+2, column = 1, sticky = W)
        
        #-----------------------------------------------------------------
        #-----------------------------------------------------------------
        
        self.dataOK_button = Button(self.dataFrame, text = 'OK', command = self.saveSelection)
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
        
        self.predictionTitle = Label(self.predictionFrame, text = 'Predict', bg = 'sea green', width = self.framewidth, font=("ComicSans", 12))
        self.predictionTitle.pack(side = TOP)
        
        self.modelName = StringVar(master)
        self.modelName.set("----")

        self.modelSelect = OptionMenu(self.predictionFrame, self.modelName, *MODELS)
        self.modelSelect.pack()
        
        self.paramSelect = Button(self.predictionFrame, text = 'Adjust Parameters', command = self.notPossible)
        self.paramSelect.pack(side = LEFT)
        
        self.predict = Button(self.predictionFrame, text = 'Predict', command = self.performPrediction)
        self.predict.pack(side = LEFT)
     

        
        #-----------------------------------------------------------------
        ########################### VISUALIZATION ########################
        #-----------------------------------------------------------------
        
        
        self.visualizationFrame = Frame(master, width = self.framewidth, bg = 'light cyan')
        self.visualizationFrame.pack(side =TOP)
        
        self.visualizationTitle = Label(self.visualizationFrame, text = 'Display', bg = 'SkyBlue', width = self.framewidth, font=("ComicSans", 12))
        self.visualizationTitle.pack(side = TOP)
        
        self.dispPred_Button = Button(self.visualizationFrame, text = 'Display Prediction', command = self.notPossible)
        self.dispPred_Button.pack(side = LEFT)
        
        self.dispPolls_Button = Button(self.visualizationFrame, text = 'Display Polls', command = self.notPossible)
        self.dispPolls_Button.pack(side = LEFT)
        
        
        
        self.selectWeeks = Label(self.visualizationFrame, text = 'How many weeks should be displayed? ', bg = 'light cyan')
        self.selectWeeks.pack(side = TOP)
        
        self.weeks = IntVar()
        self.weeks.set(10)
        self.selectWeeks = Entry(self.visualizationFrame, text = self.weeks) 
        self.selectWeeks.pack(side = TOP)
        
        self.displayOK_button = Button(self.visualizationFrame, text = 'OK', command = self.displayData)
        self.displayOK_button.pack(side = BOTTOM)
        


#------------------------------------------------------------------------
########### FUNCTIONS CHECKING DATA ###################################
#------------------------------------------------------------------------ 


    def valid_selection(self):
        #check if data is selected_data
        if not isinstance(self.selected_data,pd.core.frame.DataFrame) or len(self.selected_data.index)==0  : 
            tkinter.messagebox.showinfo('Error', 'Please select data first' )


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
        self.printText(self.Output,  pollsters)
        self.printText(self.Output,  self.all_data)
        self.printText(self.Output,  np.array(POLLING_FIRMS)[pollsters])
        self.selected_data = pp.average({k: self.all_data[k] for k in np.array(POLLING_FIRMS)[pollsters]})
        
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
        answer = tkinter.messagebox.askquestion('Confirm Update', 'Do you want to update your database?')
        if answer == 'yes':
            #table = get_tables() # deprecated
            self.all_data = getPollingData(state = False)
            
            #for key ,values in table.items() :
            #    print('Collect data from:', key)
            #    table[key].to_pickle(DATA_PATH + '/' + key+ '.p')
            tkinter.messagebox.showinfo('', 'Update Completed')


        
    
#------------------------------------------------------------------------
########### FUNCTIONS FOR PREDICTION ####################################
#------------------------------------------------------------------------

    def selectModel(self, modelName):
    
        modelName = modelName.get()
        
        if modelName == "----": 
            tkinter.messagebox.showinfo('', 'No Model Selected!')
            return None
        
        if modelName == 'AverageModel': 
            predictionModel = model_classes.AverageModel()

        if modelName == 'WeightedAverageModel': 
            predictionModel = model_classes.WeightedAverageModel()
            
        if modelName == 'LatestModel': 
            predictionModel = model_classes.LatestModel()
            
        if modelName == 'WeightedLatestModel': 
            predictionModel = model_classes.WeightedLatestModel()     
                   
        if modelName == 'DecayModel': 
            predictionModel = model_classes.DecayModel()            
            
        if modelName == 'WeightedDecayModel': 
            predictionModel = model_classes.WeightedDecayModel()            

        if modelName == 'LinearRegressionModel': 
            predictionModel = model_classes.LinearRegressionModel() 
        
        return predictionModel
            
     
    def performPrediction(self): 
   
        self.valid_selection()
            
        model = self.selectModel(self.modelName)    
        if model is not None:
            self.prediction[self.modelName.get()] = model.predict(self.selected_data)
            self.callback(self.Output, str(self.prediction[self.modelName.get()].T))




#    prediction.to_pickle( prediction_path + 'prediction_' + name + '.p')
 
 
#------------------------------------------------------------------------
########### FUNCTIONS FOR VISUALIZATION #################################
#------------------------------------------------------------------------
    def notPossible(self): 
        tkinter.messagebox.showinfo('Error', 'Not yet implemented!' )
        
    #def displayPolls(self): 
        

    def displayData(self): 
        weeks = self.weeks.get()
        
        if weeks > 0: 
            data2plot = self.plot_test_data[: weeks]
            plot_graphs(data2plot)
            url = 'file:{}'.format(pathname2url(os.path.abspath('Dashboard.html')))
            webbrowser.open(url)
        else: 
            tkinter.messagebox.showinfo('Error', 'Invalid input!' )

 

#------------------------------------------------------------------------
##########################      MAIN      ###############################
#------------------------------------------------------------------------
def main(): 

 
    root = Tk()
    root.title("Foxy Predictor")
    b = MyClass(root)
    root.mainloop()




if __name__ == "__main__":
    main()

