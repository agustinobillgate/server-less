from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_func, Bk_veran, Guest, B_storno, Bk_rart

def cancel_rsv_list_journal_listbl(from_date:date, to_date:date):
    curr_select1 = 0
    output_list_list = []
    t_out_list = []
    bk_func = bk_veran = guest = b_storno = bk_rart = None

    output_list = t_out = None

    output_list_list, Output_list = create_model("Output_list", {"str":str, "cperson":str, "tevent":str, "venue":str, "pax":str})
    t_out_list, T_out = create_model("T_out", {"rsv_date":str, "b_date":str, "rsv_no":str, "resline":str, "engager":str, "cperson":str, "tevent":str, "venue":str, "pax":str, "reason":str, "id":str, "room_rev":str, "fb_rev":str, "other_rev":str, "tot_rev":str, "f_empty":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_select1, output_list_list, t_out_list, bk_func, bk_veran, guest, b_storno, bk_rart
        nonlocal from_date, to_date


        nonlocal output_list, t_out
        nonlocal output_list_list, t_out_list
        return {"curr_select1": curr_select1, "output-list": output_list_list, "t-out": t_out_list}

    def journal_list():

        nonlocal curr_select1, output_list_list, t_out_list, bk_func, bk_veran, guest, b_storno, bk_rart
        nonlocal from_date, to_date


        nonlocal output_list, t_out
        nonlocal output_list_list, t_out_list

        other_revenue:decimal = to_decimal("0.0")
        output_list_list.clear()
        t_out_list.clear()

        b_storno_obj_list = []
        for b_storno, bk_func, bk_veran, guest in db_session.query(B_storno, Bk_func, Bk_veran, Guest).join(Bk_func,(Bk_func.veran_nr == B_storno.bankettnr)).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).join(Guest,(Guest.gastnr == B_storno.gastnr)).filter(
                 (B_storno.datum >= from_date) & (B_storno.datum <= to_date) & (B_storno.grund[inc_value(17)] != "")).order_by(B_storno._recid).all():
            if b_storno._recid in b_storno_obj_list:
                continue
            else:
                b_storno_obj_list.append(b_storno._recid)

            if bk_veran:
                other_revenue =  to_decimal("0")
                curr_select1 = int (b_storno.bankettnr)

                for bk_rart in db_session.query(Bk_rart).filter(
                         (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                    other_revenue =  to_decimal(other_revenue) + to_decimal((bk_rart.preis) * to_decimal(anzahl))

            if guest:
                output_list = Output_list()
                output_list_list.append(output_list)

                str = to_string(bk_veran.kontaktfirst, "99/99/99") + to_string(b_storno.datum, "99/99/99") + to_string(b_storno.bankettnr, ">>>>>>>>") + to_string(b_storno.breslinnr, ">>>") + to_string(guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma, "x(32)") + to_string(b_storno.grund[17], "x(62)") + to_string(b_storno.usercode, "x(3)") + to_string(bk_func.rpreis[0], "->>>,>>>,>>>,>>9.99") + to_string((bk_func.rpreis[6] * bk_func.rpersonen[0]) , "->>>,>>>,>>9.99") + to_string(other_revenue, "->>>,>>>,>>9.99") + to_string((bk_func.rpreis[0] + (bk_func.rpreis[6] * bk_func.rpersonen[0]) + other_revenue) , "->>>,>>>,>>>,>>9.99")
                output_list.pax = to_string(bk_func.personen, ">,>>>")
                output_list.venue = to_string(bk_func.raeume[0], "x(12)")
                output_list.cperson = to_string(bk_func.v_kontaktperson[0], "x(32)")
                output_list.tevent = to_string(bk_func.zweck[0], "x(18)")

        for output_list in query(output_list_list):
            t_out = T_out()
            t_out_list.append(t_out)

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