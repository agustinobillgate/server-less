from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_func, Kresline, Htparam, Bk_raum, Bediener, Bk_rart, Artikel, Masseur

def cure_parser():
    lvcarea:str = "cure-parser"
    gastnr:int = 204
    curr_date:date = None
    printnr:int = 0
    show_it:bool = True
    f_resnr:bool = False
    f_lmargin:bool = False
    resloop:int = 0
    arloop:int = 0
    lmargin:int = 1
    nskip:int = 1
    ntab:int = 1
    n:int = 0
    curr_pos:int = 0
    keychar:str = ""
    infile:str = ""
    outfile:str = ""
    texte:str = ""
    sub_text:str = ""
    bk_func = kresline = htparam = bk_raum = bediener = bk_rart = artikel = masseur = None

    bkf = htp_list = loop_list = None

    bkf_list, Bkf = create_model_like(Bk_func)
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":str})
    loop_list_list, Loop_list = create_model("Loop_list", {"texte":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        return {}

    def fill_list():

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 600)).first()
        keychar = htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 30)).order_by(len(Htparam.fchar).desc()).all():
            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.paramnr = htparam.paramnr
            htp_list.fchar = keychar + htparam.fchar


    def analyse_text():

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        i:int = 0
        j:int = 0
        l:int = 0
        found:bool = False
        sub_text = ""
        for i in range(1,len(texte)  + 1) :

            if substring(texte, i - 1, 1) == (keychar).lower() :

                htp_list = query(htp_list_list, first=True)
                while None != htp_list and not found:

                    if htp_list.fchar == substring(texte, i - 1, len(htp_list.fchar)):
                        found = True
                        j = i + len(htp_list.fchar)
                        l = len(texte) - j + 1
                        sub_text = substring(texte, 0, i - 1) + substring(texte, j - 1, l)

                        if trim(sub_text) == ("\\PAR").lower() :
                            sub_text = ""

                        if htp_list.paramnr == 650:
                            resloop = 1

                            if sub_text != "":
                                put_strln(sub_text)

                        elif htp_list.paramnr == 651:
                            resloop = resloop + 1

                        elif htp_list.paramnr == 670:
                            arloop = 1

                            if sub_text != "":
                                put_strln(sub_text)

                        elif htp_list.paramnr == 671:
                            arloop = arloop + 1
                    else:

                        htp_list = query(htp_list_list, next=True)


    def build_text_line(curr_texte:str):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        i:int = 0
        j:int = 1
        n:int = 0
        found:bool = False
        for i in range(1,len(curr_texte)  + 1) :

            if substring(curr_texte, i - 1, 1) == (keychar).lower() :

                if i == len(curr_texte):
                    found = False

                elif substring(curr_texte, i + 1 - 1, 1) == " ":
                    found = False
                else:
                    put_string(substring(curr_texte, j - 1, i - j))
                    i, found = interprete_text(curr_texte, i)
                    j = i + 1
            else:
                found = False

        if not found:
            put_string(substring(curr_texte, j - 1, len(curr_texte) - j + 1))


    def build_loop_line(curr_texte:str):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        i:int = 0
        j:int = 1
        n:int = 0
        found:bool = False
        for i in range(1,len(curr_texte)  + 1) :

            if substring(curr_texte, i - 1, 1) == (keychar).lower() :

                if i == len(curr_texte):
                    found = False

                elif substring(curr_texte, i + 1 - 1, 1) == " ":
                    found = False
                else:
                    put_string(substring(curr_texte, j - 1, i - j))
                    i, found = interprete_text(curr_texte, i)
                    j = i + 1
            else:
                found = False

        if not found:
            put_string(substring(curr_texte, j - 1, len(curr_texte) - j + 1))


    def do_reserve():

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        if sub_text != "":
            put_strln(sub_text)
        loop_list_list.clear()
        resloop = 0


    def do_debitor():

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list


        loop_list_list.clear()
        arloop = 0


    def interprete_text(curr_texte:str, i:int):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        found = False
        j:int = 0

        def generate_inner_output():
            return (i, found)

        j = i

        htp_list = query(htp_list_list, first=True)
        while None != htp_list and not found:

            if htp_list.fchar == substring(curr_texte, j - 1, len(htp_list.fchar)):
                found = True
                i = j + len(htp_list.fchar) - 1
                i = decode_key(curr_texte, htp_list.paramnr, i)

            htp_list = query(htp_list_list, next=True)

        if not found:
            put_string(substring(curr_texte, j - 1, 1))

        return generate_inner_output()


    def decode_key(curr_texte:str, paramnr:int, i:int):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        out_str:str = ""
        status_code:int = 0
        n:int = 0
        m:int = 0

        def generate_inner_output():
            return (i)

        out_str, status_code = decode_key1(paramnr)

        if status_code >= 1 and status_code <= 3:
            i = find_parameter(paramnr, curr_texte, status_code, i)

        if status_code == 1:
            m = curr_pos + 1

            if curr_pos > ntab:
                curr_pos = 1
                for n in range(2,ntab + 1) :
                    put_string(" ")
            else:
                for n in range(m,ntab + 1) :
                    put_string(" ")
            curr_pos = ntab

        elif status_code == 2:
            for n in range(1,nskip + 1) :
                curr_pos = 1

        elif status_code == 3:
            for n in range(1,lmargin + 1) :
                put_string(" ")

        return generate_inner_output()


    def find_parameter(paramnr:int, curr_texte:str, status_code:int, i:int):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        j:int = 0
        n:int = 0
        stopped:bool = False

        def generate_inner_output():
            return (i)


        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == paramnr), first=True)
        j = i + 1
        while not stopped:

            if substring(curr_texte, j - 1, 1) < ("0").lower()  or substring(curr_texte, j - 1, 1) > ("9").lower() :
                stopped = True
            else:
                j = j + 1

        if j > (i + 1):
            j = j - 1
            n = to_int(substring(curr_texte, i + 1 - 1, j - i))

            if status_code == 1:
                ntab = n

            elif status_code == 2:
                nskip = n

            elif status_code == 3:
                lmargin = n
            i = j

        return generate_inner_output()


    def decode_key1(paramnr:int):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        out_str = ""
        status_code = 0
        summe:decimal = to_decimal("0.0")
        str:str = ""
        i:int = 0
        a:str = ""

        def generate_inner_output():
            return (out_str, status_code)


        if paramnr == 1300:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):
                str = str + bkf.uhrzeiten[0] + " " + chr(10)
            put_string(str)

        elif paramnr == 1301:

            bk_raum_obj_list = []
            for bk_raum in db_session.query(Bk_raum).filter(
                     ((Bk_raum.raum.in_(list(set([bkf.raeume[0 for bkf in bkf_list]])))))).order_by(bkf.veran_seite).all():
                if bk_raum._recid in bk_raum_obj_list:
                    continue
                else:
                    bk_raum_obj_list.append(bk_raum._recid)


                str = str + bk_raum.bezeich + " " + chr(10)
            put_string(str)

        elif paramnr == 1302:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):

                if bkf.rpreis[0] != 0:
                    str = str + "Rp. " + to_string(bkf.rpreis[0], ">>>,>>>,>>>") + " nett/total" + " " + chr(10)

                if bkf.rpreis[6] != 0:
                    str = str + "Rp. " + to_string(bkf.rpreis[6], ">>>,>>>,>>>") + " nett/pax" + " " + chr(10)
            put_string(str)

        elif paramnr == 1303:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):

                if bkf.rpreis[6] != 0:
                    str = str + to_string(bkf.rpreis[6], ">>>,>>>,>>>") + " " + chr(10)
                else:
                    str = str + " - " + " " + chr(10)
            put_string(str)

        elif paramnr == 1304:

            if bk_func.rpreis[7] != 0:
                str = to_string(bk_func.rpreis[7], ">>>,>>>,>>>")
            else:
                str = "-"
            put_string(str)

        elif paramnr == 1305:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):

                if bkf.rpersonen[0] != 0:
                    str = str + to_string(bkf.rpersonen[0], ">,>>>") + " " + chr(10)
                else:
                    str = str + " - " + " " + chr(10)
            put_string(str)

        elif paramnr == 1306:
            put_string(to_string(bk_func.veran_nr))

        elif paramnr == 1307:
            put_string(to_string(bk_func.veran_seite))

        elif paramnr == 1308:

            if bk_func.sonstiges[0] != "":
                str = bk_func.sonstiges[0]
            else:
                str = ""
            put_string(str)

        elif paramnr == 1309:

            bediener = db_session.query(Bediener).filter(
                     (Bediener.userinit == bk_func.vgeschrieben)).first()

            if bediener:
                put_string(bediener.username)

        elif paramnr == 1310:

            if bk_func.bemerkung != "":
                str = bk_func.bemerkung + " Commission Rp " + to_string(bk_func.rpreis[7], ">>>,>>>,>>9.99")
            else:
                str = ""
            put_string(bk_func.bemerkung)

        elif paramnr == 1311:
            put_string(to_string(bk_func.auf__datum))

        elif paramnr == 1312:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):

                if bk_func.f_menu[0] != "":
                    str = str + to_string(bkf.datum, "99/99/99") + " " + chr(10) + bk_func.f_menu[0] + " " + chr(10)

                if bk_func.menue[0] != "":
                    str = str + bk_func.menue[0] + " " + chr(10)

                if bk_func.menue[1] != "":
                    str = str + bk_func.menue[1] + " " + chr(10)

                if bk_func.menue[2] != "":
                    str = str + bk_func.menue[2] + " " + chr(10)

                if bk_func.menue[3] != "":
                    str = str + bk_func.menue[3] + " " + chr(10)

                if bk_func.menue[4] != "":
                    str = str + bk_func.menue[4] + " " + chr(10)

                if bk_func.menue[5] != "":
                    str = str + bk_func.menue[5]
            put_string(str)

        elif paramnr == 1313:

            if bk_func.geschenk != "":
                str = bk_func.geschenk

            if bk_func.vkontrolliert != "":
                str = str + bk_func.vkontrolliert
            put_string(str)

        elif paramnr == 1314:

            if bk_func.vkontrolliert != "":

                bediener = db_session.query(Bediener).filter(
                         (Bediener.userinit == bk_func.vkontrolliert)).first()

                if bediener:
                    put_string(bediener.username)

        elif paramnr == 1315:
            put_string(to_string(bk_func.bestellt__durch))

        elif paramnr == 1316:

            if bk_func.veranstalteranschrift[0] != "":
                str = bk_func.veranstalteranschrift[0] + " " + chr(10)

            if bk_func.veranstalteranschrift[1] != "":
                str = str + bk_func.veranstalteranschrift[1] + " " + chr(10)

            if bk_func.veranstalteranschrift[2] != "":
                str = str + bk_func.veranstalteranschrift[2] + " " + chr(10)

            if bk_func.veranstalteranschrift[3] != "":
                str = str + bk_func.veranstalteranschrift[3] + " " + chr(10)
            put_string(str)

        elif paramnr == 1317:
            put_string(to_string(bk_func.v_kontaktperson[0]))

        elif paramnr == 1318:
            put_string(to_string(bk_func.v_telefon))

        elif paramnr == 1319:
            put_string(to_string(bk_func.v_telefax))

        elif paramnr == 1320:
            str = bk_func.kartentext[2]
            put_string(str)

        elif paramnr == 1321:
            str = bk_func.kartentext[3]
            put_string(str)

        elif paramnr == 1322:
            str = bk_func.kartentext[0]
            put_string(str)

        elif paramnr == 1323:
            str = bk_func.kartentext[1]
            put_string(str)

        elif paramnr == 1324:
            str = bk_func.kartentext[4]
            put_string(str)

        elif paramnr == 1325:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):
                str = str + bkf.wochentag + " " + chr(10)
            put_string(str)

        elif paramnr == 1326:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):
                str = str + to_string(bkf.datum, "99/99/99") + " " + chr(10)
            put_string(str)

        elif paramnr == 1327:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):
                str = str + bkf.zweck[0] + " " + chr(10)
            put_string(str)

        elif paramnr == 1328:

            for bkf in query(bkf_list, sort_by=[("veran_seite",False)]):

                if bkf.weine[0] != "":
                    str = str + to_string(bkf.datum, "99/99/99") + " " + chr(10) + bkf.weine[0] + " " + chr(10)

                if bkf.weine[1] != "":
                    str = str + bkf.weine[1] + " " + chr(10)

                if bkf.weine[2] != "":
                    str = str + bkf.weine[2] + " " + chr(10)

                if bkf.weine[3] != "":
                    str = str + bkf.weine[3] + " " + chr(10)

                if bkf.weine[4] != "":
                    str = str + bkf.weine[4] + " " + chr(10)

                if bkf.weine[5] != "":
                    str = str + bkf.weine[5]
            put_string(str)

        elif paramnr == 1329:
            put_string(to_string(bk_func.kartentext[5]))

        elif paramnr == 1330:
            put_string(to_string(bk_func.kartentext[6]))

        elif paramnr == 1331:

            bk_raum_obj_list = []
            for bk_raum in db_session.query(Bk_raum).filter(
                     ((Bk_raum.raum.in_(list(set([bkf.raeume[0 for bkf in bkf_list]])))))).order_by(bkf.veran_seite).all():
                if bk_raum._recid in bk_raum_obj_list:
                    continue
                else:
                    bk_raum_obj_list.append(bk_raum._recid)

                bkf = query(bkf_list, (lambda bkf: (bk_raum.raum == bkf.raeume[0])), first=True)
                str = str + to_string(bkf.datum, "99/99/99") + " - " + bkf.tischform[0] + " set up at " + bk_raum.bezeich + " for " + to_string(bkf.rpersonen[0], ">,>>>") + " pax." + " " + chr(10)
            put_string(str)

        elif paramnr == 1332:

            for bk_rart in db_session.query(Bk_rart).filter(
                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():

                if str == "":
                    str = bk_rart.bezeich
                else:
                    str = str + ", " + bk_rart.bezeich
            put_string(str)

        elif paramnr == 1333:
            str = bk_func.sonstiges[1]
            put_string(str)

        elif paramnr == 1334:
            str = bk_func.kartentext[7]
            put_string(str)

        elif paramnr == 1335:

            if bk_func.sonstiges[7] != "":
                str = CAPS (bk_func.sonstiges[7])
            else:
                str = "Selected Department"
            put_string(str)

        if paramnr == 1:

            kresline_obj_list = []
            for kresline, artikel, masseur in db_session.query(Kresline, Artikel, Masseur).join(Artikel,(Artikel.departement == htparam.finteger) & (Artikel.artnr == Kresline.artnr)).join(Masseur,(Masseur.massnr == Kresline.massnr)).filter(
                     (Kresline.gastnr == gastnr) & (Kresline.datum >= curr_date)).order_by(Kresline._recid).all():
                if kresline._recid in kresline_obj_list:
                    continue
                else:
                    kresline_obj_list.append(kresline._recid)


                str = to_string(kresline.datum, "99/99/99") + to_string(kresline.zeit, "99:99") + to_string(artikel.bezeich, "x(24)") + to_string("")
                put_string(str)

        return generate_inner_output()


    def put_string(str:str):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        len_:int = 0
        i:int = 0
        len_ = len(str)
        for i in range(1,len + 1) :
        curr_pos = curr_pos + len


    def put_strln(str:str):

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        len_:int = 0
        i:int = 0
        len_ = len(str)
        for i in range(1,len + 1) :
        curr_pos = 1


    def wword_rtf():

        nonlocal lvcarea, gastnr, curr_date, printnr, show_it, f_resnr, f_lmargin, resloop, arloop, lmargin, nskip, ntab, n, curr_pos, keychar, infile, outfile, texte, sub_text, bk_func, kresline, htparam, bk_raum, bediener, bk_rart, artikel, masseur


        nonlocal bkf, htp_list, loop_list
        nonlocal bkf_list, htp_list_list, loop_list_list

        prog_path:str = ""
        prog_name:str = ""

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 400)).first()

        if htparam.fchar != "":
            prog_path = htparam.fchar
        else:
            prog_path = "\\""program files""\\""microsoft office""\\office\\"

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 405)).first()

        if htparam.fchar != "":
            prog_name = htparam.fchar
        else:
            prog_name = "winword.exe"
        OUTPUT TO "\\runwword.bat"
        OUTPUT CLOSE
        dos silent "\\runwword.bat"
        dos silent "del \\runwword.bat"


    kresline = db_session.query(Kresline).filter(
             (Kresline.gastnr == gastnr) & (Kresline.datum >= datum)).first()

    if not kresline:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 44)).first()
    infile = htparam.fchar
    outfile = "\\VHP-CURE.RTF"
    OUTPUT STREAM s1 TO value (outfile)
    INPUT STREAM s2 from value (infile)
    fill_list()
    while True:
        texte = ""
        IMPORT STREAM s2 unformatted texte
        curr_pos = 1
        analyse_text()

        if arloop == 0 and resloop == 0:

            if f_lmargin:
                for n in range(1,lmargin + 1) :
                    put_string(" ")
            build_text_line(texte)

        elif arloop == 2 or resloop == 2:
            loop_list = Loop_list()
            loop_list_list.append(loop_list)

            loop_list.texte = texte

        elif arloop == 3:
            do_debitor()

        elif resloop == 3:
            do_reserve()

        if arloop == 1:
            arloop = 2

        if resloop == 1:
            resloop = 2
    put_string("\\par }}")
    OUTPUT STREAM s1 CLOSE
    INPUT STREAM s2 CLOSE
    wword_rtf()

    return generate_output()