from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from sqlalchemy import func
from functions.ratecode_seek import ratecode_seek
from models import Res_line, Waehrung, Guest, Artikel, Queasy, Nation, Reservation, Kontline, Zimkateg, Htparam, Zimmer, Arrangement, Genstat, Exrate, Bill, Reslin_queasy, Guest_pr, Pricecod, Argt_line, Fixleist

reslin_list_list, Reslin_list = create_model_like(Res_line)

def closingscriptbl(reslin_list_list:[Reslin_list], pvilanguage:int):
    ausweis_nr2 = ""
    karteityp = 0
    msg_str = ""
    msg_warning = ""
    cl_list_list = []
    output_list_list = []
    exchg_rate:decimal = 1
    frate:decimal = to_decimal("0.0")
    post_it:bool = False
    total_rev:decimal = to_decimal("0.0")
    new_contrate:bool = False
    foreign_rate:bool = False
    price_decimal:int = 0
    fcost:decimal = to_decimal("0.0")
    tot_pax:int = 0
    tot_com:int = 0
    tot_rm:int = 0
    tot_rate:decimal = to_decimal("0.0")
    tot_lrate:decimal = to_decimal("0.0")
    tot_lodging:decimal = to_decimal("0.0")
    tot_bfast:decimal = to_decimal("0.0")
    tot_lunch:decimal = to_decimal("0.0")
    tot_dinner:decimal = to_decimal("0.0")
    tot_misc:decimal = to_decimal("0.0")
    tot_fix:decimal = to_decimal("0.0")
    ltot_rm:int = 0
    ltot_pax:int = 0
    ltot_rate:decimal = to_decimal("0.0")
    ltot_lodging:decimal = to_decimal("0.0")
    ltot_bfast:decimal = to_decimal("0.0")
    ltot_lunch:decimal = to_decimal("0.0")
    ltot_dinner:decimal = to_decimal("0.0")
    ltot_misc:decimal = to_decimal("0.0")
    ltot_fix:decimal = to_decimal("0.0")
    curr_zinr:str = ""
    curr_resnr:int = 0
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    fb_dept:int = 0
    argt_betrag:decimal = to_decimal("0.0")
    take_it:bool = False
    prcode:int = 0
    qty:int = 0
    r_qty:int = 0
    lodge_betrag:decimal = to_decimal("0.0")
    f_betrag:decimal = to_decimal("0.0")
    s:str = ""
    ct:str = ""
    contcode:str = ""
    vat:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    curr_zikatnr:int = 0
    co_date:date = None
    datum:date = None
    curr_date:date = None
    i:int = 0
    str:str = ""
    segm__purcode:int = 0
    vat1:decimal = to_decimal("0.0")
    service1:decimal = to_decimal("0.0")
    serv1:decimal = to_decimal("0.0")
    serv2:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    vat3:decimal = to_decimal("0.0")
    vat4:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    fact1:decimal = to_decimal("0.0")
    fact2:decimal = to_decimal("0.0")
    lvcarea:str = "rmrev-bdown"
    rstat_list:List[str] = create_empty_list(13,"")
    res_line = waehrung = guest = artikel = queasy = nation = reservation = kontline = zimkateg = htparam = zimmer = arrangement = genstat = exrate = bill = reslin_queasy = guest_pr = pricecod = argt_line = fixleist = None

    reslin_list = cl_list = output_list = waehrung1 = cc_list = member1 = rguest = artikel1 = queasy1 = nation1 = bres = None

    cl_list_list, Cl_list = create_model("Cl_list", {"zinr":str, "zipreis":decimal, "localrate":decimal, "lodging":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "fixcost":decimal, "t_rev":decimal, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":str, "rstatus":int, "argt":str, "currency":str, "ratecode":str, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":str, "ex_rate":str, "fix_rate":str, "fdate":date, "tdate":date, "datum":date, "dt_rate":str}, {"sleeping": True})
    output_list_list, Output_list = create_model("Output_list", {"ci":str, "co":str, "guest":str, "rmcat":str, "card":str, "grpname":str, "res_status":str, "night":str, "adult":str, "child1":str, "child2":str, "com":str, "rmqty":str, "rmno":str, "memo_zinr":str, "voucher":str, "argt":str, "allot":str, "ratecode":str, "rmrate":str, "currency":str, "bill_reciv":str, "purpose":str, "bill_instruct":str, "deposit":str, "pay1":str, "pay2":str, "contcode":str, "email_adr":str, "nat":str, "country":str, "restatus":int, "lzuordnung3":int})

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Cc_list = Cl_list
    cc_list_list = cl_list_list

    Member1 = create_buffer("Member1",Guest)
    Rguest = create_buffer("Rguest",Guest)
    Artikel1 = create_buffer("Artikel1",Artikel)
    Queasy1 = create_buffer("Queasy1",Queasy)
    Nation1 = create_buffer("Nation1",Nation)
    Bres = create_buffer("Bres",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_list, output_list_list, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal reslin_list_list, cl_list_list, output_list_list
        return {"ausweis_nr2": ausweis_nr2, "karteityp": karteityp, "msg_str": msg_str, "msg_warning": msg_warning, "cl-list": cl_list_list, "output-list": output_list_list}

    def cal_revenue():

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_list, output_list_list, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal reslin_list_list, cl_list_list, output_list_list


        cl_list_list.clear()

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 125)).first()
        bfast_art = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 126)).first()
        fb_dept = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 87)).first()
        curr_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 240)).first()
        foreign_rate = htparam.flogical

        if not foreign_rate:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 143)).first()
            foreign_rate = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 550)).first()

        if htparam.feldtyp == 4:
            new_contrate = htparam.flogical

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == bfast_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and bfast_art != 0:
            msg_str = translateExtended ("B'fast SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 227)).first()
        lunch_art = htparam.finteger

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == lunch_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and lunch_art != 0:
            msg_str = translateExtended ("Lunch SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 228)).first()
        dinner_art = htparam.finteger

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == dinner_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and dinner_art != 0:
            msg_str = translateExtended ("Dinner SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 229)).first()
        lundin_art = htparam.finteger

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == lundin_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and lundin_art != 0:
            msg_str = translateExtended ("HalfBoard SubGrp not yed defined (Grp 7)", lvcarea, "")

            return
        r_qty = 0
        lodge_betrag =  to_decimal("0")

        reslin_list = query(reslin_list_list, first=True)

        if reslin_list:

            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == reslin_list.zinr)).first()

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == reslin_list.arrangement)).first()

            if reslin_list.abreise > reslin_list.ankunft:
                co_date = reslin_list.abreise - timedelta(days=1)
            else:
                co_date = reslin_list.abreise
            for datum in date_range(reslin_list.ankunft,co_date) :

                if datum < curr_date:
                    read_genstat()
                else:
                    read_resline()


    def read_genstat():

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_list, output_list_list, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal reslin_list_list, cl_list_list, output_list_list

        i:int = 0
        n:int = 0

        genstat = db_session.query(Genstat).filter(
                 (Genstat.zinr != "") & (Genstat.datum == datum) & (Genstat.res_logic[inc_value(1)]) & (Genstat.resnr == reslin_list.resnr) & (Genstat.res_int[inc_value(0)] == reslin_list.reslinnr)).first()

        if genstat:

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()
            service =  to_decimal("0")
            vat =  to_decimal("0")
            serv1 =  to_decimal("0")
            vat1 =  to_decimal("0")
            vat2 =  to_decimal("0")
            fact1 =  to_decimal("0")


            serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

            waehrung1 = db_session.query(Waehrung1).filter(
                     (Waehrung1.waehrungsnr == reslin_list.betriebsnr)).first()

            if waehrung1:

                exrate = db_session.query(Exrate).filter(
                         (Exrate.datum == curr_date) & (Exrate.artnr == waehrung1.waehrungsnr)).first()

                if exrate:
                    exchg_rate =  to_decimal(exrate.betrag)

            if reslin_list.reserve_dec != 0:
                frate =  to_decimal(reslin_list.reserve_dec)
            else:
                frate =  to_decimal(exchg_rate)

            if genstat.zipreis != 0:
                r_qty = r_qty + 1

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == reslin_list.gastnrpay)).first()

            member1 = db_session.query(Member1).filter(
                     (Member1.gastnr == reslin_list.gastnrmember)).first()

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == reslin_list.resnr)).first()

            if reslin_list.l_zuordnung[0] != 0:
                curr_zikatnr = reslin_list.l_zuordnung[0]
            else:
                curr_zikatnr = reslin_list.zikatnr

            bill = db_session.query(Bill).filter(
                     (Bill.resnr == reslin_list.resnr) & (Bill.reslinnr == reslin_list.reslinnr) & (Bill.zinr == reslin_list.zinr)).first()

            if not bill:

                bill = db_session.query(Bill).filter(
                         (Bill.resnr == reslin_list.resnr) & (Bill.reslinnr == reslin_list.reslinnr)).first()

            if not bill:
                msg_str = translateExtended ("Bill not found: RmNo ", lvcarea, "") + reslin_list.zinr + " - " + reslin_list.name
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.res_recid = reslin_list._recid
            cl_list.zinr = genstat.zinr
            cl_list.rstatus = genstat.resstatus
            cl_list.sleeping = zimmer.sleeping
            cl_list.argt = genstat.argt
            cl_list.name = reslin_list.name
            cl_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2
            cl_list.com = genstat.gratis + genstat.kind3
            cl_list.ankunft = reslin_list.ankunft
            cl_list.abreise = reslin_list.abreise
            cl_list.zipreis =  to_decimal(genstat.zipreis)
            cl_list.localrate =  to_decimal(genstat.rateLocal)
            cl_list.rechnr = bill.rechnr
            cl_list.t_rev =  to_decimal(genstat.zipreis)
            cl_list.currency = waehrung1.wabkurz
            cl_list.lodging =  to_decimal(genstat.logis)
            cl_list.bfast =  to_decimal(genstat.res_deci[1]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.dinner =  to_decimal(genstat.res_deci[3]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.misc =  to_decimal(genstat.res_deci[4]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.fixcost =  to_decimal(genstat.res_deci[5]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.datum = datum

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 127)).first()

            if htparam.flogical:
                cl_list.lodging = to_decimal(round((cl_list.lodging * (1 + vat1 + vat2 + serv1)) , price_decimal))

            if re.match(r".*\$CODE\$.*",reslin_list.zimmer_wunsch, re.IGNORECASE):
                s = substring(reslin_list.zimmer_wunsch, (1 + get_index(reslin_list.zimmer_wunsch, "$CODE$") + 6) - 1)
                cl_list.ratecode = trim(entry(0, s, ";"))

            if frate == 1:
                cl_list.ex_rate = to_string(frate, " >>9.99")

            elif frate <= 999:
                cl_list.ex_rate = to_string(frate, " >>9.9999")

            elif frate <= 99999:
                cl_list.ex_rate = to_string(frate, ">>,>>9.99")
            else:
                cl_list.ex_rate = to_string(frate, ">,>>>,>>9")

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == reslin_list.resnr) & (Reslin_queasy.reslinnr == reslin_list.reslinnr) & (datum >= Reslin_queasy.date1) & (datum <= Reslin_queasy.date2)).first()

            if reslin_queasy:
                cl_list.fix_rate = "YES"
                cl_list.fdate = reslin_queasy.date1
                cl_list.tdate = reslin_queasy.date2


            else:
                cl_list.fix_rate = "NO"

            if cl_list.fdate != None:
                cl_list.dt_rate = to_string(cl_list.fdate, "99/99/99") + " - " + to_string(cl_list.tdate, "99/99/99")


            tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
            tot_lrate =  to_decimal(tot_lrate) + to_decimal(cl_list.localrate)

            if not reslin_list.adrflag:
                tot_pax = tot_pax + cl_list.pax
            else:
                ltot_pax = ltot_pax + cl_list.pax
            tot_com = tot_com + cl_list.com

            if reslin_list.adrflag:
                ltot_lodging =  to_decimal(ltot_lodging) + to_decimal(cl_list.lodging)
            else:
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(cl_list.lodging)
            lodge_betrag =  to_decimal(cl_list.lodging)

            if foreign_rate and price_decimal == 0 and not reslin_list.adrflag:

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 145)).first()

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,htparam.finteger + 1) :
                        n = n * 10
                    lodge_betrag = to_decimal(round(lodge_betrag / n , 0) * n)

            if curr_zinr != reslin_list.zinr or curr_resnr != reslin_list.resnr:

                if reslin_list.adrflag:
                    ltot_rm = ltot_rm + 1
                else:
                    tot_rm = tot_rm + 1
            curr_zinr = reslin_list.zinr


            curr_resnr = reslin_list.resnr


    def read_resline():

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_list, output_list_list, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal reslin_list_list, cl_list_list, output_list_list

        i:int = 0
        n:int = 0
        service =  to_decimal("0")
        vat =  to_decimal("0")
        serv1 =  to_decimal("0")
        vat1 =  to_decimal("0")
        vat2 =  to_decimal("0")
        fact1 =  to_decimal("0")

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()

        if artikel:
            serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

        waehrung1 = db_session.query(Waehrung1).filter(
                 (Waehrung1.waehrungsnr == reslin_list.betriebsnr)).first()

        if waehrung1:
            exchg_rate =  to_decimal(waehrung1.ankauf) / to_decimal(waehrung1.einheit)

        if reslin_list.reserve_dec != 0:
            frate =  to_decimal(reslin_list.reserve_dec)
        else:
            frate =  to_decimal(exchg_rate)

        if reslin_list.zipreis != 0:
            r_qty = r_qty + 1

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == reslin_list.gastnrpay)).first()

        member1 = db_session.query(Member1).filter(
                 (Member1.gastnr == reslin_list.gastnrmember)).first()

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == reslin_list.resnr)).first()

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        bill = db_session.query(Bill).filter(
                 (Bill.resnr == reslin_list.resnr) & (Bill.reslinnr == reslin_list.reslinnr) & (Bill.zinr == reslin_list.zinr)).first()

        if not bill:

            bill = db_session.query(Bill).filter(
                     (Bill.resnr == reslin_list.resnr) & (Bill.reslinnr == reslin_list.reslinnr)).first()

        if not bill:
            msg_warning = "&W" + translateExtended ("Bill not found: RmNo ", lvcarea, "") + reslin_list.zinr + " - " + reslin_list.name
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.res_recid = reslin_list._recid
        cl_list.zinr = reslin_list.zinr
        cl_list.rstatus = reslin_list.resstatus
        cl_list.argt = reslin_list.arrangement
        cl_list.name = reslin_list.name
        cl_list.pax = reslin_list.erwachs + reslin_list.kind1 + reslin_list.kind2
        cl_list.com = reslin_list.gratis + reslin_list.l_zuordnung[3]
        cl_list.ankunft = reslin_list.ankunft
        cl_list.abreise = reslin_list.abreise
        cl_list.currency = waehrung1.wabkurz
        cl_list.datum = datum

        if bill:
            cl_list.rechnr = bill.rechnr

        if zimmer:
            cl_list.sleeping = zimmer.sleeping

        if frate == 1:
            cl_list.ex_rate = to_string(frate, " >>9.99")

        elif frate <= 999:
            cl_list.ex_rate = to_string(frate, " >>9.9999")

        elif frate <= 99999:
            cl_list.ex_rate = to_string(frate, ">>,>>9.99")
        else:
            cl_list.ex_rate = to_string(frate, ">,>>>,>>9")

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == reslin_list.resnr) & (Reslin_queasy.reslinnr == reslin_list.reslinnr) & (datum >= Reslin_queasy.date1) & (datum <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            cl_list.fix_rate = "YES"
            cl_list.zipreis =  to_decimal(reslin_queasy.deci1)
            cl_list.localrate =  to_decimal(reslin_queasy.deci1) * to_decimal(frate)
            cl_list.t_rev =  to_decimal(reslin_queasy.deci1)
            cl_list.fdate = reslin_queasy.date1
            cl_list.tdate = reslin_queasy.date2


        else:
            cl_list.fix_rate = "NO"
            cl_list.zipreis =  to_decimal(reslin_list.zipreis)
            cl_list.localrate =  to_decimal(reslin_list.zipreis) * to_decimal(frate)
            cl_list.t_rev =  to_decimal(reslin_list.zipreis)

        if cl_list.fdate != None:
            cl_list.dt_rate = to_string(cl_list.fdate, "99/99/99") + "-" + to_string(cl_list.tdate, "99/99/99")


        tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
        tot_lrate =  to_decimal(tot_lrate) + to_decimal(cl_list.localrate)

        if not reslin_list.adrflag:
            tot_pax = tot_pax + cl_list.pax
        else:
            ltot_pax = ltot_pax + cl_list.pax
        tot_com = tot_com + cl_list.com


        cl_list.lodging =  to_decimal(cl_list.zipreis)

        if cl_list.lodging != 0:
            prcode = 0
            contcode = ""

            rguest = db_session.query(Rguest).filter(
                     (Rguest.gastnr == reslin_list.gastnr)).first()

            if reslin_list.reserve_int != 0:

                guest_pr = db_session.query(Guest_pr).filter(
                         (Guest_pr.gastnr == rguest.gastnr)).first()

            if guest_pr:
                contcode = guest_pr.code
                ct = reslin_list.zimmer_wunsch

                if re.match(r".*\$CODE\$.*",ct, re.IGNORECASE):
                    ct = substring(ct, 0 + get_index(ct, "$CODE$") + 6)
                    contcode = substring(ct, 0, 1 + get_index(ct, ";") - 1)

                if new_contrate:
                    prcode = get_output(ratecode_seek(reslin_list.resnr, reslin_list.reslinnr, contcode, curr_date))
                else:

                    pricecod = db_session.query(Pricecod).filter(
                             (func.lower(Pricecod.code) == (contcode).lower()) & (Pricecod.marknr == reslin_list.reserve_int) & (Pricecod.argtnr == arrangement.argtnr) & (Pricecod.zikatnr == curr_zikatnr) & (curr_date >= Pricecod.startperiode) & (curr_date <= Pricecod.endperiode)).first()

                    if pricecod:
                        prcode = pricecod._recid

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()

                if not artikel:
                    take_it = False
                else:
                    take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                if take_it:

                    if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.bfast =  to_decimal(cl_list.bfast) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_bfast =  to_decimal(ltot_bfast) + to_decimal(argt_betrag)
                        else:
                            tot_bfast =  to_decimal(tot_bfast) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                    elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(argt_betrag)
                        else:
                            tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                    elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_dinner =  to_decimal(ltot_dinner) + to_decimal(argt_betrag)
                        else:
                            tot_dinner =  to_decimal(tot_dinner) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                    elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(argt_betrag)
                        else:
                            tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)


                    else:
                        cl_list.misc =  to_decimal(cl_list.misc) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_misc =  to_decimal(ltot_misc) + to_decimal(argt_betrag)
                        else:
                            tot_misc =  to_decimal(tot_misc) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

        if reslin_list.adrflag:
            ltot_lodging =  to_decimal(ltot_lodging) + to_decimal(cl_list.lodging)
        else:
            tot_lodging =  to_decimal(tot_lodging) + to_decimal(cl_list.lodging)
        lodge_betrag =  to_decimal(cl_list.lodging) * to_decimal(frate)

        if foreign_rate and price_decimal == 0 and not reslin_list.adrflag:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 145)).first()

            if htparam.finteger != 0:
                n = 1
                for i in range(1,htparam.finteger + 1) :
                    n = n * 10
                lodge_betrag = to_decimal(round(lodge_betrag / n , 0) * n)

        artikel1 = db_session.query(Artikel1).filter(
                 (Artikel1.artnr == arrangement.artnr_logis) & (Artikel1.departement == 0)).first()

        for fixleist in db_session.query(Fixleist).filter(
                 (Fixleist.resnr == reslin_list.resnr) & (Fixleist.reslinnr == reslin_list.reslinnr)).order_by(Fixleist._recid).all():
            post_it = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

            if post_it:
                fcost =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)
                cl_list.t_rev =  to_decimal(cl_list.t_rev) + to_decimal(fcost)

                if reslin_list.adrflag:
                    ltot_rate =  to_decimal(ltot_rate) + to_decimal(fcost)
                else:
                    tot_rate =  to_decimal(tot_rate) + to_decimal(fcost)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == fixleist.artnr) & (Artikel.departement == fixleist.departement)).first()

                if (artikel.zwkum == bfast_art and artikel.departement == fb_dept):
                    cl_list.bfast =  to_decimal(cl_list.bfast) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_bfast =  to_decimal(ltot_bfast) + to_decimal(fcost) * to_decimal(frate)
                    else:
                        tot_bfast =  to_decimal(tot_bfast) + to_decimal(fcost)

                elif (artikel.zwkum == lunch_art and artikel.departement == fb_dept):
                    cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(fcost) * to_decimal(frate)
                    else:
                        tot_lunch =  to_decimal(tot_lunch) + to_decimal(fcost)

                elif (artikel.zwkum == dinner_art and artikel.departement == fb_dept):
                    cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_dinner =  to_decimal(ltot_dinner) + to_decimal(fcost) * to_decimal(frate)
                    else:
                        tot_dinner =  to_decimal(tot_dinner) + to_decimal(fcost)
                else:
                    cl_list.fixcost =  to_decimal(cl_list.fixcost) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_fix =  to_decimal(ltot_fix) + to_decimal(fcost)
                    else:
                        tot_fix =  to_decimal(tot_fix) + to_decimal(fcost)

        if curr_zinr != reslin_list.zinr or curr_resnr != reslin_list.resnr:

            if reslin_list.adrflag:
                ltot_rm = ltot_rm + 1
            else:
                tot_rm = tot_rm + 1
        curr_zinr = reslin_list.zinr
        curr_resnr = reslin_list.resnr


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_list, output_list_list, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal reslin_list_list, cl_list_list, output_list_list

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return (post_it)


        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if reslin_list.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (reslin_list.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if lfakt == None:
                delta = 0
            else:
                delta = lfakt - reslin_list.ankunft

                if delta < 0:
                    delta = 0
            start_date = reslin_list.ankunft + timedelta(days=delta)

            if (reslin_list.abreise - start_date) < intervall:
                start_date = reslin_list.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()


    def get_argtline_rate(contcode:str, argt_recid:int):

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_list, output_list_list, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, vat, service, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal reslin_list_list, cl_list_list, output_list_list

        add_it = False
        f_betrag = to_decimal("0.0")
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        argtline = None

        def generate_inner_output():
            return (add_it, f_betrag, argt_betrag, qty)

        Argtline =  create_buffer("Argtline",Argt_line)

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        argtline = db_session.query(Argtline).filter(
                 (Argtline._recid == argt_recid)).first()

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = reslin_list.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = reslin_list.kind1

        elif argt_line.vt_percnt == 2:
            qty = reslin_list.kind2

        if qty > 0:

            if argtline.fakt_modus == 1:
                add_it = True

            elif argtline.fakt_modus == 2:

                if reslin_list.ankunft == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 3:

                if (reslin_list.ankunft + 1) == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 4 and get_day(curr_date) == 1:
                add_it = True

            elif argtline.fakt_modus == 5 and get_day(curr_date + 1) == 1:
                add_it = True

            elif argtline.fakt_modus == 6:

                if (reslin_list.ankunft + (argtline.intervall - 1)) >= curr_date:
                    add_it = True

        if add_it:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == reslin_list.resnr) & (Reslin_queasy.reslinnr == reslin_list.reslinnr) & (Reslin_queasy.number1 == argtline.departement) & (Reslin_queasy.number2 == argtline.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

            if reslin_queasy:
                argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                f_betrag =  to_decimal(argt_betrag)

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung._recid == waehrung1._recid)).first()

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == reslin_list.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.resnr == argtline.departement) & (Reslin_queasy.reslinnr == curr_zikatnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung._recid == waehrung1._recid)).first()

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.argtnr == argt_line.argtnr)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == arrangement.betriebsnr)).first()
            f_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if reslin_list.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)
            argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()

    rstat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    rstat_list[1] = translateExtended ("6 PM", lvcarea, "")
    rstat_list[2] = translateExtended ("Tentative", lvcarea, "")
    rstat_list[3] = translateExtended ("WaitList", lvcarea, "")
    rstat_list[4] = translateExtended ("Verbal Confirm", lvcarea, "")
    rstat_list[5] = translateExtended ("Main Guest", lvcarea, "")
    rstat_list[6] = ""
    rstat_list[7] = translateExtended ("Departed", lvcarea, "")
    rstat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    rstat_list[9] = translateExtended ("NoShow", lvcarea, "")
    rstat_list[10] = translateExtended ("ResSharer", lvcarea, "")
    rstat_list[11] = ""
    rstat_list[12] = translateExtended ("RmSharer", lvcarea, "")

    reslin_list = query(reslin_list_list, first=True)

    if reslin_list:
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.night = to_string(reslin_list.anztage)
        output_list.adult = to_string(reslin_list.erwachs)
        output_list.child1 = to_string(reslin_list.kind1)
        output_list.child2 = to_string(reslin_list.kind2)
        output_list.com = to_string(reslin_list.gratis)
        output_list.rmqty = to_string(reslin_list.zimmeranz)
        output_list.ci = to_string(reslin_list.ankunft, "99/99/9999")
        output_list.co = to_string(reslin_list.abreise, "99/99/9999")
        output_list.rmno = reslin_list.zinr
        output_list.argt = reslin_list.arrangement

        if reslin_list.zipreis != 0:
            output_list.rmrate = to_string(reslin_list.zipreis, ">,>>>,>>>,>>9.99")


        else:
            output_list.rmrate = "0.00"

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == reslin_list.gastnrmember)).first()

        if guest:
            output_list.guest = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            output_list.email_adr = guest.email_adr
            ausweis_nr2 = guest.ausweis_nr2
            karteityp = guest.karteityp

        nation = db_session.query(Nation).filter(
                 (Nation.kurzbez == guest.nation1)).first()

        if nation:

            if re.match(r".*;.*",nation.bezeich, re.IGNORECASE):
                output_list.nat = entry(0, nation.bezeich, ";")


            else:
                output_list.nat = nation.bezeich

        nation1 = db_session.query(Nation1).filter(
                 (Nation1.kurzbez == guest.land)).first()

        if nation1:

            if re.match(r".*;.*",nation1.bezeich, re.IGNORECASE):
                output_list.country = entry(0, nation1.bezeich, ";")


            else:
                output_list.country = nation1.bezeich

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == reslin_list.resnr)).first()

        if reservation:
            output_list.grpname = reservation.groupname

            if reservation.depositgef != 0:
                output_list.deposit = to_string(reservation.depositgef, ">,>>>,>>>,>>9.99")

            if reservation.depositbez != 0:
                output_list.pay1 = to_string(reservation.depositbez, ">,>>>,>>>,>>9.99")

            if reservation.depositbez2 != 0:
                output_list.pay2 = to_string(reservation.depositbez2, ">,>>>,>>>,>>9.99")

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == reslin_list.resnr) & (Res_line.reslinnr == reslin_list.reslinnr)).first()

        if res_line:
            output_list.res_status = rstat_list[reslin_list.resstatus - 1]
            output_list.restat = res_line.resstatus
            output_list.lzuordnung3 = res_line.l_zuordnung[2]

            if re.match(r".*;.*",res_line.memozinr, re.IGNORECASE):
                output_list.memo_zinr = entry(1, res_line.memozinr, ";")


            else:
                output_list.memo_zinr = res_line.memozinr

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrpay)).first()

            if guest:
                output_list.bill_reciv = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1


            for i in range(1,num_entries(reslin_list.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(i - 1, reslin_list.zimmer_wunsch, ";")

                if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                    segm__purcode = to_int(substring(str, 8))

                elif substring(str, 0, 6) == ("$CODE$").lower() :
                    output_list.contcode = substring(str, 6)

            queasy1 = db_session.query(Queasy1).filter(
                     (Queasy1.key == 143) & (Queasy1.number1 == segm__purcode)).first()

            if queasy1:
                output_list.purpose = queasy1.char3

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9) & (Queasy.number1 == to_int(reslin_list.code))).first()

            if queasy:
                output_list.bill_instruct = queasy.char1

        if reslin_list.kontignr > 0:

            kontline = db_session.query(Kontline).filter(
                     (Kontline.kontignr == reslin_list.kontignr) & (Kontline.kontstatus == 1)).first()
        else:

            kontline = db_session.query(Kontline).filter(
                     (Kontline.kontignr == - reslin_list.kontignr) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).first()

        if kontline:
            output_list.allot = kontline.kontcode

        if output_list.contcode != "":

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (Queasy.char1 == output_list.contcode)).first()

            if queasy:
                output_list.ratecode = queasy.char1

        waehrung1 = db_session.query(Waehrung1).filter(
                 (Waehrung1.waehrungsnr == reslin_list.betriebsnr)).first()

        if waehrung1:
            output_list.currency = waehrung1.wabkurz

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == reslin_list.zikatnr)).first()

        if zimkateg:
            output_list.rmcat = zimkateg.bezeichnung

        if res_line.kontakt_nr != 0 and res_line.resstatus <= 6:

            for bres in db_session.query(Bres).filter(
                     (Bres.resnr == reslin_list.resnr) & (Bres.reslinnr != reslin_list.reslinnr) & (Bres.kontakt_nr == reslin_list.reslinnr) & (Bres.resstatus != 9) & (Bres.resstatus != 10) & (Bres.resstatus != 12)).order_by(Bres.l_zuordnung[inc_value(2)], Bres.resstatus, Bres.name).all():

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bres.gastnrmember)).first()

                if guest:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.guest = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                            " " + guest.anrede1
                    output_list.restat = bres.resstatus
                    output_list.lzuordnung3 = bres.l_zuordnung[2]


        elif res_line.kontakt_nr != 0 and res_line.resstatus > 6:

            bres = db_session.query(Bres).filter(
                     (Bres.resnr == res_line.resnr) & (Bres.reslinnr == res_line.kontakt_nr) & (Bres.resstatus != 9) & (Bres.resstatus != 10) & (Bres.resstatus != 12)).first()

            if bres:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bres.gastnrmember)).first()

                if guest:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.guest = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                            " " + guest.anrede1
                    output_list.restat = bres.resstatus
                    output_list.lzuordnung3 = bres.l_zuordnung[2]


    cal_revenue()

    return generate_output()