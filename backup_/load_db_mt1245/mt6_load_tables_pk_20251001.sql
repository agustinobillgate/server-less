\echo Loading Table absen 
\copy mt6.absen from '/usr1/dump-MT2/CSV/absen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.absen__recid_seq', (SELECT MAX(_recid) FROM mt6.absen));
\echo Finish Table absen 
\echo . 
\echo Loading Table akt_code 
\copy mt6.akt_code from '/usr1/dump-MT2/CSV/akt-code.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.akt_code__recid_seq', (SELECT MAX(_recid) FROM mt6.akt_code));
\echo Finish Table akt_code 
\echo . 
\echo Loading Table akt_cust 
\copy mt6.akt_cust from '/usr1/dump-MT2/CSV/akt-cust.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.akt_cust__recid_seq', (SELECT MAX(_recid) FROM mt6.akt_cust));
\echo Finish Table akt_cust 
\echo . 
\echo Loading Table akt_kont 
\copy mt6.akt_kont from '/usr1/dump-MT2/CSV/akt-kont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.akt_kont__recid_seq', (SELECT MAX(_recid) FROM mt6.akt_kont));
\echo Finish Table akt_kont 
\echo . 
\echo Loading Table akt_line 
\copy mt6.akt_line from '/usr1/dump-MT2/CSV/akt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.akt_line__recid_seq', (SELECT MAX(_recid) FROM mt6.akt_line));
\echo Finish Table akt_line 
\echo . 
\echo Loading Table akthdr 
\copy mt6.akthdr from '/usr1/dump-MT2/CSV/akthdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.akthdr__recid_seq', (SELECT MAX(_recid) FROM mt6.akthdr));
\echo Finish Table akthdr 
\echo . 
\echo Loading Table aktion 
\copy mt6.aktion from '/usr1/dump-MT2/CSV/aktion.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.aktion__recid_seq', (SELECT MAX(_recid) FROM mt6.aktion));
update mt6.aktion set texte = array_replace(texte,NULL,''); 
\echo Finish Table aktion 
\echo . 
\echo Loading Table ap_journal 
\copy mt6.ap_journal from '/usr1/dump-MT2/CSV/ap-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.ap_journal__recid_seq', (SELECT MAX(_recid) FROM mt6.ap_journal));
\echo Finish Table ap_journal 
\echo . 
\echo Loading Table apt_bill 
\copy mt6.apt_bill from '/usr1/dump-MT2/CSV/apt-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.apt_bill__recid_seq', (SELECT MAX(_recid) FROM mt6.apt_bill));
update mt6.apt_bill set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table apt_bill 
\echo . 
\echo Loading Table archieve 
\copy mt6.archieve from '/usr1/dump-MT2/CSV/archieve.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.archieve__recid_seq', (SELECT MAX(_recid) FROM mt6.archieve));
update mt6.archieve set char = array_replace(char,NULL,''); 
\echo Finish Table archieve 
\echo . 
\echo Loading Table argt_line 
\copy mt6.argt_line from '/usr1/dump-MT2/CSV/argt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.argt_line__recid_seq', (SELECT MAX(_recid) FROM mt6.argt_line));
\echo Finish Table argt_line 
\echo . 
\echo Loading Table argtcost 
\copy mt6.argtcost from '/usr1/dump-MT2/CSV/argtcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.argtcost__recid_seq', (SELECT MAX(_recid) FROM mt6.argtcost));
update mt6.argtcost set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtcost 
\echo . 
\echo Loading Table argtstat 
\copy mt6.argtstat from '/usr1/dump-MT2/CSV/argtstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.argtstat__recid_seq', (SELECT MAX(_recid) FROM mt6.argtstat));
update mt6.argtstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtstat 
\echo . 
\echo Loading Table arrangement 
\copy mt6.arrangement from '/usr1/dump-MT2/CSV/arrangement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.arrangement__recid_seq', (SELECT MAX(_recid) FROM mt6.arrangement));
update mt6.arrangement set argt_rgbez2 = array_replace(argt_rgbez2,NULL,''); 
\echo Finish Table arrangement 
\echo . 
\echo Loading Table artikel 
\copy mt6.artikel from '/usr1/dump-MT2/CSV/artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.artikel__recid_seq', (SELECT MAX(_recid) FROM mt6.artikel));
\echo Finish Table artikel 
\echo . 
\echo Loading Table artprice 
\copy mt6.artprice from '/usr1/dump-MT2/CSV/artprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.artprice__recid_seq', (SELECT MAX(_recid) FROM mt6.artprice));
\echo Finish Table artprice 
\echo . 
\echo Loading Table b_history 
\copy mt6.b_history from '/usr1/dump-MT2/CSV/b-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.b_history__recid_seq', (SELECT MAX(_recid) FROM mt6.b_history));
update mt6.b_history set anlass = array_replace(anlass,NULL,''); 
update mt6.b_history set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update mt6.b_history set ape__speisen = array_replace(ape__speisen,NULL,''); 
update mt6.b_history set arrival = array_replace(arrival,NULL,''); 
update mt6.b_history set c_resstatus = array_replace(c_resstatus,NULL,''); 
update mt6.b_history set dance = array_replace(dance,NULL,''); 
update mt6.b_history set deko2 = array_replace(deko2,NULL,''); 
update mt6.b_history set dekoration = array_replace(dekoration,NULL,''); 
update mt6.b_history set digestif = array_replace(digestif,NULL,''); 
update mt6.b_history set dinner = array_replace(dinner,NULL,''); 
update mt6.b_history set f_menu = array_replace(f_menu,NULL,''); 
update mt6.b_history set f_no = array_replace(f_no,NULL,''); 
update mt6.b_history set fotograf = array_replace(fotograf,NULL,''); 
update mt6.b_history set gaestebuch = array_replace(gaestebuch,NULL,''); 
update mt6.b_history set garderobe = array_replace(garderobe,NULL,''); 
update mt6.b_history set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update mt6.b_history set kaffee = array_replace(kaffee,NULL,''); 
update mt6.b_history set kartentext = array_replace(kartentext,NULL,''); 
update mt6.b_history set kontaktperson = array_replace(kontaktperson,NULL,''); 
update mt6.b_history set kuenstler = array_replace(kuenstler,NULL,''); 
update mt6.b_history set menue = array_replace(menue,NULL,''); 
update mt6.b_history set menuekarten = array_replace(menuekarten,NULL,''); 
update mt6.b_history set musik = array_replace(musik,NULL,''); 
update mt6.b_history set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update mt6.b_history set nadkarte = array_replace(nadkarte,NULL,''); 
update mt6.b_history set ndessen = array_replace(ndessen,NULL,''); 
update mt6.b_history set payment_userinit = array_replace(payment_userinit,NULL,''); 
update mt6.b_history set personen2 = array_replace(personen2,NULL,''); 
update mt6.b_history set raeume = array_replace(raeume,NULL,''); 
update mt6.b_history set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update mt6.b_history set raummiete = array_replace(raummiete,NULL,''); 
update mt6.b_history set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update mt6.b_history set service = array_replace(service,NULL,''); 
update mt6.b_history set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update mt6.b_history set sonstiges = array_replace(sonstiges,NULL,''); 
update mt6.b_history set technik = array_replace(technik,NULL,''); 
update mt6.b_history set tischform = array_replace(tischform,NULL,''); 
update mt6.b_history set tischordnung = array_replace(tischordnung,NULL,''); 
update mt6.b_history set tischplan = array_replace(tischplan,NULL,''); 
update mt6.b_history set tischreden = array_replace(tischreden,NULL,''); 
update mt6.b_history set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update mt6.b_history set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update mt6.b_history set va_ablauf = array_replace(va_ablauf,NULL,''); 
update mt6.b_history set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update mt6.b_history set vip = array_replace(vip,NULL,''); 
update mt6.b_history set weine = array_replace(weine,NULL,''); 
update mt6.b_history set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table b_history 
\echo . 
\echo Loading Table b_oorder 
\copy mt6.b_oorder from '/usr1/dump-MT2/CSV/b-oorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.b_oorder__recid_seq', (SELECT MAX(_recid) FROM mt6.b_oorder));
\echo Finish Table b_oorder 
\echo . 
\echo Loading Table b_storno 
\copy mt6.b_storno from '/usr1/dump-MT2/CSV/b-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.b_storno__recid_seq', (SELECT MAX(_recid) FROM mt6.b_storno));
update mt6.b_storno set grund = array_replace(grund,NULL,''); 
\echo Finish Table b_storno 
\echo . 
\echo Loading Table ba_rset 
\copy mt6.ba_rset from '/usr1/dump-MT2/CSV/ba-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.ba_rset__recid_seq', (SELECT MAX(_recid) FROM mt6.ba_rset));
\echo Finish Table ba_rset 
\echo . 
\echo Loading Table ba_setup 
\copy mt6.ba_setup from '/usr1/dump-MT2/CSV/ba-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.ba_setup__recid_seq', (SELECT MAX(_recid) FROM mt6.ba_setup));
\echo Finish Table ba_setup 
\echo . 
\echo Loading Table ba_typ 
\copy mt6.ba_typ from '/usr1/dump-MT2/CSV/ba-typ.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.ba_typ__recid_seq', (SELECT MAX(_recid) FROM mt6.ba_typ));
\echo Finish Table ba_typ 
\echo . 
\echo Loading Table bankrep 
\copy mt6.bankrep from '/usr1/dump-MT2/CSV/bankrep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bankrep__recid_seq', (SELECT MAX(_recid) FROM mt6.bankrep));
update mt6.bankrep set anlass = array_replace(anlass,NULL,''); 
update mt6.bankrep set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update mt6.bankrep set ape__speisen = array_replace(ape__speisen,NULL,''); 
update mt6.bankrep set dekoration = array_replace(dekoration,NULL,''); 
update mt6.bankrep set digestif = array_replace(digestif,NULL,''); 
update mt6.bankrep set fotograf = array_replace(fotograf,NULL,''); 
update mt6.bankrep set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update mt6.bankrep set kartentext = array_replace(kartentext,NULL,''); 
update mt6.bankrep set kontaktperson = array_replace(kontaktperson,NULL,''); 
update mt6.bankrep set menue = array_replace(menue,NULL,''); 
update mt6.bankrep set menuekarten = array_replace(menuekarten,NULL,''); 
update mt6.bankrep set musik = array_replace(musik,NULL,''); 
update mt6.bankrep set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update mt6.bankrep set ndessen = array_replace(ndessen,NULL,''); 
update mt6.bankrep set personen2 = array_replace(personen2,NULL,''); 
update mt6.bankrep set raeume = array_replace(raeume,NULL,''); 
update mt6.bankrep set raummiete = array_replace(raummiete,NULL,''); 
update mt6.bankrep set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update mt6.bankrep set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update mt6.bankrep set sonstiges = array_replace(sonstiges,NULL,''); 
update mt6.bankrep set technik = array_replace(technik,NULL,''); 
update mt6.bankrep set tischform = array_replace(tischform,NULL,''); 
update mt6.bankrep set tischreden = array_replace(tischreden,NULL,''); 
update mt6.bankrep set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update mt6.bankrep set weine = array_replace(weine,NULL,''); 
update mt6.bankrep set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bankrep 
\echo . 
\echo Loading Table bankres 
\copy mt6.bankres from '/usr1/dump-MT2/CSV/bankres.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bankres__recid_seq', (SELECT MAX(_recid) FROM mt6.bankres));
update mt6.bankres set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table bankres 
\echo . 
\echo Loading Table bediener 
\copy mt6.bediener from '/usr1/dump-MT2/CSV/bediener.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bediener__recid_seq', (SELECT MAX(_recid) FROM mt6.bediener));
\echo Finish Table bediener 
\echo . 
\echo Loading Table bill 
\copy mt6.bill from '/usr1/dump-MT2/CSV/bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bill__recid_seq', (SELECT MAX(_recid) FROM mt6.bill));
\echo Finish Table bill 
\echo . 
\echo Loading Table bill_lin_tax 
\copy mt6.bill_lin_tax from '/usr1/dump-MT2/CSV/bill-lin-tax.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bill_lin_tax__recid_seq', (SELECT MAX(_recid) FROM mt6.bill_lin_tax));
\echo Finish Table bill_lin_tax 
\echo . 
\echo Loading Table bill_line 
\copy mt6.bill_line from '/usr1/dump-MT2/CSV/bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bill_line__recid_seq', (SELECT MAX(_recid) FROM mt6.bill_line));
\echo Finish Table bill_line 
\echo . 
\echo Loading Table billhis 
\copy mt6.billhis from '/usr1/dump-MT2/CSV/billhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.billhis__recid_seq', (SELECT MAX(_recid) FROM mt6.billhis));
\echo Finish Table billhis 
\echo . 
\echo Loading Table billjournal 
\copy mt6.billjournal from '/usr1/dump-MT2/CSV/billjournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.billjournal__recid_seq', (SELECT MAX(_recid) FROM mt6.billjournal));
\echo Finish Table billjournal 
\echo . 
\echo Loading Table bk_beleg 
\copy mt6.bk_beleg from '/usr1/dump-MT2/CSV/bk-beleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_beleg__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_beleg));
\echo Finish Table bk_beleg 
\echo . 
\echo Loading Table bk_fsdef 
\copy mt6.bk_fsdef from '/usr1/dump-MT2/CSV/bk-fsdef.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_fsdef__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_fsdef));
\echo Finish Table bk_fsdef 
\echo . 
\echo Loading Table bk_func 
\copy mt6.bk_func from '/usr1/dump-MT2/CSV/bk-func.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_func__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_func));
update mt6.bk_func set anlass = array_replace(anlass,NULL,''); 
update mt6.bk_func set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update mt6.bk_func set ape__speisen = array_replace(ape__speisen,NULL,''); 
update mt6.bk_func set arrival = array_replace(arrival,NULL,''); 
update mt6.bk_func set c_resstatus = array_replace(c_resstatus,NULL,''); 
update mt6.bk_func set dance = array_replace(dance,NULL,''); 
update mt6.bk_func set deko2 = array_replace(deko2,NULL,''); 
update mt6.bk_func set dekoration = array_replace(dekoration,NULL,''); 
update mt6.bk_func set digestif = array_replace(digestif,NULL,''); 
update mt6.bk_func set dinner = array_replace(dinner,NULL,''); 
update mt6.bk_func set f_menu = array_replace(f_menu,NULL,''); 
update mt6.bk_func set f_no = array_replace(f_no,NULL,''); 
update mt6.bk_func set fotograf = array_replace(fotograf,NULL,''); 
update mt6.bk_func set gaestebuch = array_replace(gaestebuch,NULL,''); 
update mt6.bk_func set garderobe = array_replace(garderobe,NULL,''); 
update mt6.bk_func set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update mt6.bk_func set kaffee = array_replace(kaffee,NULL,''); 
update mt6.bk_func set kartentext = array_replace(kartentext,NULL,''); 
update mt6.bk_func set kontaktperson = array_replace(kontaktperson,NULL,''); 
update mt6.bk_func set kuenstler = array_replace(kuenstler,NULL,''); 
update mt6.bk_func set menue = array_replace(menue,NULL,''); 
update mt6.bk_func set menuekarten = array_replace(menuekarten,NULL,''); 
update mt6.bk_func set musik = array_replace(musik,NULL,''); 
update mt6.bk_func set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update mt6.bk_func set nadkarte = array_replace(nadkarte,NULL,''); 
update mt6.bk_func set ndessen = array_replace(ndessen,NULL,''); 
update mt6.bk_func set personen2 = array_replace(personen2,NULL,''); 
update mt6.bk_func set raeume = array_replace(raeume,NULL,''); 
update mt6.bk_func set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update mt6.bk_func set raummiete = array_replace(raummiete,NULL,''); 
update mt6.bk_func set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update mt6.bk_func set service = array_replace(service,NULL,''); 
update mt6.bk_func set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update mt6.bk_func set sonstiges = array_replace(sonstiges,NULL,''); 
update mt6.bk_func set technik = array_replace(technik,NULL,''); 
update mt6.bk_func set tischform = array_replace(tischform,NULL,''); 
update mt6.bk_func set tischordnung = array_replace(tischordnung,NULL,''); 
update mt6.bk_func set tischplan = array_replace(tischplan,NULL,''); 
update mt6.bk_func set tischreden = array_replace(tischreden,NULL,''); 
update mt6.bk_func set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update mt6.bk_func set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update mt6.bk_func set va_ablauf = array_replace(va_ablauf,NULL,''); 
update mt6.bk_func set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update mt6.bk_func set vip = array_replace(vip,NULL,''); 
update mt6.bk_func set weine = array_replace(weine,NULL,''); 
update mt6.bk_func set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bk_func 
\echo . 
\echo Loading Table bk_package 
\copy mt6.bk_package from '/usr1/dump-MT2/CSV/bk-package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_package__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_package));
\echo Finish Table bk_package 
\echo . 
\echo Loading Table bk_pause 
\copy mt6.bk_pause from '/usr1/dump-MT2/CSV/bk-pause.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_pause__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_pause));
\echo Finish Table bk_pause 
\echo . 
\echo Loading Table bk_rart 
\copy mt6.bk_rart from '/usr1/dump-MT2/CSV/bk-rart.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_rart__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_rart));
\echo Finish Table bk_rart 
\echo . 
\echo Loading Table bk_raum 
\copy mt6.bk_raum from '/usr1/dump-MT2/CSV/bk-raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_raum__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_raum));
\echo Finish Table bk_raum 
\echo . 
\echo Loading Table bk_reser 
\copy mt6.bk_reser from '/usr1/dump-MT2/CSV/bk-reser.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_reser__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_reser));
\echo Finish Table bk_reser 
\echo . 
\echo Loading Table bk_rset 
\copy mt6.bk_rset from '/usr1/dump-MT2/CSV/bk-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_rset__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_rset));
\echo Finish Table bk_rset 
\echo . 
\echo Loading Table bk_setup 
\copy mt6.bk_setup from '/usr1/dump-MT2/CSV/bk-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_setup__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_setup));
\echo Finish Table bk_setup 
\echo . 
\echo Loading Table bk_stat 
\copy mt6.bk_stat from '/usr1/dump-MT2/CSV/bk-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_stat__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_stat));
\echo Finish Table bk_stat 
\echo . 
\echo Loading Table bk_veran 
\copy mt6.bk_veran from '/usr1/dump-MT2/CSV/bk-veran.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bk_veran__recid_seq', (SELECT MAX(_recid) FROM mt6.bk_veran));
update mt6.bk_veran set payment_userinit = array_replace(payment_userinit,NULL,''); 
\echo Finish Table bk_veran 
\echo . 
\echo Loading Table bl_dates 
\copy mt6.bl_dates from '/usr1/dump-MT2/CSV/bl-dates.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bl_dates__recid_seq', (SELECT MAX(_recid) FROM mt6.bl_dates));
\echo Finish Table bl_dates 
\echo . 
\echo Loading Table blinehis 
\copy mt6.blinehis from '/usr1/dump-MT2/CSV/blinehis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.blinehis__recid_seq', (SELECT MAX(_recid) FROM mt6.blinehis));
\echo Finish Table blinehis 
\echo . 
\echo Loading Table bresline 
\copy mt6.bresline from '/usr1/dump-MT2/CSV/bresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.bresline__recid_seq', (SELECT MAX(_recid) FROM mt6.bresline));
update mt6.bresline set texte = array_replace(texte,NULL,''); 
\echo Finish Table bresline 
\echo . 
\echo Loading Table brief 
\copy mt6.brief from '/usr1/dump-MT2/CSV/brief.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.brief__recid_seq', (SELECT MAX(_recid) FROM mt6.brief));
\echo Finish Table brief 
\echo . 
\echo Loading Table brieftmp 
\copy mt6.brieftmp from '/usr1/dump-MT2/CSV/brieftmp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.brieftmp__recid_seq', (SELECT MAX(_recid) FROM mt6.brieftmp));
\echo Finish Table brieftmp 
\echo . 
\echo Loading Table briefzei 
\copy mt6.briefzei from '/usr1/dump-MT2/CSV/briefzei.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.briefzei__recid_seq', (SELECT MAX(_recid) FROM mt6.briefzei));
\echo Finish Table briefzei 
\echo . 
\echo Loading Table budget 
\copy mt6.budget from '/usr1/dump-MT2/CSV/budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.budget__recid_seq', (SELECT MAX(_recid) FROM mt6.budget));
\echo Finish Table budget 
\echo . 
\echo Loading Table calls 
\copy mt6.calls from '/usr1/dump-MT2/CSV/calls.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.calls__recid_seq', (SELECT MAX(_recid) FROM mt6.calls));
\echo Finish Table calls 
\echo . 
\echo Loading Table cl_bonus 
\copy mt6.cl_bonus from '/usr1/dump-MT2/CSV/cl-bonus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_bonus__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_bonus));
\echo Finish Table cl_bonus 
\echo . 
\echo Loading Table cl_book 
\copy mt6.cl_book from '/usr1/dump-MT2/CSV/cl-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_book__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_book));
\echo Finish Table cl_book 
\echo . 
\echo Loading Table cl_checkin 
\copy mt6.cl_checkin from '/usr1/dump-MT2/CSV/cl-checkin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_checkin__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_checkin));
\echo Finish Table cl_checkin 
\echo . 
\echo Loading Table cl_class 
\copy mt6.cl_class from '/usr1/dump-MT2/CSV/cl-class.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_class__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_class));
\echo Finish Table cl_class 
\echo . 
\echo Loading Table cl_enroll 
\copy mt6.cl_enroll from '/usr1/dump-MT2/CSV/cl-enroll.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_enroll__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_enroll));
\echo Finish Table cl_enroll 
\echo . 
\echo Loading Table cl_free 
\copy mt6.cl_free from '/usr1/dump-MT2/CSV/cl-free.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_free__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_free));
\echo Finish Table cl_free 
\echo . 
\echo Loading Table cl_histci 
\copy mt6.cl_histci from '/usr1/dump-MT2/CSV/cl-histci.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_histci__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_histci));
\echo Finish Table cl_histci 
\echo . 
\echo Loading Table cl_histpay 
\copy mt6.cl_histpay from '/usr1/dump-MT2/CSV/cl-histpay.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_histpay__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_histpay));
\echo Finish Table cl_histpay 
\echo . 
\echo Loading Table cl_histstatus 
\copy mt6.cl_histstatus from '/usr1/dump-MT2/CSV/cl-histstatus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_histstatus__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_histstatus));
\echo Finish Table cl_histstatus 
\echo . 
\echo Loading Table cl_histtrain 
\copy mt6.cl_histtrain from '/usr1/dump-MT2/CSV/cl-histtrain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_histtrain__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_histtrain));
\echo Finish Table cl_histtrain 
\echo . 
\echo Loading Table cl_histvisit 
\copy mt6.cl_histvisit from '/usr1/dump-MT2/CSV/cl-histvisit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_histvisit__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_histvisit));
\echo Finish Table cl_histvisit 
\echo . 
\echo Loading Table cl_home 
\copy mt6.cl_home from '/usr1/dump-MT2/CSV/cl-home.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_home__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_home));
\echo Finish Table cl_home 
\echo . 
\echo Loading Table cl_location 
\copy mt6.cl_location from '/usr1/dump-MT2/CSV/cl-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_location__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_location));
\echo Finish Table cl_location 
\echo . 
\echo Loading Table cl_locker 
\copy mt6.cl_locker from '/usr1/dump-MT2/CSV/cl-locker.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_locker__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_locker));
\echo Finish Table cl_locker 
\echo . 
\echo Loading Table cl_log 
\copy mt6.cl_log from '/usr1/dump-MT2/CSV/cl-log.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_log__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_log));
\echo Finish Table cl_log 
\echo . 
\echo Loading Table cl_member 
\copy mt6.cl_member from '/usr1/dump-MT2/CSV/cl-member.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_member__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_member));
\echo Finish Table cl_member 
\echo . 
\echo Loading Table cl_memtype 
\copy mt6.cl_memtype from '/usr1/dump-MT2/CSV/cl-memtype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_memtype__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_memtype));
\echo Finish Table cl_memtype 
\echo . 
\echo Loading Table cl_paysched 
\copy mt6.cl_paysched from '/usr1/dump-MT2/CSV/cl-paysched.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_paysched__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_paysched));
\echo Finish Table cl_paysched 
\echo . 
\echo Loading Table cl_stat 
\copy mt6.cl_stat from '/usr1/dump-MT2/CSV/cl-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_stat__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_stat));
\echo Finish Table cl_stat 
\echo . 
\echo Loading Table cl_stat1 
\copy mt6.cl_stat1 from '/usr1/dump-MT2/CSV/cl-stat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_stat1__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_stat1));
\echo Finish Table cl_stat1 
\echo . 
\echo Loading Table cl_towel 
\copy mt6.cl_towel from '/usr1/dump-MT2/CSV/cl-towel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_towel__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_towel));
\echo Finish Table cl_towel 
\echo . 
\echo Loading Table cl_trainer 
\copy mt6.cl_trainer from '/usr1/dump-MT2/CSV/cl-trainer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_trainer__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_trainer));
\echo Finish Table cl_trainer 
\echo . 
\echo Loading Table cl_upgrade 
\copy mt6.cl_upgrade from '/usr1/dump-MT2/CSV/cl-upgrade.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cl_upgrade__recid_seq', (SELECT MAX(_recid) FROM mt6.cl_upgrade));
\echo Finish Table cl_upgrade 
\echo . 
\echo Loading Table costbudget 
\copy mt6.costbudget from '/usr1/dump-MT2/CSV/costbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.costbudget__recid_seq', (SELECT MAX(_recid) FROM mt6.costbudget));
\echo Finish Table costbudget 
\echo . 
\echo Loading Table counters 
\copy mt6.counters from '/usr1/dump-MT2/CSV/counters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.counters__recid_seq', (SELECT MAX(_recid) FROM mt6.counters));
\echo Finish Table counters 
\echo . 
\echo Loading Table crm_campaign 
\copy mt6.crm_campaign from '/usr1/dump-MT2/CSV/crm-campaign.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_campaign__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_campaign));
\echo Finish Table crm_campaign 
\echo . 
\echo Loading Table crm_category 
\copy mt6.crm_category from '/usr1/dump-MT2/CSV/crm-category.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_category__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_category));
\echo Finish Table crm_category 
\echo . 
\echo Loading Table crm_dept 
\copy mt6.crm_dept from '/usr1/dump-MT2/CSV/crm-dept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_dept__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_dept));
\echo Finish Table crm_dept 
\echo . 
\echo Loading Table crm_dtl 
\copy mt6.crm_dtl from '/usr1/dump-MT2/CSV/crm-dtl.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_dtl__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_dtl));
\echo Finish Table crm_dtl 
\echo . 
\echo Loading Table crm_email 
\copy mt6.crm_email from '/usr1/dump-MT2/CSV/crm-email.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_email__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_email));
\echo Finish Table crm_email 
\echo . 
\echo Loading Table crm_event 
\copy mt6.crm_event from '/usr1/dump-MT2/CSV/crm-event.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_event__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_event));
\echo Finish Table crm_event 
\echo . 
\echo Loading Table crm_feedhdr 
\copy mt6.crm_feedhdr from '/usr1/dump-MT2/CSV/crm-feedhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_feedhdr__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_feedhdr));
\echo Finish Table crm_feedhdr 
\echo . 
\echo Loading Table crm_fnlresult 
\copy mt6.crm_fnlresult from '/usr1/dump-MT2/CSV/crm-fnlresult.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_fnlresult__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_fnlresult));
\echo Finish Table crm_fnlresult 
\echo . 
\echo Loading Table crm_language 
\copy mt6.crm_language from '/usr1/dump-MT2/CSV/crm-language.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_language__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_language));
\echo Finish Table crm_language 
\echo . 
\echo Loading Table crm_question 
\copy mt6.crm_question from '/usr1/dump-MT2/CSV/crm-question.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_question__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_question));
\echo Finish Table crm_question 
\echo . 
\echo Loading Table crm_tamplang 
\copy mt6.crm_tamplang from '/usr1/dump-MT2/CSV/crm-tamplang.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_tamplang__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_tamplang));
\echo Finish Table crm_tamplang 
\echo . 
\echo Loading Table crm_template 
\copy mt6.crm_template from '/usr1/dump-MT2/CSV/crm-template.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.crm_template__recid_seq', (SELECT MAX(_recid) FROM mt6.crm_template));
\echo Finish Table crm_template 
\echo . 
\echo Loading Table cross_dtl 
\copy mt6.cross_dtl from '/usr1/dump-MT2/CSV/cross-DTL.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cross_dtl__recid_seq', (SELECT MAX(_recid) FROM mt6.cross_dtl));
\echo Finish Table cross_dtl 
\echo . 
\echo Loading Table cross_hdr 
\copy mt6.cross_hdr from '/usr1/dump-MT2/CSV/cross-HDR.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.cross_hdr__recid_seq', (SELECT MAX(_recid) FROM mt6.cross_hdr));
\echo Finish Table cross_hdr 
\echo . 
\echo Loading Table debitor 
\copy mt6.debitor from '/usr1/dump-MT2/CSV/debitor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.debitor__recid_seq', (SELECT MAX(_recid) FROM mt6.debitor));
\echo Finish Table debitor 
\echo . 
\echo Loading Table debthis 
\copy mt6.debthis from '/usr1/dump-MT2/CSV/debthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.debthis__recid_seq', (SELECT MAX(_recid) FROM mt6.debthis));
\echo Finish Table debthis 
\echo . 
\echo Loading Table desttext 
\copy mt6.desttext from '/usr1/dump-MT2/CSV/desttext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.desttext__recid_seq', (SELECT MAX(_recid) FROM mt6.desttext));
\echo Finish Table desttext 
\echo . 
\echo Loading Table dml_art 
\copy mt6.dml_art from '/usr1/dump-MT2/CSV/dml-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.dml_art__recid_seq', (SELECT MAX(_recid) FROM mt6.dml_art));
\echo Finish Table dml_art 
\echo . 
\echo Loading Table dml_artdep 
\copy mt6.dml_artdep from '/usr1/dump-MT2/CSV/dml-artdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.dml_artdep__recid_seq', (SELECT MAX(_recid) FROM mt6.dml_artdep));
\echo Finish Table dml_artdep 
\echo . 
\echo Loading Table dml_rate 
\copy mt6.dml_rate from '/usr1/dump-MT2/CSV/dml-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.dml_rate__recid_seq', (SELECT MAX(_recid) FROM mt6.dml_rate));
\echo Finish Table dml_rate 
\echo . 
\echo Loading Table eg_action 
\copy mt6.eg_action from '/usr1/dump-MT2/CSV/eg-action.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_action__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_action));
\echo Finish Table eg_action 
\echo . 
\echo Loading Table eg_alert 
\copy mt6.eg_alert from '/usr1/dump-MT2/CSV/eg-Alert.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_alert__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_alert));
\echo Finish Table eg_alert 
\echo . 
\echo Loading Table eg_budget 
\copy mt6.eg_budget from '/usr1/dump-MT2/CSV/eg-budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_budget__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_budget));
\echo Finish Table eg_budget 
\echo . 
\echo Loading Table eg_cost 
\copy mt6.eg_cost from '/usr1/dump-MT2/CSV/eg-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_cost__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_cost));
\echo Finish Table eg_cost 
\echo . 
\echo Loading Table eg_duration 
\copy mt6.eg_duration from '/usr1/dump-MT2/CSV/eg-Duration.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_duration__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_duration));
\echo Finish Table eg_duration 
\echo . 
\echo Loading Table eg_location 
\copy mt6.eg_location from '/usr1/dump-MT2/CSV/eg-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_location__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_location));
\echo Finish Table eg_location 
\echo . 
\echo Loading Table eg_mainstat 
\copy mt6.eg_mainstat from '/usr1/dump-MT2/CSV/eg-MainStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_mainstat__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_mainstat));
\echo Finish Table eg_mainstat 
\echo . 
\echo Loading Table eg_maintain 
\copy mt6.eg_maintain from '/usr1/dump-MT2/CSV/eg-maintain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_maintain__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_maintain));
\echo Finish Table eg_maintain 
\echo . 
\echo Loading Table eg_mdetail 
\copy mt6.eg_mdetail from '/usr1/dump-MT2/CSV/eg-mdetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_mdetail__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_mdetail));
\echo Finish Table eg_mdetail 
\echo . 
\echo Loading Table eg_messageno 
\copy mt6.eg_messageno from '/usr1/dump-MT2/CSV/eg-MessageNo.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_messageno__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_messageno));
\echo Finish Table eg_messageno 
\echo . 
\echo Loading Table eg_mobilenr 
\copy mt6.eg_mobilenr from '/usr1/dump-MT2/CSV/eg-mobileNr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_mobilenr__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_mobilenr));
\echo Finish Table eg_mobilenr 
\echo . 
\echo Loading Table eg_moveproperty 
\copy mt6.eg_moveproperty from '/usr1/dump-MT2/CSV/eg-moveProperty.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_moveproperty__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_moveproperty));
\echo Finish Table eg_moveproperty 
\echo . 
\echo Loading Table eg_property 
\copy mt6.eg_property from '/usr1/dump-MT2/CSV/eg-property.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_property__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_property));
\echo Finish Table eg_property 
\echo . 
\echo Loading Table eg_propmeter 
\copy mt6.eg_propmeter from '/usr1/dump-MT2/CSV/eg-propMeter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_propmeter__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_propmeter));
\echo Finish Table eg_propmeter 
\echo . 
\echo Loading Table eg_queasy 
\copy mt6.eg_queasy from '/usr1/dump-MT2/CSV/eg-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_queasy__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_queasy));
\echo Finish Table eg_queasy 
\echo . 
\echo Loading Table eg_reqdetail 
\copy mt6.eg_reqdetail from '/usr1/dump-MT2/CSV/eg-reqDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_reqdetail__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_reqdetail));
\echo Finish Table eg_reqdetail 
\echo . 
\echo Loading Table eg_reqif 
\copy mt6.eg_reqif from '/usr1/dump-MT2/CSV/eg-reqif.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_reqif__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_reqif));
\echo Finish Table eg_reqif 
\echo . 
\echo Loading Table eg_reqstat 
\copy mt6.eg_reqstat from '/usr1/dump-MT2/CSV/eg-ReqStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_reqstat__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_reqstat));
\echo Finish Table eg_reqstat 
\echo . 
\echo Loading Table eg_request 
\copy mt6.eg_request from '/usr1/dump-MT2/CSV/eg-request.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_request__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_request));
\echo Finish Table eg_request 
\echo . 
\echo Loading Table eg_resources 
\copy mt6.eg_resources from '/usr1/dump-MT2/CSV/eg-resources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_resources__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_resources));
\echo Finish Table eg_resources 
\echo . 
\echo Loading Table eg_staff 
\copy mt6.eg_staff from '/usr1/dump-MT2/CSV/eg-staff.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_staff__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_staff));
\echo Finish Table eg_staff 
\echo . 
\echo Loading Table eg_stat 
\copy mt6.eg_stat from '/usr1/dump-MT2/CSV/eg-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_stat__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_stat));
\echo Finish Table eg_stat 
\echo . 
\echo Loading Table eg_subtask 
\copy mt6.eg_subtask from '/usr1/dump-MT2/CSV/eg-subtask.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_subtask__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_subtask));
\echo Finish Table eg_subtask 
\echo . 
\echo Loading Table eg_vendor 
\copy mt6.eg_vendor from '/usr1/dump-MT2/CSV/eg-vendor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_vendor__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_vendor));
\echo Finish Table eg_vendor 
\echo . 
\echo Loading Table eg_vperform 
\copy mt6.eg_vperform from '/usr1/dump-MT2/CSV/eg-vperform.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.eg_vperform__recid_seq', (SELECT MAX(_recid) FROM mt6.eg_vperform));
\echo Finish Table eg_vperform 
\echo . 
\echo Loading Table ekum 
\copy mt6.ekum from '/usr1/dump-MT2/CSV/ekum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.ekum__recid_seq', (SELECT MAX(_recid) FROM mt6.ekum));
\echo Finish Table ekum 
\echo . 
\echo Loading Table employee 
\copy mt6.employee from '/usr1/dump-MT2/CSV/employee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.employee__recid_seq', (SELECT MAX(_recid) FROM mt6.employee));
update mt6.employee set child = array_replace(child,NULL,''); 
\echo Finish Table employee 
\echo . 
\echo Loading Table equiplan 
\copy mt6.equiplan from '/usr1/dump-MT2/CSV/equiplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.equiplan__recid_seq', (SELECT MAX(_recid) FROM mt6.equiplan));
\echo Finish Table equiplan 
\echo . 
\echo Loading Table exrate 
\copy mt6.exrate from '/usr1/dump-MT2/CSV/exrate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.exrate__recid_seq', (SELECT MAX(_recid) FROM mt6.exrate));
\echo Finish Table exrate 
\echo . 
\echo Loading Table fa_artikel 
\copy mt6.fa_artikel from '/usr1/dump-MT2/CSV/fa-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_artikel__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_artikel));
\echo Finish Table fa_artikel 
\echo . 
\echo Loading Table fa_counter 
\copy mt6.fa_counter from '/usr1/dump-MT2/CSV/fa-Counter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_counter__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_counter));
\echo Finish Table fa_counter 
\echo . 
\echo Loading Table fa_dp 
\copy mt6.fa_dp from '/usr1/dump-MT2/CSV/fa-DP.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_dp__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_dp));
\echo Finish Table fa_dp 
\echo . 
\echo Loading Table fa_grup 
\copy mt6.fa_grup from '/usr1/dump-MT2/CSV/fa-grup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_grup__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_grup));
\echo Finish Table fa_grup 
\echo . 
\echo Loading Table fa_kateg 
\copy mt6.fa_kateg from '/usr1/dump-MT2/CSV/fa-kateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_kateg__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_kateg));
\echo Finish Table fa_kateg 
\echo . 
\echo Loading Table fa_lager 
\copy mt6.fa_lager from '/usr1/dump-MT2/CSV/fa-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_lager__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_lager));
\echo Finish Table fa_lager 
\echo . 
\echo Loading Table fa_op 
\copy mt6.fa_op from '/usr1/dump-MT2/CSV/fa-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_op__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_op));
\echo Finish Table fa_op 
\echo . 
\echo Loading Table fa_order 
\copy mt6.fa_order from '/usr1/dump-MT2/CSV/fa-Order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_order__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_order));
\echo Finish Table fa_order 
\echo . 
\echo Loading Table fa_ordheader 
\copy mt6.fa_ordheader from '/usr1/dump-MT2/CSV/fa-OrdHeader.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_ordheader__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_ordheader));
\echo Finish Table fa_ordheader 
\echo . 
\echo Loading Table fa_quodetail 
\copy mt6.fa_quodetail from '/usr1/dump-MT2/CSV/fa-QuoDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_quodetail__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_quodetail));
\echo Finish Table fa_quodetail 
\echo . 
\echo Loading Table fa_quotation 
\copy mt6.fa_quotation from '/usr1/dump-MT2/CSV/fa-quotation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_quotation__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_quotation));
\echo Finish Table fa_quotation 
\echo . 
\echo Loading Table fa_user 
\copy mt6.fa_user from '/usr1/dump-MT2/CSV/fa-user.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fa_user__recid_seq', (SELECT MAX(_recid) FROM mt6.fa_user));
update mt6.fa_user set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table fa_user 
\echo . 
\echo Loading Table fbstat 
\copy mt6.fbstat from '/usr1/dump-MT2/CSV/fbstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fbstat__recid_seq', (SELECT MAX(_recid) FROM mt6.fbstat));
\echo Finish Table fbstat 
\echo . 
\echo Loading Table feiertag 
\copy mt6.feiertag from '/usr1/dump-MT2/CSV/feiertag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.feiertag__recid_seq', (SELECT MAX(_recid) FROM mt6.feiertag));
\echo Finish Table feiertag 
\echo . 
\echo Loading Table ffont 
\copy mt6.ffont from '/usr1/dump-MT2/CSV/ffont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.ffont__recid_seq', (SELECT MAX(_recid) FROM mt6.ffont));
\echo Finish Table ffont 
\echo . 
\echo Loading Table fixleist 
\copy mt6.fixleist from '/usr1/dump-MT2/CSV/fixleist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.fixleist__recid_seq', (SELECT MAX(_recid) FROM mt6.fixleist));
\echo Finish Table fixleist 
\echo . 
\echo Loading Table gc_giro 
\copy mt6.gc_giro from '/usr1/dump-MT2/CSV/gc-giro.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gc_giro__recid_seq', (SELECT MAX(_recid) FROM mt6.gc_giro));
update mt6.gc_giro set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_giro 
\echo . 
\echo Loading Table gc_jouhdr 
\copy mt6.gc_jouhdr from '/usr1/dump-MT2/CSV/gc-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gc_jouhdr__recid_seq', (SELECT MAX(_recid) FROM mt6.gc_jouhdr));
\echo Finish Table gc_jouhdr 
\echo . 
\echo Loading Table gc_journal 
\copy mt6.gc_journal from '/usr1/dump-MT2/CSV/gc-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gc_journal__recid_seq', (SELECT MAX(_recid) FROM mt6.gc_journal));
\echo Finish Table gc_journal 
\echo . 
\echo Loading Table gc_pi 
\copy mt6.gc_pi from '/usr1/dump-MT2/CSV/gc-PI.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gc_pi__recid_seq', (SELECT MAX(_recid) FROM mt6.gc_pi));
update mt6.gc_pi set bez_array = array_replace(bez_array,NULL,''); 
update mt6.gc_pi set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_pi 
\echo . 
\echo Loading Table gc_piacct 
\copy mt6.gc_piacct from '/usr1/dump-MT2/CSV/gc-piacct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gc_piacct__recid_seq', (SELECT MAX(_recid) FROM mt6.gc_piacct));
\echo Finish Table gc_piacct 
\echo . 
\echo Loading Table gc_pibline 
\copy mt6.gc_pibline from '/usr1/dump-MT2/CSV/gc-PIbline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gc_pibline__recid_seq', (SELECT MAX(_recid) FROM mt6.gc_pibline));
\echo Finish Table gc_pibline 
\echo . 
\echo Loading Table gc_pitype 
\copy mt6.gc_pitype from '/usr1/dump-MT2/CSV/gc-piType.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gc_pitype__recid_seq', (SELECT MAX(_recid) FROM mt6.gc_pitype));
\echo Finish Table gc_pitype 
\echo . 
\echo Loading Table genfcast 
\copy mt6.genfcast from '/usr1/dump-MT2/CSV/genfcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.genfcast__recid_seq', (SELECT MAX(_recid) FROM mt6.genfcast));
update mt6.genfcast set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genfcast 
\echo . 
\echo Loading Table genlayout 
\copy mt6.genlayout from '/usr1/dump-MT2/CSV/genlayout.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.genlayout__recid_seq', (SELECT MAX(_recid) FROM mt6.genlayout));
update mt6.genlayout set button_ext = array_replace(button_ext,NULL,''); 
update mt6.genlayout set char_ext = array_replace(char_ext,NULL,''); 
update mt6.genlayout set combo_ext = array_replace(combo_ext,NULL,''); 
update mt6.genlayout set date_ext = array_replace(date_ext,NULL,''); 
update mt6.genlayout set deci_ext = array_replace(deci_ext,NULL,''); 
update mt6.genlayout set inte_ext = array_replace(inte_ext,NULL,''); 
update mt6.genlayout set logi_ext = array_replace(logi_ext,NULL,''); 
update mt6.genlayout set string_ext = array_replace(string_ext,NULL,''); 
update mt6.genlayout set tchar_ext = array_replace(tchar_ext,NULL,''); 
update mt6.genlayout set tdate_ext = array_replace(tdate_ext,NULL,''); 
update mt6.genlayout set tdeci_ext = array_replace(tdeci_ext,NULL,''); 
update mt6.genlayout set tinte_ext = array_replace(tinte_ext,NULL,''); 
update mt6.genlayout set tlogi_ext = array_replace(tlogi_ext,NULL,''); 
\echo Finish Table genlayout 
\echo . 
\echo Loading Table genstat 
\copy mt6.genstat from '/usr1/dump-MT2/CSV/genstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.genstat__recid_seq', (SELECT MAX(_recid) FROM mt6.genstat));
update mt6.genstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genstat 
\echo . 
\echo Loading Table gentable 
\copy mt6.gentable from '/usr1/dump-MT2/CSV/gentable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gentable__recid_seq', (SELECT MAX(_recid) FROM mt6.gentable));
update mt6.gentable set char_ext = array_replace(char_ext,NULL,''); 
update mt6.gentable set combo_ext = array_replace(combo_ext,NULL,''); 
\echo Finish Table gentable 
\echo . 
\echo Loading Table gk_field 
\copy mt6.gk_field from '/usr1/dump-MT2/CSV/gk-field.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gk_field__recid_seq', (SELECT MAX(_recid) FROM mt6.gk_field));
\echo Finish Table gk_field 
\echo . 
\echo Loading Table gk_label 
\copy mt6.gk_label from '/usr1/dump-MT2/CSV/gk-label.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gk_label__recid_seq', (SELECT MAX(_recid) FROM mt6.gk_label));
\echo Finish Table gk_label 
\echo . 
\echo Loading Table gk_notes 
\copy mt6.gk_notes from '/usr1/dump-MT2/CSV/gk-notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gk_notes__recid_seq', (SELECT MAX(_recid) FROM mt6.gk_notes));
update mt6.gk_notes set notes = array_replace(notes,NULL,''); 
\echo Finish Table gk_notes 
\echo . 
\echo Loading Table gl_acct 
\copy mt6.gl_acct from '/usr1/dump-MT2/CSV/gl-acct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_acct__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_acct));
\echo Finish Table gl_acct 
\echo . 
\echo Loading Table gl_accthis 
\copy mt6.gl_accthis from '/usr1/dump-MT2/CSV/gl-accthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_accthis__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_accthis));
\echo Finish Table gl_accthis 
\echo . 
\echo Loading Table gl_coa 
\copy mt6.gl_coa from '/usr1/dump-MT2/CSV/gl-coa.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_coa__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_coa));
\echo Finish Table gl_coa 
\echo . 
\echo Loading Table gl_cost 
\copy mt6.gl_cost from '/usr1/dump-MT2/CSV/gl-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_cost__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_cost));
\echo Finish Table gl_cost 
\echo . 
\echo Loading Table gl_department 
\copy mt6.gl_department from '/usr1/dump-MT2/CSV/gl-department.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_department__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_department));
\echo Finish Table gl_department 
\echo . 
\echo Loading Table gl_fstype 
\copy mt6.gl_fstype from '/usr1/dump-MT2/CSV/gl-fstype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_fstype__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_fstype));
\echo Finish Table gl_fstype 
\echo . 
\echo Loading Table gl_htljournal 
\copy mt6.gl_htljournal from '/usr1/dump-MT2/CSV/gl-htljournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_htljournal__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_htljournal));
\echo Finish Table gl_htljournal 
\echo . 
\echo Loading Table gl_jhdrhis 
\copy mt6.gl_jhdrhis from '/usr1/dump-MT2/CSV/gl-jhdrhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_jhdrhis__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_jhdrhis));
\echo Finish Table gl_jhdrhis 
\echo . 
\echo Loading Table gl_jouhdr 
\copy mt6.gl_jouhdr from '/usr1/dump-MT2/CSV/gl-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_jouhdr__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_jouhdr));
\echo Finish Table gl_jouhdr 
\echo . 
\echo Loading Table gl_jourhis 
\copy mt6.gl_jourhis from '/usr1/dump-MT2/CSV/gl-jourhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_jourhis__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_jourhis));
\echo Finish Table gl_jourhis 
\echo . 
\echo Loading Table gl_journal 
\copy mt6.gl_journal from '/usr1/dump-MT2/CSV/gl-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_journal__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_journal));
\echo Finish Table gl_journal 
\echo . 
\echo Loading Table gl_main 
\copy mt6.gl_main from '/usr1/dump-MT2/CSV/gl-main.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.gl_main__recid_seq', (SELECT MAX(_recid) FROM mt6.gl_main));
\echo Finish Table gl_main 
\echo . 
\echo Loading Table golf_caddie 
\copy mt6.golf_caddie from '/usr1/dump-MT2/CSV/golf-caddie.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_caddie__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_caddie));
\echo Finish Table golf_caddie 
\echo . 
\echo Loading Table golf_caddie_assignment 
\copy mt6.golf_caddie_assignment from '/usr1/dump-MT2/CSV/golf-caddie-assignment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_caddie_assignment__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_caddie_assignment));
\echo Finish Table golf_caddie_assignment 
\echo . 
\echo Loading Table golf_course 
\copy mt6.golf_course from '/usr1/dump-MT2/CSV/golf-course.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_course__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_course));
\echo Finish Table golf_course 
\echo . 
\echo Loading Table golf_flight_reservation 
\copy mt6.golf_flight_reservation from '/usr1/dump-MT2/CSV/golf-flight-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_flight_reservation__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_flight_reservation));
\echo Finish Table golf_flight_reservation 
\echo . 
\echo Loading Table golf_flight_reservation_hist 
\copy mt6.golf_flight_reservation_hist from '/usr1/dump-MT2/CSV/golf-flight-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_flight_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_flight_reservation_hist));
\echo Finish Table golf_flight_reservation_hist 
\echo . 
\echo Loading Table golf_golfer_reservation 
\copy mt6.golf_golfer_reservation from '/usr1/dump-MT2/CSV/golf-golfer-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_golfer_reservation__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_golfer_reservation));
\echo Finish Table golf_golfer_reservation 
\echo . 
\echo Loading Table golf_golfer_reservation_hist 
\copy mt6.golf_golfer_reservation_hist from '/usr1/dump-MT2/CSV/golf-golfer-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_golfer_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_golfer_reservation_hist));
\echo Finish Table golf_golfer_reservation_hist 
\echo . 
\echo Loading Table golf_holiday 
\copy mt6.golf_holiday from '/usr1/dump-MT2/CSV/golf-holiday.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_holiday__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_holiday));
\echo Finish Table golf_holiday 
\echo . 
\echo Loading Table golf_main_reservation 
\copy mt6.golf_main_reservation from '/usr1/dump-MT2/CSV/golf-main-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_main_reservation__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_main_reservation));
\echo Finish Table golf_main_reservation 
\echo . 
\echo Loading Table golf_main_reservation_hist 
\copy mt6.golf_main_reservation_hist from '/usr1/dump-MT2/CSV/golf-main-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_main_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_main_reservation_hist));
\echo Finish Table golf_main_reservation_hist 
\echo . 
\echo Loading Table golf_rate 
\copy mt6.golf_rate from '/usr1/dump-MT2/CSV/golf-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_rate__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_rate));
\echo Finish Table golf_rate 
\echo . 
\echo Loading Table golf_shift 
\copy mt6.golf_shift from '/usr1/dump-MT2/CSV/golf-shift.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_shift__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_shift));
\echo Finish Table golf_shift 
\echo . 
\echo Loading Table golf_transfer 
\copy mt6.golf_transfer from '/usr1/dump-MT2/CSV/golf-transfer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.golf_transfer__recid_seq', (SELECT MAX(_recid) FROM mt6.golf_transfer));
\echo Finish Table golf_transfer 
\echo . 
\echo Loading Table guest 
\copy mt6.guest from '/usr1/dump-MT2/CSV/guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guest__recid_seq', (SELECT MAX(_recid) FROM mt6.guest));
update mt6.guest set notizen = array_replace(notizen,NULL,''); 
update mt6.guest set vornamekind = array_replace(vornamekind,NULL,''); 
\echo Finish Table guest 
\echo . 
\echo Loading Table guest_pr 
\copy mt6.guest_pr from '/usr1/dump-MT2/CSV/guest-pr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guest_pr__recid_seq', (SELECT MAX(_recid) FROM mt6.guest_pr));
\echo Finish Table guest_pr 
\echo . 
\echo Loading Table guest_queasy 
\copy mt6.guest_queasy from '/usr1/dump-MT2/CSV/guest-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guest_queasy__recid_seq', (SELECT MAX(_recid) FROM mt6.guest_queasy));
\echo Finish Table guest_queasy 
\echo . 
\echo Loading Table guest_remark 
\copy mt6.guest_remark from '/usr1/dump-MT2/CSV/guest-remark.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guest_remark__recid_seq', (SELECT MAX(_recid) FROM mt6.guest_remark));
update mt6.guest_remark set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table guest_remark 
\echo . 
\echo Loading Table guestat 
\copy mt6.guestat from '/usr1/dump-MT2/CSV/guestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guestat__recid_seq', (SELECT MAX(_recid) FROM mt6.guestat));
\echo Finish Table guestat 
\echo . 
\echo Loading Table guestat1 
\copy mt6.guestat1 from '/usr1/dump-MT2/CSV/guestat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guestat1__recid_seq', (SELECT MAX(_recid) FROM mt6.guestat1));
\echo Finish Table guestat1 
\echo . 
\echo Loading Table guestbook 
\copy mt6.guestbook from '/usr1/dump-MT2/CSV/guestbook.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guestbook__recid_seq', (SELECT MAX(_recid) FROM mt6.guestbook));
update mt6.guestbook set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table guestbook 
\echo . 
\echo Loading Table guestbud 
\copy mt6.guestbud from '/usr1/dump-MT2/CSV/guestbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guestbud__recid_seq', (SELECT MAX(_recid) FROM mt6.guestbud));
\echo Finish Table guestbud 
\echo . 
\echo Loading Table guestseg 
\copy mt6.guestseg from '/usr1/dump-MT2/CSV/guestseg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.guestseg__recid_seq', (SELECT MAX(_recid) FROM mt6.guestseg));
\echo Finish Table guestseg 
\echo . 
\echo Loading Table h_artcost 
\copy mt6.h_artcost from '/usr1/dump-MT2/CSV/h-artcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_artcost__recid_seq', (SELECT MAX(_recid) FROM mt6.h_artcost));
\echo Finish Table h_artcost 
\echo . 
\echo Loading Table h_artikel 
\copy mt6.h_artikel from '/usr1/dump-MT2/CSV/h-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_artikel__recid_seq', (SELECT MAX(_recid) FROM mt6.h_artikel));
\echo Finish Table h_artikel 
\echo . 
\echo Loading Table h_bill 
\copy mt6.h_bill from '/usr1/dump-MT2/CSV/h-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_bill__recid_seq', (SELECT MAX(_recid) FROM mt6.h_bill));
\echo Finish Table h_bill 
\echo . 
\echo Loading Table h_bill_line 
\copy mt6.h_bill_line from '/usr1/dump-MT2/CSV/h-bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_bill_line__recid_seq', (SELECT MAX(_recid) FROM mt6.h_bill_line));
\echo Finish Table h_bill_line 
\echo . 
\echo Loading Table h_compli 
\copy mt6.h_compli from '/usr1/dump-MT2/CSV/h-compli.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_compli__recid_seq', (SELECT MAX(_recid) FROM mt6.h_compli));
\echo Finish Table h_compli 
\echo . 
\echo Loading Table h_cost 
\copy mt6.h_cost from '/usr1/dump-MT2/CSV/h-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_cost__recid_seq', (SELECT MAX(_recid) FROM mt6.h_cost));
\echo Finish Table h_cost 
\echo . 
\echo Loading Table h_journal 
\copy mt6.h_journal from '/usr1/dump-MT2/CSV/h-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_journal__recid_seq', (SELECT MAX(_recid) FROM mt6.h_journal));
\echo Finish Table h_journal 
\echo . 
\echo Loading Table h_menu 
\copy mt6.h_menu from '/usr1/dump-MT2/CSV/h-menu.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_menu__recid_seq', (SELECT MAX(_recid) FROM mt6.h_menu));
\echo Finish Table h_menu 
\echo . 
\echo Loading Table h_mjourn 
\copy mt6.h_mjourn from '/usr1/dump-MT2/CSV/h-mjourn.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_mjourn__recid_seq', (SELECT MAX(_recid) FROM mt6.h_mjourn));
\echo Finish Table h_mjourn 
\echo . 
\echo Loading Table h_oldjou 
\copy mt6.h_oldjou from '/usr1/dump-MT2/CSV/h-oldjou.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_oldjou__recid_seq', (SELECT MAX(_recid) FROM mt6.h_oldjou));
\echo Finish Table h_oldjou 
\echo . 
\echo Loading Table h_order 
\copy mt6.h_order from '/usr1/dump-MT2/CSV/h-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_order__recid_seq', (SELECT MAX(_recid) FROM mt6.h_order));
update mt6.h_order set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table h_order 
\echo . 
\echo Loading Table h_queasy 
\copy mt6.h_queasy from '/usr1/dump-MT2/CSV/h-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_queasy__recid_seq', (SELECT MAX(_recid) FROM mt6.h_queasy));
\echo Finish Table h_queasy 
\echo . 
\echo Loading Table h_rezept 
\copy mt6.h_rezept from '/usr1/dump-MT2/CSV/h-rezept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_rezept__recid_seq', (SELECT MAX(_recid) FROM mt6.h_rezept));
\echo Finish Table h_rezept 
\echo . 
\echo Loading Table h_rezlin 
\copy mt6.h_rezlin from '/usr1/dump-MT2/CSV/h-rezlin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_rezlin__recid_seq', (SELECT MAX(_recid) FROM mt6.h_rezlin));
\echo Finish Table h_rezlin 
\echo . 
\echo Loading Table h_storno 
\copy mt6.h_storno from '/usr1/dump-MT2/CSV/h-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_storno__recid_seq', (SELECT MAX(_recid) FROM mt6.h_storno));
\echo Finish Table h_storno 
\echo . 
\echo Loading Table h_umsatz 
\copy mt6.h_umsatz from '/usr1/dump-MT2/CSV/h-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.h_umsatz__recid_seq', (SELECT MAX(_recid) FROM mt6.h_umsatz));
\echo Finish Table h_umsatz 
\echo . 
\echo Loading Table history 
\copy mt6.history from '/usr1/dump-MT2/CSV/history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.history__recid_seq', (SELECT MAX(_recid) FROM mt6.history));
\echo Finish Table history 
\echo . 
\echo Loading Table hoteldpt 
\copy mt6.hoteldpt from '/usr1/dump-MT2/CSV/hoteldpt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.hoteldpt__recid_seq', (SELECT MAX(_recid) FROM mt6.hoteldpt));
\echo Finish Table hoteldpt 
\echo . 
\echo Loading Table hrbeleg 
\copy mt6.hrbeleg from '/usr1/dump-MT2/CSV/hrbeleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.hrbeleg__recid_seq', (SELECT MAX(_recid) FROM mt6.hrbeleg));
\echo Finish Table hrbeleg 
\echo . 
\echo Loading Table hrsegement 
\copy mt6.hrsegement from '/usr1/dump-MT2/CSV/hrsegement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.hrsegement__recid_seq', (SELECT MAX(_recid) FROM mt6.hrsegement));
\echo Finish Table hrsegement 
\echo . 
\echo Loading Table htparam 
\copy mt6.htparam from '/usr1/dump-MT2/CSV/htparam.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.htparam__recid_seq', (SELECT MAX(_recid) FROM mt6.htparam));
\echo Finish Table htparam 
\echo . 
\echo Loading Table htreport 
\copy mt6.htreport from '/usr1/dump-MT2/CSV/htreport.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.htreport__recid_seq', (SELECT MAX(_recid) FROM mt6.htreport));
\echo Finish Table htreport 
\echo . 
\echo Loading Table iftable 
\copy mt6.iftable from '/usr1/dump-MT2/CSV/iftable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.iftable__recid_seq', (SELECT MAX(_recid) FROM mt6.iftable));
\echo Finish Table iftable 
\echo . 
\echo Loading Table interface 
\copy mt6.interface from '/usr1/dump-MT2/CSV/interface.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.interface__recid_seq', (SELECT MAX(_recid) FROM mt6.interface));
\echo Finish Table interface 
\echo . 
\echo Loading Table k_history 
\copy mt6.k_history from '/usr1/dump-MT2/CSV/k-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.k_history__recid_seq', (SELECT MAX(_recid) FROM mt6.k_history));
\echo Finish Table k_history 
\echo . 
\echo Loading Table kabine 
\copy mt6.kabine from '/usr1/dump-MT2/CSV/kabine.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kabine__recid_seq', (SELECT MAX(_recid) FROM mt6.kabine));
\echo Finish Table kabine 
\echo . 
\echo Loading Table kalender 
\copy mt6.kalender from '/usr1/dump-MT2/CSV/kalender.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kalender__recid_seq', (SELECT MAX(_recid) FROM mt6.kalender));
update mt6.kalender set note = array_replace(note,NULL,''); 
\echo Finish Table kalender 
\echo . 
\echo Loading Table kasse 
\copy mt6.kasse from '/usr1/dump-MT2/CSV/kasse.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kasse__recid_seq', (SELECT MAX(_recid) FROM mt6.kasse));
\echo Finish Table kasse 
\echo . 
\echo Loading Table katpreis 
\copy mt6.katpreis from '/usr1/dump-MT2/CSV/katpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.katpreis__recid_seq', (SELECT MAX(_recid) FROM mt6.katpreis));
\echo Finish Table katpreis 
\echo . 
\echo Loading Table kellne1 
\copy mt6.kellne1 from '/usr1/dump-MT2/CSV/kellne1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kellne1__recid_seq', (SELECT MAX(_recid) FROM mt6.kellne1));
\echo Finish Table kellne1 
\echo . 
\echo Loading Table kellner 
\copy mt6.kellner from '/usr1/dump-MT2/CSV/kellner.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kellner__recid_seq', (SELECT MAX(_recid) FROM mt6.kellner));
\echo Finish Table kellner 
\echo . 
\echo Loading Table kontakt 
\copy mt6.kontakt from '/usr1/dump-MT2/CSV/kontakt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kontakt__recid_seq', (SELECT MAX(_recid) FROM mt6.kontakt));
\echo Finish Table kontakt 
\echo . 
\echo Loading Table kontline 
\copy mt6.kontline from '/usr1/dump-MT2/CSV/kontline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kontline__recid_seq', (SELECT MAX(_recid) FROM mt6.kontline));
\echo Finish Table kontline 
\echo . 
\echo Loading Table kontlink 
\copy mt6.kontlink from '/usr1/dump-MT2/CSV/kontlink.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kontlink__recid_seq', (SELECT MAX(_recid) FROM mt6.kontlink));
\echo Finish Table kontlink 
\echo . 
\echo Loading Table kontplan 
\copy mt6.kontplan from '/usr1/dump-MT2/CSV/kontplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kontplan__recid_seq', (SELECT MAX(_recid) FROM mt6.kontplan));
\echo Finish Table kontplan 
\echo . 
\echo Loading Table kontstat 
\copy mt6.kontstat from '/usr1/dump-MT2/CSV/kontstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kontstat__recid_seq', (SELECT MAX(_recid) FROM mt6.kontstat));
update mt6.kontstat set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table kontstat 
\echo . 
\echo Loading Table kresline 
\copy mt6.kresline from '/usr1/dump-MT2/CSV/kresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.kresline__recid_seq', (SELECT MAX(_recid) FROM mt6.kresline));
\echo Finish Table kresline 
\echo . 
\echo Loading Table l_artikel 
\copy mt6.l_artikel from '/usr1/dump-MT2/CSV/l-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_artikel__recid_seq', (SELECT MAX(_recid) FROM mt6.l_artikel));
update mt6.l_artikel set lief_artnr = array_replace(lief_artnr,NULL,''); 
\echo Finish Table l_artikel 
\echo . 
\echo Loading Table l_bestand 
\copy mt6.l_bestand from '/usr1/dump-MT2/CSV/l-bestand.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_bestand__recid_seq', (SELECT MAX(_recid) FROM mt6.l_bestand));
\echo Finish Table l_bestand 
\echo . 
\echo Loading Table l_besthis 
\copy mt6.l_besthis from '/usr1/dump-MT2/CSV/l-besthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_besthis__recid_seq', (SELECT MAX(_recid) FROM mt6.l_besthis));
\echo Finish Table l_besthis 
\echo . 
\echo Loading Table l_hauptgrp 
\copy mt6.l_hauptgrp from '/usr1/dump-MT2/CSV/l-hauptgrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_hauptgrp__recid_seq', (SELECT MAX(_recid) FROM mt6.l_hauptgrp));
\echo Finish Table l_hauptgrp 
\echo . 
\echo Loading Table l_kredit 
\copy mt6.l_kredit from '/usr1/dump-MT2/CSV/l-kredit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_kredit__recid_seq', (SELECT MAX(_recid) FROM mt6.l_kredit));
\echo Finish Table l_kredit 
\echo . 
\echo Loading Table l_lager 
\copy mt6.l_lager from '/usr1/dump-MT2/CSV/l-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_lager__recid_seq', (SELECT MAX(_recid) FROM mt6.l_lager));
\echo Finish Table l_lager 
\echo . 
\echo Loading Table l_lieferant 
\copy mt6.l_lieferant from '/usr1/dump-MT2/CSV/l-lieferant.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_lieferant__recid_seq', (SELECT MAX(_recid) FROM mt6.l_lieferant));
update mt6.l_lieferant set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table l_lieferant 
\echo . 
\echo Loading Table l_liefumsatz 
\copy mt6.l_liefumsatz from '/usr1/dump-MT2/CSV/l-liefumsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_liefumsatz__recid_seq', (SELECT MAX(_recid) FROM mt6.l_liefumsatz));
\echo Finish Table l_liefumsatz 
\echo . 
\echo Loading Table l_op 
\copy mt6.l_op from '/usr1/dump-MT2/CSV/l-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_op__recid_seq', (SELECT MAX(_recid) FROM mt6.l_op));
\echo Finish Table l_op 
\echo . 
\echo Loading Table l_ophdr 
\copy mt6.l_ophdr from '/usr1/dump-MT2/CSV/l-ophdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_ophdr__recid_seq', (SELECT MAX(_recid) FROM mt6.l_ophdr));
\echo Finish Table l_ophdr 
\echo . 
\echo Loading Table l_ophhis 
\copy mt6.l_ophhis from '/usr1/dump-MT2/CSV/l-ophhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_ophhis__recid_seq', (SELECT MAX(_recid) FROM mt6.l_ophhis));
\echo Finish Table l_ophhis 
\echo . 
\echo Loading Table l_ophis 
\copy mt6.l_ophis from '/usr1/dump-MT2/CSV/l-ophis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_ophis__recid_seq', (SELECT MAX(_recid) FROM mt6.l_ophis));
\echo Finish Table l_ophis 
\echo . 
\echo Loading Table l_order 
\copy mt6.l_order from '/usr1/dump-MT2/CSV/l-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_order__recid_seq', (SELECT MAX(_recid) FROM mt6.l_order));
update mt6.l_order set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_order 
\echo . 
\echo Loading Table l_orderhdr 
\copy mt6.l_orderhdr from '/usr1/dump-MT2/CSV/l-orderhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_orderhdr__recid_seq', (SELECT MAX(_recid) FROM mt6.l_orderhdr));
update mt6.l_orderhdr set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_orderhdr 
\echo . 
\echo Loading Table l_pprice 
\copy mt6.l_pprice from '/usr1/dump-MT2/CSV/l-pprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_pprice__recid_seq', (SELECT MAX(_recid) FROM mt6.l_pprice));
\echo Finish Table l_pprice 
\echo . 
\echo Loading Table l_quote 
\copy mt6.l_quote from '/usr1/dump-MT2/CSV/l-quote.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_quote__recid_seq', (SELECT MAX(_recid) FROM mt6.l_quote));
update mt6.l_quote set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table l_quote 
\echo . 
\echo Loading Table l_segment 
\copy mt6.l_segment from '/usr1/dump-MT2/CSV/l-segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_segment__recid_seq', (SELECT MAX(_recid) FROM mt6.l_segment));
\echo Finish Table l_segment 
\echo . 
\echo Loading Table l_umsatz 
\copy mt6.l_umsatz from '/usr1/dump-MT2/CSV/l-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_umsatz__recid_seq', (SELECT MAX(_recid) FROM mt6.l_umsatz));
\echo Finish Table l_umsatz 
\echo . 
\echo Loading Table l_untergrup 
\copy mt6.l_untergrup from '/usr1/dump-MT2/CSV/l-untergrup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_untergrup__recid_seq', (SELECT MAX(_recid) FROM mt6.l_untergrup));
\echo Finish Table l_untergrup 
\echo . 
\echo Loading Table l_verbrauch 
\copy mt6.l_verbrauch from '/usr1/dump-MT2/CSV/l-verbrauch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_verbrauch__recid_seq', (SELECT MAX(_recid) FROM mt6.l_verbrauch));
\echo Finish Table l_verbrauch 
\echo . 
\echo Loading Table l_zahlbed 
\copy mt6.l_zahlbed from '/usr1/dump-MT2/CSV/l-zahlbed.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.l_zahlbed__recid_seq', (SELECT MAX(_recid) FROM mt6.l_zahlbed));
\echo Finish Table l_zahlbed 
\echo . 
\echo Loading Table landstat 
\copy mt6.landstat from '/usr1/dump-MT2/CSV/landstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.landstat__recid_seq', (SELECT MAX(_recid) FROM mt6.landstat));
\echo Finish Table landstat 
\echo . 
\echo Loading Table masseur 
\copy mt6.masseur from '/usr1/dump-MT2/CSV/masseur.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.masseur__recid_seq', (SELECT MAX(_recid) FROM mt6.masseur));
\echo Finish Table masseur 
\echo . 
\echo Loading Table mast_art 
\copy mt6.mast_art from '/usr1/dump-MT2/CSV/mast-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mast_art__recid_seq', (SELECT MAX(_recid) FROM mt6.mast_art));
\echo Finish Table mast_art 
\echo . 
\echo Loading Table master 
\copy mt6.master from '/usr1/dump-MT2/CSV/master.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.master__recid_seq', (SELECT MAX(_recid) FROM mt6.master));
\echo Finish Table master 
\echo . 
\echo Loading Table mathis 
\copy mt6.mathis from '/usr1/dump-MT2/CSV/mathis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mathis__recid_seq', (SELECT MAX(_recid) FROM mt6.mathis));
\echo Finish Table mathis 
\echo . 
\echo Loading Table mc_aclub 
\copy mt6.mc_aclub from '/usr1/dump-MT2/CSV/mc-aclub.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mc_aclub__recid_seq', (SELECT MAX(_recid) FROM mt6.mc_aclub));
\echo Finish Table mc_aclub 
\echo . 
\echo Loading Table mc_cardhis 
\copy mt6.mc_cardhis from '/usr1/dump-MT2/CSV/mc-cardhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mc_cardhis__recid_seq', (SELECT MAX(_recid) FROM mt6.mc_cardhis));
\echo Finish Table mc_cardhis 
\echo . 
\echo Loading Table mc_disc 
\copy mt6.mc_disc from '/usr1/dump-MT2/CSV/mc-disc.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mc_disc__recid_seq', (SELECT MAX(_recid) FROM mt6.mc_disc));
\echo Finish Table mc_disc 
\echo . 
\echo Loading Table mc_fee 
\copy mt6.mc_fee from '/usr1/dump-MT2/CSV/mc-fee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mc_fee__recid_seq', (SELECT MAX(_recid) FROM mt6.mc_fee));
\echo Finish Table mc_fee 
\echo . 
\echo Loading Table mc_guest 
\copy mt6.mc_guest from '/usr1/dump-MT2/CSV/mc-guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mc_guest__recid_seq', (SELECT MAX(_recid) FROM mt6.mc_guest));
\echo Finish Table mc_guest 
\echo . 
\echo Loading Table mc_types 
\copy mt6.mc_types from '/usr1/dump-MT2/CSV/mc-types.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mc_types__recid_seq', (SELECT MAX(_recid) FROM mt6.mc_types));
\echo Finish Table mc_types 
\echo . 
\echo Loading Table mealcoup 
\copy mt6.mealcoup from '/usr1/dump-MT2/CSV/mealcoup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mealcoup__recid_seq', (SELECT MAX(_recid) FROM mt6.mealcoup));
\echo Finish Table mealcoup 
\echo . 
\echo Loading Table messages 
\copy mt6.messages from '/usr1/dump-MT2/CSV/messages.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.messages__recid_seq', (SELECT MAX(_recid) FROM mt6.messages));
update mt6.messages set messtext = array_replace(messtext,NULL,''); 
\echo Finish Table messages 
\echo . 
\echo Loading Table messe 
\copy mt6.messe from '/usr1/dump-MT2/CSV/messe.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.messe__recid_seq', (SELECT MAX(_recid) FROM mt6.messe));
\echo Finish Table messe 
\echo . 
\echo Loading Table mhis_line 
\copy mt6.mhis_line from '/usr1/dump-MT2/CSV/mhis-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.mhis_line__recid_seq', (SELECT MAX(_recid) FROM mt6.mhis_line));
\echo Finish Table mhis_line 
\echo . 
\echo Loading Table nation 
\copy mt6.nation from '/usr1/dump-MT2/CSV/nation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.nation__recid_seq', (SELECT MAX(_recid) FROM mt6.nation));
\echo Finish Table nation 
\echo . 
\echo Loading Table nationstat 
\copy mt6.nationstat from '/usr1/dump-MT2/CSV/nationstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.nationstat__recid_seq', (SELECT MAX(_recid) FROM mt6.nationstat));
\echo Finish Table nationstat 
\echo . 
\echo Loading Table natstat1 
\copy mt6.natstat1 from '/usr1/dump-MT2/CSV/natstat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.natstat1__recid_seq', (SELECT MAX(_recid) FROM mt6.natstat1));
\echo Finish Table natstat1 
\echo . 
\echo Loading Table nebenst 
\copy mt6.nebenst from '/usr1/dump-MT2/CSV/nebenst.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.nebenst__recid_seq', (SELECT MAX(_recid) FROM mt6.nebenst));
\echo Finish Table nebenst 
\echo . 
\echo Loading Table nightaudit 
\copy mt6.nightaudit from '/usr1/dump-MT2/CSV/nightaudit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.nightaudit__recid_seq', (SELECT MAX(_recid) FROM mt6.nightaudit));
\echo Finish Table nightaudit 
\echo . 
\echo Loading Table nitehist 
\copy mt6.nitehist from '/usr1/dump-MT2/CSV/nitehist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.nitehist__recid_seq', (SELECT MAX(_recid) FROM mt6.nitehist));
\echo Finish Table nitehist 
\echo . 
\echo Loading Table nitestor 
\copy mt6.nitestor from '/usr1/dump-MT2/CSV/nitestor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.nitestor__recid_seq', (SELECT MAX(_recid) FROM mt6.nitestor));
\echo Finish Table nitestor 
\echo . 
\echo Loading Table notes 
\copy mt6.notes from '/usr1/dump-MT2/CSV/notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.notes__recid_seq', (SELECT MAX(_recid) FROM mt6.notes));
update mt6.notes set note = array_replace(note,NULL,''); 
\echo Finish Table notes 
\echo . 
\echo Loading Table outorder 
\copy mt6.outorder from '/usr1/dump-MT2/CSV/outorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.outorder__recid_seq', (SELECT MAX(_recid) FROM mt6.outorder));
\echo Finish Table outorder 
\echo . 
\echo Loading Table package 
\copy mt6.package from '/usr1/dump-MT2/CSV/package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.package__recid_seq', (SELECT MAX(_recid) FROM mt6.package));
\echo Finish Table package 
\echo . 
\echo Loading Table parameters 
\copy mt6.parameters from '/usr1/dump-MT2/CSV/parameters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.parameters__recid_seq', (SELECT MAX(_recid) FROM mt6.parameters));
\echo Finish Table parameters 
\echo . 
\echo Loading Table paramtext 
\copy mt6.paramtext from '/usr1/dump-MT2/CSV/paramtext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.paramtext__recid_seq', (SELECT MAX(_recid) FROM mt6.paramtext));
\echo Finish Table paramtext 
\echo . 
\echo Loading Table pricecod 
\copy mt6.pricecod from '/usr1/dump-MT2/CSV/pricecod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.pricecod__recid_seq', (SELECT MAX(_recid) FROM mt6.pricecod));
\echo Finish Table pricecod 
\echo . 
\echo Loading Table pricegrp 
\copy mt6.pricegrp from '/usr1/dump-MT2/CSV/pricegrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.pricegrp__recid_seq', (SELECT MAX(_recid) FROM mt6.pricegrp));
\echo Finish Table pricegrp 
\echo . 
\echo Loading Table printcod 
\copy mt6.printcod from '/usr1/dump-MT2/CSV/printcod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.printcod__recid_seq', (SELECT MAX(_recid) FROM mt6.printcod));
\echo Finish Table printcod 
\echo . 
\echo Loading Table printer 
\copy mt6.printer from '/usr1/dump-MT2/CSV/printer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.printer__recid_seq', (SELECT MAX(_recid) FROM mt6.printer));
\echo Finish Table printer 
\echo . 
\echo Loading Table prmarket 
\copy mt6.prmarket from '/usr1/dump-MT2/CSV/prmarket.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.prmarket__recid_seq', (SELECT MAX(_recid) FROM mt6.prmarket));
\echo Finish Table prmarket 
\echo . 
\echo Loading Table progcat 
\copy mt6.progcat from '/usr1/dump-MT2/CSV/progcat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.progcat__recid_seq', (SELECT MAX(_recid) FROM mt6.progcat));
\echo Finish Table progcat 
\echo . 
\echo Loading Table progfile 
\copy mt6.progfile from '/usr1/dump-MT2/CSV/progfile.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.progfile__recid_seq', (SELECT MAX(_recid) FROM mt6.progfile));
\echo Finish Table progfile 
\echo . 
\echo Loading Table prtable 
\copy mt6.prtable from '/usr1/dump-MT2/CSV/prtable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.prtable__recid_seq', (SELECT MAX(_recid) FROM mt6.prtable));
\echo Finish Table prtable 
\echo . 
\echo Loading Table queasy 
\copy mt6.queasy from '/usr1/dump-MT2/CSV/queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.queasy__recid_seq', (SELECT MAX(_recid) FROM mt6.queasy));
\echo Finish Table queasy 
\echo . 
\echo Loading Table ratecode 
\copy mt6.ratecode from '/usr1/dump-MT2/CSV/ratecode.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.ratecode__recid_seq', (SELECT MAX(_recid) FROM mt6.ratecode));
update mt6.ratecode set char1 = array_replace(char1,NULL,''); 
\echo Finish Table ratecode 
\echo . 
\echo Loading Table raum 
\copy mt6.raum from '/usr1/dump-MT2/CSV/raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.raum__recid_seq', (SELECT MAX(_recid) FROM mt6.raum));
\echo Finish Table raum 
\echo . 
\echo Loading Table res_history 
\copy mt6.res_history from '/usr1/dump-MT2/CSV/res-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.res_history__recid_seq', (SELECT MAX(_recid) FROM mt6.res_history));
\echo Finish Table res_history 
\echo . 
\echo Loading Table res_line 
\copy mt6.res_line from '/usr1/dump-MT2/CSV/res-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.res_line__recid_seq', (SELECT MAX(_recid) FROM mt6.res_line));
\echo Finish Table res_line 
\echo . 
\echo Loading Table reservation 
\copy mt6.reservation from '/usr1/dump-MT2/CSV/reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.reservation__recid_seq', (SELECT MAX(_recid) FROM mt6.reservation));
\echo Finish Table reservation 
\echo . 
\echo Loading Table reslin_queasy 
\copy mt6.reslin_queasy from '/usr1/dump-MT2/CSV/reslin-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.reslin_queasy__recid_seq', (SELECT MAX(_recid) FROM mt6.reslin_queasy));
\echo Finish Table reslin_queasy 
\echo . 
\echo Loading Table resplan 
\copy mt6.resplan from '/usr1/dump-MT2/CSV/resplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.resplan__recid_seq', (SELECT MAX(_recid) FROM mt6.resplan));
\echo Finish Table resplan 
\echo . 
\echo Loading Table rg_reports 
\copy mt6.rg_reports from '/usr1/dump-MT2/CSV/rg-reports.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.rg_reports__recid_seq', (SELECT MAX(_recid) FROM mt6.rg_reports));
update mt6.rg_reports set metadata = array_replace(metadata,NULL,''); 
update mt6.rg_reports set slice_name = array_replace(slice_name,NULL,''); 
update mt6.rg_reports set view_name = array_replace(view_name,NULL,''); 
\echo Finish Table rg_reports 
\echo . 
\echo Loading Table rmbudget 
\copy mt6.rmbudget from '/usr1/dump-MT2/CSV/rmbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.rmbudget__recid_seq', (SELECT MAX(_recid) FROM mt6.rmbudget));
update mt6.rmbudget set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table rmbudget 
\echo . 
\echo Loading Table sales 
\copy mt6.sales from '/usr1/dump-MT2/CSV/sales.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sales__recid_seq', (SELECT MAX(_recid) FROM mt6.sales));
\echo Finish Table sales 
\echo . 
\echo Loading Table salesbud 
\copy mt6.salesbud from '/usr1/dump-MT2/CSV/salesbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.salesbud__recid_seq', (SELECT MAX(_recid) FROM mt6.salesbud));
\echo Finish Table salesbud 
\echo . 
\echo Loading Table salestat 
\copy mt6.salestat from '/usr1/dump-MT2/CSV/salestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.salestat__recid_seq', (SELECT MAX(_recid) FROM mt6.salestat));
\echo Finish Table salestat 
\echo . 
\echo Loading Table salestim 
\copy mt6.salestim from '/usr1/dump-MT2/CSV/salestim.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.salestim__recid_seq', (SELECT MAX(_recid) FROM mt6.salestim));
\echo Finish Table salestim 
\echo . 
\echo Loading Table segment 
\copy mt6.segment from '/usr1/dump-MT2/CSV/segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.segment__recid_seq', (SELECT MAX(_recid) FROM mt6.segment));
\echo Finish Table segment 
\echo . 
\echo Loading Table segmentstat 
\copy mt6.segmentstat from '/usr1/dump-MT2/CSV/segmentstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.segmentstat__recid_seq', (SELECT MAX(_recid) FROM mt6.segmentstat));
\echo Finish Table segmentstat 
\echo . 
\echo Loading Table sms_bcaster 
\copy mt6.sms_bcaster from '/usr1/dump-MT2/CSV/sms-bcaster.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sms_bcaster__recid_seq', (SELECT MAX(_recid) FROM mt6.sms_bcaster));
\echo Finish Table sms_bcaster 
\echo . 
\echo Loading Table sms_broadcast 
\copy mt6.sms_broadcast from '/usr1/dump-MT2/CSV/sms-broadcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sms_broadcast__recid_seq', (SELECT MAX(_recid) FROM mt6.sms_broadcast));
\echo Finish Table sms_broadcast 
\echo . 
\echo Loading Table sms_group 
\copy mt6.sms_group from '/usr1/dump-MT2/CSV/sms-group.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sms_group__recid_seq', (SELECT MAX(_recid) FROM mt6.sms_group));
\echo Finish Table sms_group 
\echo . 
\echo Loading Table sms_groupmbr 
\copy mt6.sms_groupmbr from '/usr1/dump-MT2/CSV/sms-groupmbr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sms_groupmbr__recid_seq', (SELECT MAX(_recid) FROM mt6.sms_groupmbr));
\echo Finish Table sms_groupmbr 
\echo . 
\echo Loading Table sms_received 
\copy mt6.sms_received from '/usr1/dump-MT2/CSV/sms-received.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sms_received__recid_seq', (SELECT MAX(_recid) FROM mt6.sms_received));
\echo Finish Table sms_received 
\echo . 
\echo Loading Table sourccod 
\copy mt6.sourccod from '/usr1/dump-MT2/CSV/Sourccod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sourccod__recid_seq', (SELECT MAX(_recid) FROM mt6.sourccod));
\echo Finish Table sourccod 
\echo . 
\echo Loading Table sources 
\copy mt6.sources from '/usr1/dump-MT2/CSV/sources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sources__recid_seq', (SELECT MAX(_recid) FROM mt6.sources));
\echo Finish Table sources 
\echo . 
\echo Loading Table sourcetext 
\copy mt6.sourcetext from '/usr1/dump-MT2/CSV/sourcetext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.sourcetext__recid_seq', (SELECT MAX(_recid) FROM mt6.sourcetext));
\echo Finish Table sourcetext 
\echo . 
\echo Loading Table telephone 
\copy mt6.telephone from '/usr1/dump-MT2/CSV/telephone.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.telephone__recid_seq', (SELECT MAX(_recid) FROM mt6.telephone));
\echo Finish Table telephone 
\echo . 
\echo Loading Table texte 
\copy mt6.texte from '/usr1/dump-MT2/CSV/texte.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.texte__recid_seq', (SELECT MAX(_recid) FROM mt6.texte));
\echo Finish Table texte 
\echo . 
\echo Loading Table tisch 
\copy mt6.tisch from '/usr1/dump-MT2/CSV/tisch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.tisch__recid_seq', (SELECT MAX(_recid) FROM mt6.tisch));
\echo Finish Table tisch 
\echo . 
\echo Loading Table tisch_res 
\copy mt6.tisch_res from '/usr1/dump-MT2/CSV/tisch-res.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.tisch_res__recid_seq', (SELECT MAX(_recid) FROM mt6.tisch_res));
\echo Finish Table tisch_res 
\echo . 
\echo Loading Table uebertrag 
\copy mt6.uebertrag from '/usr1/dump-MT2/CSV/uebertrag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.uebertrag__recid_seq', (SELECT MAX(_recid) FROM mt6.uebertrag));
\echo Finish Table uebertrag 
\echo . 
\echo Loading Table umsatz 
\copy mt6.umsatz from '/usr1/dump-MT2/CSV/umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.umsatz__recid_seq', (SELECT MAX(_recid) FROM mt6.umsatz));
\echo Finish Table umsatz 
\echo . 
\echo Loading Table waehrung 
\copy mt6.waehrung from '/usr1/dump-MT2/CSV/waehrung.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.waehrung__recid_seq', (SELECT MAX(_recid) FROM mt6.waehrung));
\echo Finish Table waehrung 
\echo . 
\echo Loading Table wakeup 
\copy mt6.wakeup from '/usr1/dump-MT2/CSV/wakeup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.wakeup__recid_seq', (SELECT MAX(_recid) FROM mt6.wakeup));
\echo Finish Table wakeup 
\echo . 
\echo Loading Table wgrpdep 
\copy mt6.wgrpdep from '/usr1/dump-MT2/CSV/wgrpdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.wgrpdep__recid_seq', (SELECT MAX(_recid) FROM mt6.wgrpdep));
\echo Finish Table wgrpdep 
\echo . 
\echo Loading Table wgrpgen 
\copy mt6.wgrpgen from '/usr1/dump-MT2/CSV/wgrpgen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.wgrpgen__recid_seq', (SELECT MAX(_recid) FROM mt6.wgrpgen));
\echo Finish Table wgrpgen 
\echo . 
\echo Loading Table zimkateg 
\copy mt6.zimkateg from '/usr1/dump-MT2/CSV/zimkateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zimkateg__recid_seq', (SELECT MAX(_recid) FROM mt6.zimkateg));
\echo Finish Table zimkateg 
\echo . 
\echo Loading Table zimmer 
\copy mt6.zimmer from '/usr1/dump-MT2/CSV/zimmer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zimmer__recid_seq', (SELECT MAX(_recid) FROM mt6.zimmer));
update mt6.zimmer set verbindung = array_replace(verbindung,NULL,''); 
\echo Finish Table zimmer 
\echo . 
\echo Loading Table zimmer_book 
\copy mt6.zimmer_book from '/usr1/dump-MT2/CSV/zimmer-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zimmer_book__recid_seq', (SELECT MAX(_recid) FROM mt6.zimmer_book));
\echo Finish Table zimmer_book 
\echo . 
\echo Loading Table zimmer_book_line 
\copy mt6.zimmer_book_line from '/usr1/dump-MT2/CSV/zimmer-book-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zimmer_book_line__recid_seq', (SELECT MAX(_recid) FROM mt6.zimmer_book_line));
\echo Finish Table zimmer_book_line 
\echo . 
\echo Loading Table zimplan 
\copy mt6.zimplan from '/usr1/dump-MT2/CSV/zimplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zimplan__recid_seq', (SELECT MAX(_recid) FROM mt6.zimplan));
\echo Finish Table zimplan 
\echo . 
\echo Loading Table zimpreis 
\copy mt6.zimpreis from '/usr1/dump-MT2/CSV/zimpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zimpreis__recid_seq', (SELECT MAX(_recid) FROM mt6.zimpreis));
\echo Finish Table zimpreis 
\echo . 
\echo Loading Table zinrstat 
\copy mt6.zinrstat from '/usr1/dump-MT2/CSV/zinrstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zinrstat__recid_seq', (SELECT MAX(_recid) FROM mt6.zinrstat));
\echo Finish Table zinrstat 
\echo . 
\echo Loading Table zkstat 
\copy mt6.zkstat from '/usr1/dump-MT2/CSV/zkstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zkstat__recid_seq', (SELECT MAX(_recid) FROM mt6.zkstat));
\echo Finish Table zkstat 
\echo . 
\echo Loading Table zwkum 
\copy mt6.zwkum from '/usr1/dump-MT2/CSV/zwkum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt6.zwkum__recid_seq', (SELECT MAX(_recid) FROM mt6.zwkum));
\echo Finish Table zwkum 
\echo . 
