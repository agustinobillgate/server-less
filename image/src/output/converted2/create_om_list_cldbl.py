#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Outorder, Zimmer, Bediener

def create_om_list_cldbl(fdate:date, tdate:date):

    prepare_cache ([Outorder, Zimmer, Bediener])

    om_list_list = []
    datum:date = None
    user_initial:string = ""
    outorder = zimmer = bediener = None

    om_list = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":string, "userinit":string, "ind":int, "reason":string, "gespstart":date, "gespende":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal om_list_list, datum, user_initial, outorder, zimmer, bediener
        nonlocal fdate, tdate


        nonlocal om_list
        nonlocal om_list_list

        return {"om-list": om_list_list}

    if fdate != None and tdate != None:
        for datum in date_range(fdate,tdate) :

            for outorder in db_session.query(Outorder).filter(
                     ((Outorder.gespstart >= datum) & (Outorder.gespstart <= datum)) | ((Outorder.gespstart <= datum) & (Outorder.gespende >= datum))).order_by(Outorder._recid).all():

                zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

                if zimmer:

                    if num_entries(outorder.gespgrund, "$") >= 1:

                        bediener = get_cache (Bediener, {"userinit": [(eq, entry(1, outorder.gespgrund, "$"))]})

                        if bediener:
                            user_initial = bediener.userinit
                        else:

                            bediener = get_cache (Bediener, {"nr": [(eq, to_int(entry(1, outorder.gespgrund, "$")))]})

                            if bediener:
                                user_initial = bediener.userinit
                    else:

                        bediener = get_cache (Bediener, {"nr": [(eq, zimmer.bediener_nr_stat)]})

                    if bediener:
                        user_initial = bediener.userinit
                    om_list = Om_list()
                    om_list_list.append(om_list)

                    om_list.zinr = outorder.zinr
                    om_list.ind = outorder.betriebsnr + 1
                    om_list.gespstart = outorder.gespstart
                    om_list.gespende = outorder.gespende

                    if om_list.ind >= 6:
                        om_list.ind = 3
                    om_list.userinit = user_initial

                    if num_entries(outorder.gespgrund, "$") >= 1:
                        om_list.reason = entry(0, outorder.gespgrund, "$")
                    else:
                        om_list.reason = outorder.gespgrund
    else:

        for outorder in db_session.query(Outorder).order_by(Outorder._recid).all():

            zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

            if zimmer:

                if num_entries(outorder.gespgrund, "$") >= 1:

                    bediener = get_cache (Bediener, {"userinit": [(eq, entry(1, outorder.gespgrund, "$"))]})

                    if bediener:
                        user_initial = bediener.userinit
                    else:

                        bediener = get_cache (Bediener, {"nr": [(eq, to_int(entry(1, outorder.gespgrund, "$")))]})

                        if bediener:
                            user_initial = bediener.userinit
                else:

                    bediener = get_cache (Bediener, {"nr": [(eq, zimmer.bediener_nr_stat)]})

                if bediener:
                    user_initial = bediener.userinit
                om_list = Om_list()
                om_list_list.append(om_list)

                om_list.zinr = outorder.zinr
                om_list.ind = outorder.betriebsnr + 1
                om_list.gespstart = outorder.gespstart
                om_list.gespende = outorder.gespende

                if om_list.ind >= 6:
                    om_list.ind = 3
                om_list.userinit = user_initial

                if num_entries(outorder.gespgrund, "$") >= 1:
                    om_list.reason = entry(0, outorder.gespgrund, "$")
                else:
                    om_list.reason = outorder.gespgrund

    return generate_output()