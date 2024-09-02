import os
import re
import sqlalchemy as sa
from importlib import import_module

# Paths to the folders
models_folder = r'D:\docker\pixcdk\image\src\models'
source_folder = r'D:\docker\pixcdk\image\src\dotp'
destination_folder = r'D:\docker\pixcdk\image\output'

# Ensure the output folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Function to get the model class attributes
def get_model_dict_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    model_name = None
    columns = []
    
    for line in lines:
        # Match the table name
        if '__tablename__' in line:
            match = re.search(r'__tablename__\s*=\s*[\'"](\w+)[\'"]', line)
            if match:
                model_name = match.group(1)
        
        # Match column names
        match = re.search(r'sa\.Column\(([^,]+),', line)
        if match:
            column_name = match.group(1).strip()
            columns.append(column_name)
    
    model_dict = {
        "name": model_name,
        "items": columns
    }
    
    return model_dict


def get_model_attributes(models_folder):
    attributes = {}
    for attr_name in dir(models_folder):
        attr = getattr(models_folder, attr_name)
        if isinstance(attr, sa.Column):
            attributes[attr_name.lower()] = attr_name
    return attributes


# Function to replace old attribute names with the new ones in the .p files
def replace_in_file(source_path, destination_path, model_attributes):
    print("Process:", source_path)
    with open(source_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # for table_name, attributes in model_attributes.items():
    #     for old_attr, new_attr in attributes.items():
    #         old_pattern = re.compile(rf'{table_name}\.{old_attr}\b', re.IGNORECASE)
    #         content = old_pattern.sub(f'{table_name}.{new_attr}', content)
    
    with open(destination_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Load all model classes and store their attributes
model_attributes = {}
for filename in os.listdir(models_folder):
    if filename is not None  and filename != '__pycache__' and filename != '__init__.py':
        file_path = "D:\\docker\\pixcdk\\image\\src\\models\\" + filename
        model_dict = get_model_dict_from_file(file_path)
        
        # print(model_dict)



# Process each .p file
for filename in os.listdir(source_folder):

    if filename.endswith('.p'):
        # print(filename)
        source_file_path = os.path.join(source_folder, filename)
        destination_file_path = os.path.join(destination_folder, filename)
        
        replace_in_file(source_file_path, destination_file_path, model_dict)
        print(f"Processed {destination_file_path} ")

print("All files processed and saved to the output folder.")
