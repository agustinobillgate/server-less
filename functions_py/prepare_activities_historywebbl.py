#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 17-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Bediener, Res_history

def prepare_activities_historywebbl(reshist_action:string):

    prepare_cache ([Bediener])

    from_date = None
    ubuff_data = []
    t_bediener_data = []
    bediener = res_history = None

    ubuff = t_bediener = None

    ubuff_data, Ubuff = create_model("Ubuff", {"userinit":string, "username":string})
    t_bediener_data, T_bediener = create_model("T_bediener", {"userinit":string, "username":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, ubuff_data, t_bediener_data, bediener, res_history
        nonlocal reshist_action


        nonlocal ubuff, t_bediener
        nonlocal ubuff_data, t_bediener_data

        return {"from_date": from_date, "ubuff": ubuff_data, "t-bediener": t_bediener_data, "reshist_action": reshist_action}

    def check_reshistory():

        nonlocal from_date, ubuff_data, t_bediener_data, bediener, res_history
        nonlocal reshist_action


        nonlocal ubuff, t_bediener
        nonlocal ubuff_data, t_bediener_data

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Res_history)

        res_history = get_cache (Res_history, {"nr": [(eq, 0)],"betriebsnr": [(ne, 0)]})

        if not res_history:

            return
        while None != res_history:

            rbuff = db_session.query(Rbuff).filter(
                         (Rbuff._recid == res_history._recid)).first()
            rbuff.nr = rbuff.betriebsnr


            pass
            pass

            curr_recid = res_history._recid
            res_history = db_session.query(Res_history).filter(
                     (Res_history.nr == 0) & (Res_history.betriebsnr != 0) & (Res_history._recid > curr_recid)).first()


    def fill_users():

        nonlocal from_date, ubuff_data, t_bediener_data, bediener, res_history
        nonlocal reshist_action


        nonlocal ubuff, t_bediener
        nonlocal ubuff_data, t_bediener_data

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.flag == 0)).order_by(Bediener.username).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            t_bediener.userinit = bediener.userinit
            t_bediener.username = bediener.username


    def fill_key():

        nonlocal from_date, ubuff_data, t_bediener_data, bediener, res_history
        nonlocal reshist_action


        nonlocal ubuff, t_bediener
        nonlocal ubuff_data, t_bediener_data

        log_available:bool = False
        last_action:string = ""

        if reshist_action == "":
            reshist_action = ";"
            while True:
                log_available = True

                for res_history in db_session.query(Res_history).filter(
                         (Res_history.action > (last_action).lower()) & (not_(matches(reshist_action,"*;" + Res_history.action + ";*")))).order_by(Res_history.action).all():
                    log_available = True
                    last_action = res_history.action
                    reshist_action = reshist_action + res_history.action + ";"

                if not log_available:
                    return
            reshist_action = trim(reshist_action, ";")

    for bediener in db_session.query(Bediener).filter(
             (Bediener.nr != 0)).order_by(Bediener._recid).all():
        ubuff = Ubuff()
        ubuff_data.append(ubuff)

        ubuff.userinit = bediener.userinit
        ubuff.username = bediener.username


    check_reshistory()
    fill_users()
    fill_key()
    from_date = get_output(htpdate(87))

    return generate_output()