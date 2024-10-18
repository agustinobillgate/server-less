import xml.etree.ElementTree as ET
from pathlib import Path
import os
from functions.additional_functions import *

all_operations = []

def createMapping(path):
    global all_operations
    # Load the XML file
    xml_file = path + '/resourceModel.xml'
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Open the output file for writing
    output_file_path = path + '/_mapping.txt'
    with open(output_file_path, 'w') as output_file:
        output_file.write("service,function\n")

        # Iterate over <prgs:resource> elements
        for resource in root.findall(".//{http://www.progress.com/caf/camel/component/prgrs}resource"):
            resource_path = resource.get('path').replace("/","")

            # Iterate over <prgs:operation> elements within the resource
            for operation in resource.findall("{http://www.progress.com/caf/camel/component/prgrs}operation"):
                operation_name = operation.get('name').replace("-","_")
                
                if substring(operation_name,0,4) == "web_":
                    operation_name = substring(operation_name,4,len(operation_name))

                output_file.write(f"{resource_path},{operation_name}\n")
                
                if not operation_name in all_operations:
                    all_operations.append(operation_name.strip(" "))
    

# In progress, check the workspace of developer studio and go to the project
# Go to <Openedge Workspace>\<Project Name>\.services\Expose\rest\
subfolders = [ f.path for f in os.scandir(os.getcwd() + "/modules") if f.is_dir() ]
print(subfolders)
all_operation_path = os.getcwd() + "/modules/all_operation.txt"

for subfolder in subfolders:
    createMapping(subfolder)

with open(all_operation_path, 'w') as output_file_all:
    all_operations_str = "\n".join(all_operations)
    output_file_all.write(f"{all_operations_str}")
