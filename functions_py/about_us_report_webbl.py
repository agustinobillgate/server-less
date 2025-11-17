#using conversion tools version: 1.0.0.119

# =================================================
# Rulita, 17-11-2025 | EFE395
# - New compile program 
# - Fixing Foreach first Guestresmember & Guestres 
# =================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Htparam, Archieve, Reservation, Res_line, Segment, Sourccod

payload_list_data, Payload_list = create_model("Payload_list", {"from_date":date, "to_date":date})

def about_us_report_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Guest, Htparam, Archieve, Reservation, Res_line, Segment])

    info_about_data = []
    from_date:date = None
    to_date:date = None
    billdate:date = None
    guest = htparam = archieve = reservation = res_line = segment = sourccod = None

    payload_list = info_about = guestres = guestresmember = None

    info_about_data, Info_about = create_model("Info_about", {"resno":string, "reslinnr":int, "res_name":string, "guest_name":string, "adult_pax":int, "child_pax":int, "compli_pax":int, "arr_date":string, "dept_date":string, "book_source":string, "segment":string, "source_info":string})

    Guestres = create_buffer("Guestres",Guest)
    Guestresmember = create_buffer("Guestresmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal info_about_data, from_date, to_date, billdate, guest, htparam, archieve, reservation, res_line, segment, sourccod
        nonlocal guestres, guestresmember


        nonlocal payload_list, info_about, guestres, guestresmember
        nonlocal info_about_data

        return {"info-about": info_about_data}

    def create_report():

        nonlocal info_about_data, from_date, to_date, billdate, guest, htparam, archieve, reservation, res_line, segment, sourccod
        nonlocal guestres, guestresmember


        nonlocal payload_list, info_about, guestres, guestresmember
        nonlocal info_about_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 51)]})

        if htparam:
            billdate = htparam.fdate

        res_line_obj_list = {}
        res_line = Res_line()
        archieve = Archieve()
        reservation = Reservation()
        guestresmember = Guest()
        guestres = Guest()

        # Rulita, 17-11-2025
        # Fixing Foreach first Guestresmember & Guestres compile program 
        for res_line.resnr, res_line.reslinnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.ankunft, res_line.abreise, res_line._recid, archieve.char, archieve._recid, reservation.segmentcode, reservation.resart, reservation._recid, guestresmember.name, guestresmember._recid, guestresmember.vorname1, guestresmember.anrede1, guestres.name, guestres._recid, guestres.vorname1, guestres.anrede1 in db_session.query( 
            Res_line.resnr, Res_line.reslinnr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.ankunft, Res_line.abreise, Res_line._recid, Archieve.char, Archieve._recid, Reservation.segmentcode, Reservation.resart, Reservation._recid, Guestresmember.name, Guestresmember._recid, Guestresmember.vorname1, Guestresmember.anrede1, Guestres.name, Guestres._recid, Guestres.vorname1, Guestres.anrede1).join(
                Archieve,(Archieve.key == ("about-us-info").lower()) & (Archieve.num1 == Res_line.resnr) & (Archieve.num2 == Res_line.reslinnr) & (Archieve.num3 == Res_line.gastnrmember) & (trim(Archieve.char[inc_value(0)]) != "") & (Archieve.char[inc_value(0)] != None)).join(
                    Reservation,(Reservation.resnr == Res_line.resnr)).join(
                        Guestresmember,(Guestresmember.gastnr == Res_line.gastnrmember)).join(
                            Guestres,(Guestres.gastnr == Res_line.gastnr)).filter(
                                (Res_line.ankunft <= to_date) & (Res_line.abreise > from_date)).order_by(Res_line.ankunft, Guestres.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
            info_about = Info_about()
            info_about_data.append(info_about)

            info_about.resno = to_string(res_line.resnr) + "/" + to_string(res_line.reslinnr)
            info_about.reslinnr = res_line.reslinnr
            info_about.res_name = guestres.name
            info_about.guest_name = guestresmember.name + ", " + guestresmember.vorname1 + " " + guestresmember.anrede1
            info_about.adult_pax = res_line.erwachs
            info_about.child_pax = res_line.kind1 + res_line.kind2
            info_about.compli_pax = res_line.gratis
            info_about.arr_date = to_string(res_line.ankunft, "99/99/99")
            info_about.dept_date = to_string(res_line.abreise, "99/99/99")

            if Sourccod:
                info_about.book_source = Sourccod.bezeich
            else:
                info_about.book_source = ""

            if segment:
                info_about.segment = segment.bezeich
            else:
                info_about.segment = ""

            if archieve.char[0] == None:
                info_about.source_info = ""
            else:
                info_about.source_info = archieve.char[0]

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        from_date = payload_list.from_date
        to_date = payload_list.to_date


        create_report()

    return generate_output()