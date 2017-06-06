import sys
import os
sys.path.append(os.path.abspath('../models'))
import model_classes 

def select_model(): 

    modelnames = ['AverageModel', 'WeightedAverageModel', 'LatestModel', 'WeightedLatestModel', 'DecayModel', 'WeightedDecayModel', 'LinearRegressionModel']
    
    print('This is a list of all the available models:\n\n')
    
    for i, mn in enumerate(modelnames): 
        print(i, mn)
        
    print('Please enter the number of the model you want to select:')
    model_nr = int(input())   
   
    while model_nr < 0 or model_nr > len(modelnames): 
        print('please try again')
        model_nr = int(input())
        
    if modelnames[int(model_nr)] == 'AverageModel': 
            model = model_classes.AverageModel()

    if modelnames[int(model_nr)] == 'WeightedAverageModel': 
            model = model_classes.WeightedAverageModel()
            
    if modelnames[int(model_nr)] == 'LatestModel': 
            model = model_classes.LatestModel()
            
    if modelnames[int(model_nr)] == 'WeightedLatestModel': 
            model = model_classes.WeightedLatestModel()     
                   
    if modelnames[int(model_nr)] == 'DecayModel': 
            model = model_classes.DecayModel()            
            
    if modelnames[int(model_nr)] == 'WeightedDecayModel': 
            model = model_classes.WeightedDecayModel()            

    if modelnames[int(model_nr)] == 'LinearRegressionModel': 
            model = model_classes.LinearRegressionModel()      
            
                
    return model, modelnames[int(model_nr)]
