from functions.additional_functions import *
import decimal
from models import Queasy, Htparam, L_lieferant, L_kredit

def ap_read_approvalbl(inpop:int, inpint:int, inpchar:str):
    t_queasy_list = []
    p_786:str = ""
    i:int = 0
    j:int = 0
    sumuser:int = 0
    sumappr:int = 0
    ttot_debt:decimal = 0
    uidavailable:bool = False
    queasy = htparam = l_lieferant = l_kredit = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, p_786, i, j, sumuser, sumappr, ttot_debt, uidavailable, queasy, htparam, l_lieferant, l_kredit


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    if inpop == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 786)).first()

        if htparam and htparam.fchar != "":
            p_786 = htparam.fchar
            for i in range(1,num_entries(p_786, ";")  + 1) :

                if trim(entry(i - 1, p_786, ";")) != "":
                    sumuser = sumuser + 1

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 173) &  (Queasy.number1 == inpint)).all():
                sumappr = 0
                i = 0
                j = 0
                for i in range(1,num_entries(p_786, ";")  + 1) :
                    for j in range(1,num_entries(queasy.char1, ";")  + 1) :

                        if (trim(entry(i - 1, p_786, ";")) == trim(entry(j, queasy.char1, ";") - 1)) and (trim(entry(i, p_786, ";")) != "" or trim(entry(j, queasy.char1, ";") - 1) != "" - 1):
                            sumappr = sumappr + 1
                            break

                if sumappr < sumuser:
                    t_queasy = T_queasy()
                    t_queasy_list.append(t_queasy)

                    buffer_copy(queasy, t_queasy)
                    t_queasy.number3 = queasy._recid


    elif inpop == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 786)).first()

        if htparam and htparam.fchar != "":
            p_786 = htparam.fchar
            for i in range(1,num_entries(p_786, ";")  + 1) :

                if entry(i - 1, p_786, ";") == inpchar:
                    uidavailable = True
                    break

            if uidavailable:

                for queasy in db_session.query(Queasy).filter(
                        (Queasy.key == 173)).all():
                    uidavailable = False
                    ttot_debt = 0
                    for i in range(1,num_entries(queasy.char1, ";")  + 1) :

                        if entry(i - 1, queasy.char1, ";") == inpchar:
                            uidavailable = True
                            break

                    if not uidavailable:
                        t_queasy = T_queasy()
                        t_queasy_list.append(t_queasy)

                        buffer_copy(queasy, t_queasy)
                        t_queasy.number3 = queasy._recid


                        t_queasy.char2 = ";;;;"

                        l_kredit_obj_list = []
                        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == queasy.number1)).filter(
                                (L_kredit.lief_nr == queasy.number1) &  (L_kredit.rechnr == queasy.number2)).all():
                            if l_kredit._recid in l_kredit_obj_list:
                                continue
                            else:
                                l_kredit_obj_list.append(l_kredit._recid)

                            if l_kredit.opart == 2:
                                t_queasy_list.remove(t_queasy)
                                break
                            else:

                                if l_lieferant:
                                    t_queasy.char2 = entry(0, t_queasy.char2, ";", l_lieferant.firma)


                                t_queasy.char2 = entry(1, t_queasy.char2, ";", l_kredit.lscheinnr)
                                t_queasy.char2 = entry(3, t_queasy.char2, ";", to_string(l_kredit.rgdatum + l_kredit.ziel, "99/99/99"))

                                if l_kredit.zahlkonto == 0:
                                    ttot_debt = ttot_debt + l_kredit.netto
                                else:
                                    ttot_debt = ttot_debt + l_kredit.saldo

                        if t_queasy:
                            t_queasy.char2 = entry(2, t_queasy.char2, ";", to_string(ttot_debt, "->>>,>>>,>>>,>>9.99"))


    return generate_output()