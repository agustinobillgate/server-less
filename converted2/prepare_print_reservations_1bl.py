#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Guest, Reservation, Zimkateg, Paramtext, Waehrung, Messages

def prepare_print_reservations_1bl(lresnr:int, ta_gastnr:int):

    prepare_cache ([Res_line, Zimkateg, Paramtext, Waehrung])

    t_guest_data = []
    t_reservation_data = []
    t_list_data = []
    res_line = guest = reservation = zimkateg = paramtext = waehrung = messages = None

    t_list = t_guest = t_reservation = bresline = None

    t_list_data, T_list = create_model_like(Res_line, {"bed_setup":string, "str_zipreis":string, "mstr":string, "zimkateg_kurzbez":string, "sharer_no":int})
    t_guest_data, T_guest = create_model_like(Guest)
    t_reservation_data, T_reservation = create_model_like(Reservation)

    Bresline = create_buffer("Bresline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_data, t_reservation_data, t_list_data, res_line, guest, reservation, zimkateg, paramtext, waehrung, messages
        nonlocal lresnr, ta_gastnr
        nonlocal bresline


        nonlocal t_list, t_guest, t_reservation, bresline
        nonlocal t_list_data, t_guest_data, t_reservation_data

        return {"t-guest": t_guest_data, "t-reservation": t_reservation_data, "t-list": t_list_data}

    guest = get_cache (Guest, {"gastnr": [(eq, ta_gastnr)]})
    t_guest = T_guest()
    t_guest_data.append(t_guest)

    buffer_copy(guest, t_guest)

    reservation = get_cache (Reservation, {"resnr": [(eq, lresnr)]})
    t_reservation = T_reservation()
    t_reservation_data.append(t_reservation)

    buffer_copy(reservation, t_reservation)

    res_line_obj_list = {}
    res_line = Res_line()
    zimkateg = Zimkateg()
    for res_line.kontakt_nr, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.kontakt_nr, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
             (Res_line.gastnr == ta_gastnr) & (Res_line.resnr == lresnr) & (Res_line.resstatus != 12)).order_by(Res_line.zinr, Res_line.l_zuordnung[inc_value(2)], Res_line.resstatus, Res_line.name).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        t_list = T_list()
        t_list_data.append(t_list)

        buffer_copy(res_line, t_list)
        t_list.zimkateg_kurzbez = zimkateg.kurzbez
        t_list.bed_setup = ""

        if res_line.setup != 0:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, res_line.setup + 9200)]})
            t_list.bed_setup = substring(paramtext.notes, 0, 1)

        if res_line.zipreis <= 9999999:
            t_list.str_zipreis = to_string(res_line.zipreis, ">,>>>,>>9.99")
        else:
            t_list.str_zipreis = to_string(res_line.zipreis, ">>>>,>>>,>>9")

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if waehrung:
            t_list.str_zipreis = t_list.str_zipreis + to_string(waehrung.wabkurz, " x(4)")
        else:
            t_list.str_zipreis = t_list.str_zipreis + to_string("", " x(4)")

        messages = get_cache (Messages, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if messages:
            t_list.mstr = "M "
        else:
            t_list.mstr = " "

        if res_line.resstatus != 11 and res_line.resstatus != 13:

            bresline = db_session.query(Bresline).filter(
                     (Bresline.reslinnr != res_line.reslinnr) & (Bresline.kontakt_nr == res_line.reslinnr) & ((Bresline.resstatus == 11) | (Bresline.resstatus == 13))).first()

            if bresline:
                t_list.sharer_no = bresline.kontakt_nr


        else:
            t_list.sharer_no = res_line.kontakt_nr

    return generate_output()