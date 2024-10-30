from functions.additional_functions import *
import decimal
from functions.mapping_coa_1bl import mapping_coa_1bl
from functions.mapping_coa_2bl import mapping_coa_2bl
from functions.mapping_coa_3bl import mapping_coa_3bl
from functions.mapping_coa_4bl import mapping_coa_4bl

coa_list_list, Coa_list = create_model("Coa_list", {"old_fibu":str, "new_fibu":str, "bezeich":str, "coastat":int, "old_main":int, "new_main":int, "bezeichm":str, "old_dept":int, "new_dept":int, "bezeichd":str, "catno":int, "acct":int, "old_acct":int}, {"coastat": -1})

def mapping_coa_webbl(coa_list_list:[Coa_list]):


    coa_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal coa_list

        return {}


    get_output(mapping_coa_1bl(coa_list_list))
    get_output(mapping_coa_2bl(coa_list_list))
    get_output(mapping_coa_3bl(coa_list_list))
    get_output(mapping_coa_4bl(coa_list_list))

    return generate_output()