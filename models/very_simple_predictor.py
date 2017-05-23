from wahlrecht_polling_firms import get_tables
import numpy as np

def make_smart_panda(dataframe): 
    """ makes the pandas file convertable to numeric values 
    by deleting %-signs and replacing ',' by '.' """
    
    d1 = dataframe.replace('%', '',regex=True)
    return d1.replace(',', '.', regex=True)


def simple_model(data_dict):
    """ This model takes a dictionary with key = survey firm and value = pd.Dataframe containing survey data. 
    It reads the latest survey results and calculates a weighted average, the weights being the 
    number of participants in the survey. Return value is a numpy array with predictions for each party."""
    
    labels = ["CDU/CSU", "SPD", "GRÜNE", "FDP", "LINKE", "AfD", "Sonstige"]
       
    predictions = np.zeros(len(labels))
    
    normalization = 0
     
    for key, value in data_dict.items():
        weight = float(data_dict[key]["Befragte"][0])
        normalization +=  weight
        d = make_smart_panda(data_dict[key])

        for i, l in enumerate(labels): 
            predictions[i] += float(d[l][0])* weight
        
    return predictions / normalization
        
#    modelname = sys._getframe().f_code.co_name
#    date = time.strftime("%x")
#    start = min(dataframe['Datum'])
#    end = max(dataframe['Datum'])
#    
#    add_to_output_csv(modelname, date, prediction, 1, 1, 1, start, end)
    

def main():
    table = get_tables()
    all_inst = []
    use_inst = []
    for key ,values in table.items() :
        print(key)
        all_inst.append(key)   
    
    
    print("choose which firms to use (y/n): \n")
    for k in range(len(all_inst)): 
        ans = input("%s: " % all_inst[k] )
        if ans == 'y': 
            use_inst.append(all_inst[k])
   
    data = {ui:table[ui] for ui in use_inst}
    p = simple_model(data)
    labels = ["CDU/CSU", "SPD", "GRÜNE", "FDP", "LINKE", "AfD", "Sonstige"]
    
    print('\n\n Predictions from simple model:\n')
    
   
    for i in range(len(labels)): 
        print(labels[i], ':  ', p[i])
                 
            
    
if __name__ == "__main__":
    main()
