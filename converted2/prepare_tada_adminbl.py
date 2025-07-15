#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Hoteldpt, Queasy

def prepare_tada_adminbl():

    prepare_cache ([Paramtext, Hoteldpt, Queasy])

    t_param_data = []
    t_dept_data = []
    licensenr = 0
    paramtext = hoteldpt = queasy = None

    t_param = t_dept = None

    t_param_data, T_param = create_model("T_param", {"dept":int, "grup":int, "number":int, "bezeich":string, "typ":int, "logv":bool, "val":string})
    t_dept_data, T_dept = create_model("T_dept", {"nr":int, "dept":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_param_data, t_dept_data, licensenr, paramtext, hoteldpt, queasy


        nonlocal t_param, t_dept
        nonlocal t_param_data, t_dept_data

        return {"t-param": t_param_data, "t-dept": t_dept_data, "licensenr": licensenr}

    def decode_string1(in_str:string):

        nonlocal t_param_data, t_dept_data, licensenr, paramtext, hoteldpt, queasy


        nonlocal t_param, t_dept
        nonlocal t_param_data, t_dept_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal t_param_data, t_dept_data, licensenr, paramtext, hoteldpt, queasy


        nonlocal t_param, t_dept
        nonlocal t_param_data, t_dept_data

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

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_dept = T_dept()
        t_dept_data.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()


    t_param_data.clear()

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)],"number2": [(eq, 1)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 1
        queasy.char1 = "Username"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)],"number2": [(eq, 2)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 2
        queasy.char1 = "Password"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)],"number2": [(eq, 3)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 3
        queasy.char1 = "Interval Refresh Time"
        queasy.number3 = 1
        queasy.char2 = ""
        queasy.betriebsnr = 1

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1) & (Queasy.betriebsnr == 1)).order_by(Queasy.number2).all():
        t_param = T_param()
        t_param_data.append(t_param)

        t_param.dept = queasy.betriebsnr
        t_param.grup = queasy.number1
        t_param.number = queasy.number2
        t_param.bezeich = queasy.char1
        t_param.typ = queasy.number3

        if queasy.number3 == 1:
            t_param.val = to_string(queasy.char2)

        elif queasy.number3 == 2:
            t_param.val = to_string(queasy.deci1)

        elif queasy.number3 == 3:
            t_param.val = to_string(queasy.date1)

        elif queasy.number3 == 4:
            t_param.val = to_string(queasy.logi1)
            t_param.logv = queasy.logi1

        elif queasy.number3 == 5:
            t_param.val = to_string(queasy.char2)

    return generate_output()