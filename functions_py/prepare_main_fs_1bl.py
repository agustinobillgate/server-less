#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 22/7/2025
# gitlab: 606
# Quick&Dirdy function Query (need to fix later)
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bk_reser, Bk_func, Bk_veran, Guest, Akt_kont

def filter_query(
    data_list: List[Type], 
    filters: Callable[[Type], bool] = None, 
    sort_by: Optional[List[Tuple[str, bool]]] = None,
    first: bool = False,
    last: bool = False,
    curr_data: Type = None
) -> Union[Type, List[Type], None]:
    if not data_list:
        return None if first or last else []

    if first or last and not filters:
        return data_list[0] if first else data_list[-1]

    if filters:
        data_list = list(filter(filters, data_list))
    
    if not data_list:
        return None if first or last else []

    if sort_by:
        class SortWrapper:
            def __init__(self, value):
                self.value = value
            def __lt__(self, other):
                return self.value > other.value
            def __eq__(self, other):
                return self.value == other.value

        def sort_key(obj):
            key = []
            for field, descending in sort_by:
                val = getattr(obj, field, None)
                if isinstance(val, str):
                    val = val.lower()
                key.append(val if not descending else SortWrapper(val))
            return tuple(key)

        data_list.sort(key=sort_key)

    if first:
        return data_list[0]
    if last:
        return data_list[-1]

    return data_list


def prepare_main_fs_1bl(b1_resnr:int, b1_resline:int, to_date:date):

    prepare_cache ([Bk_reser, Bk_func, Bk_veran, Guest, Akt_kont])

    bis_datum = None
    curr_date = None
    ci_date = None
    p_900 = 0
    rsvsort = 0
    resnr = 0
    resline = 0
    search_str = ""
    guestsort = 0
    curr_gastnr = 0
    readequipment = False
    bk_func_recid = 0
    avail_bk_veran = False
    bk_veran_recid = 0
    bk_veran_resstatus = 0
    glist_data = []
    t_htparam_data = []
    htparam = bk_reser = bk_func = bk_veran = guest = akt_kont = None

    glist = t_htparam = b_htparam = None

    glist_data, Glist = create_model("Glist", {"gastnr":int, "karteityp":int, "name":string, "telefon":string, "land":string, "plz":string, "wohnort":string, "adresse1":string, "adresse2":string, "adresse3":string, "namekontakt":string, "von_datum":date, "bis_datum":date, "von_zeit":string, "bis_zeit":string, "rstatus":int, "fax":string, "firmen_nr":int, "func_resstatus":int})
    t_htparam_data, T_htparam = create_model("T_htparam", {"paramnr":int, "paramgr":int, "reihenfolge":int, "bezeich":string, "fieldtyp":int, "finteger":int, "fdecimal":Decimal, "fdate":date, "flogical":bool, "fchar":string, "lupdate":date, "fdefault":string, "htp_help":string})

    B_htparam = create_buffer("B_htparam",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bis_datum, curr_date, ci_date, p_900, rsvsort, resnr, resline, search_str, guestsort, curr_gastnr, readequipment, bk_func_recid, avail_bk_veran, bk_veran_recid, bk_veran_resstatus, glist_data, t_htparam_data, htparam, bk_reser, bk_func, bk_veran, guest, akt_kont
        nonlocal b1_resnr, b1_resline, to_date
        nonlocal b_htparam


        nonlocal glist, t_htparam, b_htparam
        nonlocal glist_data, t_htparam_data

        return {"bis_datum": bis_datum, "curr_date": curr_date, "ci_date": ci_date, "p_900": p_900, "rsvsort": rsvsort, "resnr": resnr, "resline": resline, "search_str": search_str, "guestsort": guestsort, "curr_gastnr": curr_gastnr, "readequipment": readequipment, "bk_func_recid": bk_func_recid, "avail_bk_veran": avail_bk_veran, "bk_veran_recid": bk_veran_recid, "bk_veran_resstatus": bk_veran_resstatus, "glist": glist_data, "t-htparam": t_htparam_data}

    def create_main_page():

        nonlocal bis_datum, curr_date, ci_date, p_900, rsvsort, resnr, resline, search_str, guestsort, curr_gastnr, readequipment, bk_func_recid, avail_bk_veran, bk_veran_recid, bk_veran_resstatus, glist_data, t_htparam_data, htparam, bk_reser, bk_func, bk_veran, guest, akt_kont
        nonlocal b1_resnr, b1_resline, to_date
        nonlocal b_htparam


        nonlocal glist, t_htparam, b_htparam
        nonlocal glist_data, t_htparam_data

        i:int = 0
        ind:int = 0
        name_contact:string = ""
        htparam_date = None
        Htparam_date =  create_buffer("Htparam_date",Htparam)
        glist_data.clear()

        if b1_resnr != 0:
            resnr = b1_resnr
            resline = b1_resline

            bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

            if bk_veran:

                guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})
                search_str = guest.name
                guestsort = guest.karteityp
                curr_gastnr = guest.gastnr

                akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

                if akt_kont:
                    name_contact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
                else:
                    name_contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                glist = query(glist_data, filters=(lambda glist: glist.gastnr == bk_veran.gastnr), first=True)

                if not glist:
                    glist = Glist()
                    glist_data.append(glist)

                    glist.gastnr = guest.gastnr
                    glist.karteityp = guest.karteityp
                    glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                    glist.adresse1 = guest.adresse1
                    glist.adresse2 = guest.adresse2
                    glist.adresse3 = guest.adresse3
                    glist.telefon = guest.telefon
                    glist.land = guest.land
                    glist.plz = guest.plz
                    glist.wohnort = guest.wohnort
                    glist.namekontakt = name_contact
                    glist.rstatus = bk_veran.resstatus
                    glist.fax = guest.fax
                    glist.firmen_nr = guest.firmen_nr
                readequipment = True

                return

        bk_veran_obj_list = {}
        bk_veran = Bk_veran()
        guest = Guest()
        bk_reser = Bk_reser()

        # Rd, 22/7/2025
        # make simpler/readable query
        # for bk_veran.gastnr, bk_veran.resstatus, bk_veran.veran_nr, bk_veran._recid, guest.name, guest.karteityp, guest.gastnr, guest.vorname1, guest.anrede1, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.land, guest.plz, guest.wohnort, guest.fax, guest.firmen_nr, guest._recid, bk_reser.veran_seite, bk_reser.datum, bk_reser._recid in db_session.query(Bk_veran.gastnr, Bk_veran.resstatus, Bk_veran.veran_nr, Bk_veran._recid, Guest.name, Guest.karteityp, Guest.gastnr, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.land, Guest.plz, Guest.wohnort, Guest.fax, Guest.firmen_nr, Guest._recid, Bk_reser.veran_seite, Bk_reser.datum, Bk_reser._recid).join(Guest,(Guest.gastnr == Bk_veran.gastnr)).join(Bk_reser,(Bk_reser.veran_nr == Bk_veran.veran_nr) & (Bk_reser.resstatus <= 3)).filter(
        #          (Bk_veran.limit_date <= to_date) & (Bk_veran.activeflag == 0)).order_by(Guest.karteityp, Guest.name).all():
        # Build initial query with joins
        query = db_session.query(
            Bk_veran.gastnr, Bk_veran.resstatus, Bk_veran.veran_nr, Bk_veran._recid,
            Guest.name, Guest.karteityp, Guest.gastnr, Guest.vorname1, Guest.anrede1, 
            Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, 
            Guest.telefon, Guest.land, Guest.plz, Guest.wohnort, Guest.fax, 
            Guest.firmen_nr, Guest._recid,
            Bk_reser.veran_seite, Bk_reser.datum, Bk_reser._recid
        ).join(Guest, Guest.gastnr == Bk_veran.gastnr
        ).join(Bk_reser, (Bk_reser.veran_nr == Bk_veran.veran_nr) & (Bk_reser.resstatus <= 3)
        ).filter(Bk_veran.activeflag == 0)

        # Add conditional filter if to_date is provided
        if to_date:
            query = query.filter(Bk_veran.limit_date <= to_date)

        # Execute ordered query
        for record in query.order_by(Guest.karteityp, Guest.name).all():
            # unpack record clearly
            (veran_gastnr, veran_resstatus, veran_veran_nr, veran_recid,
            guest_name, guest_karteityp, guest_gastnr, guest_vorname1, guest_anrede1,
            guest_anredefirma, guest_adresse1, guest_adresse2, guest_adresse3, guest_telefon,
            guest_land, guest_plz, guest_wohnort, guest_fax, guest_firmen_nr, guest_recid,
            reser_veran_seite, reser_datum, reser_recid) = record


            if bk_veran_obj_list.get(bk_veran._recid):
                continue
            else:
                bk_veran_obj_list[bk_veran._recid] = True


            ind = ind + 1

            if ind == 1:
                resnr = bk_veran.veran_nr
                resline = bk_reser.veran_seite

            akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

            if akt_kont:
                name_contact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
            else:
                name_contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

            # glist = query(glist_data, filters=(lambda glist: glist.gastnr == bk_veran.gastnr), first=True)
            glist = filter_query(
                glist_data, 
                filters=lambda g: g.gastnr == bk_veran.gastnr, 
                first=True
            )

            if not glist:
                guestsort = guest.karteityp
                glist = Glist()
                glist_data.append(glist)

                glist.gastnr = guest.gastnr
                glist.karteityp = guest.karteityp
                glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                glist.adresse1 = guest.adresse1
                glist.adresse2 = guest.adresse2
                glist.adresse3 = guest.adresse3
                glist.telefon = guest.telefon
                glist.land = guest.land
                glist.plz = guest.plz
                glist.wohnort = guest.wohnort
                glist.namekontakt = name_contact
                glist.rstatus = bk_veran.resstatus
                glist.fax = guest.fax
                glist.firmen_nr = guest.firmen_nr
        readequipment = True

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

        if not bk_veran:

            return

        guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_seite": [(eq, resline)]})

    if b1_resnr > 0:

        for bk_reser in db_session.query(Bk_reser).filter(
                 (Bk_reser.veran_nr == b1_resnr)).order_by(Bk_reser.datum).all():
            bis_datum = bk_reser.datum

    else:
        bis_datum = to_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

    if htparam:
        p_900 = htparam.finteger
    t_htparam_data.clear()

    for b_htparam in db_session.query(B_htparam).order_by(B_htparam._recid).all():
        t_htparam = T_htparam()
        t_htparam_data.append(t_htparam)

        buffer_copy(b_htparam, t_htparam)

    if b1_resnr != 0:

        bk_reser_obj_list = {}
        bk_reser = Bk_reser()
        bk_func = Bk_func()

        # Rd 22/7/2025
        # make readable query
        # for bk_reser.veran_seite, bk_reser.datum, bk_reser._recid, bk_func.resstatus, bk_func._recid in db_session.query(Bk_reser.veran_seite, Bk_reser.datum, Bk_reser._recid, Bk_func.resstatus, Bk_func._recid).join(Bk_func,(Bk_func.veran_nr == Bk_reser.veran_nr) & (Bk_func.veran_seite == Bk_reser.veran_resnr)).filter(
        #          (Bk_reser.veran_nr == b1_resnr) & (Bk_reser.veran_resnr == b1_resline)).order_by(Bk_reser._recid).all():
        query = db_session.query(
            Bk_reser.veran_seite, 
            Bk_reser.datum, 
            Bk_reser._recid, 
            Bk_func.resstatus, 
            Bk_func._recid
        ).join(
            Bk_func,
            (Bk_func.veran_nr == Bk_reser.veran_nr) &
            (Bk_func.veran_seite == Bk_reser.veran_resnr)
        ).filter(
            Bk_reser.veran_nr == b1_resnr,
            Bk_reser.veran_resnr == b1_resline
        ).order_by(Bk_reser._recid)

        # iterate through results
        for reser_veran_seite, reser_datum, reser_recid, func_resstatus, func_recid in query.all():
            if bk_reser_obj_list.get(bk_reser._recid):
                continue
            else:
                bk_reser_obj_list[bk_reser._recid] = True


            rsvsort = bk_func.resstatus
    create_main_page()

    if bk_veran:
        avail_bk_veran = True
        bk_veran_recid = bk_veran._recid
        bk_veran_resstatus = bk_veran.resstatus

    if bk_func:
        bk_func_recid = bk_func._recid

    return generate_output()