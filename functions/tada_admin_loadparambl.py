#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def tada_admin_loadparambl(dept_no:int):
    t_param_data = []
    queasy = None

    t_param = None

    t_param_data, T_param = create_model("T_param", {"dept":int, "grup":int, "number":int, "bezeich":string, "typ":int, "logv":bool, "val":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_param_data, queasy
        nonlocal dept_no


        nonlocal t_param
        nonlocal t_param_data

        return {"t-param": t_param_data}


    t_param_data.clear()
    dept_no = 1

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 1)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 1
        queasy.char1 = "Username"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 2)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 2
        queasy.char1 = "Password"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 3)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 3
        queasy.char1 = "Interval Refresh Time"
        queasy.number3 = 1
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 4)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 4
        queasy.char1 = "Department In TADA"
        queasy.number3 = 1
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 5)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 5
        queasy.char1 = "Reserve Table For TADA"
        queasy.number3 = 1
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 6)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 6
        queasy.char1 = "Program ID"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 7)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 7
        queasy.char1 = "Wallet ID TOPUP Points"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 8)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 8
        queasy.char1 = "Wallet ID TOPUP Balance"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 9)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 9
        queasy.char1 = "MID"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 10)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 10
        queasy.char1 = "Terminal ID FO"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 11)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 11
        queasy.char1 = "Terminal ID FB"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 12)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 12
        queasy.char1 = "SFTP Server Address"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 13)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 13
        queasy.char1 = "SFTP User ID"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 14)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 14
        queasy.char1 = "SFTP Private Key Filepath"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 15)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 15
        queasy.char1 = "SFTP PSCP Filepath"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 16)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 16
        queasy.char1 = "SFTP Server Filepath"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 17)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 17
        queasy.char1 = "SFTP Local Filepath"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 18)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 18
        queasy.char1 = "Segment For FO Transaction"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 19)]})

    if not queasy:
        pass
    else:
        db_session.delete(queasy)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 20)]})

    if not queasy:
        pass
    else:
        db_session.delete(queasy)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 21)]})

    if not queasy:
        pass
    else:
        db_session.delete(queasy)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 22)]})

    if not queasy:
        pass
    else:
        db_session.delete(queasy)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 23)]})

    if not queasy:
        pass
    else:
        db_session.delete(queasy)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 24)]})

    if not queasy:
        pass
    else:
        db_session.delete(queasy)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 25)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 25
        queasy.char1 = "Dummy Guest Number For Payment FB"
        queasy.number3 = 1
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 26)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 26
        queasy.char1 = "Artikel Number For Guest Ledger"
        queasy.number3 = 1
        queasy.char2 = ""
        queasy.betriebsnr = dept_no

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 27)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 27
        queasy.char1 = "Credential For FO (deptno;username;password;tadadept;vhpartdisc)"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no


    else:
        queasy.char1 = "Credential For FO (deptno;username;password;tadadept;vhpartdisc)"

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 28)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 28
        queasy.char1 = "Credential For Outlet (deptno;username;password;tadadept;vhpartdisc)"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no


    else:
        queasy.char1 = "Credential For Outlet (deptno;username;password;tadadept;vhpartdisc)"

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 29)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 29
        queasy.char1 = "Credential For Outlet (deptno;username;password;tadadept;vhpartdisc)"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no


    else:
        queasy.char1 = "Credential For Outlet (deptno;username;password;tadadept;vhpartdisc)"

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, dept_no)],"number2": [(eq, 30)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 270
        queasy.number1 = 1
        queasy.number2 = 30
        queasy.char1 = "Credential For Outlet (deptno;username;password;tadadept;vhpartdisc)"
        queasy.number3 = 5
        queasy.char2 = ""
        queasy.betriebsnr = dept_no


    else:
        queasy.char1 = "Credential For Outlet (deptno;username;password;tadadept;vhpartdisc)"

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1) & (Queasy.betriebsnr == dept_no)).order_by(Queasy.number2).all():
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