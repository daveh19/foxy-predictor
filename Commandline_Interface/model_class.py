import numpy as np
from very_simple_predictor import make_smart_panda
class model: 

    def simple_model(self, data_dict):
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
