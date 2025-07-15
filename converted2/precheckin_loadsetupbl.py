#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_queasybl import read_queasybl
from functions.nation_adminbl import nation_adminbl
from functions.htpchar import htpchar
from functions.read_nationbl import read_nationbl
from functions.read_nation1bl import read_nation1bl
from datetime import date
from models import Queasy, Nation, Htparam, Paramtext, Res_line, Zimmer

def precheckin_loadsetupbl(icase:int):

    prepare_cache ([Queasy, Htparam, Paramtext, Res_line])

    pci_setup_data = []
    htl_name:string = ""
    country:string = ""
    f_char:string = ""
    def_nation:int = 0
    do_it:bool = False
    ci_date:date = None
    tot_room:int = 0
    occ_room:int = 0
    occ_perc:Decimal = to_decimal("0.0")
    occ1:Decimal = None
    occ2:Decimal = to_decimal("0.0")
    p_223:bool = False
    queasy = nation = htparam = paramtext = res_line = zimmer = None

    pci_setup = t_queasy = t_nation1 = t_nation = t_subnation = bresline = None

    pci_setup_data, Pci_setup = create_model("Pci_setup", {"number1":int, "number2":int, "descr":string, "setupvalue":string, "setupflag":bool, "price":Decimal, "remarks":string})
    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_nation1_data, T_nation1 = create_model_like(Nation)
    t_nation_data, T_nation = create_model_like(Nation, {"marksegm":string, "rec_id":int})
    t_subnation_data, T_subnation = create_model_like(Nation)

    Bresline = create_buffer("Bresline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pci_setup_data, htl_name, country, f_char, def_nation, do_it, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, p_223, queasy, nation, htparam, paramtext, res_line, zimmer
        nonlocal icase
        nonlocal bresline


        nonlocal pci_setup, t_queasy, t_nation1, t_nation, t_subnation, bresline
        nonlocal pci_setup_data, t_queasy_data, t_nation1_data, t_nation_data, t_subnation_data

        return {"pci-setup": pci_setup_data}

    def decode_string(in_str:string):

        nonlocal pci_setup_data, htl_name, country, f_char, def_nation, do_it, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, p_223, queasy, nation, htparam, paramtext, res_line, zimmer
        nonlocal icase
        nonlocal bresline


        nonlocal pci_setup, t_queasy, t_nation1, t_nation, t_subnation, bresline
        nonlocal pci_setup_data, t_queasy_data, t_nation1_data, t_nation_data, t_subnation_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    if icase == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216)).order_by(Queasy._recid).all():
            pci_setup = Pci_setup()
            pci_setup_data.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char1
            pci_setup.setupflag = queasy.logi1
            pci_setup.setupvalue = queasy.char3
            pci_setup.price =  to_decimal(queasy.deci1)
            pci_setup.remarks = queasy.char2

    elif icase == 2:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216) & (Queasy.logi1)).order_by(Queasy._recid).all():
            pci_setup = Pci_setup()
            pci_setup_data.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char1
            pci_setup.setupflag = queasy.logi1
            pci_setup.setupvalue = queasy.char3
            pci_setup.price =  to_decimal(queasy.deci1)
            pci_setup.remarks = queasy.char2


    t_queasy_data = get_output(read_queasybl(3, 27, None, ""))

    for t_queasy in query(t_queasy_data):
        pci_setup = Pci_setup()
        pci_setup_data.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 0
        pci_setup.descr = "TYPE OF DOCUMENT"
        pci_setup.setupflag = True
        pci_setup.setupvalue = t_queasy.char1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    if htparam.fchar != "":
        country = htparam.fchar
        pci_setup = Pci_setup()
        pci_setup_data.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 1
        pci_setup.descr = "DEFAULT country CODE"
        pci_setup.setupflag = True
        pci_setup.setupvalue = country

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 240)]})

    if paramtext and paramtext.ptexte != "":
        htl_name = decode_string(paramtext.ptexte)
        pci_setup = Pci_setup()
        pci_setup_data.append(pci_setup)

        pci_setup.number1 = 99
        pci_setup.number2 = 1
        pci_setup.descr = "HOTEL NAME"
        pci_setup.setupflag = True
        pci_setup.setupvalue = htl_name


    t_nation_data, t_nation1_data = get_output(nation_adminbl(0))

    for t_nation in query(t_nation_data, sort_by=[("entry(",False))]:
        pci_setup = Pci_setup()
        pci_setup_data.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 2
        pci_setup.descr = t_nation.kurzbez
        pci_setup.setupflag = True
        pci_setup.setupvalue = entry(0, t_nation.bezeich, ";")


    t_nation1_data.clear()
    t_nation_data.clear()
    f_char = get_output(htpchar(153))
    t_nation1_data = get_output(read_nationbl(0, f_char, ""))

    t_nation1 = query(t_nation1_data, first=True)
    def_nation = t_nation1.nationnr
    t_subnation_data = get_output(read_nation1bl(2, def_nation, None, None, "", "", None))

    for t_subnation in query(t_subnation_data, sort_by=[("bezeich",False)]):
        pci_setup = Pci_setup()
        pci_setup_data.append(pci_setup)

        pci_setup.number1 = 9
        pci_setup.number2 = 3
        pci_setup.descr = t_subnation.kurzbez
        pci_setup.setupflag = True
        pci_setup.setupvalue = t_subnation.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    pci_setup = Pci_setup()
    pci_setup_data.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 4
    pci_setup.descr = "SYSTEM DATE"
    pci_setup.setupflag = True
    pci_setup.setupvalue = to_string(htparam.fdate, "99/99/9999")


    pci_setup = Pci_setup()
    pci_setup_data.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 5
    pci_setup.descr = "LICENSE WA/SMS GATEWAY"
    pci_setup.setupflag = True
    pci_setup.setupvalue = ""

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    zimmer = db_session.query(Zimmer).filter(
             (Zimmer.sleeping)).first()
    while None != zimmer:
        tot_room = tot_room + 1

        curr_recid = zimmer._recid
        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.sleeping) & (Zimmer._recid > curr_recid)).first()

    for bresline in db_session.query(Bresline).filter(
             (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.ankunft == ci_date) & (Bresline.l_zuordnung[inc_value(2)] == 0)).order_by(Bresline._recid).all():
        do_it = True

        if bresline.zinr != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
            do_it = zimmer.sleeping

        if do_it:
            occ_room = occ_room + bresline.zimmeranz
    occ1 =  to_decimal(occ_room) / to_decimal(tot_room) * to_decimal("100")


    pci_setup = Pci_setup()
    pci_setup_data.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 6
    pci_setup.descr = "OCCUPANCY TODAY"
    pci_setup.setupflag = True
    pci_setup.setupvalue = ""
    pci_setup.price =  to_decimal(occ1)

    pci_setup = Pci_setup()
    pci_setup_data.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 7
    pci_setup.descr = "SERVER TIME"
    pci_setup.setupflag = True
    pci_setup.setupvalue = to_string(get_current_time_in_seconds(), "HH:MM:SS")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 223)]})
    p_223 = htparam.flogical
    pci_setup = Pci_setup()
    pci_setup_data.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 8
    pci_setup.descr = "LICENSE MEMBERSHIP"
    pci_setup.setupflag = p_223
    pci_setup.setupvalue = ""


    pci_setup = Pci_setup()
    pci_setup_data.append(pci_setup)

    pci_setup.number1 = 9
    pci_setup.number2 = 9
    pci_setup.descr = "SERVER DATE"
    pci_setup.setupflag = True
    pci_setup.setupvalue = to_string(get_current_date())

    return generate_output()