#using conversion tools version: 1.0.0.119
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, Messages, Res_line, Zimplan, Outorder, Zinrstat, Guest, Reservation
from sqlalchemy import func

def noshowbl(user_init:string):

    prepare_cache ([Htparam, Bediener, Zinrstat, Guest, Reservation])

    mail_exist = False
    res_recid1:int = 0
    i:int = 0
    ci_date:date = None
    cofftime:int = 18
    htparam = bediener = messages = res_line = zimplan = outorder = zinrstat = guest = reservation = None

    reslist = None

    reslist_data, Reslist = create_model("Reslist", {"resnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mail_exist, res_recid1, i, ci_date, cofftime, htparam, bediener, messages, res_line, zimplan, outorder, zinrstat, guest, reservation
        nonlocal user_init


        nonlocal reslist
        nonlocal reslist_data

        return {"mail_exist": mail_exist}

    def read_messages():

        nonlocal mail_exist, res_recid1, i, ci_date, cofftime, htparam, bediener, messages, res_line, zimplan, outorder, zinrstat, guest, reservation
        nonlocal user_init


        nonlocal reslist
        nonlocal reslist_data

        date_str:string = ""
        date_str = to_string(get_year(get_current_date())) + "/" + to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99")

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if not bediener:
            pass
        else:

            messages = db_session.query(Messages).filter(
                        (Messages.gastnr == bediener.nr) & (Messages.reslinnr <= 2) & 
                        (Messages.resnr == 0) & (Messages.betriebsnr == 0) & 
                        (((Messages.name == "")) | ((Messages.name <= (date_str).lower())))).first()
            mail_exist = None != messages


    def noshow():

        nonlocal mail_exist, res_recid1, i, ci_date, cofftime, htparam, bediener, messages, res_line, zimplan, outorder, zinrstat, guest, reservation
        nonlocal user_init
        nonlocal reslist
        nonlocal reslist_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 297)]})

        if htparam.feldtyp == 1 and htparam.finteger >= 2 and htparam.finteger <= 11:
            cofftime = htparam.finteger + 12

        if get_current_time_in_seconds() <= (cofftime * 3600 + 5 * 60):

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        # res_line = get_cache (Res_line, {"active_flag": [(eq, 0)],"ankunft": [(eq, ci_date)],"resstatus": [(eq, 2)]})
        res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus == 2)).with_for_update().first()
        while None != res_line:

            # reslist = query(reslist_data, filters=(lambda reslist: reslist.resnr == res_line.resnr), first=True)
            reslist = db_session.query(Reslist).filter(Reslist.resnr == res_line.resnr).with_for_update().first()

            if not reslist:
                reslist = Reslist()
                reslist_data.append(reslist)

                reslist.resnr = res_line.resnr

            if res_line.zinr != "":
                res_recid1 = res_line._recid

                for zimplan in db_session.query(Zimplan).filter(
                             (Zimplan.zinr == res_line.zinr) & (Zimplan.datum >= ci_date) & (Zimplan.datum <= res_line.abreise) & (Zimplan.res_recid == res_recid1)).order_by(Zimplan._recid).all():
                    db_session.delete(zimplan)

                outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"betriebsnr": [(eq, res_line.resnr)]})

                if outorder:
                    db_session.delete(outorder)
                    pass
            pass
            res_line.betrieb_gastpay = res_line.resstatus
            res_line.resstatus = 10
            res_line.active_flag = 2

            # zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "no-show")],"datum": [(eq, ci_date)]})
            zinrstat = db_session.query(Zinrstat).filter(func.lower(Zinrstat.zinr) == ("No-Show").lower(), 
                                                       Zinrstat.datum == ci_date).with_for_update().first()

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = ci_date
                zinrstat.zinr = "No-Show"


            zinrstat.zimmeranz = zinrstat.zimmeranz + res_line.zimmeranz
            zinrstat.personen = zinrstat.personen + res_line.erwachs


            pass

            # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).with_for_update().first()

            if guest:
                guest.noshows = guest.noshows + 1
                pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus == 2) & (Res_line._recid > curr_recid)).with_for_update().first()

        for reslist in query(reslist_data):

            res_line = get_cache (Res_line, {"resnr": [(eq, reslist.resnr)],"active_flag": [(lt, 2)]})

            if not res_line:

                # reservation = get_cache (Reservation, {"resnr": [(eq, reslist.resnr)]})
                reservation = db_session.query(Reservation).filter(Reservation.resnr == reslist.resnr).with_for_update().first()
                reservation.activeflag = 1
                reservation.vesrdepot2 = "No-show 6PM"
                pass
            reslist_data.remove(reslist)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 373)]})

    if htparam.flogical:
        noshow()
    read_messages()

    return generate_output()