#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.selforder_addhtp5bl import selforder_addhtp5bl
from models import Paramtext, Hoteldpt, Queasy

def prepare_selforder_adminbl():

    prepare_cache ([Paramtext, Hoteldpt, Queasy])

    t_param_list = []
    t_dept_list = []
    licensenr = 0
    paramtext = hoteldpt = queasy = None

    t_param = t_dept = None

    t_param_list, T_param = create_model("T_param", {"dept":int, "grup":int, "number":int, "bezeich":string, "typ":int, "logv":bool, "val":string})
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_param_list, t_dept_list, licensenr, paramtext, hoteldpt, queasy


        nonlocal t_param, t_dept
        nonlocal t_param_list, t_dept_list

        return {"t-param": t_param_list, "t-dept": t_dept_list, "licensenr": licensenr}

    def decode_string1(in_str:string):

        nonlocal t_param_list, t_dept_list, licensenr, paramtext, hoteldpt, queasy


        nonlocal t_param, t_dept
        nonlocal t_param_list, t_dept_list

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

        nonlocal t_param_list, t_dept_list, licensenr, paramtext, hoteldpt, queasy


        nonlocal t_param, t_dept
        nonlocal t_param_list, t_dept_list

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

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()


    t_param_list.clear()

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 1
        queasy.char1 = "URL Image Logo Hotel"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 2
        queasy.char1 = "Font Color 1"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 3
        queasy.char1 = "Font Color 2"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 4
        queasy.char1 = "Background Color"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 5
        queasy.char1 = "Using Payment Gateway"
        queasy.number3 = 4
        queasy.char2 = ""
        queasy.logi1 = True
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 6
        queasy.char1 = "URL Endpoint WebServices"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 7
        queasy.char1 = "Parameter Payment Gateway MIDtrans"
        queasy.number3 = 5
        queasy.char2 = "MERCHANTID=11129189"
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 8
        queasy.char1 = "Parameter Payment Gateway QRIS"
        queasy.number3 = 5
        queasy.char2 = "MALLID=3836;CLIENTID=3836"
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 9
        queasy.char1 = "UserInit For SelfOrder"
        queasy.number3 = 5
        queasy.char2 = "01"
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 10
        queasy.char1 = "Parameter Payment Gateway DOKU"
        queasy.number3 = 5
        queasy.char2 = "MERCHANTID=11129189"
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 11
        queasy.char1 = "Price Include Tax and Services"
        queasy.number3 = 4
        queasy.logi1 = False
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 12
        queasy.char1 = "Enable Item Notes"
        queasy.number3 = 4
        queasy.logi1 = False
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 13
        queasy.char1 = "Interval Refresh Selforder Dashboard"
        queasy.number3 = 1
        queasy.char2 = "60"
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 14
        queasy.char1 = "Use Dinamic QRCode"
        queasy.number3 = 4
        queasy.logi1 = True
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 15
        queasy.char1 = "Allow Post Menu Without Confirmation"
        queasy.number3 = 4
        queasy.logi1 = True
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 16
        queasy.char1 = "Range For Geofancing (in meters)"
        queasy.number3 = 1
        queasy.char2 = "1000"
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 17
        queasy.char1 = "Location For Geofancing (longitude, latitude)"
        queasy.number3 = 5
        queasy.char2 = "-6.147497652789192, 106.89989726843324"
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 18
        queasy.char1 = "Hotel Additional Info"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 19
        queasy.char1 = "Hotel Additional Link"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 222
        queasy.number1 = 1
        queasy.number2 = 20
        queasy.char1 = "Email Receiver For Copy Bill"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = 1


    get_output(selforder_addhtp5bl())

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.betriebsnr == 1)).order_by(Queasy.number2).all():
        t_param = T_param()
        t_param_list.append(t_param)

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