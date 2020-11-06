import os
import pandas as pd
from com_dayoung_api.cmm.util.file_helper import FileReader

class UserDfo:
    """
    [This class is the main operator for user]
    Creates User Database with 7 columns.
    This enables user CRUD (Crete, Read, Update, Delete)
    Args:
        object ([object]): [description]
    """
    def __init__(self):
        """
        Creates fileReader object and sets the path to ""
        """
        self.fileReader = FileReader()
        self.path = os.path.abspath("")

    def hook(self):
        """
            Creates new model,

            for now it simply creates new_model which gets data from user.csv
        """
        usr_df = self.new_model()
        print(usr_df)
        mycolumns = {
            'user_id':'usr_id'
        }
        sort_df = usr_df.rename(columns=mycolumns)
        data = sort_df
        
        return data

    def new_model(self) -> object:        
        path = os.path.abspath("")
        # \com_dayoung_api\
        fname = r"\com_dayoung_api\usr\model\data\user.csv"
        data = pd.read_csv(path + fname, encoding='utf-8')
        # print('***********')
        # data = data.head()
        # print(data)
        return data