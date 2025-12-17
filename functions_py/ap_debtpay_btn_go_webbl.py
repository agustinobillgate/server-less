# using conversion tools version: 1.0.0.119

# ===============================
# Rulita, 14-11-2025 | C8AAF9
# Recompile Program

# yusufwijasena, 28/11/2025
# - Fixed variable name: age_list.comment -> age_list.comments

# yusufwijasena, 16/12/2025
# - stip value bill_name from input param
# - fixed error duplicate key _recid when query for all suplier
# ===============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_lieferant, Artikel, L_kredit, Bediener, Queasy, Gl_jouhdr, Gl_acct, Gl_journal, L_order

from functions import log_program


def ap_debtpay_btn_go_webbl(art_selected: int, bill_name: str, bill_date: date):

    prepare_cache([Htparam, L_lieferant, L_kredit, Bediener, Queasy, Gl_jouhdr, Gl_acct, Gl_journal, L_order])

    bill_name = bill_name.strip()

    outstand = to_decimal("0.0")
    age_list_data = []
    t_l_lieferant_data = []
    i: int = 0
    p_986 = ""
    p_395 = ""
    htparam = l_lieferant = artikel = l_kredit = bediener = queasy = gl_jouhdr = gl_acct = gl_journal = l_order = None

    age_list = t_l_lieferant = None

    age_list_data, Age_list = create_model(
        "Age_list",
        {
            "selected": bool,
            "ap_recid": int,
            "counter": int,
            "docu_nr": str,
            "rechnr": int,
            "lief_nr": int,
            "lscheinnr": str,
            "supplier": str,
            "rgdatum": date,
            "rabatt": Decimal,
            "rabattbetrag": Decimal,
            "ziel": date,
            "netto": Decimal,
            "user_init": str,
            "debt": Decimal,
            "credit": Decimal,
            "bemerk": str,
            "tot_debt": Decimal,
            "rec_id": int,
            "resname": str,
            "comments": str,
            "fibukonto": str,
            "t_bezeich": str,
            "debt2": Decimal,
            "recv_date": date,
            "bank_name": str,
            "bank_acct": str,
            "fibu": str,
            "remark": str,
            "amount": str,
            "is_manual": int,
            "remark_manual": str
        })
    t_l_lieferant_data, T_l_lieferant = create_model(
        "T_l_lieferant",
        {
            "telefon": str,
            "fax": str,
            "adresse1": str,
            "notizen_1": str,
            "lief_nr": int
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstand, age_list_data, t_l_lieferant_data, i, p_986, p_395, htparam, l_lieferant, artikel, l_kredit, bediener, queasy, gl_jouhdr, gl_acct, gl_journal, l_order
        nonlocal art_selected, bill_name, bill_date
        nonlocal age_list, t_l_lieferant
        nonlocal age_list_data, t_l_lieferant_data

        return {
            "art_selected": art_selected,
            "outstand": outstand,
            "age-list": age_list_data,
            "t-l-lieferant": t_l_lieferant_data
        }

    def create_age_list():
        nonlocal outstand, age_list_data, t_l_lieferant_data, i, p_986, p_395, htparam, l_lieferant, artikel, l_kredit, bediener, queasy, gl_jouhdr, gl_acct, gl_journal, l_order
        nonlocal art_selected, bill_name, bill_date
        nonlocal age_list, t_l_lieferant
        nonlocal age_list_data, t_l_lieferant_data

        artikel1 = None
        curr_rechnr: int = 0
        curr_saldo: Decimal = to_decimal("0.0")
        opart: int = 1
        create_it: bool = False
        Artikel1 = create_buffer("Artikel1", Artikel)
        age_list_data.clear()
        curr_rechnr = 0
        outstand = to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        # for l_kredit.counter, l_kredit.name, l_kredit.rechnr, l_kredit.lief_nr, l_kredit._recid, l_kredit.bediener_nr, l_kredit.rgdatum, l_kredit.saldo, l_kredit.rabatt, l_kredit.rabattbetrag, l_kredit.netto, l_kredit.ziel, l_kredit.lscheinnr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.zahlkonto, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.bank, l_lieferant.kontonr, l_lieferant.lief_nr, l_lieferant.telefon, l_lieferant.fax, l_lieferant.adresse1, l_lieferant.notizen, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.name, L_kredit.rechnr, L_kredit.lief_nr, L_kredit._recid, L_kredit.bediener_nr, L_kredit.rgdatum, L_kredit.saldo, L_kredit.rabatt, L_kredit.rabattbetrag, L_kredit.netto, L_kredit.ziel, L_kredit.lscheinnr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.zahlkonto, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.bank, L_lieferant.kontonr, L_lieferant.lief_nr, L_lieferant.telefon, L_lieferant.fax, L_lieferant.adresse1, L_lieferant.notizen, L_lieferant._recid).join(L_lieferant, (L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
        #         (L_kredit.rgdatum <= bill_date) & (L_kredit.opart < 2) & (L_kredit.counter >= 0)).order_by(L_lieferant.firma, L_kredit.counter, L_kredit.rgdatum, L_kredit.zahlkonto).all():
        
            # if l_kredit_obj_list.get(kredit_recid):
            #     continue

            # l_kredit_obj_list[kredit_recid] = True

        # start - yusufwijasena, fix: error duplicate key _recid
        l_lieferant_query = (
            db_session.query(
                L_kredit.counter,
                L_kredit.name,
                L_kredit.rechnr,
                L_kredit.lief_nr,
                L_kredit._recid,
                L_kredit.bediener_nr,
                L_kredit.rgdatum,
                L_kredit.saldo,
                L_kredit.rabatt,
                L_kredit.rabattbetrag,
                L_kredit.netto,
                L_kredit.ziel,
                L_kredit.lscheinnr,
                L_kredit.bemerk,
                L_kredit.steuercode,
                L_kredit.zahlkonto,
                L_lieferant.firma,
                L_lieferant.anredefirma,
                L_lieferant.bank,
                L_lieferant.kontonr,
                L_lieferant.lief_nr,
                L_lieferant.telefon,
                L_lieferant.fax,
                L_lieferant.adresse1,
                L_lieferant.notizen,
                L_lieferant._recid,
                )
            .join(L_lieferant, L_lieferant.lief_nr == L_kredit.lief_nr)
            .filter(
                L_kredit.rgdatum <= bill_date,
                L_kredit.opart < 2,
                L_kredit.counter >= 0,
                )
            .order_by(
                L_lieferant.firma,
                L_kredit.counter,
                L_kredit.rgdatum,
                L_kredit.zahlkonto,
                )
        )
        
        for l_kredit in l_lieferant_query:
            create_it = False
            if l_kredit.counter == 0:
                create_it = True
            else:
                age_list = query(age_list_data, filters=(
                    lambda age_list: age_list.counter == l_kredit.counter), first=True)

                if not age_list:
                    create_it = True

        # end - yusufwijasena, fix: error duplicate key _recid
        
            if create_it:
                age_list = Age_list()
                age_list_data.append(age_list)

                age_list.counter = l_kredit.counter
                age_list.docu_nr = l_kredit.name
                age_list.rechnr = l_kredit.rechnr
                age_list.lief_nr = l_kredit.lief_nr
                age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                age_list.rec_id = l_kredit._recid
                for i in range(1, length(l_lieferant.bank) + 1):

                    if matches(substring(l_lieferant.bank, i - 1, 3), r"a/n"):
                        break
                age_list.bank_name = substring(l_lieferant.bank, 0, i - 1)
                age_list.bank_acct = l_lieferant.kontonr

            if l_kredit.zahlkonto == 0:
                bediener = get_cache(
                    Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    age_list.user_init = bediener.userinit
                age_list.ap_recid = l_kredit._recid
                age_list.rgdatum = l_kredit.rgdatum
                age_list.debt = to_decimal(l_kredit.saldo)
                age_list.rabatt = to_decimal(l_kredit.rabatt)
                age_list.rabattbetrag = to_decimal(l_kredit.rabattbetrag)
                age_list.netto = to_decimal(l_kredit.netto)
                age_list.ziel = l_kredit.rgdatum + \
                    timedelta(days=l_kredit.ziel)
                age_list.lscheinnr = l_kredit.lscheinnr
                age_list.bemerk = l_kredit.bemerk
                age_list.tot_debt = to_decimal(
                    age_list.tot_debt) + to_decimal(l_kredit.netto)

                queasy = get_cache(
                    Queasy, {"key": [(eq, 221)], "char1": [(eq, l_kredit.name)]})

                if queasy:
                    age_list.recv_date = queasy.date1

            else:
                age_list.credit = to_decimal(
                    age_list.credit) - to_decimal(l_kredit.saldo)
                age_list.tot_debt = to_decimal(
                    age_list.tot_debt) + to_decimal(l_kredit.saldo)
            disp_l_lieferant_debt()

            gl_jouhdr = get_cache(Gl_jouhdr, {"refno": [(eq, l_kredit.name)]})

            if gl_jouhdr and l_kredit.zahlkonto == 0:
                gl_journal = Gl_journal()
                gl_acct = Gl_acct()
                for gl_journal.fibukonto, gl_journal.debit, gl_journal.credit, gl_journal.bemerk, gl_journal._recid, gl_acct.bezeich, gl_acct._recid in db_session.query(Gl_journal.fibukonto, Gl_journal.debit, Gl_journal.credit, Gl_journal.bemerk, Gl_journal._recid, Gl_acct.bezeich, Gl_acct._recid).join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto) & ((Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4) | (Gl_acct.acc_type == 5))).filter(
                        (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                    # yusufwijasena: fix variable name: age_list.comment -> age_list.comments
                    # age_list.comment = age_list.comment + ";" + to_string(gl_journal.fibukonto) + ";" + to_string(l_kredit.steuercode)
                    age_list.comments = f"{age_list.comments};{to_string(gl_journal.fibukonto)};{to_string(l_kredit.steuercode)}"
                    age_list.fibukonto = gl_journal.fibukonto
                    age_list.t_bezeich = gl_acct.bezeich

                    if gl_journal.debit > 0:
                        age_list.debt2 = to_decimal(gl_journal.debit)

                    elif gl_journal.credit > 0:
                        age_list.debt2 = - to_decimal((gl_journal.credit))

                    if gl_journal.fibukonto.lower() == (p_986).lower() or gl_journal.fibukonto.lower() == (p_395).lower():
                        pass
                    else:
                        age_list.fibu = age_list.fibu + ";" + gl_journal.fibukonto
                        age_list.remark = age_list.remark + ";" + gl_acct.bezeich
                        age_list.amount = age_list.amount + \
                            ";" + to_string(age_list.debt2)
                        age_list.remark_manual = age_list.remark_manual + ";" + gl_journal.bemerk

            age_list.is_manual = l_kredit.steuercode
        art_selected = 1

    def create_age_list1():
        nonlocal outstand, age_list_data, t_l_lieferant_data, i, p_986, p_395, htparam, l_lieferant, artikel, l_kredit, bediener, queasy, gl_jouhdr, gl_acct, gl_journal, l_order
        nonlocal art_selected, bill_name, bill_date
        nonlocal age_list, t_l_lieferant
        nonlocal age_list_data, t_l_lieferant_data

        artikel1 = None
        curr_rechnr: int = 0
        curr_saldo: Decimal = to_decimal("0.0")
        opart: int = 1
        create_it: bool = False
        Artikel1 = create_buffer("Artikel1", Artikel)
        age_list_data.clear()
        curr_rechnr = 0
        outstand = to_decimal("0")

        l_lieferant = get_cache(L_lieferant, {"firma": [(eq, bill_name)]})

        if l_lieferant:
            for l_kredit in db_session.query(L_kredit).filter(
                    (L_kredit.rgdatum <= bill_date) & (L_kredit.opart < 2) & (L_kredit.lief_nr == l_lieferant.lief_nr)).order_by(L_kredit.counter, L_kredit.rgdatum, L_kredit.zahlkonto).all():
                create_it = False

                if l_kredit.counter == 0:
                    create_it = True
                else:
                    age_list = query(age_list_data, filters=(
                        lambda age_list: age_list.counter == l_kredit.counter), first=True)

                    if not age_list:
                        create_it = True

                if create_it:
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.counter = l_kredit.counter
                    age_list.docu_nr = l_kredit.name
                    age_list.rechnr = l_kredit.rechnr
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                    age_list.rec_id = l_kredit._recid
                    for i in range(1, length(l_lieferant.bank) + 1):

                        if matches(substring(l_lieferant.bank, i - 1, 3), r"a/n"):
                            break
                    age_list.bank_name = substring(l_lieferant.bank, 0, i - 1)
                    age_list.bank_acct = l_lieferant.kontonr

                if l_kredit.zahlkonto == 0:
                    bediener = get_cache(
                        Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.ap_recid = l_kredit._recid
                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.debt = to_decimal(l_kredit.saldo)
                    age_list.netto = to_decimal(l_kredit.netto)
                    age_list.ziel = l_kredit.rgdatum + \
                        timedelta(days=l_kredit.ziel)
                    age_list.lscheinnr = l_kredit.lscheinnr
                    age_list.bemerk = l_kredit.bemerk
                    age_list.tot_debt = to_decimal(
                        age_list.tot_debt) + to_decimal(l_kredit.netto)

                    if l_kredit.name != l_kredit.lscheinnr:
                        l_order = get_cache(L_order, {"lief_nr": [(eq, l_kredit.lief_nr)], "docu_nr": [
                                            (eq, l_kredit.name)], "pos": [(eq, 0)]})

                        if l_order:
                            age_list.rabattbetrag = to_decimal(
                                l_order.warenwert)

                    queasy = get_cache(
                        Queasy, {"key": [(eq, 221)], "char1": [(eq, l_kredit.name)]})

                    if queasy:
                        age_list.recv_date = queasy.date1

                else:
                    age_list.credit = to_decimal(
                        age_list.credit) - to_decimal(l_kredit.saldo)
                    age_list.tot_debt = to_decimal(
                        age_list.tot_debt) + to_decimal(l_kredit.saldo)
                disp_l_lieferant_debt()

                gl_jouhdr = get_cache(
                    Gl_jouhdr, {"refno": [(eq, l_kredit.name)]})

                if gl_jouhdr and l_kredit.zahlkonto == 0:
                    gl_journal = Gl_journal()
                    gl_acct = Gl_acct()
                    for gl_journal.fibukonto, gl_journal.debit, gl_journal.credit, gl_journal.bemerk, gl_journal._recid, gl_acct.bezeich, gl_acct._recid in db_session.query(Gl_journal.fibukonto, Gl_journal.debit, Gl_journal.credit, Gl_journal.bemerk, Gl_journal._recid, Gl_acct.bezeich, Gl_acct._recid).join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto) & ((Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4) | (Gl_acct.acc_type == 5))).filter(
                            (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                        # age_list.comment = age_list.comment + ";" + to_string(gl_journal.fibukonto) + ";" + to_string(l_kredit.steuercode)
                        # yusufwijasena: fix variable name: age_list.comment -> age_list.comments
                        age_list.comments = f"{age_list.comments};{to_string(gl_journal.fibukonto)};{to_string(l_kredit.steuercode)}"
                        age_list.fibukonto = gl_journal.fibukonto
                        age_list.t_bezeich = gl_acct.bezeich

                        if gl_journal.debit > 0:
                            age_list.debt2 = to_decimal(gl_journal.debit)

                        elif gl_journal.credit > 0:
                            age_list.debt2 = - to_decimal((gl_journal.credit))

                        if gl_journal.fibukonto.lower() == (p_986).lower() or gl_journal.fibukonto.lower() == (p_395).lower():
                            pass
                        else:
                            age_list.fibu = age_list.fibu + ";" + gl_journal.fibukonto
                            age_list.remark = age_list.remark + ";" + gl_acct.bezeich
                            age_list.amount = age_list.amount + \
                                ";" + to_string(age_list.debt2)
                            age_list.remark_manual = age_list.remark_manual + ";" + gl_journal.bemerk

                age_list.is_manual = l_kredit.steuercode

        art_selected = 1

    def disp_l_lieferant_debt():
        nonlocal outstand, age_list_data, t_l_lieferant_data, i, p_986, p_395, htparam, l_lieferant, artikel, l_kredit, bediener, queasy, gl_jouhdr, gl_acct, gl_journal, l_order
        nonlocal art_selected, bill_name, bill_date
        nonlocal age_list, t_l_lieferant
        nonlocal age_list_data, t_l_lieferant_data

        lief_nr: int = 0
        
        # log_program.write_log('LOG', f'age_list_data processed: {len(age_list_data)}')

        if age_list:
            lief_nr = age_list.lief_nr

            l_lieferant = get_cache(L_lieferant, {"lief_nr": [(eq, lief_nr)]})

            age_list.resname = l_lieferant.firma + ", " + l_lieferant.anredefirma + chr_unicode(10) +\
                l_lieferant.adresse1 + \
                chr_unicode(10) + l_lieferant.wohnort + " " + l_lieferant.plz
            age_list.comments = age_list.bemerk

    htparam = get_cache(Htparam, {"paramnr": [(eq, 986)]})
    

    if htparam:
        p_986 = htparam.fchar

    htparam = get_cache(Htparam, {"paramnr": [(eq, 395)]})
    

    if htparam:
        p_395 = htparam.fchar

    if bill_name == "":
        create_age_list()
    else:
        create_age_list1()

    for age_list in query(age_list_data):
        l_lieferant = get_cache(
            L_lieferant, {"lief_nr": [(eq, age_list.lief_nr)]})

        if l_lieferant:
            t_l_lieferant = query(t_l_lieferant_data, filters=(
                lambda t_l_lieferant: t_l_lieferant.lief_nr == l_lieferant.lief_nr), first=True)

            if not t_l_lieferant:
                t_l_lieferant = T_l_lieferant()
                t_l_lieferant_data.append(t_l_lieferant)

                t_l_lieferant.telefon = l_lieferant.telefon
                t_l_lieferant.fax = l_lieferant.fax
                t_l_lieferant.adresse1 = l_lieferant.adresse1
                t_l_lieferant.notizen_1 = l_lieferant.notizen[0]
                t_l_lieferant.lief_nr = l_lieferant.lief_nr
                

    return generate_output()
