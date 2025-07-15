#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Paramtext, Htparam

def prepare_qrcode_generatorbl():

    prepare_cache ([Hoteldpt, Paramtext])

    licensenr = 0
    license_cashless = False
    t_dept_data = []
    hoteldpt = paramtext = htparam = None

    t_dept = None

    t_dept_data, T_dept = create_model("T_dept", {"nr":int, "dept":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal licensenr, license_cashless, t_dept_data, hoteldpt, paramtext, htparam


        nonlocal t_dept
        nonlocal t_dept_data

        return {"licensenr": licensenr, "license_cashless": license_cashless, "t-dept": t_dept_data}

    def decode_string(in_str:string):

        nonlocal licensenr, license_cashless, t_dept_data, hoteldpt, paramtext, htparam


        nonlocal t_dept
        nonlocal t_dept_data

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


    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_dept = T_dept()
        t_dept_data.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1022) & (Htparam.bezeichnung != ("not used").lower()) & (Htparam.flogical)).first()

    if htparam:
        license_cashless = True

    return generate_output()