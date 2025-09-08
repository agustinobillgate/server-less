#using conversion tools version: 1.0.0.117

# ======================================================
# Rulita, 08-09-2025 
# Issue : Fixing cl_list sort by nr & s_list sort by nat
# ======================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Zimmer, Paramtext, Guest, Zimkateg, Reservation, Res_line, Guestseg, Nation, Genstat

def longshort_stay_btn_webbl(sorttype:int, to_date:date, from_date:date, long_stay:int):

    prepare_cache ([Htparam, Zimmer, Paramtext, Guest, Zimkateg, Res_line, Guestseg, Nation])

    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    tot_avail = 0
    inactive = 0
    cl_list_data = []
    s_list_data = []
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    htparam = zimmer = paramtext = guest = zimkateg = reservation = res_line = guestseg = nation = genstat = None

    str_list = cl_list = s_list = setup_list = None

    str_list_data, Str_list = create_model("Str_list", {"flag":int, "long_stay":bool, "line1":string, "line2":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "resstatus":string, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "bemerk":string, "ratecode":string, "lodging":Decimal})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int})
    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, cl_list_data, s_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam, zimmer, paramtext, guest, zimkateg, reservation, res_line, guestseg, nation, genstat
        nonlocal sorttype, to_date, from_date, long_stay


        nonlocal str_list, cl_list, s_list, setup_list
        nonlocal str_list_data, cl_list_data, s_list_data, setup_list_data

        # Rulita | Fixing cl_list sort by nr & s_list sort by nat
        cl_sorted = sorted(list(cl_list_data), key=lambda x: x.nr)
        s_sorted = sorted(list(s_list_data), key=lambda x: x.nat)

        return {"tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "tot_avail": tot_avail, "inactive": inactive, "cl-list": cl_sorted, "s-list": s_sorted}

    def bed_setup():

        nonlocal tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, cl_list_data, s_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam, zimmer, paramtext, guest, zimkateg, reservation, res_line, guestseg, nation, genstat
        nonlocal sorttype, to_date, from_date, long_stay


        nonlocal str_list, cl_list, s_list, setup_list
        nonlocal str_list_data, cl_list_data, s_list_data, setup_list_data


        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.setup != 0)).order_by(Zimmer._recid).all():

            paramtext = db_session.query(Paramtext).filter(
                     ((Paramtext.txtnr - 9200) == zimmer.setup)).first()

            if paramtext:

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == (zimmer.setup + 1)), first=True)

                if not setup_list:
                    setup_list = Setup_list()
                    setup_list_data.append(setup_list)

                    setup_list.nr = zimmer.setup + 1
                    setup_list.char = substring(paramtext.notes, 0, 1)


    def longstay_list():

        nonlocal tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, cl_list_data, s_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam, zimmer, paramtext, guest, zimkateg, reservation, res_line, guestseg, nation, genstat
        nonlocal sorttype, to_date, from_date, long_stay


        nonlocal str_list, cl_list, s_list, setup_list
        nonlocal str_list_data, cl_list_data, s_list_data, setup_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        gmember = None
        num_date:int = 0
        s:string = ""
        Gmember =  create_buffer("Gmember",Guest)
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0
        inactive = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1
        num_date = (to_date - from_date).days
        tot_avail = tot_avail * (num_date + 1)

        res_line_obj_list = {}
        for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                 (Res_line.active_flag <= 2) & (Res_line.resstatus <= 8) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & ((Res_line.abreise - Res_line.ankunft) >= long_stay) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.erwachs > 0)).order_by(Res_line.ankunft, Res_line.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            nr = nr + 1
            vip_flag = ""

            for guestseg in db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == gmember.gastnr)).order_by(Guestseg._recid).all():

                if guestseg.segmentcode == vipnr1:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr2:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr3:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr4:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr5:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr6:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr7:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr8:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr9:
                    vip_flag = "VIP"
                    break
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.nr = nr
            cl_list.rmcat = zimkateg.kurzbez + setup_list.char
            cl_list.kurzbez = zimkateg.kurzbez
            cl_list.bezeich = zimkateg.bezeichnung
            cl_list.nat = gmember.nation1
            cl_list.resnr = res_line.resnr
            cl_list.vip = vip_flag
            cl_list.name = res_line.name
            cl_list.rmno = res_line.zinr
            cl_list.arrive = res_line.ankunft
            cl_list.depart = res_line.abreise
            cl_list.resstatus = to_string(res_line.resstatus)
            cl_list.qty = res_line.zimmeranz
            cl_list.a = res_line.erwachs
            cl_list.c = res_line.kind1 + res_line.kind2
            cl_list.co = res_line.gratis
            cl_list.argt = res_line.arrangement
            cl_list.flight = substring(res_line.flight_nr, 11, 6)
            cl_list.etd = substring(res_line.flight_nr, 17, 5)
            cl_list.company = guest.name + ", " + guest.vorname1 +\
                    " " + guest.anrede1 + guest.anredefirma

            if cl_list.nat == "":
                cl_list.nat = "?"
            for i in range(1,length(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                    cl_list.bemerk = cl_list.bemerk + " "
                else:
                    cl_list.bemerk = cl_list.bemerk + substring(res_line.bemerk, i - 1, 1)
            cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

            if cl_list.nat == "":
                cl_list.nat = "?"
            else:

                nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                if nation:
                    cl_list.nation = nation.bezeich

            if res_line.resstatus != 13:

                if zimmer and zimmer.sleeping:
                    tot_rm = tot_rm + 1
                else:
                    inactive = inactive + 1
            tot_a = tot_a + res_line.erwachs
            tot_c = tot_c + res_line.kind1 + res_line.kind2
            tot_co = tot_co + res_line.gratis

            if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
                s = substring(res_line.zimmer_wunsch, (get_index(res_line.zimmer_wunsch, "$CODE$") + 6) - 1)
                cl_list.ratecode = trim(entry(0, s, ";"))

            genstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)],"res_int[0]": [(eq, res_line.reslinnr)]})

            if genstat:
                pass
            cl_list.lodging =  to_decimal(res_line.zipreis)

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

    def shortstay_list():

        nonlocal tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, cl_list_data, s_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam, zimmer, paramtext, guest, zimkateg, reservation, res_line, guestseg, nation, genstat
        nonlocal sorttype, to_date, from_date, long_stay


        nonlocal str_list, cl_list, s_list, setup_list
        nonlocal str_list_data, cl_list_data, s_list_data, setup_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        num_date:int = 0
        s:string = ""
        gmember = None
        Gmember =  create_buffer("Gmember",Guest)
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0
        inactive = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1
        num_date = (to_date - from_date).days
        tot_avail = tot_avail * (num_date + 1)

        res_line_obj_list = {}
        for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                 (Res_line.active_flag <= 2) & (Res_line.resstatus <= 8) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & ((Res_line.abreise - Res_line.ankunft) < long_stay) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.erwachs > 0)).order_by(Res_line.ankunft, Res_line.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            nr = nr + 1
            vip_flag = ""

            for guestseg in db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == gmember.gastnr)).order_by(Guestseg._recid).all():

                if guestseg.segmentcode == vipnr1:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr2:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr3:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr4:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr5:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr6:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr7:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr8:
                    vip_flag = "VIP"
                    break

                elif guestseg.segmentcode == vipnr9:
                    vip_flag = "VIP"
                    break
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.nr = nr
            cl_list.rmcat = zimkateg.kurzbez + setup_list.char
            cl_list.kurzbez = zimkateg.kurzbez
            cl_list.bezeich = zimkateg.bezeichnung
            cl_list.nat = gmember.nation1
            cl_list.resnr = res_line.resnr
            cl_list.vip = vip_flag
            cl_list.name = res_line.name
            cl_list.rmno = res_line.zinr
            cl_list.arrive = res_line.ankunft
            cl_list.depart = res_line.abreise
            cl_list.resstatus = to_string(res_line.resstatus)
            cl_list.qty = res_line.zimmeranz
            cl_list.a = res_line.erwachs
            cl_list.c = res_line.kind1 + res_line.kind2
            cl_list.co = res_line.gratis
            cl_list.argt = res_line.arrangement
            cl_list.flight = substring(res_line.flight_nr, 11, 6)
            cl_list.etd = substring(res_line.flight_nr, 17, 5)
            cl_list.company = guest.name + ", " + guest.vorname1 +\
                    " " + guest.anrede1 + guest.anredefirma

            if cl_list.nat == "":
                cl_list.nat = "?"
            for i in range(1,length(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                    cl_list.bemerk = cl_list.bemerk + " "
                else:
                    cl_list.bemerk = cl_list.bemerk + substring(res_line.bemerk, i - 1, 1)
            cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

            if cl_list.nat == "":
                cl_list.nat = "?"
            else:

                nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                if nation:
                    cl_list.nation = nation.bezeich

            if res_line.resstatus != 13:

                if zimmer and zimmer.sleeping:
                    tot_rm = tot_rm + 1
                else:
                    inactive = inactive + 1
            tot_a = tot_a + res_line.erwachs
            tot_c = tot_c + res_line.kind1 + res_line.kind2
            tot_co = tot_co + res_line.gratis

            if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
                s = substring(res_line.zimmer_wunsch, (get_index(res_line.zimmer_wunsch, "$CODE$") + 6) - 1)
                cl_list.ratecode = trim(entry(0, s, ";"))
            cl_list.lodging =  to_decimal(res_line.zipreis)

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger
    bed_setup()

    if sorttype == 1:
        longstay_list()
    else:
        shortstay_list()

    return generate_output()