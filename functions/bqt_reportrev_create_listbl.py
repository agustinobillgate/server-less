#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Guest, Bk_stat, Bk_func, Bediener

def bqt_reportrev_create_listbl(from_date:date, to_date:date):

    prepare_cache ([Bk_veran, Guest, Bk_stat, Bk_func, Bediener])

    output_list_data = []
    troomrev:Decimal = to_decimal("0.0")
    tfbrev:Decimal = to_decimal("0.0")
    tothrev:Decimal = to_decimal("0.0")
    ttrev:Decimal = to_decimal("0.0")
    bk_veran = guest = bk_stat = bk_func = bediener = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"company":string, "booker":string, "datum":date, "room":string, "resnr":int, "sales":string, "cmid":string, "rm_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal, "tot_rev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, troomrev, tfbrev, tothrev, ttrev, bk_veran, guest, bk_stat, bk_func, bediener
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_list():

        nonlocal output_list_data, troomrev, tfbrev, tothrev, ttrev, bk_veran, guest, bk_stat, bk_func, bediener
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        other_rev:Decimal = to_decimal("0.0")
        troomrev =  to_decimal("0")
        tfbrev =  to_decimal("0")
        tothrev =  to_decimal("0")
        ttrev =  to_decimal("0")


        output_list_data.clear()

        bk_stat_obj_list = {}
        bk_stat = Bk_stat()
        bk_veran = Bk_veran()
        guest = Guest()
        for bk_stat.datum, bk_stat.room, bk_stat.resnr, bk_stat.rm_rev, bk_stat.fb_rev, bk_stat.other_rev, bk_stat.salesid, bk_stat._recid, bk_veran.veran_nr, bk_veran._recid, guest.name, guest.phonetik2, guest._recid in db_session.query(Bk_stat.datum, Bk_stat.room, Bk_stat.resnr, Bk_stat.rm_rev, Bk_stat.fb_rev, Bk_stat.other_rev, Bk_stat.salesid, Bk_stat._recid, Bk_veran.veran_nr, Bk_veran._recid, Guest.name, Guest.phonetik2, Guest._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_stat.resnr)).join(Guest,(Guest.gastnr == Bk_veran.gastnr)).filter(
                 (Bk_stat.datum >= from_date) & (Bk_stat.datum <= to_date)).order_by(Bk_stat._recid).all():
            if bk_stat_obj_list.get(bk_stat._recid):
                continue
            else:
                bk_stat_obj_list[bk_stat._recid] = True

            if bk_stat:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.company = guest.name
                output_list.datum = bk_stat.datum
                output_list.room = bk_stat.room
                output_list.resnr = bk_stat.resnr
                output_list.rm_rev =  to_decimal(bk_stat.rm_rev)
                output_list.fb_rev =  to_decimal(bk_stat.fb_rev)
                output_list.other_rev =  to_decimal(bk_stat.other_rev)
                output_list.tot_rev =  to_decimal(bk_stat.rm_rev) + to_decimal(bk_stat.fb_rev) + to_decimal(bk_stat.other_rev)

                bk_func = get_cache (Bk_func, {"veran_nr": [(eq, bk_veran.veran_nr)]})

                if bk_func:
                    output_list.booker = bk_func.kontaktperson[0]

                bediener = get_cache (Bediener, {"userinit": [(eq, bk_stat.salesid)]})

                if bediener:
                    output_list.sales = bediener.username

                bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik2)]})

                if bediener:
                    output_list.cmid = bediener.username

    create_list()

    return generate_output()