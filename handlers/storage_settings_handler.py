## built-in modules
from datetime import datetime

import os
import shutil
import time
import base64
import typing

## custom modules
from modules.toolkit import Toolkit
from modules.file_ensurer import FileEnsurer
from modules.logger import Logger

from handlers.file_handler import FileHandler
from handlers.local_handler import LocalHandler
from handlers.remote_handler import RemoteHandler
from handlers.connection_handler import ConnectionHandler

class StorageSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings.
    
    """
##--------------------start-of-change_storage_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def change_storage_settings() -> None:
        
        """"

        Controls the pathing for all storage settings.

        """

        Toolkit.clear_console()

        storage_message = "What are you trying to do?\n\n1.Reset Local With Remote\n2.Reset Remote with Local\n3.Reset Local & Remote to Default\n4.Restore Backup\n5.Export Vocab Deck\n6.Import Vocab Deck"

        print(storage_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 6, storage_message)

        if(type_setting == "1"):
            
            StorageSettingsHandler.reset_local_with_remote()

            Toolkit.pause_console()

        elif(type_setting == "2"):

            RemoteHandler.reset_remote_storage()

            Toolkit.pause_console()
        
        elif(type_setting == "3"):

            StorageSettingsHandler.reset_local_and_remote_to_default()

            Toolkit.pause_console()

        elif(type_setting == "4"):
            StorageSettingsHandler.restore_backup()

        elif(type_setting == "5"):
            StorageSettingsHandler.export_deck()
            
        elif(type_setting == "6"):
            StorageSettingsHandler.import_deck()

##--------------------start-of-reset_local_with_remote()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def reset_local_with_remote(hard_reset:bool=False) -> None:

        """

        Resets local storage with remote storage.

        """

        ## local storage does not reset if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("local storage reset") == False):
            print("No valid database connection.\n")
            time.sleep(1)
            return

        with open(FileEnsurer.last_local_remote_overwrite_timestamp_path, 'r', encoding="utf-8") as file:
            strips_to_perform = " \n\x00"

            last_backup_date = file.read()

            last_backup_date = last_backup_date.strip(strips_to_perform)
        
        if(last_backup_date == ""):
            last_backup_date = "(NEVER)"

        if(hard_reset):
            confirm = "1"
        
        else:
            confirm = str(input("Warning, remote storage has not been updated since " + last_backup_date + ", all changes made to local storage after this will be lost. Are you sure you wish to continue? (1 for yes 2 for no):\n"))

        if(confirm == "1"):
            RemoteHandler.reset_local_storage()
            LocalHandler.load_words_from_local_storage()

            Toolkit.clear_console()

            Logger.log_action("Local has been reset with remote.", output=True, omit_timestamp=True)

        else:
            print("Cancelled.\n")

##--------------------start-of-reset_local_and_remote_to_default()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def reset_local_and_remote_to_default() -> None:

        """"

        Resets local and remote storage to default.

        """

        try:

            shutil.rmtree(FileEnsurer.kana_dir)
            shutil.rmtree(FileEnsurer.vocab_dir)

        ## if files are open, which they usually are when im testing this.
        except PermissionError:

            Toolkit.clear_console()

            print("Permission error, you likely have the config folder/files open. Please close all of that and try again. If issue persists contact Bikatr7 on github.\n")

            Toolkit.pause_console()

            return
        
        ## either way files are likely fucked so....
        ## mainly because it's easier just to delete local storage, reset it and then reset remote with it.. idk if thats good practice but meh.
        finally:

            FileEnsurer.ensure_files()

        RemoteHandler.reset_remote_storage(omit_print=True)

        LocalHandler.load_words_from_local_storage()

        Logger.log_action("Local & Remote have been reset to default", output=True, omit_timestamp=True)

##--------------------start-of-restore_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def restore_backup() -> None: 
                
        """

        Restores a local or remote backup.
        
        """ 

        Toolkit.clear_console()

        backup_message = "Which backup do you wish to restore?\n\n1.Local\n2.Remote\n"

        print(backup_message)

        type_backup = Toolkit.input_check(4, Toolkit.get_single_key(), 2, backup_message)

        if(type_backup == "1"):

            LocalHandler.restore_local_backup()

            Toolkit.pause_console()
            Toolkit.clear_console()

        elif(type_backup == "2"):

            RemoteHandler.restore_remote_backup()
            
            Toolkit.pause_console()
            Toolkit.clear_console()

        FileEnsurer.ensure_files()
        LocalHandler.load_words_from_local_storage()

##--------------------start-of-export_deck()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def export_deck() -> None:

        """
        
        Exports the current vocab deck to a file in the script directory.
        
        """ 

        file_name = "deck-" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".seisen"
        export_path = os.path.join(FileEnsurer.script_dir, file_name)

        is_first_portion = True

        with open(export_path, 'w', encoding="utf-8") as export_file:
            export_file.write("Seisen Vocab Deck\n")
            
            for path in FileEnsurer.vocab_paths:
                if(not FileHandler.is_file_damaged(path)):
                    with open(path, 'r', encoding="utf-8") as file:
                        content = file.read()
                        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

                        ## --- is the delimiter for portions of the deck.
                        ## Don't wanna write a delimiter at the start of the file.
                        if(is_first_portion):
                            is_first_portion = False
                        else:
                            export_file.write("\n---\n")

                        export_file.write(encoded_content)

        Toolkit.clear_console()

        print(f"{file_name} has been placed in the script directory.\n")
        
        Toolkit.pause_console()

##--------------------start-of-import_deck()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def import_deck() -> None:

        """

        Imports an external vocab deck into Seisen.

        """

        valid_import_paths = []
        valid_import_names = []

        import_deck = []

        portions_write: typing.Dict[str, typing.List[str]] = {}

        target_index = -1

        deck_to_import_prompt = ""

        for file_name in os.listdir(FileEnsurer.script_dir):

            if(file_name.endswith(".seisen")): 

                file_path = os.path.join(FileEnsurer.script_dir, file_name)
                file_name = file_name.replace(".seisen", "")

                valid_import_paths.append(file_path)
                valid_import_names.append(file_name)

                deck_to_import_prompt += file_name + "\n" 

        deck_to_import_prompt += "\nWhat deck would you like to import?"

        if(len(valid_import_paths) == 0):
                
            print("No decks to import.\n")

            Toolkit.pause_console()

            return

        try: ## user confirm will throw a UserCancel error if the user wants to cancel the backup restore.

            deck_to_import = Toolkit.user_confirm(deck_to_import_prompt)

            if(deck_to_import in valid_import_names):
                Toolkit.clear_console()

                target_index = valid_import_names.index(deck_to_import)

            else:
                print("Invalid Deck Choice.\n")
                time.sleep(Toolkit.sleep_constant)
                return

        except Toolkit.UserCancelError:
            Logger.log_action("\nCancelled deck import", output=True, omit_timestamp=True)
            time.sleep(Toolkit.sleep_constant)
            return
        
        with open(valid_import_paths[target_index], 'r', encoding="utf-8") as file:
            import_deck = file.readlines()

        if(import_deck[0] != "Seisen Vocab Deck\n"):
            print("Invalid Deck, please make sure the .seisen file is a Seisen Vocab Deck.\n")
            time.sleep(2)
            return
        
        ## Gets rid of the Seisen Vocab Deck Identifier
        import_deck.pop(0)

        portion_index = 0

        for line in import_deck:
            
            ## Delimiter for portions of the deck.
            if(line == "---\n"):
                portion_index += 1  # move to the next portion
                continue

            decoded_content = base64.b64decode(line.strip()).decode('utf-8')
            portion = FileEnsurer.vocab_paths[portion_index]

            if(portion not in portions_write):
                portions_write[portion] = []

            portions_write[portion].append(decoded_content)

        for portion, lines in portions_write.items():
            with open(portion, 'w+', encoding="utf-8") as file:
                file.writelines(lines)

        LocalHandler.load_words_from_local_storage()

        Logger.log_action("Imported the " + deck_to_import + " vocab deck.", output=True, omit_timestamp=True)

        time.sleep(2)