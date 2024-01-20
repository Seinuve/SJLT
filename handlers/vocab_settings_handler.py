## built-in modules
import typing
import time

## custom modules
from handlers.local_handler import LocalHandler
from handlers.remote_handler import RemoteHandler
from handlers.file_handler import FileHandler

from modules.searcher import Searcher
from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from entities.vocab import Vocab as vocab_blueprint 
from entities.testing_material import TestingMaterial as testing_material_blueprint
from entities.synonym import Synonym as synonym_blueprint
from entities.reading import Reading as reading_blueprint
from entities.typo import Typo as typo_blueprint
from entities.incorrect_typo import IncorrectTypo as incorrect_typo_blueprint

from entities.vocab import Vocab
from entities.synonym import Synonym
from entities.reading import Reading
from entities.typo import Typo
from entities.incorrect_typo import IncorrectTypo
from entities.testing_material import TestingMaterial

class VocabSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings.
    
    """
##--------------------start-of-change_vocab_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def change_vocab_settings() -> None:

        """

        Controls the pathing for all vocab settings.

        """ 

        Logger.log_action("User is changing vocab settings.")

        vocab_message = "What are you trying to do?\n\n1.Add Entity\n2.Edit Entity\n3.Delete Entity\n4.Search Entity\n"

        print(vocab_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 4, vocab_message)

        if(type_setting == "1"):
            VocabSettingsHandler.add_entity()

##--------------------start-of-add_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def add_entity() -> None:

        """

        Adds a vocab entity to the database.

        """ 

        Logger.log_action("User is adding a vocab entity.")

        entity_message = "What type of entity are you trying to add?\n\n1.Add Vocab\n2.Add Synonym to Existing Vocab\n3.Add TestingMaterial to Existing Vocab\n4.Add Reading to Existing Vocab\n5.Add Typo to Existing Vocab\n6.Add IncorrectTypo to Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 6, entity_message)

        if(type_setting == "1"):
            VocabSettingsHandler.add_vocab()

##--------------------start-of-edit_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_entity() -> None:

        """

        Edits a vocab entity in the database.

        """ 

        Logger.log_action("User is editing a vocab entity.")

        entity_message = "What type of entity are you trying to edit?\n\n1.Edit Vocab\n2.Edit Synonym of Existing Vocab\n3.Edit TestingMaterial of Existing Vocab\n4.Edit Reading of Existing Vocab\n5.Edit Typo of Existing Vocab\n6.Edit IncorrectTypo of Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 6, entity_message)

##--------------------start-of-delete_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def delete_entity() -> None:

        """

        Deletes a vocab entity from the database.

        """ 

        Logger.log_action("User is deleting a vocab entity.")

        entity_message = "What type of entity are you trying to delete?\n\n1.Delete Vocab\n2.Delete Synonym of Existing Vocab\n3.Delete TestingMaterial of Existing Vocab\n4.Delete Reading of Existing Vocab\n5.Delete Typo of Existing Vocab\n6.Delete IncorrectTypo of Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 6, entity_message)

##--------------------start-of-search_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def search_entity() -> None:

        """

        Searches for a vocab entity in the database.

        """ 

        pass

##--------------------start-of-add_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_vocab() -> None:

        """

        Adds a vocab entity to the database.

        """ 

        ## gets new vocab id
        new_vocab_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(6))

        ## raw strings
        raw_testing_material:typing.List[str] = []
        raw_romaji:typing.List[str] = []
        raw_furigana:typing.List[str] = []
        raw_synonyms:typing.List[str] = []

        ## actual objects
        testing_material:typing.List[TestingMaterial] = []
        readings:typing.List[Reading] = []
        synonyms:typing.List[Synonym] = []

        ## get vocab components
        try:

            ## testing material
            curr_raw_testing_material = Toolkit.user_confirm("Please enter your vocab's main testing material (testing material are kanji/kana that are used as the material to be tested on).")
            raw_testing_material.append(curr_raw_testing_material)

            while(input(f"Enter 1 if {curr_raw_testing_material} has any additional testing material, otherwise enter 2 (testing material are kanji/kana that are used as the material to be tested on).") == "1"):
                Toolkit.clear_stream()
                raw_testing_material.append(Toolkit.user_confirm("Please enter your vocab's additional testing material (testing material are kanji/kana that are used as the material to be tested on)."))

            ## romaji and furigana (reading)
            curr_raw_romaji = Toolkit.user_confirm(f"Please enter {curr_raw_testing_material}'s main romaji (romaji are the pronunciation of the testing material, your main romaji should match the main testing material).")
            curr_raw_furigana = Toolkit.user_confirm(f"Please enter {curr_raw_romaji}'s furigana (furigana is the kana spelling of {curr_raw_romaji}).") 

            raw_romaji.append(curr_raw_romaji)
            raw_furigana.append(curr_raw_furigana)

            while(input(f"Enter 1 if {raw_testing_material} has any additional romaji, otherwise enter 2 (romaji are the pronunciation of the testing material).") == "1"):
                Toolkit.clear_stream()
                raw_romaji.append(Toolkit.user_confirm(f"Please enter {raw_testing_material}'s additional romaji (romaji are the pronunciation of the testing material. Additional Romaji can match any)."))
                raw_furigana.append(Toolkit.user_confirm(f"Please enter {raw_romaji[-1]}'s furigana (furigana is the kana spelling of {raw_romaji[-1]})."))

            ## synonyms
            raw_synonyms.append(Toolkit.user_confirm(f"Please enter {curr_raw_testing_material}'s main synonym (Synonyms are the definition of the testing material. Your main synonym should match the main testing material)."))

            while(input(f"Enter 1 if {raw_testing_material} has any additional synonyms, otherwise enter 2 (Synonyms are the definition of the testing material).") == "1"):
                Toolkit.clear_stream()
                raw_synonyms.append(Toolkit.user_confirm(f"Please enter {raw_testing_material}'s additional synonym (Synonyms are the definition of the testing material. Additional synonyms can match any)."))

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        ## assemble actual objects and assign ids
        for i in range(len(raw_testing_material)):
            new_testing_material_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(12))
            testing_material.append(testing_material_blueprint(new_vocab_id, new_testing_material_id, raw_testing_material[i]))

            stuff_to_write = [new_vocab_id, new_testing_material_id, raw_testing_material[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_testing_material_path, stuff_to_write)

        for i in range(len(raw_romaji)):
            new_reading_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(10))
            readings.append(reading_blueprint(new_vocab_id, new_reading_id, raw_furigana[i], raw_romaji[i]))

            stuff_to_write = [new_vocab_id, new_reading_id, raw_furigana[i], raw_romaji[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_readings_path, stuff_to_write)

        for i in range(len(raw_synonyms)):
            new_synonym_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))
            synonyms.append(synonym_blueprint(new_vocab_id, new_synonym_id, raw_synonyms[i]))

            stuff_to_write = [new_vocab_id, new_synonym_id, raw_synonyms[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_synonyms_path, stuff_to_write)

        ## assemble vocab object
        new_vocab = vocab_blueprint(new_vocab_id, testing_material, synonyms[0], synonyms, readings, incoming_correct_count=0, incoming_incorrect_count=0)

        ## write to file
        stuff_to_write = [new_vocab_id, new_vocab.correct_count, new_vocab.incorrect_count]
        FileHandler.write_seisen_line(FileEnsurer.vocab_path, stuff_to_write)

        ## add to current session
        LocalHandler.vocab.append(new_vocab)