## built-in modules
import os
import time
import typing
import base64

## third party modules
from mysql.connector import pooling
from mysql.connector import cursor

import mysql.connector 

## custom modules
from modules import util

from modules.logger import logger
from modules.fileEnsurer import fileEnsurer


class connectionHandler():

    """
    
    The handler that handles the connection to the database and all interactions with it.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer, logger:logger) -> None:

        """
        
        Initializes the connectionHandler class.\n

        Parameters:\n
        self (object - connectionHandler) : The handler object.\n
        file_ensurer (object - fileEnsurer) : The file ensurer object.\n
        logger (object - logger) : The logger object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.fileEnsurer = file_ensurer

        self.logger = logger

        ##----------------------------------------------------------------dirs----------------------------------------------------------------

        ## lib files for remoteHandler.py
        self.remote_lib_dir = os.path.join(self.fileEnsurer.lib_dir, "remote")

        ##----------------------------------------------------------------paths----------------------------------------------------------------

        ## if remoteHandler failed to make a database connection
        self.database_connection_failed_path = os.path.join(self.remote_lib_dir, "isConnectionFailed.txt")

        ## the path to the file that stores the password
        self.credentials_path = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Logins"), "credentials.txt")

        ##----------------------------------------------------------------other----------------------------------------------------------------

        ## the database connection, can either be itself or none
        self.connection, self.cursor = self.initialize_database_connection()

##-------------------start-of-check_connection_validity()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_connection_validity(self, reason_for_check:str) -> bool:

        """
        
        Determines if we have a valid connection.\n

        Parameters:\n
        self (object - connectionHandler) : The connection handler object.\n

        Returns:\n
        isValid (bool) : True if valid, False otherwise

        """

        log_message = "Checking connection for reason: " + reason_for_check + ", Connection is valid, continuing."
        isValid = True

        if(self.connection == None or self.cursor == None):
            isValid = False
            log_message = "Checking connection for reason: " + reason_for_check + ", Connection is invalid, skipping."
        
        self.logger.log_action(log_message)

        return isValid

##-------------------start-of-initialize_database_connection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def initialize_database_connection(self) -> typing.Tuple[typing.Union[mysql.connector.connection.MySQLConnection, mysql.connector.pooling.PooledMySQLConnection, None], typing.Union[cursor.MySQLCursor, None]]:

        """

        Sets up the database connection. If the user has already entered the password for the database, the program will use the saved password. If not, the program will ask the user for the password.\n

        Parameters:\n
        None.\n

        Returns:\n
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) or None : The connection object to the database.\n

        """

        connection = None
        cursor = None
        
        with open(self.database_connection_failed_path, "r+", encoding="utf-8") as file:
            if(file.read().strip() == "true"):
                self.logger.log_action("Database connection has failed previously.... skipping connection initialization")
                return connection, cursor

        self.start_marked_succeeded_database_connection()

        try:

            with open(self.credentials_path, 'r', encoding='utf-8') as file:  ## get saved connection credentials if exists
                credentials = file.readlines()

                database_name = base64.b64decode((credentials[0].strip()).encode('utf-8')).decode('utf-8')
                password = base64.b64decode((credentials[1].strip()).encode('utf-8')).decode('utf-8')

            connection = self.create_database_connection("localhost", "root", database_name, password)
            cursor = connection.cursor()

            self.logger.log_action("Used saved credentials in " + self.credentials_path)

        except: ## else try to get credentials manually

            try: ## if valid save the credentials

                database_name = util.user_confirm("Please enter the name of the database you have")

                util.clear_console()

                password = util.user_confirm("Please enter the root password for your local database you have")

                credentials = [
                    base64.b64encode(database_name.encode('utf-8')).decode('utf-8'),
                        base64.b64encode(password.encode('utf-8')).decode('utf-8')]
                
                connection = self.create_database_connection("localhost", "root", database_name, password)
                cursor = connection.cursor()
                            
                util.standard_create_file(self.credentials_path, self.logger) 

                time.sleep(0.1)

                credentials = [x + '\n' for x  in credentials]

                with open(self.credentials_path, "w+",encoding='utf-8') as file:
                    file.writelines(credentials)

            except AssertionError:
                
                util.clear_console()

                self.start_marked_failed_database_connection()

            except Exception as e: ## if invalid exit
                        
                util.clear_console()

                print(str(e))
                print("Error with creating connection object, please double check your password and database name\n")

                self.start_marked_failed_database_connection()

                util.pause_console()
            
        return connection, cursor
    
##--------------------start-of-mark_failed_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def start_marked_failed_database_connection(self) -> None:
         
        """
        
        Marks a file in lib that the most recently attempted database connection has failed to connect.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        with open(self.database_connection_failed_path, "w+", encoding="utf-8") as file:
            file.write("true")
            
        self.logger.log_action("Database Connection Failed")

##--------------------start-of-mark_succeeded_database_connection()---------------------------S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def start_marked_succeeded_database_connection(self) -> None:
         
        """
        
        Marks a file in lib that the most recently attempted database connection has succeeded.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        with open(self.database_connection_failed_path, "w+", encoding="utf-8") as file:
            file.write("false")

        self.logger.log_action("Database Connection Succeeded")

##--------------------start-of-create_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_database_connection(self, host_name:str, user_name:str, db_name:str, user_password:str) -> typing.Union[mysql.connector.connection.MySQLConnection, pooling.PooledMySQLConnection]:

        """

        Creates a connection to the database.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        host_name (str) : The host name of the database.\n
        user_name (str) : The user name of the database.\n
        db_name (str) : The name of the database.\n
        user_password (str) : The password of the database.\n

        Returns:\n
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) or None : The connection object to the database.\n

        """

        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            database= db_name,
            passwd=user_password)

        self.logger.log_action("Successfully connected to the " + db_name + " database")

        return connection
    
##--------------------start-of-clear_credentials_File()---------------------------S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def clear_credentials_file(self) -> None:

        """
        
        Clears the credentials file.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        with open(self.credentials_path, "w+", encoding="utf-8") as file: ## clears the credentials file allowing for a different database connection to be added if the current one is valid
            file.truncate()

##--------------------start-of-execute_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def execute_query(self, query:str) -> None:

        """

        Executes a query to the database\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        query (str) : The query to be executed.\n

        Returns:\n
        None.\n

        """

        self.logger.log_action("--------------------------------------------------------------")
    
        self.cursor.execute(query) ## type: ignore
        
        self.connection.commit() ## type: ignore

        self.logger.log_action("The following query was sent and accepted by the database : ")
        self.logger.log_action(query.strip())

        self.logger.log_action("--------------------------------------------------------------")

##--------------------start-of-read_single_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_single_column_query(self, query:str) -> typing.List[str]:

        """

        reads a single column query from the database.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        query (str) : The query to be executed.\n

        Returns:\n
        results_actual (list - string) : The results of the query.\n

        """
        
        results_actual = []

        self.cursor.execute(query) ## type: ignore
        results = self.cursor.fetchall() ## type: ignore

        results_actual = [str(i[0]) for i in results]

        return results_actual
    
##--------------------start-of-insert_into_table()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def insert_into_table(self, table_name, data) -> None:

        """
        
        inserts data into a table.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        table_name (str) : The name of the table.\n
        data (dict) : The data to be inserted.\n

        Returns:\n
        None\n

        """

        columns = ", ".join(data.keys())
        values = ", ".join([f"'{value}'" for value in data.values()])

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        self.execute_query(query)

##--------------------start-of-read_multi_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_multi_column_query(self, query:str) -> typing.List[typing.List[str]]:

        """

        reads a multi column query from the database.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        query (str) : The query to be executed.\n

        Returns:\n
        results_by_column (list - list) : The results of the query.\n

        """

        self.cursor.execute(query) ## type: ignore

        results = self.cursor.fetchall() ## type: ignore

        if(len(results) == 0):
            return [[]] * self.cursor.description.__len__() if self.cursor.description else [[]] ## type: ignore

        results_by_column = [[] for i in range(len(results[0]))]
        
        for row in results:
            for i, value in enumerate(row):
                results_by_column[i].append(str(value))

        return results_by_column