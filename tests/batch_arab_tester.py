# -*- coding: utf-8 -*-

# import built-in module
import os
import json
import warnings

# import third-party modules

# import your own module
from pons_dictionary.arab import Arab

if __name__ == "__main__":
    """
    Batch Arab tester.

    Goal:       Identify unhandled behavior from Arab.
    Procedure:  We go through a folder of json content from API calls and input each arab dict string into Arab, and we 
                look at the final result. Offending dicts will be added to the testing set.
    """

    json_data_folder = 'pons_api_reference_data/fr_to_de'
    see_all_entries = True

    warnings.filterwarnings("error")

    for file in os.listdir(json_data_folder):
        full_file_path = json_data_folder + "/" + file
        with open(full_file_path) as f:
            json_data = json.load(f)

            for hit in json_data[0]['hits']:
                if "roms" in hit:
                    for rom in hit['roms']:
                        for arab in rom['arabs']:
                            try:
                                a = Arab(arab, False, False, True)
                            except UserWarning as w:
                                print("====================================")
                                print("FILE: " + full_file_path)
                                print("WARNING: " + str(w))
                                print("\tARAB")
                                print("\traw header: " + arab["header"])
                                if a.headword is not None:
                                    print("\theadword: " + a.headword)
                                else:
                                    print("\theadword: None")
                                input("")
                            else:
                                if see_all_entries:
                                    print("====================================")
                                    print("FILE: " + full_file_path)
                                    print("\tARAB")
                                    print("\traw header: " + arab["header"])
                                    if a.headword is not None:
                                        print("\theadword: " + a.headword)
                                    else:
                                        print("\theadword: None")
                                    input("")

