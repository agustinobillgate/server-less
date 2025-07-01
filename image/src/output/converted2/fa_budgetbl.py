#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis, Fa_artikel, Fa_grup, Gl_acct, Fa_op, Htparam

def fa_budgetbl(from_date:date, to_date:date, detailed:bool):

    prepare_cache ([Mathis, Fa_artikel, Fa_grup, Gl_acct, Fa_op, Htparam])

    fa_budget_list = []
    i:int = 0
    c:string = ""
    fibu:string = ""
    beg_date:date = None
    jan:int = 1
    mm:int = 0
    mtd_budget:Decimal = to_decimal("0.0")
    mtd_balance:Decimal = to_decimal("0.0")
    ytd_budget:Decimal = to_decimal("0.0")
    ytd_balance:Decimal = to_decimal("0.0")
    t_anzahl:Decimal = to_decimal("0.0")
    t_warenwert:Decimal = to_decimal("0.0")
    t_mtd_balance:Decimal = to_decimal("0.0")
    t_ytd_balance:Decimal = to_decimal("0.0")
    tt_anzahl:Decimal = to_decimal("0.0")
    tt_warenwert:Decimal = to_decimal("0.0")
    tt_mtd_balance:Decimal = to_decimal("0.0")
    tt_ytd_balance:Decimal = to_decimal("0.0")
    mathis = fa_artikel = fa_grup = gl_acct = fa_op = htparam = None

    fa_budget = None

    fa_budget_list, Fa_budget = create_model("Fa_budget", {"name":string, "asset":string, "datum":date, "bezeich":string, "fibukonto":string, "price":Decimal, "price_str":string, "anzahl":int, "anzahl_str":string, "warenwert":Decimal, "warenwert_str":string, "mtd_budget":Decimal, "mtd_budget_str":string, "mtd_balance":Decimal, "mtd_balance_str":string, "ytd_budget":Decimal, "ytd_budget_str":string, "ytd_balance":Decimal, "ytd_balance_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_budget_list, i, c, fibu, beg_date, jan, mm, mtd_budget, mtd_balance, ytd_budget, ytd_balance, t_anzahl, t_warenwert, t_mtd_balance, t_ytd_balance, tt_anzahl, tt_warenwert, tt_mtd_balance, tt_ytd_balance, mathis, fa_artikel, fa_grup, gl_acct, fa_op, htparam
        nonlocal from_date, to_date, detailed


        nonlocal fa_budget
        nonlocal fa_budget_list

        return {"fa-budget": fa_budget_list}

    def convert_fibu(konto:string):

        nonlocal fa_budget_list, c, fibu, beg_date, jan, mm, mtd_budget, mtd_balance, ytd_budget, ytd_balance, t_anzahl, t_warenwert, t_mtd_balance, t_ytd_balance, tt_anzahl, tt_warenwert, tt_mtd_balance, tt_ytd_balance, mathis, fa_artikel, fa_grup, gl_acct, fa_op, htparam
        nonlocal from_date, to_date, detailed


        nonlocal fa_budget
        nonlocal fa_budget_list

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()

    beg_date = date_mdy(1, 1, get_year(to_date))
    mm = get_month(to_date)

    if detailed:

        fa_op_obj_list = {}
        fa_op = Fa_op()
        mathis = Mathis()
        fa_artikel = Fa_artikel()
        fa_grup = Fa_grup()
        gl_acct = Gl_acct()
        for fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.einzelpreis, fa_op._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid, gl_acct.budget, gl_acct._recid in db_session.query(Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.einzelpreis, Fa_op._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid, Gl_acct.budget, Gl_acct._recid).join(Mathis,(Mathis.nr == Fa_op.nr)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag > 0)).join(Gl_acct,(Gl_acct.fibukonto == Fa_artikel.fibukonto)).filter(
                 (Fa_op.loeschflag <= 1) & (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date)).order_by(Fa_artikel.fibukonto, Fa_op.datum).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True

            if fibu == "":
                mtd_budget =  to_decimal("0")
                ytd_budget =  to_decimal("0")
                c = convert_fibu(fa_artikel.fibukonto)
                mtd_budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1])
                for i in range(jan,mm + 1) :
                    ytd_budget =  to_decimal(ytd_budget) + to_decimal(gl_acct.budget[i - 1])
                fa_budget = Fa_budget()
                fa_budget_list.append(fa_budget)

                fa_budget.bezeich = fa_grup.bezeich + " - " + c
                fa_budget.fibukonto = fa_artikel.fibukonto
                fa_budget.mtd_budget_str = to_string(mtd_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget.ytd_budget_str = to_string(ytd_budget, "->>>,>>>,>>>,>>>,>>9.99")


                fibu = fa_artikel.fibukonto
                t_anzahl =  to_decimal("0")
                t_warenwert =  to_decimal("0")
                t_mtd_balance =  to_decimal("0")
                t_ytd_balance =  to_decimal("0")

            if fibu != fa_artikel.fibukonto:
                c = convert_fibu(fa_artikel.fibukonto)
                fa_budget = Fa_budget()
                fa_budget_list.append(fa_budget)

                fa_budget.bezeich = "T O T A L"
                fa_budget.fibukonto = fa_artikel.fibukonto
                fa_budget.anzahl_str = to_string(t_anzahl, "->>>,>>9")
                fa_budget.warenwert_str = to_string(t_warenwert, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget.mtd_budget_str = to_string(mtd_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget.mtd_balance_str = to_string(mtd_balance, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget.ytd_budget_str = to_string(ytd_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget.ytd_balance_str = to_string(ytd_balance, "->>>,>>>,>>>,>>>,>>9.99")


                mtd_budget =  to_decimal("0")
                ytd_budget =  to_decimal("0")
                mtd_budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1])
                for i in range(jan,mm + 1) :
                    ytd_budget =  to_decimal(ytd_budget) + to_decimal(gl_acct.budget[i - 1])
                fa_budget = Fa_budget()
                fa_budget_list.append(fa_budget)

                fa_budget.bezeich = fa_grup.bezeich + " - " + c
                fa_budget.fibukonto = fa_artikel.fibukonto
                fa_budget.mtd_budget_str = to_string(mtd_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget.ytd_budget_str = to_string(ytd_budget, "->>>,>>>,>>>,>>>,>>9.99")


                fibu = fa_artikel.fibukonto
                t_anzahl =  to_decimal("0")
                t_warenwert =  to_decimal("0")
                t_mtd_balance =  to_decimal("0")
                t_ytd_balance =  to_decimal("0")
            t_anzahl =  to_decimal(t_anzahl) + to_decimal(fa_op.anzahl)
            t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
            mtd_balance = ( to_decimal(mtd_budget) - to_decimal(t_warenwert) )
            ytd_balance = ( to_decimal(ytd_budget) - to_decimal(t_warenwert) )
            t_mtd_balance =  to_decimal(t_mtd_balance) + to_decimal(mtd_balance)
            t_ytd_balance =  to_decimal(t_ytd_balance) + to_decimal(ytd_balance)
            tt_anzahl =  to_decimal(tt_anzahl) + to_decimal(fa_op.anzahl)
            tt_warenwert =  to_decimal(tt_warenwert) + to_decimal(fa_op.warenwert)
            tt_mtd_balance =  to_decimal(tt_mtd_balance) + to_decimal(mtd_balance)
            tt_ytd_balance =  to_decimal(tt_ytd_balance) + to_decimal(ytd_balance)


            fa_budget = Fa_budget()
            fa_budget_list.append(fa_budget)

            fa_budget.bezeich = mathis.name
            fa_budget.datum = fa_op.datum
            fa_budget.fibukonto = fa_artikel.fibukonto
            fa_budget.price_str = to_string(fa_op.einzelpreis, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget.anzahl_str = to_string(fa_op.anzahl, "->>>,>>9")
            fa_budget.warenwert_str = to_string(fa_op.warenwert, "->>>,>>>,>>>,>>>,>>9.99")


        fa_budget = Fa_budget()
        fa_budget_list.append(fa_budget)

        fa_budget.bezeich = "T O T A L"
        fa_budget.anzahl_str = to_string(t_anzahl, "->>>,>>9")
        fa_budget.warenwert_str = to_string(t_warenwert, "->>>,>>>,>>>,>>>,>>9.99")
        fa_budget.mtd_budget_str = to_string(mtd_budget, "->>>,>>>,>>>,>>>,>>9.99")
        fa_budget.mtd_balance_str = to_string(mtd_balance, "->>>,>>>,>>>,>>>,>>9.99")
        fa_budget.ytd_budget_str = to_string(ytd_budget, "->>>,>>>,>>>,>>>,>>9.99")
        fa_budget.ytd_balance_str = to_string(ytd_balance, "->>>,>>>,>>>,>>>,>>9.99")


    else:
        mtd_budget =  to_decimal("0")
        ytd_budget =  to_decimal("0")
        fa_budget_list.clear()

        fa_op_obj_list = {}
        fa_op = Fa_op()
        mathis = Mathis()
        fa_artikel = Fa_artikel()
        fa_grup = Fa_grup()
        gl_acct = Gl_acct()
        for fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.einzelpreis, fa_op._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid, gl_acct.budget, gl_acct._recid in db_session.query(Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.einzelpreis, Fa_op._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid, Gl_acct.budget, Gl_acct._recid).join(Mathis,(Mathis.nr == Fa_op.nr)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag > 0)).join(Gl_acct,(Gl_acct.fibukonto == Fa_artikel.fibukonto)).filter(
                 (Fa_op.loeschflag <= 1) & (Fa_op.datum >= beg_date) & (Fa_op.datum <= to_date)).order_by(Fa_artikel.fibukonto, Fa_op.datum).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True

            if fibu != fa_artikel.fibukonto:
                mtd_budget =  to_decimal("0")
                ytd_budget =  to_decimal("0")
                t_anzahl =  to_decimal("0")
                t_warenwert =  to_decimal("0")
                t_mtd_balance =  to_decimal("0")
                t_ytd_balance =  to_decimal("0")
                c = convert_fibu(fa_artikel.fibukonto)
                mtd_budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1])
                for i in range(jan,mm + 1) :
                    ytd_budget =  to_decimal(ytd_budget) + to_decimal(gl_acct.budget[i - 1])

                if fa_op.datum >= from_date and fa_op.datum <= to_date:
                    fa_budget = Fa_budget()
                    fa_budget_list.append(fa_budget)

                    fa_budget.bezeich = fa_grup.bezeich + " - " + c
                    fa_budget.fibukonto = fa_artikel.fibukonto
                    fa_budget.mtd_budget_str = to_string(mtd_budget, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget.ytd_budget_str = to_string(ytd_budget, "->>>,>>>,>>>,>>>,>>9.99")


                    fibu = fa_artikel.fibukonto

            if fa_op.datum >= from_date and fa_op.datum <= to_date:
                t_anzahl =  to_decimal(t_anzahl) + to_decimal(fa_op.anzahl)
                t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
                mtd_balance = ( to_decimal(mtd_budget) - to_decimal(t_warenwert))
            tt_warenwert =  to_decimal(tt_warenwert) + to_decimal(fa_op.warenwert)
            ytd_balance = ( to_decimal(ytd_budget) - to_decimal(tt_warenwert) )
            t_mtd_balance =  to_decimal(t_mtd_balance) + to_decimal(mtd_balance)
            t_ytd_balance =  to_decimal(t_ytd_balance) + to_decimal(ytd_balance)
            fa_budget.anzahl_str = to_string(t_anzahl, "->>>,>>9")
            fa_budget.warenwert_str = to_string(t_warenwert, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget.mtd_balance_str = to_string(mtd_balance, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget.ytd_balance_str = to_string(ytd_balance, "->>>,>>>,>>>,>>>,>>9.99")

    return generate_output()