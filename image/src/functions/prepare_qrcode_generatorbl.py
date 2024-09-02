from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Hoteldpt, Paramtext, Htparam

def prepare_qrcode_generatorbl():
    licensenr = 0
    license_cashless = False
    t_dept_list = []
    hoteldpt = paramtext = htparam = None

    t_dept = None

    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal licensenr, license_cashless, t_dept_list, hoteldpt, paramtext, htparam


        nonlocal t_dept
        nonlocal t_dept_list
        return {"licensenr": licensenr, "license_cashless": license_cashless, "t-dept": t_dept_list}

    def decode_string(in_str:str):

        nonlocal licensenr, license_cashless, t_dept_list, hoteldpt, paramtext, htparam


        nonlocal t_dept
        nonlocal t_dept_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(ptexte)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1022) &  (func.lower(Htparam.bezeich) != "not used") &  (Htparam.flogical)).first()

    if htparam:
        license_cashless = True

    return generate_output()