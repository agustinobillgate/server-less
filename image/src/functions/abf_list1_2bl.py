from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Genstat, Arrangement, Artikel, Argt_line, Reslin_queasy, Fixleist, Guest, Reservation, Segment, Ratecode, Res_line, Bill, Master

def abf_list1_2bl(fdate:date, bfast_artnr:int, bfast_dept:int, zikat_list:[Zikat_list]):
    abf_list_list = []
    genstat = arrangement = artikel = argt_line = reslin_queasy = fixleist = guest = reservation = segment = ratecode = res_line = bill = master = None

    abf_list = zikat_list = invoice = None

    abf_list_list, Abf_list = create_model("Abf_list", {"zinr":str, "name":str, "segmentcode":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":str, "arrangement":str, "zimmeranz":int, "erwachs":int, "kind1":int, "gratis":int, "resnr":int, "bemerk":str, "gastnr":int, "resstatus":int, "resname":str, "address":str, "city":str, "comments":str, "datum":date, "nation1":str, "bezeich":str, "zipreis":decimal, "code":str, "id":str, "bezeichnung":str, "mobil_telefon":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":str, "bezeich":str})

    Invoice = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal abf_list_list, genstat, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, res_line, bill, master
        nonlocal invoice


        nonlocal abf_list, zikat_list, invoice
        nonlocal abf_list_list, zikat_list_list
        return {"abf-list": abf_list_list}

    def disp_arlist1():

        nonlocal abf_list_list, genstat, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, res_line, bill, master
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

        genstat_obj_list = []
        for genstat, zikat_list in db_session.query(Genstat, Zikat_list).join(Zikat_list,(Zikat_list.zikatnr == Genstat.zikatnr) &  (Zikat_list.SELECTED)).filter(
                ((Genstat.resstatus != 3) &  (Genstat.resstatus != 4) &  (Genstat.resstatus != 8) &  (Genstat.resstatus != 9) &  (Genstat.resstatus != 10) &  (Genstat.resstatus != 12)) &  (Genstat.datum == fdate)).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)


            do_it = False
            roflag = True
            qty = 0

            if (genstat.erwachs + genstat.kind1 + genstat.gratis + genstat.kind3) == 0:
                1
            else:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == genstat.argt)).first()

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

                for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str = entry(i - 1, genstat.res_char[1], ";")

                    if substring(str, 0, 6) == "$CODE$":
                        contcode = substring(str, 6)
                        break

                if contcode != "":

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == genstat.res_int[1]) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == bfast_artnr) &  (Reslin_queasy.resnr == bfast_dept) &  (Reslin_queasy.reslinnr == genstat.zikatnr) &  (Reslin_queasy.date1 <= fdate) &  (Reslin_queasy.date2 >= fdate) &  (Reslin_queasy.deci1 > 0)).first()

                    if not reslin_queasy:

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.number1 == bfast_dept) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == bfast_artnr) &  (Reslin_queasy.resnr == genstat.resnr) &  (Reslin_queasy.reslinnr == genstat.res_int[0]) &  (Reslin_queasy.date1 <= fdate) &  (Reslin_queasy.date2 >= fdate) &  (Reslin_queasy.deci1 > 0)).first()
                do_it = None != reslin_queasy
                roflag = not do_it

            if not do_it:

                for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == genstat.resnr) &  (Fixleist.reslinnr == genstat.res_int[0]) &  (Fixleist.artnr == bfast_artnr) &  (Fixleist.departement == bfast_dept)).all():
                    dont_post = check_fixleist_posted1(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not dont_post:
                        do_it = True
                        qty = qty + fixleist.number

            if do_it:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == genstat.gastnrmember)).first()

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == genstat.resnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()

                ratecode = db_session.query(Ratecode).filter(
                        (Ratecode.CODE == genstat.argt)).first()
                abf_list = Abf_list()
                abf_list_list.append(abf_list)


                if not roflag:
                    buffer_copy(genstat, abf_list)
                else:
                    buffer_copy(genstat, abf_list,except_fields=["erwachs","kind1","gratis","datum"])
                    abf_list.erwachs = 0


                abf_list.datum = genstat.datum
                abf_list.segmentcode = reservation.segmentcode
                abf_list.kurzbez = zikat_list.kurzbez
                abf_list.erwachs = abf_list.erwachs + qty
                abf_list.gastnr = genstat.gastnr
                abf_list.resname = reservation.name
                abf_list.comments = reservation.bemerk
                abf_list.bezeich = segment.bezeich
                abf_list.zipreis = genstat.zipreis
                abf_list.ankunft = genstat.res_date[0]
                abf_list.abreise = genstat.res_date[1]
                abf_list.arrangement = genstat.argt
                abf_list.id = reservation.useridanlage

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr(10)

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                if res_line:
                    abf_list.bemerk = abf_list.comments + res_line.bemerk

                if abf_list.comments != "":
                    abf_list.comments = abf_list.comments + chr(10)

                if not roflag:
                    abf_list.kind1 = abf_list.kind1 + genstat.kind1

                if zimkateg:
                    abf_list.kurzbez = zimkateg.kurzbez

                if ratecode:
                    abf_list.CODE = ratecode.CODE

                if guest:
                    abf_list.address = guest.adresse1
                    abf_list.city = guest.wohnort + " " + guest.plz
                    abf_list.name = guest.name
                    abf_list.comments = abf_list.comments + guest.bemerk
                    abf_list.nation1 = guest.nation1
                    abf_list.mobil_telefon = guest.mobil_telefon

    def check_fixleist_posted1(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal abf_list_list, genstat, arrangement, artikel, argt_line, reslin_queasy, fixleist, guest, reservation, segment, ratecode, res_line, bill, master
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
                    (Invoice.resnr == genstat.resnr) &  (Invoice.reslinnr == 0)).first()
        else:

            invoice = db_session.query(Invoice).filter(
                    (Invoice.zinr == genstat.zinr) &  (Invoice.resnr == genstat.resnr) &  (Invoice.reslinnr == genstat.res_int[0]) &  (Invoice.billtyp == 0) &  (Invoice.billnr == 1) &  (Invoice.flag == 0)).first()

        if not dont_post:

            if fakt_modus == 2:

                if genstat.datum != fdate:
                    dont_post = True

            elif fakt_modus == 3:

                if (genstat.datum + 1) != fdate:
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
                    delta = lfakt - genstat.datum

                    if delta < 0:
                        delta = 0
                start_date = genstat.datum + delta

                if (genstat.datum - start_date) < intervall:
                    start_date = genstat.datum

                if fdate > (start_date + (intervall - 1)):
                    dont_post = True

                if fdate < start_date:
                    dont_post = True


        return generate_inner_output()

    disp_arlist1()

    return generate_output()