# -*- coding: utf-8 -*-

# import built-in module
import os
import json
import warnings

# import third-party modules

# import your own module
from pons_dictionary.translation_entry import TranslationEntry

def gen_dict_extract(key, var):
    """
    From https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
    """
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

if __name__ == "__main__":
    """
    Batch TranslationEntry tester.
    
    Goal:       Identify unhandled behavior from TranslationEntry.
    Procedure:  We go through a folder of json content from API calls and input each source and target
                string into TranslationEntry, and we look at the final result. Offending strings will be added
                to the testing set.
    """

    json_data_folder = 'pons_api_reference_data/dede'
    see_all_entries = True

    warnings.filterwarnings("error")

    for file in os.listdir(json_data_folder):
        full_file_path = json_data_folder + "/" + file
        with open(full_file_path) as f:
            json_data = json.load(f)

            source_strings = list(gen_dict_extract('source', json_data[0]))
            target_strings = list(gen_dict_extract('target', json_data[0]))

            for source, target in zip(source_strings, target_strings):
                te_source = None
                te_target = None
                try:
                    te_source = TranslationEntry(source, False, False, True)
                    te_target = TranslationEntry(target, False, False, True)
                except UserWarning as w:
                    print("====================================")
                    print("FILE: " + full_file_path)
                    print("WARNING: " + str(w))
                    print("\tSOURCE")
                    print("\traw string: " + source)
                    print("\tTranslationEntry: " + str(te_source))
                    print("\tTARGET")
                    print("\traw string: " + target)
                    print("\tTranslationEntry: " + str(te_target))
                    input("")
                else:
                    if see_all_entries:
                        print("====================================")
                        print("FILE: " + full_file_path)
                        print("\tSOURCE")
                        print("\traw string: " + source)
                        print("\tTranslationEntry: " + str(te_source))
                        print("\tTARGET")
                        print("\traw string: " + target)
                        print("\tTranslationEntry: " + str(te_target))
                        input("")

