from functions.additional_functions import *
import decimal
from models import Artikel

def fo_inv_price_listbl(billart:int, artdept:int, double_currency:bool, zipreis:decimal, res_exrate:decimal, price_decimal:int, foreign_rate:bool, p_145:int):
    description = ""
    qty = 0
    price = 0
    msg_int = 0
    i:int = 0
    n:int = 0
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model("T_artikel", {"artnr":int, "bezeich":str, "epreis":decimal, "departement":int, "artart":int, "activeflag":bool, "artgrp":int, "bezaendern":bool, "autosaldo":bool, "pricetab":bool, "betriebsnr":int, "resart":bool, "zwkum":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal description, qty, price, msg_int, i, n, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"description": description, "qty": qty, "price": price, "msg_int": msg_int}

    for artikel in db_session.query(Artikel).filter(
            (Artikel.activeflag)).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    t_artikel = query(t_artikel_list, filters=(lambda t_artikel :t_artikel.artnr == billart and t_artikel.departement == artdept and t_artikel.activeflag), first=True)

    if not t_artikel:
        msg_int = 1

    if t_artikel and (t_artikel.artart == 0 or t_artikel.artart == 2 or t_artikel.artart == 6 or t_artikel.artart == 7 or t_artikel.artart == 8 or t_artikel.artart == 9):
        description = t_artikel.bezeich
        qty = 1

        if (t_artikel.artart != 9) or (t_artikel.artart == 9 and t_artikel.artgrp != 0):
            price = t_artikel.epreis
        else:

            if not double_currency:
                price = round (zipreis * res_exrate, price_decimal)

                if foreign_rate and price_decimal == 0:

                    if p_145 != 0:
                        n = 1
                        for i in range(1,p_145 + 1) :
                            n = n * 10
                        price = round(price / n, 0) * n
            else:
                price = zipreis

            if price == 0:
                msg_int = 2

    return generate_output()