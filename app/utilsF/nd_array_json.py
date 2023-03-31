import numpy as np 
from json import JSONEncoder
import json
import os 

path_root = os.getcwd()
path_file = os.path.join(path_root + '/app/utilsF/','file_json.json')

class NumpyArrayEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object,np.ndarray):
            return object.tolist()
        return JSONEncoder.default(self,object)


def SerializeJSON(n_cedula:str,np_array):
    data = {'n_cedula':n_cedula,'np_array':np_array}
    print(path_file)
    with open(path_file,'w') as write_file:
        json.dump(data,write_file,cls=NumpyArrayEncoder)

