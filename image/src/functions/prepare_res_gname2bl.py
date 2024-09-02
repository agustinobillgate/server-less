from functions.additional_functions import *
import decimal
from datetime import date
from models import Master, Htparam, Reservation, Guest, Zimkateg, Zimmer, Nation, Res_line

def prepare_res_gname2bl(resnr:int):
    if_flag = False
    ci_date = None
    default_nat = ""
    htparam_feldtyp = 0
    htparam_flogical = False
    master_exist = False
    htparam_flogical2 = False
    troom = ""
    grprline_list_list = []
    s_list_list = []
    zimkateg_list_list = []
    resline_list_list = []
    zimmer_list_list = []
    nation1_list = []
    master = htparam = reservation = guest = zimkateg = zimmer = nation = res_line = None

    nation1 = grprline_list = s_list = zimkateg_list = resline_list = zimmer_list = None

    nation1_list, Nation1 = create_model("Nation1", {"kurzbez":str})
    grprline_list_list, Grprline_list = create_model("Grprline_list", {"s_recid":int, "zinr":str})
    s_list_list, S_list = create_model("S_list", {"res_recid":int, "resstatus":int, "active_flag":int, "flag":int, "karteityp":int, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "old_zinr":str, "name":str, "nat":str, "land":str, "zinr":str, "eta":str, "etd":str, "flight1":str, "flight2":str, "rmcat":str, "ankunft":date, "abreise":date, "zipreis":decimal, "bemerk":str})
    zimkateg_list_list, Zimkateg_list = create_model("Zimkateg_list", {"zikatnr":int, "kurzbez":str})
    resline_list_list, Resline_list = create_model("Resline_list", {"resnr":int, "reslinnr":int, "setup":int, "zikatnr":int, "active_flag":int, "resstatus":int, "zimmeranz":int, "ankunft":date, "abreise":date, "rec_id":int})
    zimmer_list_list, Zimmer_list = create_model("Zimmer_list", {"zinr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal if_flag, ci_date, default_nat, htparam_feldtyp, htparam_flogical, master_exist, htparam_flogical2, troom, grprline_list_list, s_list_list, zimkateg_list_list, resline_list_list, zimmer_list_list, nation1_list, master, htparam, reservation, guest, zimkateg, zimmer, nation, res_line


        nonlocal nation1, grprline_list, s_list, zimkateg_list, resline_list, zimmer_list
        nonlocal nation1_list, grprline_list_list, s_list_list, zimkateg_list_list, resline_list_list, zimmer_list_list
        return {"if_flag": if_flag, "ci_date": ci_date, "default_nat": default_nat, "htparam_feldtyp": htparam_feldtyp, "htparam_flogical": htparam_flogical, "master_exist": master_exist, "htparam_flogical2": htparam_flogical2, "troom": troom, "grprline-list": grprline_list_list, "s-list": s_list_list, "zimkateg-list": zimkateg_list_list, "resline-list": resline_list_list, "zimmer-list": zimmer_list_list, "nation1": nation1_list}

    def create_list():

        nonlocal if_flag, ci_date, default_nat, htparam_feldtyp, htparam_flogical, master_exist, htparam_flogical2, troom, grprline_list_list, s_list_list, zimkateg_list_list, resline_list_list, zimmer_list_list, nation1_list, master, htparam, reservation, guest, zimkateg, zimmer, nation, res_line


        nonlocal nation1, grprline_list, s_list, zimkateg_list, resline_list, zimmer_list
        nonlocal nation1_list, grprline_list_list, s_list_list, zimkateg_list_list, resline_list_list, zimmer_list_list


        grprline_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.active_flag < 2) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikat)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()
            s_list = S_list()
            s_list_list.append(s_list)

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
            s_list.zipreis = res_line.zipreis
            s_list.bemerk = res_line.bemerk


            resline_list = Resline_list()
            resline_list_list.append(resline_list)

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
            grprline_list_list.append(grprline_list)

            grprline_list.s_recid = s_list.res_recid
            grprline_list.zinr = res_line.zinr


    master = db_session.query(Master).filter(
            (Master.resnr == resnr)).first()

    if master:
        master_exist = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 76)).first()
    htparam_flogical2 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 961)).first()
    htparam_feldtyp = htparam.feldtyp
    htparam_flogical = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 307)).first()
    if_flag = htparam.flogical

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == reservation.gastnr)).first()

    if guest.karteityp >= 1 and guest.land != "":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 153)).first()

        if htparam.fchar != "" and guest.land != htparam.fchar:
            default_nat = guest.land
    create_list()

    for zimkateg in db_session.query(Zimkateg).all():
        zimkateg_list = Zimkateg_list()
        zimkateg_list_list.append(zimkateg_list)

        zimkateg_list.zikatnr = zimkateg.zikatnr
        zimkateg_list.kurzbez = zimkateg.kurzbez

    for zimmer in db_session.query(Zimmer).filter(
            (not Zimmer.sleeping)).all():
        zimmer_list = Zimmer_list()
        zimmer_list_list.append(zimmer_list)

        zimmer_list.zinr = zimmer.zinr

    zimmer = db_session.query(Zimmer).first()
    troom = zimmer.zinr

    for nation in db_session.query(Nation).all():
        nation1 = Nation1()
        nation1_list.append(nation1)

        nation1.kurzbez = nation.kurzbez

    return generate_output()