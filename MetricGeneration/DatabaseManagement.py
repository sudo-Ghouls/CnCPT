# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


import sqlite3

import pandas as pd

COLUMNS_NAMES = ["Apple", "Banana"]
COLUMNS_TYPES = ["text", "number"]


class DatabaseManager:
    def __init__(self, dataframe, database):
        self.dataframe = dataframe
        self.database = database

    @classmethod
    def initialize_manager(cls, database_name="CnCPT_Database", col_names=COLUMNS_NAMES, col_types=COLUMNS_TYPES):
        """

        """
        # Make new SQL Database
        new_database = sqlite3.connect("{0}.db".format(database_name))
        columns = " ".join(["{0} {1}".format(col_names[i],col_types[i]) for i in range(len(col_names))])
        cursor = new_database.cursor()
        cursor.execute('CREATE TABLE {0} ({1})'.format(database_name, columns))
        new_database.commit()

        # Make new Panda's DataFrame
        new_dataframe = pd.DataFrame(None, columns=COLUMNS_NAMES)
        return cls(new_dataframe, new_database)

if __name__ == "__main__":
    DatabaseManager.initialize_manager()
