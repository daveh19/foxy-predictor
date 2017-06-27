from tkinter import *
import tkinter.messagebox
import pandas as pd
import sys
import os

# imports for data 
sys.path.append(os.path.abspath('../Backend'))
from wahlrecht_polling_firms import get_tables

#imports for prediction
sys.path.append(os.path.abspath('../models'))
import model_classes 

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
    
        self.framewidth = 50
        self.textwidth = 75
        
        self.plot_test_data = pd.read_pickle(DATA_PATH + '/forsa.p')
        
        #-----------------------------------------------------------------
        ########################## TEXT OUTPUT ###########################
        #-----------------------------------------------------------------

        self.outputFrame = Frame(master, width = self.textwidth)
        self.outputFrame.pack(side = RIGHT, anchor = N)
        
        self.outputTitle = Label(self.outputFrame, text = 'Results', bg = 'purple',  width = self.textwidth, font = ("ComicSans", 12))
        self.outputTitle.pack(side = TOP)
        
        self.Output = Text(self.outputFrame, width = self.textwidth) 
        self.Output.pack()
        
        self.clearButton = Button(self.outputFrame, text = 'Clear', command = self.deleteText(self.Output))
        self.clearButton.pack(side = RIGHT)
        
        self.textVar = StringVar()
        self.textVar.set('Hello\n')
        
        self.printButton = Button(self.outputFrame, text = 'Print', command = self.printText(self.Output,  self.textVar.get()))
        self.printButton.pack(side = RIGHT)

        self.helpButton = Button(self.outputFrame, text = 'Help', command = self.printText(self.Output,  HELP_TEXT))
        self.helpButton.pack(side = RIGHT)

        
        
        #-----------------------------------------------------------------
        ############################# DATA ############################### 
        #-----------------------------------------------------------------
      
        self.dataFrame = Frame(master, width = self.framewidth)
        self.dataFrame.pack(side = TOP)
        
        self.dataTitle = Label(self.dataFrame, text = 'Data', bg = 'red', width = self.framewidth, font=("ComicSans", 12))
        self.dataTitle.pack(side = TOP)
        
        
        #-----------------------------------------------------------------
        ########################  data selection ######################### 
        #-----------------------------------------------------------------
        self.leftTopFrame = Frame(self.dataFrame)
        self.leftTopFrame.pack(side= TOP)
   
        self.dataHelp = Label(self.leftTopFrame, text = 'Select the data you want to use')
        self.dataHelp.grid(row = 1, sticky = W)
        
        self.data = POLLING_FIRMS
        self.var = [1 for i in range(len(POLLING_FIRMS))] #default is to select all firms
        
        for i in range(len(self.data)):
            self.var[i] = Variable()
            self.var[i].set(1)
            check = Checkbutton(self.leftTopFrame, text = self.data[i], variable = self.var[i])
            check.grid(row = i+2, sticky = W)
        
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
        
        self.predictionFrame = Frame(master, width = self.framewidth)
        self.predictionFrame.pack(side = TOP)
        
        self.predictionTitle = Label(self.predictionFrame, text = 'Predict', bg = 'green', width = self.framewidth, font=("ComicSans", 12))
        self.predictionTitle.pack(side = TOP)
        
        self.modelName = StringVar(master)
        self.modelName.set("----")
        
        self.modelSelect = OptionMenu(self.predictionFrame, self.modelName, *MODELS)
        self.modelSelect.pack()
        
        self.paramSelect = Button(self.predictionFrame, text = 'Adjust Parameters')
        self.paramSelect.pack(side = LEFT)
        
        self.predict = Button(self.predictionFrame, text = 'Predict', command = self.performPrediction)
        self.predict.pack(side = LEFT, )
        
        

        
        #-----------------------------------------------------------------
        ########################### VISUALIZATION ########################
        #-----------------------------------------------------------------
        
        
        self.visualizationFrame = Frame(master, width = self.framewidth)
        self.visualizationFrame.pack(side =TOP)
        
        self.visualizationTitle = Label(self.visualizationFrame, text = 'Display', bg = 'blue', width = self.framewidth, font=("ComicSans", 12))
        self.visualizationTitle.pack(side = TOP)
        
        self.selectWeeks = Label(self.visualizationFrame, text = 'How many weeks should be displayed? ')
        self.selectWeeks.pack(side = TOP)
        
        self.weeks = IntVar()
        self.weeks.set(10)
        self.selectWeeks = Entry(self.visualizationFrame, text = self.weeks) 
        self.selectWeeks.pack(side = TOP)
        
        self.displayOK_button = Button(self.visualizationFrame, text = 'OK', command = self.displayData)
        self.displayOK_button.pack(side = BOTTOM)
        
        
        
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
         

#------------------------------------------------------------------------
########### FUNCTIONS FOR DATA ##########################################
#------------------------------------------------------------------------
    def saveSelection(self): 
        for i in range(len(self.var)): 
            print(self.var[i].get())
                     
    def dataStatus(self): 

        table = pd.read_pickle(DATA_PATH + '/forsa.p')
        date = table['Datum'][0]
    
        tkinter.messagebox.showinfo('Latest Polls', 'Latest Poll is from ' + str(date))
       
    def dataUpdate(self): 
        answer = tkinter.messagebox.askquestion('Confirm Update', 'Do you want to update your database?')
        if answer == 'yes':
            table = get_tables()
            
            
            for key ,values in table.items() :
                print('Collect data from:', key)
                table[key].to_pickle(DATA_PATH + '/' + key+ '.p')
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
    
        model = self.selectModel(self.modelName)
        if model is not None:
            prediction = model.predict(self.test_data)
            self.printText(self.Output, prediction)



#    prediction.to_pickle( prediction_path + 'prediction_' + name + '.p')
 
 
#------------------------------------------------------------------------
########### FUNCTIONS FOR VISUALIZATION #################################
#------------------------------------------------------------------------
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

