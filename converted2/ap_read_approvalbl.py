#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Htparam, L_lieferant, L_kredit

def ap_read_approvalbl(inpop:int, inpint:int, inpchar:string):

    prepare_cache ([Htparam, L_lieferant, L_kredit])

    t_queasy_data = []
    p_786:string = ""
    i:int = 0
    j:int = 0
    sumuser:int = 0
    sumappr:int = 0
    ttot_debt:Decimal = to_decimal("0.0")
    uidavailable:bool = False
    queasy = htparam = l_lieferant = l_kredit = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, p_786, i, j, sumuser, sumappr, ttot_debt, uidavailable, queasy, htparam, l_lieferant, l_kredit
        nonlocal inpop, inpint, inpchar


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"t-queasy": t_queasy_data}

    if inpop == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 786)]})

        if htparam and htparam.fchar != "":
            p_786 = htparam.fchar
            for i in range(1,num_entries(p_786, ";")  + 1) :

                if trim(entry(i - 1, p_786, ";")) != "":
                    sumuser = sumuser + 1

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 173) & (Queasy.number1 == inpint)).order_by(Queasy._recid).all():
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
                    t_queasy_data.append(t_queasy)

                    buffer_copy(queasy, t_queasy)
                    t_queasy.number3 = queasy._recid


    elif inpop == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 786)]})

        if htparam and htparam.fchar != "":
            p_786 = htparam.fchar
            for i in range(1,num_entries(p_786, ";")  + 1) :

                if entry(i - 1, p_786, ";") == inpchar:
                    uidavailable = True
                    break

            if uidavailable:

                for queasy in db_session.query(Queasy).filter(
                         (Queasy.key == 173)).order_by(Queasy._recid).all():
                    uidavailable = False
                    ttot_debt =  to_decimal("0")
                    for i in range(1,num_entries(queasy.char1, ";")  + 1) :

                        if entry(i - 1, queasy.char1, ";") == inpchar:
                            uidavailable = True
                            break

                    if not uidavailable:
                        t_queasy = T_queasy()
                        t_queasy_data.append(t_queasy)

                        buffer_copy(queasy, t_queasy)
                        t_queasy.number3 = queasy._recid


                        t_queasy.char2 = ";;;;"

                        l_kredit_obj_list = {}
                        l_kredit = L_kredit()
                        l_lieferant = L_lieferant()
                        for l_kredit.lscheinnr, l_kredit.rgdatum, l_kredit.ziel, l_kredit.netto, l_kredit.saldo, l_kredit.opart, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.lscheinnr, L_kredit.rgdatum, L_kredit.ziel, L_kredit.netto, L_kredit.saldo, L_kredit.opart, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == queasy.number1)).filter(
                                 (L_kredit.lief_nr == queasy.number1) & (L_kredit.rechnr == queasy.number2)).order_by(L_kredit._recid).all():
                            if l_kredit_obj_list.get(l_kredit._recid):
                                continue
                            else:
                                l_kredit_obj_list[l_kredit._recid] = True

                            if l_kredit.opart == 2:
                                t_queasy_data.remove(t_queasy)
                                break
                            else:

                                if l_lieferant:
                                    t_queasy.char2 = entry(0, t_queasy.char2, ";", l_lieferant.firma)


                                t_queasy.char2 = entry(1, t_queasy.char2, ";", l_kredit.lscheinnr)
                                t_queasy.char2 = entry(3, t_queasy.char2, ";", to_string(l_kredit.rgdatum + l_kredit.ziel, "99/99/99"))

                                if l_kredit.zahlkonto == 0:
                                    ttot_debt =  to_decimal(ttot_debt) + to_decimal(l_kredit.netto)
                                else:
                                    ttot_debt =  to_decimal(ttot_debt) + to_decimal(l_kredit.saldo)

                        if t_queasy:
                            t_queasy.char2 = entry(2, t_queasy.char2, ";", to_string(ttot_debt, "->>>,>>>,>>>,>>9.99"))


    return generate_output()