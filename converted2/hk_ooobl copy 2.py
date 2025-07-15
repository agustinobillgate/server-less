from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from models import Bediener, Zimmer, Outorder

om_list_list, Om_list = create_model("Om_list", {"zinr":str, "userinit":str, "ind":int, "reason":str, "gespstart":date, "gespende":date})

def hk_ooobl(om_list_list:[Om_list], fdate:date, tdate:date, disptype:int, sorttype:int, user_init:str):
    ci_date = None
    ooo_list_list = []
    bediener = zimmer = outorder = None

    om_list = ooo_list = None

    ooo_list_list, Ooo_list = create_model("Ooo_list", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, ooo_list_list, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal om_list_list, ooo_list_list
        return {"ci_date": ci_date, "ooo-list": ooo_list_list}

    def disp_it():

        nonlocal ci_date, ooo_list_list, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal om_list_list, ooo_list_list

        if disptype == 0:

            if sorttype == 0:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()


        elif disptype == 1:

            if sorttype == 0:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()


        elif disptype == 2:

            if sorttype == 0:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

    def disp_it1():

        nonlocal ci_date, ooo_list_list, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal om_list_list, ooo_list_list

        if disptype == 0:

            if sorttype == 0:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()


        elif disptype == 1:

            if sorttype == 0:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()


        elif disptype == 2:

            if sorttype == 0:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_list, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    assign_it()

    def assign_it():

        nonlocal ci_date, ooo_list_list, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal om_list_list, ooo_list_list


        ooo_list = Ooo_list()
        ooo_list_list.append(ooo_list)

        ooo_list.zinr = outorder.zinr
        ooo_list.gespstart = outorder.gespstart
        ooo_list.gespende = outorder.gespende
        ooo_list.userinit = om_list.userinit
        ooo_list.etage = zimmer.etage
        ooo_list.bezeich = zimmer.bezeich
        ooo_list.ind = om_list.ind
        ooo_list.betriebsnr = outorder.betriebsnr

        if re.match(".*\$.*",om_list.reason, re.IGNORECASE):
            ooo_list.gespgrund = entry(1, om_list.reason, "$")
        else:
            ooo_list.gespgrund = om_list.reason


    ooo_list_list.clear()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    ci_date = get_output(htpdate(87))

    if fdate == None and tdate == None:
        disp_it()

    elif fdate != None and tdate != None:
        disp_it1()

    return generate_output()