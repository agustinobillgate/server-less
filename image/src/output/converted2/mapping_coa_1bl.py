from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr, L_op, L_ophis, L_ophhis, Artikel, L_artikel, L_order, Htparam, L_lieferant, Fa_op, Parameters, Zwkum, L_untergrup, Fa_artikel, Fa_grup

coa_list_list, Coa_list = create_model("Coa_list", {"old_fibu":str, "new_fibu":str, "bezeich":str, "coastat":int, "old_main":int, "new_main":int, "bezeichm":str, "old_dept":int, "new_dept":int, "bezeichd":str, "catno":int, "acct":int, "old_acct":int}, {"coastat": -1})

def mapping_coa_1bl(coa_list_list:[Coa_list]):
    l_ophdr = l_op = l_ophis = l_ophhis = artikel = l_artikel = l_order = htparam = l_lieferant = fa_op = parameters = zwkum = l_untergrup = fa_artikel = fa_grup = None

    coa_list = l_ophdrbuff = l_opbuff = l_ophisbuff = l_ophhisbuff = l_hhisbuff = artbuff = lartbuff = lodbuff = htpbuff = suppbuff = faopbuff = parambuff = zwkumbuff = lzwkumbuff = fa_artbuff = fa_zwbuff = None

    L_ophdrbuff = create_buffer("L_ophdrbuff",L_ophdr)
    L_opbuff = create_buffer("L_opbuff",L_op)
    L_ophisbuff = create_buffer("L_ophisbuff",L_ophis)
    L_ophhisbuff = create_buffer("L_ophhisbuff",L_ophhis)
    L_hhisbuff = create_buffer("L_hhisbuff",L_ophhis)
    Artbuff = create_buffer("Artbuff",Artikel)
    Lartbuff = create_buffer("Lartbuff",L_artikel)
    Lodbuff = create_buffer("Lodbuff",L_order)
    Htpbuff = create_buffer("Htpbuff",Htparam)
    Suppbuff = create_buffer("Suppbuff",L_lieferant)
    Faopbuff = create_buffer("Faopbuff",Fa_op)
    Parambuff = create_buffer("Parambuff",Parameters)
    Zwkumbuff = create_buffer("Zwkumbuff",Zwkum)
    Lzwkumbuff = create_buffer("Lzwkumbuff",L_untergrup)
    Fa_artbuff = create_buffer("Fa_artbuff",Fa_artikel)
    Fa_zwbuff = create_buffer("Fa_zwbuff",Fa_grup)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        return {}

    def update_lop():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        l_op = db_session.query(L_op).filter(
                 (L_op.op_art == 3) & (L_op.stornogrund != "")).first()
        while None != l_op:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_op.stornogrund and coa_list.new_fibu != None), first=True)

            if coa_list:

                l_opbuff = db_session.query(L_opbuff).filter(
                         (L_opbuff._recid == l_op._recid)).first()
                l_opbuff.stornogrund = coa_list.new_fibu


                pass

            curr_recid = l_op._recid
            l_op = db_session.query(L_op).filter(
                     (L_op.op_art == 3) & (L_op.stornogrund != "")).filter(L_op._recid > curr_recid).first()

        l_ophis = db_session.query(L_ophis).filter(
                 (L_ophis.op_art == 3) & (L_ophis.fibukonto != "")).first()
        while None != l_ophis:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_ophis.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                l_ophisbuff = db_session.query(L_ophisbuff).filter(
                         (L_ophisbuff._recid == l_ophis._recid)).first()
                l_ophisbuff.fibukonto = coa_list.new_fibu


                pass

            curr_recid = l_ophis._recid
            l_ophis = db_session.query(L_ophis).filter(
                     (L_ophis.op_art == 3) & (L_ophis.fibukonto != "")).filter(L_ophis._recid > curr_recid).first()

        l_ophdr = db_session.query(L_ophdr).filter(
                 (func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.fibukonto != "")).first()
        while None != l_ophdr:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_ophdr.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                l_ophdrbuff = db_session.query(L_ophdrbuff).filter(
                         (L_ophdrbuff._recid == l_ophdr._recid)).first()
                l_ophdrbuff.fibukonto = coa_list.new_fibu


                pass

            curr_recid = l_ophdr._recid
            l_ophdr = db_session.query(L_ophdr).filter(
                     (func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.fibukonto != "")).filter(L_ophdr._recid > curr_recid).first()

        l_ophhis = db_session.query(L_ophhis).filter(
                 (func.lower(L_ophhis.op_typ) == ("STT").lower()) & (L_ophhis.fibukonto != "")).first()
        while None != l_ophhis:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_ophhis.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                l_ophhisbuff = db_session.query(L_ophhisbuff).filter(
                         (L_ophhisbuff._recid == l_ophhis._recid)).first()
                l_ophhisbuff.fibukonto = coa_list.new_fibu


                pass

            curr_recid = l_ophhis._recid
            l_ophhis = db_session.query(L_ophhis).filter(
                     (func.lower(L_ophhis.op_typ) == ("STT").lower()) & (L_ophhis.fibukonto != "")).filter(L_ophhis._recid > curr_recid).first()


    def update_order():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        l_order = db_session.query(L_order).filter(
                 (L_order.stornogrund != "")).first()
        while None != l_order:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_order.stornogrund and coa_list.new_fibu != None), first=True)

            if coa_list:

                lodbuff = db_session.query(Lodbuff).filter(
                         (lodBuff._recid == l_order._recid)).first()
                lodbuff.stornogrund = coa_list.new_fibu


                pass

            curr_recid = l_order._recid
            l_order = db_session.query(L_order).filter(
                     (L_order.stornogrund != "")).filter(L_order._recid > curr_recid).first()


    def update_supplier():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        l_lieferant = db_session.query(L_lieferant).filter(
                 (L_lieferant.z_code != "")).first()
        while None != l_lieferant:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_lieferant.z_code and coa_list.new_fibu != None), first=True)

            if coa_list:

                suppbuff = db_session.query(Suppbuff).filter(
                         (suppBuff._recid == l_lieferant._recid)).first()
                suppbuff.z_code = coa_list.new_fibu


                pass

            curr_recid = l_lieferant._recid
            l_lieferant = db_session.query(L_lieferant).filter(
                     (L_lieferant.z_code != "")).filter(L_lieferant._recid > curr_recid).first()


    def update_parameters():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        parameters = db_session.query(Parameters).filter(
                 (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("Alloc").lower())).first()
        while None != parameters:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == parameters.vstring and coa_list.new_fibu != None), first=True)

            if coa_list:

                parambuff = db_session.query(Parambuff).filter(
                         (paramBuff._recid == parameters._recid)).first()
                parambuff.vstring = coa_list.new_fibu


                pass

            curr_recid = parameters._recid
            parameters = db_session.query(Parameters).filter(
                     (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("Alloc").lower())).filter(Parameters._recid > curr_recid).first()


    def update_htparam():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        htparam = db_session.query(Htparam).filter(
                 (Htparam.fchar != "")).first()
        while None != htparam:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == htparam.fchar and coa_list.new_fibu != None), first=True)

            if coa_list:

                htpbuff = db_session.query(Htpbuff).filter(
                         (htpBuff._recid == htparam._recid)).first()
                htpbuff.fchar = coa_list.new_fibu


                pass

            curr_recid = htparam._recid
            htparam = db_session.query(Htparam).filter(
                     (Htparam.fchar != "")).filter(Htparam._recid > curr_recid).first()


    def update_artikel():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        artikel = db_session.query(Artikel).first()
        while None != artikel:

            artbuff = db_session.query(Artbuff).filter(
                         (artbuff._recid == artikel._recid)).first()

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == artikel.bezeich1 and coa_list.new_fibu != None), first=True)

            if coa_list:
                artbuff.bezeich1 = coa_list.new_fibu

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == artikel.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                artbuff.fibukonto = coa_list.new_fibu


            pass


            curr_recid = artikel._recid
            artikel = db_session.query(Artikel).filter(Artikel._recid > curr_recid).first()

        zwkum = db_session.query(Zwkum).filter(
                 (Zwkum.fibukonto != "")).first()
        while None != zwkum:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == zwkum.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                zwkumbuff = db_session.query(Zwkumbuff).filter(
                         (zwkumBuff._recid == zwkum._recid)).first()
                zwkumbuff.fibukonto = coa_list.new_fibu


                pass

            curr_recid = zwkum._recid
            zwkum = db_session.query(Zwkum).filter(
                     (Zwkum.fibukonto != "")).filter(Zwkum._recid > curr_recid).first()


    def update_l_artikel():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        l_artikel = db_session.query(L_artikel).filter(
                 (L_artikel.fibukonto != "")).first()
        while None != l_artikel:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_artikel.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                lartbuff = db_session.query(Lartbuff).filter(
                         (lartbuff._recid == l_artikel._recid)).first()
                lartbuff.fibukonto = coa_list.new_fibu


                pass

            curr_recid = l_artikel._recid
            l_artikel = db_session.query(L_artikel).filter(
                     (L_artikel.fibukonto != "")).filter(L_artikel._recid > curr_recid).first()

        l_untergrup = db_session.query(L_untergrup).filter(
                 (L_untergrup.fibukonto != "")).first()
        while None != l_untergrup:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == l_untergrup.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                lzwkumbuff = db_session.query(Lzwkumbuff).filter(
                         (lzwkumBuff._recid == l_untergrup._recid)).first()
                lzwkumbuff.fibukonto = coa_list.new_fibu


                pass

            curr_recid = l_untergrup._recid
            l_untergrup = db_session.query(L_untergrup).filter(
                     (L_untergrup.fibukonto != "")).filter(L_untergrup._recid > curr_recid).first()


    def update_fa_artikel():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        fa_artikel = db_session.query(Fa_artikel).first()
        while None != fa_artikel:

            fa_artbuff = db_session.query(Fa_artbuff).filter(
                         (fa_artbuff._recid == fa_artikel._recid)).first()

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == fa_artikel.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_artbuff.fibukonto = coa_list.new_fibu

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == fa_artikel.credit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_artbuff.credit_fibu = coa_list.new_fibu

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == fa_artikel.debit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_artbuff.debit_fibu = coa_list.new_fibu


            pass


            curr_recid = fa_artikel._recid
            fa_artikel = db_session.query(Fa_artikel).filter(Fa_artikel._recid > curr_recid).first()

        fa_grup = db_session.query(Fa_grup).first()
        while None != fa_grup:

            fa_zwbuff = db_session.query(Fa_zwbuff).filter(
                         (fa_zwBuff._recid == fa_grup._recid)).first()

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == fa_grup.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_zwbuff.fibukonto = coa_list.new_fibu

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == fa_grup.credit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_zwbuff.credit_fibu = coa_list.new_fibu

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == fa_grup.debit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_zwbuff.debit_fibu = coa_list.new_fibu


            pass


            curr_recid = fa_grup._recid
            fa_grup = db_session.query(Fa_grup).filter(Fa_grup._recid > curr_recid).first()

        fa_op = db_session.query(Fa_op).filter(
                 (Fa_op.fibukonto != "")).first()
        while None != fa_op:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == fa_op.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                faopbuff = db_session.query(Faopbuff).filter(
                         (faopBuff._recid == fa_op._recid)).first()
                faopbuff.fibukonto = coa_list.new_fibu


                pass

            curr_recid = fa_op._recid
            fa_op = db_session.query(Fa_op).filter(
                     (Fa_op.fibukonto != "")).filter(Fa_op._recid > curr_recid).first()

    update_lop()
    update_order()
    update_supplier()
    update_parameters()
    update_htparam()
    update_artikel()
    update_l_artikel()
    update_fa_artikel()

    return generate_output()