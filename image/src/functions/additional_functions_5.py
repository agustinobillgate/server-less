import sqlalchemy as sa
from sqlalchemy.exc import OperationalError

# from models import Sourcetext, Desttext

import importlib
import math,re

import dataclasses
from dataclasses import field, fields, dataclass, MISSING

from datetime import date, datetime, time
from typing import List,Dict,Type, Optional, Callable, Union
from cryptography.fernet import Fernet

import threading, hashlib,pytz,inspect, os, base64
import boto3, botocore
import uuid
import pandas as pd
import operator

from typing import TypeVar, Generic

T = TypeVar('T')

os.environ['AWS_ROLE_ARN'] = "arn:aws:iam::341938954922:user/christofer"
os.environ['AWS_ACCESS_KEY_ID'] = "AKIAU7HJGMKVE2H37NYU"
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-1'

local_storage = threading.local()
local_storage.combo_flag = False    
s3_bucket_name = 'elasticbeanstalk-ap-southeast-1-341938954922'


def create_model(model_name: str, create_fields: Dict[str, Type], default_values=None):
    if default_values is None:
        default_values = {}

    fields = {}
    post_init_defaults = {}

    def post_init_method(self):
        for name, value in post_init_defaults.items():
            setattr(self, name, value)

    for name, field_type in create_fields.items():
        set_default_value = True
        if name in default_values:
            set_default_value = False

        if type(field_type) == list:
            inner_type = field_type[0]
            fields[name] = List[inner_type]

            if len(field_type) == 2:
                size = field_type[1]
            else:
                size = 0

            if set_default_value:
                default_values[name] = lambda: []

                if inner_type == int: post_init_defaults[name] = [0] * size
                elif inner_type == float: post_init_defaults[name] = [0.0] * size
                elif inner_type == bool: post_init_defaults[name] = [False] * size
                elif inner_type == str: post_init_defaults[name] = [""] * size
                else: post_init_defaults[name] = [None] * size

        else:
            fields[name] = field_type
            if set_default_value:

                if field_type == int: default_values[name] = 0
                elif field_type == float: default_values[name] = 0.0
                elif field_type == bool: default_values[name] = False
                elif field_type == str: default_values[name] = ""
                else: default_values[name] = None         
        
    return [], dataclass(type(model_name, (object,), {
        '__annotations__': fields,
        '__post_init__': post_init_method,
        **{k: field(default_factory=lambda v=v: v) for k, v in default_values.items()}  # set default values
    }))


def create_model_like(model, additional_fields=None, default_values=None):
    if additional_fields is None:
        additional_fields = {}
    if default_values is None:
        default_values = {}

    fields_ = {}
    post_init_defaults = {}

    if dataclasses.is_dataclass(model):
        fields_.update({f.name: f.type for f in dataclasses.fields(model)})
        for field_ in fields(model):
            if not field_.name in default_values:
                if field_.default is not MISSING:
                    default_values[field_.name] = field_.default
                elif field_.default_factory is not MISSING:
                    default_values[field_.name] = field_.default_factory()

    else:
        type_map = {
            sa.Integer: int,
            sa.String: str,
            sa.Float: float,
            sa.Boolean: bool,
            sa.Date: date,
            sa.DateTime: datetime,
            sa.Text: str,
            sa.Numeric: float,
            sa.LargeBinary: bytes
        }

        for column in sa.inspect(model).columns:
            name = column.name
            if isinstance(column.type, sa.ARRAY):
                inner_type = column.type.item_type
                python_inner_type = type_map.get(type(inner_type), None)

                if python_inner_type is None:
                    raise ValueError(f"Unsupported array inner type: {type(inner_type)}")

                field_type = list[python_inner_type]
                fields_[name] = field_type  # field type, defaults handled in post_init

                if not name in default_values:
                    # If the column has a default value, add it to post_init_defaults
                    if column.default is not None and column.default.is_scalar:
                        post_init_defaults[name] = column.default.arg
                    else:
                        post_init_defaults[name] = []
                    default_values[name] = field(default_factory=list)

            else:
                field_type = type_map.get(type(column.type), None)
                if field_type is None:
                    raise ValueError(f"Unsupported column type: {type(column.type)}")

                fields_[name] = field_type
                
                if not name in default_values:
                    # Handle default values for non-array fields
                    if field_type == int:
                        default_values[name] = 0
                    elif field_type == float:
                        default_values[name] = 0.0
                    elif field_type == bool:
                        default_values[name] = False
                    elif field_type == str or field_type == sa.Text:
                        default_values[name] = ""
                    else:
                        default_values[name] = None

    # Merge additional fields if provided
    for name, field_type in additional_fields.items():
        if type(field_type) == list:
            inner_type = field_type[0]

            fields_[name] = List[inner_type]

            if len(field_type) == 2:
                size = field_type[1]
            else:
                size = 0
            
            if not name in default_values:

                default_values[name] = lambda: []

                if inner_type == int: post_init_defaults[name] = [0] * size
                elif inner_type == float: post_init_defaults[name] = [0.0] * size
                elif inner_type == bool: post_init_defaults[name] = [False] * size
                elif inner_type == str: post_init_defaults[name] = [""] * size
                else: post_init_defaults[name] = [None] * size

        else:
            fields_[name] = field_type
            if not name in default_values:
                if field_type == int: default_values[name] = 0
                elif field_type == float: default_values[name] = 0.0
                elif field_type == bool: default_values[name] = False
                elif field_type == str: default_values[name] = ""
                else: default_values[name] = None         


    original_post_init = getattr(model, '__post_init__', None)

    def combined_post_init(self, *args, **kwargs):
        if original_post_init:
            original_post_init(self, *args, **kwargs)
        for name, default in post_init_defaults.items():
            setattr(self, name, default)

    DataclassModel = dataclass(type(model.__name__, (object,), {
        '__annotations__': fields_,
        '__post_init__': combined_post_init,
        **{k: field(default=v) for k, v in default_values.items()}  # set default values
    }))
    return [], DataclassModel

def run_program(function_name, *args):
    function_name = function_name.replace(".p","").lower().replace("-","_")

    module_name = "functions." + function_name

    # Check if module and function exist
    if importlib.util.find_spec(module_name):
        module = importlib.import_module(module_name)
        if hasattr(module, function_name):
            function_to_call = getattr(module, function_name)
            # Call the function with unpacked arguments
            output_data = function_to_call(*args)
            return output_data
    
    return None

# def buffer_copy(from_buffer, model, except_fields=[]):
#     return model(**{col.name: getattr(from_buffer, col.name) 
#                     for col in sa.inspect(type(from_buffer)).columns 
#                     if col.name not in except_fields})

def buffer_copy(from_buffer, to_buffer, except_fields=[]):
    for col in sa.inspect(type(from_buffer)).columns:
        if col.name not in except_fields:
            setattr(to_buffer, col.name, getattr(from_buffer, col.name))
    return to_buffer


def query(data: List[Type], 
          filters: Callable[[Type], bool] = None, 
          sort_by: Optional[str] = None, 
          descending: bool = False,
          first: bool = False,
          last: bool = False) -> Union[Type, List[Type], None]:
    
    # If only the first or last result is desired without sorting, use next() for efficiency
    if (first or last) and not sort_by:
        if len(data) == 1:
            return data[0]

        data_gen = (item for item in data if (filters and filters(item) or not filters))

        if last:
            data_gen = reversed(list(data_gen))

        return next(data_gen, None)

    # Convert to list for sorting
    data = list(filter(filters, data))
    
    # Apply sorting
    if sort_by:
        data.sort(key=lambda x: getattr(x, sort_by), reverse=descending)
    
    # Return the first or last item after sorting
    if first:
        return data[0] if data else None
    if last:
        return data[-1] if data else None
    
    return data


def indexed_list(table_name,query_results,fields=[]):
    data = []
    for obj in query_results:
        data_line = {}
        data_line[table_name] = obj
        for field in fields:
            data_line[field] = getattr(obj,field)

        data.append(data_line)
    return pd.DataFrame(data)

def get_first_matching_record(obj_name,df, conditions):
    """
    Get the first record from the DataFrame based on multiple filtering conditions.

    :param df: pandas DataFrame to search in
    :param conditions: Dictionary with column names as keys and (operator, value) tuples as values
    :return: The first matching record, or None if no match is found
    """
    # Define a dictionary of available operators
    operators = {
        "==": operator.eq,
        "!=": operator.ne,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge
    }

    # Start with the full DataFrame
    filtered_df = df

    # Apply each condition
    for column, (op, value) in conditions.items():
        func = operators[op]
        filtered_df = filtered_df[func(filtered_df[column], value)]

    if not filtered_df.empty:
        return filtered_df.iloc[0][obj_name]
    else:
        return None
    
def get_first_matching_record_optimized(df, conditions):
    """
    Get the first record from the DataFrame based on multiple filtering conditions.
    This version attempts to find the index of the first match to optimize the process.

    :param df: pandas DataFrame to search in.
    :param conditions: Dictionary with column names as keys and (operator, value) tuples as values.
    :return: The first matching record, or None if no match is found.
    """
    # Define a dictionary of available operators
    operators = {
        "==": operator.eq,
        "!=": operator.ne,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge
    }

    # Combine all conditions
    combined_condition = pd.Series([True] * len(df))
    for column, (op, value) in conditions.items():
        func = operators[op]
        combined_condition &= func(df[column], value)

        # Find the index of the first match
        first_match_index = combined_condition.idxmax()

        # Check if a match was found
        if combined_condition[first_match_index]:
            # Return the row at the first match index
            return df.iloc[first_match_index]
        else:
            # No match found
            return None    
    
def remove_object_from_list(list,remove_obj):
    return [obj for obj in list if obj is not remove_obj]

def convert_yy_to_yyyy(yy):
    if yy >= 80:
        return 1900 + yy
    else:
        return 2000 + yy

def get_output(output_data):
    if output_data == None:
        return None
    elif len(output_data) > 1:
        return tuple(output_data.values())
    else:
        return output_data[next(iter(output_data))]

def substring(input_str:str, start:int, length:int):
    if input_str == "":
        return input_str
    
    return input_str[start: start + length]

def num_entries(input_str, delimiter):
    return len(input_str.split(delimiter))

def entry(entry_num, input_str, delimiter,str_value=""):
    if str_value != "":
        str_list = str.split(delimiter)
        str_list[entry_num] = str_value

        return delimiter.join(str_list)
    
    if input_str.count("/") + 1 == 1:
        return input_str
    else:
        return input_str.rsplit(delimiter,input_str.count("/") + 1)[entry_num]

def camelCase(input_str):
    output = ''.join(x for x in input_str.title() if x.isalnum())
    return output[0].lower() + output[1:]

def to_int(input_str):
    try:
        int_value = int(input_str)
    except (TypeError, ValueError):
        int_value = 0
    return int_value

# def to_string(input_str,format=""):
#     return str(input_str)

from datetime import datetime

def to_string(input_value, format_spec=""):
    if format_spec == "":
        return str(input_value)
    
    if format_spec.startswith("x("):
        # String formatting: x(15) in ABL is like {:15} in Python
        width = int(format_spec[2:-1])
        formatted = f"{input_value:<{width}}"
    elif any(char.isdigit() for char in format_spec) and '.' in format_spec:
        # Numeric formatting with potential right alignment
        decimal_places = format_spec.split('.')[-1]
        num_decimal = len(decimal_places)
        total_width = len(format_spec.split('.')[0])
        if ',' in format_spec:
            formatted = f"{input_value:>{total_width},.{num_decimal}f}"
        else:
            formatted = f"{input_value:>{total_width}.{num_decimal}f}"
    elif '/' in format_spec:
        # Date formatting, assuming '99/99/9999' is month/day/year
        date_format = format_spec.replace('9999', '%Y').replace('99', '%m')
        date_format = date_format.replace('%m/%m', '%m/%d')  # Correcting the format
        if isinstance(input_value, datetime):
            formatted = input_value.strftime(date_format)
        else:
            formatted = input_value  # or handle as error
    else:
        # Default or unrecognized format, return as-is
        formatted = str(input_value)

    return formatted


def sha1_hex(input_str):
    return hashlib.sha1(input_str.encode()).hexdigest()

def sha1(input_str):
    return hashlib.sha1(input_str.encode())

def get_delimited_data(input_str,delimiter,key,has_value):
    list = input_str.split(delimiter)
    for data in list:
        if (data.startswith(key)):
            if has_value:
                return data[len(key):]
            else:
                return True

    if has_value:
        return ""
    else:
        return False
    
def update_key_delimited_data(input_str,delimiter,key,value=""):
    foundFlag = False

    list = input_str.split(delimiter)
    output = ""
    for data in list:
        if data.startswith(key) and not foundFlag:
            output += key + value + ";"
            foundFlag = True
        else:
            output += data + ";"
    
    if not foundFlag:
        output += key + value

    return output

def del_key_delimited_data(input_str,delimiter,key):

    list = input_str.split(delimiter)
    output = ""
    for data in list:
        if not data.startswith(key):
            output += data + ";"

    return output


def get_date_input(input_date):
    if type(input_date) == str:
        year = int(entry(2,input_date,"/"))

        if year < 100:
            input_date = entry(0,input_date,"/") + "/" + entry(1,input_date,"/") + "/" + str(convert_yy_to_yyyy(year))
            
        return datetime.strptime(input_date,'%m/%d/%Y').date()
    else:
        return input_date
    
def get_date_temp_table(input_date):
    if type(input_date) == str:
        return datetime.strptime(input_date,'%Y/%m/%d').date()
    else:
        return input_date

def set_date_temp_table(input_date):
    if input_date == None:
        return None
    return input_date.strftime('%Y/%m/%d')

def get_weekday(input_date):
    weekday = input_date.weekday()
    
    if weekday == 6:
        return 1
    else:
        return weekday + 2
    
def get_day(input_date):
    return input_date.day

def get_month(input_date):
    return input_date.month

def get_year(input_date):
    return input_date.year

def date_mdy(month,day,year):
    return date(year,month,day)

def create_output_date(input_date):
    if input_date == None:
        return None

    return input_date.strftime('%Y-%m-%d')


def get_current_date():
    if(hasattr(local_storage,"timezone")):
        return datetime.now(pytz.timezone(local_storage.timezone)).date()
    else:
        return None

def get_current_time():
    if(hasattr(local_storage,"timezone")):
        return datetime.now(pytz.timezone(local_storage.timezone)).time()
    else:
        return None

def get_current_time_in_seconds():
    if(hasattr(local_storage,"timezone")):
        now = datetime.now(pytz.timezone(local_storage.timezone))
        return now.hour * 3600 + now.minute * 60 + now.second
    else:
        return 0

def time_into_seconds(time:datetime):
    return time.hour * 3600 + time.minute * 60 + time.second

def seconds_into_time(total_seconds,format=""):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    result_time = time(hour=hours, minute=minutes, second=seconds)
    if format == "":
        return result_time
    else:
        return result_time.strftime(format)

def get_index(input_str, substring):
    return input_str.find(substring)

def trim(input_str, char=" "):
    return input_str.strip(char)

def fill(input_str, num_repitition=" "):
    return "".ljust(num_repitition,input_str)

def replace_exact(text, search, replacement):
    # Escape special characters in the search string
    escaped_search = re.escape(search)
    # Construct the pattern to match the whole word
    pattern = r'\b{}\b'.format(escaped_search)
    # Replace using the pattern and the original replacement string
    return re.sub(pattern, replacement, text)


def replace_str(input_str, replace_from, replace_to):
    return input_str.replace(replace_from, replace_to)

def set_search_path(schema):
    from models.base import SessionLocal
    from models import Queasy

    db_session = SessionLocal()
    db_session.execute(sa.text("SET SEARCH_PATH TO '" + schema + "'"))
    local_storage.db_session = db_session

    # TODO: genparam for timezone
    queasy = db_session.query(Queasy).filter(Queasy.key == 999).first()
    if queasy:
        local_storage.timezone = queasy.char1
    else:
        local_storage.timezone = ""


def get_db_url(hotelCode):
    from models.base import get_database_session

    #TODO: db for tenant
    session = get_database_session("postgresql://postgres:password@localhost:5432/tenants")
    # session = get_database_session("postgresql://postgres:VHPLite#2023@localhost:5432/tenants")
    # session = get_database_session("postgresql://vhpadmin:VHPLogin2023@vhp-dev.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com:5432/tenants")

    #TODO: testing only
    if not test_database_connection(session):
        return "postgresql://postgres:password@localhost:5432/vhp_rental"
        # return get_database_session("postgresql://postgres:VHPLite#2023@localhost:5432/vhp_rental")
        # return "postgresql://vhpadmin:VHPLogin2023@/vhp-dev.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com:5432/vhp_rental"
    
    group = session.execute(sa.text("select name from hotelgroup where '" + hotelCode + "' = any(hotelcodes)")).fetchone()
    if group:
        groupname = group[0]
    else:
        groupname = "rental"

    ip,port,db_name,username,enc_pass = session.execute(sa.text("SELECT ip,port,db,username,password from dbaccess where groupname = '" + groupname  + "'")).fetchone()
    session.close()

    return "postgresql://" + username + ":" + decrypt(enc_pass) + "@" + ip + ":" + str(port) + "/" + db_name


def set_db_and_schema(hotelCode):
    from models import Queasy

    db_session = create_db_session(hotelCode)

    db_session.execute(sa.text("SET SEARCH_PATH TO 'shared', '" + hotelCode + "'"))
    local_storage.db_session = db_session
    local_storage.hotelCode = hotelCode
    local_storage.pvILanguage = 1

    # TODO: genparam for timezone
    queasy = db_session.query(Queasy).filter(Queasy.key == 999).first()
    if queasy:
        local_storage.timezone = queasy.char1
    else:
        local_storage.timezone = ""

def set_combo_session(hotelCode,var2=None,var3=None,var4=None):
    db_session = create_db_session(hotelCode)
    if db_session:
        local_storage.combo_db_session = db_session
        return True
    
    return False
        
def resset_combo_session():
    local_storage.combo_db_session = None


def create_db_session(hotelCode):
    from models.base import get_database_session

    db_url = get_db_url(hotelCode)
    db_session = get_database_session(db_url)

    return db_session


    
def test_database_connection(session):
    try:
        session.execute(sa.text("SELECT 1"))
        return True
    except OperationalError:
        return False

#TODO: build library cryptography using Docker amazonlinux
def encrypt(input_str):
    # key = Fernet.generate_key()
    # print(key.decode('utf-8'))
    cipher_suite = Fernet("uBGnw5sWA1Bx6kzsEEQHktdmEEDpjCjvoT9Sbgl28C0=")
    return cipher_suite.encrypt(input_str.encode('utf-8')).decode("utf-8")
    # return str

def decrypt(input_str):
    cipher_suite = Fernet("uBGnw5sWA1Bx6kzsEEQHktdmEEDpjCjvoT9Sbgl28C0=")
    return cipher_suite.decrypt(input_str).decode("utf-8")
    # return str

def replace(input_str:str,from_str,to_str):
    return input_str.replace(from_str,to_str)

def parameter_and_inner_types(func):
    sig = inspect.signature(func)
    param_types = {}

    for name, param in sig.parameters.items():
        annotation = param.annotation
        param_types[name] = annotation
        """        
        # Directly use the annotation if it's a basic type
        if annotation in (int, float, str, bool, date):  # Add any other basic types you want to handle
            # param_types[name] = annotation.__name__
            param_types[name] = annotation
        
        # Check if annotation is a typing generic like List
        elif hasattr(annotation, '__origin__'):
            origin = annotation.__origin__
            if origin in (list, List):  # Can extend for other types like Dict, Tuple, etc.
                inner_type = get_args(annotation)[0]
                param_types[name] = type([{inner_type.__name__}])
            else:
                param_types[name] = type(origin.__name__)
        else:
            param_types[name] = type(annotation.__name__) if inspect.isclass(annotation) else str(annotation)
        """
    return param_types


def convert_to_bool(val):
    if type(val) == bool:
        return val
    elif type(val) == str and val == 'true':
        return True
    else:
        return False

def convert_to_int(val):
    if type(val) == int:
        return val
    elif type(val) == str:
        val = val.strip(" ")
        if val == "":
            return 0
        return int(val)

def upload_file_s3(s3_filename, subfolder, file_content, from_base64=False):
    s3 = boto3.resource('s3')
    object_key = subfolder + "/" + local_storage.hotelCode + '/' + s3_filename

    # with open('path_to_your_local_file.extension', 'rb') as file:
    #     file_content = file.read()

    if from_base64:
        file_content = base64_decode(file_content)

    s3.Object(s3_bucket_name, object_key).put(Body=file_content)

def download_file_s3(s3_filename, to_base64=False):
    s3 = boto3.resource('s3')
    object_key = local_storage.hotelCode + '/' + s3_filename  # Update with the desired "folder" and file name

    content = ""

    try:
        # Attempt to fetch the object
        response = s3.Object(s3_bucket_name, object_key).get()
        content = response['Body'].read()

    except botocore.exceptions.ClientError as e:
        return None
    
    if to_base64:
        return base64_encode(content)
    
    return content
    

def base64_encode(file_content):
    if file_content:
        base64_content = base64.b64encode(file_content)
        return base64_content.decode('utf-8')
    return ""

def base64_decode(base64_string):
    return base64.b64decode(base64_string)

def add_log(str, as_error=False):
    if as_error:
        local_storage.app.logger.error(str)
    else:
        local_storage.app.logger.debug(str)

def recid(obj):
    return obj.recid

def logical(value):
    # Handle the 'unknown' case
    if value is None or value == '?':
        return None
    # Handle the string "false" case-insensitively
    if isinstance(value, str) and value.strip().lower() == 'false':
        return False
    # Use Python's bool() for all other cases
    return bool(value)


def truncate(number, decimals=0):
    if not isinstance(decimals, int):
        raise ValueError("Decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("Decimal places must be zero or more.")
    
    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


def generate_uuid():
    return uuid

def guid(uuid_):
    return uuid_.uuid4()

def proversion():
    return "11.6"

def translateExtended(ipCOriText, ipCContext, ipCDelimiter):
    return ipCOriText
"""
def translateExtended(ipCOriText, ipCContext, ipCDelimiter):

    ipILang = local_storage.pvILanguage

    if not ipILang or ipILang <= 1: 
        return ipCOriText

    db_session = local_storage.db_session
    
    # TODO
    
    # IF ipCDelimiter EQ "":U OR ipCDelimiter EQ ? THEN 
    #         lvINumEntries = 1. 
    #     ELSE 
    #         lvINumEntries = NUM-ENTRIES(ipCOriText, ipCDelimiter). 
    #     IF ipCOriText EQ ? OR ipCOriText EQ "" THEN 
    #         RETURN ipCOriText. 
    #     DO lvIIdx = 1 TO lvINumEntries: 
    #         /* Extract single "Word" TO translate */ 
    #         IF lvINumEntries EQ 1 THEN 
    #             lvCText = ipCOriText. 
    #         ELSE 
    #             lvCText = ENTRY(lvIIdx, ipCOriText, ipCDelimiter). 
    

    lvCText = ipCOriText

    seq_texts = 0
    sourcetext = db_session.query(Sourcetext).order_by(Sourcetext.refcode.desc())

    if sourcetext:
        seq_texts = sourcetext.refcode + 1
    else:
        seq_texts = 1


    sourcetext = db_session.query(Sourcetext).filter(
            (Sourcetext.refcontext == ipCContext) & (Sourcetext.reftext == lvCText)).first()

    if not sourcetext:
        sourcetext = Sourcetext()
        sourcetext.refcode      = seq_texts
        sourcetext.refcontext   = ipCContext 
        sourcetext.reftext      = lvCText 
        sourcetext.flag1        = 0 


    desttext = db_session.query(Desttext).filter(
            (Desttext.refcode == sourcetext.refcode) & Desttext.lang == ipILang)
    

    if not desttext:
        desttext = Desttext()
        desttext.refcode    = sourcetext.refcode 
        desttext.lang       = ipILang
        desttext.dtext      = ""     

    lvCDesttext = desttext.dtext

    if lvCDesttext == "":
            lvCDesttext = lvCText
    
    opCText = opCText + ipCDelimiter + lvCDesttext

    if ipCDelimiter != "":
        return substring(opCText,1) 
    
    return opCText
"""



