from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Bediener, Res_history

def prepare_activities_historywebbl(reshist_action:str):
    from_date = None
    ubuff_list = []
    t_bediener_list = []
    bediener = res_history = None

    ubuff = t_bediener = rbuff = None

    ubuff_list, Ubuff = create_model("Ubuff", {"userinit":str, "username":str})
    t_bediener_list, T_bediener = create_model("T_bediener", {"userinit":str, "username":str})

    Rbuff = Res_history

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, ubuff_list, t_bediener_list, bediener, res_history
        nonlocal rbuff


        nonlocal ubuff, t_bediener, rbuff
        nonlocal ubuff_list, t_bediener_list
        return {"from_date": from_date, "ubuff": ubuff_list, "t-bediener": t_bediener_list}

    def check_reshistory():

        nonlocal from_date, ubuff_list, t_bediener_list, bediener, res_history
        nonlocal rbuff


        nonlocal ubuff, t_bediener, rbuff
        nonlocal ubuff_list, t_bediener_list


        Rbuff = Res_history

        res_history = db_session.query(Res_history).filter(
                (Res_history.nr == 0) &  (Res_history.betriebsnr != 0)).first()

        if not res_history:

            return
        while None != res_history:

            rbuff = db_session.query(Rbuff).filter(
                        (Rbuff._recid == res_history._recid)).first()
            rbuff.nr = rbuff.betriebsnr

            rbuff = db_session.query(Rbuff).first()

            res_history = db_session.query(Res_history).filter(
                    (Res_history.nr == 0) &  (Res_history.betriebsnr != 0)).first()

    def fill_users():

        nonlocal from_date, ubuff_list, t_bediener_list, bediener, res_history
        nonlocal rbuff


        nonlocal ubuff, t_bediener, rbuff
        nonlocal ubuff_list, t_bediener_list

        for bediener in db_session.query(Bediener).filter(
                (Bediener.flag == 0)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            t_bediener.userinit = bediener.userinit
            t_bediener.username = bediener.username

    def fill_key():

        nonlocal from_date, ubuff_list, t_bediener_list, bediener, res_history
        nonlocal rbuff


        nonlocal ubuff, t_bediener, rbuff
        nonlocal ubuff_list, t_bediener_list

        curr_action:str = " "
        loopi:int = 0

        if reshist_action == "":

            res_history = db_session.query(Res_history).first()
            while None != res_history :

                if res_history.action.lower()  != (curr_action).lower() :
                    reshist_action = res_history.action + ";" + reshist_action


                curr_action = res_history.action

                res_history = db_session.query(Res_history).first()
        else:

            return


    for bediener in db_session.query(Bediener).filter(
            (Bediener.nr != 0)).all():
        ubuff = Ubuff()
        ubuff_list.append(ubuff)

        ubuff.userinit = bediener.userinit
        ubuff.username = bediener.username


    check_reshistory()
    fill_users()
    fill_key()
    from_date = get_output(htpdate(87))

    return generate_output()