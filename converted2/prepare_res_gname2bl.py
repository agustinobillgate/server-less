#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Master, Htparam, Reservation, Guest, Zimkateg, Zimmer, Nation, Res_line

def prepare_res_gname2bl(resnr:int):

    prepare_cache ([Htparam, Reservation, Guest, Zimkateg, Zimmer, Nation, Res_line])

    if_flag = False
    ci_date = None
    default_nat = ""
    htparam_feldtyp = 0
    htparam_flogical = False
    master_exist = False
    htparam_flogical2 = False
    troom = ""
    grprline_list_data = []
    s_list_data = []
    zimkateg_list_data = []
    resline_list_data = []
    zimmer_list_data = []
    nation1_data = []
    master = htparam = reservation = guest = zimkateg = zimmer = nation = res_line = None

    nation1 = grprline_list = s_list = zimkateg_list = resline_list = zimmer_list = None

    nation1_data, Nation1 = create_model("Nation1", {"kurzbez":string})
    grprline_list_data, Grprline_list = create_model("Grprline_list", {"s_recid":int, "zinr":string})
    s_list_data, S_list = create_model("S_list", {"res_recid":int, "resstatus":int, "active_flag":int, "flag":int, "karteityp":int, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "old_zinr":string, "name":string, "nat":string, "land":string, "zinr":string, "eta":string, "etd":string, "flight1":string, "flight2":string, "rmcat":string, "ankunft":date, "abreise":date, "zipreis":Decimal, "bemerk":string})
    zimkateg_list_data, Zimkateg_list = create_model("Zimkateg_list", {"zikatnr":int, "kurzbez":string})
    resline_list_data, Resline_list = create_model("Resline_list", {"resnr":int, "reslinnr":int, "setup":int, "zikatnr":int, "active_flag":int, "resstatus":int, "zimmeranz":int, "ankunft":date, "abreise":date, "rec_id":int})
    zimmer_list_data, Zimmer_list = create_model("Zimmer_list", {"zinr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal if_flag, ci_date, default_nat, htparam_feldtyp, htparam_flogical, master_exist, htparam_flogical2, troom, grprline_list_data, s_list_data, zimkateg_list_data, resline_list_data, zimmer_list_data, nation1_data, master, htparam, reservation, guest, zimkateg, zimmer, nation, res_line
        nonlocal resnr


        nonlocal nation1, grprline_list, s_list, zimkateg_list, resline_list, zimmer_list
        nonlocal nation1_data, grprline_list_data, s_list_data, zimkateg_list_data, resline_list_data, zimmer_list_data

        return {"if_flag": if_flag, "ci_date": ci_date, "default_nat": default_nat, "htparam_feldtyp": htparam_feldtyp, "htparam_flogical": htparam_flogical, "master_exist": master_exist, "htparam_flogical2": htparam_flogical2, "troom": troom, "grprline-list": grprline_list_data, "s-list": s_list_data, "zimkateg-list": zimkateg_list_data, "resline-list": resline_list_data, "zimmer-list": zimmer_list_data, "nation1": nation1_data}

    def create_list():

        nonlocal if_flag, ci_date, default_nat, htparam_feldtyp, htparam_flogical, master_exist, htparam_flogical2, troom, grprline_list_data, s_list_data, zimkateg_list_data, resline_list_data, zimmer_list_data, nation1_data, master, htparam, reservation, guest, zimkateg, zimmer, nation, res_line
        nonlocal resnr


        nonlocal nation1, grprline_list, s_list, zimkateg_list, resline_list, zimmer_list
        nonlocal nation1_data, grprline_list_data, s_list_data, zimkateg_list_data, resline_list_data, zimmer_list_data


        grprline_list_data.clear()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.active_flag < 2) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikat)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.res_recid = res_line._recid
            s_list.name = guest.name + ", " + guest.vorname1 + ", " +\
                    guest.anrede1
            s_list.name = trim(s_list.name)
            s_list.flag = res_line.gastnrmember
            s_list.nat = guest.nation1
            s_list.land = guest.land
            s_list.zinr = res_line.zinr
            s_list.old_zinr = res_line.zinr
            s_list.flight1 = substring(res_line.flight_nr, 0, 6)
            s_list.eta = substring(res_line.flight_nr, 6, 4)
            s_list.flight2 = substring(res_line.flight_nr, 11, 6)
            s_list.etd = substring(res_line.flight_nr, 17, 4)
            s_list.zimmeranz = res_line.zimmeranz
            s_list.resstatus = res_line.resstatus
            s_list.active_flag = res_line.active_flag
            s_list.karteityp = guest.karteityp
            s_list.erwachs = res_line.erwachs
            s_list.rmcat = zimkateg.kurzbez
            s_list.ankunft = res_line.ankunft
            s_list.abreise = res_line.abreise
            s_list.kind1 = res_line.kind1
            s_list.kind2 = res_line.kind2
            s_list.zipreis =  to_decimal(res_line.zipreis)
            s_list.bemerk = res_line.bemerk


            resline_list = Resline_list()
            resline_list_data.append(resline_list)

            resline_list.resnr = res_line.resnr
            resline_list.reslinnr = res_line.reslinnr
            resline_list.setup = res_line.setup
            resline_list.zikatnr = res_line.zikatnr
            resline_list.active_flag = res_line.active_flag
            resline_list.resstatus = res_line.resstatus
            resline_list.zimmeranz = res_line.zimmeranz
            resline_list.ankunft = res_line.ankunft
            resline_list.abreise = res_line.abreise
            resline_list.rec_id = res_line._recid

            if s_list.nat == "":
                s_list.nat = default_nat
            grprline_list = Grprline_list()
            grprline_list_data.append(grprline_list)

            grprline_list.s_recid = s_list.res_recid
            grprline_list.zinr = res_line.zinr

    master = get_cache (Master, {"resnr": [(eq, resnr)]})

    if master:
        master_exist = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 76)]})
    htparam_flogical2 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 961)]})
    htparam_feldtyp = htparam.feldtyp
    htparam_flogical = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})
    if_flag = htparam.flogical

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if reservation:

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

        if guest:

            if guest.karteityp >= 1 and guest.land != "":

                htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

                if htparam:

                    if htparam.fchar != "" and htparam.fchar != guest.land:
                        default_nat = guest.land


    create_list()

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        zimkateg_list = Zimkateg_list()
        zimkateg_list_data.append(zimkateg_list)

        zimkateg_list.zikatnr = zimkateg.zikatnr
        zimkateg_list.kurzbez = zimkateg.kurzbez

    for zimmer in db_session.query(Zimmer).filter(
             not_ (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        zimmer_list = Zimmer_list()
        zimmer_list_data.append(zimmer_list)

        zimmer_list.zinr = zimmer.zinr

    zimmer = db_session.query(Zimmer).order_by(Zimmer._recid.desc()).first()
    troom = zimmer.zinr

    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        nation1 = Nation1()
        nation1_data.append(nation1)

        nation1.kurzbez = nation.kurzbez

    return generate_output()