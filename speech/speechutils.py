

from callbacks.callbacks import *

import winspeech
from utils import configreader

TRIGGER_KEYWORD = configreader.get_preferences().get_trigger_keyword()
raw_phrases = configreader.get_phrases()
reverse = {tuple(phrase_tuple): callback_method for callback_method, phrase_tuple in raw_phrases.items()}
phrases = {}  # {<phrases>:<callback function name string>}


def _prepend_trigger_keyword(phrase):
    return TRIGGER_KEYWORD + " " + phrase


def initialize():
    """ Start listening for phrases """
    for phrase_tuple in raw_phrases.values():
        new_phrase_list = []
        for phrase in phrase_tuple:
            if phrase[0] != "*":
                new_phrase_list.append(phrase)
            else:
                # If the command has a wild card we'll append both versions i.e the command on its own
                # and the command prepended by the trigger keyword
                new_phrase_list.append(phrase[1:])
                new_phrase_list.append(_prepend_trigger_keyword(phrase[1:]))

        phrases[tuple(new_phrase_list)] = reverse[tuple(phrase_tuple)]

    for phrase_list in phrases.keys():
        winspeech.listen_for(phrase_list, eval(phrases[phrase_list]))
        #print(phrase_list)

    winspeech.listen_for_anything(default_listener)
