from functions.additional_functions import *
import decimal
from sqlalchemy import desc
from models import H_artikel, Htparam, Wgrpdep, Hoteldpt, Queasy, Wgrpgen, Artikel

def prepare_rarticle_adminbl(dept:int):
    long_digit = False
    d_bezeich = ""
    q1_list_list = []
    h_artikel = htparam = wgrpdep = hoteldpt = queasy = wgrpgen = artikel = None

    wbuff = q1_list = None

    wbuff_list, Wbuff = create_model("Wbuff", {"departement":int, "zknr":int, "bez":str})
    q1_list_list, Q1_list = create_model_like(H_artikel, {"bez":str, "zknr":int, "bezeich2":str, "zk_bezeich":str, "ek_bezeich":str, "fart_bezeich":str, "fo_dept":int})


    db_session = local_storage.db_session
    
    def generate_output():
        nonlocal long_digit, d_bezeich, q1_list_list, h_artikel, htparam, wgrpdep, hoteldpt, queasy, wgrpgen, artikel


        nonlocal wbuff, q1_list
        nonlocal wbuff_list, q1_list_list
        return {"long_digit": long_digit, "d_bezeich": d_bezeich, "q1-list": q1_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    for wgrpdep in db_session.query(Wgrpdep).filter(
            (Wgrpdep.departement == dept)).all():
        wbuff = Wbuff()
        wbuff.departement = dept
        wbuff.zknr = wgrpdep.zknr
        wbuff.bez = wgrpdep.bezeich
        wbuff_list.append(wbuff)
        
    # print("wbuff_list:", wbuff_list)

    
    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    
    d_bezeich = hoteldpt.depart
    h_artikel_obj_list = []
    
    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == dept)).all():
        
        wbuff = query(wbuff_list,filters=(lambda wbuff:(wbuff.zknr == h_artikel.zwkum) and (wbuff.departement == h_artikel.departement)),first=True)
        if h_artikel._recid in h_artikel_obj_list:
            continue
        else:
            h_artikel_obj_list.append(h_artikel._recid)


        q1_list = Q1_list()
        buffer_copy(h_artikel, q1_list)
        q1_list.bez = wbuff.bez
        q1_list.zknr = wbuff.zknr
        
        q1_list_list.append(q1_list)

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 38) &  (Queasy.number1 == h_artikel.departement) &  (Queasy.number2 == h_artikel.artnr)).first()

        if queasy:
            q1_list.bezeich2 = queasy.char3

        wgrpdep = db_session.query(Wgrpdep).filter(
                (Wgrpdep.zknr == h_artikel.zwkum) &  (Wgrpdep.departement == dept)).first()

        if wgrpdep:
            q1_list.zk_bezeich = wgrpdep.bezeich
        else:
            q1_list.zk_bezeich = "?????"

        wgrpgen = db_session.query(Wgrpgen).filter(
                (Wgrpgen.eknr == h_artikel.endkum)).first()

        if wgrpgen:
            q1_list.ek_bezeich = wgrpgen.bezeich
        else:
            q1_list.ek_bezeich = "?????"

        if h_artikel.artart <= 1:
            q1_list.fo_dept = dept
        else:
            q1_list.fo_dept = 0

        artikel = db_session.query(Artikel).filter( (Artikel.artnr == h_artikel.artnrfront) &  (Artikel.departement == q1_list.fo_dept)).first()

        if artikel:
            q1_list.bezeichnung = artikel.bezeich
        else:
            q1_list.fart_bezeich = "????????"

    return generate_output()