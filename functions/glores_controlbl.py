#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Guest, Res_line, Kontline, Reservation, Zimkateg

def glores_controlbl(pvilanguage:int, del_flag:bool, from_date:date, to_date:date, from_name:string, to_name:string):

    prepare_cache ([Bediener, Guest, Res_line, Kontline, Zimkateg])

    glores_control_list_data = []
    datum:date = None
    usr_init:string = ""
    i:int = 0
    count:int = 0
    currresnr:int = 0
    anz1:List[int] = create_empty_list(31,0)
    anz2:List[int] = create_empty_list(31,0)
    t_anz0:List[int] = create_empty_list(31,0)
    t_anz1:List[int] = create_empty_list(31,0)
    t_anz2:List[int] = create_empty_list(31,0)
    avail_allotm:List[int] = create_empty_list(31,0)
    overbook:List[int] = create_empty_list(31,0)
    wday:List[string] = ["SU", "MO", "TU", "WE", "TH", "FR", "SA", "SU"]
    lvcarea:string = "pickup-list"
    bediener = guest = res_line = kontline = reservation = zimkateg = None

    glores_control_list = k_list = usr = None

    glores_control_list_data, Glores_control_list = create_model("Glores_control_list", {"datum":date, "gastnr":int, "firma":string, "kontcode":string, "zikatnr":int, "kurzbez":string, "erwachs":int, "kind1":int, "gloanz":int, "gresanz":int, "resanz":int, "resnrstr":string})
    k_list_data, K_list = create_model("K_list", {"gastnr":int, "bediener_nr":int, "kontcode":string, "ankunft":date, "zikatnr":int, "argt":string, "zimmeranz":[int,31], "erwachs":int, "kind1":int, "ruecktage":int, "overbooking":int, "abreise":date, "useridanlage":string, "resdate":date, "bemerk":string})

    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal glores_control_list_data, datum, usr_init, i, count, currresnr, anz1, anz2, t_anz0, t_anz1, t_anz2, avail_allotm, overbook, wday, lvcarea, bediener, guest, res_line, kontline, reservation, zimkateg
        nonlocal pvilanguage, del_flag, from_date, to_date, from_name, to_name
        nonlocal usr


        nonlocal glores_control_list, k_list, usr
        nonlocal glores_control_list_data, k_list_data

        return {"glores-control-list": glores_control_list_data}

    def create_alist():

        nonlocal glores_control_list_data, datum, usr_init, count, currresnr, anz1, anz2, t_anz0, t_anz1, t_anz2, avail_allotm, overbook, wday, lvcarea, bediener, guest, res_line, kontline, reservation, zimkateg
        nonlocal pvilanguage, del_flag, from_date, to_date, from_name, to_name
        nonlocal usr


        nonlocal glores_control_list, k_list, usr
        nonlocal glores_control_list_data, k_list_data

        curr_code:string = ""
        d:date = None
        d1:date = None
        d2:date = None
        i:int = 0

        kontline_obj_list = {}
        kontline = Kontline()
        guest = Guest()
        for kontline.kontcode, kontline.bediener_nr, kontline.ankunft, kontline.zikatnr, kontline.arrangement, kontline.erwachs, kontline.kind1, kontline.ruecktage, kontline.overbooking, kontline.abreise, kontline.useridanlage, kontline.resdat, kontline.bemerk, kontline.gastnr, kontline.zimmeranz, kontline._recid, guest.gastnr, guest.name, guest._recid in db_session.query(Kontline.kontcode, Kontline.bediener_nr, Kontline.ankunft, Kontline.zikatnr, Kontline.arrangement, Kontline.erwachs, Kontline.kind1, Kontline.ruecktage, Kontline.overbooking, Kontline.abreise, Kontline.useridanlage, Kontline.resdat, Kontline.bemerk, Kontline.gastnr, Kontline.zimmeranz, Kontline._recid, Guest.gastnr, Guest.name, Guest._recid).join(Guest,(Guest.gastnr == Kontline.gastnr) & (Guest.name >= (from_name).lower()) & (Guest.name <= (to_name).lower())).filter(
                 (Kontline.betriebsnr == 1) & (not_ (Kontline.ankunft > to_date)) & (not_ (Kontline.abreise < from_date)) & (Kontline.kontstatus == 1)).order_by(Guest.name, Kontline.kontcode, Kontline.ankunft).all():
            if kontline_obj_list.get(kontline._recid):
                continue
            else:
                kontline_obj_list[kontline._recid] = True

            if curr_code != kontline.kontcode:

                usr = get_cache (Bediener, {"nr": [(eq, kontline.bediener_nr)]})
                curr_code = kontline.kontcode
                k_list = K_list()
                k_list_data.append(k_list)

                k_list.gastnr = guest.gastnr
                k_list.kontcode = curr_code
                k_list.ankunft = kontline.ankunft
                k_list.zikatnr = kontline.zikatnr
                k_list.argt = kontline.arrangement
                k_list.erwachs = kontline.erwachs
                k_list.kind1 = kontline.kind1
                k_list.ruecktage = kontline.ruecktage
                k_list.overbooking = kontline.overbooking
                k_list.abreise = kontline.abreise
                k_list.useridanlage = kontline.useridanlage
                k_list.resdat = kontline.resdat
                k_list.bemerk = kontline.bemerk

                if usr:
                    k_list.bediener_nr = usr.nr
            else:
                k_list.abreise = kontline.abreise

            if from_date > kontline.ankunft:
                d1 = from_date
            else:
                d1 = kontline.ankunft

            if to_date < kontline.abreise:
                d2 = to_date
            else:
                d2 = kontline.abreise
            i = (d1 - from_date).days
            for d in date_range(d1,d2) :
                glores_control_list = Glores_control_list()
                glores_control_list_data.append(glores_control_list)


                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, k_list.zikatnr)]})
                glores_control_list.datum = d
                glores_control_list.gastnr = kontline.gastnr
                glores_control_list.firma = guest.name
                glores_control_list.kontcode = kontline.kontcode
                glores_control_list.zikatnr = kontline.zikatnr
                glores_control_list.gloanz = kontline.zimmeranz
                glores_control_list.erwachs = kontline.erwachs
                glores_control_list.kind1 = kontline.kind1

                if zimkateg:
                    glores_control_list.kurzbez = zimkateg.kurzbez


                i = i + 1

                if d >= kontline.ankunft and d <= kontline.abreise:
                    k_list.zimmeranz[i - 1] = kontline.zimmeranz


    k_list_data.clear()
    glores_control_list_data.clear()
    create_alist()

    for k_list in query(k_list_data, sort_by=[("ankunft",False)]):

        guest = get_cache (Guest, {"gastnr": [(eq, k_list.gastnr)]})

        if not guest:

            return generate_output()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnr == k_list.gastnr) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < from_date)) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.kontignr == 0)).order_by(Res_line.resnr).all():
            for datum in date_range(from_date,to_date) :

                if res_line.ankunft <= datum and res_line.abreise > datum:

                    glores_control_list = query(glores_control_list_data, filters=(lambda glores_control_list: glores_control_list.datum == datum and glores_control_list.gastnr == res_line.gastnr and glores_control_list.zikatnr == res_line.zikatnr and glores_control_list.erwachs >= res_line.erwachs), first=True)

                    if not glores_control_list:

                        glores_control_list = query(glores_control_list_data, filters=(lambda glores_control_list: glores_control_list.datum == datum and glores_control_list.gastnr == res_line.gastnr and glores_control_list.zikatnr == res_line.zikatnr), first=True)

                    if glores_control_list:
                        glores_control_list.resanz = glores_control_list.resanz + res_line.zimmeranz

                    if currresnr != res_line.resnr:
                        currresnr = res_line.resnr
                        glores_control_list.resnrstr = glores_control_list.resnrstr +\
                                trim(to_string(res_line.resnr, ">>>>>>>9")) + "; "

        res_line_obj_list = {}
        res_line = Res_line()
        kontline = Kontline()
        for res_line.abreise, res_line.gastnr, res_line.zikatnr, res_line.erwachs, res_line.zimmeranz, res_line.resnr, res_line.ankunft, res_line._recid, kontline.kontcode, kontline.bediener_nr, kontline.ankunft, kontline.zikatnr, kontline.arrangement, kontline.erwachs, kontline.kind1, kontline.ruecktage, kontline.overbooking, kontline.abreise, kontline.useridanlage, kontline.resdat, kontline.bemerk, kontline.gastnr, kontline.zimmeranz, kontline._recid in db_session.query(Res_line.abreise, Res_line.gastnr, Res_line.zikatnr, Res_line.erwachs, Res_line.zimmeranz, Res_line.resnr, Res_line.ankunft, Res_line._recid, Kontline.kontcode, Kontline.bediener_nr, Kontline.ankunft, Kontline.zikatnr, Kontline.arrangement, Kontline.erwachs, Kontline.kind1, Kontline.ruecktage, Kontline.overbooking, Kontline.abreise, Kontline.useridanlage, Kontline.resdat, Kontline.bemerk, Kontline.gastnr, Kontline.zimmeranz, Kontline._recid).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) & (Kontline.kontcode == k_list.kontcode) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.gastnr == k_list.gastnr) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < from_date)) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.kontignr < 0)).order_by(Res_line.ankunft, Res_line.abreise, Res_line.resnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
            for datum in date_range(from_date,to_date) :

                if res_line.ankunft <= datum and res_line.abreise > datum:

                    glores_control_list = query(glores_control_list_data, filters=(lambda glores_control_list: glores_control_list.datum == datum and glores_control_list.gastnr == res_line.gastnr and glores_control_list.kontcode == k_list.kontcode), first=True)

                    if glores_control_list:
                        glores_control_list.gresanz = glores_control_list.gresanz + res_line.zimmeranz

    return generate_output()