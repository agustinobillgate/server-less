from functions.additional_functions import *
import decimal
from datetime import date
from models import Guestseg, Segment, Guest, Guestat1

def comp_productbl(pvilanguage:int, curr_date:str):
    compproduct_list_list = []
    mm:int = 0
    yy:int = 0
    i:int = 0
    from_date:date = None
    to_date:date = None
    datum:date = None
    lvcarea:str = "comp_product"
    guestseg = segment = guest = guestat1 = None

    compproduct_list = r_list = None

    compproduct_list_list, Compproduct_list = create_model("Compproduct_list", {"num":int, "nr":int, "bezeich":str, "room":[int, 12], "ytd":int, "lytd":int})

    R_list = Compproduct_list
    r_list_list = compproduct_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal compproduct_list_list, mm, yy, i, from_date, to_date, datum, lvcarea, guestseg, segment, guest, guestat1
        nonlocal r_list


        nonlocal compproduct_list, r_list
        nonlocal compproduct_list_list
        return {"compproduct-list": compproduct_list_list}


    mm = to_int(substring(curr_date, 0, 2))
    yy = to_int(substring(curr_date, 2, 4))
    r_list_list.clear()

    guest_obj_list = []
    for guest, guestseg, segment in db_session.query(Guest, Guestseg, Segment).join(Guestseg,(Guestseg.gastnr == Guest.gastnr) &  (Guestseg.reihenfolge == 1)).join(Segment,(Segment.segmentcode == guestseg.segmentcode) &  (Segment.betriebsnr == 0)).filter(
            (Guest.karteityp == 1) &  (Guest.name > "") &  (Guest.logiernachte > 0)).all():
        if guest._recid in guest_obj_list:
            continue
        else:
            guest_obj_list.append(guest._recid)


        compproduct_list = Compproduct_list()
        compproduct_list_list.append(compproduct_list)

        compproduct_list.bezeich = guest.name
        for i in range(1,mm + 1) :
            from_date = date_mdy(i, 1, yy)
            to_date = from_date + 32
            to_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1
            for datum in range(from_date,to_date + 1) :

                guestat1 = db_session.query(Guestat1).filter(
                        (Guestat1.gastnr == guest.gastnr) &  (Guestat1.datum == datum)).first()

                if guestat1:
                    compproduct_list.room[i - 1] = compproduct_list.room[i - 1] + guestat1.zimmeranz
                    compproduct_list.ytd = compproduct_list.ytd + guestat1.zimmeranz
        for i in range(1,mm + 1) :
            from_date = date_mdy(i, 1, (yy - 1))
            to_date = from_date + 32
            to_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1
            for datum in range(from_date,to_date + 1) :

                guestat1 = db_session.query(Guestat1).filter(
                        (Guestat1.gastnr == guest.gastnr) &  (Guestat1.datum == datum)).first()

                if guestat1:
                    compproduct_list.lytd = compproduct_list.lytd + guestat1.zimmeranz
    i = 0

    for compproduct_list in query(compproduct_list_list, filters=(lambda compproduct_list :compproduct_list.ytd != 0)):
        i = i + 1
        compproduct_list.nr = i
        compproduct_list.num = i

    for compproduct_list in query(compproduct_list_list, filters=(lambda compproduct_list :(compproduct_list.nr == 0))):
        compproduct_list_list.remove(compproduct_list)
    compproduct_list = Compproduct_list()
    compproduct_list_list.append(compproduct_list)

    compproduct_list.num = 9999
    compproduct_list.bezeich = translateExtended ("T O T A L", lvcarea, "")

    for r_list in query(r_list_list, filters=(lambda r_list :r_list.num < 9999)):
        for i in range(1,12 + 1) :
            compproduct_list.room[i - 1] = compproduct_list.room[i - 1] + r_list.room[i - 1]
        compproduct_list.ytd = compproduct_list.ytd + r_list.ytd
        compproduct_list.lytd = compproduct_list.lytd + r_list.lytd

    return generate_output()