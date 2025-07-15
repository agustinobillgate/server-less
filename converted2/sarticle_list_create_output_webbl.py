#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Queasy

t_l_artikel_data, T_l_artikel = create_model_like(L_artikel, {"stock_onhand":Decimal})

def sarticle_list_create_output_webbl(idflag:string, t_l_artikel_data:[T_l_artikel]):
    curr_art = ""
    curr_art1 = 0
    doneflag = False
    counter:int = 0
    l_artikel = queasy = None

    t_l_artikel = tqueasy = dqueasy = pqueasy = None

    Tqueasy = create_buffer("Tqueasy",Queasy)
    Dqueasy = create_buffer("Dqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_art, curr_art1, doneflag, counter, l_artikel, queasy
        nonlocal idflag
        nonlocal tqueasy, dqueasy, pqueasy


        nonlocal t_l_artikel, tqueasy, dqueasy, pqueasy

        return {"curr_art": curr_art, "curr_art1": curr_art1, "doneflag": doneflag, "t-l-artikel": t_l_artikel_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == ("Artikel List").lower())).order_by(Queasy.char2).all():
        counter = counter + 1

        if counter > 1000:
            break
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        t_l_artikel.artnr = to_int(entry(0, queasy.char2, "|"))
        t_l_artikel.bezeich = entry(1, queasy.char2, "|")

        dqueasy = db_session.query(Dqueasy).filter(
                 (Dqueasy._recid == queasy._recid)).first()
        db_session.delete(dqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Artikel List").lower())).first()

    if pqueasy:
        curr_art1 = 0


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Artikel List").lower()) & (Tqueasy.number1 == 1)).first()

        if tqueasy:
            curr_art1 = 0


        else:
            curr_art1 = 1

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("Artikel List").lower()) & (Tqueasy.number1 == 0)).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()