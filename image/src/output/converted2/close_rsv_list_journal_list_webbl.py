#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import B_history, Bk_rart, Bk_stat, Bk_veran, Bediener, Guest

def close_rsv_list_journal_list_webbl(from_date:date, to_date:date):

    prepare_cache ([B_history, Bk_rart, Bk_stat, Bk_veran, Bediener, Guest])

    troomrev = to_decimal("0.0")
    tfbrev = to_decimal("0.0")
    tothrev = to_decimal("0.0")
    ttrev = to_decimal("0.0")
    output_list_list = []
    total_rev:Decimal = to_decimal("0.0")
    b_history = bk_rart = bk_stat = bk_veran = bediener = guest = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"datum":date, "engager":string, "contact_person":string, "ba_event":string, "venue":string, "ba_time":string, "pax":int, "room_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal, "total_rev":Decimal, "salesid":string, "cmid":string, "resnr":int, "resline":int, "tablesetup":string, "remark":string, "ba_status":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troomrev, tfbrev, tothrev, ttrev, output_list_list, total_rev, b_history, bk_rart, bk_stat, bk_veran, bediener, guest
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_list

        return {"troomrev": troomrev, "tfbrev": tfbrev, "tothrev": tothrev, "ttrev": ttrev, "output-list": output_list_list}

    def journal_list():

        nonlocal troomrev, tfbrev, tothrev, ttrev, output_list_list, total_rev, b_history, bk_rart, bk_stat, bk_veran, bediener, guest
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_list

        other_rev:Decimal = to_decimal("0.0")
        troomrev =  to_decimal("0")
        tfbrev =  to_decimal("0")
        tothrev =  to_decimal("0")
        ttrev =  to_decimal("0")


        output_list_list.clear()

        for b_history in db_session.query(B_history).filter(
                 (B_history.datum >= from_date) & (B_history.datum <= to_date) & (B_history.resstatus != 5)).order_by(B_history._recid).all():
            other_rev =  to_decimal("0")

            for bk_rart in db_session.query(Bk_rart).filter(
                     (Bk_rart.veran_nr == b_history.veran_nr) & (Bk_rart.veran_seite == b_history.veran_seite)).order_by(Bk_rart._recid).all():
                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = b_history.datum
            output_list.engager = b_history.bestellt__durch
            output_list.contact_person = b_history.v_kontaktperson[0]
            output_list.ba_event = b_history.anlass[0]
            output_list.venue = b_history.raeume[0]
            output_list.ba_time = b_history.uhrzeit
            output_list.pax = b_history.personen

            bk_stat = get_cache (Bk_stat, {"resnr": [(eq, b_history.veran_nr)]})

            if bk_stat and bk_stat.salesID != "":
                output_list.salesid = bk_stat.salesID
            else:

                bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, b_history.veran_nr)]})

                if bk_veran:

                    if bk_veran.betrieb_gast > 0:

                        bediener = get_cache (Bediener, {"nr": [(eq, bk_veran.betrieb_gast)]})

                    if bediener:
                        output_list.salesid = bediener.userinit
                    else:

                        guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                        if guest.phonetik3 != "":
                            output_list.salesid = guest.phonetik3
                        else:
                            output_list.salesid = "**"

                        if guest.phonetik2 != "":
                            output_list.cmid = to_string(guest.phonetik2, "x(2)")
                        else:
                            output_list.cmid = "**"
                else:
                    output_list.salesid = "**"
            output_list.tablesetup = b_history.tischform[0]
            output_list.remark = b_history.bemerkung
            output_list.resnr = b_history.veran_nr
            output_list.resline = b_history.veran_seite
            output_list.ba_status = b_history.c_resstatus[0]
            output_list.room_rev =  to_decimal(b_history.rpreis[0])
            output_list.fb_rev =  to_decimal(b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0])
            output_list.other_rev =  to_decimal(other_rev)
            output_list.total_rev =  to_decimal(b_history.rpreis[0] + (b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0])) +\
                    other_rev
            total_rev =  to_decimal(total_rev) + to_decimal(b_history.deposit)
            troomrev =  to_decimal(troomrev) + to_decimal(b_history.rpreis[0])
            tfbrev =  to_decimal(tfbrev) + to_decimal((b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0]) )
            tothrev =  to_decimal(tothrev) + to_decimal(other_rev)
            ttrev =  to_decimal(ttrev) + to_decimal((b_history.rpreis[0] + (b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0])) +\
                    other_rev )

    journal_list()

    return generate_output()