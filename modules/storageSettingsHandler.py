## built-in modules
import msvcrt
import shutil

## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

from modules.vocab import vocab as vocab_blueprint 

from modules.csep import csep as csep_blueprint

class storageSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings
    
    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, local_handler:localHandler, remote_handler:remoteHandler) -> None:

        """
        
        Initializes the storageSettingsHandler class.\n

        Parameters:\n
        local_handler (object - localHandler) : The local handler object.\n
        remote_handler (object - remoteHandler) : The remote handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.local_handler = local_handler

        self.remote_handler = remote_handler

##--------------------start-of-change_storage_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_storage_settings(self) -> None:
        
        """"

        Controls the pathing for all storage settings.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n

        """

        self.local_handler.toolkit.clear_console()

        storage_message = "What are you trying to do?\n\n1.Reset Local With Remote\n2.Reset Remote with Local\n3.Reset Local & Remote to Default\n4.Restore Backup\n"

        print(storage_message)

        type_setting = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 4, storage_message)

        if(type_setting == "1"):
            
            self.reset_local_with_remote()

        elif(type_setting == "2"):

            self.remote_handler.reset_remote_storage()
        
        elif(type_setting == "3"):

            self.reset_local_and_remote_to_default()

        elif(type_setting == "4"):
            self.restore_backup()
            

##--------------------start-of-reset_local_with_remote()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_local_with_remote(self) -> None:

        """

        Resets local storage with remote storage.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n

        """

        with open(self.remote_handler.last_local_remote_backup_accurate_path, 'r', encoding="utf-8") as file:
            last_backup_date = str(file.read().strip()).strip('\x00').strip()
        
        if(last_backup_date == ""):
            last_backup_date = "(NEVER)"

        confirm = str(input("Warning, remote storage has not been updated since " + last_backup_date + ", all changes made to local storage after this will be lost. Are you sure you wish to continue? (1 for yes 2 for no)\n"))

        if(confirm == "1"):
            self.remote_handler.reset_local_storage()
            self.local_handler.load_words_from_local_storage()
        else:
            pass

##--------------------start-of-reset_local_and_remote_to_default()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_local_and_remote_to_default(self) -> None:

        """"

        Resets local and remote storage to default.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n

        """

        shutil.rmtree(self.local_handler.fileEnsurer.kana_dir)
        shutil.rmtree(self.local_handler.fileEnsurer.vocab_dir)

        self.local_handler.fileEnsurer.ensure_files()

        self.remote_handler.reset_remote_storage()

        self.local_handler.load_words_from_local_storage()

##--------------------start-of-restore_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def restore_backup(self) -> None: 
                
        """

        Restores a local or remote backup.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n
        
        """ 

        self.local_handler.toolkit.clear_console()

        backup_message = "Which backup do you wish to restore?\n\n1.Local\n2.Remote\n"

        print(backup_message)

        type_backup = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 2, backup_message)

        if(type_backup == "1"):

            self.local_handler.restore_local_backup()
            self.local_handler.fileEnsurer.ensure_files()
            self.local_handler.load_words_from_local_storage()

        elif(type_backup == "2"):

            self.remote_handler.restore_remote_backup()
            self.local_handler.fileEnsurer.ensure_files()
            self.local_handler.load_words_from_local_storage()