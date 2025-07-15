#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Hoteldpt, Paramtext

def check_dept_limit_1bl():

    prepare_cache ([Htparam, Paramtext])

    dept_limit = 0
    curr_anz = 0
    epoch_signature = 0
    signature_list_data = []
    htparam = hoteldpt = paramtext = None

    value_list = signature_list = None

    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_limit, curr_anz, epoch_signature, signature_list_data, htparam, hoteldpt, paramtext


        nonlocal value_list, signature_list
        nonlocal value_list_data, signature_list_data

        return {"dept_limit": dept_limit, "curr_anz": curr_anz, "epoch_signature": epoch_signature, "signature-list": signature_list_data}

    def check_dept_limit():

        nonlocal dept_limit, curr_anz, epoch_signature, signature_list_data, htparam, hoteldpt, paramtext


        nonlocal value_list, signature_list
        nonlocal value_list_data, signature_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 989)]})

        if htparam.finteger > 0:
            dept_limit = htparam.finteger
        curr_anz = -1

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            curr_anz = curr_anz + 1
        create_output()


    def create_output():

        nonlocal dept_limit, curr_anz, epoch_signature, signature_list_data, htparam, hoteldpt, paramtext


        nonlocal value_list, signature_list
        nonlocal value_list_data, signature_list_data


        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "deptLimit"
        value_list.value_str = to_string(dept_limit)


        epoch_signature, signature_list_data = create_signature(input_username, value_list_data)


    def create_signature(user_name:string, value_list_data:[Value_list]):

        nonlocal dept_limit, curr_anz, epoch_signature, signature_list_data, htparam, hoteldpt, paramtext


        nonlocal value_list, signature_list
        nonlocal signature_list_data

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:string = ""
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_data)


        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_data):
            value_str = value_list.value_str.lower()
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_data.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal dept_limit, curr_anz, epoch_signature, signature_list_data, htparam, hoteldpt, paramtext


        nonlocal value_list, signature_list
        nonlocal value_list_data, signature_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    check_dept_limit()

    return generate_output()