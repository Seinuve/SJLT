## built-in libraries
import typing

## custom modules
from modules.toolkit import Toolkit

from handlers.local_handler import LocalHandler


##--------------------start-of-searcher------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Searcher:

    '''

    The search class is used to search for things in localHandler.\n
        
    '''

##--------------------start-of-get_vocab_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_vocab_print_item_from_id(vocab_id:int) -> str:

        """
        
        Gets a print item for a vocab given an id.

        Parameters:
        vocab_id (int) : the id of the vocab we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.
        
        """
            
        target_vocab = None

        for vocab in LocalHandler.vocab:
            if(vocab.word_id == vocab_id):
                target_vocab = vocab

        if(target_vocab == None):
            raise Searcher.IDNotFoundError(vocab_id)
        
        mini_csep_print = [str(csep.csep_id) for csep in target_vocab.testing_material_answer_all]

        print_item = (
            f"---------------------------------\n"
            f"Vocab: {target_vocab.testing_material}\n"
            f"Romaji: {target_vocab.romaji}\n"
            f"Furigana: {target_vocab.furigana}\n"
            f"Definition: {target_vocab.testing_material_answer_main}\n"
            f"Incorrect Guesses: {target_vocab.incorrect_count}\n"
            f"Correct Guesses: {target_vocab.correct_count}\n"
            f"ID: {target_vocab.word_id}\n"
            f"CSEP ID(S): {mini_csep_print}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_csep_print_item_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_csep_print_item_from_id(csep_id:int) -> str:

        """
        
        Gets a print item for a csep given a csep id.

        Parameters:
        csep_id (int) : the id of the vocab we are getting a print item for.

        Returns:
        print_item (str) : the print item for the id.\n
        
        """
        
        target_vocab = None
        target_csep = None

        for vocab in LocalHandler.vocab:
            for csep in vocab.testing_material_answer_all:
                if(csep.csep_id == csep_id):
                    target_csep = csep
                    target_vocab = vocab

        if(target_csep == None or target_vocab == None):
            raise Searcher.IDNotFoundError(csep_id)
        
        print_item = (
            f"---------------------------------\n"
            f"CSEP: {target_csep.csep_value}\n"
            f"CSEP ID: {target_csep.csep_id}\n"
            f"VOCAB: {target_vocab.testing_material}\n"
            f"VOCAB ID: {target_csep.word_id}\n"
            f"WORD TYPE: {target_csep.word_type}\n"
            f"---------------------------------\n"
        )

        return print_item
    
##--------------------start-of-get_csep_print_items_from_vocab_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_csep_print_items_from_vocab_id(vocab_id:int) -> typing.List[str]:

        """
        
        Gets a print item for a csep given a vocab id.

        Parameters:
        vocab_id (int) : the id of the vocab we are getting a print item for.

        Returns:
        print_items (list - str) : the print item for the id.
        
        """
            
        target_vocab = None
        print_items = []

        for vocab in LocalHandler.vocab:
            if(vocab.word_id == vocab_id):
                target_vocab = vocab

        if(target_vocab == None):
            raise Searcher.IDNotFoundError(vocab_id)
        
        for csep in target_vocab.testing_material_answer_all:

            print_item = (
                f"---------------------------------\n"
                f"CSEP: {csep.csep_value}\n"
                f"CSEP ID: {csep.csep_id}\n"
                f"VOCAB ID {csep.word_id}\n"
                f"WORD TYPE: {csep.word_type}\n"
                f"---------------------------------\n"
            )

            print_items.append(print_item)

        return print_items

##--------------------start-of-get_vocab_term_from_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_vocab_term_from_id(vocab_id:int) -> str:

        """
        
        Gets a vocab term given an id.

        Parameters:
        vocab_id (int) : the id for the term we are searching for.

        Returns:
        term (str) : the term if found, otherwise "-1".

        """

        term = "-1"
        
        for vocab in LocalHandler.vocab:
            if(vocab.word_id == vocab_id):
                term = vocab.testing_material

        return term
    
##--------------------start-of-get_id_from_term()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_id_from_vocab_term(term:str) -> int:

        """
        
        Gets a vocab id given an verb.

        Parameters:
        tern (str) : the term for the id we are searching for.

        Returns:
        final_id (int) : the id if found, otherwise -1.

        """

        matching_ids = []

        id_print_message = ""

        final_id = -1

        for vocab in LocalHandler.vocab:
            if(vocab.testing_material == term):
                matching_ids.append(vocab.word_id)

        if(len(matching_ids) == 0):
            return final_id
        elif(len(matching_ids) == 1):
            final_id = matching_ids[0]
            return final_id
        
        for id in matching_ids:
            id_print_message += Searcher.get_vocab_print_item_from_id(id)

        id_print_message += "\n\nWhich vocab are you looking for? (Enter position 1-" + str(len(matching_ids)) + ")"

        target_index = int(Toolkit.input_check(4, Toolkit.get_single_key(), len(matching_ids), id_print_message)) - 1

        final_id = matching_ids[target_index]

        return final_id
    
##--------------------start-of-get_ids_from_japanese()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def get_ids_from_japanese(term:str) -> typing.List[int]:
    
        """
        
        Gets vocab ids that match a given japanese term.

        Parameters:
        term (str) : the term we are searching with.\n

        Returns:
        vocab_ids (list = int) : matching vocab ids.\n

        """

        vocab_ids = []

        for vocab in LocalHandler.vocab:

            if(term == vocab.testing_material or term == vocab.furigana):
                vocab_ids.append(vocab.word_id)
            
        return vocab_ids

##--------------------start-of-get_ids_from_alpha_term()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_ids_from_alpha_term(term:str) -> typing.Tuple[typing.List[int], typing.List[int]]:

        """
        
        Gets vocab and csep ids that match a given term.

        Parameters:
        term (str) : the term we are searching with.

        Returns:
        vocab_ids (list = int) : matching vocab ids.
        csep_ids (list - int) : matching csep ids.

        """

        vocab_ids = []
        csep_ids = []

        for vocab in LocalHandler.vocab:

            ## if term matches romaji or definition 
            if(vocab.romaji == term or vocab.testing_material_answer_main == term):
                vocab_ids.append(vocab.word_id)

            for csep in vocab.testing_material_answer_all:
                if(csep.csep_value == term):
                    vocab_ids.append(vocab.word_id)
                    csep_ids.append(csep.csep_id)
            
            
        vocab_ids = [int(id) for id in set(vocab_ids)]
        csep_ids = [int(id) for id in set(csep_ids)]

        return vocab_ids, csep_ids
        
##--------------------start-of-IDNotFoundError------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    class IDNotFoundError(Exception):

        """
    
        Is raised when an id is not found.

        """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        def __init__(self, id_value:int):

            """
            
            Initializes a new IDNotFoundError Exception.

            Parameters:\n
            id_value (int) : The id value that wasn't found.

            """

            self.message = f"ID '{id_value}' not found."