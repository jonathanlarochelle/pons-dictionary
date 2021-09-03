# -*- coding: utf-8 -*-

# import built-in module
import os
import json
import warnings

# import third-party modules

# import your own module
from pons_dictionary.entry import Rom

if __name__ == "__main__":
    """
    Batch Rom tester.

    Goal:       Identify unhandled behavior from Rom.
    Procedure:  We go through a folder of json content from API calls and input each rom dict string into Rom, and we 
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
                        try:
                            r = Rom(rom, False, False, True)
                        except UserWarning as w:
                            print("====================================")
                            print("FILE: " + full_file_path)
                            print("WARNING: " + str(w))
                            print("\tARAB")
                            print("\theadword_full: " + rom["headword_full"])
                            print("\theadword: " + r.headword)
                            input("")
                        else:
                            if see_all_entries:
                                print("====================================")
                                print("FILE: " + full_file_path)
                                print("\tARAB")
                                print("\theadword_full: " + rom["headword_full"])
                                print("\theadword: " + r.headword)
                                input("")

