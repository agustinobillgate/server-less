#---------------------------------------------------------------------------
# Update dari folder:
# D:\VHP-Projects\vhp-master-source\VHPWebBased\.services\Expose\rest
# copy ke:
# D:\VHP-Projects\vhp-serverless\modules
#---------------------------------------------------------------------------

import xml.etree.ElementTree as ET
from pathlib import Path
import os, shutil
from functions.additional_functions import *

all_operations = []

gitlab_xml = f"C:/Users/Dev-Bill.G/Downloads/VHPMobile-Webservice/VHPMobile/webservice/.services/Expose/rest"
vhp_projects_xml = f"C:/Users/Dev-Bill.G/api-python/vhp-serverless/modules/VHPMobile"

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
            # print(resource_path)
            # Iterate over <prgs:operation> elements within the resource
            for operation in resource.findall("{http://www.progress.com/caf/camel/component/prgrs}operation"):
                operation_name = operation.get('name').replace("-","_")
                
                if substring(operation_name,0,4) == "web_":
                    operation_name = substring(operation_name,4,len(operation_name))

                output_file.write(f"{resource_path},{operation_name}\n")
                # print(f"{resource_path},{operation_name}")
                
                if not operation_name in all_operations:
                    all_operations.append(operation_name.strip(" "))
    

# In progress, check the workspace of developer studio and go to the project
# Go to <Openedge Workspace>\<Project Name>\.services\Expose\rest\
subfolders = [ f.path for f in os.scandir(os.getcwd() + "/modules/VHPMobile") if f.is_dir() ]
all_operation_path = os.getcwd() + "/modules/all_operation.txt"

for subfolder in subfolders:
    print(subfolder)
    curr_module = os.path.basename(subfolder)
    xml_gitlab1 = f"{gitlab_xml}/{curr_module}/resourceModel.xml"
    xml_module = f"{subfolder}/resourceModel.xml"
    
    if os.path.isfile(xml_gitlab1) and Path(xml_gitlab1).exists():
        os.makedirs(os.path.dirname(xml_module), exist_ok=True)
        shutil.copyfile(xml_gitlab1, xml_module)
        print(f"Copied: {xml_gitlab1} → {xml_module}")
        print("-----------------------------------------------")
        createMapping(subfolder)  # Move this inside the if
    else:
        print(f"Source file not found: {xml_gitlab1}")
        print("-----------------------------------------------")
        # Don't copy or create mapping if file doesn't exist

with open(all_operation_path, 'w') as output_file_all:
    all_operations_str = "\n".join(all_operations)
    output_file_all.write(f"{all_operations_str}")
