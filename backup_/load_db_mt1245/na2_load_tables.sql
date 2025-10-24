\echo Loading Table absen 
\copy na2.absen from '/usr1/dump-MT1/CSV/absen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.absen__recid_seq', (SELECT MAX(_recid) FROM na2.absen));
\echo Finish Table absen 
\echo . 
\echo Loading Table akt_code 
\copy na2.akt_code from '/usr1/dump-MT1/CSV/akt-code.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.akt_code__recid_seq', (SELECT MAX(_recid) FROM na2.akt_code));
\echo Finish Table akt_code 
\echo . 
\echo Loading Table akt_cust 
\copy na2.akt_cust from '/usr1/dump-MT1/CSV/akt-cust.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.akt_cust__recid_seq', (SELECT MAX(_recid) FROM na2.akt_cust));
\echo Finish Table akt_cust 
\echo . 
\echo Loading Table akt_kont 
\copy na2.akt_kont from '/usr1/dump-MT1/CSV/akt-kont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.akt_kont__recid_seq', (SELECT MAX(_recid) FROM na2.akt_kont));
\echo Finish Table akt_kont 
\echo . 
\echo Loading Table akt_line 
\copy na2.akt_line from '/usr1/dump-MT1/CSV/akt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.akt_line__recid_seq', (SELECT MAX(_recid) FROM na2.akt_line));
\echo Finish Table akt_line 
\echo . 
\echo Loading Table akthdr 
\copy na2.akthdr from '/usr1/dump-MT1/CSV/akthdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.akthdr__recid_seq', (SELECT MAX(_recid) FROM na2.akthdr));
\echo Finish Table akthdr 
\echo . 
\echo Loading Table aktion 
\copy na2.aktion from '/usr1/dump-MT1/CSV/aktion.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.aktion__recid_seq', (SELECT MAX(_recid) FROM na2.aktion));
update na2.aktion set texte = array_replace(texte,NULL,''); 
\echo Finish Table aktion 
\echo . 
\echo Loading Table ap_journal 
\copy na2.ap_journal from '/usr1/dump-MT1/CSV/ap-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.ap_journal__recid_seq', (SELECT MAX(_recid) FROM na2.ap_journal));
\echo Finish Table ap_journal 
\echo . 
\echo Loading Table apt_bill 
\copy na2.apt_bill from '/usr1/dump-MT1/CSV/apt-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.apt_bill__recid_seq', (SELECT MAX(_recid) FROM na2.apt_bill));
update na2.apt_bill set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table apt_bill 
\echo . 
\echo Loading Table archieve 
\copy na2.archieve from '/usr1/dump-MT1/CSV/archieve.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.archieve__recid_seq', (SELECT MAX(_recid) FROM na2.archieve));
update na2.archieve set char = array_replace(char,NULL,''); 
\echo Finish Table archieve 
\echo . 
\echo Loading Table argt_line 
\copy na2.argt_line from '/usr1/dump-MT1/CSV/argt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.argt_line__recid_seq', (SELECT MAX(_recid) FROM na2.argt_line));
\echo Finish Table argt_line 
\echo . 
\echo Loading Table argtcost 
\copy na2.argtcost from '/usr1/dump-MT1/CSV/argtcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.argtcost__recid_seq', (SELECT MAX(_recid) FROM na2.argtcost));
update na2.argtcost set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtcost 
\echo . 
\echo Loading Table argtstat 
\copy na2.argtstat from '/usr1/dump-MT1/CSV/argtstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.argtstat__recid_seq', (SELECT MAX(_recid) FROM na2.argtstat));
update na2.argtstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtstat 
\echo . 
\echo Loading Table arrangement 
\copy na2.arrangement from '/usr1/dump-MT1/CSV/arrangement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.arrangement__recid_seq', (SELECT MAX(_recid) FROM na2.arrangement));
update na2.arrangement set argt_rgbez2 = array_replace(argt_rgbez2,NULL,''); 
\echo Finish Table arrangement 
\echo . 
\echo Loading Table artikel 
\copy na2.artikel from '/usr1/dump-MT1/CSV/artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.artikel__recid_seq', (SELECT MAX(_recid) FROM na2.artikel));
\echo Finish Table artikel 
\echo . 
\echo Loading Table artprice 
\copy na2.artprice from '/usr1/dump-MT1/CSV/artprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.artprice__recid_seq', (SELECT MAX(_recid) FROM na2.artprice));
\echo Finish Table artprice 
\echo . 
\echo Loading Table b_history 
\copy na2.b_history from '/usr1/dump-MT1/CSV/b-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.b_history__recid_seq', (SELECT MAX(_recid) FROM na2.b_history));
update na2.b_history set anlass = array_replace(anlass,NULL,''); 
update na2.b_history set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update na2.b_history set ape__speisen = array_replace(ape__speisen,NULL,''); 
update na2.b_history set arrival = array_replace(arrival,NULL,''); 
update na2.b_history set c_resstatus = array_replace(c_resstatus,NULL,''); 
update na2.b_history set dance = array_replace(dance,NULL,''); 
update na2.b_history set deko2 = array_replace(deko2,NULL,''); 
update na2.b_history set dekoration = array_replace(dekoration,NULL,''); 
update na2.b_history set digestif = array_replace(digestif,NULL,''); 
update na2.b_history set dinner = array_replace(dinner,NULL,''); 
update na2.b_history set f_menu = array_replace(f_menu,NULL,''); 
update na2.b_history set f_no = array_replace(f_no,NULL,''); 
update na2.b_history set fotograf = array_replace(fotograf,NULL,''); 
update na2.b_history set gaestebuch = array_replace(gaestebuch,NULL,''); 
update na2.b_history set garderobe = array_replace(garderobe,NULL,''); 
update na2.b_history set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update na2.b_history set kaffee = array_replace(kaffee,NULL,''); 
update na2.b_history set kartentext = array_replace(kartentext,NULL,''); 
update na2.b_history set kontaktperson = array_replace(kontaktperson,NULL,''); 
update na2.b_history set kuenstler = array_replace(kuenstler,NULL,''); 
update na2.b_history set menue = array_replace(menue,NULL,''); 
update na2.b_history set menuekarten = array_replace(menuekarten,NULL,''); 
update na2.b_history set musik = array_replace(musik,NULL,''); 
update na2.b_history set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update na2.b_history set nadkarte = array_replace(nadkarte,NULL,''); 
update na2.b_history set ndessen = array_replace(ndessen,NULL,''); 
update na2.b_history set payment_userinit = array_replace(payment_userinit,NULL,''); 
update na2.b_history set personen2 = array_replace(personen2,NULL,''); 
update na2.b_history set raeume = array_replace(raeume,NULL,''); 
update na2.b_history set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update na2.b_history set raummiete = array_replace(raummiete,NULL,''); 
update na2.b_history set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update na2.b_history set service = array_replace(service,NULL,''); 
update na2.b_history set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update na2.b_history set sonstiges = array_replace(sonstiges,NULL,''); 
update na2.b_history set technik = array_replace(technik,NULL,''); 
update na2.b_history set tischform = array_replace(tischform,NULL,''); 
update na2.b_history set tischordnung = array_replace(tischordnung,NULL,''); 
update na2.b_history set tischplan = array_replace(tischplan,NULL,''); 
update na2.b_history set tischreden = array_replace(tischreden,NULL,''); 
update na2.b_history set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update na2.b_history set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update na2.b_history set va_ablauf = array_replace(va_ablauf,NULL,''); 
update na2.b_history set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update na2.b_history set vip = array_replace(vip,NULL,''); 
update na2.b_history set weine = array_replace(weine,NULL,''); 
update na2.b_history set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table b_history 
\echo . 
\echo Loading Table b_oorder 
\copy na2.b_oorder from '/usr1/dump-MT1/CSV/b-oorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.b_oorder__recid_seq', (SELECT MAX(_recid) FROM na2.b_oorder));
\echo Finish Table b_oorder 
\echo . 
\echo Loading Table b_storno 
\copy na2.b_storno from '/usr1/dump-MT1/CSV/b-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.b_storno__recid_seq', (SELECT MAX(_recid) FROM na2.b_storno));
update na2.b_storno set grund = array_replace(grund,NULL,''); 
\echo Finish Table b_storno 
\echo . 
\echo Loading Table ba_rset 
\copy na2.ba_rset from '/usr1/dump-MT1/CSV/ba-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.ba_rset__recid_seq', (SELECT MAX(_recid) FROM na2.ba_rset));
\echo Finish Table ba_rset 
\echo . 
\echo Loading Table ba_setup 
\copy na2.ba_setup from '/usr1/dump-MT1/CSV/ba-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.ba_setup__recid_seq', (SELECT MAX(_recid) FROM na2.ba_setup));
\echo Finish Table ba_setup 
\echo . 
\echo Loading Table ba_typ 
\copy na2.ba_typ from '/usr1/dump-MT1/CSV/ba-typ.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.ba_typ__recid_seq', (SELECT MAX(_recid) FROM na2.ba_typ));
\echo Finish Table ba_typ 
\echo . 
\echo Loading Table bankrep 
\copy na2.bankrep from '/usr1/dump-MT1/CSV/bankrep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bankrep__recid_seq', (SELECT MAX(_recid) FROM na2.bankrep));
update na2.bankrep set anlass = array_replace(anlass,NULL,''); 
update na2.bankrep set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update na2.bankrep set ape__speisen = array_replace(ape__speisen,NULL,''); 
update na2.bankrep set dekoration = array_replace(dekoration,NULL,''); 
update na2.bankrep set digestif = array_replace(digestif,NULL,''); 
update na2.bankrep set fotograf = array_replace(fotograf,NULL,''); 
update na2.bankrep set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update na2.bankrep set kartentext = array_replace(kartentext,NULL,''); 
update na2.bankrep set kontaktperson = array_replace(kontaktperson,NULL,''); 
update na2.bankrep set menue = array_replace(menue,NULL,''); 
update na2.bankrep set menuekarten = array_replace(menuekarten,NULL,''); 
update na2.bankrep set musik = array_replace(musik,NULL,''); 
update na2.bankrep set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update na2.bankrep set ndessen = array_replace(ndessen,NULL,''); 
update na2.bankrep set personen2 = array_replace(personen2,NULL,''); 
update na2.bankrep set raeume = array_replace(raeume,NULL,''); 
update na2.bankrep set raummiete = array_replace(raummiete,NULL,''); 
update na2.bankrep set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update na2.bankrep set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update na2.bankrep set sonstiges = array_replace(sonstiges,NULL,''); 
update na2.bankrep set technik = array_replace(technik,NULL,''); 
update na2.bankrep set tischform = array_replace(tischform,NULL,''); 
update na2.bankrep set tischreden = array_replace(tischreden,NULL,''); 
update na2.bankrep set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update na2.bankrep set weine = array_replace(weine,NULL,''); 
update na2.bankrep set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bankrep 
\echo . 
\echo Loading Table bankres 
\copy na2.bankres from '/usr1/dump-MT1/CSV/bankres.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bankres__recid_seq', (SELECT MAX(_recid) FROM na2.bankres));
update na2.bankres set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table bankres 
\echo . 
\echo Loading Table bediener 
\copy na2.bediener from '/usr1/dump-MT1/CSV/bediener.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bediener__recid_seq', (SELECT MAX(_recid) FROM na2.bediener));
\echo Finish Table bediener 
\echo . 
\echo Loading Table bill 
\copy na2.bill from '/usr1/dump-MT1/CSV/bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bill__recid_seq', (SELECT MAX(_recid) FROM na2.bill));
\echo Finish Table bill 
\echo . 
\echo Loading Table bill_lin_tax 
\copy na2.bill_lin_tax from '/usr1/dump-MT1/CSV/bill-lin-tax.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bill_lin_tax__recid_seq', (SELECT MAX(_recid) FROM na2.bill_lin_tax));
\echo Finish Table bill_lin_tax 
\echo . 
\echo Loading Table bill_line 
\copy na2.bill_line from '/usr1/dump-MT1/CSV/bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bill_line__recid_seq', (SELECT MAX(_recid) FROM na2.bill_line));
\echo Finish Table bill_line 
\echo . 
\echo Loading Table billhis 
\copy na2.billhis from '/usr1/dump-MT1/CSV/billhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.billhis__recid_seq', (SELECT MAX(_recid) FROM na2.billhis));
\echo Finish Table billhis 
\echo . 
\echo Loading Table billjournal 
\copy na2.billjournal from '/usr1/dump-MT1/CSV/billjournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.billjournal__recid_seq', (SELECT MAX(_recid) FROM na2.billjournal));
\echo Finish Table billjournal 
\echo . 
\echo Loading Table bk_beleg 
\copy na2.bk_beleg from '/usr1/dump-MT1/CSV/bk-beleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_beleg__recid_seq', (SELECT MAX(_recid) FROM na2.bk_beleg));
\echo Finish Table bk_beleg 
\echo . 
\echo Loading Table bk_fsdef 
\copy na2.bk_fsdef from '/usr1/dump-MT1/CSV/bk-fsdef.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_fsdef__recid_seq', (SELECT MAX(_recid) FROM na2.bk_fsdef));
\echo Finish Table bk_fsdef 
\echo . 
\echo Loading Table bk_func 
\copy na2.bk_func from '/usr1/dump-MT1/CSV/bk-func.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_func__recid_seq', (SELECT MAX(_recid) FROM na2.bk_func));
update na2.bk_func set anlass = array_replace(anlass,NULL,''); 
update na2.bk_func set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update na2.bk_func set ape__speisen = array_replace(ape__speisen,NULL,''); 
update na2.bk_func set arrival = array_replace(arrival,NULL,''); 
update na2.bk_func set c_resstatus = array_replace(c_resstatus,NULL,''); 
update na2.bk_func set dance = array_replace(dance,NULL,''); 
update na2.bk_func set deko2 = array_replace(deko2,NULL,''); 
update na2.bk_func set dekoration = array_replace(dekoration,NULL,''); 
update na2.bk_func set digestif = array_replace(digestif,NULL,''); 
update na2.bk_func set dinner = array_replace(dinner,NULL,''); 
update na2.bk_func set f_menu = array_replace(f_menu,NULL,''); 
update na2.bk_func set f_no = array_replace(f_no,NULL,''); 
update na2.bk_func set fotograf = array_replace(fotograf,NULL,''); 
update na2.bk_func set gaestebuch = array_replace(gaestebuch,NULL,''); 
update na2.bk_func set garderobe = array_replace(garderobe,NULL,''); 
update na2.bk_func set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update na2.bk_func set kaffee = array_replace(kaffee,NULL,''); 
update na2.bk_func set kartentext = array_replace(kartentext,NULL,''); 
update na2.bk_func set kontaktperson = array_replace(kontaktperson,NULL,''); 
update na2.bk_func set kuenstler = array_replace(kuenstler,NULL,''); 
update na2.bk_func set menue = array_replace(menue,NULL,''); 
update na2.bk_func set menuekarten = array_replace(menuekarten,NULL,''); 
update na2.bk_func set musik = array_replace(musik,NULL,''); 
update na2.bk_func set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update na2.bk_func set nadkarte = array_replace(nadkarte,NULL,''); 
update na2.bk_func set ndessen = array_replace(ndessen,NULL,''); 
update na2.bk_func set personen2 = array_replace(personen2,NULL,''); 
update na2.bk_func set raeume = array_replace(raeume,NULL,''); 
update na2.bk_func set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update na2.bk_func set raummiete = array_replace(raummiete,NULL,''); 
update na2.bk_func set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update na2.bk_func set service = array_replace(service,NULL,''); 
update na2.bk_func set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update na2.bk_func set sonstiges = array_replace(sonstiges,NULL,''); 
update na2.bk_func set technik = array_replace(technik,NULL,''); 
update na2.bk_func set tischform = array_replace(tischform,NULL,''); 
update na2.bk_func set tischordnung = array_replace(tischordnung,NULL,''); 
update na2.bk_func set tischplan = array_replace(tischplan,NULL,''); 
update na2.bk_func set tischreden = array_replace(tischreden,NULL,''); 
update na2.bk_func set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update na2.bk_func set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update na2.bk_func set va_ablauf = array_replace(va_ablauf,NULL,''); 
update na2.bk_func set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update na2.bk_func set vip = array_replace(vip,NULL,''); 
update na2.bk_func set weine = array_replace(weine,NULL,''); 
update na2.bk_func set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bk_func 
\echo . 
\echo Loading Table bk_package 
\copy na2.bk_package from '/usr1/dump-MT1/CSV/bk-package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_package__recid_seq', (SELECT MAX(_recid) FROM na2.bk_package));
\echo Finish Table bk_package 
\echo . 
\echo Loading Table bk_pause 
\copy na2.bk_pause from '/usr1/dump-MT1/CSV/bk-pause.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_pause__recid_seq', (SELECT MAX(_recid) FROM na2.bk_pause));
\echo Finish Table bk_pause 
\echo . 
\echo Loading Table bk_rart 
\copy na2.bk_rart from '/usr1/dump-MT1/CSV/bk-rart.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_rart__recid_seq', (SELECT MAX(_recid) FROM na2.bk_rart));
\echo Finish Table bk_rart 
\echo . 
\echo Loading Table bk_raum 
\copy na2.bk_raum from '/usr1/dump-MT1/CSV/bk-raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_raum__recid_seq', (SELECT MAX(_recid) FROM na2.bk_raum));
\echo Finish Table bk_raum 
\echo . 
\echo Loading Table bk_reser 
\copy na2.bk_reser from '/usr1/dump-MT1/CSV/bk-reser.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_reser__recid_seq', (SELECT MAX(_recid) FROM na2.bk_reser));
\echo Finish Table bk_reser 
\echo . 
\echo Loading Table bk_rset 
\copy na2.bk_rset from '/usr1/dump-MT1/CSV/bk-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_rset__recid_seq', (SELECT MAX(_recid) FROM na2.bk_rset));
\echo Finish Table bk_rset 
\echo . 
\echo Loading Table bk_setup 
\copy na2.bk_setup from '/usr1/dump-MT1/CSV/bk-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_setup__recid_seq', (SELECT MAX(_recid) FROM na2.bk_setup));
\echo Finish Table bk_setup 
\echo . 
\echo Loading Table bk_stat 
\copy na2.bk_stat from '/usr1/dump-MT1/CSV/bk-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_stat__recid_seq', (SELECT MAX(_recid) FROM na2.bk_stat));
\echo Finish Table bk_stat 
\echo . 
\echo Loading Table bk_veran 
\copy na2.bk_veran from '/usr1/dump-MT1/CSV/bk-veran.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bk_veran__recid_seq', (SELECT MAX(_recid) FROM na2.bk_veran));
update na2.bk_veran set payment_userinit = array_replace(payment_userinit,NULL,''); 
\echo Finish Table bk_veran 
\echo . 
\echo Loading Table bl_dates 
\copy na2.bl_dates from '/usr1/dump-MT1/CSV/bl-dates.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bl_dates__recid_seq', (SELECT MAX(_recid) FROM na2.bl_dates));
\echo Finish Table bl_dates 
\echo . 
\echo Loading Table blinehis 
\copy na2.blinehis from '/usr1/dump-MT1/CSV/blinehis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.blinehis__recid_seq', (SELECT MAX(_recid) FROM na2.blinehis));
\echo Finish Table blinehis 
\echo . 
\echo Loading Table bresline 
\copy na2.bresline from '/usr1/dump-MT1/CSV/bresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.bresline__recid_seq', (SELECT MAX(_recid) FROM na2.bresline));
update na2.bresline set texte = array_replace(texte,NULL,''); 
\echo Finish Table bresline 
\echo . 
\echo Loading Table brief 
\copy na2.brief from '/usr1/dump-MT1/CSV/brief.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.brief__recid_seq', (SELECT MAX(_recid) FROM na2.brief));
\echo Finish Table brief 
\echo . 
\echo Loading Table brieftmp 
\copy na2.brieftmp from '/usr1/dump-MT1/CSV/brieftmp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.brieftmp__recid_seq', (SELECT MAX(_recid) FROM na2.brieftmp));
\echo Finish Table brieftmp 
\echo . 
\echo Loading Table briefzei 
\copy na2.briefzei from '/usr1/dump-MT1/CSV/briefzei.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.briefzei__recid_seq', (SELECT MAX(_recid) FROM na2.briefzei));
\echo Finish Table briefzei 
\echo . 
\echo Loading Table budget 
\copy na2.budget from '/usr1/dump-MT1/CSV/budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.budget__recid_seq', (SELECT MAX(_recid) FROM na2.budget));
\echo Finish Table budget 
\echo . 
\echo Loading Table calls 
\copy na2.calls from '/usr1/dump-MT1/CSV/calls.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.calls__recid_seq', (SELECT MAX(_recid) FROM na2.calls));
\echo Finish Table calls 
\echo . 
\echo Loading Table cl_bonus 
\copy na2.cl_bonus from '/usr1/dump-MT1/CSV/cl-bonus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_bonus__recid_seq', (SELECT MAX(_recid) FROM na2.cl_bonus));
\echo Finish Table cl_bonus 
\echo . 
\echo Loading Table cl_book 
\copy na2.cl_book from '/usr1/dump-MT1/CSV/cl-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_book__recid_seq', (SELECT MAX(_recid) FROM na2.cl_book));
\echo Finish Table cl_book 
\echo . 
\echo Loading Table cl_checkin 
\copy na2.cl_checkin from '/usr1/dump-MT1/CSV/cl-checkin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_checkin__recid_seq', (SELECT MAX(_recid) FROM na2.cl_checkin));
\echo Finish Table cl_checkin 
\echo . 
\echo Loading Table cl_class 
\copy na2.cl_class from '/usr1/dump-MT1/CSV/cl-class.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_class__recid_seq', (SELECT MAX(_recid) FROM na2.cl_class));
\echo Finish Table cl_class 
\echo . 
\echo Loading Table cl_enroll 
\copy na2.cl_enroll from '/usr1/dump-MT1/CSV/cl-enroll.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_enroll__recid_seq', (SELECT MAX(_recid) FROM na2.cl_enroll));
\echo Finish Table cl_enroll 
\echo . 
\echo Loading Table cl_free 
\copy na2.cl_free from '/usr1/dump-MT1/CSV/cl-free.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_free__recid_seq', (SELECT MAX(_recid) FROM na2.cl_free));
\echo Finish Table cl_free 
\echo . 
\echo Loading Table cl_histci 
\copy na2.cl_histci from '/usr1/dump-MT1/CSV/cl-histci.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_histci__recid_seq', (SELECT MAX(_recid) FROM na2.cl_histci));
\echo Finish Table cl_histci 
\echo . 
\echo Loading Table cl_histpay 
\copy na2.cl_histpay from '/usr1/dump-MT1/CSV/cl-histpay.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_histpay__recid_seq', (SELECT MAX(_recid) FROM na2.cl_histpay));
\echo Finish Table cl_histpay 
\echo . 
\echo Loading Table cl_histstatus 
\copy na2.cl_histstatus from '/usr1/dump-MT1/CSV/cl-histstatus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_histstatus__recid_seq', (SELECT MAX(_recid) FROM na2.cl_histstatus));
\echo Finish Table cl_histstatus 
\echo . 
\echo Loading Table cl_histtrain 
\copy na2.cl_histtrain from '/usr1/dump-MT1/CSV/cl-histtrain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_histtrain__recid_seq', (SELECT MAX(_recid) FROM na2.cl_histtrain));
\echo Finish Table cl_histtrain 
\echo . 
\echo Loading Table cl_histvisit 
\copy na2.cl_histvisit from '/usr1/dump-MT1/CSV/cl-histvisit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_histvisit__recid_seq', (SELECT MAX(_recid) FROM na2.cl_histvisit));
\echo Finish Table cl_histvisit 
\echo . 
\echo Loading Table cl_home 
\copy na2.cl_home from '/usr1/dump-MT1/CSV/cl-home.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_home__recid_seq', (SELECT MAX(_recid) FROM na2.cl_home));
\echo Finish Table cl_home 
\echo . 
\echo Loading Table cl_location 
\copy na2.cl_location from '/usr1/dump-MT1/CSV/cl-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_location__recid_seq', (SELECT MAX(_recid) FROM na2.cl_location));
\echo Finish Table cl_location 
\echo . 
\echo Loading Table cl_locker 
\copy na2.cl_locker from '/usr1/dump-MT1/CSV/cl-locker.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_locker__recid_seq', (SELECT MAX(_recid) FROM na2.cl_locker));
\echo Finish Table cl_locker 
\echo . 
\echo Loading Table cl_log 
\copy na2.cl_log from '/usr1/dump-MT1/CSV/cl-log.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_log__recid_seq', (SELECT MAX(_recid) FROM na2.cl_log));
\echo Finish Table cl_log 
\echo . 
\echo Loading Table cl_member 
\copy na2.cl_member from '/usr1/dump-MT1/CSV/cl-member.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_member__recid_seq', (SELECT MAX(_recid) FROM na2.cl_member));
\echo Finish Table cl_member 
\echo . 
\echo Loading Table cl_memtype 
\copy na2.cl_memtype from '/usr1/dump-MT1/CSV/cl-memtype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_memtype__recid_seq', (SELECT MAX(_recid) FROM na2.cl_memtype));
\echo Finish Table cl_memtype 
\echo . 
\echo Loading Table cl_paysched 
\copy na2.cl_paysched from '/usr1/dump-MT1/CSV/cl-paysched.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_paysched__recid_seq', (SELECT MAX(_recid) FROM na2.cl_paysched));
\echo Finish Table cl_paysched 
\echo . 
\echo Loading Table cl_stat 
\copy na2.cl_stat from '/usr1/dump-MT1/CSV/cl-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_stat__recid_seq', (SELECT MAX(_recid) FROM na2.cl_stat));
\echo Finish Table cl_stat 
\echo . 
\echo Loading Table cl_stat1 
\copy na2.cl_stat1 from '/usr1/dump-MT1/CSV/cl-stat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_stat1__recid_seq', (SELECT MAX(_recid) FROM na2.cl_stat1));
\echo Finish Table cl_stat1 
\echo . 
\echo Loading Table cl_towel 
\copy na2.cl_towel from '/usr1/dump-MT1/CSV/cl-towel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_towel__recid_seq', (SELECT MAX(_recid) FROM na2.cl_towel));
\echo Finish Table cl_towel 
\echo . 
\echo Loading Table cl_trainer 
\copy na2.cl_trainer from '/usr1/dump-MT1/CSV/cl-trainer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_trainer__recid_seq', (SELECT MAX(_recid) FROM na2.cl_trainer));
\echo Finish Table cl_trainer 
\echo . 
\echo Loading Table cl_upgrade 
\copy na2.cl_upgrade from '/usr1/dump-MT1/CSV/cl-upgrade.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cl_upgrade__recid_seq', (SELECT MAX(_recid) FROM na2.cl_upgrade));
\echo Finish Table cl_upgrade 
\echo . 
\echo Loading Table costbudget 
\copy na2.costbudget from '/usr1/dump-MT1/CSV/costbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.costbudget__recid_seq', (SELECT MAX(_recid) FROM na2.costbudget));
\echo Finish Table costbudget 
\echo . 
\echo Loading Table counters 
\copy na2.counters from '/usr1/dump-MT1/CSV/counters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.counters__recid_seq', (SELECT MAX(_recid) FROM na2.counters));
\echo Finish Table counters 
\echo . 
\echo Loading Table crm_campaign 
\copy na2.crm_campaign from '/usr1/dump-MT1/CSV/crm-campaign.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_campaign__recid_seq', (SELECT MAX(_recid) FROM na2.crm_campaign));
\echo Finish Table crm_campaign 
\echo . 
\echo Loading Table crm_category 
\copy na2.crm_category from '/usr1/dump-MT1/CSV/crm-category.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_category__recid_seq', (SELECT MAX(_recid) FROM na2.crm_category));
\echo Finish Table crm_category 
\echo . 
\echo Loading Table crm_dept 
\copy na2.crm_dept from '/usr1/dump-MT1/CSV/crm-dept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_dept__recid_seq', (SELECT MAX(_recid) FROM na2.crm_dept));
\echo Finish Table crm_dept 
\echo . 
\echo Loading Table crm_dtl 
\copy na2.crm_dtl from '/usr1/dump-MT1/CSV/crm-dtl.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_dtl__recid_seq', (SELECT MAX(_recid) FROM na2.crm_dtl));
\echo Finish Table crm_dtl 
\echo . 
\echo Loading Table crm_email 
\copy na2.crm_email from '/usr1/dump-MT1/CSV/crm-email.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_email__recid_seq', (SELECT MAX(_recid) FROM na2.crm_email));
\echo Finish Table crm_email 
\echo . 
\echo Loading Table crm_event 
\copy na2.crm_event from '/usr1/dump-MT1/CSV/crm-event.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_event__recid_seq', (SELECT MAX(_recid) FROM na2.crm_event));
\echo Finish Table crm_event 
\echo . 
\echo Loading Table crm_feedhdr 
\copy na2.crm_feedhdr from '/usr1/dump-MT1/CSV/crm-feedhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_feedhdr__recid_seq', (SELECT MAX(_recid) FROM na2.crm_feedhdr));
\echo Finish Table crm_feedhdr 
\echo . 
\echo Loading Table crm_fnlresult 
\copy na2.crm_fnlresult from '/usr1/dump-MT1/CSV/crm-fnlresult.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_fnlresult__recid_seq', (SELECT MAX(_recid) FROM na2.crm_fnlresult));
\echo Finish Table crm_fnlresult 
\echo . 
\echo Loading Table crm_language 
\copy na2.crm_language from '/usr1/dump-MT1/CSV/crm-language.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_language__recid_seq', (SELECT MAX(_recid) FROM na2.crm_language));
\echo Finish Table crm_language 
\echo . 
\echo Loading Table crm_question 
\copy na2.crm_question from '/usr1/dump-MT1/CSV/crm-question.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_question__recid_seq', (SELECT MAX(_recid) FROM na2.crm_question));
\echo Finish Table crm_question 
\echo . 
\echo Loading Table crm_tamplang 
\copy na2.crm_tamplang from '/usr1/dump-MT1/CSV/crm-tamplang.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_tamplang__recid_seq', (SELECT MAX(_recid) FROM na2.crm_tamplang));
\echo Finish Table crm_tamplang 
\echo . 
\echo Loading Table crm_template 
\copy na2.crm_template from '/usr1/dump-MT1/CSV/crm-template.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.crm_template__recid_seq', (SELECT MAX(_recid) FROM na2.crm_template));
\echo Finish Table crm_template 
\echo . 
\echo Loading Table cross_dtl 
\copy na2.cross_dtl from '/usr1/dump-MT1/CSV/cross-DTL.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cross_dtl__recid_seq', (SELECT MAX(_recid) FROM na2.cross_dtl));
\echo Finish Table cross_dtl 
\echo . 
\echo Loading Table cross_hdr 
\copy na2.cross_hdr from '/usr1/dump-MT1/CSV/cross-HDR.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.cross_hdr__recid_seq', (SELECT MAX(_recid) FROM na2.cross_hdr));
\echo Finish Table cross_hdr 
\echo . 
\echo Loading Table debitor 
\copy na2.debitor from '/usr1/dump-MT1/CSV/debitor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.debitor__recid_seq', (SELECT MAX(_recid) FROM na2.debitor));
\echo Finish Table debitor 
\echo . 
\echo Loading Table debthis 
\copy na2.debthis from '/usr1/dump-MT1/CSV/debthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.debthis__recid_seq', (SELECT MAX(_recid) FROM na2.debthis));
\echo Finish Table debthis 
\echo . 
\echo Loading Table desttext 
\copy na2.desttext from '/usr1/dump-MT1/CSV/desttext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.desttext__recid_seq', (SELECT MAX(_recid) FROM na2.desttext));
\echo Finish Table desttext 
\echo . 
\echo Loading Table dml_art 
\copy na2.dml_art from '/usr1/dump-MT1/CSV/dml-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.dml_art__recid_seq', (SELECT MAX(_recid) FROM na2.dml_art));
\echo Finish Table dml_art 
\echo . 
\echo Loading Table dml_artdep 
\copy na2.dml_artdep from '/usr1/dump-MT1/CSV/dml-artdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.dml_artdep__recid_seq', (SELECT MAX(_recid) FROM na2.dml_artdep));
\echo Finish Table dml_artdep 
\echo . 
\echo Loading Table dml_rate 
\copy na2.dml_rate from '/usr1/dump-MT1/CSV/dml-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.dml_rate__recid_seq', (SELECT MAX(_recid) FROM na2.dml_rate));
\echo Finish Table dml_rate 
\echo . 
\echo Loading Table eg_action 
\copy na2.eg_action from '/usr1/dump-MT1/CSV/eg-action.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_action__recid_seq', (SELECT MAX(_recid) FROM na2.eg_action));
\echo Finish Table eg_action 
\echo . 
\echo Loading Table eg_alert 
\copy na2.eg_alert from '/usr1/dump-MT1/CSV/eg-Alert.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_alert__recid_seq', (SELECT MAX(_recid) FROM na2.eg_alert));
\echo Finish Table eg_alert 
\echo . 
\echo Loading Table eg_budget 
\copy na2.eg_budget from '/usr1/dump-MT1/CSV/eg-budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_budget__recid_seq', (SELECT MAX(_recid) FROM na2.eg_budget));
\echo Finish Table eg_budget 
\echo . 
\echo Loading Table eg_cost 
\copy na2.eg_cost from '/usr1/dump-MT1/CSV/eg-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_cost__recid_seq', (SELECT MAX(_recid) FROM na2.eg_cost));
\echo Finish Table eg_cost 
\echo . 
\echo Loading Table eg_duration 
\copy na2.eg_duration from '/usr1/dump-MT1/CSV/eg-Duration.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_duration__recid_seq', (SELECT MAX(_recid) FROM na2.eg_duration));
\echo Finish Table eg_duration 
\echo . 
\echo Loading Table eg_location 
\copy na2.eg_location from '/usr1/dump-MT1/CSV/eg-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_location__recid_seq', (SELECT MAX(_recid) FROM na2.eg_location));
\echo Finish Table eg_location 
\echo . 
\echo Loading Table eg_mainstat 
\copy na2.eg_mainstat from '/usr1/dump-MT1/CSV/eg-MainStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_mainstat__recid_seq', (SELECT MAX(_recid) FROM na2.eg_mainstat));
\echo Finish Table eg_mainstat 
\echo . 
\echo Loading Table eg_maintain 
\copy na2.eg_maintain from '/usr1/dump-MT1/CSV/eg-maintain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_maintain__recid_seq', (SELECT MAX(_recid) FROM na2.eg_maintain));
\echo Finish Table eg_maintain 
\echo . 
\echo Loading Table eg_mdetail 
\copy na2.eg_mdetail from '/usr1/dump-MT1/CSV/eg-mdetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_mdetail__recid_seq', (SELECT MAX(_recid) FROM na2.eg_mdetail));
\echo Finish Table eg_mdetail 
\echo . 
\echo Loading Table eg_messageno 
\copy na2.eg_messageno from '/usr1/dump-MT1/CSV/eg-MessageNo.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_messageno__recid_seq', (SELECT MAX(_recid) FROM na2.eg_messageno));
\echo Finish Table eg_messageno 
\echo . 
\echo Loading Table eg_mobilenr 
\copy na2.eg_mobilenr from '/usr1/dump-MT1/CSV/eg-mobileNr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_mobilenr__recid_seq', (SELECT MAX(_recid) FROM na2.eg_mobilenr));
\echo Finish Table eg_mobilenr 
\echo . 
\echo Loading Table eg_moveproperty 
\copy na2.eg_moveproperty from '/usr1/dump-MT1/CSV/eg-moveProperty.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_moveproperty__recid_seq', (SELECT MAX(_recid) FROM na2.eg_moveproperty));
\echo Finish Table eg_moveproperty 
\echo . 
\echo Loading Table eg_property 
\copy na2.eg_property from '/usr1/dump-MT1/CSV/eg-property.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_property__recid_seq', (SELECT MAX(_recid) FROM na2.eg_property));
\echo Finish Table eg_property 
\echo . 
\echo Loading Table eg_propmeter 
\copy na2.eg_propmeter from '/usr1/dump-MT1/CSV/eg-propMeter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_propmeter__recid_seq', (SELECT MAX(_recid) FROM na2.eg_propmeter));
\echo Finish Table eg_propmeter 
\echo . 
\echo Loading Table eg_queasy 
\copy na2.eg_queasy from '/usr1/dump-MT1/CSV/eg-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_queasy__recid_seq', (SELECT MAX(_recid) FROM na2.eg_queasy));
\echo Finish Table eg_queasy 
\echo . 
\echo Loading Table eg_reqdetail 
\copy na2.eg_reqdetail from '/usr1/dump-MT1/CSV/eg-reqDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_reqdetail__recid_seq', (SELECT MAX(_recid) FROM na2.eg_reqdetail));
\echo Finish Table eg_reqdetail 
\echo . 
\echo Loading Table eg_reqif 
\copy na2.eg_reqif from '/usr1/dump-MT1/CSV/eg-reqif.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_reqif__recid_seq', (SELECT MAX(_recid) FROM na2.eg_reqif));
\echo Finish Table eg_reqif 
\echo . 
\echo Loading Table eg_reqstat 
\copy na2.eg_reqstat from '/usr1/dump-MT1/CSV/eg-ReqStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_reqstat__recid_seq', (SELECT MAX(_recid) FROM na2.eg_reqstat));
\echo Finish Table eg_reqstat 
\echo . 
\echo Loading Table eg_request 
\copy na2.eg_request from '/usr1/dump-MT1/CSV/eg-request.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_request__recid_seq', (SELECT MAX(_recid) FROM na2.eg_request));
\echo Finish Table eg_request 
\echo . 
\echo Loading Table eg_resources 
\copy na2.eg_resources from '/usr1/dump-MT1/CSV/eg-resources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_resources__recid_seq', (SELECT MAX(_recid) FROM na2.eg_resources));
\echo Finish Table eg_resources 
\echo . 
\echo Loading Table eg_staff 
\copy na2.eg_staff from '/usr1/dump-MT1/CSV/eg-staff.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_staff__recid_seq', (SELECT MAX(_recid) FROM na2.eg_staff));
\echo Finish Table eg_staff 
\echo . 
\echo Loading Table eg_stat 
\copy na2.eg_stat from '/usr1/dump-MT1/CSV/eg-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_stat__recid_seq', (SELECT MAX(_recid) FROM na2.eg_stat));
\echo Finish Table eg_stat 
\echo . 
\echo Loading Table eg_subtask 
\copy na2.eg_subtask from '/usr1/dump-MT1/CSV/eg-subtask.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_subtask__recid_seq', (SELECT MAX(_recid) FROM na2.eg_subtask));
\echo Finish Table eg_subtask 
\echo . 
\echo Loading Table eg_vendor 
\copy na2.eg_vendor from '/usr1/dump-MT1/CSV/eg-vendor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_vendor__recid_seq', (SELECT MAX(_recid) FROM na2.eg_vendor));
\echo Finish Table eg_vendor 
\echo . 
\echo Loading Table eg_vperform 
\copy na2.eg_vperform from '/usr1/dump-MT1/CSV/eg-vperform.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.eg_vperform__recid_seq', (SELECT MAX(_recid) FROM na2.eg_vperform));
\echo Finish Table eg_vperform 
\echo . 
\echo Loading Table ekum 
\copy na2.ekum from '/usr1/dump-MT1/CSV/ekum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.ekum__recid_seq', (SELECT MAX(_recid) FROM na2.ekum));
\echo Finish Table ekum 
\echo . 
\echo Loading Table employee 
\copy na2.employee from '/usr1/dump-MT1/CSV/employee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.employee__recid_seq', (SELECT MAX(_recid) FROM na2.employee));
update na2.employee set child = array_replace(child,NULL,''); 
\echo Finish Table employee 
\echo . 
\echo Loading Table equiplan 
\copy na2.equiplan from '/usr1/dump-MT1/CSV/equiplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.equiplan__recid_seq', (SELECT MAX(_recid) FROM na2.equiplan));
\echo Finish Table equiplan 
\echo . 
\echo Loading Table exrate 
\copy na2.exrate from '/usr1/dump-MT1/CSV/exrate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.exrate__recid_seq', (SELECT MAX(_recid) FROM na2.exrate));
\echo Finish Table exrate 
\echo . 
\echo Loading Table fa_artikel 
\copy na2.fa_artikel from '/usr1/dump-MT1/CSV/fa-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_artikel__recid_seq', (SELECT MAX(_recid) FROM na2.fa_artikel));
\echo Finish Table fa_artikel 
\echo . 
\echo Loading Table fa_counter 
\copy na2.fa_counter from '/usr1/dump-MT1/CSV/fa-Counter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_counter__recid_seq', (SELECT MAX(_recid) FROM na2.fa_counter));
\echo Finish Table fa_counter 
\echo . 
\echo Loading Table fa_dp 
\copy na2.fa_dp from '/usr1/dump-MT1/CSV/fa-DP.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_dp__recid_seq', (SELECT MAX(_recid) FROM na2.fa_dp));
\echo Finish Table fa_dp 
\echo . 
\echo Loading Table fa_grup 
\copy na2.fa_grup from '/usr1/dump-MT1/CSV/fa-grup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_grup__recid_seq', (SELECT MAX(_recid) FROM na2.fa_grup));
\echo Finish Table fa_grup 
\echo . 
\echo Loading Table fa_kateg 
\copy na2.fa_kateg from '/usr1/dump-MT1/CSV/fa-kateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_kateg__recid_seq', (SELECT MAX(_recid) FROM na2.fa_kateg));
\echo Finish Table fa_kateg 
\echo . 
\echo Loading Table fa_lager 
\copy na2.fa_lager from '/usr1/dump-MT1/CSV/fa-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_lager__recid_seq', (SELECT MAX(_recid) FROM na2.fa_lager));
\echo Finish Table fa_lager 
\echo . 
\echo Loading Table fa_op 
\copy na2.fa_op from '/usr1/dump-MT1/CSV/fa-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_op__recid_seq', (SELECT MAX(_recid) FROM na2.fa_op));
\echo Finish Table fa_op 
\echo . 
\echo Loading Table fa_order 
\copy na2.fa_order from '/usr1/dump-MT1/CSV/fa-Order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_order__recid_seq', (SELECT MAX(_recid) FROM na2.fa_order));
\echo Finish Table fa_order 
\echo . 
\echo Loading Table fa_ordheader 
\copy na2.fa_ordheader from '/usr1/dump-MT1/CSV/fa-OrdHeader.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_ordheader__recid_seq', (SELECT MAX(_recid) FROM na2.fa_ordheader));
\echo Finish Table fa_ordheader 
\echo . 
\echo Loading Table fa_quodetail 
\copy na2.fa_quodetail from '/usr1/dump-MT1/CSV/fa-QuoDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_quodetail__recid_seq', (SELECT MAX(_recid) FROM na2.fa_quodetail));
\echo Finish Table fa_quodetail 
\echo . 
\echo Loading Table fa_quotation 
\copy na2.fa_quotation from '/usr1/dump-MT1/CSV/fa-quotation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_quotation__recid_seq', (SELECT MAX(_recid) FROM na2.fa_quotation));
\echo Finish Table fa_quotation 
\echo . 
\echo Loading Table fa_user 
\copy na2.fa_user from '/usr1/dump-MT1/CSV/fa-user.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fa_user__recid_seq', (SELECT MAX(_recid) FROM na2.fa_user));
update na2.fa_user set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table fa_user 
\echo . 
\echo Loading Table fbstat 
\copy na2.fbstat from '/usr1/dump-MT1/CSV/fbstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fbstat__recid_seq', (SELECT MAX(_recid) FROM na2.fbstat));
\echo Finish Table fbstat 
\echo . 
\echo Loading Table feiertag 
\copy na2.feiertag from '/usr1/dump-MT1/CSV/feiertag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.feiertag__recid_seq', (SELECT MAX(_recid) FROM na2.feiertag));
\echo Finish Table feiertag 
\echo . 
\echo Loading Table ffont 
\copy na2.ffont from '/usr1/dump-MT1/CSV/ffont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.ffont__recid_seq', (SELECT MAX(_recid) FROM na2.ffont));
\echo Finish Table ffont 
\echo . 
\echo Loading Table fixleist 
\copy na2.fixleist from '/usr1/dump-MT1/CSV/fixleist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.fixleist__recid_seq', (SELECT MAX(_recid) FROM na2.fixleist));
\echo Finish Table fixleist 
\echo . 
\echo Loading Table gc_giro 
\copy na2.gc_giro from '/usr1/dump-MT1/CSV/gc-giro.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gc_giro__recid_seq', (SELECT MAX(_recid) FROM na2.gc_giro));
update na2.gc_giro set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_giro 
\echo . 
\echo Loading Table gc_jouhdr 
\copy na2.gc_jouhdr from '/usr1/dump-MT1/CSV/gc-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gc_jouhdr__recid_seq', (SELECT MAX(_recid) FROM na2.gc_jouhdr));
\echo Finish Table gc_jouhdr 
\echo . 
\echo Loading Table gc_journal 
\copy na2.gc_journal from '/usr1/dump-MT1/CSV/gc-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gc_journal__recid_seq', (SELECT MAX(_recid) FROM na2.gc_journal));
\echo Finish Table gc_journal 
\echo . 
\echo Loading Table gc_pi 
\copy na2.gc_pi from '/usr1/dump-MT1/CSV/gc-PI.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gc_pi__recid_seq', (SELECT MAX(_recid) FROM na2.gc_pi));
update na2.gc_pi set bez_array = array_replace(bez_array,NULL,''); 
update na2.gc_pi set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_pi 
\echo . 
\echo Loading Table gc_piacct 
\copy na2.gc_piacct from '/usr1/dump-MT1/CSV/gc-piacct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gc_piacct__recid_seq', (SELECT MAX(_recid) FROM na2.gc_piacct));
\echo Finish Table gc_piacct 
\echo . 
\echo Loading Table gc_pibline 
\copy na2.gc_pibline from '/usr1/dump-MT1/CSV/gc-PIbline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gc_pibline__recid_seq', (SELECT MAX(_recid) FROM na2.gc_pibline));
\echo Finish Table gc_pibline 
\echo . 
\echo Loading Table gc_pitype 
\copy na2.gc_pitype from '/usr1/dump-MT1/CSV/gc-piType.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gc_pitype__recid_seq', (SELECT MAX(_recid) FROM na2.gc_pitype));
\echo Finish Table gc_pitype 
\echo . 
\echo Loading Table genfcast 
\copy na2.genfcast from '/usr1/dump-MT1/CSV/genfcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.genfcast__recid_seq', (SELECT MAX(_recid) FROM na2.genfcast));
update na2.genfcast set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genfcast 
\echo . 
\echo Loading Table genlayout 
\copy na2.genlayout from '/usr1/dump-MT1/CSV/genlayout.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.genlayout__recid_seq', (SELECT MAX(_recid) FROM na2.genlayout));
update na2.genlayout set button_ext = array_replace(button_ext,NULL,''); 
update na2.genlayout set char_ext = array_replace(char_ext,NULL,''); 
update na2.genlayout set combo_ext = array_replace(combo_ext,NULL,''); 
update na2.genlayout set date_ext = array_replace(date_ext,NULL,''); 
update na2.genlayout set deci_ext = array_replace(deci_ext,NULL,''); 
update na2.genlayout set inte_ext = array_replace(inte_ext,NULL,''); 
update na2.genlayout set logi_ext = array_replace(logi_ext,NULL,''); 
update na2.genlayout set string_ext = array_replace(string_ext,NULL,''); 
update na2.genlayout set tchar_ext = array_replace(tchar_ext,NULL,''); 
update na2.genlayout set tdate_ext = array_replace(tdate_ext,NULL,''); 
update na2.genlayout set tdeci_ext = array_replace(tdeci_ext,NULL,''); 
update na2.genlayout set tinte_ext = array_replace(tinte_ext,NULL,''); 
update na2.genlayout set tlogi_ext = array_replace(tlogi_ext,NULL,''); 
\echo Finish Table genlayout 
\echo . 
\echo Loading Table genstat 
\copy na2.genstat from '/usr1/dump-MT1/CSV/genstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.genstat__recid_seq', (SELECT MAX(_recid) FROM na2.genstat));
update na2.genstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genstat 
\echo . 
\echo Loading Table gentable 
\copy na2.gentable from '/usr1/dump-MT1/CSV/gentable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gentable__recid_seq', (SELECT MAX(_recid) FROM na2.gentable));
update na2.gentable set char_ext = array_replace(char_ext,NULL,''); 
update na2.gentable set combo_ext = array_replace(combo_ext,NULL,''); 
\echo Finish Table gentable 
\echo . 
\echo Loading Table gk_field 
\copy na2.gk_field from '/usr1/dump-MT1/CSV/gk-field.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gk_field__recid_seq', (SELECT MAX(_recid) FROM na2.gk_field));
\echo Finish Table gk_field 
\echo . 
\echo Loading Table gk_label 
\copy na2.gk_label from '/usr1/dump-MT1/CSV/gk-label.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gk_label__recid_seq', (SELECT MAX(_recid) FROM na2.gk_label));
\echo Finish Table gk_label 
\echo . 
\echo Loading Table gk_notes 
\copy na2.gk_notes from '/usr1/dump-MT1/CSV/gk-notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gk_notes__recid_seq', (SELECT MAX(_recid) FROM na2.gk_notes));
update na2.gk_notes set notes = array_replace(notes,NULL,''); 
\echo Finish Table gk_notes 
\echo . 
\echo Loading Table gl_acct 
\copy na2.gl_acct from '/usr1/dump-MT1/CSV/gl-acct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_acct__recid_seq', (SELECT MAX(_recid) FROM na2.gl_acct));
\echo Finish Table gl_acct 
\echo . 
\echo Loading Table gl_accthis 
\copy na2.gl_accthis from '/usr1/dump-MT1/CSV/gl-accthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_accthis__recid_seq', (SELECT MAX(_recid) FROM na2.gl_accthis));
\echo Finish Table gl_accthis 
\echo . 
\echo Loading Table gl_coa 
\copy na2.gl_coa from '/usr1/dump-MT1/CSV/gl-coa.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_coa__recid_seq', (SELECT MAX(_recid) FROM na2.gl_coa));
\echo Finish Table gl_coa 
\echo . 
\echo Loading Table gl_cost 
\copy na2.gl_cost from '/usr1/dump-MT1/CSV/gl-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_cost__recid_seq', (SELECT MAX(_recid) FROM na2.gl_cost));
\echo Finish Table gl_cost 
\echo . 
\echo Loading Table gl_department 
\copy na2.gl_department from '/usr1/dump-MT1/CSV/gl-department.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_department__recid_seq', (SELECT MAX(_recid) FROM na2.gl_department));
\echo Finish Table gl_department 
\echo . 
\echo Loading Table gl_fstype 
\copy na2.gl_fstype from '/usr1/dump-MT1/CSV/gl-fstype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_fstype__recid_seq', (SELECT MAX(_recid) FROM na2.gl_fstype));
\echo Finish Table gl_fstype 
\echo . 
\echo Loading Table gl_htljournal 
\copy na2.gl_htljournal from '/usr1/dump-MT1/CSV/gl-htljournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_htljournal__recid_seq', (SELECT MAX(_recid) FROM na2.gl_htljournal));
\echo Finish Table gl_htljournal 
\echo . 
\echo Loading Table gl_jhdrhis 
\copy na2.gl_jhdrhis from '/usr1/dump-MT1/CSV/gl-jhdrhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_jhdrhis__recid_seq', (SELECT MAX(_recid) FROM na2.gl_jhdrhis));
\echo Finish Table gl_jhdrhis 
\echo . 
\echo Loading Table gl_jouhdr 
\copy na2.gl_jouhdr from '/usr1/dump-MT1/CSV/gl-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_jouhdr__recid_seq', (SELECT MAX(_recid) FROM na2.gl_jouhdr));
\echo Finish Table gl_jouhdr 
\echo . 
\echo Loading Table gl_jourhis 
\copy na2.gl_jourhis from '/usr1/dump-MT1/CSV/gl-jourhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_jourhis__recid_seq', (SELECT MAX(_recid) FROM na2.gl_jourhis));
\echo Finish Table gl_jourhis 
\echo . 
\echo Loading Table gl_journal 
\copy na2.gl_journal from '/usr1/dump-MT1/CSV/gl-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_journal__recid_seq', (SELECT MAX(_recid) FROM na2.gl_journal));
\echo Finish Table gl_journal 
\echo . 
\echo Loading Table gl_main 
\copy na2.gl_main from '/usr1/dump-MT1/CSV/gl-main.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.gl_main__recid_seq', (SELECT MAX(_recid) FROM na2.gl_main));
\echo Finish Table gl_main 
\echo . 
\echo Loading Table golf_caddie 
\copy na2.golf_caddie from '/usr1/dump-MT1/CSV/golf-caddie.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_caddie__recid_seq', (SELECT MAX(_recid) FROM na2.golf_caddie));
\echo Finish Table golf_caddie 
\echo . 
\echo Loading Table golf_caddie_assignment 
\copy na2.golf_caddie_assignment from '/usr1/dump-MT1/CSV/golf-caddie-assignment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_caddie_assignment__recid_seq', (SELECT MAX(_recid) FROM na2.golf_caddie_assignment));
\echo Finish Table golf_caddie_assignment 
\echo . 
\echo Loading Table golf_course 
\copy na2.golf_course from '/usr1/dump-MT1/CSV/golf-course.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_course__recid_seq', (SELECT MAX(_recid) FROM na2.golf_course));
\echo Finish Table golf_course 
\echo . 
\echo Loading Table golf_flight_reservation 
\copy na2.golf_flight_reservation from '/usr1/dump-MT1/CSV/golf-flight-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_flight_reservation__recid_seq', (SELECT MAX(_recid) FROM na2.golf_flight_reservation));
\echo Finish Table golf_flight_reservation 
\echo . 
\echo Loading Table golf_flight_reservation_hist 
\copy na2.golf_flight_reservation_hist from '/usr1/dump-MT1/CSV/golf-flight-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_flight_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM na2.golf_flight_reservation_hist));
\echo Finish Table golf_flight_reservation_hist 
\echo . 
\echo Loading Table golf_golfer_reservation 
\copy na2.golf_golfer_reservation from '/usr1/dump-MT1/CSV/golf-golfer-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_golfer_reservation__recid_seq', (SELECT MAX(_recid) FROM na2.golf_golfer_reservation));
\echo Finish Table golf_golfer_reservation 
\echo . 
\echo Loading Table golf_golfer_reservation_hist 
\copy na2.golf_golfer_reservation_hist from '/usr1/dump-MT1/CSV/golf-golfer-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_golfer_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM na2.golf_golfer_reservation_hist));
\echo Finish Table golf_golfer_reservation_hist 
\echo . 
\echo Loading Table golf_holiday 
\copy na2.golf_holiday from '/usr1/dump-MT1/CSV/golf-holiday.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_holiday__recid_seq', (SELECT MAX(_recid) FROM na2.golf_holiday));
\echo Finish Table golf_holiday 
\echo . 
\echo Loading Table golf_main_reservation 
\copy na2.golf_main_reservation from '/usr1/dump-MT1/CSV/golf-main-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_main_reservation__recid_seq', (SELECT MAX(_recid) FROM na2.golf_main_reservation));
\echo Finish Table golf_main_reservation 
\echo . 
\echo Loading Table golf_main_reservation_hist 
\copy na2.golf_main_reservation_hist from '/usr1/dump-MT1/CSV/golf-main-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_main_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM na2.golf_main_reservation_hist));
\echo Finish Table golf_main_reservation_hist 
\echo . 
\echo Loading Table golf_rate 
\copy na2.golf_rate from '/usr1/dump-MT1/CSV/golf-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_rate__recid_seq', (SELECT MAX(_recid) FROM na2.golf_rate));
\echo Finish Table golf_rate 
\echo . 
\echo Loading Table golf_shift 
\copy na2.golf_shift from '/usr1/dump-MT1/CSV/golf-shift.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_shift__recid_seq', (SELECT MAX(_recid) FROM na2.golf_shift));
\echo Finish Table golf_shift 
\echo . 
\echo Loading Table golf_transfer 
\copy na2.golf_transfer from '/usr1/dump-MT1/CSV/golf-transfer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.golf_transfer__recid_seq', (SELECT MAX(_recid) FROM na2.golf_transfer));
\echo Finish Table golf_transfer 
\echo . 
\echo Loading Table guest 
\copy na2.guest from '/usr1/dump-MT1/CSV/guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guest__recid_seq', (SELECT MAX(_recid) FROM na2.guest));
update na2.guest set notizen = array_replace(notizen,NULL,''); 
update na2.guest set vornamekind = array_replace(vornamekind,NULL,''); 
\echo Finish Table guest 
\echo . 
\echo Loading Table guest_pr 
\copy na2.guest_pr from '/usr1/dump-MT1/CSV/guest-pr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guest_pr__recid_seq', (SELECT MAX(_recid) FROM na2.guest_pr));
\echo Finish Table guest_pr 
\echo . 
\echo Loading Table guest_queasy 
\copy na2.guest_queasy from '/usr1/dump-MT1/CSV/guest-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guest_queasy__recid_seq', (SELECT MAX(_recid) FROM na2.guest_queasy));
\echo Finish Table guest_queasy 
\echo . 
\echo Loading Table guest_remark 
\copy na2.guest_remark from '/usr1/dump-MT1/CSV/guest-remark.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guest_remark__recid_seq', (SELECT MAX(_recid) FROM na2.guest_remark));
update na2.guest_remark set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table guest_remark 
\echo . 
\echo Loading Table guestat 
\copy na2.guestat from '/usr1/dump-MT1/CSV/guestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guestat__recid_seq', (SELECT MAX(_recid) FROM na2.guestat));
\echo Finish Table guestat 
\echo . 
\echo Loading Table guestat1 
\copy na2.guestat1 from '/usr1/dump-MT1/CSV/guestat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guestat1__recid_seq', (SELECT MAX(_recid) FROM na2.guestat1));
\echo Finish Table guestat1 
\echo . 
\echo Loading Table guestbook 
\copy na2.guestbook from '/usr1/dump-MT1/CSV/guestbook.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guestbook__recid_seq', (SELECT MAX(_recid) FROM na2.guestbook));
update na2.guestbook set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table guestbook 
\echo . 
\echo Loading Table guestbud 
\copy na2.guestbud from '/usr1/dump-MT1/CSV/guestbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guestbud__recid_seq', (SELECT MAX(_recid) FROM na2.guestbud));
\echo Finish Table guestbud 
\echo . 
\echo Loading Table guestseg 
\copy na2.guestseg from '/usr1/dump-MT1/CSV/guestseg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.guestseg__recid_seq', (SELECT MAX(_recid) FROM na2.guestseg));
\echo Finish Table guestseg 
\echo . 
\echo Loading Table h_artcost 
\copy na2.h_artcost from '/usr1/dump-MT1/CSV/h-artcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_artcost__recid_seq', (SELECT MAX(_recid) FROM na2.h_artcost));
\echo Finish Table h_artcost 
\echo . 
\echo Loading Table h_artikel 
\copy na2.h_artikel from '/usr1/dump-MT1/CSV/h-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_artikel__recid_seq', (SELECT MAX(_recid) FROM na2.h_artikel));
\echo Finish Table h_artikel 
\echo . 
\echo Loading Table h_bill 
\copy na2.h_bill from '/usr1/dump-MT1/CSV/h-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_bill__recid_seq', (SELECT MAX(_recid) FROM na2.h_bill));
\echo Finish Table h_bill 
\echo . 
\echo Loading Table h_bill_line 
\copy na2.h_bill_line from '/usr1/dump-MT1/CSV/h-bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_bill_line__recid_seq', (SELECT MAX(_recid) FROM na2.h_bill_line));
\echo Finish Table h_bill_line 
\echo . 
\echo Loading Table h_compli 
\copy na2.h_compli from '/usr1/dump-MT1/CSV/h-compli.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_compli__recid_seq', (SELECT MAX(_recid) FROM na2.h_compli));
\echo Finish Table h_compli 
\echo . 
\echo Loading Table h_cost 
\copy na2.h_cost from '/usr1/dump-MT1/CSV/h-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_cost__recid_seq', (SELECT MAX(_recid) FROM na2.h_cost));
\echo Finish Table h_cost 
\echo . 
\echo Loading Table h_journal 
\copy na2.h_journal from '/usr1/dump-MT1/CSV/h-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_journal__recid_seq', (SELECT MAX(_recid) FROM na2.h_journal));
\echo Finish Table h_journal 
\echo . 
\echo Loading Table h_menu 
\copy na2.h_menu from '/usr1/dump-MT1/CSV/h-menu.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_menu__recid_seq', (SELECT MAX(_recid) FROM na2.h_menu));
\echo Finish Table h_menu 
\echo . 
\echo Loading Table h_mjourn 
\copy na2.h_mjourn from '/usr1/dump-MT1/CSV/h-mjourn.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_mjourn__recid_seq', (SELECT MAX(_recid) FROM na2.h_mjourn));
\echo Finish Table h_mjourn 
\echo . 
\echo Loading Table h_oldjou 
\copy na2.h_oldjou from '/usr1/dump-MT1/CSV/h-oldjou.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_oldjou__recid_seq', (SELECT MAX(_recid) FROM na2.h_oldjou));
\echo Finish Table h_oldjou 
\echo . 
\echo Loading Table h_order 
\copy na2.h_order from '/usr1/dump-MT1/CSV/h-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_order__recid_seq', (SELECT MAX(_recid) FROM na2.h_order));
update na2.h_order set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table h_order 
\echo . 
\echo Loading Table h_queasy 
\copy na2.h_queasy from '/usr1/dump-MT1/CSV/h-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_queasy__recid_seq', (SELECT MAX(_recid) FROM na2.h_queasy));
\echo Finish Table h_queasy 
\echo . 
\echo Loading Table h_rezept 
\copy na2.h_rezept from '/usr1/dump-MT1/CSV/h-rezept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_rezept__recid_seq', (SELECT MAX(_recid) FROM na2.h_rezept));
\echo Finish Table h_rezept 
\echo . 
\echo Loading Table h_rezlin 
\copy na2.h_rezlin from '/usr1/dump-MT1/CSV/h-rezlin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_rezlin__recid_seq', (SELECT MAX(_recid) FROM na2.h_rezlin));
\echo Finish Table h_rezlin 
\echo . 
\echo Loading Table h_storno 
\copy na2.h_storno from '/usr1/dump-MT1/CSV/h-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_storno__recid_seq', (SELECT MAX(_recid) FROM na2.h_storno));
\echo Finish Table h_storno 
\echo . 
\echo Loading Table h_umsatz 
\copy na2.h_umsatz from '/usr1/dump-MT1/CSV/h-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.h_umsatz__recid_seq', (SELECT MAX(_recid) FROM na2.h_umsatz));
\echo Finish Table h_umsatz 
\echo . 
\echo Loading Table history 
\copy na2.history from '/usr1/dump-MT1/CSV/history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.history__recid_seq', (SELECT MAX(_recid) FROM na2.history));
\echo Finish Table history 
\echo . 
\echo Loading Table hoteldpt 
\copy na2.hoteldpt from '/usr1/dump-MT1/CSV/hoteldpt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.hoteldpt__recid_seq', (SELECT MAX(_recid) FROM na2.hoteldpt));
\echo Finish Table hoteldpt 
\echo . 
\echo Loading Table hrbeleg 
\copy na2.hrbeleg from '/usr1/dump-MT1/CSV/hrbeleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.hrbeleg__recid_seq', (SELECT MAX(_recid) FROM na2.hrbeleg));
\echo Finish Table hrbeleg 
\echo . 
\echo Loading Table hrsegement 
\copy na2.hrsegement from '/usr1/dump-MT1/CSV/hrsegement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.hrsegement__recid_seq', (SELECT MAX(_recid) FROM na2.hrsegement));
\echo Finish Table hrsegement 
\echo . 
\echo Loading Table htparam 
\copy na2.htparam from '/usr1/dump-MT1/CSV/htparam.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.htparam__recid_seq', (SELECT MAX(_recid) FROM na2.htparam));
\echo Finish Table htparam 
\echo . 
\echo Loading Table htreport 
\copy na2.htreport from '/usr1/dump-MT1/CSV/htreport.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.htreport__recid_seq', (SELECT MAX(_recid) FROM na2.htreport));
\echo Finish Table htreport 
\echo . 
\echo Loading Table iftable 
\copy na2.iftable from '/usr1/dump-MT1/CSV/iftable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.iftable__recid_seq', (SELECT MAX(_recid) FROM na2.iftable));
\echo Finish Table iftable 
\echo . 
\echo Loading Table interface 
\copy na2.interface from '/usr1/dump-MT1/CSV/interface.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.interface__recid_seq', (SELECT MAX(_recid) FROM na2.interface));
\echo Finish Table interface 
\echo . 
\echo Loading Table k_history 
\copy na2.k_history from '/usr1/dump-MT1/CSV/k-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.k_history__recid_seq', (SELECT MAX(_recid) FROM na2.k_history));
\echo Finish Table k_history 
\echo . 
\echo Loading Table kabine 
\copy na2.kabine from '/usr1/dump-MT1/CSV/kabine.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kabine__recid_seq', (SELECT MAX(_recid) FROM na2.kabine));
\echo Finish Table kabine 
\echo . 
\echo Loading Table kalender 
\copy na2.kalender from '/usr1/dump-MT1/CSV/kalender.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kalender__recid_seq', (SELECT MAX(_recid) FROM na2.kalender));
update na2.kalender set note = array_replace(note,NULL,''); 
\echo Finish Table kalender 
\echo . 
\echo Loading Table kasse 
\copy na2.kasse from '/usr1/dump-MT1/CSV/kasse.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kasse__recid_seq', (SELECT MAX(_recid) FROM na2.kasse));
\echo Finish Table kasse 
\echo . 
\echo Loading Table katpreis 
\copy na2.katpreis from '/usr1/dump-MT1/CSV/katpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.katpreis__recid_seq', (SELECT MAX(_recid) FROM na2.katpreis));
\echo Finish Table katpreis 
\echo . 
\echo Loading Table kellne1 
\copy na2.kellne1 from '/usr1/dump-MT1/CSV/kellne1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kellne1__recid_seq', (SELECT MAX(_recid) FROM na2.kellne1));
\echo Finish Table kellne1 
\echo . 
\echo Loading Table kellner 
\copy na2.kellner from '/usr1/dump-MT1/CSV/kellner.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kellner__recid_seq', (SELECT MAX(_recid) FROM na2.kellner));
\echo Finish Table kellner 
\echo . 
\echo Loading Table kontakt 
\copy na2.kontakt from '/usr1/dump-MT1/CSV/kontakt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kontakt__recid_seq', (SELECT MAX(_recid) FROM na2.kontakt));
\echo Finish Table kontakt 
\echo . 
\echo Loading Table kontline 
\copy na2.kontline from '/usr1/dump-MT1/CSV/kontline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kontline__recid_seq', (SELECT MAX(_recid) FROM na2.kontline));
\echo Finish Table kontline 
\echo . 
\echo Loading Table kontlink 
\copy na2.kontlink from '/usr1/dump-MT1/CSV/kontlink.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kontlink__recid_seq', (SELECT MAX(_recid) FROM na2.kontlink));
\echo Finish Table kontlink 
\echo . 
\echo Loading Table kontplan 
\copy na2.kontplan from '/usr1/dump-MT1/CSV/kontplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kontplan__recid_seq', (SELECT MAX(_recid) FROM na2.kontplan));
\echo Finish Table kontplan 
\echo . 
\echo Loading Table kontstat 
\copy na2.kontstat from '/usr1/dump-MT1/CSV/kontstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kontstat__recid_seq', (SELECT MAX(_recid) FROM na2.kontstat));
update na2.kontstat set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table kontstat 
\echo . 
\echo Loading Table kresline 
\copy na2.kresline from '/usr1/dump-MT1/CSV/kresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.kresline__recid_seq', (SELECT MAX(_recid) FROM na2.kresline));
\echo Finish Table kresline 
\echo . 
\echo Loading Table l_artikel 
\copy na2.l_artikel from '/usr1/dump-MT1/CSV/l-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_artikel__recid_seq', (SELECT MAX(_recid) FROM na2.l_artikel));
update na2.l_artikel set lief_artnr = array_replace(lief_artnr,NULL,''); 
\echo Finish Table l_artikel 
\echo . 
\echo Loading Table l_bestand 
\copy na2.l_bestand from '/usr1/dump-MT1/CSV/l-bestand.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_bestand__recid_seq', (SELECT MAX(_recid) FROM na2.l_bestand));
\echo Finish Table l_bestand 
\echo . 
\echo Loading Table l_besthis 
\copy na2.l_besthis from '/usr1/dump-MT1/CSV/l-besthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_besthis__recid_seq', (SELECT MAX(_recid) FROM na2.l_besthis));
\echo Finish Table l_besthis 
\echo . 
\echo Loading Table l_hauptgrp 
\copy na2.l_hauptgrp from '/usr1/dump-MT1/CSV/l-hauptgrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_hauptgrp__recid_seq', (SELECT MAX(_recid) FROM na2.l_hauptgrp));
\echo Finish Table l_hauptgrp 
\echo . 
\echo Loading Table l_kredit 
\copy na2.l_kredit from '/usr1/dump-MT1/CSV/l-kredit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_kredit__recid_seq', (SELECT MAX(_recid) FROM na2.l_kredit));
\echo Finish Table l_kredit 
\echo . 
\echo Loading Table l_lager 
\copy na2.l_lager from '/usr1/dump-MT1/CSV/l-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_lager__recid_seq', (SELECT MAX(_recid) FROM na2.l_lager));
\echo Finish Table l_lager 
\echo . 
\echo Loading Table l_lieferant 
\copy na2.l_lieferant from '/usr1/dump-MT1/CSV/l-lieferant.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_lieferant__recid_seq', (SELECT MAX(_recid) FROM na2.l_lieferant));
update na2.l_lieferant set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table l_lieferant 
\echo . 
\echo Loading Table l_liefumsatz 
\copy na2.l_liefumsatz from '/usr1/dump-MT1/CSV/l-liefumsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_liefumsatz__recid_seq', (SELECT MAX(_recid) FROM na2.l_liefumsatz));
\echo Finish Table l_liefumsatz 
\echo . 
\echo Loading Table l_op 
\copy na2.l_op from '/usr1/dump-MT1/CSV/l-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_op__recid_seq', (SELECT MAX(_recid) FROM na2.l_op));
\echo Finish Table l_op 
\echo . 
\echo Loading Table l_ophdr 
\copy na2.l_ophdr from '/usr1/dump-MT1/CSV/l-ophdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_ophdr__recid_seq', (SELECT MAX(_recid) FROM na2.l_ophdr));
\echo Finish Table l_ophdr 
\echo . 
\echo Loading Table l_ophhis 
\copy na2.l_ophhis from '/usr1/dump-MT1/CSV/l-ophhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_ophhis__recid_seq', (SELECT MAX(_recid) FROM na2.l_ophhis));
\echo Finish Table l_ophhis 
\echo . 
\echo Loading Table l_ophis 
\copy na2.l_ophis from '/usr1/dump-MT1/CSV/l-ophis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_ophis__recid_seq', (SELECT MAX(_recid) FROM na2.l_ophis));
\echo Finish Table l_ophis 
\echo . 
\echo Loading Table l_order 
\copy na2.l_order from '/usr1/dump-MT1/CSV/l-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_order__recid_seq', (SELECT MAX(_recid) FROM na2.l_order));
update na2.l_order set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_order 
\echo . 
\echo Loading Table l_orderhdr 
\copy na2.l_orderhdr from '/usr1/dump-MT1/CSV/l-orderhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_orderhdr__recid_seq', (SELECT MAX(_recid) FROM na2.l_orderhdr));
update na2.l_orderhdr set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_orderhdr 
\echo . 
\echo Loading Table l_pprice 
\copy na2.l_pprice from '/usr1/dump-MT1/CSV/l-pprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_pprice__recid_seq', (SELECT MAX(_recid) FROM na2.l_pprice));
\echo Finish Table l_pprice 
\echo . 
\echo Loading Table l_quote 
\copy na2.l_quote from '/usr1/dump-MT1/CSV/l-quote.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_quote__recid_seq', (SELECT MAX(_recid) FROM na2.l_quote));
update na2.l_quote set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table l_quote 
\echo . 
\echo Loading Table l_segment 
\copy na2.l_segment from '/usr1/dump-MT1/CSV/l-segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_segment__recid_seq', (SELECT MAX(_recid) FROM na2.l_segment));
\echo Finish Table l_segment 
\echo . 
\echo Loading Table l_umsatz 
\copy na2.l_umsatz from '/usr1/dump-MT1/CSV/l-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_umsatz__recid_seq', (SELECT MAX(_recid) FROM na2.l_umsatz));
\echo Finish Table l_umsatz 
\echo . 
\echo Loading Table l_untergrup 
\copy na2.l_untergrup from '/usr1/dump-MT1/CSV/l-untergrup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_untergrup__recid_seq', (SELECT MAX(_recid) FROM na2.l_untergrup));
\echo Finish Table l_untergrup 
\echo . 
\echo Loading Table l_verbrauch 
\copy na2.l_verbrauch from '/usr1/dump-MT1/CSV/l-verbrauch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_verbrauch__recid_seq', (SELECT MAX(_recid) FROM na2.l_verbrauch));
\echo Finish Table l_verbrauch 
\echo . 
\echo Loading Table l_zahlbed 
\copy na2.l_zahlbed from '/usr1/dump-MT1/CSV/l-zahlbed.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.l_zahlbed__recid_seq', (SELECT MAX(_recid) FROM na2.l_zahlbed));
\echo Finish Table l_zahlbed 
\echo . 
\echo Loading Table landstat 
\copy na2.landstat from '/usr1/dump-MT1/CSV/landstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.landstat__recid_seq', (SELECT MAX(_recid) FROM na2.landstat));
\echo Finish Table landstat 
\echo . 
\echo Loading Table masseur 
\copy na2.masseur from '/usr1/dump-MT1/CSV/masseur.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.masseur__recid_seq', (SELECT MAX(_recid) FROM na2.masseur));
\echo Finish Table masseur 
\echo . 
\echo Loading Table mast_art 
\copy na2.mast_art from '/usr1/dump-MT1/CSV/mast-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mast_art__recid_seq', (SELECT MAX(_recid) FROM na2.mast_art));
\echo Finish Table mast_art 
\echo . 
\echo Loading Table master 
\copy na2.master from '/usr1/dump-MT1/CSV/master.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.master__recid_seq', (SELECT MAX(_recid) FROM na2.master));
\echo Finish Table master 
\echo . 
\echo Loading Table mathis 
\copy na2.mathis from '/usr1/dump-MT1/CSV/mathis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mathis__recid_seq', (SELECT MAX(_recid) FROM na2.mathis));
\echo Finish Table mathis 
\echo . 
\echo Loading Table mc_aclub 
\copy na2.mc_aclub from '/usr1/dump-MT1/CSV/mc-aclub.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mc_aclub__recid_seq', (SELECT MAX(_recid) FROM na2.mc_aclub));
\echo Finish Table mc_aclub 
\echo . 
\echo Loading Table mc_cardhis 
\copy na2.mc_cardhis from '/usr1/dump-MT1/CSV/mc-cardhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mc_cardhis__recid_seq', (SELECT MAX(_recid) FROM na2.mc_cardhis));
\echo Finish Table mc_cardhis 
\echo . 
\echo Loading Table mc_disc 
\copy na2.mc_disc from '/usr1/dump-MT1/CSV/mc-disc.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mc_disc__recid_seq', (SELECT MAX(_recid) FROM na2.mc_disc));
\echo Finish Table mc_disc 
\echo . 
\echo Loading Table mc_fee 
\copy na2.mc_fee from '/usr1/dump-MT1/CSV/mc-fee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mc_fee__recid_seq', (SELECT MAX(_recid) FROM na2.mc_fee));
\echo Finish Table mc_fee 
\echo . 
\echo Loading Table mc_guest 
\copy na2.mc_guest from '/usr1/dump-MT1/CSV/mc-guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mc_guest__recid_seq', (SELECT MAX(_recid) FROM na2.mc_guest));
\echo Finish Table mc_guest 
\echo . 
\echo Loading Table mc_types 
\copy na2.mc_types from '/usr1/dump-MT1/CSV/mc-types.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mc_types__recid_seq', (SELECT MAX(_recid) FROM na2.mc_types));
\echo Finish Table mc_types 
\echo . 
\echo Loading Table mealcoup 
\copy na2.mealcoup from '/usr1/dump-MT1/CSV/mealcoup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mealcoup__recid_seq', (SELECT MAX(_recid) FROM na2.mealcoup));
\echo Finish Table mealcoup 
\echo . 
\echo Loading Table messages 
\copy na2.messages from '/usr1/dump-MT1/CSV/messages.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.messages__recid_seq', (SELECT MAX(_recid) FROM na2.messages));
update na2.messages set messtext = array_replace(messtext,NULL,''); 
\echo Finish Table messages 
\echo . 
\echo Loading Table messe 
\copy na2.messe from '/usr1/dump-MT1/CSV/messe.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.messe__recid_seq', (SELECT MAX(_recid) FROM na2.messe));
\echo Finish Table messe 
\echo . 
\echo Loading Table mhis_line 
\copy na2.mhis_line from '/usr1/dump-MT1/CSV/mhis-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.mhis_line__recid_seq', (SELECT MAX(_recid) FROM na2.mhis_line));
\echo Finish Table mhis_line 
\echo . 
\echo Loading Table nation 
\copy na2.nation from '/usr1/dump-MT1/CSV/nation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.nation__recid_seq', (SELECT MAX(_recid) FROM na2.nation));
\echo Finish Table nation 
\echo . 
\echo Loading Table nationstat 
\copy na2.nationstat from '/usr1/dump-MT1/CSV/nationstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.nationstat__recid_seq', (SELECT MAX(_recid) FROM na2.nationstat));
\echo Finish Table nationstat 
\echo . 
\echo Loading Table natstat1 
\copy na2.natstat1 from '/usr1/dump-MT1/CSV/natstat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.natstat1__recid_seq', (SELECT MAX(_recid) FROM na2.natstat1));
\echo Finish Table natstat1 
\echo . 
\echo Loading Table nebenst 
\copy na2.nebenst from '/usr1/dump-MT1/CSV/nebenst.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.nebenst__recid_seq', (SELECT MAX(_recid) FROM na2.nebenst));
\echo Finish Table nebenst 
\echo . 
\echo Loading Table nightaudit 
\copy na2.nightaudit from '/usr1/dump-MT1/CSV/nightaudit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.nightaudit__recid_seq', (SELECT MAX(_recid) FROM na2.nightaudit));
\echo Finish Table nightaudit 
\echo . 
\echo Loading Table nitehist 
\copy na2.nitehist from '/usr1/dump-MT1/CSV/nitehist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.nitehist__recid_seq', (SELECT MAX(_recid) FROM na2.nitehist));
\echo Finish Table nitehist 
\echo . 
\echo Loading Table nitestor 
\copy na2.nitestor from '/usr1/dump-MT1/CSV/nitestor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.nitestor__recid_seq', (SELECT MAX(_recid) FROM na2.nitestor));
\echo Finish Table nitestor 
\echo . 
\echo Loading Table notes 
\copy na2.notes from '/usr1/dump-MT1/CSV/notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.notes__recid_seq', (SELECT MAX(_recid) FROM na2.notes));
update na2.notes set note = array_replace(note,NULL,''); 
\echo Finish Table notes 
\echo . 
\echo Loading Table outorder 
\copy na2.outorder from '/usr1/dump-MT1/CSV/outorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.outorder__recid_seq', (SELECT MAX(_recid) FROM na2.outorder));
\echo Finish Table outorder 
\echo . 
\echo Loading Table package 
\copy na2.package from '/usr1/dump-MT1/CSV/package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.package__recid_seq', (SELECT MAX(_recid) FROM na2.package));
\echo Finish Table package 
\echo . 
\echo Loading Table parameters 
\copy na2.parameters from '/usr1/dump-MT1/CSV/parameters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.parameters__recid_seq', (SELECT MAX(_recid) FROM na2.parameters));
\echo Finish Table parameters 
\echo . 
\echo Loading Table paramtext 
\copy na2.paramtext from '/usr1/dump-MT1/CSV/paramtext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.paramtext__recid_seq', (SELECT MAX(_recid) FROM na2.paramtext));
\echo Finish Table paramtext 
\echo . 
\echo Loading Table pricecod 
\copy na2.pricecod from '/usr1/dump-MT1/CSV/pricecod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.pricecod__recid_seq', (SELECT MAX(_recid) FROM na2.pricecod));
\echo Finish Table pricecod 
\echo . 
\echo Loading Table pricegrp 
\copy na2.pricegrp from '/usr1/dump-MT1/CSV/pricegrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.pricegrp__recid_seq', (SELECT MAX(_recid) FROM na2.pricegrp));
\echo Finish Table pricegrp 
\echo . 
\echo Loading Table printcod 
\copy na2.printcod from '/usr1/dump-MT1/CSV/printcod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.printcod__recid_seq', (SELECT MAX(_recid) FROM na2.printcod));
\echo Finish Table printcod 
\echo . 
\echo Loading Table printer 
\copy na2.printer from '/usr1/dump-MT1/CSV/printer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.printer__recid_seq', (SELECT MAX(_recid) FROM na2.printer));
\echo Finish Table printer 
\echo . 
\echo Loading Table prmarket 
\copy na2.prmarket from '/usr1/dump-MT1/CSV/prmarket.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.prmarket__recid_seq', (SELECT MAX(_recid) FROM na2.prmarket));
\echo Finish Table prmarket 
\echo . 
\echo Loading Table progcat 
\copy na2.progcat from '/usr1/dump-MT1/CSV/progcat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.progcat__recid_seq', (SELECT MAX(_recid) FROM na2.progcat));
\echo Finish Table progcat 
\echo . 
\echo Loading Table progfile 
\copy na2.progfile from '/usr1/dump-MT1/CSV/progfile.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.progfile__recid_seq', (SELECT MAX(_recid) FROM na2.progfile));
\echo Finish Table progfile 
\echo . 
\echo Loading Table prtable 
\copy na2.prtable from '/usr1/dump-MT1/CSV/prtable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.prtable__recid_seq', (SELECT MAX(_recid) FROM na2.prtable));
\echo Finish Table prtable 
\echo . 
\echo Loading Table queasy 
\copy na2.queasy from '/usr1/dump-MT1/CSV/queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.queasy__recid_seq', (SELECT MAX(_recid) FROM na2.queasy));
\echo Finish Table queasy 
\echo . 
\echo Loading Table ratecode 
\copy na2.ratecode from '/usr1/dump-MT1/CSV/ratecode.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.ratecode__recid_seq', (SELECT MAX(_recid) FROM na2.ratecode));
update na2.ratecode set char1 = array_replace(char1,NULL,''); 
\echo Finish Table ratecode 
\echo . 
\echo Loading Table raum 
\copy na2.raum from '/usr1/dump-MT1/CSV/raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.raum__recid_seq', (SELECT MAX(_recid) FROM na2.raum));
\echo Finish Table raum 
\echo . 
\echo Loading Table res_history 
\copy na2.res_history from '/usr1/dump-MT1/CSV/res-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.res_history__recid_seq', (SELECT MAX(_recid) FROM na2.res_history));
\echo Finish Table res_history 
\echo . 
\echo Loading Table res_line 
\copy na2.res_line from '/usr1/dump-MT1/CSV/res-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.res_line__recid_seq', (SELECT MAX(_recid) FROM na2.res_line));
\echo Finish Table res_line 
\echo . 
\echo Loading Table reservation 
\copy na2.reservation from '/usr1/dump-MT1/CSV/reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.reservation__recid_seq', (SELECT MAX(_recid) FROM na2.reservation));
\echo Finish Table reservation 
\echo . 
\echo Loading Table reslin_queasy 
\copy na2.reslin_queasy from '/usr1/dump-MT1/CSV/reslin-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.reslin_queasy__recid_seq', (SELECT MAX(_recid) FROM na2.reslin_queasy));
\echo Finish Table reslin_queasy 
\echo . 
\echo Loading Table resplan 
\copy na2.resplan from '/usr1/dump-MT1/CSV/resplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.resplan__recid_seq', (SELECT MAX(_recid) FROM na2.resplan));
\echo Finish Table resplan 
\echo . 
\echo Loading Table rg_reports 
\copy na2.rg_reports from '/usr1/dump-MT1/CSV/rg-reports.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.rg_reports__recid_seq', (SELECT MAX(_recid) FROM na2.rg_reports));
update na2.rg_reports set metadata = array_replace(metadata,NULL,''); 
update na2.rg_reports set slice_name = array_replace(slice_name,NULL,''); 
update na2.rg_reports set view_name = array_replace(view_name,NULL,''); 
\echo Finish Table rg_reports 
\echo . 
\echo Loading Table rmbudget 
\copy na2.rmbudget from '/usr1/dump-MT1/CSV/rmbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.rmbudget__recid_seq', (SELECT MAX(_recid) FROM na2.rmbudget));
update na2.rmbudget set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table rmbudget 
\echo . 
\echo Loading Table sales 
\copy na2.sales from '/usr1/dump-MT1/CSV/sales.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sales__recid_seq', (SELECT MAX(_recid) FROM na2.sales));
\echo Finish Table sales 
\echo . 
\echo Loading Table salesbud 
\copy na2.salesbud from '/usr1/dump-MT1/CSV/salesbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.salesbud__recid_seq', (SELECT MAX(_recid) FROM na2.salesbud));
\echo Finish Table salesbud 
\echo . 
\echo Loading Table salestat 
\copy na2.salestat from '/usr1/dump-MT1/CSV/salestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.salestat__recid_seq', (SELECT MAX(_recid) FROM na2.salestat));
\echo Finish Table salestat 
\echo . 
\echo Loading Table salestim 
\copy na2.salestim from '/usr1/dump-MT1/CSV/salestim.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.salestim__recid_seq', (SELECT MAX(_recid) FROM na2.salestim));
\echo Finish Table salestim 
\echo . 
\echo Loading Table segment 
\copy na2.segment from '/usr1/dump-MT1/CSV/segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.segment__recid_seq', (SELECT MAX(_recid) FROM na2.segment));
\echo Finish Table segment 
\echo . 
\echo Loading Table segmentstat 
\copy na2.segmentstat from '/usr1/dump-MT1/CSV/segmentstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.segmentstat__recid_seq', (SELECT MAX(_recid) FROM na2.segmentstat));
\echo Finish Table segmentstat 
\echo . 
\echo Loading Table sms_bcaster 
\copy na2.sms_bcaster from '/usr1/dump-MT1/CSV/sms-bcaster.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sms_bcaster__recid_seq', (SELECT MAX(_recid) FROM na2.sms_bcaster));
\echo Finish Table sms_bcaster 
\echo . 
\echo Loading Table sms_broadcast 
\copy na2.sms_broadcast from '/usr1/dump-MT1/CSV/sms-broadcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sms_broadcast__recid_seq', (SELECT MAX(_recid) FROM na2.sms_broadcast));
\echo Finish Table sms_broadcast 
\echo . 
\echo Loading Table sms_group 
\copy na2.sms_group from '/usr1/dump-MT1/CSV/sms-group.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sms_group__recid_seq', (SELECT MAX(_recid) FROM na2.sms_group));
\echo Finish Table sms_group 
\echo . 
\echo Loading Table sms_groupmbr 
\copy na2.sms_groupmbr from '/usr1/dump-MT1/CSV/sms-groupmbr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sms_groupmbr__recid_seq', (SELECT MAX(_recid) FROM na2.sms_groupmbr));
\echo Finish Table sms_groupmbr 
\echo . 
\echo Loading Table sms_received 
\copy na2.sms_received from '/usr1/dump-MT1/CSV/sms-received.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sms_received__recid_seq', (SELECT MAX(_recid) FROM na2.sms_received));
\echo Finish Table sms_received 
\echo . 
\echo Loading Table sourccod 
\copy na2.sourccod from '/usr1/dump-MT1/CSV/Sourccod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sourccod__recid_seq', (SELECT MAX(_recid) FROM na2.sourccod));
\echo Finish Table sourccod 
\echo . 
\echo Loading Table sources 
\copy na2.sources from '/usr1/dump-MT1/CSV/sources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sources__recid_seq', (SELECT MAX(_recid) FROM na2.sources));
\echo Finish Table sources 
\echo . 
\echo Loading Table sourcetext 
\copy na2.sourcetext from '/usr1/dump-MT1/CSV/sourcetext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.sourcetext__recid_seq', (SELECT MAX(_recid) FROM na2.sourcetext));
\echo Finish Table sourcetext 
\echo . 
\echo Loading Table telephone 
\copy na2.telephone from '/usr1/dump-MT1/CSV/telephone.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.telephone__recid_seq', (SELECT MAX(_recid) FROM na2.telephone));
\echo Finish Table telephone 
\echo . 
\echo Loading Table texte 
\copy na2.texte from '/usr1/dump-MT1/CSV/texte.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.texte__recid_seq', (SELECT MAX(_recid) FROM na2.texte));
\echo Finish Table texte 
\echo . 
\echo Loading Table tisch 
\copy na2.tisch from '/usr1/dump-MT1/CSV/tisch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.tisch__recid_seq', (SELECT MAX(_recid) FROM na2.tisch));
\echo Finish Table tisch 
\echo . 
\echo Loading Table tisch_res 
\copy na2.tisch_res from '/usr1/dump-MT1/CSV/tisch-res.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.tisch_res__recid_seq', (SELECT MAX(_recid) FROM na2.tisch_res));
\echo Finish Table tisch_res 
\echo . 
\echo Loading Table uebertrag 
\copy na2.uebertrag from '/usr1/dump-MT1/CSV/uebertrag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.uebertrag__recid_seq', (SELECT MAX(_recid) FROM na2.uebertrag));
\echo Finish Table uebertrag 
\echo . 
\echo Loading Table umsatz 
\copy na2.umsatz from '/usr1/dump-MT1/CSV/umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.umsatz__recid_seq', (SELECT MAX(_recid) FROM na2.umsatz));
\echo Finish Table umsatz 
\echo . 
\echo Loading Table waehrung 
\copy na2.waehrung from '/usr1/dump-MT1/CSV/waehrung.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.waehrung__recid_seq', (SELECT MAX(_recid) FROM na2.waehrung));
\echo Finish Table waehrung 
\echo . 
\echo Loading Table wakeup 
\copy na2.wakeup from '/usr1/dump-MT1/CSV/wakeup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.wakeup__recid_seq', (SELECT MAX(_recid) FROM na2.wakeup));
\echo Finish Table wakeup 
\echo . 
\echo Loading Table wgrpdep 
\copy na2.wgrpdep from '/usr1/dump-MT1/CSV/wgrpdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.wgrpdep__recid_seq', (SELECT MAX(_recid) FROM na2.wgrpdep));
\echo Finish Table wgrpdep 
\echo . 
\echo Loading Table wgrpgen 
\copy na2.wgrpgen from '/usr1/dump-MT1/CSV/wgrpgen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.wgrpgen__recid_seq', (SELECT MAX(_recid) FROM na2.wgrpgen));
\echo Finish Table wgrpgen 
\echo . 
\echo Loading Table zimkateg 
\copy na2.zimkateg from '/usr1/dump-MT1/CSV/zimkateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zimkateg__recid_seq', (SELECT MAX(_recid) FROM na2.zimkateg));
\echo Finish Table zimkateg 
\echo . 
\echo Loading Table zimmer 
\copy na2.zimmer from '/usr1/dump-MT1/CSV/zimmer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zimmer__recid_seq', (SELECT MAX(_recid) FROM na2.zimmer));
update na2.zimmer set verbindung = array_replace(verbindung,NULL,''); 
\echo Finish Table zimmer 
\echo . 
\echo Loading Table zimmer_book 
\copy na2.zimmer_book from '/usr1/dump-MT1/CSV/zimmer-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zimmer_book__recid_seq', (SELECT MAX(_recid) FROM na2.zimmer_book));
\echo Finish Table zimmer_book 
\echo . 
\echo Loading Table zimmer_book_line 
\copy na2.zimmer_book_line from '/usr1/dump-MT1/CSV/zimmer-book-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zimmer_book_line__recid_seq', (SELECT MAX(_recid) FROM na2.zimmer_book_line));
\echo Finish Table zimmer_book_line 
\echo . 
\echo Loading Table zimplan 
\copy na2.zimplan from '/usr1/dump-MT1/CSV/zimplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zimplan__recid_seq', (SELECT MAX(_recid) FROM na2.zimplan));
\echo Finish Table zimplan 
\echo . 
\echo Loading Table zimpreis 
\copy na2.zimpreis from '/usr1/dump-MT1/CSV/zimpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zimpreis__recid_seq', (SELECT MAX(_recid) FROM na2.zimpreis));
\echo Finish Table zimpreis 
\echo . 
\echo Loading Table zinrstat 
\copy na2.zinrstat from '/usr1/dump-MT1/CSV/zinrstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zinrstat__recid_seq', (SELECT MAX(_recid) FROM na2.zinrstat));
\echo Finish Table zinrstat 
\echo . 
\echo Loading Table zkstat 
\copy na2.zkstat from '/usr1/dump-MT1/CSV/zkstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zkstat__recid_seq', (SELECT MAX(_recid) FROM na2.zkstat));
\echo Finish Table zkstat 
\echo . 
\echo Loading Table zwkum 
\copy na2.zwkum from '/usr1/dump-MT1/CSV/zwkum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na2.zwkum__recid_seq', (SELECT MAX(_recid) FROM na2.zwkum));
\echo Finish Table zwkum 
\echo . 
