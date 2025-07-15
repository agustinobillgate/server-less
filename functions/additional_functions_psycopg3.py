# version = 1.0.0.35

import sqlalchemy as sa
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import aliased, load_only
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression, Cast
from sqlalchemy import not_, func, text, Function, and_
from sqlalchemy.dialects.postgresql import CITEXT
from operator import gt, ge, lt, le, ne, eq
# from models import Sourcetext, Desttext
# from functions.additional_class import ExtendedDate
string = str

import importlib
# import ast
import math,re, random

from dataclasses import field, fields, dataclass, MISSING, is_dataclass

from time import strftime,gmtime
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from typing import List,Dict,Type, Optional, Callable, Union, get_origin
from cryptography.fernet import Fernet

import threading, hashlib,pytz,inspect, os, base64
import boto3, botocore
import uuid
# import pandas as pd
import operator

# import decimal
from decimal import Decimal, DivisionByZero
from typing import TypeVar, Generic, Tuple

T = TypeVar('T')


"""
os.environ['AWS_ROLE_ARN'] = "arn:aws:iam::341938954922:user/christofer"
os.environ['AWS_ACCESS_KEY_ID'] = "AKIAU7HJGMKVE2H37NYU"
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-1'
"""
local_storage = threading.local()
s3_bucket_name = 'elasticbeanstalk-ap-southeast-1-341938954922'

# pd.options.display.min_rows = 100

def initialize_local_storage():
    local_storage.combo_flag = False    
    local_storage.data_cache = {}
    local_storage.simplified_model_list = {}
    local_storage.function_cache = {}

def create_buffer(buffer_name, model):
    return aliased(model, name=buffer_name)

def get_localstorage():
    return local_storage

def get_simplified_model(model):
    return local_storage.simplified_model_list[model]

def prepare_func_cache(function_name):
    if function_name not in local_storage.function_cache:
        local_storage.function_cache[function_name] = {}


def prepare_cache(model_list):
    for model in model_list:
        if model not in local_storage.simplified_model_list.keys():
            # local_storage.data_cache[model] = {}
            # _, Simplfied_model = create_model_like(model)
            # local_storage.simplified_model_list[model] = Simplfied_model()
            local_storage.simplified_model_list[model] = model()

        if model not in local_storage.data_cache.keys():
            local_storage.data_cache[model] = {}
            
def get_cache_value_list(model, field_name):
    return local_storage.data_cache[model]["value_list"][field_name]


def set_cache(model, filters=None, list_of_condition_field_name_list=[], skip_flag=False, variable_field_name_list=[], field_value_list=[]):
    prepare_cache([model])
    db_result = None

    if filters is None:
        db_result = local_storage.db_session.query(model).all()
    else:
        db_result = local_storage.db_session.query(model).filter(filters).all()

    sorted_list_of_condition_field_name_list = []
    for field_name_list in list_of_condition_field_name_list:
        sorted_list_of_condition_field_name_list.append(sorted(field_name_list))

    list_of_condition_field_name_list = sorted_list_of_condition_field_name_list

    local_storage.data_cache[model]["value_list"] = {}
    local_storage.data_cache[model]["value_dict_list"] = {}

    for field_name in field_value_list:
        local_storage.data_cache[model]["value_list"][field_name] = []
        local_storage.data_cache[model]["value_dict_list"][field_name] = {}
        
    
    for data in db_result:
        data_obj = {"data": data}

        for field_name in field_value_list:
            value = getattr(data,field_name)
            if local_storage.data_cache[model]["value_dict_list"][field_name].get(value):
                local_storage.data_cache[model]["value_dict_list"][field_name][value] = ""
                local_storage.data_cache[model]["value_list"][field_name].append(value)

        for field_name_list in list_of_condition_field_name_list:
            filter_obj = {}
    
            for field_name in field_name_list:
                value = getattr(data,field_name)
                filter_obj[field_name] = value


            filter_str = string(filter_obj)

            if filter_str not in local_storage.data_cache[model]:
                local_storage.data_cache[model][filter_str] = []

            if variable_field_name_list != []:
                for field_name in variable_field_name_list:
                    data_obj[field_name] = getattr(data,field_name)
            local_storage.data_cache[model][filter_str].append(data_obj)

    local_storage.data_cache[model]["skip_flag"] = skip_flag

def update_cache(obj, fields=[]):
    model = type(obj)
    condition_dict = {}

    for field_name in sorted(fields):
        condition_dict[field_name] = getattr(obj, field_name)

    condition_str = string(condition_dict)

    if not condition_str in local_storage.data_cache[model]:
        local_storage.data_cache[model][condition_str] = []
        local_storage.data_cache[model][condition_str].append({"data":obj})


def get_cache_st(model, filters, field_names=[]):
    field_names = []
    cache_dict_objs = local_storage.data_cache.get(model)

    other_filters = {}
    for key, value in filters.items():
        if type(value) == tuple:
            other_filters[key] = value
    for key in other_filters:
        filters.pop(key)

    filters_str = string(filters)

    # Check if cache exists and is not empty
    if cache_dict_objs != None and cache_dict_objs != {}:
        query_results = cache_dict_objs.get(filters_str)
        if query_results != None:
            if other_filters == {}:
                return query_results[0]["data"]
            
            for query_result in query_results:
                match = True
                for field, (operator_func, value) in other_filters.items():
                    if not field in query_result or not operator_func(query_result[field], value):
                        match = False
                        break  # Stop checking this record

                if match:
                    return query_result["data"]
            
    if cache_dict_objs != None and cache_dict_objs.get("skip_flag"):
        return None
    

    # If not found in cache, fetch from the database
    # filter_conditions = [getattr(model, field) == value for field, value in filters.items()]
    filter_conditions = []

    for field, (op, value) in other_filters.items():
        if "[" in field and "]" in field:  # Handle indexed fields like "prices[0]"
            base_field, index = field.split("[")
            index = int(index.strip("]")) + 1 # Convert index to int
            column = getattr(model, base_field)[index]  # Extract indexed value
        else:
            column = getattr(model, field)

        if op == le:
            filter_conditions.append(column <= value)
        elif op == lt:
            filter_conditions.append(column < value)
        elif op == ge:
            filter_conditions.append(column >= value)
        elif op == gt:
            filter_conditions.append(column > value)
        elif op == ne:
            filter_conditions.append(column != value)

    for field, value in filters.items():
        if "[" in field and "]" in field:  # Handle indexed fields like "prices[0]"
            base_field, index = field.split("[")
            index = int(index.strip("]")) + 1 # Convert index to int
            column = getattr(model, base_field)[index]  # Extract indexed value
        else:
            column = getattr(model, field)

        filter_conditions.append(column == value)

    if field_names != []:
        columns = [getattr(model, col) for col in field_names if hasattr(model, col)]
        db_result = local_storage.db_session.query(model).options(load_only(*columns)).filter(and_(*filter_conditions)).first()
    else:
        db_result = local_storage.db_session.query(model).filter(and_(*filter_conditions)).first()
    
    if db_result:
        if not model in local_storage.data_cache:
            local_storage.data_cache[model] = {}

        if other_filters == {}:
            local_storage.data_cache[model][filters_str] = [{"data": db_result}]
        else:

            if not filters_str in local_storage.data_cache[model]:
                local_storage.data_cache[model][filters_str] = []

            result_obj = {"data": db_result}
            for field_name in other_filters.keys():
                # local_storage.data_cache[model][filters_str][field_name] = getattr(db_result,field_name)
                result_obj[field_name] = getattr(db_result,field_name)

            local_storage.data_cache[model][filters_str].append(result_obj)

    return db_result


def get_cache(model, input_filters, field_names=[]):
    field_names = []
    cache_dict_objs = local_storage.data_cache.get(model)

    input_filters = dict(sorted(input_filters.items()))
    filters = {}
    other_filters = {}

    for field_name in input_filters:
        for condition in input_filters[field_name]:
            (comparison_operator, value) = condition
            if comparison_operator != eq:
                if not field_name in other_filters:
                    other_filters[field_name] = []
                other_filters[field_name].append(condition)
            else:
                filters[field_name] = value

    filters_str = string(filters)

    # Check if cache exists and is not empty
    if cache_dict_objs != None and cache_dict_objs != {}:
        query_results = cache_dict_objs.get(filters_str)

        if query_results != None:
            if other_filters == {}:
                return query_results[0]["data"]
            
            for query_result in query_results:
                match = True
                for field in other_filters:
                    for condition in other_filters[field]:
                        (operator_func,value) = condition
                        if not field in query_result or not operator_func(query_result[field], value):
                            match = False
                            break  # Stop checking this record

                if match:
                    return query_result["data"]
            
    if cache_dict_objs != None and cache_dict_objs.get("skip_flag"):
        return None
    

    # If not found in cache, fetch from the database
    # filter_conditions = [getattr(model, field) == value for field, value in filters.items()]
    filter_conditions = []

    for field in other_filters:
        for condition in other_filters[field]:
            (op, value) = condition
            if "[" in field and "]" in field:  # Handle indexed fields like "prices[0]"
                base_field, index = field.split("[")
                index = int(index.strip("]")) + 1 # Convert index to int
                column = getattr(model, base_field)[index]  # Extract indexed value
            else:
                column = getattr(model, field) 

            if op == le:
                filter_conditions.append(column <= value)
            elif op == lt:
                filter_conditions.append(column < value)
            elif op == ge:
                filter_conditions.append(column >= value)
            elif op == gt:
                filter_conditions.append(column > value)
            elif op == ne:
                filter_conditions.append(column != value)

    for field,value in filters.items():
        if "[" in field and "]" in field:  # Handle indexed fields like "prices[0]"
            base_field, index = field.split("[")
            index = int(index.strip("]")) + 1 # Convert index to int
            column = getattr(model, base_field)[index]  # Extract indexed value
        else:
            column = getattr(model, field)

        filter_conditions.append(column == value)


    if field_names != []:
        columns = [getattr(model, col) for col in field_names if hasattr(model, col)]
        db_result = local_storage.db_session.query(model).options(load_only(*columns)).filter(and_(*filter_conditions)).first()
    else:
        db_result = local_storage.db_session.query(model).filter(and_(*filter_conditions)).first()
    
    if db_result:
        if not model in local_storage.data_cache:
            local_storage.data_cache[model] = {}

        if other_filters == {}:
            local_storage.data_cache[model][filters_str] = [{"data": db_result}]
        else:

            if not filters_str in local_storage.data_cache[model]:
                local_storage.data_cache[model][filters_str] = []

            result_obj = {"data": db_result}
            for field_name in other_filters.keys():
                # local_storage.data_cache[model][filters_str][field_name] = getattr(db_result,field_name)
                result_obj[field_name] = getattr(db_result,field_name)

            local_storage.data_cache[model][filters_str].append(result_obj)

    return db_result
"""
def get_cache(model, filters, field_names=[]):
    field_names = []
    cache_dict_objs = local_storage.data_cache.get(model)

    filters_str = str(filters)

    # Check if cache exists and is not empty
    if cache_dict_objs != None and cache_dict_objs != {}:
        query_result = cache_dict_objs.get(filters_str)

        if query_result != None:
            return query_result
    
    # if cache_dict_objs != None and cache_dict_objs.get("skipFlag"):
    #     return None

    # If not found in cache, fetch from the database
    filter_conditions = [getattr(model, field) == value for field, value in filters.items()]

    if field_names != []:
        columns = [getattr(model, col) for col in field_names if hasattr(model, col)]
        db_result = local_storage.db_session.query(model).options(load_only(*columns)).filter(and_(*filter_conditions)).first()
    else:
        db_result = local_storage.db_session.query(model).filter(and_(*filter_conditions)).first()
    
    if db_result:
        local_storage.data_cache[model][filters_str] = db_result

    return db_result
"""

def create_model(model_name: string, create_fields: Dict[string, Type], default_values=None):
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
                elif re.match(".*decimal.*",string(inner_type),re.IGNORECASE): post_init_defaults[name] = [Decimal("0")] * size
                elif inner_type == bool: post_init_defaults[name] = [False] * size
                elif inner_type == str: post_init_defaults[name] = [""] * size
                else: post_init_defaults[name] = [None] * size

        else:
            fields[name] = field_type
            if set_default_value:

                if field_type == int: default_values[name] = 0
                elif field_type == float: default_values[name] = 0.0
                elif re.match(".*decimal.*",string(field_type),re.IGNORECASE): default_values[name] = Decimal("0")
                elif field_type == bool: default_values[name] = False
                elif field_type == string: default_values[name] = ""
                else: default_values[name] = None         
        
    return [], dataclass(type(model_name, (object,), {
        '__annotations__': fields,
        '__post_init__': post_init_method,
        **{k: field(default_factory=lambda v=v: v) for k, v in default_values.items()}  # set default values
    }))


# def create_model_like(model, additional_fields=None, default_values=None):
def create_model_like(model, additional_fields=None, default_values=None):
    if additional_fields is None:
        additional_fields = {}
    if default_values is None:
        default_values = {}

    fields_ = {}
    post_init_defaults = {}

    if is_dataclass(model):
        fields_.update({f.name: f.type for f in fields(model)})
        for field_ in fields(model):
            if not field_.name in default_values:
                if field_.default is not MISSING:
                    default_values[field_.name] = field_.default
                elif field_.default_factory is not MISSING:
                    default_values[field_.name] = field_.default_factory()

    else:
        type_map = {
            sa.Integer: int,
            sa.String: string,
            sa.Float: float,
            sa.Boolean: bool,
            sa.Date: date,
            sa.DateTime: datetime,
            sa.Text: string,
            sa.Numeric: float,
            sa.LargeBinary: bytes,
            CITEXT: string
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
                    elif field_type == string or field_type == sa.Text:
                        default_values[name] = ""
                    else:
                        default_values[name] = None

    # Merge additional fields if provided
    for name, field_type in additional_fields.items():
        if type(field_type) == list:
            inner_type = field_type[0]

            fields_[name] = list[inner_type]

            if len(field_type) == 2:
                size = field_type[1]
            else:
                size = 0
            
            if not name in default_values:

                default_values[name] = lambda: []

                if inner_type == int: post_init_defaults[name] = [0] * size
                elif inner_type == float: post_init_defaults[name] = [0.0] * size
                elif inner_type == Decimal: post_init_defaults[name] = [0.0] * size
                elif inner_type == bool: post_init_defaults[name] = [False] * size
                elif inner_type == string: post_init_defaults[name] = [""] * size
                else: post_init_defaults[name] = [None] * size

        else:
            fields_[name] = field_type
            if not name in default_values:
                if field_type == int: default_values[name] = 0
                elif field_type == float: default_values[name] = 0.0
                elif field_type == Decimal: default_values[name] = 0.0
                elif field_type == bool: default_values[name] = False
                elif field_type == string: default_values[name] = ""
                else: default_values[name] = None         


    original_post_init = getattr(model, '__post_init__', None)

    def combined_post_init(self, *args, **kwargs):
        if original_post_init:
            original_post_init(self, *args, **kwargs)
        for name, default in post_init_defaults.items():
            setattr(self, name, default)

    DataclassModel = dataclass(type(model.__name__ + string(random.randint(111111,999999)), (object,), {
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

def buffer_copy(from_buffer, to_buffer, except_fields=[]):
    from models.base import Base

    if from_buffer == None:
        return

    if  isinstance(from_buffer,Base):  
        for col in sa.inspect(type(from_buffer)).columns:
            if col.name not in except_fields:
                setattr(to_buffer, col.name, getattr(from_buffer, col.name))

        if isinstance(to_buffer,Base):
            setattr(to_buffer, "_recid", None)
        
    else:
        if isinstance(to_buffer,Base):
            setattr(from_buffer, "_recid", to_buffer._recid)
        
        for field in [field.name for field in fields(from_buffer)]:
                setattr(to_buffer, field, getattr(from_buffer, field))

    return to_buffer

def query(
          data_list: List[Type], 
          filters: Callable[[Type], bool] = None, 
          sort_by: Optional[List[Tuple[string, bool]]] = None,
          first: bool = False,
          last: bool = False,
          curr_data:Type = None) -> Union[Type, List[Type], None]:

    if not data_list:
        return None if first or last else []

    if (first or last):
        if filters == None:
            if first:
                return data_list[0]
            elif last:
                return data_list[-1]

    # Filtering
    if filters:
        data_list = list(filter(filters, data_list))
        
    if not data_list:
        return None if first or last else []

    # Sorting with multiple fields, corrected approach
    if sort_by:
        for field, descending in reversed(sort_by):
            data_list.sort(key=lambda x: getattr(x, field) is None, reverse=descending)

    # Handling first or last items
    if first:
        return data_list[0] if data_list else None
    if last:
        return data_list[-1] if data_list else None
    
    return data_list


# def indexed_list(query_results,fields=[]):
#     data = []
#     for obj in query_results:
#         data_line = {}
#         data_line["data_object"] = obj
#         for field in fields:
#             data_line[field] = getattr(obj,field)

#         data.append(data_line)
#     return pd.DataFrame(data)
#     # return data

# def get_indexed_record(df, conditions, first=False):
#     """
#     Get the first record from the DataFrame based on multiple filtering conditions.

#     :param df: pandas DataFrame to search in
#     :param conditions: Dictionary with column names as keys and (operator, value) tuples as values
#     :return: The first matching record, or None if no match is found
#     """
#     # Define a dictionary of available operators
#     operators = {
#         "==": operator.eq,
#         "!=": operator.ne,
#         "<": operator.lt,
#         "<=": operator.le,
#         ">": operator.gt,
#         ">=": operator.ge
#     }

#     # Start with the full DataFrame
#     filtered_df = df

#     # Apply each condition
#     for column, (op, value) in conditions.items():
#         func = operators[op]
#         filtered_df = filtered_df[func(filtered_df[column], value)]

#     if not filtered_df.empty:
#         if first:
#             return filtered_df.iloc[0]['data_object']
#         else:
#             return filtered_df['data_object']
#     else:
#         return None
    
# def get_first_matching_record_optimized(df, conditions):
#     """
#     Get the first record from the DataFrame based on multiple filtering conditions.
#     This version attempts to find the index of the first match to optimize the process.

#     :param df: pandas DataFrame to search in.
#     :param conditions: Dictionary with column names as keys and (operator, value) tuples as values.
#     :return: The first matching record, or None if no match is found.
#     """
#     # Define a dictionary of available operators
#     operators = {
#         "==": operator.eq,
#         "!=": operator.ne,
#         "<": operator.lt,
#         "<=": operator.le,
#         ">": operator.gt,
#         ">=": operator.ge
#     }

#     # Combine all conditions
#     combined_condition = pd.Series([True] * len(df))
#     for column, (op, value) in conditions.items():
#         func = operators[op]
#         combined_condition &= func(df[column], value)

#         # Find the index of the first match
#         first_match_index = combined_condition.idxmax()

#         # Check if a match was found
#         if combined_condition[first_match_index]:
#             # Return the row at the first match index
#             return df.iloc[first_match_index]
#         else:
#             # No match found
#             return None    
    
def remove_object_from_list(list,remove_obj):
    return [obj for obj in list if obj is not remove_obj]

def date_range(start_date, end_date):

    desc = False

    if start_date > end_date:
        desc = True

    res_date = start_date

    if not desc:
        while res_date <= end_date:
            yield res_date
            res_date += timedelta(days=1)
    else:
        while res_date >= end_date:
            yield res_date
            res_date -= timedelta(days=1)

def convert_yy_to_yyyy(yy):
    if yy >= 80:
        return 1900 + yy
    else:
        return 2000 + yy
    
def add_output_table(table_name, output_data):
    updated_data = {}
    updated_data[camelCase(table_name)] = {table_name: output_data}
    return updated_data

def get_output(output_data):
    if output_data == None or output_data == {}:
        return {}
    elif len(output_data) > 1:
        return tuple(output_data.values())
    else:
        return output_data[next(iter(output_data))]

def replace_substring(input_str:string, start:int, length:int, replace_str:string):
    return substring(input_str,0,start - 1) +  replace_str +  substring(input_str, start + length - 1,len(input_str)) 

def substring(input_str, start:int, length:int = None):
    if isinstance(input_str, string):
        if input_str == "":
            return input_str
        
        if length == None:
            return input_str[start:]
        
        return input_str[start: start + length]
    elif is_sqlalchemy_data(input_str):
        output_str = func.substr(input_str,start + 1, length)

        if output_str is None:
            output_str = ""

        return output_str


def overlay(original_string, start_pos, overlay_string):
    # Adjusting start_pos to be zero-indexed in Python
    start_pos -= 1

    # If the original string is shorter than the start position, pad with spaces
    if len(original_string) < start_pos:
        original_string = original_string.ljust(start_pos)
    
    return original_string[:start_pos] + overlay_string + original_string[start_pos + len(overlay_string):]


def num_entries(input_str, delimiter=","):
    if type(input_str) == string:
        return len(input_str.split(delimiter))
    else:
        return func.length(input_str) - func.length(func.replace(input_str, delimiter, ""))

def entry(entry_num, input_str, delimiter,str_value=""):
    if is_sqlalchemy_data(input_str):
        extracted_value = func.split_part(input_str, delimiter, entry_num + 1)
        return extracted_value

    elif str_value != "":
        str_list = input_str.split(delimiter)
        str_list[entry_num] = str_value

        return delimiter.join(str_list)
    
    if input_str.count(delimiter) + 1 == 1:
        return input_str
    else:
        if entry_num < num_entries(input_str,delimiter):
            return input_str.split(delimiter)[entry_num]
        else:
            return None
        
def camelCase(input_str):
    output = ''
    was_digit = False
    capitalize_next = False  # Track if the next character should be capitalized
    
    for char in input_str:
        if char == '_' or char == '-':  # Underscore signals a new word
            capitalize_next = True
            was_digit = False
        elif char.isdigit():
            output += char
            was_digit = True
            capitalize_next = False
        elif char.isalpha():
            if was_digit:
                output += char.lower()  # Lowercase if following a digit
                # output += char.upper()  # Capitalize if following a digit
            elif capitalize_next:
                output += char.upper()  # Capitalize if after an underscore
            else:
                output += char.lower()  # Default to lowercase
            was_digit = False
            capitalize_next = False
    return output[0].lower() + output[1:] if output else output

# def camelCase(input_str):
#     output = ''.join(x for x in input_str.title() if x.isalnum())
#     return output[0].lower() + output[1:]

def to_decimal(input_value):
    if type(input_value) == string:
        input_value = input_value.replace(",","").strip(" ")

    if input_value == "":
        return 0
    
    if input_value == None or input_value == "?":
        return None

    if is_sqlalchemy_data(input_value):
        return sa.cast(input_value, sa.Numeric)
    
    return Decimal(input_value)

def to_int(input_str):
    try:
        if is_sqlalchemy_data(input_str):    
            return sa.cast(sa.case((input_str == "", "0"), else_=input_str), sa.Integer)
        if input_str == None:
            return None

        int_value = int(input_str)
    except (TypeError, ValueError):
        int_value = 0

    return int_value


def to_string(input_value, format_spec=""):
    if is_sqlalchemy_data(input_value):    
        return sa.cast(input_value, sa.String)

    if format_spec == "":
        if type(input_value) == date:

            #TODO: 2 digits for month and day

            # date_str = str(get_month(input_value)) + "/" + str(get_day(input_value)) + "/" + str(get_year(input_value))[2:]

            # return date_str
            date_format = "%m/%d/%y"
            formatted = input_value.strftime(date_format)
            return formatted
        
        return string(input_value)

    clean_format_spec = format_spec.strip(" ")

    if clean_format_spec.startswith("x("):
        # String formatting: x(15) in ABL is like {:15} in Python
        width = int(clean_format_spec[2:-1])
        formatted = f"{input_value:<{width}}"
    elif any(char.isdigit() for char in format_spec) and '.' in clean_format_spec:
        # Numeric formatting with potential right alignment
        decimal_places = clean_format_spec.split('.')[-1]
        num_decimal = len(decimal_places)
        total_width = len(clean_format_spec.split('.')[0])
        if ',' in format_spec:
            formatted = f"{input_value:>{total_width},.{num_decimal}f}"
        else:
            formatted = f"{input_value:>{total_width}.{num_decimal}f}"
    elif type(input_value) == bool:
        if input_value:
            formatted = clean_format_spec.split("/")[0]
        else:
            formatted = clean_format_spec.split("/")[1]
    elif '/' in clean_format_spec:
        # Date formatting, assuming '99/99/9999' is month/day/year
        date_format = clean_format_spec.replace("99/99/9999","%m/%d/%Y")
        date_format = date_format.replace("99/99/99","%m/%d/%y")
        # date_format = date_format.replace('9999', '%Y').replace('99', '%m')
        # date_format = date_format.replace('%m/%m', '%m/%d')  # Correcting the format
        if isinstance(input_value, datetime) or isinstance(input_value, date):
            formatted = input_value.strftime(date_format)
        else:
            formatted = input_value  # or handle as error
    elif type(input_value) == int and re.match(".*[HMS].*",format_spec,re.IGNORECASE):
        clean_format_spec = clean_format_spec.replace("HH","H").replace("MM","M").replace("SS","S")
        clean_format_spec = clean_format_spec.replace("H","%H").replace("M","%M").replace("S","%S")
        formatted = strftime(clean_format_spec, gmtime(input_value))
    else:
        # Default or unrecognized format, return as-is
        formatted = string(input_value)

    if " " in format_spec:
        formatted = format_spec.replace(format_spec.strip(" "),formatted)

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
    if type(input_date) == string:
        input_date = input_date.replace("-","/").replace("?","").split("T")[0]
        if input_date == "":
            return None

        if re.match("..../../..",input_date):
            return datetime.strptime(input_date,'%Y/%m/%d').date()

        year = int(entry(2,input_date,"/"))

        if year < 100:
            input_date = entry(0,input_date,"/") + "/" + entry(1,input_date,"/") + "/" + string(convert_yy_to_yyyy(year))
            
        return datetime.strptime(input_date,'%m/%d/%Y').date()
    else:
        return input_date
    
def get_date_temp_table(input_date):
    if type(input_date) == string:
        input_date = input_date.strip(" ").replace("?","")
        if input_date == "":
            return None
        input_date = input_date.replace("-","/")

        year_str = input_date.split("/")[0]
        if len(year_str) == 2:
            year_str = convert_yy_to_yyyy(to_int(year_str))
            input_date = to_string(year_str,"9999") + "/" + "/".join(input_date.split("/")[1:])

        return datetime.strptime(input_date,'%Y/%m/%d').date()
    else:
        return input_date

def set_date_temp_table(input_date):
    if input_date == None:
        return None
    # return input_date.strftime('%Y/%m/%d')
    return input_date.strftime('%Y-%m-%d')

def add_interval(start_date, interval_value, interval_unit):
    interval_unit = interval_unit.rstrip("s")
    interval_unit += "s"
    if interval_unit in ['days', 'weeks', 'hours', 'minutes', 'seconds']:
        # For intervals that timedelta can handle directly
        kwargs = {interval_unit: interval_value}
        return start_date + timedelta(**kwargs)
    elif interval_unit == 'months':
        # Handling months separately as they are not consistent in length
        return start_date + relativedelta(months=interval_value)
    elif interval_unit == 'years':
        # Handling years
        return start_date + relativedelta(years=interval_value)
    else:
        raise ValueError("Unsupported interval unit")
    
def get_interval(start_date, end_date, interval_unit):
    delta = start_date - end_date
    interval = None
    if interval_unit == "weeks":
        interval = delta / timedelta(weeks=1)
    elif interval_unit == "days":
        interval = delta / timedelta(days=1)
    elif interval_unit == "hours":
        interval = delta / timedelta(hours=1)
    elif interval_unit == "minutes":
        interval = delta / timedelta(minutes=1)
    elif interval_unit == "seconds":
        interval = delta / timedelta(seconds=1)
    elif interval_unit == "microseconds":
        interval = delta / timedelta(microseconds=1)
    elif interval_unit == "milliseconds":
        interval = delta / timedelta(milliseconds=1)
    else:
        return None

    return int(interval)

def create_empty_list(size,value):
    return  [value for x in range(size)]

def get_weekday(input_date):
    weekday = input_date.weekday()
    
    if weekday == 6:
        return 1
    else:
        return weekday + 2
    
def get_day(input_date):
    if isinstance(input_date, datetime) or isinstance(input_date, date):
        return input_date.day
    elif is_sqlalchemy_data(input_date):
        return func.extract('day', input_date)

def get_month(input_date):
    if isinstance(input_date, datetime) or isinstance(input_date, date):
        return input_date.month
    elif is_sqlalchemy_data(input_date):
        return func.extract('month', input_date)

def get_year(input_date):
    if isinstance(input_date, datetime) or isinstance(input_date, date):
        return input_date.year
    elif is_sqlalchemy_data(input_date):
        return func.extract('year', input_date)

def date_mdy(*args):
    day = 0
    month = 0
    year = 0

    # input string dd/mm/yyyyy
    if len(args) == 1 and isinstance(args[0], string):
        input_str = args[0]        


        if input_str.strip(" ") == "":
            return None

        date_str = input_str.split("/")
        
        day = to_int(date_str[0])
        month = to_int(date_str[1])
        year = to_int(date_str[2])

    #input integer m,d,y
    elif len(args) == 3 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[0], int):
        month = args[0]
        day = args[1]
        year = args[2]

    if year < 100:
        year = convert_yy_to_yyyy(year)

    if month >= 1 and month <= 12 and day >= 1 and day <= 31:
        return date(year,month,day)

    return None

"""
def date_mdy(input_str:str):
    date_str = input_str.split("/")
    day = to_int(date_str[0])
    month = to_int(date_str[1])
    year = to_int(date_str[2])

    if year < 100:
        year = convert_yy_to_yyyy(year)

    return date(year,month,day)

def date_mdy(month:int,day:int, year:int):
    return date(year,month,day)
"""

def session_date_format():
    return "mdy"

#TODO
def to_datetime(input_value):
    return None

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
    
def get_current_datetime():
    if(hasattr(local_storage,"timezone")):
        return datetime.now(pytz.timezone(local_storage.timezone))
    else:
        return None
    
def get_datetime_from_isoformat(datetime_str):
    return datetime.fromisoformat(datetime_str.replace("_","-"))


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

def inc_value(value):
    return value + 1

def get_index(input_data, substring):
    if is_sqlalchemy_data(input_data):
        return func.position(sa.literal(substring).op("IN")(input_data))

    return input_data.find(substring) + 1

def length(input_data):
    if is_sqlalchemy_data(input_data):
        return func.length(input_data)
    return len(input_data)

def trim(input_str, char=" "):
    if is_sqlalchemy_data(input_str):
        return func.trim(char, input_str)

    return input_str.strip(char)

def left_trim(input_str, char=" "):
    return input_str.lstrip(char)

def right_trim(input_str, char=" "):
    return input_str.rstrip(char)

def fill(input_str, num_repitition=" "):
    return "".ljust(num_repitition,input_str)

def replace_exact(text, search, replacement):
    # Escape special characters in the search string
    escaped_search = re.escape(search)
    # Construct the pattern to match the whole word
    pattern = r'\b{}\b'.format(escaped_search)
    # Replace using the pattern and the original replacement string
    return re.sub(pattern, replacement, text)

def is_sqlalchemy_data(input_data):
    return (isinstance(input_data, InstrumentedAttribute) or 
            isinstance(input_data, BinaryExpression) or 
            isinstance(input_data, Cast) or 
            isinstance(input_data, Function))
    

def matches(input_str, pattern):
    if is_sqlalchemy_data(input_str):
        return input_str.ilike(pattern.replace("\\","\\\\").replace("_","\\_").replace("%","\\%").replace("~*",r"{asterisk}").replace("~.",r"{dot}").replace("~~",r"{tilde}").replace("*","%").replace(".","_").replace(r"{asterisk}","*").replace(r"{dot}", ".").replace(r"{tilde}", "~"), escape="\\")
    
    return re.match(pattern.replace("\\","\\\\").replace("[","\[").replace("]","\]").replace("(","\(").replace(")","\)").replace("-","\-").replace("$","\$").replace("^","\^").replace("~*",r"{asterisk}").replace("~.",r"{dot}").replace("~~",r"{tilde}").replace("*",".*").replace(r"{asterisk}","\*").replace(r"{dot}", "\.").replace(r"{tilde}", "~"), input_str,re.IGNORECASE)


def replace_str(input_str, replace_from, replace_to):
    return input_str.replace(replace_from, replace_to)

def set_search_path(schema):
    from models.base import SessionLocal
    from models import Htparam

    db_session = SessionLocal()
    db_session.execute(sa.text("SET SEARCH_PATH TO '" + schema + "'"))
    local_storage.db_session = db_session

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 91).first()

    if htparam:
        local_storage.timezone = htparam.fchar
    else:
        local_storage.timezone = ""


def get_db_url(hotelCode):
    from models.base import get_database_session

    # #TODO: db for tenant
    # session = get_database_session("postgresql://postgres:password@localhost:5432/tenants")
    # # session = get_database_session("postgresql://postgres:VHPLite#2023@localhost:5432/tenants")
    # # session = get_database_session("postgresql://vhpadmin:VHPLogin2023@vhp-dev.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com:5432/tenants")
    # print("get DB URL")
    # TODO: db for tenant
    # DB_HOST = "vhp-devtest.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com"
    # DB_NAME = "vhpdb"
    # DB_USER = "vhpadmin"
    # DB_PASSWORD = "bFdq8QsQoxH1vAvO"
    # DB_PORT     = 5432

    # DB_HOST = "vhp-qctest.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com"
    # DB_NAME = "vhpdb"
    # DB_USER = "postgres"
    # DB_PASSWORD = "bFdq8QsQoxH1vAvO"
    # DB_PORT     = 5432

    DB_HOST = "psql.staging.e1-vhp.com"
    DB_NAME = "qctest"
    DB_USER = "postgres"
    DB_PASSWORD = "DevPostgreSQL#2024"
    DB_PORT     = 5432

    # print("Enc:", encrypt("superlite#rds"))

   
    # session = get_database_session("postgresql://vhpadmin:VHPLogin2023@vhp-dev.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com:5432/tenants")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?application_name=aws_lambda_serverless"
    session = get_database_session(DATABASE_URL)
    #TODO: testing only
    if not test_database_connection(session):
        return "postgresql://postgres:password@localhost:5432/vhp_rental"
        # return get_database_session("postgresql://postgres:VHPLite#2023@localhost:5432/vhp_rental")
        # return "postgresql://vhpadmin:VHPLogin2023@/vhp-dev.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com:5432/vhp_rental"
    
    group = session.execute(sa.text("select name from public.hotelgroup where '" + hotelCode + "' = any(hotelcodes)")).fetchone()
    print("group:", DB_HOST, DB_NAME, group)
    if group:
        groupname = group[0]
    else:
        groupname = "rental"
        
    try:
        ip,port,db_name,username,enc_pass = session.execute(sa.text("SELECT ip,port,db,username,password from dbaccess where groupname = '" + groupname  + "'")).fetchone()
    except TypeError:
        print(groupname)
        return ""        
    session.close()
    
    print(f"Masuk EC2:{db_name}")
    # return "postgresql://" + username + ":" + decrypt(enc_pass) + "@" + ip + ":" + str(port) + "/" + db_name

    return "postgresql+psycopg://" + username + ":" + enc_pass + "@" + ip + ":" + str(port) + "/" + db_name
    # return "postgresql://postgres:shadow2010@localhost:5432/qctest"


def set_db_and_schema(hotelCode):
    from models import Htparam

    local_storage.db_session = None
    local_storage.hotelCode = ""
    local_storage.pvILanguage = 1
    local_storage.timezone = ""

    
    db_session = create_db_session(hotelCode)

    if db_session:
        results = db_session.execute(text("SELECT schema_name FROM information_schema.schemata"))

        if hotelCode in [result[0] for result in results]:

            db_session.execute(sa.text("SET SEARCH_PATH TO 'shared', '" + hotelCode + "'"))
            
            local_storage.db_session = db_session
            local_storage.hotelCode = hotelCode
            local_storage.pvILanguage = 1

            htparam = db_session.query(Htparam).filter(Htparam.paramnr == 91).first()
            if htparam:
                local_storage.timezone = htparam.fchar
            else:
                local_storage.timezone = ""

def run_program(function_name:string, input_data=()):
    if re.match(".*\.(p|r)",function_name):
        function_name.replace(".p","").replace(".r","").replace("_","__").replace("-","__").lower()
    function_name = function_name.replace(".py","")
    module_name = "functions." + function_name
    module = importlib.import_module(module_name)

    obj = getattr(module, function_name)
    return  obj(*input_data)

def set_combo_session(hotelCode,var2=None,var3=None,var4=None):
    db_session = create_db_session(hotelCode)
    if db_session:
        local_storage.combo_db_session = db_session
        return True
    
    return False
        
def reset_combo_session():
    local_storage.combo_db_session = None
    return True


def create_db_session(hotelCode):
    from models.base import get_database_session

    db_url = get_db_url(hotelCode)
    if db_url == "":
        return None
    
    db_session = get_database_session(db_url)

    return db_session


    
def test_database_connection(session):
    try:
        session.execute(sa.text("SELECT 1"))
        return True
    except OperationalError:
        return False

def message_digest(hash_method, input_str, salt=""):
    if hash_method == "sha-256":
        return hashlib.sha256(input_str.encode())


def create_cipher_suite(key):
    return Fernet(base64_encode(key))

def encrypt_with_cipher_suite(input_str, cipher_suite:Fernet):
    return cipher_suite.encrypt(input_str.encode('utf-8'))

def decrypt_with_cipher_suite(input_str, cipher_suite:Fernet):
    return cipher_suite.decrypt(input_str).decode("utf-8")

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

def replace(input_str:string,from_str,to_str):
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
    elif type(val) == string and val == 'true':
        return True
    else:
        return False
    
def convert_to_bytes(val):
    if type(val) == string:
        return base64_decode(val)
    
    return None

def convert_to_int(val):
    if type(val) == int:
        return val
    elif type(val) == string:
        val = val.strip(" ")
        if val == "":
            return 0
        elif val == "?":
            return None
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

def add_log(log_str, as_error=False):
    if as_error:
        local_storage.app.logger.error(log_str)
    else:
        local_storage.app.logger.debug(log_str)

def recid(obj):
    return obj._recid

def logical(value):
    # Handle the 'unknown' case
    if value is None or value == '?':
        return None
    # Handle the string "false" case-insensitively
    if isinstance(value, string) and value.strip().lower() == 'false':
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

def round_it(round_method:int,round_betrag:Decimal,rate:Decimal):
    rate1 = 0
    rate_str:string = ""
    rate_str1:string = ""
    rate_str2:string = ""
    length_round:int = 0

    if round_method == 1:
        rate = rate + round_betrag * 0.5 - 1

    elif round_method == 2:
        rate = rate - round_betrag * 0.5
    length_round = len(to_string(round_betrag / 2))
    rate_str = to_string(rate)
    rate_str1 = substring(rate_str, 0, len(rate_str) - length_round)
    rate_str1 = rate_str1 + fill("0", length_round)
    rate_str2 = substring(rate_str, len(rate_str) - length_round + 1 - 1)
    rate1 = Decimal(rate_str1)

    if Decimal(rate_str2) >= (round_betrag * 1.5):
        rate1 = rate1 + round_betrag * 2

    elif Decimal(rate_str2) >= (round_betrag * 0.5):
        rate1 = rate1 + round_betrag

    return rate1

def print_beautify(obj):
    if not isinstance(obj, list):
        obj = [obj]

def close_session():
    db_session = local_storage.db_session
    db_session.close()
    engine = db_session.bind
    engine.dispose()    

def asc(input_char):
    try:
        return ord(input_char)
    finally:
        return -1

def chr_unicode(input_char):
    output_char = chr(input_char)
    if output_char == "\x00":
        output_char = ""

    return output_char

#TODO
def translateExtended(ipCOriText, ipCContext, ipCDelimiter):
    return ipCOriText
