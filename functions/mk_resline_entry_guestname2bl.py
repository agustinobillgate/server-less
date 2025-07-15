#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Master, Nation

def mk_resline_entry_guestname2bl(gcfmember:int, inp_resno:int, res_mode:string):

    prepare_cache ([Guest, Nation])

    billname = ""
    billadress = ""
    billcity = ""
    billland = ""
    name_editor = ""
    avail_mbuff = 0
    guest = master = nation = None

    member1 = mbuff = None

    Member1 = create_buffer("Member1",Guest)
    Mbuff = create_buffer("Mbuff",Master)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billname, billadress, billcity, billland, name_editor, avail_mbuff, guest, master, nation
        nonlocal gcfmember, inp_resno, res_mode
        nonlocal member1, mbuff


        nonlocal member1, mbuff

        return {"billname": billname, "billadress": billadress, "billcity": billcity, "billland": billland, "name_editor": name_editor, "avail_mbuff": avail_mbuff}


    member1 = get_cache (Guest, {"gastnr": [(eq, gcfmember)]})
    billname = member1.name + ", " + member1.vorname1 + member1.anredefirma + " " + member1.anrede1
    billadress = member1.adresse1
    billcity = member1.wohnort + " " + member1.plz
    billland = ""

    nation = get_cache (Nation, {"kurzbez": [(eq, member1.land)]})

    if nation:
        billland = nation.bezeich
    name_editor = billname + chr_unicode(10) + chr_unicode(10) + billadress + chr_unicode(10) + billcity + chr_unicode(10) + chr_unicode(10) + billland

    if res_mode.lower()  == ("new").lower() :

        mbuff = db_session.query(Mbuff).filter(
                 (Mbuff.resnr == inp_resno)).first()

        if member1.zahlungsart == 0 and not mbuff:
            avail_mbuff = 1
        else:
            avail_mbuff = 2

    return generate_output()