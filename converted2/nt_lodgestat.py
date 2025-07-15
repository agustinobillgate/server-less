from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Segment, Htparam, Bill_line, Artikel, Bill, Reservation, Segmentstat, Zinrstat, Sources, Res_line, Guest, Nation, Natstat1, Landstat, Guestseg

def nt_lodgestat():
    bill_date:date = None
    resno:int = 0
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    lodg_betrag:decimal = to_decimal("0.0")
    serv_vat:bool = False
    segment = htparam = bill_line = artikel = bill = reservation = segmentstat = zinrstat = sources = res_line = guest = nation = natstat1 = landstat = guestseg = None

    segbuff0 = segbuff1 = None

    Segbuff0 = create_buffer("Segbuff0",Segment)
    Segbuff1 = create_buffer("Segbuff1",Segment)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, resno, service, vat, vat2, fact, lodg_betrag, serv_vat, segment, htparam, bill_line, artikel, bill, reservation, segmentstat, zinrstat, sources, res_line, guest, nation, natstat1, landstat, guestseg
        nonlocal segbuff0, segbuff1


        nonlocal segbuff0, segbuff1

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_vat = htparam.flogical

    for bill_line in db_session.query(Bill_line).filter(
             (Bill_line.rechnr > 0) & (Bill_line.bill_datum == bill_date) & (Bill_line.zeit >= 0) & (Bill_line.departement == 0)).order_by(Bill_line.rechnr).all():

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()

        if artikel.umsatzart == 1:
            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))

            bill = db_session.query(Bill).filter(
                     (Bill.rechnr == bill_line.rechnr)).first()
            resno = bill.resnr

            if resno == 0:
                resno = bill_line.massnr

            if resno > 0:
                lodg_betrag =  to_decimal(bill_line.betrag) / to_decimal(fact)

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == resno)).first()

                segmentstat = db_session.query(Segmentstat).filter(
                         (Segmentstat.segmentcode == reservation.segmentcode) & (Segmentstat.datum == bill_date)).first()

                if not segmentstat:
                    segmentstat = Segmentstat()
                    db_session.add(segmentstat)

                    segmentstat.segmentcode = reservation.segmentcode
                    segmentstat.datum = bill_date


                segmentstat.logis =  to_decimal(segmentstat.logis) + to_decimal(lodg_betrag)

                if bill_line.zinr != "":

                    zinrstat = db_session.query(Zinrstat).filter(
                             (Zinrstat.zinr == bill_line.zinr) & (Zinrstat.datum == bill_date)).first()

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = bill_date
                        zinrstat.zinr = bill_line.zinr


                    zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(lodg_betrag)

                if reservation.resart > 0:

                    sources = db_session.query(Sources).filter(
                             (Sources.source_code == reservation.resart) & (Sources.datum == bill_date)).first()

                    if not sources:
                        sources = Sources()
                        db_session.add(sources)

                        sources.datum = bill_date
                        sources.source_code = reservation.resart


                    sources.logis =  to_decimal(sources.logis) + to_decimal(lodg_betrag)

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr)).first()
                pass
                pass

                if res_line:

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == res_line.gastnrmember)).first()

                if guest:

                    nation = db_session.query(Nation).filter(
                             (Nation.kurzbez == guest.nation1)).first()

                if nation:

                    natstat1 = db_session.query(Natstat1).filter(
                             (Natstat1.nationnr == nation.nationnr) & (Natstat1.datum == bill_date)).first()

                    if not natstat1:
                        natstat1 = Natstat1()
                        db_session.add(natstat1)

                        natstat1.datum = bill_date
                        natstat1.nationnr = nation.nationnr


                    natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(lodg_betrag)


                pass

                if guest and guest.nation2 != "":

                    nation = db_session.query(Nation).filter(
                             (Nation.kurzbez == guest.nation2)).first()

                if nation:

                    natstat1 = db_session.query(Natstat1).filter(
                             (Natstat1.nationnr == nation.nationnr) & (Natstat1.datum == bill_date)).first()

                    if not natstat1:
                        natstat1 = Natstat1()
                        db_session.add(natstat1)

                        natstat1.datum = bill_date
                        natstat1.nationnr = nation.nationnr


                    natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(lodg_betrag)


                pass

                if guest:

                    nation = db_session.query(Nation).filter(
                             (Nation.kurzbez == guest.land)).first()

                if nation:

                    landstat = db_session.query(Landstat).filter(
                             (Landstat.nationnr == nation.nationnr) & (Landstat.datum == bill_date)).first()

                    if not landstat:
                        landstat = Landstat()
                        db_session.add(landstat)

                        landstat.datum = bill_date
                        landstat.nationnr = nation.nationnr


                    landstat.logis =  to_decimal(landstat.logis) + to_decimal(lodg_betrag)


            else:
                pass
                pass
                pass

                for guestseg in db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == bill.gastnr)).order_by(Guestseg.reihenfolge.desc()).all():

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == guestseg.segmentcode)).first()

                    if segment.betriebsnr == 0:

                        segbuff0 = db_session.query(Segbuff0).filter(
                                 (Segbuff0._recid == segment._recid)).first()
                        break

                    elif segment.betriebsnr == 1:

                        segbuff1 = db_session.query(Segbuff1).filter(
                                 (Segbuff1._recid == segment._recid)).first()

                if segbuff0:

                    segment = db_session.query(Segment).filter(
                             (Segment._recid == segbuff0._recid)).first()

                elif segbuff1:

                    segment = db_session.query(Segment).filter(
                             (Segment._recid == segbuff1._recid)).first()

                if segment:

                    segmentstat = db_session.query(Segmentstat).filter(
                             (Segmentstat.segmentcode == segment.segmentcode) & (Segmentstat.datum == bill_date)).first()

                    if not segmentstat:
                        segmentstat = Segmentstat()
                        db_session.add(segmentstat)

                        segmentstat.segmentcode = segment.segmentcode
                        segmentstat.datum = bill_date


                    segmentstat.logis =  to_decimal(segmentstat.logis) + to_decimal(lodg_betrag)

    return generate_output()