#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_func, Bk_veran, Guest, B_storno, Bk_rart

def cancel_rsv_list_journal_listbl(from_date:date, to_date:date):

    prepare_cache ([Bk_func, Bk_veran, Guest, B_storno, Bk_rart])

    curr_select1 = 0
    output_list_data = []
    t_out_data = []
    bk_func = bk_veran = guest = b_storno = bk_rart = None

    output_list = t_out = None

    output_list_data, Output_list = create_model("Output_list", {"str":string, "cperson":string, "tevent":string, "venue":string, "pax":string})
    t_out_data, T_out = create_model("T_out", {"rsv_date":string, "b_date":string, "rsv_no":string, "resline":string, "engager":string, "cperson":string, "tevent":string, "venue":string, "pax":string, "reason":string, "id":string, "room_rev":string, "fb_rev":string, "other_rev":string, "tot_rev":string, "f_empty":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_select1, output_list_data, t_out_data, bk_func, bk_veran, guest, b_storno, bk_rart
        nonlocal from_date, to_date


        nonlocal output_list, t_out
        nonlocal output_list_data, t_out_data

        return {"curr_select1": curr_select1, "output-list": output_list_data, "t-out": t_out_data}

    def journal_list():

        nonlocal curr_select1, output_list_data, t_out_data, bk_func, bk_veran, guest, b_storno, bk_rart
        nonlocal from_date, to_date


        nonlocal output_list, t_out
        nonlocal output_list_data, t_out_data

        other_revenue:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_out_data.clear()

        b_storno_obj_list = {}
        b_storno = B_storno()
        bk_func = Bk_func()
        bk_veran = Bk_veran()
        guest = Guest()
        for b_storno.bankettnr, b_storno.datum, b_storno.breslinnr, b_storno.grund, b_storno.usercode, b_storno._recid, bk_func.veran_nr, bk_func.veran_seite, bk_func.rpreis, bk_func.rpersonen, bk_func.personen, bk_func.raeume, bk_func.v_kontaktperson, bk_func.zweck, bk_func._recid, bk_veran.kontaktfirst, bk_veran._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest._recid in db_session.query(B_storno.bankettnr, B_storno.datum, B_storno.breslinnr, B_storno.grund, B_storno.usercode, B_storno._recid, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.personen, Bk_func.raeume, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest._recid).join(Bk_func,(Bk_func.veran_nr == B_storno.bankettnr)).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).join(Guest,(Guest.gastnr == B_storno.gastnr)).filter(
                 (B_storno.datum >= from_date) & (B_storno.datum <= to_date) & (B_storno.grund[inc_value(17)] != "")).order_by(B_storno._recid).all():
            if b_storno_obj_list.get(b_storno._recid):
                continue
            else:
                b_storno_obj_list[b_storno._recid] = True

            if bk_veran:
                other_revenue =  to_decimal("0")
                curr_select1 = int (b_storno.bankettnr)

                for bk_rart in db_session.query(Bk_rart).filter(
                         (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                    other_revenue =  to_decimal(other_revenue) + to_decimal((bk_rart.preis) * to_decimal(anzahl))

            if guest:
                output_list = Output_list()
                output_list_data.append(output_list)

                str = to_string(bk_veran.kontaktfirst, "99/99/99") + to_string(b_storno.datum, "99/99/99") + to_string(b_storno.bankettnr, ">>>>>>>>") + to_string(b_storno.breslinnr, ">>>") + to_string(guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma, "x(32)") + to_string(b_storno.grund[17], "x(62)") + to_string(b_storno.usercode, "x(3)") + to_string(bk_func.rpreis[0], "->>>,>>>,>>>,>>9.99") + to_string((bk_func.rpreis[6] * bk_func.rpersonen[0]) , "->>>,>>>,>>9.99") + to_string(other_revenue, "->>>,>>>,>>9.99") + to_string((bk_func.rpreis[0] + (bk_func.rpreis[6] * bk_func.rpersonen[0]) + other_revenue) , "->>>,>>>,>>>,>>9.99")
                output_list.pax = to_string(bk_func.personen, ">,>>>")
                output_list.venue = to_string(bk_func.raeume[0], "x(12)")
                output_list.cperson = to_string(bk_func.v_kontaktperson[0], "x(32)")
                output_list.tevent = to_string(bk_func.zweck[0], "x(18)")

        for output_list in query(output_list_data):
            t_out = T_out()
            t_out_data.append(t_out)

            t_out.rsv_date = substring(STR, 0, 8)
            t_out.b_date = substring(STR, 8, 8)
            t_out.rsv_no = substring(STR, 16, 8)
            t_out.resline = substring(STR, 24, 3)
            t_out.engager = substring(STR, 27, 32)
            t_out.reason = substring(STR, 59, 62)
            t_out.id = substring(STR, 121, 3)
            t_out.room_rev = substring(str, 124, 19)
            t_out.fb_rev = substring(str, 143, 15)
            t_out.other_rev = substring(str, 158, 15)
            t_out.tot_rev = substring(str, 173, 19)
            t_out.pax = output_list.pax
            t_out.venue = output_list.venue
            t_out.cperson = output_list.cperson


    journal_list()

    return generate_output()