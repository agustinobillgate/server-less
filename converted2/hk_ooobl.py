#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Bediener, Zimmer, Outorder

om_list_data, Om_list = create_model("Om_list", {"zinr":string, "userinit":string, "ind":int, "reason":string, "gespstart":date, "gespende":date})

def hk_ooobl(om_list_data:[Om_list], fdate:date, tdate:date, disptype:int, sorttype:int, user_init:string):

    prepare_cache ([Zimmer, Outorder])

    ci_date = None
    ooo_list_data = []
    bediener = zimmer = outorder = None

    om_list = ooo_list = None

    ooo_list_data, Ooo_list = create_model("Ooo_list", {"zinr":string, "gespgrund":string, "gespstart":date, "gespende":date, "userinit":string, "etage":int, "ind":int, "bezeich":string, "betriebsnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, ooo_list_data, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal ooo_list_data

        return {"ci_date": ci_date, "ooo-list": ooo_list_data}

    def disp_it():

        nonlocal ci_date, ooo_list_data, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal ooo_list_data

        if disptype == 0:

            if sorttype == 0:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()


        elif disptype == 1:

            if sorttype == 0:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()


        elif disptype == 2:

            if sorttype == 0:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

    def disp_it1():

        nonlocal ci_date, ooo_list_data, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal ooo_list_data

        if disptype == 0:

            if sorttype == 0:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()


        elif disptype == 1:

            if sorttype == 0:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind != 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()


        elif disptype == 2:

            if sorttype == 0:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by((Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).order_by(Outorder.betriebsnr, (Outorder.zinr)).all():
                    om_list = query(om_list_data, (lambda om_list: om_list.zinr == outorder.zinr and om_list.ind == 3 and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)
                    if not om_list:
                        continue

                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    assign_it()

    def assign_it():

        nonlocal ci_date, ooo_list_data, bediener, zimmer, outorder
        nonlocal fdate, tdate, disptype, sorttype, user_init


        nonlocal om_list, ooo_list
        nonlocal ooo_list_data


        ooo_list = Ooo_list()
        ooo_list_data.append(ooo_list)

        ooo_list.zinr = outorder.zinr
        ooo_list.gespstart = outorder.gespstart
        ooo_list.gespende = outorder.gespende
        ooo_list.userinit = om_list.userinit
        ooo_list.etage = zimmer.etage
        ooo_list.bezeich = zimmer.bezeich
        ooo_list.ind = om_list.ind
        ooo_list.betriebsnr = outorder.betriebsnr

        if matches(om_list.reason,r"*$*"):
            ooo_list.gespgrund = entry(1, om_list.reason, "$")
        else:
            ooo_list.gespgrund = om_list.reason


    ooo_list_data.clear()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    ci_date = get_output(htpdate(87))

    if fdate == None and tdate == None:
        disp_it()

    elif fdate != None and tdate != None:
        disp_it1()

    return generate_output()