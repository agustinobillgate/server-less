from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_veran, Guest, Bk_stat, Bk_func, Bediener

def bqt_reportrev_create_listbl(from_date:date, to_date:date):
    output_list_list = []
    troomrev:decimal = to_decimal("0.0")
    tfbrev:decimal = to_decimal("0.0")
    tothrev:decimal = to_decimal("0.0")
    ttrev:decimal = to_decimal("0.0")
    bk_veran = guest = bk_stat = bk_func = bediener = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"company":str, "booker":str, "datum":date, "room":str, "resnr":int, "sales":str, "cmid":str, "rm_rev":decimal, "fb_rev":decimal, "other_rev":decimal, "tot_rev":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, troomrev, tfbrev, tothrev, ttrev, bk_veran, guest, bk_stat, bk_func, bediener
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def create_list():

        nonlocal output_list_list, troomrev, tfbrev, tothrev, ttrev, bk_veran, guest, bk_stat, bk_func, bediener
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_list

        other_rev:decimal = to_decimal("0.0")
        troomrev =  to_decimal("0")
        tfbrev =  to_decimal("0")
        tothrev =  to_decimal("0")
        ttrev =  to_decimal("0")


        output_list_list.clear()

        bk_stat_obj_list = []
        for bk_stat, bk_veran, guest in db_session.query(Bk_stat, Bk_veran, Guest).join(Bk_veran,(Bk_veran.veran_nr == Bk_stat.resnr)).join(Guest,(Guest.gastnr == Bk_veran.gastnr)).filter(
                 (Bk_stat.datum >= from_date) & (Bk_stat.datum <= to_date)).order_by(Bk_stat._recid).all():
            if bk_stat._recid in bk_stat_obj_list:
                continue
            else:
                bk_stat_obj_list.append(bk_stat._recid)

            if bk_stat:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.company = guest.name
                output_list.datum = bk_stat.datum
                output_list.room = bk_stat.room
                output_list.resnr = bk_stat.resnr
                output_list.rm_rev =  to_decimal(bk_stat.rm_rev)
                output_list.fb_rev =  to_decimal(bk_stat.fb_rev)
                output_list.other_rev =  to_decimal(bk_stat.other_rev)
                output_list.tot_rev =  to_decimal(bk_stat.rm_rev) + to_decimal(bk_stat.fb_rev) + to_decimal(bk_stat.other_rev)

                bk_func = db_session.query(Bk_func).filter(
                         (Bk_func.veran_nr == bk_veran.veran_nr)).first()

                if bk_func:
                    output_list.booker = bk_func.kontaktperson[0]

                bediener = db_session.query(Bediener).filter(
                         (Bediener.userinit == bk_stat.salesid)).first()

                if bediener:
                    output_list.sales = bediener.username

                bediener = db_session.query(Bediener).filter(
                         (Bediener.userinit == guest.phonetik2)).first()

                if bediener:
                    output_list.cmid = bediener.username

    create_list()

    return generate_output()