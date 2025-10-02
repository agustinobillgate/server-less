\echo Loading Table absen 
\copy mt5.absen from '/usr1/dump-MT5/absen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.absen__recid_seq', (SELECT MAX(_recid) FROM mt5.absen));
\echo Finish Table absen 
\echo . 
\echo Loading Table akt_code 
\copy mt5.akt_code from '/usr1/dump-MT5/akt-code.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.akt_code__recid_seq', (SELECT MAX(_recid) FROM mt5.akt_code));
\echo Finish Table akt_code 
\echo . 
\echo Loading Table akt_cust 
\copy mt5.akt_cust from '/usr1/dump-MT5/akt-cust.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.akt_cust__recid_seq', (SELECT MAX(_recid) FROM mt5.akt_cust));
\echo Finish Table akt_cust 
\echo . 
\echo Loading Table akt_kont 
\copy mt5.akt_kont from '/usr1/dump-MT5/akt-kont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.akt_kont__recid_seq', (SELECT MAX(_recid) FROM mt5.akt_kont));
\echo Finish Table akt_kont 
\echo . 
\echo Loading Table akt_line 
\copy mt5.akt_line from '/usr1/dump-MT5/akt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.akt_line__recid_seq', (SELECT MAX(_recid) FROM mt5.akt_line));
\echo Finish Table akt_line 
\echo . 
\echo Loading Table akthdr 
\copy mt5.akthdr from '/usr1/dump-MT5/akthdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.akthdr__recid_seq', (SELECT MAX(_recid) FROM mt5.akthdr));
\echo Finish Table akthdr 
\echo . 
\echo Loading Table aktion 
\copy mt5.aktion from '/usr1/dump-MT5/aktion.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.aktion__recid_seq', (SELECT MAX(_recid) FROM mt5.aktion));
update mt5.aktion set texte = array_replace(texte,NULL,''); 
\echo Finish Table aktion 
\echo . 
\echo Loading Table ap_journal 
\copy mt5.ap_journal from '/usr1/dump-MT5/ap-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.ap_journal__recid_seq', (SELECT MAX(_recid) FROM mt5.ap_journal));
\echo Finish Table ap_journal 
\echo . 
\echo Loading Table apt_bill 
\copy mt5.apt_bill from '/usr1/dump-MT5/apt-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.apt_bill__recid_seq', (SELECT MAX(_recid) FROM mt5.apt_bill));
update mt5.apt_bill set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table apt_bill 
\echo . 
\echo Loading Table archieve 
\copy mt5.archieve from '/usr1/dump-MT5/archieve.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.archieve__recid_seq', (SELECT MAX(_recid) FROM mt5.archieve));
update mt5.archieve set char = array_replace(char,NULL,''); 
\echo Finish Table archieve 
\echo . 
\echo Loading Table argt_line 
\copy mt5.argt_line from '/usr1/dump-MT5/argt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.argt_line__recid_seq', (SELECT MAX(_recid) FROM mt5.argt_line));
\echo Finish Table argt_line 
\echo . 
\echo Loading Table argtcost 
\copy mt5.argtcost from '/usr1/dump-MT5/argtcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.argtcost__recid_seq', (SELECT MAX(_recid) FROM mt5.argtcost));
update mt5.argtcost set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtcost 
\echo . 
\echo Loading Table argtstat 
\copy mt5.argtstat from '/usr1/dump-MT5/argtstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.argtstat__recid_seq', (SELECT MAX(_recid) FROM mt5.argtstat));
update mt5.argtstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtstat 
\echo . 
\echo Loading Table arrangement 
\copy mt5.arrangement from '/usr1/dump-MT5/arrangement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.arrangement__recid_seq', (SELECT MAX(_recid) FROM mt5.arrangement));
update mt5.arrangement set argt_rgbez2 = array_replace(argt_rgbez2,NULL,''); 
\echo Finish Table arrangement 
\echo . 
\echo Loading Table artikel 
\copy mt5.artikel from '/usr1/dump-MT5/artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.artikel__recid_seq', (SELECT MAX(_recid) FROM mt5.artikel));
\echo Finish Table artikel 
\echo . 
\echo Loading Table artprice 
\copy mt5.artprice from '/usr1/dump-MT5/artprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.artprice__recid_seq', (SELECT MAX(_recid) FROM mt5.artprice));
\echo Finish Table artprice 
\echo . 
\echo Loading Table b_history 
\copy mt5.b_history from '/usr1/dump-MT5/b-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.b_history__recid_seq', (SELECT MAX(_recid) FROM mt5.b_history));
update mt5.b_history set anlass = array_replace(anlass,NULL,''); 
update mt5.b_history set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update mt5.b_history set ape__speisen = array_replace(ape__speisen,NULL,''); 
update mt5.b_history set arrival = array_replace(arrival,NULL,''); 
update mt5.b_history set c_resstatus = array_replace(c_resstatus,NULL,''); 
update mt5.b_history set dance = array_replace(dance,NULL,''); 
update mt5.b_history set deko2 = array_replace(deko2,NULL,''); 
update mt5.b_history set dekoration = array_replace(dekoration,NULL,''); 
update mt5.b_history set digestif = array_replace(digestif,NULL,''); 
update mt5.b_history set dinner = array_replace(dinner,NULL,''); 
update mt5.b_history set f_menu = array_replace(f_menu,NULL,''); 
update mt5.b_history set f_no = array_replace(f_no,NULL,''); 
update mt5.b_history set fotograf = array_replace(fotograf,NULL,''); 
update mt5.b_history set gaestebuch = array_replace(gaestebuch,NULL,''); 
update mt5.b_history set garderobe = array_replace(garderobe,NULL,''); 
update mt5.b_history set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update mt5.b_history set kaffee = array_replace(kaffee,NULL,''); 
update mt5.b_history set kartentext = array_replace(kartentext,NULL,''); 
update mt5.b_history set kontaktperson = array_replace(kontaktperson,NULL,''); 
update mt5.b_history set kuenstler = array_replace(kuenstler,NULL,''); 
update mt5.b_history set menue = array_replace(menue,NULL,''); 
update mt5.b_history set menuekarten = array_replace(menuekarten,NULL,''); 
update mt5.b_history set musik = array_replace(musik,NULL,''); 
update mt5.b_history set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update mt5.b_history set nadkarte = array_replace(nadkarte,NULL,''); 
update mt5.b_history set ndessen = array_replace(ndessen,NULL,''); 
update mt5.b_history set payment_userinit = array_replace(payment_userinit,NULL,''); 
update mt5.b_history set personen2 = array_replace(personen2,NULL,''); 
update mt5.b_history set raeume = array_replace(raeume,NULL,''); 
update mt5.b_history set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update mt5.b_history set raummiete = array_replace(raummiete,NULL,''); 
update mt5.b_history set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update mt5.b_history set service = array_replace(service,NULL,''); 
update mt5.b_history set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update mt5.b_history set sonstiges = array_replace(sonstiges,NULL,''); 
update mt5.b_history set technik = array_replace(technik,NULL,''); 
update mt5.b_history set tischform = array_replace(tischform,NULL,''); 
update mt5.b_history set tischordnung = array_replace(tischordnung,NULL,''); 
update mt5.b_history set tischplan = array_replace(tischplan,NULL,''); 
update mt5.b_history set tischreden = array_replace(tischreden,NULL,''); 
update mt5.b_history set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update mt5.b_history set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update mt5.b_history set va_ablauf = array_replace(va_ablauf,NULL,''); 
update mt5.b_history set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update mt5.b_history set vip = array_replace(vip,NULL,''); 
update mt5.b_history set weine = array_replace(weine,NULL,''); 
update mt5.b_history set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table b_history 
\echo . 
\echo Loading Table b_oorder 
\copy mt5.b_oorder from '/usr1/dump-MT5/b-oorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.b_oorder__recid_seq', (SELECT MAX(_recid) FROM mt5.b_oorder));
\echo Finish Table b_oorder 
\echo . 
\echo Loading Table b_storno 
\copy mt5.b_storno from '/usr1/dump-MT5/b-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.b_storno__recid_seq', (SELECT MAX(_recid) FROM mt5.b_storno));
update mt5.b_storno set grund = array_replace(grund,NULL,''); 
\echo Finish Table b_storno 
\echo . 
\echo Loading Table ba_rset 
\copy mt5.ba_rset from '/usr1/dump-MT5/ba-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.ba_rset__recid_seq', (SELECT MAX(_recid) FROM mt5.ba_rset));
\echo Finish Table ba_rset 
\echo . 
\echo Loading Table ba_setup 
\copy mt5.ba_setup from '/usr1/dump-MT5/ba-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.ba_setup__recid_seq', (SELECT MAX(_recid) FROM mt5.ba_setup));
\echo Finish Table ba_setup 
\echo . 
\echo Loading Table ba_typ 
\copy mt5.ba_typ from '/usr1/dump-MT5/ba-typ.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.ba_typ__recid_seq', (SELECT MAX(_recid) FROM mt5.ba_typ));
\echo Finish Table ba_typ 
\echo . 
\echo Loading Table bankrep 
\copy mt5.bankrep from '/usr1/dump-MT5/bankrep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bankrep__recid_seq', (SELECT MAX(_recid) FROM mt5.bankrep));
update mt5.bankrep set anlass = array_replace(anlass,NULL,''); 
update mt5.bankrep set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update mt5.bankrep set ape__speisen = array_replace(ape__speisen,NULL,''); 
update mt5.bankrep set dekoration = array_replace(dekoration,NULL,''); 
update mt5.bankrep set digestif = array_replace(digestif,NULL,''); 
update mt5.bankrep set fotograf = array_replace(fotograf,NULL,''); 
update mt5.bankrep set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update mt5.bankrep set kartentext = array_replace(kartentext,NULL,''); 
update mt5.bankrep set kontaktperson = array_replace(kontaktperson,NULL,''); 
update mt5.bankrep set menue = array_replace(menue,NULL,''); 
update mt5.bankrep set menuekarten = array_replace(menuekarten,NULL,''); 
update mt5.bankrep set musik = array_replace(musik,NULL,''); 
update mt5.bankrep set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update mt5.bankrep set ndessen = array_replace(ndessen,NULL,''); 
update mt5.bankrep set personen2 = array_replace(personen2,NULL,''); 
update mt5.bankrep set raeume = array_replace(raeume,NULL,''); 
update mt5.bankrep set raummiete = array_replace(raummiete,NULL,''); 
update mt5.bankrep set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update mt5.bankrep set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update mt5.bankrep set sonstiges = array_replace(sonstiges,NULL,''); 
update mt5.bankrep set technik = array_replace(technik,NULL,''); 
update mt5.bankrep set tischform = array_replace(tischform,NULL,''); 
update mt5.bankrep set tischreden = array_replace(tischreden,NULL,''); 
update mt5.bankrep set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update mt5.bankrep set weine = array_replace(weine,NULL,''); 
update mt5.bankrep set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bankrep 
\echo . 
\echo Loading Table bankres 
\copy mt5.bankres from '/usr1/dump-MT5/bankres.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bankres__recid_seq', (SELECT MAX(_recid) FROM mt5.bankres));
update mt5.bankres set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table bankres 
\echo . 
\echo Loading Table bediener 
\copy mt5.bediener from '/usr1/dump-MT5/bediener.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bediener__recid_seq', (SELECT MAX(_recid) FROM mt5.bediener));
\echo Finish Table bediener 
\echo . 
\echo Loading Table bill 
\copy mt5.bill from '/usr1/dump-MT5/bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bill__recid_seq', (SELECT MAX(_recid) FROM mt5.bill));
\echo Finish Table bill 
\echo . 
\echo Loading Table bill_lin_tax 
\copy mt5.bill_lin_tax from '/usr1/dump-MT5/bill-lin-tax.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bill_lin_tax__recid_seq', (SELECT MAX(_recid) FROM mt5.bill_lin_tax));
\echo Finish Table bill_lin_tax 
\echo . 
\echo Loading Table bill_line 
\copy mt5.bill_line from '/usr1/dump-MT5/bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bill_line__recid_seq', (SELECT MAX(_recid) FROM mt5.bill_line));
\echo Finish Table bill_line 
\echo . 
\echo Loading Table billhis 
\copy mt5.billhis from '/usr1/dump-MT5/billhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.billhis__recid_seq', (SELECT MAX(_recid) FROM mt5.billhis));
\echo Finish Table billhis 
\echo . 
\echo Loading Table billjournal 
\copy mt5.billjournal from '/usr1/dump-MT5/billjournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.billjournal__recid_seq', (SELECT MAX(_recid) FROM mt5.billjournal));
\echo Finish Table billjournal 
\echo . 
\echo Loading Table bk_beleg 
\copy mt5.bk_beleg from '/usr1/dump-MT5/bk-beleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_beleg__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_beleg));
\echo Finish Table bk_beleg 
\echo . 
\echo Loading Table bk_fsdef 
\copy mt5.bk_fsdef from '/usr1/dump-MT5/bk-fsdef.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_fsdef__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_fsdef));
\echo Finish Table bk_fsdef 
\echo . 
\echo Loading Table bk_func 
\copy mt5.bk_func from '/usr1/dump-MT5/bk-func.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_func__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_func));
update mt5.bk_func set anlass = array_replace(anlass,NULL,''); 
update mt5.bk_func set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update mt5.bk_func set ape__speisen = array_replace(ape__speisen,NULL,''); 
update mt5.bk_func set arrival = array_replace(arrival,NULL,''); 
update mt5.bk_func set c_resstatus = array_replace(c_resstatus,NULL,''); 
update mt5.bk_func set dance = array_replace(dance,NULL,''); 
update mt5.bk_func set deko2 = array_replace(deko2,NULL,''); 
update mt5.bk_func set dekoration = array_replace(dekoration,NULL,''); 
update mt5.bk_func set digestif = array_replace(digestif,NULL,''); 
update mt5.bk_func set dinner = array_replace(dinner,NULL,''); 
update mt5.bk_func set f_menu = array_replace(f_menu,NULL,''); 
update mt5.bk_func set f_no = array_replace(f_no,NULL,''); 
update mt5.bk_func set fotograf = array_replace(fotograf,NULL,''); 
update mt5.bk_func set gaestebuch = array_replace(gaestebuch,NULL,''); 
update mt5.bk_func set garderobe = array_replace(garderobe,NULL,''); 
update mt5.bk_func set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update mt5.bk_func set kaffee = array_replace(kaffee,NULL,''); 
update mt5.bk_func set kartentext = array_replace(kartentext,NULL,''); 
update mt5.bk_func set kontaktperson = array_replace(kontaktperson,NULL,''); 
update mt5.bk_func set kuenstler = array_replace(kuenstler,NULL,''); 
update mt5.bk_func set menue = array_replace(menue,NULL,''); 
update mt5.bk_func set menuekarten = array_replace(menuekarten,NULL,''); 
update mt5.bk_func set musik = array_replace(musik,NULL,''); 
update mt5.bk_func set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update mt5.bk_func set nadkarte = array_replace(nadkarte,NULL,''); 
update mt5.bk_func set ndessen = array_replace(ndessen,NULL,''); 
update mt5.bk_func set personen2 = array_replace(personen2,NULL,''); 
update mt5.bk_func set raeume = array_replace(raeume,NULL,''); 
update mt5.bk_func set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update mt5.bk_func set raummiete = array_replace(raummiete,NULL,''); 
update mt5.bk_func set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update mt5.bk_func set service = array_replace(service,NULL,''); 
update mt5.bk_func set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update mt5.bk_func set sonstiges = array_replace(sonstiges,NULL,''); 
update mt5.bk_func set technik = array_replace(technik,NULL,''); 
update mt5.bk_func set tischform = array_replace(tischform,NULL,''); 
update mt5.bk_func set tischordnung = array_replace(tischordnung,NULL,''); 
update mt5.bk_func set tischplan = array_replace(tischplan,NULL,''); 
update mt5.bk_func set tischreden = array_replace(tischreden,NULL,''); 
update mt5.bk_func set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update mt5.bk_func set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update mt5.bk_func set va_ablauf = array_replace(va_ablauf,NULL,''); 
update mt5.bk_func set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update mt5.bk_func set vip = array_replace(vip,NULL,''); 
update mt5.bk_func set weine = array_replace(weine,NULL,''); 
update mt5.bk_func set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bk_func 
\echo . 
\echo Loading Table bk_package 
\copy mt5.bk_package from '/usr1/dump-MT5/bk-package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_package__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_package));
\echo Finish Table bk_package 
\echo . 
\echo Loading Table bk_pause 
\copy mt5.bk_pause from '/usr1/dump-MT5/bk-pause.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_pause__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_pause));
\echo Finish Table bk_pause 
\echo . 
\echo Loading Table bk_rart 
\copy mt5.bk_rart from '/usr1/dump-MT5/bk-rart.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_rart__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_rart));
\echo Finish Table bk_rart 
\echo . 
\echo Loading Table bk_raum 
\copy mt5.bk_raum from '/usr1/dump-MT5/bk-raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_raum__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_raum));
\echo Finish Table bk_raum 
\echo . 
\echo Loading Table bk_reser 
\copy mt5.bk_reser from '/usr1/dump-MT5/bk-reser.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_reser__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_reser));
\echo Finish Table bk_reser 
\echo . 
\echo Loading Table bk_rset 
\copy mt5.bk_rset from '/usr1/dump-MT5/bk-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_rset__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_rset));
\echo Finish Table bk_rset 
\echo . 
\echo Loading Table bk_setup 
\copy mt5.bk_setup from '/usr1/dump-MT5/bk-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_setup__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_setup));
\echo Finish Table bk_setup 
\echo . 
\echo Loading Table bk_stat 
\copy mt5.bk_stat from '/usr1/dump-MT5/bk-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_stat__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_stat));
\echo Finish Table bk_stat 
\echo . 
\echo Loading Table bk_veran 
\copy mt5.bk_veran from '/usr1/dump-MT5/bk-veran.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bk_veran__recid_seq', (SELECT MAX(_recid) FROM mt5.bk_veran));
update mt5.bk_veran set payment_userinit = array_replace(payment_userinit,NULL,''); 
\echo Finish Table bk_veran 
\echo . 
\echo Loading Table bl_dates 
\copy mt5.bl_dates from '/usr1/dump-MT5/bl-dates.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bl_dates__recid_seq', (SELECT MAX(_recid) FROM mt5.bl_dates));
\echo Finish Table bl_dates 
\echo . 
\echo Loading Table blinehis 
\copy mt5.blinehis from '/usr1/dump-MT5/blinehis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.blinehis__recid_seq', (SELECT MAX(_recid) FROM mt5.blinehis));
\echo Finish Table blinehis 
\echo . 
\echo Loading Table bresline 
\copy mt5.bresline from '/usr1/dump-MT5/bresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.bresline__recid_seq', (SELECT MAX(_recid) FROM mt5.bresline));
update mt5.bresline set texte = array_replace(texte,NULL,''); 
\echo Finish Table bresline 
\echo . 
\echo Loading Table brief 
\copy mt5.brief from '/usr1/dump-MT5/brief.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.brief__recid_seq', (SELECT MAX(_recid) FROM mt5.brief));
\echo Finish Table brief 
\echo . 
\echo Loading Table brieftmp 
\copy mt5.brieftmp from '/usr1/dump-MT5/brieftmp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.brieftmp__recid_seq', (SELECT MAX(_recid) FROM mt5.brieftmp));
\echo Finish Table brieftmp 
\echo . 
\echo Loading Table briefzei 
\copy mt5.briefzei from '/usr1/dump-MT5/briefzei.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.briefzei__recid_seq', (SELECT MAX(_recid) FROM mt5.briefzei));
\echo Finish Table briefzei 
\echo . 
\echo Loading Table budget 
\copy mt5.budget from '/usr1/dump-MT5/budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.budget__recid_seq', (SELECT MAX(_recid) FROM mt5.budget));
\echo Finish Table budget 
\echo . 
\echo Loading Table calls 
\copy mt5.calls from '/usr1/dump-MT5/calls.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.calls__recid_seq', (SELECT MAX(_recid) FROM mt5.calls));
\echo Finish Table calls 
\echo . 
\echo Loading Table cl_bonus 
\copy mt5.cl_bonus from '/usr1/dump-MT5/cl-bonus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_bonus__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_bonus));
\echo Finish Table cl_bonus 
\echo . 
\echo Loading Table cl_book 
\copy mt5.cl_book from '/usr1/dump-MT5/cl-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_book__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_book));
\echo Finish Table cl_book 
\echo . 
\echo Loading Table cl_checkin 
\copy mt5.cl_checkin from '/usr1/dump-MT5/cl-checkin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_checkin__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_checkin));
\echo Finish Table cl_checkin 
\echo . 
\echo Loading Table cl_class 
\copy mt5.cl_class from '/usr1/dump-MT5/cl-class.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_class__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_class));
\echo Finish Table cl_class 
\echo . 
\echo Loading Table cl_enroll 
\copy mt5.cl_enroll from '/usr1/dump-MT5/cl-enroll.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_enroll__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_enroll));
\echo Finish Table cl_enroll 
\echo . 
\echo Loading Table cl_free 
\copy mt5.cl_free from '/usr1/dump-MT5/cl-free.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_free__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_free));
\echo Finish Table cl_free 
\echo . 
\echo Loading Table cl_histci 
\copy mt5.cl_histci from '/usr1/dump-MT5/cl-histci.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_histci__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_histci));
\echo Finish Table cl_histci 
\echo . 
\echo Loading Table cl_histpay 
\copy mt5.cl_histpay from '/usr1/dump-MT5/cl-histpay.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_histpay__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_histpay));
\echo Finish Table cl_histpay 
\echo . 
\echo Loading Table cl_histstatus 
\copy mt5.cl_histstatus from '/usr1/dump-MT5/cl-histstatus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_histstatus__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_histstatus));
\echo Finish Table cl_histstatus 
\echo . 
\echo Loading Table cl_histtrain 
\copy mt5.cl_histtrain from '/usr1/dump-MT5/cl-histtrain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_histtrain__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_histtrain));
\echo Finish Table cl_histtrain 
\echo . 
\echo Loading Table cl_histvisit 
\copy mt5.cl_histvisit from '/usr1/dump-MT5/cl-histvisit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_histvisit__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_histvisit));
\echo Finish Table cl_histvisit 
\echo . 
\echo Loading Table cl_home 
\copy mt5.cl_home from '/usr1/dump-MT5/cl-home.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_home__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_home));
\echo Finish Table cl_home 
\echo . 
\echo Loading Table cl_location 
\copy mt5.cl_location from '/usr1/dump-MT5/cl-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_location__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_location));
\echo Finish Table cl_location 
\echo . 
\echo Loading Table cl_locker 
\copy mt5.cl_locker from '/usr1/dump-MT5/cl-locker.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_locker__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_locker));
\echo Finish Table cl_locker 
\echo . 
\echo Loading Table cl_log 
\copy mt5.cl_log from '/usr1/dump-MT5/cl-log.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_log__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_log));
\echo Finish Table cl_log 
\echo . 
\echo Loading Table cl_member 
\copy mt5.cl_member from '/usr1/dump-MT5/cl-member.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_member__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_member));
\echo Finish Table cl_member 
\echo . 
\echo Loading Table cl_memtype 
\copy mt5.cl_memtype from '/usr1/dump-MT5/cl-memtype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_memtype__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_memtype));
\echo Finish Table cl_memtype 
\echo . 
\echo Loading Table cl_paysched 
\copy mt5.cl_paysched from '/usr1/dump-MT5/cl-paysched.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_paysched__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_paysched));
\echo Finish Table cl_paysched 
\echo . 
\echo Loading Table cl_stat 
\copy mt5.cl_stat from '/usr1/dump-MT5/cl-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_stat__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_stat));
\echo Finish Table cl_stat 
\echo . 
\echo Loading Table cl_stat1 
\copy mt5.cl_stat1 from '/usr1/dump-MT5/cl-stat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_stat1__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_stat1));
\echo Finish Table cl_stat1 
\echo . 
\echo Loading Table cl_towel 
\copy mt5.cl_towel from '/usr1/dump-MT5/cl-towel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_towel__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_towel));
\echo Finish Table cl_towel 
\echo . 
\echo Loading Table cl_trainer 
\copy mt5.cl_trainer from '/usr1/dump-MT5/cl-trainer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_trainer__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_trainer));
\echo Finish Table cl_trainer 
\echo . 
\echo Loading Table cl_upgrade 
\copy mt5.cl_upgrade from '/usr1/dump-MT5/cl-upgrade.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cl_upgrade__recid_seq', (SELECT MAX(_recid) FROM mt5.cl_upgrade));
\echo Finish Table cl_upgrade 
\echo . 
\echo Loading Table costbudget 
\copy mt5.costbudget from '/usr1/dump-MT5/costbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.costbudget__recid_seq', (SELECT MAX(_recid) FROM mt5.costbudget));
\echo Finish Table costbudget 
\echo . 
\echo Loading Table counters 
\copy mt5.counters from '/usr1/dump-MT5/counters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.counters__recid_seq', (SELECT MAX(_recid) FROM mt5.counters));
\echo Finish Table counters 
\echo . 
\echo Loading Table crm_campaign 
\copy mt5.crm_campaign from '/usr1/dump-MT5/crm-campaign.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_campaign__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_campaign));
\echo Finish Table crm_campaign 
\echo . 
\echo Loading Table crm_category 
\copy mt5.crm_category from '/usr1/dump-MT5/crm-category.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_category__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_category));
\echo Finish Table crm_category 
\echo . 
\echo Loading Table crm_dept 
\copy mt5.crm_dept from '/usr1/dump-MT5/crm-dept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_dept__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_dept));
\echo Finish Table crm_dept 
\echo . 
\echo Loading Table crm_dtl 
\copy mt5.crm_dtl from '/usr1/dump-MT5/crm-dtl.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_dtl__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_dtl));
\echo Finish Table crm_dtl 
\echo . 
\echo Loading Table crm_email 
\copy mt5.crm_email from '/usr1/dump-MT5/crm-email.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_email__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_email));
\echo Finish Table crm_email 
\echo . 
\echo Loading Table crm_event 
\copy mt5.crm_event from '/usr1/dump-MT5/crm-event.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_event__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_event));
\echo Finish Table crm_event 
\echo . 
\echo Loading Table crm_feedhdr 
\copy mt5.crm_feedhdr from '/usr1/dump-MT5/crm-feedhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_feedhdr__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_feedhdr));
\echo Finish Table crm_feedhdr 
\echo . 
\echo Loading Table crm_fnlresult 
\copy mt5.crm_fnlresult from '/usr1/dump-MT5/crm-fnlresult.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_fnlresult__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_fnlresult));
\echo Finish Table crm_fnlresult 
\echo . 
\echo Loading Table crm_language 
\copy mt5.crm_language from '/usr1/dump-MT5/crm-language.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_language__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_language));
\echo Finish Table crm_language 
\echo . 
\echo Loading Table crm_question 
\copy mt5.crm_question from '/usr1/dump-MT5/crm-question.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_question__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_question));
\echo Finish Table crm_question 
\echo . 
\echo Loading Table crm_tamplang 
\copy mt5.crm_tamplang from '/usr1/dump-MT5/crm-tamplang.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_tamplang__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_tamplang));
\echo Finish Table crm_tamplang 
\echo . 
\echo Loading Table crm_template 
\copy mt5.crm_template from '/usr1/dump-MT5/crm-template.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.crm_template__recid_seq', (SELECT MAX(_recid) FROM mt5.crm_template));
\echo Finish Table crm_template 
\echo . 
\echo Loading Table cross_dtl 
\copy mt5.cross_dtl from '/usr1/dump-MT5/cross-DTL.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cross_dtl__recid_seq', (SELECT MAX(_recid) FROM mt5.cross_dtl));
\echo Finish Table cross_dtl 
\echo . 
\echo Loading Table cross_hdr 
\copy mt5.cross_hdr from '/usr1/dump-MT5/cross-HDR.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.cross_hdr__recid_seq', (SELECT MAX(_recid) FROM mt5.cross_hdr));
\echo Finish Table cross_hdr 
\echo . 
\echo Loading Table debitor 
\copy mt5.debitor from '/usr1/dump-MT5/debitor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.debitor__recid_seq', (SELECT MAX(_recid) FROM mt5.debitor));
\echo Finish Table debitor 
\echo . 
\echo Loading Table debthis 
\copy mt5.debthis from '/usr1/dump-MT5/debthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.debthis__recid_seq', (SELECT MAX(_recid) FROM mt5.debthis));
\echo Finish Table debthis 
\echo . 
\echo Loading Table desttext 
\copy mt5.desttext from '/usr1/dump-MT5/desttext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.desttext__recid_seq', (SELECT MAX(_recid) FROM mt5.desttext));
\echo Finish Table desttext 
\echo . 
\echo Loading Table dml_art 
\copy mt5.dml_art from '/usr1/dump-MT5/dml-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.dml_art__recid_seq', (SELECT MAX(_recid) FROM mt5.dml_art));
\echo Finish Table dml_art 
\echo . 
\echo Loading Table dml_artdep 
\copy mt5.dml_artdep from '/usr1/dump-MT5/dml-artdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.dml_artdep__recid_seq', (SELECT MAX(_recid) FROM mt5.dml_artdep));
\echo Finish Table dml_artdep 
\echo . 
\echo Loading Table dml_rate 
\copy mt5.dml_rate from '/usr1/dump-MT5/dml-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.dml_rate__recid_seq', (SELECT MAX(_recid) FROM mt5.dml_rate));
\echo Finish Table dml_rate 
\echo . 
\echo Loading Table eg_action 
\copy mt5.eg_action from '/usr1/dump-MT5/eg-action.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_action__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_action));
\echo Finish Table eg_action 
\echo . 
\echo Loading Table eg_alert 
\copy mt5.eg_alert from '/usr1/dump-MT5/eg-Alert.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_alert__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_alert));
\echo Finish Table eg_alert 
\echo . 
\echo Loading Table eg_budget 
\copy mt5.eg_budget from '/usr1/dump-MT5/eg-budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_budget__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_budget));
\echo Finish Table eg_budget 
\echo . 
\echo Loading Table eg_cost 
\copy mt5.eg_cost from '/usr1/dump-MT5/eg-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_cost__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_cost));
\echo Finish Table eg_cost 
\echo . 
\echo Loading Table eg_duration 
\copy mt5.eg_duration from '/usr1/dump-MT5/eg-Duration.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_duration__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_duration));
\echo Finish Table eg_duration 
\echo . 
\echo Loading Table eg_location 
\copy mt5.eg_location from '/usr1/dump-MT5/eg-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_location__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_location));
\echo Finish Table eg_location 
\echo . 
\echo Loading Table eg_mainstat 
\copy mt5.eg_mainstat from '/usr1/dump-MT5/eg-MainStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_mainstat__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_mainstat));
\echo Finish Table eg_mainstat 
\echo . 
\echo Loading Table eg_maintain 
\copy mt5.eg_maintain from '/usr1/dump-MT5/eg-maintain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_maintain__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_maintain));
\echo Finish Table eg_maintain 
\echo . 
\echo Loading Table eg_mdetail 
\copy mt5.eg_mdetail from '/usr1/dump-MT5/eg-mdetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_mdetail__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_mdetail));
\echo Finish Table eg_mdetail 
\echo . 
\echo Loading Table eg_messageno 
\copy mt5.eg_messageno from '/usr1/dump-MT5/eg-MessageNo.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_messageno__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_messageno));
\echo Finish Table eg_messageno 
\echo . 
\echo Loading Table eg_mobilenr 
\copy mt5.eg_mobilenr from '/usr1/dump-MT5/eg-mobileNr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_mobilenr__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_mobilenr));
\echo Finish Table eg_mobilenr 
\echo . 
\echo Loading Table eg_moveproperty 
\copy mt5.eg_moveproperty from '/usr1/dump-MT5/eg-moveProperty.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_moveproperty__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_moveproperty));
\echo Finish Table eg_moveproperty 
\echo . 
\echo Loading Table eg_property 
\copy mt5.eg_property from '/usr1/dump-MT5/eg-property.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_property__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_property));
\echo Finish Table eg_property 
\echo . 
\echo Loading Table eg_propmeter 
\copy mt5.eg_propmeter from '/usr1/dump-MT5/eg-propMeter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_propmeter__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_propmeter));
\echo Finish Table eg_propmeter 
\echo . 
\echo Loading Table eg_queasy 
\copy mt5.eg_queasy from '/usr1/dump-MT5/eg-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_queasy__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_queasy));
\echo Finish Table eg_queasy 
\echo . 
\echo Loading Table eg_reqdetail 
\copy mt5.eg_reqdetail from '/usr1/dump-MT5/eg-reqDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_reqdetail__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_reqdetail));
\echo Finish Table eg_reqdetail 
\echo . 
\echo Loading Table eg_reqif 
\copy mt5.eg_reqif from '/usr1/dump-MT5/eg-reqif.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_reqif__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_reqif));
\echo Finish Table eg_reqif 
\echo . 
\echo Loading Table eg_reqstat 
\copy mt5.eg_reqstat from '/usr1/dump-MT5/eg-ReqStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_reqstat__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_reqstat));
\echo Finish Table eg_reqstat 
\echo . 
\echo Loading Table eg_request 
\copy mt5.eg_request from '/usr1/dump-MT5/eg-request.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_request__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_request));
\echo Finish Table eg_request 
\echo . 
\echo Loading Table eg_resources 
\copy mt5.eg_resources from '/usr1/dump-MT5/eg-resources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_resources__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_resources));
\echo Finish Table eg_resources 
\echo . 
\echo Loading Table eg_staff 
\copy mt5.eg_staff from '/usr1/dump-MT5/eg-staff.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_staff__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_staff));
\echo Finish Table eg_staff 
\echo . 
\echo Loading Table eg_stat 
\copy mt5.eg_stat from '/usr1/dump-MT5/eg-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_stat__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_stat));
\echo Finish Table eg_stat 
\echo . 
\echo Loading Table eg_subtask 
\copy mt5.eg_subtask from '/usr1/dump-MT5/eg-subtask.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_subtask__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_subtask));
\echo Finish Table eg_subtask 
\echo . 
\echo Loading Table eg_vendor 
\copy mt5.eg_vendor from '/usr1/dump-MT5/eg-vendor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_vendor__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_vendor));
\echo Finish Table eg_vendor 
\echo . 
\echo Loading Table eg_vperform 
\copy mt5.eg_vperform from '/usr1/dump-MT5/eg-vperform.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.eg_vperform__recid_seq', (SELECT MAX(_recid) FROM mt5.eg_vperform));
\echo Finish Table eg_vperform 
\echo . 
\echo Loading Table ekum 
\copy mt5.ekum from '/usr1/dump-MT5/ekum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.ekum__recid_seq', (SELECT MAX(_recid) FROM mt5.ekum));
\echo Finish Table ekum 
\echo . 
\echo Loading Table employee 
\copy mt5.employee from '/usr1/dump-MT5/employee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.employee__recid_seq', (SELECT MAX(_recid) FROM mt5.employee));
update mt5.employee set child = array_replace(child,NULL,''); 
\echo Finish Table employee 
\echo . 
\echo Loading Table equiplan 
\copy mt5.equiplan from '/usr1/dump-MT5/equiplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.equiplan__recid_seq', (SELECT MAX(_recid) FROM mt5.equiplan));
\echo Finish Table equiplan 
\echo . 
\echo Loading Table exrate 
\copy mt5.exrate from '/usr1/dump-MT5/exrate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.exrate__recid_seq', (SELECT MAX(_recid) FROM mt5.exrate));
\echo Finish Table exrate 
\echo . 
\echo Loading Table fa_artikel 
\copy mt5.fa_artikel from '/usr1/dump-MT5/fa-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_artikel__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_artikel));
\echo Finish Table fa_artikel 
\echo . 
\echo Loading Table fa_counter 
\copy mt5.fa_counter from '/usr1/dump-MT5/fa-Counter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_counter__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_counter));
\echo Finish Table fa_counter 
\echo . 
\echo Loading Table fa_dp 
\copy mt5.fa_dp from '/usr1/dump-MT5/fa-DP.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_dp__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_dp));
\echo Finish Table fa_dp 
\echo . 
\echo Loading Table fa_grup 
\copy mt5.fa_grup from '/usr1/dump-MT5/fa-grup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_grup__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_grup));
\echo Finish Table fa_grup 
\echo . 
\echo Loading Table fa_kateg 
\copy mt5.fa_kateg from '/usr1/dump-MT5/fa-kateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_kateg__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_kateg));
\echo Finish Table fa_kateg 
\echo . 
\echo Loading Table fa_lager 
\copy mt5.fa_lager from '/usr1/dump-MT5/fa-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_lager__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_lager));
\echo Finish Table fa_lager 
\echo . 
\echo Loading Table fa_op 
\copy mt5.fa_op from '/usr1/dump-MT5/fa-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_op__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_op));
\echo Finish Table fa_op 
\echo . 
\echo Loading Table fa_order 
\copy mt5.fa_order from '/usr1/dump-MT5/fa-Order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_order__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_order));
\echo Finish Table fa_order 
\echo . 
\echo Loading Table fa_ordheader 
\copy mt5.fa_ordheader from '/usr1/dump-MT5/fa-OrdHeader.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_ordheader__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_ordheader));
\echo Finish Table fa_ordheader 
\echo . 
\echo Loading Table fa_quodetail 
\copy mt5.fa_quodetail from '/usr1/dump-MT5/fa-QuoDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_quodetail__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_quodetail));
\echo Finish Table fa_quodetail 
\echo . 
\echo Loading Table fa_quotation 
\copy mt5.fa_quotation from '/usr1/dump-MT5/fa-quotation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_quotation__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_quotation));
\echo Finish Table fa_quotation 
\echo . 
\echo Loading Table fa_user 
\copy mt5.fa_user from '/usr1/dump-MT5/fa-user.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fa_user__recid_seq', (SELECT MAX(_recid) FROM mt5.fa_user));
update mt5.fa_user set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table fa_user 
\echo . 
\echo Loading Table fbstat 
\copy mt5.fbstat from '/usr1/dump-MT5/fbstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fbstat__recid_seq', (SELECT MAX(_recid) FROM mt5.fbstat));
\echo Finish Table fbstat 
\echo . 
\echo Loading Table feiertag 
\copy mt5.feiertag from '/usr1/dump-MT5/feiertag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.feiertag__recid_seq', (SELECT MAX(_recid) FROM mt5.feiertag));
\echo Finish Table feiertag 
\echo . 
\echo Loading Table ffont 
\copy mt5.ffont from '/usr1/dump-MT5/ffont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.ffont__recid_seq', (SELECT MAX(_recid) FROM mt5.ffont));
\echo Finish Table ffont 
\echo . 
\echo Loading Table fixleist 
\copy mt5.fixleist from '/usr1/dump-MT5/fixleist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.fixleist__recid_seq', (SELECT MAX(_recid) FROM mt5.fixleist));
\echo Finish Table fixleist 
\echo . 
\echo Loading Table gc_giro 
\copy mt5.gc_giro from '/usr1/dump-MT5/gc-giro.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gc_giro__recid_seq', (SELECT MAX(_recid) FROM mt5.gc_giro));
update mt5.gc_giro set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_giro 
\echo . 
\echo Loading Table gc_jouhdr 
\copy mt5.gc_jouhdr from '/usr1/dump-MT5/gc-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gc_jouhdr__recid_seq', (SELECT MAX(_recid) FROM mt5.gc_jouhdr));
\echo Finish Table gc_jouhdr 
\echo . 
\echo Loading Table gc_journal 
\copy mt5.gc_journal from '/usr1/dump-MT5/gc-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gc_journal__recid_seq', (SELECT MAX(_recid) FROM mt5.gc_journal));
\echo Finish Table gc_journal 
\echo . 
\echo Loading Table gc_pi 
\copy mt5.gc_pi from '/usr1/dump-MT5/gc-PI.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gc_pi__recid_seq', (SELECT MAX(_recid) FROM mt5.gc_pi));
update mt5.gc_pi set bez_array = array_replace(bez_array,NULL,''); 
update mt5.gc_pi set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_pi 
\echo . 
\echo Loading Table gc_piacct 
\copy mt5.gc_piacct from '/usr1/dump-MT5/gc-piacct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gc_piacct__recid_seq', (SELECT MAX(_recid) FROM mt5.gc_piacct));
\echo Finish Table gc_piacct 
\echo . 
\echo Loading Table gc_pibline 
\copy mt5.gc_pibline from '/usr1/dump-MT5/gc-PIbline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gc_pibline__recid_seq', (SELECT MAX(_recid) FROM mt5.gc_pibline));
\echo Finish Table gc_pibline 
\echo . 
\echo Loading Table gc_pitype 
\copy mt5.gc_pitype from '/usr1/dump-MT5/gc-piType.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gc_pitype__recid_seq', (SELECT MAX(_recid) FROM mt5.gc_pitype));
\echo Finish Table gc_pitype 
\echo . 
\echo Loading Table genfcast 
\copy mt5.genfcast from '/usr1/dump-MT5/genfcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.genfcast__recid_seq', (SELECT MAX(_recid) FROM mt5.genfcast));
update mt5.genfcast set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genfcast 
\echo . 
\echo Loading Table genlayout 
\copy mt5.genlayout from '/usr1/dump-MT5/genlayout.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.genlayout__recid_seq', (SELECT MAX(_recid) FROM mt5.genlayout));
update mt5.genlayout set button_ext = array_replace(button_ext,NULL,''); 
update mt5.genlayout set char_ext = array_replace(char_ext,NULL,''); 
update mt5.genlayout set combo_ext = array_replace(combo_ext,NULL,''); 
update mt5.genlayout set date_ext = array_replace(date_ext,NULL,''); 
update mt5.genlayout set deci_ext = array_replace(deci_ext,NULL,''); 
update mt5.genlayout set inte_ext = array_replace(inte_ext,NULL,''); 
update mt5.genlayout set logi_ext = array_replace(logi_ext,NULL,''); 
update mt5.genlayout set string_ext = array_replace(string_ext,NULL,''); 
update mt5.genlayout set tchar_ext = array_replace(tchar_ext,NULL,''); 
update mt5.genlayout set tdate_ext = array_replace(tdate_ext,NULL,''); 
update mt5.genlayout set tdeci_ext = array_replace(tdeci_ext,NULL,''); 
update mt5.genlayout set tinte_ext = array_replace(tinte_ext,NULL,''); 
update mt5.genlayout set tlogi_ext = array_replace(tlogi_ext,NULL,''); 
\echo Finish Table genlayout 
\echo . 
\echo Loading Table genstat 
\copy mt5.genstat from '/usr1/dump-MT5/genstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.genstat__recid_seq', (SELECT MAX(_recid) FROM mt5.genstat));
update mt5.genstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genstat 
\echo . 
\echo Loading Table gentable 
\copy mt5.gentable from '/usr1/dump-MT5/gentable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gentable__recid_seq', (SELECT MAX(_recid) FROM mt5.gentable));
update mt5.gentable set char_ext = array_replace(char_ext,NULL,''); 
update mt5.gentable set combo_ext = array_replace(combo_ext,NULL,''); 
\echo Finish Table gentable 
\echo . 
\echo Loading Table gk_field 
\copy mt5.gk_field from '/usr1/dump-MT5/gk-field.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gk_field__recid_seq', (SELECT MAX(_recid) FROM mt5.gk_field));
\echo Finish Table gk_field 
\echo . 
\echo Loading Table gk_label 
\copy mt5.gk_label from '/usr1/dump-MT5/gk-label.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gk_label__recid_seq', (SELECT MAX(_recid) FROM mt5.gk_label));
\echo Finish Table gk_label 
\echo . 
\echo Loading Table gk_notes 
\copy mt5.gk_notes from '/usr1/dump-MT5/gk-notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gk_notes__recid_seq', (SELECT MAX(_recid) FROM mt5.gk_notes));
update mt5.gk_notes set notes = array_replace(notes,NULL,''); 
\echo Finish Table gk_notes 
\echo . 
\echo Loading Table gl_acct 
\copy mt5.gl_acct from '/usr1/dump-MT5/gl-acct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_acct__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_acct));
\echo Finish Table gl_acct 
\echo . 
\echo Loading Table gl_accthis 
\copy mt5.gl_accthis from '/usr1/dump-MT5/gl-accthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_accthis__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_accthis));
\echo Finish Table gl_accthis 
\echo . 
\echo Loading Table gl_coa 
\copy mt5.gl_coa from '/usr1/dump-MT5/gl-coa.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_coa__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_coa));
\echo Finish Table gl_coa 
\echo . 
\echo Loading Table gl_cost 
\copy mt5.gl_cost from '/usr1/dump-MT5/gl-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_cost__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_cost));
\echo Finish Table gl_cost 
\echo . 
\echo Loading Table gl_department 
\copy mt5.gl_department from '/usr1/dump-MT5/gl-department.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_department__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_department));
\echo Finish Table gl_department 
\echo . 
\echo Loading Table gl_fstype 
\copy mt5.gl_fstype from '/usr1/dump-MT5/gl-fstype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_fstype__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_fstype));
\echo Finish Table gl_fstype 
\echo . 
\echo Loading Table gl_htljournal 
\copy mt5.gl_htljournal from '/usr1/dump-MT5/gl-htljournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_htljournal__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_htljournal));
\echo Finish Table gl_htljournal 
\echo . 
\echo Loading Table gl_jhdrhis 
\copy mt5.gl_jhdrhis from '/usr1/dump-MT5/gl-jhdrhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_jhdrhis__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_jhdrhis));
\echo Finish Table gl_jhdrhis 
\echo . 
\echo Loading Table gl_jouhdr 
\copy mt5.gl_jouhdr from '/usr1/dump-MT5/gl-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_jouhdr__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_jouhdr));
\echo Finish Table gl_jouhdr 
\echo . 
\echo Loading Table gl_jourhis 
\copy mt5.gl_jourhis from '/usr1/dump-MT5/gl-jourhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_jourhis__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_jourhis));
\echo Finish Table gl_jourhis 
\echo . 
\echo Loading Table gl_journal 
\copy mt5.gl_journal from '/usr1/dump-MT5/gl-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_journal__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_journal));
\echo Finish Table gl_journal 
\echo . 
\echo Loading Table gl_main 
\copy mt5.gl_main from '/usr1/dump-MT5/gl-main.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.gl_main__recid_seq', (SELECT MAX(_recid) FROM mt5.gl_main));
\echo Finish Table gl_main 
\echo . 
\echo Loading Table golf_caddie 
\copy mt5.golf_caddie from '/usr1/dump-MT5/golf-caddie.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_caddie__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_caddie));
\echo Finish Table golf_caddie 
\echo . 
\echo Loading Table golf_caddie_assignment 
\copy mt5.golf_caddie_assignment from '/usr1/dump-MT5/golf-caddie-assignment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_caddie_assignment__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_caddie_assignment));
\echo Finish Table golf_caddie_assignment 
\echo . 
\echo Loading Table golf_course 
\copy mt5.golf_course from '/usr1/dump-MT5/golf-course.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_course__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_course));
\echo Finish Table golf_course 
\echo . 
\echo Loading Table golf_flight_reservation 
\copy mt5.golf_flight_reservation from '/usr1/dump-MT5/golf-flight-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_flight_reservation__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_flight_reservation));
\echo Finish Table golf_flight_reservation 
\echo . 
\echo Loading Table golf_flight_reservation_hist 
\copy mt5.golf_flight_reservation_hist from '/usr1/dump-MT5/golf-flight-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_flight_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_flight_reservation_hist));
\echo Finish Table golf_flight_reservation_hist 
\echo . 
\echo Loading Table golf_golfer_reservation 
\copy mt5.golf_golfer_reservation from '/usr1/dump-MT5/golf-golfer-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_golfer_reservation__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_golfer_reservation));
\echo Finish Table golf_golfer_reservation 
\echo . 
\echo Loading Table golf_golfer_reservation_hist 
\copy mt5.golf_golfer_reservation_hist from '/usr1/dump-MT5/golf-golfer-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_golfer_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_golfer_reservation_hist));
\echo Finish Table golf_golfer_reservation_hist 
\echo . 
\echo Loading Table golf_holiday 
\copy mt5.golf_holiday from '/usr1/dump-MT5/golf-holiday.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_holiday__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_holiday));
\echo Finish Table golf_holiday 
\echo . 
\echo Loading Table golf_main_reservation 
\copy mt5.golf_main_reservation from '/usr1/dump-MT5/golf-main-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_main_reservation__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_main_reservation));
\echo Finish Table golf_main_reservation 
\echo . 
\echo Loading Table golf_main_reservation_hist 
\copy mt5.golf_main_reservation_hist from '/usr1/dump-MT5/golf-main-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_main_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_main_reservation_hist));
\echo Finish Table golf_main_reservation_hist 
\echo . 
\echo Loading Table golf_rate 
\copy mt5.golf_rate from '/usr1/dump-MT5/golf-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_rate__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_rate));
\echo Finish Table golf_rate 
\echo . 
\echo Loading Table golf_shift 
\copy mt5.golf_shift from '/usr1/dump-MT5/golf-shift.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_shift__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_shift));
\echo Finish Table golf_shift 
\echo . 
\echo Loading Table golf_transfer 
\copy mt5.golf_transfer from '/usr1/dump-MT5/golf-transfer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.golf_transfer__recid_seq', (SELECT MAX(_recid) FROM mt5.golf_transfer));
\echo Finish Table golf_transfer 
\echo . 
\echo Loading Table guest 
\copy mt5.guest from '/usr1/dump-MT5/guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guest__recid_seq', (SELECT MAX(_recid) FROM mt5.guest));
update mt5.guest set notizen = array_replace(notizen,NULL,''); 
update mt5.guest set vornamekind = array_replace(vornamekind,NULL,''); 
\echo Finish Table guest 
\echo . 
\echo Loading Table guest_pr 
\copy mt5.guest_pr from '/usr1/dump-MT5/guest-pr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guest_pr__recid_seq', (SELECT MAX(_recid) FROM mt5.guest_pr));
\echo Finish Table guest_pr 
\echo . 
\echo Loading Table guest_queasy 
\copy mt5.guest_queasy from '/usr1/dump-MT5/guest-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guest_queasy__recid_seq', (SELECT MAX(_recid) FROM mt5.guest_queasy));
\echo Finish Table guest_queasy 
\echo . 
\echo Loading Table guest_remark 
\copy mt5.guest_remark from '/usr1/dump-MT5/guest-remark.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guest_remark__recid_seq', (SELECT MAX(_recid) FROM mt5.guest_remark));
update mt5.guest_remark set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table guest_remark 
\echo . 
\echo Loading Table guestat 
\copy mt5.guestat from '/usr1/dump-MT5/guestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guestat__recid_seq', (SELECT MAX(_recid) FROM mt5.guestat));
\echo Finish Table guestat 
\echo . 
\echo Loading Table guestat1 
\copy mt5.guestat1 from '/usr1/dump-MT5/guestat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guestat1__recid_seq', (SELECT MAX(_recid) FROM mt5.guestat1));
\echo Finish Table guestat1 
\echo . 
\echo Loading Table guestbook 
\copy mt5.guestbook from '/usr1/dump-MT5/guestbook.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guestbook__recid_seq', (SELECT MAX(_recid) FROM mt5.guestbook));
update mt5.guestbook set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table guestbook 
\echo . 
\echo Loading Table guestbud 
\copy mt5.guestbud from '/usr1/dump-MT5/guestbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guestbud__recid_seq', (SELECT MAX(_recid) FROM mt5.guestbud));
\echo Finish Table guestbud 
\echo . 
\echo Loading Table guestseg 
\copy mt5.guestseg from '/usr1/dump-MT5/guestseg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.guestseg__recid_seq', (SELECT MAX(_recid) FROM mt5.guestseg));
\echo Finish Table guestseg 
\echo . 
\echo Loading Table h_artcost 
\copy mt5.h_artcost from '/usr1/dump-MT5/h-artcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_artcost__recid_seq', (SELECT MAX(_recid) FROM mt5.h_artcost));
\echo Finish Table h_artcost 
\echo . 
\echo Loading Table h_artikel 
\copy mt5.h_artikel from '/usr1/dump-MT5/h-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_artikel__recid_seq', (SELECT MAX(_recid) FROM mt5.h_artikel));
\echo Finish Table h_artikel 
\echo . 
\echo Loading Table h_bill 
\copy mt5.h_bill from '/usr1/dump-MT5/h-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_bill__recid_seq', (SELECT MAX(_recid) FROM mt5.h_bill));
\echo Finish Table h_bill 
\echo . 
\echo Loading Table h_bill_line 
\copy mt5.h_bill_line from '/usr1/dump-MT5/h-bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_bill_line__recid_seq', (SELECT MAX(_recid) FROM mt5.h_bill_line));
\echo Finish Table h_bill_line 
\echo . 
\echo Loading Table h_compli 
\copy mt5.h_compli from '/usr1/dump-MT5/h-compli.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_compli__recid_seq', (SELECT MAX(_recid) FROM mt5.h_compli));
\echo Finish Table h_compli 
\echo . 
\echo Loading Table h_cost 
\copy mt5.h_cost from '/usr1/dump-MT5/h-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_cost__recid_seq', (SELECT MAX(_recid) FROM mt5.h_cost));
\echo Finish Table h_cost 
\echo . 
\echo Loading Table h_journal 
\copy mt5.h_journal from '/usr1/dump-MT5/h-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_journal__recid_seq', (SELECT MAX(_recid) FROM mt5.h_journal));
\echo Finish Table h_journal 
\echo . 
\echo Loading Table h_menu 
\copy mt5.h_menu from '/usr1/dump-MT5/h-menu.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_menu__recid_seq', (SELECT MAX(_recid) FROM mt5.h_menu));
\echo Finish Table h_menu 
\echo . 
\echo Loading Table h_mjourn 
\copy mt5.h_mjourn from '/usr1/dump-MT5/h-mjourn.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_mjourn__recid_seq', (SELECT MAX(_recid) FROM mt5.h_mjourn));
\echo Finish Table h_mjourn 
\echo . 
\echo Loading Table h_oldjou 
\copy mt5.h_oldjou from '/usr1/dump-MT5/h-oldjou.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_oldjou__recid_seq', (SELECT MAX(_recid) FROM mt5.h_oldjou));
\echo Finish Table h_oldjou 
\echo . 
\echo Loading Table h_order 
\copy mt5.h_order from '/usr1/dump-MT5/h-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_order__recid_seq', (SELECT MAX(_recid) FROM mt5.h_order));
update mt5.h_order set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table h_order 
\echo . 
\echo Loading Table h_queasy 
\copy mt5.h_queasy from '/usr1/dump-MT5/h-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_queasy__recid_seq', (SELECT MAX(_recid) FROM mt5.h_queasy));
\echo Finish Table h_queasy 
\echo . 
\echo Loading Table h_rezept 
\copy mt5.h_rezept from '/usr1/dump-MT5/h-rezept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_rezept__recid_seq', (SELECT MAX(_recid) FROM mt5.h_rezept));
\echo Finish Table h_rezept 
\echo . 
\echo Loading Table h_rezlin 
\copy mt5.h_rezlin from '/usr1/dump-MT5/h-rezlin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_rezlin__recid_seq', (SELECT MAX(_recid) FROM mt5.h_rezlin));
\echo Finish Table h_rezlin 
\echo . 
\echo Loading Table h_storno 
\copy mt5.h_storno from '/usr1/dump-MT5/h-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_storno__recid_seq', (SELECT MAX(_recid) FROM mt5.h_storno));
\echo Finish Table h_storno 
\echo . 
\echo Loading Table h_umsatz 
\copy mt5.h_umsatz from '/usr1/dump-MT5/h-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.h_umsatz__recid_seq', (SELECT MAX(_recid) FROM mt5.h_umsatz));
\echo Finish Table h_umsatz 
\echo . 
\echo Loading Table history 
\copy mt5.history from '/usr1/dump-MT5/history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.history__recid_seq', (SELECT MAX(_recid) FROM mt5.history));
\echo Finish Table history 
\echo . 
\echo Loading Table hoteldpt 
\copy mt5.hoteldpt from '/usr1/dump-MT5/hoteldpt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.hoteldpt__recid_seq', (SELECT MAX(_recid) FROM mt5.hoteldpt));
\echo Finish Table hoteldpt 
\echo . 
\echo Loading Table hrbeleg 
\copy mt5.hrbeleg from '/usr1/dump-MT5/hrbeleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.hrbeleg__recid_seq', (SELECT MAX(_recid) FROM mt5.hrbeleg));
\echo Finish Table hrbeleg 
\echo . 
\echo Loading Table hrsegement 
\copy mt5.hrsegement from '/usr1/dump-MT5/hrsegement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.hrsegement__recid_seq', (SELECT MAX(_recid) FROM mt5.hrsegement));
\echo Finish Table hrsegement 
\echo . 
\echo Loading Table htparam 
\copy mt5.htparam from '/usr1/dump-MT5/htparam.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.htparam__recid_seq', (SELECT MAX(_recid) FROM mt5.htparam));
\echo Finish Table htparam 
\echo . 
\echo Loading Table htreport 
\copy mt5.htreport from '/usr1/dump-MT5/htreport.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.htreport__recid_seq', (SELECT MAX(_recid) FROM mt5.htreport));
\echo Finish Table htreport 
\echo . 
\echo Loading Table iftable 
\copy mt5.iftable from '/usr1/dump-MT5/iftable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.iftable__recid_seq', (SELECT MAX(_recid) FROM mt5.iftable));
\echo Finish Table iftable 
\echo . 
\echo Loading Table interface 
\copy mt5.interface from '/usr1/dump-MT5/interface.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.interface__recid_seq', (SELECT MAX(_recid) FROM mt5.interface));
\echo Finish Table interface 
\echo . 
\echo Loading Table k_history 
\copy mt5.k_history from '/usr1/dump-MT5/k-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.k_history__recid_seq', (SELECT MAX(_recid) FROM mt5.k_history));
\echo Finish Table k_history 
\echo . 
\echo Loading Table kabine 
\copy mt5.kabine from '/usr1/dump-MT5/kabine.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kabine__recid_seq', (SELECT MAX(_recid) FROM mt5.kabine));
\echo Finish Table kabine 
\echo . 
\echo Loading Table kalender 
\copy mt5.kalender from '/usr1/dump-MT5/kalender.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kalender__recid_seq', (SELECT MAX(_recid) FROM mt5.kalender));
update mt5.kalender set note = array_replace(note,NULL,''); 
\echo Finish Table kalender 
\echo . 
\echo Loading Table kasse 
\copy mt5.kasse from '/usr1/dump-MT5/kasse.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kasse__recid_seq', (SELECT MAX(_recid) FROM mt5.kasse));
\echo Finish Table kasse 
\echo . 
\echo Loading Table katpreis 
\copy mt5.katpreis from '/usr1/dump-MT5/katpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.katpreis__recid_seq', (SELECT MAX(_recid) FROM mt5.katpreis));
\echo Finish Table katpreis 
\echo . 
\echo Loading Table kellne1 
\copy mt5.kellne1 from '/usr1/dump-MT5/kellne1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kellne1__recid_seq', (SELECT MAX(_recid) FROM mt5.kellne1));
\echo Finish Table kellne1 
\echo . 
\echo Loading Table kellner 
\copy mt5.kellner from '/usr1/dump-MT5/kellner.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kellner__recid_seq', (SELECT MAX(_recid) FROM mt5.kellner));
\echo Finish Table kellner 
\echo . 
\echo Loading Table kontakt 
\copy mt5.kontakt from '/usr1/dump-MT5/kontakt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kontakt__recid_seq', (SELECT MAX(_recid) FROM mt5.kontakt));
\echo Finish Table kontakt 
\echo . 
\echo Loading Table kontline 
\copy mt5.kontline from '/usr1/dump-MT5/kontline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kontline__recid_seq', (SELECT MAX(_recid) FROM mt5.kontline));
\echo Finish Table kontline 
\echo . 
\echo Loading Table kontlink 
\copy mt5.kontlink from '/usr1/dump-MT5/kontlink.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kontlink__recid_seq', (SELECT MAX(_recid) FROM mt5.kontlink));
\echo Finish Table kontlink 
\echo . 
\echo Loading Table kontplan 
\copy mt5.kontplan from '/usr1/dump-MT5/kontplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kontplan__recid_seq', (SELECT MAX(_recid) FROM mt5.kontplan));
\echo Finish Table kontplan 
\echo . 
\echo Loading Table kontstat 
\copy mt5.kontstat from '/usr1/dump-MT5/kontstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kontstat__recid_seq', (SELECT MAX(_recid) FROM mt5.kontstat));
update mt5.kontstat set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table kontstat 
\echo . 
\echo Loading Table kresline 
\copy mt5.kresline from '/usr1/dump-MT5/kresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.kresline__recid_seq', (SELECT MAX(_recid) FROM mt5.kresline));
\echo Finish Table kresline 
\echo . 
\echo Loading Table l_artikel 
\copy mt5.l_artikel from '/usr1/dump-MT5/l-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_artikel__recid_seq', (SELECT MAX(_recid) FROM mt5.l_artikel));
update mt5.l_artikel set lief_artnr = array_replace(lief_artnr,NULL,''); 
\echo Finish Table l_artikel 
\echo . 
\echo Loading Table l_bestand 
\copy mt5.l_bestand from '/usr1/dump-MT5/l-bestand.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_bestand__recid_seq', (SELECT MAX(_recid) FROM mt5.l_bestand));
\echo Finish Table l_bestand 
\echo . 
\echo Loading Table l_besthis 
\copy mt5.l_besthis from '/usr1/dump-MT5/l-besthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_besthis__recid_seq', (SELECT MAX(_recid) FROM mt5.l_besthis));
\echo Finish Table l_besthis 
\echo . 
\echo Loading Table l_hauptgrp 
\copy mt5.l_hauptgrp from '/usr1/dump-MT5/l-hauptgrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_hauptgrp__recid_seq', (SELECT MAX(_recid) FROM mt5.l_hauptgrp));
\echo Finish Table l_hauptgrp 
\echo . 
\echo Loading Table l_kredit 
\copy mt5.l_kredit from '/usr1/dump-MT5/l-kredit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_kredit__recid_seq', (SELECT MAX(_recid) FROM mt5.l_kredit));
\echo Finish Table l_kredit 
\echo . 
\echo Loading Table l_lager 
\copy mt5.l_lager from '/usr1/dump-MT5/l-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_lager__recid_seq', (SELECT MAX(_recid) FROM mt5.l_lager));
\echo Finish Table l_lager 
\echo . 
\echo Loading Table l_lieferant 
\copy mt5.l_lieferant from '/usr1/dump-MT5/l-lieferant.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_lieferant__recid_seq', (SELECT MAX(_recid) FROM mt5.l_lieferant));
update mt5.l_lieferant set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table l_lieferant 
\echo . 
\echo Loading Table l_liefumsatz 
\copy mt5.l_liefumsatz from '/usr1/dump-MT5/l-liefumsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_liefumsatz__recid_seq', (SELECT MAX(_recid) FROM mt5.l_liefumsatz));
\echo Finish Table l_liefumsatz 
\echo . 
\echo Loading Table l_op 
\copy mt5.l_op from '/usr1/dump-MT5/l-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_op__recid_seq', (SELECT MAX(_recid) FROM mt5.l_op));
\echo Finish Table l_op 
\echo . 
\echo Loading Table l_ophdr 
\copy mt5.l_ophdr from '/usr1/dump-MT5/l-ophdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_ophdr__recid_seq', (SELECT MAX(_recid) FROM mt5.l_ophdr));
\echo Finish Table l_ophdr 
\echo . 
\echo Loading Table l_ophhis 
\copy mt5.l_ophhis from '/usr1/dump-MT5/l-ophhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_ophhis__recid_seq', (SELECT MAX(_recid) FROM mt5.l_ophhis));
\echo Finish Table l_ophhis 
\echo . 
\echo Loading Table l_ophis 
\copy mt5.l_ophis from '/usr1/dump-MT5/l-ophis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_ophis__recid_seq', (SELECT MAX(_recid) FROM mt5.l_ophis));
\echo Finish Table l_ophis 
\echo . 
\echo Loading Table l_order 
\copy mt5.l_order from '/usr1/dump-MT5/l-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_order__recid_seq', (SELECT MAX(_recid) FROM mt5.l_order));
update mt5.l_order set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_order 
\echo . 
\echo Loading Table l_orderhdr 
\copy mt5.l_orderhdr from '/usr1/dump-MT5/l-orderhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_orderhdr__recid_seq', (SELECT MAX(_recid) FROM mt5.l_orderhdr));
update mt5.l_orderhdr set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_orderhdr 
\echo . 
\echo Loading Table l_pprice 
\copy mt5.l_pprice from '/usr1/dump-MT5/l-pprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_pprice__recid_seq', (SELECT MAX(_recid) FROM mt5.l_pprice));
\echo Finish Table l_pprice 
\echo . 
\echo Loading Table l_quote 
\copy mt5.l_quote from '/usr1/dump-MT5/l-quote.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_quote__recid_seq', (SELECT MAX(_recid) FROM mt5.l_quote));
update mt5.l_quote set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table l_quote 
\echo . 
\echo Loading Table l_segment 
\copy mt5.l_segment from '/usr1/dump-MT5/l-segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_segment__recid_seq', (SELECT MAX(_recid) FROM mt5.l_segment));
\echo Finish Table l_segment 
\echo . 
\echo Loading Table l_umsatz 
\copy mt5.l_umsatz from '/usr1/dump-MT5/l-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_umsatz__recid_seq', (SELECT MAX(_recid) FROM mt5.l_umsatz));
\echo Finish Table l_umsatz 
\echo . 
\echo Loading Table l_untergrup 
\copy mt5.l_untergrup from '/usr1/dump-MT5/l-untergrup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_untergrup__recid_seq', (SELECT MAX(_recid) FROM mt5.l_untergrup));
\echo Finish Table l_untergrup 
\echo . 
\echo Loading Table l_verbrauch 
\copy mt5.l_verbrauch from '/usr1/dump-MT5/l-verbrauch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_verbrauch__recid_seq', (SELECT MAX(_recid) FROM mt5.l_verbrauch));
\echo Finish Table l_verbrauch 
\echo . 
\echo Loading Table l_zahlbed 
\copy mt5.l_zahlbed from '/usr1/dump-MT5/l-zahlbed.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.l_zahlbed__recid_seq', (SELECT MAX(_recid) FROM mt5.l_zahlbed));
\echo Finish Table l_zahlbed 
\echo . 
\echo Loading Table landstat 
\copy mt5.landstat from '/usr1/dump-MT5/landstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.landstat__recid_seq', (SELECT MAX(_recid) FROM mt5.landstat));
\echo Finish Table landstat 
\echo . 
\echo Loading Table masseur 
\copy mt5.masseur from '/usr1/dump-MT5/masseur.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.masseur__recid_seq', (SELECT MAX(_recid) FROM mt5.masseur));
\echo Finish Table masseur 
\echo . 
\echo Loading Table mast_art 
\copy mt5.mast_art from '/usr1/dump-MT5/mast-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mast_art__recid_seq', (SELECT MAX(_recid) FROM mt5.mast_art));
\echo Finish Table mast_art 
\echo . 
\echo Loading Table master 
\copy mt5.master from '/usr1/dump-MT5/master.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.master__recid_seq', (SELECT MAX(_recid) FROM mt5.master));
\echo Finish Table master 
\echo . 
\echo Loading Table mathis 
\copy mt5.mathis from '/usr1/dump-MT5/mathis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mathis__recid_seq', (SELECT MAX(_recid) FROM mt5.mathis));
\echo Finish Table mathis 
\echo . 
\echo Loading Table mc_aclub 
\copy mt5.mc_aclub from '/usr1/dump-MT5/mc-aclub.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mc_aclub__recid_seq', (SELECT MAX(_recid) FROM mt5.mc_aclub));
\echo Finish Table mc_aclub 
\echo . 
\echo Loading Table mc_cardhis 
\copy mt5.mc_cardhis from '/usr1/dump-MT5/mc-cardhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mc_cardhis__recid_seq', (SELECT MAX(_recid) FROM mt5.mc_cardhis));
\echo Finish Table mc_cardhis 
\echo . 
\echo Loading Table mc_disc 
\copy mt5.mc_disc from '/usr1/dump-MT5/mc-disc.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mc_disc__recid_seq', (SELECT MAX(_recid) FROM mt5.mc_disc));
\echo Finish Table mc_disc 
\echo . 
\echo Loading Table mc_fee 
\copy mt5.mc_fee from '/usr1/dump-MT5/mc-fee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mc_fee__recid_seq', (SELECT MAX(_recid) FROM mt5.mc_fee));
\echo Finish Table mc_fee 
\echo . 
\echo Loading Table mc_guest 
\copy mt5.mc_guest from '/usr1/dump-MT5/mc-guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mc_guest__recid_seq', (SELECT MAX(_recid) FROM mt5.mc_guest));
\echo Finish Table mc_guest 
\echo . 
\echo Loading Table mc_types 
\copy mt5.mc_types from '/usr1/dump-MT5/mc-types.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mc_types__recid_seq', (SELECT MAX(_recid) FROM mt5.mc_types));
\echo Finish Table mc_types 
\echo . 
\echo Loading Table mealcoup 
\copy mt5.mealcoup from '/usr1/dump-MT5/mealcoup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mealcoup__recid_seq', (SELECT MAX(_recid) FROM mt5.mealcoup));
\echo Finish Table mealcoup 
\echo . 
\echo Loading Table messages 
\copy mt5.messages from '/usr1/dump-MT5/messages.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.messages__recid_seq', (SELECT MAX(_recid) FROM mt5.messages));
update mt5.messages set messtext = array_replace(messtext,NULL,''); 
\echo Finish Table messages 
\echo . 
\echo Loading Table messe 
\copy mt5.messe from '/usr1/dump-MT5/messe.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.messe__recid_seq', (SELECT MAX(_recid) FROM mt5.messe));
\echo Finish Table messe 
\echo . 
\echo Loading Table mhis_line 
\copy mt5.mhis_line from '/usr1/dump-MT5/mhis-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.mhis_line__recid_seq', (SELECT MAX(_recid) FROM mt5.mhis_line));
\echo Finish Table mhis_line 
\echo . 
\echo Loading Table nation 
\copy mt5.nation from '/usr1/dump-MT5/nation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.nation__recid_seq', (SELECT MAX(_recid) FROM mt5.nation));
\echo Finish Table nation 
\echo . 
\echo Loading Table nationstat 
\copy mt5.nationstat from '/usr1/dump-MT5/nationstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.nationstat__recid_seq', (SELECT MAX(_recid) FROM mt5.nationstat));
\echo Finish Table nationstat 
\echo . 
\echo Loading Table natstat1 
\copy mt5.natstat1 from '/usr1/dump-MT5/natstat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.natstat1__recid_seq', (SELECT MAX(_recid) FROM mt5.natstat1));
\echo Finish Table natstat1 
\echo . 
\echo Loading Table nebenst 
\copy mt5.nebenst from '/usr1/dump-MT5/nebenst.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.nebenst__recid_seq', (SELECT MAX(_recid) FROM mt5.nebenst));
\echo Finish Table nebenst 
\echo . 
\echo Loading Table nightaudit 
\copy mt5.nightaudit from '/usr1/dump-MT5/nightaudit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.nightaudit__recid_seq', (SELECT MAX(_recid) FROM mt5.nightaudit));
\echo Finish Table nightaudit 
\echo . 
\echo Loading Table nitehist 
\copy mt5.nitehist from '/usr1/dump-MT5/nitehist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.nitehist__recid_seq', (SELECT MAX(_recid) FROM mt5.nitehist));
\echo Finish Table nitehist 
\echo . 
\echo Loading Table nitestor 
\copy mt5.nitestor from '/usr1/dump-MT5/nitestor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.nitestor__recid_seq', (SELECT MAX(_recid) FROM mt5.nitestor));
\echo Finish Table nitestor 
\echo . 
\echo Loading Table notes 
\copy mt5.notes from '/usr1/dump-MT5/notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.notes__recid_seq', (SELECT MAX(_recid) FROM mt5.notes));
update mt5.notes set note = array_replace(note,NULL,''); 
\echo Finish Table notes 
\echo . 
\echo Loading Table outorder 
\copy mt5.outorder from '/usr1/dump-MT5/outorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.outorder__recid_seq', (SELECT MAX(_recid) FROM mt5.outorder));
\echo Finish Table outorder 
\echo . 
\echo Loading Table package 
\copy mt5.package from '/usr1/dump-MT5/package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.package__recid_seq', (SELECT MAX(_recid) FROM mt5.package));
\echo Finish Table package 
\echo . 
\echo Loading Table parameters 
\copy mt5.parameters from '/usr1/dump-MT5/parameters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.parameters__recid_seq', (SELECT MAX(_recid) FROM mt5.parameters));
\echo Finish Table parameters 
\echo . 
\echo Loading Table paramtext 
\copy mt5.paramtext from '/usr1/dump-MT5/paramtext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.paramtext__recid_seq', (SELECT MAX(_recid) FROM mt5.paramtext));
\echo Finish Table paramtext 
\echo . 
\echo Loading Table pricecod 
\copy mt5.pricecod from '/usr1/dump-MT5/pricecod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.pricecod__recid_seq', (SELECT MAX(_recid) FROM mt5.pricecod));
\echo Finish Table pricecod 
\echo . 
\echo Loading Table pricegrp 
\copy mt5.pricegrp from '/usr1/dump-MT5/pricegrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.pricegrp__recid_seq', (SELECT MAX(_recid) FROM mt5.pricegrp));
\echo Finish Table pricegrp 
\echo . 
\echo Loading Table printcod 
\copy mt5.printcod from '/usr1/dump-MT5/printcod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.printcod__recid_seq', (SELECT MAX(_recid) FROM mt5.printcod));
\echo Finish Table printcod 
\echo . 
\echo Loading Table printer 
\copy mt5.printer from '/usr1/dump-MT5/printer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.printer__recid_seq', (SELECT MAX(_recid) FROM mt5.printer));
\echo Finish Table printer 
\echo . 
\echo Loading Table prmarket 
\copy mt5.prmarket from '/usr1/dump-MT5/prmarket.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.prmarket__recid_seq', (SELECT MAX(_recid) FROM mt5.prmarket));
\echo Finish Table prmarket 
\echo . 
\echo Loading Table progcat 
\copy mt5.progcat from '/usr1/dump-MT5/progcat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.progcat__recid_seq', (SELECT MAX(_recid) FROM mt5.progcat));
\echo Finish Table progcat 
\echo . 
\echo Loading Table progfile 
\copy mt5.progfile from '/usr1/dump-MT5/progfile.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.progfile__recid_seq', (SELECT MAX(_recid) FROM mt5.progfile));
\echo Finish Table progfile 
\echo . 
\echo Loading Table prtable 
\copy mt5.prtable from '/usr1/dump-MT5/prtable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.prtable__recid_seq', (SELECT MAX(_recid) FROM mt5.prtable));
\echo Finish Table prtable 
\echo . 
\echo Loading Table queasy 
\copy mt5.queasy from '/usr1/dump-MT5/queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.queasy__recid_seq', (SELECT MAX(_recid) FROM mt5.queasy));
\echo Finish Table queasy 
\echo . 
\echo Loading Table ratecode 
\copy mt5.ratecode from '/usr1/dump-MT5/ratecode.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.ratecode__recid_seq', (SELECT MAX(_recid) FROM mt5.ratecode));
update mt5.ratecode set char1 = array_replace(char1,NULL,''); 
\echo Finish Table ratecode 
\echo . 
\echo Loading Table raum 
\copy mt5.raum from '/usr1/dump-MT5/raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.raum__recid_seq', (SELECT MAX(_recid) FROM mt5.raum));
\echo Finish Table raum 
\echo . 
\echo Loading Table res_history 
\copy mt5.res_history from '/usr1/dump-MT5/res-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.res_history__recid_seq', (SELECT MAX(_recid) FROM mt5.res_history));
\echo Finish Table res_history 
\echo . 
\echo Loading Table res_line 
\copy mt5.res_line from '/usr1/dump-MT5/res-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.res_line__recid_seq', (SELECT MAX(_recid) FROM mt5.res_line));
\echo Finish Table res_line 
\echo . 
\echo Loading Table reservation 
\copy mt5.reservation from '/usr1/dump-MT5/reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.reservation__recid_seq', (SELECT MAX(_recid) FROM mt5.reservation));
\echo Finish Table reservation 
\echo . 
\echo Loading Table reslin_queasy 
\copy mt5.reslin_queasy from '/usr1/dump-MT5/reslin-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.reslin_queasy__recid_seq', (SELECT MAX(_recid) FROM mt5.reslin_queasy));
\echo Finish Table reslin_queasy 
\echo . 
\echo Loading Table resplan 
\copy mt5.resplan from '/usr1/dump-MT5/resplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.resplan__recid_seq', (SELECT MAX(_recid) FROM mt5.resplan));
\echo Finish Table resplan 
\echo . 
\echo Loading Table rg_reports 
\copy mt5.rg_reports from '/usr1/dump-MT5/rg-reports.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.rg_reports__recid_seq', (SELECT MAX(_recid) FROM mt5.rg_reports));
update mt5.rg_reports set metadata = array_replace(metadata,NULL,''); 
update mt5.rg_reports set slice_name = array_replace(slice_name,NULL,''); 
update mt5.rg_reports set view_name = array_replace(view_name,NULL,''); 
\echo Finish Table rg_reports 
\echo . 
\echo Loading Table rmbudget 
\copy mt5.rmbudget from '/usr1/dump-MT5/rmbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.rmbudget__recid_seq', (SELECT MAX(_recid) FROM mt5.rmbudget));
update mt5.rmbudget set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table rmbudget 
\echo . 
\echo Loading Table sales 
\copy mt5.sales from '/usr1/dump-MT5/sales.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sales__recid_seq', (SELECT MAX(_recid) FROM mt5.sales));
\echo Finish Table sales 
\echo . 
\echo Loading Table salesbud 
\copy mt5.salesbud from '/usr1/dump-MT5/salesbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.salesbud__recid_seq', (SELECT MAX(_recid) FROM mt5.salesbud));
\echo Finish Table salesbud 
\echo . 
\echo Loading Table salestat 
\copy mt5.salestat from '/usr1/dump-MT5/salestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.salestat__recid_seq', (SELECT MAX(_recid) FROM mt5.salestat));
\echo Finish Table salestat 
\echo . 
\echo Loading Table salestim 
\copy mt5.salestim from '/usr1/dump-MT5/salestim.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.salestim__recid_seq', (SELECT MAX(_recid) FROM mt5.salestim));
\echo Finish Table salestim 
\echo . 
\echo Loading Table segment 
\copy mt5.segment from '/usr1/dump-MT5/segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.segment__recid_seq', (SELECT MAX(_recid) FROM mt5.segment));
\echo Finish Table segment 
\echo . 
\echo Loading Table segmentstat 
\copy mt5.segmentstat from '/usr1/dump-MT5/segmentstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.segmentstat__recid_seq', (SELECT MAX(_recid) FROM mt5.segmentstat));
\echo Finish Table segmentstat 
\echo . 
\echo Loading Table sms_bcaster 
\copy mt5.sms_bcaster from '/usr1/dump-MT5/sms-bcaster.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sms_bcaster__recid_seq', (SELECT MAX(_recid) FROM mt5.sms_bcaster));
\echo Finish Table sms_bcaster 
\echo . 
\echo Loading Table sms_broadcast 
\copy mt5.sms_broadcast from '/usr1/dump-MT5/sms-broadcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sms_broadcast__recid_seq', (SELECT MAX(_recid) FROM mt5.sms_broadcast));
\echo Finish Table sms_broadcast 
\echo . 
\echo Loading Table sms_group 
\copy mt5.sms_group from '/usr1/dump-MT5/sms-group.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sms_group__recid_seq', (SELECT MAX(_recid) FROM mt5.sms_group));
\echo Finish Table sms_group 
\echo . 
\echo Loading Table sms_groupmbr 
\copy mt5.sms_groupmbr from '/usr1/dump-MT5/sms-groupmbr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sms_groupmbr__recid_seq', (SELECT MAX(_recid) FROM mt5.sms_groupmbr));
\echo Finish Table sms_groupmbr 
\echo . 
\echo Loading Table sms_received 
\copy mt5.sms_received from '/usr1/dump-MT5/sms-received.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sms_received__recid_seq', (SELECT MAX(_recid) FROM mt5.sms_received));
\echo Finish Table sms_received 
\echo . 
\echo Loading Table sourccod 
\copy mt5.sourccod from '/usr1/dump-MT5/Sourccod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sourccod__recid_seq', (SELECT MAX(_recid) FROM mt5.sourccod));
\echo Finish Table sourccod 
\echo . 
\echo Loading Table sources 
\copy mt5.sources from '/usr1/dump-MT5/sources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sources__recid_seq', (SELECT MAX(_recid) FROM mt5.sources));
\echo Finish Table sources 
\echo . 
\echo Loading Table sourcetext 
\copy mt5.sourcetext from '/usr1/dump-MT5/sourcetext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.sourcetext__recid_seq', (SELECT MAX(_recid) FROM mt5.sourcetext));
\echo Finish Table sourcetext 
\echo . 
\echo Loading Table telephone 
\copy mt5.telephone from '/usr1/dump-MT5/telephone.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.telephone__recid_seq', (SELECT MAX(_recid) FROM mt5.telephone));
\echo Finish Table telephone 
\echo . 
\echo Loading Table texte 
\copy mt5.texte from '/usr1/dump-MT5/texte.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.texte__recid_seq', (SELECT MAX(_recid) FROM mt5.texte));
\echo Finish Table texte 
\echo . 
\echo Loading Table tisch 
\copy mt5.tisch from '/usr1/dump-MT5/tisch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.tisch__recid_seq', (SELECT MAX(_recid) FROM mt5.tisch));
\echo Finish Table tisch 
\echo . 
\echo Loading Table tisch_res 
\copy mt5.tisch_res from '/usr1/dump-MT5/tisch-res.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.tisch_res__recid_seq', (SELECT MAX(_recid) FROM mt5.tisch_res));
\echo Finish Table tisch_res 
\echo . 
\echo Loading Table uebertrag 
\copy mt5.uebertrag from '/usr1/dump-MT5/uebertrag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.uebertrag__recid_seq', (SELECT MAX(_recid) FROM mt5.uebertrag));
\echo Finish Table uebertrag 
\echo . 
\echo Loading Table umsatz 
\copy mt5.umsatz from '/usr1/dump-MT5/umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.umsatz__recid_seq', (SELECT MAX(_recid) FROM mt5.umsatz));
\echo Finish Table umsatz 
\echo . 
\echo Loading Table waehrung 
\copy mt5.waehrung from '/usr1/dump-MT5/waehrung.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.waehrung__recid_seq', (SELECT MAX(_recid) FROM mt5.waehrung));
\echo Finish Table waehrung 
\echo . 
\echo Loading Table wakeup 
\copy mt5.wakeup from '/usr1/dump-MT5/wakeup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.wakeup__recid_seq', (SELECT MAX(_recid) FROM mt5.wakeup));
\echo Finish Table wakeup 
\echo . 
\echo Loading Table wgrpdep 
\copy mt5.wgrpdep from '/usr1/dump-MT5/wgrpdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.wgrpdep__recid_seq', (SELECT MAX(_recid) FROM mt5.wgrpdep));
\echo Finish Table wgrpdep 
\echo . 
\echo Loading Table wgrpgen 
\copy mt5.wgrpgen from '/usr1/dump-MT5/wgrpgen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.wgrpgen__recid_seq', (SELECT MAX(_recid) FROM mt5.wgrpgen));
\echo Finish Table wgrpgen 
\echo . 
\echo Loading Table zimkateg 
\copy mt5.zimkateg from '/usr1/dump-MT5/zimkateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zimkateg__recid_seq', (SELECT MAX(_recid) FROM mt5.zimkateg));
\echo Finish Table zimkateg 
\echo . 
\echo Loading Table zimmer 
\copy mt5.zimmer from '/usr1/dump-MT5/zimmer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zimmer__recid_seq', (SELECT MAX(_recid) FROM mt5.zimmer));
update mt5.zimmer set verbindung = array_replace(verbindung,NULL,''); 
\echo Finish Table zimmer 
\echo . 
\echo Loading Table zimmer_book 
\copy mt5.zimmer_book from '/usr1/dump-MT5/zimmer-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zimmer_book__recid_seq', (SELECT MAX(_recid) FROM mt5.zimmer_book));
\echo Finish Table zimmer_book 
\echo . 
\echo Loading Table zimmer_book_line 
\copy mt5.zimmer_book_line from '/usr1/dump-MT5/zimmer-book-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zimmer_book_line__recid_seq', (SELECT MAX(_recid) FROM mt5.zimmer_book_line));
\echo Finish Table zimmer_book_line 
\echo . 
\echo Loading Table zimplan 
\copy mt5.zimplan from '/usr1/dump-MT5/zimplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zimplan__recid_seq', (SELECT MAX(_recid) FROM mt5.zimplan));
\echo Finish Table zimplan 
\echo . 
\echo Loading Table zimpreis 
\copy mt5.zimpreis from '/usr1/dump-MT5/zimpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zimpreis__recid_seq', (SELECT MAX(_recid) FROM mt5.zimpreis));
\echo Finish Table zimpreis 
\echo . 
\echo Loading Table zinrstat 
\copy mt5.zinrstat from '/usr1/dump-MT5/zinrstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zinrstat__recid_seq', (SELECT MAX(_recid) FROM mt5.zinrstat));
\echo Finish Table zinrstat 
\echo . 
\echo Loading Table zkstat 
\copy mt5.zkstat from '/usr1/dump-MT5/zkstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zkstat__recid_seq', (SELECT MAX(_recid) FROM mt5.zkstat));
\echo Finish Table zkstat 
\echo . 
\echo Loading Table zwkum 
\copy mt5.zwkum from '/usr1/dump-MT5/zwkum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('mt5.zwkum__recid_seq', (SELECT MAX(_recid) FROM mt5.zwkum));
\echo Finish Table zwkum 
\echo . 
