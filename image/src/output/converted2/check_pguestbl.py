from functions.additional_functions import *
import decimal
from datetime import date
from functions.read_nationbl import read_nationbl
from functions.htpchar import htpchar
from functions.htpdate import htpdate
from models import Nation, Htparam, Outorder, Res_line, Reservation, Guest, Guestseg, Segment, Sourccod

def check_pguestbl(pvilanguage:int):
    msg_str = ""
    tot_room = 0
    ext_char = ""
    bill_date = None
    t_nation_list = []
    c_list_list = []
    lvcarea:str = "check-puest"
    nation = htparam = outorder = res_line = reservation = guest = guestseg = segment = sourccod = None

    c_list = t_nation = None

    c_list_list, C_list = create_model("C_list", {"gastnr":int, "resstatus":int, "res_recid":int, "zipreis":decimal, "zinr":str, "name":str, "pax":int, "com":int, "abreise":date, "land":str, "nat":str, "nat2":str, "resart":int, "segm":int, "segmentcode":int, "ch":str, "error_code":int, "nation_ok":bool, "land_ok":bool, "grpflag":bool, "cardtype":int, "resnr":int, "reslinnr":int, "rgastnr":int, "email":str, "segm_descr":str, "resart_descr":str})
    t_nation_list, T_nation = create_model_like(Nation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, tot_room, ext_char, bill_date, t_nation_list, c_list_list, lvcarea, nation, htparam, outorder, res_line, reservation, guest, guestseg, segment, sourccod
        nonlocal pvilanguage


        nonlocal c_list, t_nation
        nonlocal c_list_list, t_nation_list
        return {"msg_str": msg_str, "tot_room": tot_room, "ext_char": ext_char, "bill_date": bill_date, "t-nation": t_nation_list, "c-list": c_list_list}

    def check_it():

        nonlocal msg_str, tot_room, ext_char, bill_date, t_nation_list, c_list_list, lvcarea, nation, htparam, outorder, res_line, reservation, guest, guestseg, segment, sourccod
        nonlocal pvilanguage


        nonlocal c_list, t_nation
        nonlocal c_list_list, t_nation_list

        segmentcode:int = 0

        for outorder in db_session.query(Outorder).filter(
                 (Outorder.gespende == bill_date)).order_by(Outorder.zinr).all():
            c_list = C_list()
            c_list_list.append(c_list)

            c_list.zinr = outorder.zinr
            c_list.name = outorder.gespgrund
            c_list.abreise = outorder.gespende
            c_list.resstatus = 14
            c_list.land = "-"
            c_list.nat = "-"

            if outorder.betriebsnr > 1:
                c_list.resstatus = 15

        res_line = db_session.query(Res_line).filter(
                 (Res_line.zinr == "") & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).first()
        while None != res_line:
            msg_str = msg_str + "&W" + translateExtended ("Mal Reservation found! ResNo:", lvcarea, "") + " " + to_string(res_line.resnr) + chr(10) + translateExtended ("Guest Name:", lvcarea, "") + " " + res_line.name + chr(10) + translateExtended ("Status inhouse but RmNo not assigend; set back to GUARANTEED.", lvcarea, "")
            res_line.resstatus = 1
            res_line.active_flag = 0

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.zinr == "") & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).filter(Res_line._recid > curr_recid).first()

        res_line = db_session.query(Res_line).filter(
                 (Res_line.zinr != "") & (((Res_line.resstatus == 6) & (Res_line.active_flag == 0)) | ((Res_line.resstatus == 1) & (Res_line.active_flag == 1)))).first()
        while None != res_line:
            res_line.resstatus = 6
            res_line.active_flag = 1

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.zinr != "") & (((Res_line.resstatus == 6) & (Res_line.active_flag == 0)) | ((Res_line.resstatus == 1) & (Res_line.active_flag == 1)))).filter(Res_line._recid > curr_recid).first()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr).all():
            tot_room = tot_room + 1
            segmentcode = 0

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr)).first()

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == guest.gastnr) & (Guestseg.reihenfolge == 1)).first()

            if guestseg:
                segmentcode = guestseg.segmentcode
            c_list = C_list()
            c_list_list.append(c_list)

            c_list.gastnr = res_line.gastnrmember
            c_list.resstatus = res_line.resstatus
            c_list.res_recid = res_line._recid
            c_list.zipreis =  to_decimal(res_line.zipreis)
            c_list.zinr = res_line.zinr
            c_list.name = res_line.name
            c_list.pax = res_line.erwachs
            c_list.com = res_line.gratis
            c_list.abreise = res_line.abreise
            c_list.land = guest.land
            c_list.nat = guest.nation1
            c_list.nat2 = guest.nation2
            c_list.resart = reservation.resart
            c_list.segmentcode = segmentcode
            c_list.segm = reservation.segmentcode
            c_list.cardtype = guest.karteityp
            c_list.resnr = res_line.resnr
            c_list.reslinnr = res_line.reslinnr
            c_list.rgastnr = reservation.gastnr
            c_list.grpflag = reservation.grpflag
            c_list.email = guest.email_adr

            if c_list.nat != "":

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == c_list.nat)).first()
                c_list.nation_ok = None ! == nation

            if c_list.land != "":

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == c_list.land)).first()
                c_list.land_ok = None ! == nation

            if c_list.segm != 0:

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == c_list.segm)).first()

                if segment:
                    c_list.segm_descr = segment.bezeich

            if c_list.resart != 0:

                sourccod = db_session.query(Sourccod).filter(
                         (Sourccod.source_code == c_list.resart)).first()

                if Sourccod:
                    c_list.resart_descr = Sourccod.bezeich

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 276)).first()

    if htparam.fchar != "":
        t_nation_list = get_output(read_nationbl(0, htparam.fchar, ""))

    t_nation = query(t_nation_list, first=True)

    if not t_nation:

        return generate_output()
    ext_char = get_output(htpchar(148))
    bill_date = get_output(htpdate(110))
    check_it()

    return generate_output()