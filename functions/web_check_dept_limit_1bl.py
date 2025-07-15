#using conversion tools version: 1.0.0.45

from functions.additional_functions import *
import decimal
from functions.check_userkeybl import check_userkeybl
from models import Htparam, Hoteldpt, Paramtext

def web_check_dept_limit_1bl(input_username:str, input_userkey:str):
    output_ok_flag = False
    dept_limit = 0
    curr_anz = 0
    epoch_signature = 0
    signature_list_list = []
    htparam = hoteldpt = paramtext = None

    value_list = signature_list = None

    value_list_list, Value_list = create_model("Value_list", {"var_name":str, "value_str":str})
    signature_list_list, Signature_list = create_model("Signature_list", {"var_name":str, "signature":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_ok_flag, dept_limit, curr_anz, epoch_signature, signature_list_list, htparam, hoteldpt, paramtext
        nonlocal input_username, input_userkey


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list

        return {"output_ok_flag": output_ok_flag, "dept_limit": dept_limit, "curr_anz": curr_anz, "epoch_signature": epoch_signature, "signature-list": signature_list_list}

    def check_dept_limit():

        nonlocal output_ok_flag, dept_limit, curr_anz, epoch_signature, signature_list_list, htparam, hoteldpt, paramtext
        nonlocal input_username, input_userkey


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 989)).first()

        if htparam.finteger > 0:
            dept_limit = htparam.finteger
        curr_anz = -1

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            curr_anz = curr_anz + 1
        create_output()


    def create_output():

        nonlocal output_ok_flag, dept_limit, curr_anz, epoch_signature, signature_list_list, htparam, hoteldpt, paramtext
        nonlocal input_username, input_userkey


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list


        value_list = Value_list()
        value_list_list.append(value_list)

        value_list.var_name = "deptLimit"
        value_list.value_str = to_string(dept_limit)


        epoch_signature, signature_list_list = create_signature(input_username, value_list_list)


    def create_signature(user_name:str, value_list_list:[Value_list]):

        nonlocal output_ok_flag, dept_limit, curr_anz, epoch_signature, signature_list_list, htparam, hoteldpt, paramtext
        nonlocal input_username, input_userkey


        nonlocal value_list, signature_list
        nonlocal signature_list_list

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:str = ""
        data:str = ""
        value_str:str = ""

        def generate_inner_output():
            return (epoch, signature_list)


        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 243)).first()

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_list):
            value_str = value_list.value_str.lower()
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_list.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:str):

        nonlocal output_ok_flag, dept_limit, curr_anz, epoch_signature, signature_list_list, htparam, hoteldpt, paramtext
        nonlocal input_username, input_userkey


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list

        out_str = ""
        s:str = ""
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


    output_ok_flag = get_output(check_userkeybl(input_username, input_userkey))

    if not output_ok_flag:

        return generate_output()


    check_dept_limit()

    return generate_output()