from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_vipnrbl import get_vipnrbl
from models import Guest, Guestseg, Htparam, Zimkateg, Res_line, Reservation, Segment, Nation

def pickup_listbl(pvilanguage:int, disp_pickup:bool, check_ftd:bool, fdate:date, frdate:date, tdate:date):
    ci_date = None
    pickup_list_list = []
    vipnr1:int = 0
    vipnr2:int = 0
    vipnr3:int = 0
    vipnr4:int = 0
    vipnr5:int = 0
    vipnr6:int = 0
    vipnr7:int = 0
    vipnr8:int = 0
    vipnr9:int = 0
    vip_code:str = ""
    nat_str:str = ""
    lvcarea:str = "availability"
    stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    guest = guestseg = htparam = zimkateg = res_line = reservation = segment = nation = None

    pickup_list = gmember = gsegbuff = None

    pickup_list_list, Pickup_list = create_model("Pickup_list", {"gastnr":int, "gastnrmember":int, "resnr":int, "reslinnr":int, "zinr":str, "name":str, "vip":str, "segmentcode":int, "ankunft":date, "arrtime":str, "flight1":str, "eta":str, "abreise":date, "flight2":str, "etd":str, "zimmeranz":int, "kurzbez":str, "erwachs":int, "kind1":int, "gratis":int, "statstr":str, "arrangemment":str, "zipreis":decimal, "bemerk":str, "resname":str, "adresse":str, "wohnort":str, "nat1":str, "groupname":str, "betrieb_gastmem":int})

    Gmember = Guest
    Gsegbuff = Guestseg

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, pickup_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_list
        return {"ci_date": ci_date, "pickup-list": pickup_list_list}

    def disp_pickup():

        nonlocal ci_date, pickup_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_list

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == fdate) &  (Res_line.zimmer_wunsch.op("~")(".*pickup.*"))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == res_line.gastnrmember) &  (Guestseg.reihenfolge == 1)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()

            gmember = db_session.query(Gmember).filter(
                    (Gmember.gastnr == res_line.gastnrmember)).first()
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                    (Gsegbuff.gastnr == res_line.gastnrmember) &  ((Gsegbuff.segmentcode == vipnr1) |  (Gsegbuff.segmentcode == vipnr2) |  (Gsegbuff.segmentcode == vipnr3) |  (Gsegbuff.segmentcode == vipnr4) |  (Gsegbuff.segmentcode == vipnr5) |  (Gsegbuff.segmentcode == vipnr6) |  (Gsegbuff.segmentcode == vipnr7) |  (Gsegbuff.segmentcode == vipnr8) |  (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == gsegbuff.segmentcode)).first()
                vip_code = segment.bezeich
            nat_str = ""

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == gmember.nation1)).first()

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_list.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = guestseg.segmentcode
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statStr = stat_list[res_line.resstatus - 1]
            pickup_list.arrangemment = res_line.arrangement
            pickup_list.resname = guest.name
            pickup_list.adresse = gmember.adresse1 + ", " + gmember.adresse2
            pickup_list.wohnort = gmember.wohnort + " " + gmember.plz
            pickup_list.nat1 = nat_str
            pickup_list.groupname = reservation.groupname

    def disp_drop():

        nonlocal ci_date, pickup_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_list

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag <= 1) &  (Res_line.abreise == fdate) &  (Res_line.zimmer_wunsch.op("~")(".*drop_passanger.*"))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == res_line.gastnrmember) &  (Guestseg.reihenfolge == 1)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()

            gmember = db_session.query(Gmember).filter(
                    (Gmember.gastnr == res_line.gastnrmember)).first()
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                    (Gsegbuff.gastnr == res_line.gastnrmember) &  ((Gsegbuff.segmentcode == vipnr1) |  (Gsegbuff.segmentcode == vipnr2) |  (Gsegbuff.segmentcode == vipnr3) |  (Gsegbuff.segmentcode == vipnr4) |  (Gsegbuff.segmentcode == vipnr5) |  (Gsegbuff.segmentcode == vipnr6) |  (Gsegbuff.segmentcode == vipnr7) |  (Gsegbuff.segmentcode == vipnr8) |  (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == gsegbuff.segmentcode)).first()
                vip_code = segment.bezeich
            nat_str = ""

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == gmember.nation1)).first()

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_list.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = guestseg.segmentcode
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statStr = stat_list[res_line.resstatus - 1]
            pickup_list.arrangemment = res_line.arrangement
            pickup_list.resname = guest.name
            pickup_list.adresse = gmember.adresse1 + ", " + gmember.adresse2
            pickup_list.wohnort = gmember.wohnort + " " + gmember.plz
            pickup_list.nat1 = nat_str
            pickup_list.groupname = reservation.groupname

    def disp_pickup1():

        nonlocal ci_date, pickup_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_list

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft >= frdate) &  (Res_line.ankunft <= tdate) &  (Res_line.zimmer_wunsch.op("~")(".*pickup.*"))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == res_line.gastnrmember) &  (Guestseg.reihenfolge == 1)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()

            gmember = db_session.query(Gmember).filter(
                    (Gmember.gastnr == res_line.gastnrmember)).first()
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                    (Gsegbuff.gastnr == res_line.gastnrmember) &  ((Gsegbuff.segmentcode == vipnr1) |  (Gsegbuff.segmentcode == vipnr2) |  (Gsegbuff.segmentcode == vipnr3) |  (Gsegbuff.segmentcode == vipnr4) |  (Gsegbuff.segmentcode == vipnr5) |  (Gsegbuff.segmentcode == vipnr6) |  (Gsegbuff.segmentcode == vipnr7) |  (Gsegbuff.segmentcode == vipnr8) |  (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == gsegbuff.segmentcode)).first()
                vip_code = segment.bezeich
            nat_str = ""

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == gmember.nation1)).first()

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_list.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = guestseg.segmentcode
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statStr = stat_list[res_line.resstatus - 1]
            pickup_list.arrangemment = res_line.arrangement
            pickup_list.resname = guest.name
            pickup_list.adresse = gmember.adresse1 + ", " + gmember.adresse2
            pickup_list.wohnort = gmember.wohnort + " " + gmember.plz
            pickup_list.nat1 = nat_str
            pickup_list.groupname = reservation.groupname

    def disp_drop1():

        nonlocal ci_date, pickup_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_list

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag <= 1) &  (Res_line.abreise >= frdate) &  (Res_line.abreise <= tdate) &  (Res_line.zimmer_wunsch.op("~")(".*drop_passanger.*"))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == res_line.gastnrmember) &  (Guestseg.reihenfolge == 1)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()

            gmember = db_session.query(Gmember).filter(
                    (Gmember.gastnr == res_line.gastnrmember)).first()
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                    (Gsegbuff.gastnr == res_line.gastnrmember) &  ((Gsegbuff.segmentcode == vipnr1) |  (Gsegbuff.segmentcode == vipnr2) |  (Gsegbuff.segmentcode == vipnr3) |  (Gsegbuff.segmentcode == vipnr4) |  (Gsegbuff.segmentcode == vipnr5) |  (Gsegbuff.segmentcode == vipnr6) |  (Gsegbuff.segmentcode == vipnr7) |  (Gsegbuff.segmentcode == vipnr8) |  (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == gsegbuff.segmentcode)).first()
                vip_code = segment.bezeich
            nat_str = ""

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == gmember.nation1)).first()

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_list.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = guestseg.segmentcode
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statStr = stat_list[res_line.resstatus - 1]
            pickup_list.arrangemment = res_line.arrangement
            pickup_list.resname = guest.name
            pickup_list.adresse = gmember.adresse1 + ", " + gmember.adresse2
            pickup_list.wohnort = gmember.wohnort + " " + gmember.plz
            pickup_list.nat1 = nat_str
            pickup_list.groupname = reservation.groupname


    stat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    stat_list[1] = translateExtended ("6 PM", lvcarea, "")
    stat_list[2] = translateExtended ("Tentative", lvcarea, "")
    stat_list[3] = translateExtended ("WaitList", lvcarea, "")
    stat_list[4] = translateExtended ("OralConfirm", lvcarea, "")
    stat_list[5] = translateExtended ("Inhouse", lvcarea, "")
    stat_list[6] = ""
    stat_list[7] = translateExtended ("Departed", lvcarea, "")
    stat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    stat_list[9] = translateExtended ("NoShow", lvcarea, "")
    stat_list[10] = translateExtended ("ShareRes", lvcarea, "")
    stat_list[11] = ""
    stat_list[12] = translateExtended ("RmSharer", lvcarea, "")
    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 297)).first()

    if htparam.finteger != 0:
        stat_list[1] = to_string(htparam.finteger) + " " + translateExtended ("PM", lvcarea, "")

    if check_ftd == False:

        if disp_pickup:
            disp_pickup()

        elif not disp_pickup:
            disp_drop()

    elif check_ftd :

        if disp_pickup:
            disp_pickup1()

        elif not disp_pickup:
            disp_drop1()

    return generate_output()