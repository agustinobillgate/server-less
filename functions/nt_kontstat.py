from functions.additional_functions import *
import decimal
from datetime import date
from models import Kontstat, Htparam, Kontline, Zimmer, Res_line, Bill, Queasy, Guest

def nt_kontstat():
    dayuse:bool = False
    bill_date:date = None
    anz:int = 762
    kontstat = htparam = kontline = zimmer = res_line = bill = queasy = guest = None

    kbuff = None

    Kbuff = create_buffer("Kbuff",Kontstat)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dayuse, bill_date, anz, kontstat, htparam, kontline, zimmer, res_line, bill, queasy, guest
        nonlocal kbuff


        nonlocal kbuff

        return {}

    def check_global_allotment():

        nonlocal dayuse, bill_date, anz, kontstat, htparam, kontline, zimmer, res_line, bill, queasy, guest
        nonlocal kbuff


        nonlocal kbuff

        tokcounter:int = 0
        mesvalue:str = ""

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 147) & (Queasy.number1 == kontline.gastnr) & (Queasy.char1 == kontline.kontcode)).first()

        if queasy:
            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if mesvalue != "":

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == to_int(mesvalue))).first()

                    if guest:

                        kontstat = db_session.query(Kontstat).filter(
                                 (Kontstat.gastnr == guest.gastnr) & (Kontstat.kontcode == kontline.kontcode) & (Kontstat.datum == bill_date)).first()

                        if not kontstat:
                            kontstat = Kontstat()
                            db_session.add(kontstat)

                            kontstat.gastnr = guest.gastnr
                            kontstat.kontcode = kontline.kontcode
                            kontstat.datum = bill_date
                            kontstat.zikatnr = kontline.zikatnr
                            kontstat.arrangement = kontline.arrangement
                            kontstat.erwachs = kontline.erwachs
                            kontstat.kind1 = kontline.kind1
                            kontstat.zimmeranz = kontline.zimmeranz
                            kontstat.overbook = kontline.overbook

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    for kontline in db_session.query(Kontline).filter(
             (Kontline.ankunft <= bill_date) & (Kontline.abreise >= bill_date) & (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1)).order_by(Kontline.kontcode).all():

        kontstat = db_session.query(Kontstat).filter(
                 (Kontstat.gastnr == kontline.gastnr) & (Kontstat.kontcode == kontline.kontcode) & (Kontstat.datum == bill_date)).first()

        if not kontstat:
            kontstat = Kontstat()
            db_session.add(kontstat)

            kontstat.gastnr = kontline.gastnr
            kontstat.kontcode = kontline.kontcode
            kontstat.datum = bill_date
            kontstat.zikatnr = kontline.zikatnr
            kontstat.arrangement = kontline.arrangement
            kontstat.erwachs = kontline.erwachs
            kontstat.kind1 = kontline.kind1
            kontstat.zimmeranz = kontline.zimmeranz
            kontstat.overbook = kontline.overbook


        check_global_allotment()

    res_line_obj_list = []
    for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.abreise == bill_date) & (Res_line.resstatus == 8)) & (Res_line.kontignr > 0)).order_by(Res_line.gastnr, Res_line.kontignr).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)

        kontline = db_session.query(Kontline).filter(
                 (Kontline.kontignr == res_line.kontignr) & (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1)).first()
        dayuse = False

        if res_line.active_flag == 2 and res_line.ankunft == bill_date:

            bill = db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).first()

            if bill and bill.argtumsatz > 0:
                dayuse = True

        if kontline and ((res_line.abreise > res_line.ankunft) or dayuse):

            kontstat = db_session.query(Kontstat).filter(
                     (Kontstat.gastnr == res_line.gastnr) & (Kontstat.kontcode == kontline.kontcode) & (Kontstat.datum == bill_date) & (kontline.kontstatus == 1)).first()

            if not kontstat:
                kontstat = Kontstat()
                db_session.add(kontstat)

                kontstat.gastnr = res_line.gastnr
                kontstat.kontcode = kontline.kontcode
                kontstat.datum = bill_date
                kontstat.zikatnr = kontline.zikatnr
                kontstat.arrangement = kontline.arrangement
                kontstat.erwachs = kontline.erwachs
                kontstat.kind1 = kontline.kind1
                kontstat.zimmeranz = kontline.zimmeranz
                kontstat.overbook = kontline.overbook

            if not res_line.zimmerfix:
                kontstat.belegt = kontstat.belegt + res_line.zimmeranz


            kontstat.personen = kontstat.personen + res_line.erwachs +\
                    res_line.kind1 + res_line.kind2 + res_line.gratis

    kontstat = db_session.query(Kontstat).filter(
             (Kontstat.datum <= (bill_date - timedelta(days=anz)))).first()
    while None != kontstat:

        kbuff = db_session.query(Kbuff).filter(
                     (Kbuff._recid == kontstat._recid)).first()
        kbuff_list.remove(kbuff)
        pass


        curr_recid = kontstat._recid
        kontstat = db_session.query(Kontstat).filter(
                 (Kontstat.datum <= (bill_date - timedelta(days=anz))) & (Kontstat._recid > curr_recid)).first()

    return generate_output()