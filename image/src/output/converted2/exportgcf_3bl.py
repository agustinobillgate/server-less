#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Genstat, Nation, Res_line, Reservation, Sourccod, History

def exportgcf_3bl(fdate:date, tdate:date):

    prepare_cache ([Guest, Genstat, Nation, Res_line, Reservation, Sourccod, History])

    tguest_list = []
    end_date:date = None
    tmp_date:date = None
    guest = genstat = nation = res_line = reservation = sourccod = history = None

    tguest = b_guest = None

    tguest_list, Tguest = create_model("Tguest", {"karteityp":int, "gastnr":int, "anlage_datum":date, "name":string, "vorname1":string, "anredefirma":string, "anrede1":string, "adresse1":string, "adresse2":string, "adresse3":string, "plz":string, "wohnort":string, "land":string, "email_adr":string, "telefon":string, "geburtdatum1":date, "geschlecht":string, "propid":string, "ankunft":date, "abreise":date, "zinr":string, "sob":string, "bezeich":string, "tacomp":string, "mobil_telefon":string})

    B_guest = create_buffer("B_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tguest_list, end_date, tmp_date, guest, genstat, nation, res_line, reservation, sourccod, history
        nonlocal fdate, tdate
        nonlocal b_guest


        nonlocal tguest, b_guest
        nonlocal tguest_list

        return {"tguest": tguest_list}

    def create_genstat(date1:date, date2:date):

        nonlocal tguest_list, end_date, tmp_date, guest, genstat, nation, res_line, reservation, sourccod, history
        nonlocal fdate, tdate
        nonlocal b_guest


        nonlocal tguest, b_guest
        nonlocal tguest_list

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= date1) & (Genstat.datum <= date2) & (Genstat.gastnr > 0) & (Genstat.zinr != "") & (Genstat.resstatus != 11) & (Genstat.resstatus != 13) & (Genstat.resstatus != 4) & (Genstat.resstatus != 3) & (Genstat.resstatus != 9)).order_by(Genstat.gastnrmember).all():

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)],"karteityp": [(eq, 0)],"name": [(ne, "")]})

            if guest:

                tguest = query(tguest_list, filters=(lambda tguest: tguest.gastnr == guest.gastnr), first=True)

                if not tguest:
                    tguest = Tguest()
                    tguest_list.append(tguest)

                    buffer_copy(guest, tguest)
                    tguest.propid = ""
                    tguest.ankunft = genstat.res_date[0]
                    tguest.abreise = genstat.res_date[1]
                    tguest.zinr = genstat.zinr
                    tguest.telefon = guest.telefon
                    tguest.mobil_telefon = guest.mobil_telefon


    def create_rline(date1:date, date2:date):

        nonlocal tguest_list, end_date, tmp_date, guest, genstat, nation, res_line, reservation, sourccod, history
        nonlocal fdate, tdate
        nonlocal b_guest


        nonlocal tguest, b_guest
        nonlocal tguest_list

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.ankunft <= date2) & (Res_line.abreise >= date1) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13)).order_by(Res_line.gastnrmember).all():

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)],"karteityp": [(eq, 0)],"name": [(ne, "")]})

            if guest:

                tguest = query(tguest_list, filters=(lambda tguest: tguest.gastnr == guest.gastnr), first=True)

                if not tguest:
                    tguest = Tguest()
                    tguest_list.append(tguest)

                    buffer_copy(guest, tguest)
                    tguest.propid = ""
                    tguest.ankunft = res_line.ankunft
                    tguest.abreise = res_line.abreise
                    tguest.zinr = res_line.zinr
                    tguest.telefon = guest.telefon
                    tguest.mobil_telefon = guest.mobil_telefon


    for genstat in db_session.query(Genstat).order_by(Genstat.datum.desc()).yield_per(100):

        if genstat.gastnr != None:
            end_date = genstat.datum

            if end_date != None:
                break

    if tdate < end_date:
        end_date = tdate

    if fdate < end_date:
        create_genstat(fdate, end_date)

    if tdate > end_date:
        tmp_date = end_date + timedelta(days=1)
    create_rline(tmp_date, tdate)

    if fdate >= end_date:
        create_rline(fdate, tdate)

    for tguest in query(tguest_list):

        nation = get_cache (Nation, {"kurzbez": [(eq, tguest.land)]})

        if nation:
            tguest.bezeich = nation.bezeich

        res_line = get_cache (Res_line, {"gastnrmember": [(eq, tguest.gastnr)]})

        if res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            if reservation:

                sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

            if sourccod:
                tguest.sob = sourccod.bezeich
            else:
                tguest.sob = ""

        if res_line:

            b_guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"karteityp": [(ne, 0)]})

            if b_guest:
                tguest.tacomp = to_string(b_guest.name + ", " + b_guest.anredefirma)
            else:
                tguest.tacomp = ""
        else:

            history = get_cache (History, {"gastnr": [(eq, tguest.gastnr)],"zi_wechsel": [(eq, False)],"reslinnr": [(eq, 999)]})

            if history:

                b_guest = get_cache (Guest, {"gastnr": [(eq, history.gastnr)]})

                if b_guest:
                    tguest.tacomp = to_string(b_guest.name + ", " + b_guest.vorname1)
            else:
                tguest.tacomp = ""

    return generate_output()