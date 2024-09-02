from functions.additional_functions import *
import decimal
from datetime import date
from models import Outorder, Zimmer, Bediener

def create_om_list_cldbl(fdate:date, tdate:date):
    om_list_list = []
    datum:date = None
    outorder = zimmer = bediener = None

    om_list = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "userinit":str, "ind":int, "reason":str, "gespstart":date, "gespende":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal om_list_list, datum, outorder, zimmer, bediener


        nonlocal om_list
        nonlocal om_list_list
        return {"om-list": om_list_list}

    if fdate != None and tdate != None:
        for datum in range(fdate,tdate + 1) :

            for outorder in db_session.query(Outorder).filter(
                    ((Outorder.gespstart >= datum) &  (Outorder.gespstart <= datum)) |  ((Outorder.gespstart <= datum) &  (Outorder.gespende >= datum))).all():

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == outorder.zinr)).first()

                if zimmer:

                    if num_entries(outorder.gespgrund, "$") >= 1:

                        bediener = db_session.query(Bediener).filter(
                                (Bediener.nr == to_int(entry(1, outorder.gespgrund, "$")))).first()
                    else:

                        bediener = db_session.query(Bediener).filter(
                                (Bediener.nr == zimmer.bediener_nr_stat)).first()
                    om_list = Om_list()
                    om_list_list.append(om_list)

                    om_list.zinr = outorder.zinr
                    om_list.ind = outorder.betriebsnr + 1
                    om_list.gespstart = outorder.gespstart
                    om_list.gespende = outorder.gespende

                    if om_list.ind >= 6:
                        om_list.ind = 3

                    if bediener:
                        om_list.userinit = bediener.userinit

                    if num_entries(outorder.gespgrund, "$") >= 1:
                        om_list.reason = entry(0, outorder.gespgrund, "$")
                    else:
                        om_list.reason = outorder.gespgrund
    else:

        for outorder in db_session.query(Outorder).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == outorder.zinr)).first()

            if zimmer:

                if num_entries(outorder.gespgrund, "$") >= 1:

                    bediener = db_session.query(Bediener).filter(
                            (Bediener.nr == to_int(entry(1, outorder.gespgrund, "$")))).first()
                else:

                    bediener = db_session.query(Bediener).filter(
                            (Bediener.nr == zimmer.bediener_nr_stat)).first()
                om_list = Om_list()
                om_list_list.append(om_list)

                om_list.zinr = outorder.zinr
                om_list.ind = outorder.betriebsnr + 1
                om_list.gespstart = outorder.gespstart
                om_list.gespende = outorder.gespende

                if om_list.ind >= 6:
                    om_list.ind = 3

                if bediener:
                    om_list.userinit = bediener.userinit

                if num_entries(outorder.gespgrund, "$") >= 1:
                    om_list.reason = entry(0, outorder.gespgrund, "$")
                else:
                    om_list.reason = outorder.gespgrund

    return generate_output()