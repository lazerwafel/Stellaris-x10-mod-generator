import os
import re
import shutil
import json

modifiers = []

config_file = open("config.json", "r")
config = json.load(config_file)
config_file.close()

hoi4dir = config["hoi4dir"]
print("Hearts of Iron 4 X10 Mod Creation Script by iusNiko")
print("Using HoI4 Directory: " + hoi4dir)
print("PLEASE MAKE SURE THAT THE HOI4 DIRECTORY IS CORRECT! YOU CAN CHANGE IT IN THE CONFIG.JSON FILE")
print("If you've changed the directory, please restart the script")

factor = input("Enter desired factor: ")

root_dir = "./workdir"
base_dir = "./base"

shutil.rmtree(root_dir)

print("Removed Workdir files")

shutil.copytree(base_dir + "/", root_dir)

print("Copied Base files")

mod_file = open("modifiers.txt", "r")
for modifier in mod_file:
    modifiers.append(modifier.strip())
mod_file.close()

mod_file = open("dynamic_modifiers.txt", "r")
for modifier in mod_file:
    modifiers.append(modifier.strip())
mod_file.close()

for directory, subdirectories, files in os.walk(root_dir):
    for file in files:
        edited_file = open(os.path.join(directory, file), "r")
        print("Editing file: " + os.path.join(directory, file))
        new_content = ""
        try:
            edited_file.readlines()
        except:
            continue
        edited_file = open(os.path.join(directory, file), "r")
        for line in edited_file:
            new_line = line
            numbers = re.findall(r"-?\d+\.?\d*", line)
            if len(numbers) != 0:
                for modifier in modifiers:
                    modifier_pos = line.find(modifier[1:])
                    if(modifier_pos == -1):
                        continue
                    if (modifier_pos == 0 or (modifier_pos > 0 and line[modifier_pos - 1] == " ") or (modifier_pos > 0 and line[modifier_pos - 1] == "\t")) and (line[modifier_pos + len(modifier) - 1] == " " or line[modifier_pos + len(modifier) - 1] == "="):
                        
                        if float(numbers[0]) < 0 and modifier[0] == '+':
                            continue
                        if float(numbers[0]) > 0 and modifier[0] == '-':
                            continue
                            
                        new_line = line.replace(str(numbers[0]), "{:.3f}".format(float(numbers[0]) * factor))
                        break
            new_content += new_line
        edited_file.close()
        edited_file = open(os.path.join(directory, file), "w")
        edited_file.write(new_content)