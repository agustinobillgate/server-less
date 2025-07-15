#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_vipnrbl import get_vipnrbl
from sqlalchemy import func
from models import Guest, Guestseg, Htparam, Zimkateg, Res_line, Reservation, Segment, Nation

def pickup_listbl(pvilanguage:int, disp_pickup:bool, check_ftd:bool, fdate:date, frdate:date, tdate:date):

    prepare_cache ([Guest, Guestseg, Htparam, Zimkateg, Reservation, Segment, Nation])

    ci_date = None
    pickup_list_data = []
    vipnr1:int = 0
    vipnr2:int = 0
    vipnr3:int = 0
    vipnr4:int = 0
    vipnr5:int = 0
    vipnr6:int = 0
    vipnr7:int = 0
    vipnr8:int = 0
    vipnr9:int = 0
    vip_code:string = ""
    nat_str:string = ""
    lvcarea:string = "availability"
    stat_list:List[string] = create_empty_list(13,"")
    guest = guestseg = htparam = zimkateg = res_line = reservation = segment = nation = None

    pickup_list = gmember = gsegbuff = None

    pickup_list_data, Pickup_list = create_model("Pickup_list", {"gastnr":int, "gastnrmember":int, "resnr":int, "reslinnr":int, "zinr":string, "name":string, "vip":string, "segmentcode":int, "ankunft":date, "arrtime":string, "flight1":string, "eta":string, "abreise":date, "flight2":string, "etd":string, "zimmeranz":int, "kurzbez":string, "erwachs":int, "kind1":int, "gratis":int, "statstr":string, "arrangemment":string, "zipreis":Decimal, "bemerk":string, "resname":string, "adresse":string, "wohnort":string, "nat1":string, "groupname":string, "betrieb_gastmem":int})

    Gmember = create_buffer("Gmember",Guest)
    Gsegbuff = create_buffer("Gsegbuff",Guestseg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, pickup_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal pvilanguage, disp_pickup, check_ftd, fdate, frdate, tdate
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_data

        return {"ci_date": ci_date, "pickup-list": pickup_list_data}

    def disp_pickup():

        nonlocal ci_date, pickup_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal pvilanguage, disp_pickup, check_ftd, fdate, frdate, tdate
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_data

        tmp_segm:int = 0

        res_line_obj_list = {}
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == fdate) & (matches(Res_line.zimmer_wunsch,("*pickup*")))).order_by(to_int(func.substring(Res_line.flight_nr, 6, 5))).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, res_line.gastnrmember)],"reihenfolge": [(eq, 1)]})

            if guestseg:
                tmp_segm = guestseg.segmentcode
            else:
                tmp_segm = 0

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                     (Gsegbuff.gastnr == res_line.gastnrmember) & ((Gsegbuff.segmentcode == vipnr1) | (Gsegbuff.segmentcode == vipnr2) | (Gsegbuff.segmentcode == vipnr3) | (Gsegbuff.segmentcode == vipnr4) | (Gsegbuff.segmentcode == vipnr5) | (Gsegbuff.segmentcode == vipnr6) | (Gsegbuff.segmentcode == vipnr7) | (Gsegbuff.segmentcode == vipnr8) | (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = get_cache (Segment, {"segmentcode": [(eq, gsegbuff.segmentcode)]})
                vip_code = segment.bezeich
            nat_str = ""

            nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_data.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = tmp_segm
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statstr = stat_list[res_line.resstatus - 1]
            pickup_list.arrangemment = res_line.arrangement
            pickup_list.resname = guest.name
            pickup_list.adresse = gmember.adresse1 + ", " + gmember.adresse2
            pickup_list.wohnort = gmember.wohnort + " " + gmember.plz
            pickup_list.nat1 = nat_str
            pickup_list.groupname = reservation.groupname


    def disp_drop():

        nonlocal ci_date, pickup_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal pvilanguage, disp_pickup, check_ftd, fdate, frdate, tdate
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_data

        tmp_segm_drop:int = 0

        res_line_obj_list = {}
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.active_flag <= 1) & (Res_line.abreise == fdate) & (matches(Res_line.zimmer_wunsch,("*drop-passanger*")))).order_by(to_int(func.substring(Res_line.flight_nr, 17, 5))).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, res_line.gastnrmember)],"reihenfolge": [(eq, 1)]})

            if guestseg:
                tmp_segm_drop = guestseg.segmentcode
            else:
                tmp_segm_drop = 0

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                     (Gsegbuff.gastnr == res_line.gastnrmember) & ((Gsegbuff.segmentcode == vipnr1) | (Gsegbuff.segmentcode == vipnr2) | (Gsegbuff.segmentcode == vipnr3) | (Gsegbuff.segmentcode == vipnr4) | (Gsegbuff.segmentcode == vipnr5) | (Gsegbuff.segmentcode == vipnr6) | (Gsegbuff.segmentcode == vipnr7) | (Gsegbuff.segmentcode == vipnr8) | (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = get_cache (Segment, {"segmentcode": [(eq, gsegbuff.segmentcode)]})
                vip_code = segment.bezeich
            nat_str = ""

            nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_data.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = tmp_segm_drop
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statstr = stat_list[res_line.resstatus - 1]
            pickup_list.arrangemment = res_line.arrangement
            pickup_list.resname = guest.name
            pickup_list.adresse = gmember.adresse1 + ", " + gmember.adresse2
            pickup_list.wohnort = gmember.wohnort + " " + gmember.plz
            pickup_list.nat1 = nat_str
            pickup_list.groupname = reservation.groupname


    def disp_pickup1():

        nonlocal ci_date, pickup_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal pvilanguage, disp_pickup, check_ftd, fdate, frdate, tdate
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_data

        tmp_segm1:int = 0

        res_line_obj_list = {}
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft >= frdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.zimmer_wunsch,("*pickup*")))).order_by(to_int(func.substring(Res_line.flight_nr, 6, 5))).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, res_line.gastnrmember)],"reihenfolge": [(eq, 1)]})

            if guestseg:
                tmp_segm1 = guestseg.segmentcode
            else:
                tmp_segm1 = 0

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                     (Gsegbuff.gastnr == res_line.gastnrmember) & ((Gsegbuff.segmentcode == vipnr1) | (Gsegbuff.segmentcode == vipnr2) | (Gsegbuff.segmentcode == vipnr3) | (Gsegbuff.segmentcode == vipnr4) | (Gsegbuff.segmentcode == vipnr5) | (Gsegbuff.segmentcode == vipnr6) | (Gsegbuff.segmentcode == vipnr7) | (Gsegbuff.segmentcode == vipnr8) | (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = get_cache (Segment, {"segmentcode": [(eq, gsegbuff.segmentcode)]})
                vip_code = segment.bezeich
            nat_str = ""

            nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_data.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = tmp_segm1
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statstr = stat_list[res_line.resstatus - 1]
            pickup_list.arrangemment = res_line.arrangement
            pickup_list.resname = guest.name
            pickup_list.adresse = gmember.adresse1 + ", " + gmember.adresse2
            pickup_list.wohnort = gmember.wohnort + " " + gmember.plz
            pickup_list.nat1 = nat_str
            pickup_list.groupname = reservation.groupname


    def disp_drop1():

        nonlocal ci_date, pickup_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_code, nat_str, lvcarea, stat_list, guest, guestseg, htparam, zimkateg, res_line, reservation, segment, nation
        nonlocal pvilanguage, disp_pickup, check_ftd, fdate, frdate, tdate
        nonlocal gmember, gsegbuff


        nonlocal pickup_list, gmember, gsegbuff
        nonlocal pickup_list_data

        tmp_segm1_drop:int = 0

        res_line_obj_list = {}
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.active_flag <= 1) & (Res_line.abreise >= frdate) & (Res_line.abreise <= tdate) & (matches(Res_line.zimmer_wunsch,("*drop-passanger*")))).order_by(to_int(func.substring(Res_line.flight_nr, 17, 5))).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, res_line.gastnrmember)],"reihenfolge": [(eq, 1)]})

            if guestseg:
                tmp_segm1_drop = guestseg.segmentcode
            else:
                tmp_segm1_drop = 0

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            vip_code = ""

            gsegbuff = db_session.query(Gsegbuff).filter(
                     (Gsegbuff.gastnr == res_line.gastnrmember) & ((Gsegbuff.segmentcode == vipnr1) | (Gsegbuff.segmentcode == vipnr2) | (Gsegbuff.segmentcode == vipnr3) | (Gsegbuff.segmentcode == vipnr4) | (Gsegbuff.segmentcode == vipnr5) | (Gsegbuff.segmentcode == vipnr6) | (Gsegbuff.segmentcode == vipnr7) | (Gsegbuff.segmentcode == vipnr8) | (Gsegbuff.segmentcode == vipnr9))).first()

            if gsegbuff:

                segment = get_cache (Segment, {"segmentcode": [(eq, gsegbuff.segmentcode)]})
                vip_code = segment.bezeich
            nat_str = ""

            nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

            if nation:
                nat_str = nation.bezeich
            pickup_list = Pickup_list()
            pickup_list_data.append(pickup_list)

            buffer_copy(res_line, pickup_list)
            pickup_list.vip = vip_code
            pickup_list.segmentcode = tmp_segm1_drop
            pickup_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
            pickup_list.flight1 = substring(res_line.flight_nr, 0, 6)
            pickup_list.eta = substring(res_line.flight_nr, 6, 5)
            pickup_list.flight2 = substring(res_line.flight_nr, 11, 6)
            pickup_list.etd = substring(res_line.flight_nr, 17, 5)
            pickup_list.kurzbez = zimkateg.kurzbez
            pickup_list.statstr = stat_list[res_line.resstatus - 1]
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 297)]})

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