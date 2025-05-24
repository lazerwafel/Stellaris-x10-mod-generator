import os
import re
import shutil
import json

modifiers = []

config_file = open("config.json", "r")
config = json.load(config_file)
config_file.close()

hoi4dir = config["Stellarisdir"]
print("original script created by iusNiko")
print("Stellaris X10 version forked by lazerwafel")
print("Using Stellaris Directory: " + hoi4dir)
print("PLEASE MAKE SURE THAT THE Stellaris DIRECTORY IS CORRECT! YOU CAN CHANGE IT IN THE CONFIG.JSON FILE")
print("If you've changed the directory, please restart the script")

factor = float(input("Enter desired factor: "))

if hoi4dir[len(hoi4dir) - 1] != "/" and hoi4dir[len(hoi4dir) - 1] != "\\":
    hoi4dir = hoi4dir + "/"

mod_root_dir = "./mod/"

if os.path.exists(mod_root_dir):
    shutil.rmtree(mod_root_dir)

print("Removed existing mod files")

for dirToCopy in config["include"]:
    shutil.copytree(hoi4dir + dirToCopy, mod_root_dir + dirToCopy)

print("Copied vanilla files")

mod_file = open(config["modifiers_list"], "r")
for modifier in mod_file:
    if(modifier[0] == '#'):
        continue
    modifiers.append(modifier.strip())
mod_file.close()


# Edit copied files
for directory, subdirectories, files in os.walk(mod_root_dir):
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
                            
                        new_line = line.replace(str(numbers[0]), "{:.3f}".format(float(numbers[0]) * factor))
                        break
            new_content += new_line
        edited_file.close()
        edited_file = open(os.path.join(directory, file), "w")
        edited_file.write(new_content)

# Create "defines"

defines_folder = mod_root_dir + "common/defines/"

os.makedirs(defines_folder, exist_ok=True)

for define in config["defines"]:
    print("Creating define file: " + define)
    define_file = open(defines_folder + define, "w")
    for property, value in config["defines"][define].items():
        define_file.write(property + " = " + str(value) + "\n")
    define_file.close()
