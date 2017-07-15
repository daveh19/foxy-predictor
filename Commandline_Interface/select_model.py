import sys
import os
sys.path.append(os.path.abspath('../models'))
sys.path.append(os.path.abspath('../Python_Gui'))
import model_classes
from vars import MODELS
from vars import MODELS_classes
def select_model():


    print('This is a list of all the available models:\n\n')

    for i, mn in enumerate(MODELS):
        print(i, mn)

    print('Please enter the number of the model you want to select:')
    model_nr = int(input())

    while model_nr < 0 or model_nr > len(MODELS_classes):
        print('please try again')
        model_nr = int(input())


    model = MODELS_classes[model_nr]()
    return model, MODELS[int(model_nr)]
