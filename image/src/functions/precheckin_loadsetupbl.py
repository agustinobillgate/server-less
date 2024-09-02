from functions.additional_functions import *
import decimal
from functions.read_queasybl import read_queasybl
from functions.nation_adminbl import nation_adminbl
from functions.htpchar import htpchar
from functions.read_nationbl import read_nationbl
from functions.read_nation1bl import read_nation1bl
from datetime import date
from models import Queasy, Nation, Htparam, Paramtext, Res_line, Zimmer, Bresline

def precheckin_loadsetupbl(icase:int):
    pci_setup_list = []
    htl_name:str = ""
    country:str = ""
    f_char:str = ""
    def_nation:int = 0
    do_it:bool = False
    ci_date:date = None
    tot_room:int = 0
    occ_room:int = 0
    occ_perc:decimal = 0
    occ1:decimal = None
    occ2:decimal = 0
    p_223:bool = False
    queasy = nation = htparam = paramtext = res_line = zimmer = bresline = None

    pci_setup = t_queasy = t_nation1 = t_nation = t_subnation = bresline = None

    pci_setup_list, Pci_setup = create_model("Pci_setup", {"number1":int, "number2":int, "descr":str, "setupvalue":str, "setupflag":bool, "price":decimal, "remarks":str})
    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_nation1_list, T_nation1 = create_model_like(Nation)
    t_nation_list, T_nation = create_model_like(Nation, {"marksegm":str, "rec_id":int})
    t_subnation_list, T_subnation = create_model_like(Nation)

    Bresline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pci_setup_list, htl_name, country, f_char, def_nation, do_it, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, p_223, queasy, nation, htparam, paramtext, res_line, zimmer, bresline
        nonlocal bresline


        nonlocal pci_setup, t_queasy, t_nation1, t_nation, t_subnation, bresline
        nonlocal pci_setup_list, t_queasy_list, t_nation1_list, t_nation_list, t_subnation_list
        return {"pci-setup": pci_setup_list}

    def decode_string(in_str:str):

        nonlocal pci_setup_list, htl_name, country, f_char, def_nation, do_it, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, p_223, queasy, nation, htparam, paramtext, res_line, zimmer, bresline
        nonlocal bresline


        nonlocal pci_setup, t_queasy, t_nation1, t_nation, t_subnation, bresline
        nonlocal pci_setup_list, t_queasy_list, t_nation1_list, t_nation_list, t_subnation_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    if icase == 1:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 216)).all():
            pci_setup = Pci_setup()
            pci_setup_list.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char1
            pci_setup.setupflag = queasy.logi1
            pci_setup.setupvalue = queasy.char3
            pci_setup.price = queasy.deci1
            pci_setup.remarks = queasy.char2

    elif icase == 2:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 216) &  (Queasy.logi1)).all():
            pci_setup = Pci_setup()
            pci_setup_list.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char1
            pci_setup.setupflag = queasy.logi1
            pci_setup.setupvalue = queasy.char3
            pci_setup.price = queasy.deci1
            pci_setup.remarks = queasy.char2


    t_queasy_list = get_output(read_queasybl(3, 27, None, ""))

    for t_queasy in query(t_queasy_list):
        pci_setup = Pci_setup()
        pci_setup_list.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 0
        pci_setup.descr = "TYPE OF DOCUMENT"
        pci_setup.setupflag = True
        pci_setup.setupvalue = t_queasy.char1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 153)).first()

    if htparam.fchar != "":
        country = htparam.fchar
        pci_setup = Pci_setup()
        pci_setup_list.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 1
        pci_setup.descr = "DEFAULT country CODE"
        pci_setup.setupflag = True
        pci_setup.setupvalue = country

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 240)).first()

    if paramtext and paramtext.ptexte != "":
        htl_name = decode_string(paramtext.ptexte)
        pci_setup = Pci_setup()
        pci_setup_list.append(pci_setup)

        pci_setup.number1 = 99
        pci_setup.number2 = 1
        pci_setup.descr = "HOTEL NAME"
        pci_setup.setupflag = True
        pci_setup.setupvalue = htl_name


    t_nation_list, t_nation1_list = get_output(nation_adminbl(0))

    for t_nation in query(t_nation_list):
        pci_setup = Pci_setup()
        pci_setup_list.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 2
        pci_setup.descr = t_nation.kurzbez
        pci_setup.setupflag = True
        pci_setup.setupvalue = entry(0, t_nation.bezeich, ";")


    t_nation1._list.clear()
    t_nation._list.clear()
    f_char = get_output(htpchar(153))
    t_nation1_list = get_output(read_nationbl(0, f_char, ""))

    t_nation1 = query(t_nation1_list, first=True)
    def_nation = t_nation1.nationnr
    t_subnation_list = get_output(read_nation1bl(2, def_nation, None, None, "", "", None))

    for t_subnation in query(t_subnation_list):
        pci_setup = Pci_setup()
        pci_setup_list.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 3
        pci_setup.descr = t_subnation.kurzbez
        pci_setup.setupflag = True
        pci_setup.setupvalue = t_subnation.bezeich

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    pci_setup = Pci_setup()
    pci_setup_list.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 4
    pci_setup.descr = "SYSTEM DATE"
    pci_setup.setupflag = True
    pci_setup.setupvalue = to_string(htparam.fdate, "99/99/9999")


    pci_setup = Pci_setup()
    pci_setup_list.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 5
    pci_setup.descr = "LICENSE WA/SMS GATEWAY"
    pci_setup.setupflag = True
    pci_setup.setupvalue = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    zimmer = db_session.query(Zimmer).filter(
            (Zimmer.sleeping)).first()
    while None != zimmer:
        tot_room = tot_room + 1

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).first()

    for bresline in db_session.query(Bresline).filter(
            (Bresline.active_flag <= 1) &  (Bresline.resstatus <= 6) &  (Bresline.resstatus != 3) &  (Bresline.resstatus != 4) &  (Bresline.resstatus != 12) &  (Bresline.resstatus != 11) &  (Bresline.resstatus != 13) &  (Bresline.ankunft == ci_date) &  (Bresline.l_zuordnung[2] == 0)).all():
        do_it = True

        if bresline.zinr != "":

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == bresline.zinr)).first()
            do_it = zimmer.sleeping

        if do_it:
            occ_room = occ_room + bresline.zimmeranz
    occ1 = occ_room / tot_room * 100


    pci_setup = Pci_setup()
    pci_setup_list.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 6
    pci_setup.descr = "OCCUPANCY TODAY"
    pci_setup.setupflag = True
    pci_setup.setupvalue = ""
    pci_setup.price = occ1


    pass
    pci_setup = Pci_setup()
    pci_setup_list.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 7
    pci_setup.descr = "SERVER TIME"
    pci_setup.setupflag = True
    pci_setup.setupvalue = to_string(get_current_time_in_seconds(), "HH:MM:SS")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()
    p_223 = htparam.flogical
    pci_setup = Pci_setup()
    pci_setup_list.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 8
    pci_setup.descr = "LICENSE MEMBERSHIP"
    pci_setup.setupflag = p_223
    pci_setup.setupvalue = ""


    pci_setup = Pci_setup()
    pci_setup_list.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 9
    pci_setup.descr = "SERVER DATE"
    pci_setup.setupflag = True
    pci_setup.setupvalue = to_string(get_current_date())

    return generate_output()