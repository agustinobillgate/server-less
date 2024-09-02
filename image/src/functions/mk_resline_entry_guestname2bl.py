from functions.additional_functions import *
import decimal
from models import Guest, Master, Nation

def mk_resline_entry_guestname2bl(gcfmember:int, inp_resno:int, res_mode:str):
    billname = ""
    billadress = ""
    billcity = ""
    billland = ""
    name_editor = ""
    avail_mbuff = 0
    guest = master = nation = None

    member1 = mbuff = None

    Member1 = Guest
    Mbuff = Master

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billname, billadress, billcity, billland, name_editor, avail_mbuff, guest, master, nation
        nonlocal member1, mbuff


        nonlocal member1, mbuff
        return {"billname": billname, "billadress": billadress, "billcity": billcity, "billland": billland, "name_editor": name_editor, "avail_mbuff": avail_mbuff}


    member1 = db_session.query(Member1).filter(
            (Member1.gastnr == gcfmember)).first()
    billname = member1.name + ", " + member1.vorname1 + member1.anredefirma + " " + member1.anrede1
    billadress = member1.adresse1
    billcity = member1.wohnort + " " + member1.plz
    billland = ""

    nation = db_session.query(Nation).filter(
            (Nation.kurzbez == member1.land)).first()

    if nation:
        billland = nation.bezeich
    name_editor = billname + chr (10) + chr (10) + billadress + chr (10) + billcity + chr (10) + chr (10) + billland

    if res_mode.lower()  == "new":

        mbuff = db_session.query(Mbuff).filter(
                (Mbuff.resnr == inp_resno)).first()

        if member1.zahlungsart == 0 and not mbuff:
            avail_mbuff = 1
        else:
            avail_mbuff = 2

    return generate_output()