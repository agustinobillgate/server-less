#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr, L_op, L_ophis, L_ophhis, Artikel, L_artikel, L_order, Htparam, L_lieferant, Fa_op, Parameters, Zwkum, L_untergrup, Fa_artikel, Fa_grup
from sqlalchemy import func

coa_list_data, Coa_list = create_model("Coa_list", {"old_fibu":string, "new_fibu":string, "bezeich":string, "coastat":int, "old_main":int, "new_main":int, "bezeichm":string, "old_dept":int, "new_dept":int, "bezeichd":string, "catno":int, "acct":int, "old_acct":int}, {"coastat": -1})

def mapping_coa_1bl(coa_list_data:[Coa_list]):

    prepare_cache ([L_ophdr, L_op, L_ophis, L_ophhis, Artikel, L_artikel, L_order, Htparam, L_lieferant, Fa_op, Parameters, Zwkum, L_untergrup, Fa_artikel, Fa_grup])

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

        l_op = get_cache (L_op, {"op_art": [(eq, 3)],"stornogrund": [(ne, "")]})
        while None != l_op:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_op.stornogrund and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # l_opbuff = get_cache (L_op, {"_recid": [(eq, l_op._recid)]})
                l_opbuff = db_session.query(L_op).filter(L_op._recid == l_op._recid).with_for_update().first()
                l_opbuff.stornogrund = coa_list.new_fibu


                pass
                pass

            curr_recid = l_op._recid
            l_op = db_session.query(L_op).filter(
                     (L_op.op_art == 3) & (L_op.stornogrund != "") & (L_op._recid > curr_recid)).first()

        l_ophis = get_cache (L_ophis, {"op_art": [(eq, 3)],"fibukonto": [(ne, "")]})
        while None != l_ophis:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_ophis.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # l_ophisbuff = get_cache (L_ophis, {"_recid": [(eq, l_ophis._recid)]})
                l_ophisbuff = db_session.query(L_ophis).filter(L_ophis._recid == l_ophis._recid).with_for_update().first()
                l_ophisbuff.fibukonto = coa_list.new_fibu

            curr_recid = l_ophis._recid
            l_ophis = db_session.query(L_ophis).filter(
                     (L_ophis.op_art == 3) & (L_ophis.fibukonto != "") & (L_ophis._recid > curr_recid)).first()

        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "stt")],"fibukonto": [(ne, "")]})
        while None != l_ophdr:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_ophdr.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list: 
                # Rd, 25/11/2025, add .with_for_update
                # l_ophdrbuff = get_cache (L_ophdr, {"_recid": [(eq, l_ophdr._recid)]})
                l_ophdrbuff = db_session.query(L_ophdr).filter(L_ophdr._recid == l_ophdr._recid).with_for_update().first()
                l_ophdrbuff.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = l_ophdr._recid
            l_ophdr = db_session.query(L_ophdr).filter(
                     (func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.fibukonto != "") & (L_ophdr._recid > curr_recid)).first()

        l_ophhis = get_cache (L_ophhis, {"op_typ": [(eq, "stt")],"fibukonto": [(ne, "")]})
        while None != l_ophhis:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_ophhis.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # l_ophhisbuff = get_cache (L_ophhis, {"_recid": [(eq, l_ophhis._recid)]})
                l_ophhisbuff = db_session.query(L_ophhis).filter(L_ophhis._recid == l_ophhis._recid).with_for_update().first()
                l_ophhisbuff.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = l_ophhis._recid
            l_ophhis = db_session.query(L_ophhis).filter(
                     (func.lower(L_ophhis.op_typ) == ("STT").lower()) & (L_ophhis.fibukonto != "") & (L_ophhis._recid > curr_recid)).first()


    def update_order():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        l_order = get_cache (L_order, {"stornogrund": [(ne, "")]})
        while None != l_order:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_order.stornogrund and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # lodbuff = get_cache (L_order, {"_recid": [(eq, l_order._recid)]})
                lodbuff = db_session.query(L_order).filter(L_order._recid == l_order._recid).with_for_update().first()
                lodbuff.stornogrund = coa_list.new_fibu


                pass
                pass

            curr_recid = l_order._recid
            l_order = db_session.query(L_order).filter(
                     (L_order.stornogrund != "") & (L_order._recid > curr_recid)).first()


    def update_supplier():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        l_lieferant = get_cache (L_lieferant, {"z_code": [(ne, "")]})
        while None != l_lieferant:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_lieferant.z_code and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # suppbuff = get_cache (L_lieferant, {"_recid": [(eq, l_lieferant._recid)]})
                suppbuff = db_session.query(L_lieferant).filter(L_lieferant._recid == l_lieferant._recid).with_for_update().first()
                suppbuff.z_code = coa_list.new_fibu


                pass
                pass

            curr_recid = l_lieferant._recid
            l_lieferant = db_session.query(L_lieferant).filter(
                     (L_lieferant.z_code != "") & (L_lieferant._recid > curr_recid)).first()


    def update_parameters():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")]})
        while None != parameters:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == parameters.vstring and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # parambuff = get_cache (Parameters, {"_recid": [(eq, parameters._recid)]})
                parambuff = db_session.query(Parameters).filter(Parameters._recid == parameters._recid).with_for_update().first()
                parambuff.vstring = coa_list.new_fibu


                pass
                pass

            curr_recid = parameters._recid
            parameters = db_session.query(Parameters).filter(
                     (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("Alloc").lower()) & (Parameters._recid > curr_recid)).first()


    def update_htparam():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        htparam = get_cache (Htparam, {"fchar": [(ne, "")]})
        while None != htparam:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == htparam.fchar and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # htpbuff = get_cache (Htparam, {"_recid": [(eq, htparam._recid)]})
                htpbuff = db_session.query(Htparam).filter(Htparam._recid == htparam._recid).with_for_update().first()
                htpbuff.fchar = coa_list.new_fibu


                pass
                pass

            curr_recid = htparam._recid
            htparam = db_session.query(Htparam).filter(
                     (Htparam.fchar != "") & (Htparam._recid > curr_recid)).first()


    def update_artikel():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        artikel = db_session.query(Artikel).first()
        while None != artikel:
            # Rd, 25/11/2025, add .with_for_update
            # artbuff = get_cache (Artikel, {"_recid": [(eq, artikel._recid)]})
            artbuff = db_session.query(Artikel).filter(Artikel._recid == artikel._recid).with_for_update().first()

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == artikel.bezeich1 and coa_list.new_fibu != None), first=True)

            if coa_list:
                artbuff.bezeich1 = coa_list.new_fibu

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == artikel.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                artbuff.fibukonto = coa_list.new_fibu


            pass
            pass

            curr_recid = artikel._recid
            artikel = db_session.query(Artikel).filter(Artikel._recid > curr_recid).first()

        zwkum = get_cache (Zwkum, {"fibukonto": [(ne, "")]})
        while None != zwkum:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == zwkum.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # zwkumbuff = get_cache (Zwkum, {"_recid": [(eq, zwkum._recid)]})
                zwkumbuff = db_session.query(Zwkum).filter(Zwkum._recid == zwkum._recid).with_for_update().first()
                zwkumbuff.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = zwkum._recid
            zwkum = db_session.query(Zwkum).filter(
                     (Zwkum.fibukonto != "") & (Zwkum._recid > curr_recid)).first()


    def update_l_artikel():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        l_artikel = get_cache (L_artikel, {"fibukonto": [(ne, "")]})
        while None != l_artikel:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_artikel.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # lartbuff = get_cache (L_artikel, {"_recid": [(eq, l_artikel._recid)]})
                lartbuff = db_session.query(L_artikel).filter(L_artikel._recid == l_artikel._recid).with_for_update().first()
                lartbuff.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = l_artikel._recid
            l_artikel = db_session.query(L_artikel).filter(
                     (L_artikel.fibukonto != "") & (L_artikel._recid > curr_recid)).first()

        l_untergrup = get_cache (L_untergrup, {"fibukonto": [(ne, "")]})
        while None != l_untergrup:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == l_untergrup.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # lzwkumbuff = get_cache (L_untergrup, {"_recid": [(eq, l_untergrup._recid)]})
                lzwkumbuff = db_session.query(L_untergrup).filter(L_untergrup._recid == l_untergrup._recid).with_for_update().first()
                lzwkumbuff.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = l_untergrup._recid
            l_untergrup = db_session.query(L_untergrup).filter(
                     (L_untergrup.fibukonto != "") & (L_untergrup._recid > curr_recid)).first()


    def update_fa_artikel():

        nonlocal l_ophdr, l_op, l_ophis, l_ophhis, artikel, l_artikel, l_order, htparam, l_lieferant, fa_op, parameters, zwkum, l_untergrup, fa_artikel, fa_grup
        nonlocal l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff


        nonlocal coa_list, l_ophdrbuff, l_opbuff, l_ophisbuff, l_ophhisbuff, l_hhisbuff, artbuff, lartbuff, lodbuff, htpbuff, suppbuff, faopbuff, parambuff, zwkumbuff, lzwkumbuff, fa_artbuff, fa_zwbuff

        fa_artikel = db_session.query(Fa_artikel).first()
        while None != fa_artikel:
            # Rd, 25/11/2025, add .with_for_update
            # fa_artbuff = get_cache (Fa_artikel, {"_recid": [(eq, fa_artikel._recid)]})
            fa_artbuff = db_session.query(Fa_artikel).filter(Fa_artikel._recid == fa_artikel._recid).with_for_update().first()

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == fa_artikel.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_artbuff.fibukonto = coa_list.new_fibu

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == fa_artikel.credit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_artbuff.credit_fibu = coa_list.new_fibu

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == fa_artikel.debit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_artbuff.debit_fibu = coa_list.new_fibu


            pass
            pass

            curr_recid = fa_artikel._recid
            fa_artikel = db_session.query(Fa_artikel).filter(Fa_artikel._recid > curr_recid).first()

        fa_grup = db_session.query(Fa_grup).first()
        while None != fa_grup:
            # Rd, 25/11/2025, add .with_for_update
            # fa_zwbuff = get_cache (Fa_grup, {"_recid": [(eq, fa_grup._recid)]})
            fa_zwbuff = db_session.query(Fa_grup).filter(Fa_grup._recid == fa_grup._recid).with_for_update().first()

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == fa_grup.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_zwbuff.fibukonto = coa_list.new_fibu

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == fa_grup.credit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_zwbuff.credit_fibu = coa_list.new_fibu

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == fa_grup.debit_fibu and coa_list.new_fibu != None), first=True)

            if coa_list:
                fa_zwbuff.debit_fibu = coa_list.new_fibu


            pass
            pass

            curr_recid = fa_grup._recid
            fa_grup = db_session.query(Fa_grup).filter(Fa_grup._recid > curr_recid).first()

        fa_op = get_cache (Fa_op, {"fibukonto": [(ne, "")]})
        while None != fa_op:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == fa_op.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                # Rd, 25/11/2025, add .with_for_update
                # faopbuff = get_cache (Fa_op, {"_recid": [(eq, fa_op._recid)]})
                faopbuff = db_session.query(Fa_op).filter(Fa_op._recid == fa_op._recid).with_for_update().first()
                faopbuff.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = fa_op._recid
            fa_op = db_session.query(Fa_op).filter(
                     (Fa_op.fibukonto != "") & (Fa_op._recid > curr_recid)).first()

    update_lop()
    update_order()
    update_supplier()
    update_parameters()
    update_htparam()
    update_artikel()
    update_l_artikel()
    update_fa_artikel()

    return generate_output()