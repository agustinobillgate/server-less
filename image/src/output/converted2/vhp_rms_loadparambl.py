#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def vhp_rms_loadparambl(dept_no:int):

    prepare_cache ([Queasy])

    t_param_list = []
    loop_i:int = 0
    rpt_list:List[string] = create_empty_list(19,"")
    queasy = None

    t_param = None

    t_param_list, T_param = create_model("T_param", {"dept":int, "grup":int, "number":int, "bezeich":string, "typ":int, "logv":bool, "val":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_param_list, loop_i, rpt_list, queasy
        nonlocal dept_no


        nonlocal t_param
        nonlocal t_param_list

        return {"t-param": t_param_list}

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 1)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 1
        queasy.char1 = "Username"
        queasy.number3 = 5
        queasy.char2 = ""

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 2)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 2
        queasy.char1 = "Password"
        queasy.number3 = 5
        queasy.char2 = ""

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 3)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 3
        queasy.char1 = "Hotel Code"
        queasy.number3 = 5
        queasy.char2 = ""

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 4)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 4
        queasy.char1 = "Interval Refresh Time"
        queasy.number3 = 1
        queasy.char2 = ""

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 5)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 5
        queasy.char1 = "Output Local Filepath"
        queasy.number3 = 5
        queasy.char2 = "C:\\e1-vhp\\rms\\"


    rpt_list[5] = "Master Data"
    rpt_list[6] = "Room Overview"
    rpt_list[7] = "Room Availability"
    rpt_list[8] = "Monthly Forecast Of Room Occupancy"
    rpt_list[9] = "Forecast Room Production"
    rpt_list[10] = "Future Booking"
    rpt_list[11] = "Reservation By Creation Date"
    rpt_list[12] = "Inhouse Guest List"
    rpt_list[13] = "Cancelled Reservation"
    rpt_list[14] = "Room Revenue Breakdown"
    rpt_list[15] = "Front Office Turnover Report"
    rpt_list[16] = "Company Room Production"
    rpt_list[17] = "Travel Agent Room Production"
    rpt_list[18] = "Room Recapitulation With Guest Segment"
    for loop_i in range(6,19 + 1) :

        queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, loop_i)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 347
            queasy.betriebsnr = 3
            queasy.number1 = loop_i
            queasy.char1 = "URL " + rpt_list[loop_i - 1] + " (method;url)"
            queasy.number3 = 5
            queasy.char2 = ""

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 20)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 20
        queasy.char1 = "Debug Mode"
        queasy.number3 = 4
        queasy.logi1 = True

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 21)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 21
        queasy.char1 = "Using Token"
        queasy.number3 = 4
        queasy.logi1 = False

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 22)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 22
        queasy.char1 = "URL Get Token"
        queasy.number3 = 5
        queasy.char2 = ""

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 23)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 23
        queasy.char1 = "Authentication Method"
        queasy.number3 = 5
        queasy.char2 = ""

    queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, 24)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 347
        queasy.betriebsnr = 3
        queasy.number1 = 24
        queasy.char1 = "Authentication Code"
        queasy.number3 = 5
        queasy.char2 = ""

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 347) & (Queasy.betriebsnr == 3)).order_by(Queasy.number1).all():
        t_param = T_param()
        t_param_list.append(t_param)

        t_param.dept = queasy.betriebsnr
        t_param.number = queasy.number1
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