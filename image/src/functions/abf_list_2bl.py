from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Res_line, Arrangement, Artikel, Argt_line, Reslin_queasy, Fixleist, Guest, Reservation, Segment, Ratecode, Bill, Master

def abf_list_2bl(fdate:date, bfast_artnr:int, bfast_dept:int, zikat_list:[Zikat_list]):
    abf_list_list = []
    mxtime_dayuse:int = 0
    param_561:str = ""
    htparam = res_line = arrangement = artikel = argt_line = reslin_queasy = fixleist = guest = reservation = segment = ratecode = bill = master = None

    abf_list = zikat_list = invoice = None

    abf_list_list, Abf_list = create_model("Abf_list", {"zinr":str, "name":str, "segmentcode":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":str, "arrangement":str, "zimmeranz":int, "erwachs":int, "kind1":int, "gratis":int, "resnr":int, "bemerk":str, "gastnr":int, "resstatus":int, "resname":str, "address":str, "city":str, "comments":str, "datum":date, "nation1":str, "bezeich":str, "zipreis":decimal, "code":str, "id":str, "bezeichnung":str, "mobil_telefon":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":str, "bezeich":str})

    Invoice = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal abf_list_list, mxtime_dayuse, param_561, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, bill, master
        nonlocal invoice


        nonlocal abf_list, zikat_list, invoice
        nonlocal abf_list_list, zikat_list_list
        return {"abf-list": abf_list_list}

    def disp_arlist():

        nonlocal abf_list_list, mxtime_dayuse, param_561, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, bill, master
        nonlocal invoice


        nonlocal abf_list, zikat_list, invoice
        nonlocal abf_list_list, zikat_list_list

        do_it:bool = False
        roflag:bool = False
        epreis:decimal = 0
        qty:int = 0
        i:int = 0
        str:str = ""
        contcode:str = ""
        dont_post:bool = False
        abf_list_list.clear()

        res_line_obj_list = []
        for res_line, zikat_list in db_session.query(Res_line, Zikat_list).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).filter(
                ((Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)) &  (Res_line.active_flag <= 1) &  (((Res_line.ankunft < fdate) &  (Res_line.abreise >= fdate)) |  ((Res_line.ankunft == fdate) &  (Res_line.abreise == fdate) &  (Res_line.ankzeit <= mxtime_dayuse))) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            do_it = False
            roflag = True
            qty = 0

            if (res_line.erwachs + res_line.kind1 + res_line.gratis + res_line.l_zuordnung[3]) == 0:
                1
            else:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                if arrangement:

                    argt_line_obj_list = []
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == bfast_dept) &  (Artikel.zwkum == bfast_artnr)).filter(
                            (Argt_line.argtnr == arrangement.argtnr)).all():
                        if argt_line._recid in argt_line_obj_list:
                            continue
                        else:
                            argt_line_obj_list.append(argt_line._recid)


                        do_it = True
                        roflag = False
                        epreis = argt_line.betrag


                        break

            if do_it and epreis == 0:
                contcode = ""

                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == "$CODE$":
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == res_line.reserve_int) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == bfast_artnr) &  (Reslin_queasy.resnr == bfast_dept) &  (Reslin_queasy.reslinnr == res_line.zikatnr) &  (Reslin_queasy.date1 <= fdate) &  (Reslin_queasy.date2 >= fdate) &  (Reslin_queasy.deci1 > 0)).first()

                    if not reslin_queasy:

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.number1 == bfast_dept) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == bfast_artnr) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= fdate) &  (Reslin_queasy.date2 >= fdate) &  (Reslin_queasy.deci1 > 0)).first()
                do_it = None != reslin_queasy
                roflag = not do_it

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr) &  (Fixleist.artnr == bfast_artnr) &  (Fixleist.departement == bfast_dept)).all():
                    dont_post = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == res_line.argt_typ)).first()

                ratecode = db_session.query(Ratecode).filter(
                        (Ratecode.CODE == res_line.arrangement)).first()
                abf_list = Abf_list()
                abf_list_list.append(abf_list)


                if not roflag:
                    buffer_copy(res_line, abf_list)
                else:
                    buffer_copy(res_line, abf_list,except_fields=["erwachs","kind1","gratis"])
                    abf_list.erwachs = 0


                abf_list.segmentcode = reservation.segmentcode
                abf_list.kurzbez = zikat_list.kurzbez
                abf_list.erwachs = abf_list.erwachs + qty
                abf_list.gastnr = res_line.gastnr
                abf_list.resname = reservation.name
                abf_list.comments = reservation.bemerk
                abf_list.bezeich = segment.bezeich
                abf_list.zipreis = res_line.zipreis
                abf_list.id = reservation.useridanlage

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr(10)
                abf_list.comments = abf_list.comments + res_line.bemerk

                if not roflag:
                    abf_list.kind1 = abf_list.kind1 + res_line.l_zuordnung[3]

                if zimkateg:
                    abf_list.kurzbez = zimkateg.kurzbez

                if ratecode:
                    abf_list.CODE = ratecode.CODE

                if guest:
                    abf_list.address = guest.adresse1
                    abf_list.city = guest.wohnort + " " + guest.plz
                    abf_list.nation1 = guest.nation1
                    abf_list.mobil_telefon = guest.mobil_telefon

    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal abf_list_list, mxtime_dayuse, param_561, htparam, res_line, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, bill, master
        nonlocal invoice


        nonlocal abf_list, zikat_list, invoice
        nonlocal abf_list_list, zikat_list_list

        dont_post = False
        master_flag:bool = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return dont_post
        Invoice = Bill

        master = db_session.query(Master).filter(
                (Master.resnr == res_line.resnr) &  (Master.active) &  (Master.flag == 0)).first()

        if master and master.umsatzart[1] :
            master_flag = True

        if master_flag:

            invoice = db_session.query(Invoice).filter(
                    (Invoice.resnr == res_line.resnr) &  (Invoice.reslinnr == 0)).first()
        else:

            invoice = db_session.query(Invoice).filter(
                    (Invoice.zinr == res_line.zinr) &  (Invoice.resnr == res_line.resnr) &  (Invoice.reslinnr == res_line.reslinnr) &  (Invoice.billtyp == 0) &  (Invoice.billnr == 1) &  (Invoice.flag == 0)).first()

        if not dont_post:

            if fakt_modus == 2:

                if res_line.ankunft != fdate:
                    dont_post = True

            elif fakt_modus == 3:

                if (res_line.ankunft + 1) != fdate:
                    dont_post = True

            elif fakt_modus == 4:

                if get_day(fdate) != 1:
                    dont_post = True

            elif fakt_modus == 5:

                if get_day(fdate + timedelta(days=1)) != 1:
                    dont_post = True

            elif fakt_modus == 6:

                if lfakt == None:
                    delta = 0
                else:
                    delta = lfakt - res_line.ankunft

                    if delta < 0:
                        delta = 0
                start_date = res_line.ankunft + delta

                if (res_line.abreise - start_date) < intervall:
                    start_date = res_line.ankunft

                if fdate > (start_date + (intervall - 1)):
                    dont_post = True

                if fdate < start_date:
                    dont_post = True


        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 561)).first()

    if htparam:
        param_561 = trim(htparam.fchar)

    if param_561 != "":
        mxtime_dayuse = to_int(substring(param_561, 0, 2)) * 3600 + to_int(substring(param_561, 3, 2)) * 60
    disp_arlist()

    return generate_output()