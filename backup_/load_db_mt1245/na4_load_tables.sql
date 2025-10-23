\echo Loading Table absen 
\copy na4.absen from '/usr1/dump-MT1/CSV/absen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.absen__recid_seq', (SELECT MAX(_recid) FROM na4.absen));
\echo Finish Table absen 
\echo . 
\echo Loading Table akt_code 
\copy na4.akt_code from '/usr1/dump-MT1/CSV/akt-code.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.akt_code__recid_seq', (SELECT MAX(_recid) FROM na4.akt_code));
\echo Finish Table akt_code 
\echo . 
\echo Loading Table akt_cust 
\copy na4.akt_cust from '/usr1/dump-MT1/CSV/akt-cust.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.akt_cust__recid_seq', (SELECT MAX(_recid) FROM na4.akt_cust));
\echo Finish Table akt_cust 
\echo . 
\echo Loading Table akt_kont 
\copy na4.akt_kont from '/usr1/dump-MT1/CSV/akt-kont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.akt_kont__recid_seq', (SELECT MAX(_recid) FROM na4.akt_kont));
\echo Finish Table akt_kont 
\echo . 
\echo Loading Table akt_line 
\copy na4.akt_line from '/usr1/dump-MT1/CSV/akt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.akt_line__recid_seq', (SELECT MAX(_recid) FROM na4.akt_line));
\echo Finish Table akt_line 
\echo . 
\echo Loading Table akthdr 
\copy na4.akthdr from '/usr1/dump-MT1/CSV/akthdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.akthdr__recid_seq', (SELECT MAX(_recid) FROM na4.akthdr));
\echo Finish Table akthdr 
\echo . 
\echo Loading Table aktion 
\copy na4.aktion from '/usr1/dump-MT1/CSV/aktion.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.aktion__recid_seq', (SELECT MAX(_recid) FROM na4.aktion));
update na4.aktion set texte = array_replace(texte,NULL,''); 
\echo Finish Table aktion 
\echo . 
\echo Loading Table ap_journal 
\copy na4.ap_journal from '/usr1/dump-MT1/CSV/ap-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.ap_journal__recid_seq', (SELECT MAX(_recid) FROM na4.ap_journal));
\echo Finish Table ap_journal 
\echo . 
\echo Loading Table apt_bill 
\copy na4.apt_bill from '/usr1/dump-MT1/CSV/apt-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.apt_bill__recid_seq', (SELECT MAX(_recid) FROM na4.apt_bill));
update na4.apt_bill set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table apt_bill 
\echo . 
\echo Loading Table archieve 
\copy na4.archieve from '/usr1/dump-MT1/CSV/archieve.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.archieve__recid_seq', (SELECT MAX(_recid) FROM na4.archieve));
update na4.archieve set char = array_replace(char,NULL,''); 
\echo Finish Table archieve 
\echo . 
\echo Loading Table argt_line 
\copy na4.argt_line from '/usr1/dump-MT1/CSV/argt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.argt_line__recid_seq', (SELECT MAX(_recid) FROM na4.argt_line));
\echo Finish Table argt_line 
\echo . 
\echo Loading Table argtcost 
\copy na4.argtcost from '/usr1/dump-MT1/CSV/argtcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.argtcost__recid_seq', (SELECT MAX(_recid) FROM na4.argtcost));
update na4.argtcost set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtcost 
\echo . 
\echo Loading Table argtstat 
\copy na4.argtstat from '/usr1/dump-MT1/CSV/argtstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.argtstat__recid_seq', (SELECT MAX(_recid) FROM na4.argtstat));
update na4.argtstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtstat 
\echo . 
\echo Loading Table arrangement 
\copy na4.arrangement from '/usr1/dump-MT1/CSV/arrangement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.arrangement__recid_seq', (SELECT MAX(_recid) FROM na4.arrangement));
update na4.arrangement set argt_rgbez2 = array_replace(argt_rgbez2,NULL,''); 
\echo Finish Table arrangement 
\echo . 
\echo Loading Table artikel 
\copy na4.artikel from '/usr1/dump-MT1/CSV/artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.artikel__recid_seq', (SELECT MAX(_recid) FROM na4.artikel));
\echo Finish Table artikel 
\echo . 
\echo Loading Table artprice 
\copy na4.artprice from '/usr1/dump-MT1/CSV/artprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.artprice__recid_seq', (SELECT MAX(_recid) FROM na4.artprice));
\echo Finish Table artprice 
\echo . 
\echo Loading Table b_history 
\copy na4.b_history from '/usr1/dump-MT1/CSV/b-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.b_history__recid_seq', (SELECT MAX(_recid) FROM na4.b_history));
update na4.b_history set anlass = array_replace(anlass,NULL,''); 
update na4.b_history set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update na4.b_history set ape__speisen = array_replace(ape__speisen,NULL,''); 
update na4.b_history set arrival = array_replace(arrival,NULL,''); 
update na4.b_history set c_resstatus = array_replace(c_resstatus,NULL,''); 
update na4.b_history set dance = array_replace(dance,NULL,''); 
update na4.b_history set deko2 = array_replace(deko2,NULL,''); 
update na4.b_history set dekoration = array_replace(dekoration,NULL,''); 
update na4.b_history set digestif = array_replace(digestif,NULL,''); 
update na4.b_history set dinner = array_replace(dinner,NULL,''); 
update na4.b_history set f_menu = array_replace(f_menu,NULL,''); 
update na4.b_history set f_no = array_replace(f_no,NULL,''); 
update na4.b_history set fotograf = array_replace(fotograf,NULL,''); 
update na4.b_history set gaestebuch = array_replace(gaestebuch,NULL,''); 
update na4.b_history set garderobe = array_replace(garderobe,NULL,''); 
update na4.b_history set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update na4.b_history set kaffee = array_replace(kaffee,NULL,''); 
update na4.b_history set kartentext = array_replace(kartentext,NULL,''); 
update na4.b_history set kontaktperson = array_replace(kontaktperson,NULL,''); 
update na4.b_history set kuenstler = array_replace(kuenstler,NULL,''); 
update na4.b_history set menue = array_replace(menue,NULL,''); 
update na4.b_history set menuekarten = array_replace(menuekarten,NULL,''); 
update na4.b_history set musik = array_replace(musik,NULL,''); 
update na4.b_history set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update na4.b_history set nadkarte = array_replace(nadkarte,NULL,''); 
update na4.b_history set ndessen = array_replace(ndessen,NULL,''); 
update na4.b_history set payment_userinit = array_replace(payment_userinit,NULL,''); 
update na4.b_history set personen2 = array_replace(personen2,NULL,''); 
update na4.b_history set raeume = array_replace(raeume,NULL,''); 
update na4.b_history set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update na4.b_history set raummiete = array_replace(raummiete,NULL,''); 
update na4.b_history set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update na4.b_history set service = array_replace(service,NULL,''); 
update na4.b_history set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update na4.b_history set sonstiges = array_replace(sonstiges,NULL,''); 
update na4.b_history set technik = array_replace(technik,NULL,''); 
update na4.b_history set tischform = array_replace(tischform,NULL,''); 
update na4.b_history set tischordnung = array_replace(tischordnung,NULL,''); 
update na4.b_history set tischplan = array_replace(tischplan,NULL,''); 
update na4.b_history set tischreden = array_replace(tischreden,NULL,''); 
update na4.b_history set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update na4.b_history set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update na4.b_history set va_ablauf = array_replace(va_ablauf,NULL,''); 
update na4.b_history set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update na4.b_history set vip = array_replace(vip,NULL,''); 
update na4.b_history set weine = array_replace(weine,NULL,''); 
update na4.b_history set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table b_history 
\echo . 
\echo Loading Table b_oorder 
\copy na4.b_oorder from '/usr1/dump-MT1/CSV/b-oorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.b_oorder__recid_seq', (SELECT MAX(_recid) FROM na4.b_oorder));
\echo Finish Table b_oorder 
\echo . 
\echo Loading Table b_storno 
\copy na4.b_storno from '/usr1/dump-MT1/CSV/b-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.b_storno__recid_seq', (SELECT MAX(_recid) FROM na4.b_storno));
update na4.b_storno set grund = array_replace(grund,NULL,''); 
\echo Finish Table b_storno 
\echo . 
\echo Loading Table ba_rset 
\copy na4.ba_rset from '/usr1/dump-MT1/CSV/ba-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.ba_rset__recid_seq', (SELECT MAX(_recid) FROM na4.ba_rset));
\echo Finish Table ba_rset 
\echo . 
\echo Loading Table ba_setup 
\copy na4.ba_setup from '/usr1/dump-MT1/CSV/ba-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.ba_setup__recid_seq', (SELECT MAX(_recid) FROM na4.ba_setup));
\echo Finish Table ba_setup 
\echo . 
\echo Loading Table ba_typ 
\copy na4.ba_typ from '/usr1/dump-MT1/CSV/ba-typ.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.ba_typ__recid_seq', (SELECT MAX(_recid) FROM na4.ba_typ));
\echo Finish Table ba_typ 
\echo . 
\echo Loading Table bankrep 
\copy na4.bankrep from '/usr1/dump-MT1/CSV/bankrep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bankrep__recid_seq', (SELECT MAX(_recid) FROM na4.bankrep));
update na4.bankrep set anlass = array_replace(anlass,NULL,''); 
update na4.bankrep set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update na4.bankrep set ape__speisen = array_replace(ape__speisen,NULL,''); 
update na4.bankrep set dekoration = array_replace(dekoration,NULL,''); 
update na4.bankrep set digestif = array_replace(digestif,NULL,''); 
update na4.bankrep set fotograf = array_replace(fotograf,NULL,''); 
update na4.bankrep set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update na4.bankrep set kartentext = array_replace(kartentext,NULL,''); 
update na4.bankrep set kontaktperson = array_replace(kontaktperson,NULL,''); 
update na4.bankrep set menue = array_replace(menue,NULL,''); 
update na4.bankrep set menuekarten = array_replace(menuekarten,NULL,''); 
update na4.bankrep set musik = array_replace(musik,NULL,''); 
update na4.bankrep set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update na4.bankrep set ndessen = array_replace(ndessen,NULL,''); 
update na4.bankrep set personen2 = array_replace(personen2,NULL,''); 
update na4.bankrep set raeume = array_replace(raeume,NULL,''); 
update na4.bankrep set raummiete = array_replace(raummiete,NULL,''); 
update na4.bankrep set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update na4.bankrep set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update na4.bankrep set sonstiges = array_replace(sonstiges,NULL,''); 
update na4.bankrep set technik = array_replace(technik,NULL,''); 
update na4.bankrep set tischform = array_replace(tischform,NULL,''); 
update na4.bankrep set tischreden = array_replace(tischreden,NULL,''); 
update na4.bankrep set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update na4.bankrep set weine = array_replace(weine,NULL,''); 
update na4.bankrep set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bankrep 
\echo . 
\echo Loading Table bankres 
\copy na4.bankres from '/usr1/dump-MT1/CSV/bankres.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bankres__recid_seq', (SELECT MAX(_recid) FROM na4.bankres));
update na4.bankres set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table bankres 
\echo . 
\echo Loading Table bediener 
\copy na4.bediener from '/usr1/dump-MT1/CSV/bediener.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bediener__recid_seq', (SELECT MAX(_recid) FROM na4.bediener));
\echo Finish Table bediener 
\echo . 
\echo Loading Table bill 
\copy na4.bill from '/usr1/dump-MT1/CSV/bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bill__recid_seq', (SELECT MAX(_recid) FROM na4.bill));
\echo Finish Table bill 
\echo . 
\echo Loading Table bill_lin_tax 
\copy na4.bill_lin_tax from '/usr1/dump-MT1/CSV/bill-lin-tax.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bill_lin_tax__recid_seq', (SELECT MAX(_recid) FROM na4.bill_lin_tax));
\echo Finish Table bill_lin_tax 
\echo . 
\echo Loading Table bill_line 
\copy na4.bill_line from '/usr1/dump-MT1/CSV/bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bill_line__recid_seq', (SELECT MAX(_recid) FROM na4.bill_line));
\echo Finish Table bill_line 
\echo . 
\echo Loading Table billhis 
\copy na4.billhis from '/usr1/dump-MT1/CSV/billhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.billhis__recid_seq', (SELECT MAX(_recid) FROM na4.billhis));
\echo Finish Table billhis 
\echo . 
\echo Loading Table billjournal 
\copy na4.billjournal from '/usr1/dump-MT1/CSV/billjournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.billjournal__recid_seq', (SELECT MAX(_recid) FROM na4.billjournal));
\echo Finish Table billjournal 
\echo . 
\echo Loading Table bk_beleg 
\copy na4.bk_beleg from '/usr1/dump-MT1/CSV/bk-beleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_beleg__recid_seq', (SELECT MAX(_recid) FROM na4.bk_beleg));
\echo Finish Table bk_beleg 
\echo . 
\echo Loading Table bk_fsdef 
\copy na4.bk_fsdef from '/usr1/dump-MT1/CSV/bk-fsdef.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_fsdef__recid_seq', (SELECT MAX(_recid) FROM na4.bk_fsdef));
\echo Finish Table bk_fsdef 
\echo . 
\echo Loading Table bk_func 
\copy na4.bk_func from '/usr1/dump-MT1/CSV/bk-func.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_func__recid_seq', (SELECT MAX(_recid) FROM na4.bk_func));
update na4.bk_func set anlass = array_replace(anlass,NULL,''); 
update na4.bk_func set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update na4.bk_func set ape__speisen = array_replace(ape__speisen,NULL,''); 
update na4.bk_func set arrival = array_replace(arrival,NULL,''); 
update na4.bk_func set c_resstatus = array_replace(c_resstatus,NULL,''); 
update na4.bk_func set dance = array_replace(dance,NULL,''); 
update na4.bk_func set deko2 = array_replace(deko2,NULL,''); 
update na4.bk_func set dekoration = array_replace(dekoration,NULL,''); 
update na4.bk_func set digestif = array_replace(digestif,NULL,''); 
update na4.bk_func set dinner = array_replace(dinner,NULL,''); 
update na4.bk_func set f_menu = array_replace(f_menu,NULL,''); 
update na4.bk_func set f_no = array_replace(f_no,NULL,''); 
update na4.bk_func set fotograf = array_replace(fotograf,NULL,''); 
update na4.bk_func set gaestebuch = array_replace(gaestebuch,NULL,''); 
update na4.bk_func set garderobe = array_replace(garderobe,NULL,''); 
update na4.bk_func set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update na4.bk_func set kaffee = array_replace(kaffee,NULL,''); 
update na4.bk_func set kartentext = array_replace(kartentext,NULL,''); 
update na4.bk_func set kontaktperson = array_replace(kontaktperson,NULL,''); 
update na4.bk_func set kuenstler = array_replace(kuenstler,NULL,''); 
update na4.bk_func set menue = array_replace(menue,NULL,''); 
update na4.bk_func set menuekarten = array_replace(menuekarten,NULL,''); 
update na4.bk_func set musik = array_replace(musik,NULL,''); 
update na4.bk_func set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update na4.bk_func set nadkarte = array_replace(nadkarte,NULL,''); 
update na4.bk_func set ndessen = array_replace(ndessen,NULL,''); 
update na4.bk_func set personen2 = array_replace(personen2,NULL,''); 
update na4.bk_func set raeume = array_replace(raeume,NULL,''); 
update na4.bk_func set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update na4.bk_func set raummiete = array_replace(raummiete,NULL,''); 
update na4.bk_func set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update na4.bk_func set service = array_replace(service,NULL,''); 
update na4.bk_func set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update na4.bk_func set sonstiges = array_replace(sonstiges,NULL,''); 
update na4.bk_func set technik = array_replace(technik,NULL,''); 
update na4.bk_func set tischform = array_replace(tischform,NULL,''); 
update na4.bk_func set tischordnung = array_replace(tischordnung,NULL,''); 
update na4.bk_func set tischplan = array_replace(tischplan,NULL,''); 
update na4.bk_func set tischreden = array_replace(tischreden,NULL,''); 
update na4.bk_func set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update na4.bk_func set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update na4.bk_func set va_ablauf = array_replace(va_ablauf,NULL,''); 
update na4.bk_func set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update na4.bk_func set vip = array_replace(vip,NULL,''); 
update na4.bk_func set weine = array_replace(weine,NULL,''); 
update na4.bk_func set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bk_func 
\echo . 
\echo Loading Table bk_package 
\copy na4.bk_package from '/usr1/dump-MT1/CSV/bk-package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_package__recid_seq', (SELECT MAX(_recid) FROM na4.bk_package));
\echo Finish Table bk_package 
\echo . 
\echo Loading Table bk_pause 
\copy na4.bk_pause from '/usr1/dump-MT1/CSV/bk-pause.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_pause__recid_seq', (SELECT MAX(_recid) FROM na4.bk_pause));
\echo Finish Table bk_pause 
\echo . 
\echo Loading Table bk_rart 
\copy na4.bk_rart from '/usr1/dump-MT1/CSV/bk-rart.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_rart__recid_seq', (SELECT MAX(_recid) FROM na4.bk_rart));
\echo Finish Table bk_rart 
\echo . 
\echo Loading Table bk_raum 
\copy na4.bk_raum from '/usr1/dump-MT1/CSV/bk-raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_raum__recid_seq', (SELECT MAX(_recid) FROM na4.bk_raum));
\echo Finish Table bk_raum 
\echo . 
\echo Loading Table bk_reser 
\copy na4.bk_reser from '/usr1/dump-MT1/CSV/bk-reser.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_reser__recid_seq', (SELECT MAX(_recid) FROM na4.bk_reser));
\echo Finish Table bk_reser 
\echo . 
\echo Loading Table bk_rset 
\copy na4.bk_rset from '/usr1/dump-MT1/CSV/bk-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_rset__recid_seq', (SELECT MAX(_recid) FROM na4.bk_rset));
\echo Finish Table bk_rset 
\echo . 
\echo Loading Table bk_setup 
\copy na4.bk_setup from '/usr1/dump-MT1/CSV/bk-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_setup__recid_seq', (SELECT MAX(_recid) FROM na4.bk_setup));
\echo Finish Table bk_setup 
\echo . 
\echo Loading Table bk_stat 
\copy na4.bk_stat from '/usr1/dump-MT1/CSV/bk-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_stat__recid_seq', (SELECT MAX(_recid) FROM na4.bk_stat));
\echo Finish Table bk_stat 
\echo . 
\echo Loading Table bk_veran 
\copy na4.bk_veran from '/usr1/dump-MT1/CSV/bk-veran.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bk_veran__recid_seq', (SELECT MAX(_recid) FROM na4.bk_veran));
update na4.bk_veran set payment_userinit = array_replace(payment_userinit,NULL,''); 
\echo Finish Table bk_veran 
\echo . 
\echo Loading Table bl_dates 
\copy na4.bl_dates from '/usr1/dump-MT1/CSV/bl-dates.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bl_dates__recid_seq', (SELECT MAX(_recid) FROM na4.bl_dates));
\echo Finish Table bl_dates 
\echo . 
\echo Loading Table blinehis 
\copy na4.blinehis from '/usr1/dump-MT1/CSV/blinehis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.blinehis__recid_seq', (SELECT MAX(_recid) FROM na4.blinehis));
\echo Finish Table blinehis 
\echo . 
\echo Loading Table bresline 
\copy na4.bresline from '/usr1/dump-MT1/CSV/bresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.bresline__recid_seq', (SELECT MAX(_recid) FROM na4.bresline));
update na4.bresline set texte = array_replace(texte,NULL,''); 
\echo Finish Table bresline 
\echo . 
\echo Loading Table brief 
\copy na4.brief from '/usr1/dump-MT1/CSV/brief.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.brief__recid_seq', (SELECT MAX(_recid) FROM na4.brief));
\echo Finish Table brief 
\echo . 
\echo Loading Table brieftmp 
\copy na4.brieftmp from '/usr1/dump-MT1/CSV/brieftmp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.brieftmp__recid_seq', (SELECT MAX(_recid) FROM na4.brieftmp));
\echo Finish Table brieftmp 
\echo . 
\echo Loading Table briefzei 
\copy na4.briefzei from '/usr1/dump-MT1/CSV/briefzei.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.briefzei__recid_seq', (SELECT MAX(_recid) FROM na4.briefzei));
\echo Finish Table briefzei 
\echo . 
\echo Loading Table budget 
\copy na4.budget from '/usr1/dump-MT1/CSV/budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.budget__recid_seq', (SELECT MAX(_recid) FROM na4.budget));
\echo Finish Table budget 
\echo . 
\echo Loading Table calls 
\copy na4.calls from '/usr1/dump-MT1/CSV/calls.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.calls__recid_seq', (SELECT MAX(_recid) FROM na4.calls));
\echo Finish Table calls 
\echo . 
\echo Loading Table cl_bonus 
\copy na4.cl_bonus from '/usr1/dump-MT1/CSV/cl-bonus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_bonus__recid_seq', (SELECT MAX(_recid) FROM na4.cl_bonus));
\echo Finish Table cl_bonus 
\echo . 
\echo Loading Table cl_book 
\copy na4.cl_book from '/usr1/dump-MT1/CSV/cl-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_book__recid_seq', (SELECT MAX(_recid) FROM na4.cl_book));
\echo Finish Table cl_book 
\echo . 
\echo Loading Table cl_checkin 
\copy na4.cl_checkin from '/usr1/dump-MT1/CSV/cl-checkin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_checkin__recid_seq', (SELECT MAX(_recid) FROM na4.cl_checkin));
\echo Finish Table cl_checkin 
\echo . 
\echo Loading Table cl_class 
\copy na4.cl_class from '/usr1/dump-MT1/CSV/cl-class.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_class__recid_seq', (SELECT MAX(_recid) FROM na4.cl_class));
\echo Finish Table cl_class 
\echo . 
\echo Loading Table cl_enroll 
\copy na4.cl_enroll from '/usr1/dump-MT1/CSV/cl-enroll.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_enroll__recid_seq', (SELECT MAX(_recid) FROM na4.cl_enroll));
\echo Finish Table cl_enroll 
\echo . 
\echo Loading Table cl_free 
\copy na4.cl_free from '/usr1/dump-MT1/CSV/cl-free.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_free__recid_seq', (SELECT MAX(_recid) FROM na4.cl_free));
\echo Finish Table cl_free 
\echo . 
\echo Loading Table cl_histci 
\copy na4.cl_histci from '/usr1/dump-MT1/CSV/cl-histci.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_histci__recid_seq', (SELECT MAX(_recid) FROM na4.cl_histci));
\echo Finish Table cl_histci 
\echo . 
\echo Loading Table cl_histpay 
\copy na4.cl_histpay from '/usr1/dump-MT1/CSV/cl-histpay.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_histpay__recid_seq', (SELECT MAX(_recid) FROM na4.cl_histpay));
\echo Finish Table cl_histpay 
\echo . 
\echo Loading Table cl_histstatus 
\copy na4.cl_histstatus from '/usr1/dump-MT1/CSV/cl-histstatus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_histstatus__recid_seq', (SELECT MAX(_recid) FROM na4.cl_histstatus));
\echo Finish Table cl_histstatus 
\echo . 
\echo Loading Table cl_histtrain 
\copy na4.cl_histtrain from '/usr1/dump-MT1/CSV/cl-histtrain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_histtrain__recid_seq', (SELECT MAX(_recid) FROM na4.cl_histtrain));
\echo Finish Table cl_histtrain 
\echo . 
\echo Loading Table cl_histvisit 
\copy na4.cl_histvisit from '/usr1/dump-MT1/CSV/cl-histvisit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_histvisit__recid_seq', (SELECT MAX(_recid) FROM na4.cl_histvisit));
\echo Finish Table cl_histvisit 
\echo . 
\echo Loading Table cl_home 
\copy na4.cl_home from '/usr1/dump-MT1/CSV/cl-home.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_home__recid_seq', (SELECT MAX(_recid) FROM na4.cl_home));
\echo Finish Table cl_home 
\echo . 
\echo Loading Table cl_location 
\copy na4.cl_location from '/usr1/dump-MT1/CSV/cl-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_location__recid_seq', (SELECT MAX(_recid) FROM na4.cl_location));
\echo Finish Table cl_location 
\echo . 
\echo Loading Table cl_locker 
\copy na4.cl_locker from '/usr1/dump-MT1/CSV/cl-locker.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_locker__recid_seq', (SELECT MAX(_recid) FROM na4.cl_locker));
\echo Finish Table cl_locker 
\echo . 
\echo Loading Table cl_log 
\copy na4.cl_log from '/usr1/dump-MT1/CSV/cl-log.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_log__recid_seq', (SELECT MAX(_recid) FROM na4.cl_log));
\echo Finish Table cl_log 
\echo . 
\echo Loading Table cl_member 
\copy na4.cl_member from '/usr1/dump-MT1/CSV/cl-member.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_member__recid_seq', (SELECT MAX(_recid) FROM na4.cl_member));
\echo Finish Table cl_member 
\echo . 
\echo Loading Table cl_memtype 
\copy na4.cl_memtype from '/usr1/dump-MT1/CSV/cl-memtype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_memtype__recid_seq', (SELECT MAX(_recid) FROM na4.cl_memtype));
\echo Finish Table cl_memtype 
\echo . 
\echo Loading Table cl_paysched 
\copy na4.cl_paysched from '/usr1/dump-MT1/CSV/cl-paysched.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_paysched__recid_seq', (SELECT MAX(_recid) FROM na4.cl_paysched));
\echo Finish Table cl_paysched 
\echo . 
\echo Loading Table cl_stat 
\copy na4.cl_stat from '/usr1/dump-MT1/CSV/cl-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_stat__recid_seq', (SELECT MAX(_recid) FROM na4.cl_stat));
\echo Finish Table cl_stat 
\echo . 
\echo Loading Table cl_stat1 
\copy na4.cl_stat1 from '/usr1/dump-MT1/CSV/cl-stat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_stat1__recid_seq', (SELECT MAX(_recid) FROM na4.cl_stat1));
\echo Finish Table cl_stat1 
\echo . 
\echo Loading Table cl_towel 
\copy na4.cl_towel from '/usr1/dump-MT1/CSV/cl-towel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_towel__recid_seq', (SELECT MAX(_recid) FROM na4.cl_towel));
\echo Finish Table cl_towel 
\echo . 
\echo Loading Table cl_trainer 
\copy na4.cl_trainer from '/usr1/dump-MT1/CSV/cl-trainer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_trainer__recid_seq', (SELECT MAX(_recid) FROM na4.cl_trainer));
\echo Finish Table cl_trainer 
\echo . 
\echo Loading Table cl_upgrade 
\copy na4.cl_upgrade from '/usr1/dump-MT1/CSV/cl-upgrade.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cl_upgrade__recid_seq', (SELECT MAX(_recid) FROM na4.cl_upgrade));
\echo Finish Table cl_upgrade 
\echo . 
\echo Loading Table costbudget 
\copy na4.costbudget from '/usr1/dump-MT1/CSV/costbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.costbudget__recid_seq', (SELECT MAX(_recid) FROM na4.costbudget));
\echo Finish Table costbudget 
\echo . 
\echo Loading Table counters 
\copy na4.counters from '/usr1/dump-MT1/CSV/counters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.counters__recid_seq', (SELECT MAX(_recid) FROM na4.counters));
\echo Finish Table counters 
\echo . 
\echo Loading Table crm_campaign 
\copy na4.crm_campaign from '/usr1/dump-MT1/CSV/crm-campaign.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_campaign__recid_seq', (SELECT MAX(_recid) FROM na4.crm_campaign));
\echo Finish Table crm_campaign 
\echo . 
\echo Loading Table crm_category 
\copy na4.crm_category from '/usr1/dump-MT1/CSV/crm-category.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_category__recid_seq', (SELECT MAX(_recid) FROM na4.crm_category));
\echo Finish Table crm_category 
\echo . 
\echo Loading Table crm_dept 
\copy na4.crm_dept from '/usr1/dump-MT1/CSV/crm-dept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_dept__recid_seq', (SELECT MAX(_recid) FROM na4.crm_dept));
\echo Finish Table crm_dept 
\echo . 
\echo Loading Table crm_dtl 
\copy na4.crm_dtl from '/usr1/dump-MT1/CSV/crm-dtl.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_dtl__recid_seq', (SELECT MAX(_recid) FROM na4.crm_dtl));
\echo Finish Table crm_dtl 
\echo . 
\echo Loading Table crm_email 
\copy na4.crm_email from '/usr1/dump-MT1/CSV/crm-email.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_email__recid_seq', (SELECT MAX(_recid) FROM na4.crm_email));
\echo Finish Table crm_email 
\echo . 
\echo Loading Table crm_event 
\copy na4.crm_event from '/usr1/dump-MT1/CSV/crm-event.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_event__recid_seq', (SELECT MAX(_recid) FROM na4.crm_event));
\echo Finish Table crm_event 
\echo . 
\echo Loading Table crm_feedhdr 
\copy na4.crm_feedhdr from '/usr1/dump-MT1/CSV/crm-feedhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_feedhdr__recid_seq', (SELECT MAX(_recid) FROM na4.crm_feedhdr));
\echo Finish Table crm_feedhdr 
\echo . 
\echo Loading Table crm_fnlresult 
\copy na4.crm_fnlresult from '/usr1/dump-MT1/CSV/crm-fnlresult.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_fnlresult__recid_seq', (SELECT MAX(_recid) FROM na4.crm_fnlresult));
\echo Finish Table crm_fnlresult 
\echo . 
\echo Loading Table crm_language 
\copy na4.crm_language from '/usr1/dump-MT1/CSV/crm-language.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_language__recid_seq', (SELECT MAX(_recid) FROM na4.crm_language));
\echo Finish Table crm_language 
\echo . 
\echo Loading Table crm_question 
\copy na4.crm_question from '/usr1/dump-MT1/CSV/crm-question.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_question__recid_seq', (SELECT MAX(_recid) FROM na4.crm_question));
\echo Finish Table crm_question 
\echo . 
\echo Loading Table crm_tamplang 
\copy na4.crm_tamplang from '/usr1/dump-MT1/CSV/crm-tamplang.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_tamplang__recid_seq', (SELECT MAX(_recid) FROM na4.crm_tamplang));
\echo Finish Table crm_tamplang 
\echo . 
\echo Loading Table crm_template 
\copy na4.crm_template from '/usr1/dump-MT1/CSV/crm-template.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.crm_template__recid_seq', (SELECT MAX(_recid) FROM na4.crm_template));
\echo Finish Table crm_template 
\echo . 
\echo Loading Table cross_dtl 
\copy na4.cross_dtl from '/usr1/dump-MT1/CSV/cross-DTL.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cross_dtl__recid_seq', (SELECT MAX(_recid) FROM na4.cross_dtl));
\echo Finish Table cross_dtl 
\echo . 
\echo Loading Table cross_hdr 
\copy na4.cross_hdr from '/usr1/dump-MT1/CSV/cross-HDR.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.cross_hdr__recid_seq', (SELECT MAX(_recid) FROM na4.cross_hdr));
\echo Finish Table cross_hdr 
\echo . 
\echo Loading Table debitor 
\copy na4.debitor from '/usr1/dump-MT1/CSV/debitor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.debitor__recid_seq', (SELECT MAX(_recid) FROM na4.debitor));
\echo Finish Table debitor 
\echo . 
\echo Loading Table debthis 
\copy na4.debthis from '/usr1/dump-MT1/CSV/debthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.debthis__recid_seq', (SELECT MAX(_recid) FROM na4.debthis));
\echo Finish Table debthis 
\echo . 
\echo Loading Table desttext 
\copy na4.desttext from '/usr1/dump-MT1/CSV/desttext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.desttext__recid_seq', (SELECT MAX(_recid) FROM na4.desttext));
\echo Finish Table desttext 
\echo . 
\echo Loading Table dml_art 
\copy na4.dml_art from '/usr1/dump-MT1/CSV/dml-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.dml_art__recid_seq', (SELECT MAX(_recid) FROM na4.dml_art));
\echo Finish Table dml_art 
\echo . 
\echo Loading Table dml_artdep 
\copy na4.dml_artdep from '/usr1/dump-MT1/CSV/dml-artdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.dml_artdep__recid_seq', (SELECT MAX(_recid) FROM na4.dml_artdep));
\echo Finish Table dml_artdep 
\echo . 
\echo Loading Table dml_rate 
\copy na4.dml_rate from '/usr1/dump-MT1/CSV/dml-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.dml_rate__recid_seq', (SELECT MAX(_recid) FROM na4.dml_rate));
\echo Finish Table dml_rate 
\echo . 
\echo Loading Table eg_action 
\copy na4.eg_action from '/usr1/dump-MT1/CSV/eg-action.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_action__recid_seq', (SELECT MAX(_recid) FROM na4.eg_action));
\echo Finish Table eg_action 
\echo . 
\echo Loading Table eg_alert 
\copy na4.eg_alert from '/usr1/dump-MT1/CSV/eg-Alert.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_alert__recid_seq', (SELECT MAX(_recid) FROM na4.eg_alert));
\echo Finish Table eg_alert 
\echo . 
\echo Loading Table eg_budget 
\copy na4.eg_budget from '/usr1/dump-MT1/CSV/eg-budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_budget__recid_seq', (SELECT MAX(_recid) FROM na4.eg_budget));
\echo Finish Table eg_budget 
\echo . 
\echo Loading Table eg_cost 
\copy na4.eg_cost from '/usr1/dump-MT1/CSV/eg-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_cost__recid_seq', (SELECT MAX(_recid) FROM na4.eg_cost));
\echo Finish Table eg_cost 
\echo . 
\echo Loading Table eg_duration 
\copy na4.eg_duration from '/usr1/dump-MT1/CSV/eg-Duration.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_duration__recid_seq', (SELECT MAX(_recid) FROM na4.eg_duration));
\echo Finish Table eg_duration 
\echo . 
\echo Loading Table eg_location 
\copy na4.eg_location from '/usr1/dump-MT1/CSV/eg-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_location__recid_seq', (SELECT MAX(_recid) FROM na4.eg_location));
\echo Finish Table eg_location 
\echo . 
\echo Loading Table eg_mainstat 
\copy na4.eg_mainstat from '/usr1/dump-MT1/CSV/eg-MainStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_mainstat__recid_seq', (SELECT MAX(_recid) FROM na4.eg_mainstat));
\echo Finish Table eg_mainstat 
\echo . 
\echo Loading Table eg_maintain 
\copy na4.eg_maintain from '/usr1/dump-MT1/CSV/eg-maintain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_maintain__recid_seq', (SELECT MAX(_recid) FROM na4.eg_maintain));
\echo Finish Table eg_maintain 
\echo . 
\echo Loading Table eg_mdetail 
\copy na4.eg_mdetail from '/usr1/dump-MT1/CSV/eg-mdetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_mdetail__recid_seq', (SELECT MAX(_recid) FROM na4.eg_mdetail));
\echo Finish Table eg_mdetail 
\echo . 
\echo Loading Table eg_messageno 
\copy na4.eg_messageno from '/usr1/dump-MT1/CSV/eg-MessageNo.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_messageno__recid_seq', (SELECT MAX(_recid) FROM na4.eg_messageno));
\echo Finish Table eg_messageno 
\echo . 
\echo Loading Table eg_mobilenr 
\copy na4.eg_mobilenr from '/usr1/dump-MT1/CSV/eg-mobileNr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_mobilenr__recid_seq', (SELECT MAX(_recid) FROM na4.eg_mobilenr));
\echo Finish Table eg_mobilenr 
\echo . 
\echo Loading Table eg_moveproperty 
\copy na4.eg_moveproperty from '/usr1/dump-MT1/CSV/eg-moveProperty.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_moveproperty__recid_seq', (SELECT MAX(_recid) FROM na4.eg_moveproperty));
\echo Finish Table eg_moveproperty 
\echo . 
\echo Loading Table eg_property 
\copy na4.eg_property from '/usr1/dump-MT1/CSV/eg-property.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_property__recid_seq', (SELECT MAX(_recid) FROM na4.eg_property));
\echo Finish Table eg_property 
\echo . 
\echo Loading Table eg_propmeter 
\copy na4.eg_propmeter from '/usr1/dump-MT1/CSV/eg-propMeter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_propmeter__recid_seq', (SELECT MAX(_recid) FROM na4.eg_propmeter));
\echo Finish Table eg_propmeter 
\echo . 
\echo Loading Table eg_queasy 
\copy na4.eg_queasy from '/usr1/dump-MT1/CSV/eg-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_queasy__recid_seq', (SELECT MAX(_recid) FROM na4.eg_queasy));
\echo Finish Table eg_queasy 
\echo . 
\echo Loading Table eg_reqdetail 
\copy na4.eg_reqdetail from '/usr1/dump-MT1/CSV/eg-reqDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_reqdetail__recid_seq', (SELECT MAX(_recid) FROM na4.eg_reqdetail));
\echo Finish Table eg_reqdetail 
\echo . 
\echo Loading Table eg_reqif 
\copy na4.eg_reqif from '/usr1/dump-MT1/CSV/eg-reqif.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_reqif__recid_seq', (SELECT MAX(_recid) FROM na4.eg_reqif));
\echo Finish Table eg_reqif 
\echo . 
\echo Loading Table eg_reqstat 
\copy na4.eg_reqstat from '/usr1/dump-MT1/CSV/eg-ReqStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_reqstat__recid_seq', (SELECT MAX(_recid) FROM na4.eg_reqstat));
\echo Finish Table eg_reqstat 
\echo . 
\echo Loading Table eg_request 
\copy na4.eg_request from '/usr1/dump-MT1/CSV/eg-request.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_request__recid_seq', (SELECT MAX(_recid) FROM na4.eg_request));
\echo Finish Table eg_request 
\echo . 
\echo Loading Table eg_resources 
\copy na4.eg_resources from '/usr1/dump-MT1/CSV/eg-resources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_resources__recid_seq', (SELECT MAX(_recid) FROM na4.eg_resources));
\echo Finish Table eg_resources 
\echo . 
\echo Loading Table eg_staff 
\copy na4.eg_staff from '/usr1/dump-MT1/CSV/eg-staff.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_staff__recid_seq', (SELECT MAX(_recid) FROM na4.eg_staff));
\echo Finish Table eg_staff 
\echo . 
\echo Loading Table eg_stat 
\copy na4.eg_stat from '/usr1/dump-MT1/CSV/eg-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_stat__recid_seq', (SELECT MAX(_recid) FROM na4.eg_stat));
\echo Finish Table eg_stat 
\echo . 
\echo Loading Table eg_subtask 
\copy na4.eg_subtask from '/usr1/dump-MT1/CSV/eg-subtask.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_subtask__recid_seq', (SELECT MAX(_recid) FROM na4.eg_subtask));
\echo Finish Table eg_subtask 
\echo . 
\echo Loading Table eg_vendor 
\copy na4.eg_vendor from '/usr1/dump-MT1/CSV/eg-vendor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_vendor__recid_seq', (SELECT MAX(_recid) FROM na4.eg_vendor));
\echo Finish Table eg_vendor 
\echo . 
\echo Loading Table eg_vperform 
\copy na4.eg_vperform from '/usr1/dump-MT1/CSV/eg-vperform.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.eg_vperform__recid_seq', (SELECT MAX(_recid) FROM na4.eg_vperform));
\echo Finish Table eg_vperform 
\echo . 
\echo Loading Table ekum 
\copy na4.ekum from '/usr1/dump-MT1/CSV/ekum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.ekum__recid_seq', (SELECT MAX(_recid) FROM na4.ekum));
\echo Finish Table ekum 
\echo . 
\echo Loading Table employee 
\copy na4.employee from '/usr1/dump-MT1/CSV/employee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.employee__recid_seq', (SELECT MAX(_recid) FROM na4.employee));
update na4.employee set child = array_replace(child,NULL,''); 
\echo Finish Table employee 
\echo . 
\echo Loading Table equiplan 
\copy na4.equiplan from '/usr1/dump-MT1/CSV/equiplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.equiplan__recid_seq', (SELECT MAX(_recid) FROM na4.equiplan));
\echo Finish Table equiplan 
\echo . 
\echo Loading Table exrate 
\copy na4.exrate from '/usr1/dump-MT1/CSV/exrate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.exrate__recid_seq', (SELECT MAX(_recid) FROM na4.exrate));
\echo Finish Table exrate 
\echo . 
\echo Loading Table fa_artikel 
\copy na4.fa_artikel from '/usr1/dump-MT1/CSV/fa-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_artikel__recid_seq', (SELECT MAX(_recid) FROM na4.fa_artikel));
\echo Finish Table fa_artikel 
\echo . 
\echo Loading Table fa_counter 
\copy na4.fa_counter from '/usr1/dump-MT1/CSV/fa-Counter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_counter__recid_seq', (SELECT MAX(_recid) FROM na4.fa_counter));
\echo Finish Table fa_counter 
\echo . 
\echo Loading Table fa_dp 
\copy na4.fa_dp from '/usr1/dump-MT1/CSV/fa-DP.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_dp__recid_seq', (SELECT MAX(_recid) FROM na4.fa_dp));
\echo Finish Table fa_dp 
\echo . 
\echo Loading Table fa_grup 
\copy na4.fa_grup from '/usr1/dump-MT1/CSV/fa-grup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_grup__recid_seq', (SELECT MAX(_recid) FROM na4.fa_grup));
\echo Finish Table fa_grup 
\echo . 
\echo Loading Table fa_kateg 
\copy na4.fa_kateg from '/usr1/dump-MT1/CSV/fa-kateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_kateg__recid_seq', (SELECT MAX(_recid) FROM na4.fa_kateg));
\echo Finish Table fa_kateg 
\echo . 
\echo Loading Table fa_lager 
\copy na4.fa_lager from '/usr1/dump-MT1/CSV/fa-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_lager__recid_seq', (SELECT MAX(_recid) FROM na4.fa_lager));
\echo Finish Table fa_lager 
\echo . 
\echo Loading Table fa_op 
\copy na4.fa_op from '/usr1/dump-MT1/CSV/fa-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_op__recid_seq', (SELECT MAX(_recid) FROM na4.fa_op));
\echo Finish Table fa_op 
\echo . 
\echo Loading Table fa_order 
\copy na4.fa_order from '/usr1/dump-MT1/CSV/fa-Order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_order__recid_seq', (SELECT MAX(_recid) FROM na4.fa_order));
\echo Finish Table fa_order 
\echo . 
\echo Loading Table fa_ordheader 
\copy na4.fa_ordheader from '/usr1/dump-MT1/CSV/fa-OrdHeader.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_ordheader__recid_seq', (SELECT MAX(_recid) FROM na4.fa_ordheader));
\echo Finish Table fa_ordheader 
\echo . 
\echo Loading Table fa_quodetail 
\copy na4.fa_quodetail from '/usr1/dump-MT1/CSV/fa-QuoDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_quodetail__recid_seq', (SELECT MAX(_recid) FROM na4.fa_quodetail));
\echo Finish Table fa_quodetail 
\echo . 
\echo Loading Table fa_quotation 
\copy na4.fa_quotation from '/usr1/dump-MT1/CSV/fa-quotation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_quotation__recid_seq', (SELECT MAX(_recid) FROM na4.fa_quotation));
\echo Finish Table fa_quotation 
\echo . 
\echo Loading Table fa_user 
\copy na4.fa_user from '/usr1/dump-MT1/CSV/fa-user.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fa_user__recid_seq', (SELECT MAX(_recid) FROM na4.fa_user));
update na4.fa_user set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table fa_user 
\echo . 
\echo Loading Table fbstat 
\copy na4.fbstat from '/usr1/dump-MT1/CSV/fbstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fbstat__recid_seq', (SELECT MAX(_recid) FROM na4.fbstat));
\echo Finish Table fbstat 
\echo . 
\echo Loading Table feiertag 
\copy na4.feiertag from '/usr1/dump-MT1/CSV/feiertag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.feiertag__recid_seq', (SELECT MAX(_recid) FROM na4.feiertag));
\echo Finish Table feiertag 
\echo . 
\echo Loading Table ffont 
\copy na4.ffont from '/usr1/dump-MT1/CSV/ffont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.ffont__recid_seq', (SELECT MAX(_recid) FROM na4.ffont));
\echo Finish Table ffont 
\echo . 
\echo Loading Table fixleist 
\copy na4.fixleist from '/usr1/dump-MT1/CSV/fixleist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.fixleist__recid_seq', (SELECT MAX(_recid) FROM na4.fixleist));
\echo Finish Table fixleist 
\echo . 
\echo Loading Table gc_giro 
\copy na4.gc_giro from '/usr1/dump-MT1/CSV/gc-giro.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gc_giro__recid_seq', (SELECT MAX(_recid) FROM na4.gc_giro));
update na4.gc_giro set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_giro 
\echo . 
\echo Loading Table gc_jouhdr 
\copy na4.gc_jouhdr from '/usr1/dump-MT1/CSV/gc-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gc_jouhdr__recid_seq', (SELECT MAX(_recid) FROM na4.gc_jouhdr));
\echo Finish Table gc_jouhdr 
\echo . 
\echo Loading Table gc_journal 
\copy na4.gc_journal from '/usr1/dump-MT1/CSV/gc-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gc_journal__recid_seq', (SELECT MAX(_recid) FROM na4.gc_journal));
\echo Finish Table gc_journal 
\echo . 
\echo Loading Table gc_pi 
\copy na4.gc_pi from '/usr1/dump-MT1/CSV/gc-PI.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gc_pi__recid_seq', (SELECT MAX(_recid) FROM na4.gc_pi));
update na4.gc_pi set bez_array = array_replace(bez_array,NULL,''); 
update na4.gc_pi set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_pi 
\echo . 
\echo Loading Table gc_piacct 
\copy na4.gc_piacct from '/usr1/dump-MT1/CSV/gc-piacct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gc_piacct__recid_seq', (SELECT MAX(_recid) FROM na4.gc_piacct));
\echo Finish Table gc_piacct 
\echo . 
\echo Loading Table gc_pibline 
\copy na4.gc_pibline from '/usr1/dump-MT1/CSV/gc-PIbline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gc_pibline__recid_seq', (SELECT MAX(_recid) FROM na4.gc_pibline));
\echo Finish Table gc_pibline 
\echo . 
\echo Loading Table gc_pitype 
\copy na4.gc_pitype from '/usr1/dump-MT1/CSV/gc-piType.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gc_pitype__recid_seq', (SELECT MAX(_recid) FROM na4.gc_pitype));
\echo Finish Table gc_pitype 
\echo . 
\echo Loading Table genfcast 
\copy na4.genfcast from '/usr1/dump-MT1/CSV/genfcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.genfcast__recid_seq', (SELECT MAX(_recid) FROM na4.genfcast));
update na4.genfcast set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genfcast 
\echo . 
\echo Loading Table genlayout 
\copy na4.genlayout from '/usr1/dump-MT1/CSV/genlayout.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.genlayout__recid_seq', (SELECT MAX(_recid) FROM na4.genlayout));
update na4.genlayout set button_ext = array_replace(button_ext,NULL,''); 
update na4.genlayout set char_ext = array_replace(char_ext,NULL,''); 
update na4.genlayout set combo_ext = array_replace(combo_ext,NULL,''); 
update na4.genlayout set date_ext = array_replace(date_ext,NULL,''); 
update na4.genlayout set deci_ext = array_replace(deci_ext,NULL,''); 
update na4.genlayout set inte_ext = array_replace(inte_ext,NULL,''); 
update na4.genlayout set logi_ext = array_replace(logi_ext,NULL,''); 
update na4.genlayout set string_ext = array_replace(string_ext,NULL,''); 
update na4.genlayout set tchar_ext = array_replace(tchar_ext,NULL,''); 
update na4.genlayout set tdate_ext = array_replace(tdate_ext,NULL,''); 
update na4.genlayout set tdeci_ext = array_replace(tdeci_ext,NULL,''); 
update na4.genlayout set tinte_ext = array_replace(tinte_ext,NULL,''); 
update na4.genlayout set tlogi_ext = array_replace(tlogi_ext,NULL,''); 
\echo Finish Table genlayout 
\echo . 
\echo Loading Table genstat 
\copy na4.genstat from '/usr1/dump-MT1/CSV/genstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.genstat__recid_seq', (SELECT MAX(_recid) FROM na4.genstat));
update na4.genstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genstat 
\echo . 
\echo Loading Table gentable 
\copy na4.gentable from '/usr1/dump-MT1/CSV/gentable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gentable__recid_seq', (SELECT MAX(_recid) FROM na4.gentable));
update na4.gentable set char_ext = array_replace(char_ext,NULL,''); 
update na4.gentable set combo_ext = array_replace(combo_ext,NULL,''); 
\echo Finish Table gentable 
\echo . 
\echo Loading Table gk_field 
\copy na4.gk_field from '/usr1/dump-MT1/CSV/gk-field.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gk_field__recid_seq', (SELECT MAX(_recid) FROM na4.gk_field));
\echo Finish Table gk_field 
\echo . 
\echo Loading Table gk_label 
\copy na4.gk_label from '/usr1/dump-MT1/CSV/gk-label.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gk_label__recid_seq', (SELECT MAX(_recid) FROM na4.gk_label));
\echo Finish Table gk_label 
\echo . 
\echo Loading Table gk_notes 
\copy na4.gk_notes from '/usr1/dump-MT1/CSV/gk-notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gk_notes__recid_seq', (SELECT MAX(_recid) FROM na4.gk_notes));
update na4.gk_notes set notes = array_replace(notes,NULL,''); 
\echo Finish Table gk_notes 
\echo . 
\echo Loading Table gl_acct 
\copy na4.gl_acct from '/usr1/dump-MT1/CSV/gl-acct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_acct__recid_seq', (SELECT MAX(_recid) FROM na4.gl_acct));
\echo Finish Table gl_acct 
\echo . 
\echo Loading Table gl_accthis 
\copy na4.gl_accthis from '/usr1/dump-MT1/CSV/gl-accthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_accthis__recid_seq', (SELECT MAX(_recid) FROM na4.gl_accthis));
\echo Finish Table gl_accthis 
\echo . 
\echo Loading Table gl_coa 
\copy na4.gl_coa from '/usr1/dump-MT1/CSV/gl-coa.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_coa__recid_seq', (SELECT MAX(_recid) FROM na4.gl_coa));
\echo Finish Table gl_coa 
\echo . 
\echo Loading Table gl_cost 
\copy na4.gl_cost from '/usr1/dump-MT1/CSV/gl-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_cost__recid_seq', (SELECT MAX(_recid) FROM na4.gl_cost));
\echo Finish Table gl_cost 
\echo . 
\echo Loading Table gl_department 
\copy na4.gl_department from '/usr1/dump-MT1/CSV/gl-department.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_department__recid_seq', (SELECT MAX(_recid) FROM na4.gl_department));
\echo Finish Table gl_department 
\echo . 
\echo Loading Table gl_fstype 
\copy na4.gl_fstype from '/usr1/dump-MT1/CSV/gl-fstype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_fstype__recid_seq', (SELECT MAX(_recid) FROM na4.gl_fstype));
\echo Finish Table gl_fstype 
\echo . 
\echo Loading Table gl_htljournal 
\copy na4.gl_htljournal from '/usr1/dump-MT1/CSV/gl-htljournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_htljournal__recid_seq', (SELECT MAX(_recid) FROM na4.gl_htljournal));
\echo Finish Table gl_htljournal 
\echo . 
\echo Loading Table gl_jhdrhis 
\copy na4.gl_jhdrhis from '/usr1/dump-MT1/CSV/gl-jhdrhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_jhdrhis__recid_seq', (SELECT MAX(_recid) FROM na4.gl_jhdrhis));
\echo Finish Table gl_jhdrhis 
\echo . 
\echo Loading Table gl_jouhdr 
\copy na4.gl_jouhdr from '/usr1/dump-MT1/CSV/gl-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_jouhdr__recid_seq', (SELECT MAX(_recid) FROM na4.gl_jouhdr));
\echo Finish Table gl_jouhdr 
\echo . 
\echo Loading Table gl_jourhis 
\copy na4.gl_jourhis from '/usr1/dump-MT1/CSV/gl-jourhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_jourhis__recid_seq', (SELECT MAX(_recid) FROM na4.gl_jourhis));
\echo Finish Table gl_jourhis 
\echo . 
\echo Loading Table gl_journal 
\copy na4.gl_journal from '/usr1/dump-MT1/CSV/gl-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_journal__recid_seq', (SELECT MAX(_recid) FROM na4.gl_journal));
\echo Finish Table gl_journal 
\echo . 
\echo Loading Table gl_main 
\copy na4.gl_main from '/usr1/dump-MT1/CSV/gl-main.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.gl_main__recid_seq', (SELECT MAX(_recid) FROM na4.gl_main));
\echo Finish Table gl_main 
\echo . 
\echo Loading Table golf_caddie 
\copy na4.golf_caddie from '/usr1/dump-MT1/CSV/golf-caddie.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_caddie__recid_seq', (SELECT MAX(_recid) FROM na4.golf_caddie));
\echo Finish Table golf_caddie 
\echo . 
\echo Loading Table golf_caddie_assignment 
\copy na4.golf_caddie_assignment from '/usr1/dump-MT1/CSV/golf-caddie-assignment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_caddie_assignment__recid_seq', (SELECT MAX(_recid) FROM na4.golf_caddie_assignment));
\echo Finish Table golf_caddie_assignment 
\echo . 
\echo Loading Table golf_course 
\copy na4.golf_course from '/usr1/dump-MT1/CSV/golf-course.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_course__recid_seq', (SELECT MAX(_recid) FROM na4.golf_course));
\echo Finish Table golf_course 
\echo . 
\echo Loading Table golf_flight_reservation 
\copy na4.golf_flight_reservation from '/usr1/dump-MT1/CSV/golf-flight-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_flight_reservation__recid_seq', (SELECT MAX(_recid) FROM na4.golf_flight_reservation));
\echo Finish Table golf_flight_reservation 
\echo . 
\echo Loading Table golf_flight_reservation_hist 
\copy na4.golf_flight_reservation_hist from '/usr1/dump-MT1/CSV/golf-flight-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_flight_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM na4.golf_flight_reservation_hist));
\echo Finish Table golf_flight_reservation_hist 
\echo . 
\echo Loading Table golf_golfer_reservation 
\copy na4.golf_golfer_reservation from '/usr1/dump-MT1/CSV/golf-golfer-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_golfer_reservation__recid_seq', (SELECT MAX(_recid) FROM na4.golf_golfer_reservation));
\echo Finish Table golf_golfer_reservation 
\echo . 
\echo Loading Table golf_golfer_reservation_hist 
\copy na4.golf_golfer_reservation_hist from '/usr1/dump-MT1/CSV/golf-golfer-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_golfer_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM na4.golf_golfer_reservation_hist));
\echo Finish Table golf_golfer_reservation_hist 
\echo . 
\echo Loading Table golf_holiday 
\copy na4.golf_holiday from '/usr1/dump-MT1/CSV/golf-holiday.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_holiday__recid_seq', (SELECT MAX(_recid) FROM na4.golf_holiday));
\echo Finish Table golf_holiday 
\echo . 
\echo Loading Table golf_main_reservation 
\copy na4.golf_main_reservation from '/usr1/dump-MT1/CSV/golf-main-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_main_reservation__recid_seq', (SELECT MAX(_recid) FROM na4.golf_main_reservation));
\echo Finish Table golf_main_reservation 
\echo . 
\echo Loading Table golf_main_reservation_hist 
\copy na4.golf_main_reservation_hist from '/usr1/dump-MT1/CSV/golf-main-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_main_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM na4.golf_main_reservation_hist));
\echo Finish Table golf_main_reservation_hist 
\echo . 
\echo Loading Table golf_rate 
\copy na4.golf_rate from '/usr1/dump-MT1/CSV/golf-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_rate__recid_seq', (SELECT MAX(_recid) FROM na4.golf_rate));
\echo Finish Table golf_rate 
\echo . 
\echo Loading Table golf_shift 
\copy na4.golf_shift from '/usr1/dump-MT1/CSV/golf-shift.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_shift__recid_seq', (SELECT MAX(_recid) FROM na4.golf_shift));
\echo Finish Table golf_shift 
\echo . 
\echo Loading Table golf_transfer 
\copy na4.golf_transfer from '/usr1/dump-MT1/CSV/golf-transfer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.golf_transfer__recid_seq', (SELECT MAX(_recid) FROM na4.golf_transfer));
\echo Finish Table golf_transfer 
\echo . 
\echo Loading Table guest 
\copy na4.guest from '/usr1/dump-MT1/CSV/guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guest__recid_seq', (SELECT MAX(_recid) FROM na4.guest));
update na4.guest set notizen = array_replace(notizen,NULL,''); 
update na4.guest set vornamekind = array_replace(vornamekind,NULL,''); 
\echo Finish Table guest 
\echo . 
\echo Loading Table guest_pr 
\copy na4.guest_pr from '/usr1/dump-MT1/CSV/guest-pr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guest_pr__recid_seq', (SELECT MAX(_recid) FROM na4.guest_pr));
\echo Finish Table guest_pr 
\echo . 
\echo Loading Table guest_queasy 
\copy na4.guest_queasy from '/usr1/dump-MT1/CSV/guest-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guest_queasy__recid_seq', (SELECT MAX(_recid) FROM na4.guest_queasy));
\echo Finish Table guest_queasy 
\echo . 
\echo Loading Table guest_remark 
\copy na4.guest_remark from '/usr1/dump-MT1/CSV/guest-remark.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guest_remark__recid_seq', (SELECT MAX(_recid) FROM na4.guest_remark));
update na4.guest_remark set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table guest_remark 
\echo . 
\echo Loading Table guestat 
\copy na4.guestat from '/usr1/dump-MT1/CSV/guestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guestat__recid_seq', (SELECT MAX(_recid) FROM na4.guestat));
\echo Finish Table guestat 
\echo . 
\echo Loading Table guestat1 
\copy na4.guestat1 from '/usr1/dump-MT1/CSV/guestat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guestat1__recid_seq', (SELECT MAX(_recid) FROM na4.guestat1));
\echo Finish Table guestat1 
\echo . 
\echo Loading Table guestbook 
\copy na4.guestbook from '/usr1/dump-MT1/CSV/guestbook.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guestbook__recid_seq', (SELECT MAX(_recid) FROM na4.guestbook));
update na4.guestbook set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table guestbook 
\echo . 
\echo Loading Table guestbud 
\copy na4.guestbud from '/usr1/dump-MT1/CSV/guestbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guestbud__recid_seq', (SELECT MAX(_recid) FROM na4.guestbud));
\echo Finish Table guestbud 
\echo . 
\echo Loading Table guestseg 
\copy na4.guestseg from '/usr1/dump-MT1/CSV/guestseg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.guestseg__recid_seq', (SELECT MAX(_recid) FROM na4.guestseg));
\echo Finish Table guestseg 
\echo . 
\echo Loading Table h_artcost 
\copy na4.h_artcost from '/usr1/dump-MT1/CSV/h-artcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_artcost__recid_seq', (SELECT MAX(_recid) FROM na4.h_artcost));
\echo Finish Table h_artcost 
\echo . 
\echo Loading Table h_artikel 
\copy na4.h_artikel from '/usr1/dump-MT1/CSV/h-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_artikel__recid_seq', (SELECT MAX(_recid) FROM na4.h_artikel));
\echo Finish Table h_artikel 
\echo . 
\echo Loading Table h_bill 
\copy na4.h_bill from '/usr1/dump-MT1/CSV/h-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_bill__recid_seq', (SELECT MAX(_recid) FROM na4.h_bill));
\echo Finish Table h_bill 
\echo . 
\echo Loading Table h_bill_line 
\copy na4.h_bill_line from '/usr1/dump-MT1/CSV/h-bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_bill_line__recid_seq', (SELECT MAX(_recid) FROM na4.h_bill_line));
\echo Finish Table h_bill_line 
\echo . 
\echo Loading Table h_compli 
\copy na4.h_compli from '/usr1/dump-MT1/CSV/h-compli.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_compli__recid_seq', (SELECT MAX(_recid) FROM na4.h_compli));
\echo Finish Table h_compli 
\echo . 
\echo Loading Table h_cost 
\copy na4.h_cost from '/usr1/dump-MT1/CSV/h-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_cost__recid_seq', (SELECT MAX(_recid) FROM na4.h_cost));
\echo Finish Table h_cost 
\echo . 
\echo Loading Table h_journal 
\copy na4.h_journal from '/usr1/dump-MT1/CSV/h-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_journal__recid_seq', (SELECT MAX(_recid) FROM na4.h_journal));
\echo Finish Table h_journal 
\echo . 
\echo Loading Table h_menu 
\copy na4.h_menu from '/usr1/dump-MT1/CSV/h-menu.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_menu__recid_seq', (SELECT MAX(_recid) FROM na4.h_menu));
\echo Finish Table h_menu 
\echo . 
\echo Loading Table h_mjourn 
\copy na4.h_mjourn from '/usr1/dump-MT1/CSV/h-mjourn.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_mjourn__recid_seq', (SELECT MAX(_recid) FROM na4.h_mjourn));
\echo Finish Table h_mjourn 
\echo . 
\echo Loading Table h_oldjou 
\copy na4.h_oldjou from '/usr1/dump-MT1/CSV/h-oldjou.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_oldjou__recid_seq', (SELECT MAX(_recid) FROM na4.h_oldjou));
\echo Finish Table h_oldjou 
\echo . 
\echo Loading Table h_order 
\copy na4.h_order from '/usr1/dump-MT1/CSV/h-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_order__recid_seq', (SELECT MAX(_recid) FROM na4.h_order));
update na4.h_order set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table h_order 
\echo . 
\echo Loading Table h_queasy 
\copy na4.h_queasy from '/usr1/dump-MT1/CSV/h-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_queasy__recid_seq', (SELECT MAX(_recid) FROM na4.h_queasy));
\echo Finish Table h_queasy 
\echo . 
\echo Loading Table h_rezept 
\copy na4.h_rezept from '/usr1/dump-MT1/CSV/h-rezept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_rezept__recid_seq', (SELECT MAX(_recid) FROM na4.h_rezept));
\echo Finish Table h_rezept 
\echo . 
\echo Loading Table h_rezlin 
\copy na4.h_rezlin from '/usr1/dump-MT1/CSV/h-rezlin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_rezlin__recid_seq', (SELECT MAX(_recid) FROM na4.h_rezlin));
\echo Finish Table h_rezlin 
\echo . 
\echo Loading Table h_storno 
\copy na4.h_storno from '/usr1/dump-MT1/CSV/h-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_storno__recid_seq', (SELECT MAX(_recid) FROM na4.h_storno));
\echo Finish Table h_storno 
\echo . 
\echo Loading Table h_umsatz 
\copy na4.h_umsatz from '/usr1/dump-MT1/CSV/h-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.h_umsatz__recid_seq', (SELECT MAX(_recid) FROM na4.h_umsatz));
\echo Finish Table h_umsatz 
\echo . 
\echo Loading Table history 
\copy na4.history from '/usr1/dump-MT1/CSV/history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.history__recid_seq', (SELECT MAX(_recid) FROM na4.history));
\echo Finish Table history 
\echo . 
\echo Loading Table hoteldpt 
\copy na4.hoteldpt from '/usr1/dump-MT1/CSV/hoteldpt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.hoteldpt__recid_seq', (SELECT MAX(_recid) FROM na4.hoteldpt));
\echo Finish Table hoteldpt 
\echo . 
\echo Loading Table hrbeleg 
\copy na4.hrbeleg from '/usr1/dump-MT1/CSV/hrbeleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.hrbeleg__recid_seq', (SELECT MAX(_recid) FROM na4.hrbeleg));
\echo Finish Table hrbeleg 
\echo . 
\echo Loading Table hrsegement 
\copy na4.hrsegement from '/usr1/dump-MT1/CSV/hrsegement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.hrsegement__recid_seq', (SELECT MAX(_recid) FROM na4.hrsegement));
\echo Finish Table hrsegement 
\echo . 
\echo Loading Table htparam 
\copy na4.htparam from '/usr1/dump-MT1/CSV/htparam.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.htparam__recid_seq', (SELECT MAX(_recid) FROM na4.htparam));
\echo Finish Table htparam 
\echo . 
\echo Loading Table htreport 
\copy na4.htreport from '/usr1/dump-MT1/CSV/htreport.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.htreport__recid_seq', (SELECT MAX(_recid) FROM na4.htreport));
\echo Finish Table htreport 
\echo . 
\echo Loading Table iftable 
\copy na4.iftable from '/usr1/dump-MT1/CSV/iftable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.iftable__recid_seq', (SELECT MAX(_recid) FROM na4.iftable));
\echo Finish Table iftable 
\echo . 
\echo Loading Table interface 
\copy na4.interface from '/usr1/dump-MT1/CSV/interface.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.interface__recid_seq', (SELECT MAX(_recid) FROM na4.interface));
\echo Finish Table interface 
\echo . 
\echo Loading Table k_history 
\copy na4.k_history from '/usr1/dump-MT1/CSV/k-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.k_history__recid_seq', (SELECT MAX(_recid) FROM na4.k_history));
\echo Finish Table k_history 
\echo . 
\echo Loading Table kabine 
\copy na4.kabine from '/usr1/dump-MT1/CSV/kabine.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kabine__recid_seq', (SELECT MAX(_recid) FROM na4.kabine));
\echo Finish Table kabine 
\echo . 
\echo Loading Table kalender 
\copy na4.kalender from '/usr1/dump-MT1/CSV/kalender.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kalender__recid_seq', (SELECT MAX(_recid) FROM na4.kalender));
update na4.kalender set note = array_replace(note,NULL,''); 
\echo Finish Table kalender 
\echo . 
\echo Loading Table kasse 
\copy na4.kasse from '/usr1/dump-MT1/CSV/kasse.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kasse__recid_seq', (SELECT MAX(_recid) FROM na4.kasse));
\echo Finish Table kasse 
\echo . 
\echo Loading Table katpreis 
\copy na4.katpreis from '/usr1/dump-MT1/CSV/katpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.katpreis__recid_seq', (SELECT MAX(_recid) FROM na4.katpreis));
\echo Finish Table katpreis 
\echo . 
\echo Loading Table kellne1 
\copy na4.kellne1 from '/usr1/dump-MT1/CSV/kellne1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kellne1__recid_seq', (SELECT MAX(_recid) FROM na4.kellne1));
\echo Finish Table kellne1 
\echo . 
\echo Loading Table kellner 
\copy na4.kellner from '/usr1/dump-MT1/CSV/kellner.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kellner__recid_seq', (SELECT MAX(_recid) FROM na4.kellner));
\echo Finish Table kellner 
\echo . 
\echo Loading Table kontakt 
\copy na4.kontakt from '/usr1/dump-MT1/CSV/kontakt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kontakt__recid_seq', (SELECT MAX(_recid) FROM na4.kontakt));
\echo Finish Table kontakt 
\echo . 
\echo Loading Table kontline 
\copy na4.kontline from '/usr1/dump-MT1/CSV/kontline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kontline__recid_seq', (SELECT MAX(_recid) FROM na4.kontline));
\echo Finish Table kontline 
\echo . 
\echo Loading Table kontlink 
\copy na4.kontlink from '/usr1/dump-MT1/CSV/kontlink.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kontlink__recid_seq', (SELECT MAX(_recid) FROM na4.kontlink));
\echo Finish Table kontlink 
\echo . 
\echo Loading Table kontplan 
\copy na4.kontplan from '/usr1/dump-MT1/CSV/kontplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kontplan__recid_seq', (SELECT MAX(_recid) FROM na4.kontplan));
\echo Finish Table kontplan 
\echo . 
\echo Loading Table kontstat 
\copy na4.kontstat from '/usr1/dump-MT1/CSV/kontstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kontstat__recid_seq', (SELECT MAX(_recid) FROM na4.kontstat));
update na4.kontstat set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table kontstat 
\echo . 
\echo Loading Table kresline 
\copy na4.kresline from '/usr1/dump-MT1/CSV/kresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.kresline__recid_seq', (SELECT MAX(_recid) FROM na4.kresline));
\echo Finish Table kresline 
\echo . 
\echo Loading Table l_artikel 
\copy na4.l_artikel from '/usr1/dump-MT1/CSV/l-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_artikel__recid_seq', (SELECT MAX(_recid) FROM na4.l_artikel));
update na4.l_artikel set lief_artnr = array_replace(lief_artnr,NULL,''); 
\echo Finish Table l_artikel 
\echo . 
\echo Loading Table l_bestand 
\copy na4.l_bestand from '/usr1/dump-MT1/CSV/l-bestand.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_bestand__recid_seq', (SELECT MAX(_recid) FROM na4.l_bestand));
\echo Finish Table l_bestand 
\echo . 
\echo Loading Table l_besthis 
\copy na4.l_besthis from '/usr1/dump-MT1/CSV/l-besthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_besthis__recid_seq', (SELECT MAX(_recid) FROM na4.l_besthis));
\echo Finish Table l_besthis 
\echo . 
\echo Loading Table l_hauptgrp 
\copy na4.l_hauptgrp from '/usr1/dump-MT1/CSV/l-hauptgrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_hauptgrp__recid_seq', (SELECT MAX(_recid) FROM na4.l_hauptgrp));
\echo Finish Table l_hauptgrp 
\echo . 
\echo Loading Table l_kredit 
\copy na4.l_kredit from '/usr1/dump-MT1/CSV/l-kredit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_kredit__recid_seq', (SELECT MAX(_recid) FROM na4.l_kredit));
\echo Finish Table l_kredit 
\echo . 
\echo Loading Table l_lager 
\copy na4.l_lager from '/usr1/dump-MT1/CSV/l-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_lager__recid_seq', (SELECT MAX(_recid) FROM na4.l_lager));
\echo Finish Table l_lager 
\echo . 
\echo Loading Table l_lieferant 
\copy na4.l_lieferant from '/usr1/dump-MT1/CSV/l-lieferant.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_lieferant__recid_seq', (SELECT MAX(_recid) FROM na4.l_lieferant));
update na4.l_lieferant set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table l_lieferant 
\echo . 
\echo Loading Table l_liefumsatz 
\copy na4.l_liefumsatz from '/usr1/dump-MT1/CSV/l-liefumsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_liefumsatz__recid_seq', (SELECT MAX(_recid) FROM na4.l_liefumsatz));
\echo Finish Table l_liefumsatz 
\echo . 
\echo Loading Table l_op 
\copy na4.l_op from '/usr1/dump-MT1/CSV/l-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_op__recid_seq', (SELECT MAX(_recid) FROM na4.l_op));
\echo Finish Table l_op 
\echo . 
\echo Loading Table l_ophdr 
\copy na4.l_ophdr from '/usr1/dump-MT1/CSV/l-ophdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_ophdr__recid_seq', (SELECT MAX(_recid) FROM na4.l_ophdr));
\echo Finish Table l_ophdr 
\echo . 
\echo Loading Table l_ophhis 
\copy na4.l_ophhis from '/usr1/dump-MT1/CSV/l-ophhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_ophhis__recid_seq', (SELECT MAX(_recid) FROM na4.l_ophhis));
\echo Finish Table l_ophhis 
\echo . 
\echo Loading Table l_ophis 
\copy na4.l_ophis from '/usr1/dump-MT1/CSV/l-ophis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_ophis__recid_seq', (SELECT MAX(_recid) FROM na4.l_ophis));
\echo Finish Table l_ophis 
\echo . 
\echo Loading Table l_order 
\copy na4.l_order from '/usr1/dump-MT1/CSV/l-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_order__recid_seq', (SELECT MAX(_recid) FROM na4.l_order));
update na4.l_order set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_order 
\echo . 
\echo Loading Table l_orderhdr 
\copy na4.l_orderhdr from '/usr1/dump-MT1/CSV/l-orderhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_orderhdr__recid_seq', (SELECT MAX(_recid) FROM na4.l_orderhdr));
update na4.l_orderhdr set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_orderhdr 
\echo . 
\echo Loading Table l_pprice 
\copy na4.l_pprice from '/usr1/dump-MT1/CSV/l-pprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_pprice__recid_seq', (SELECT MAX(_recid) FROM na4.l_pprice));
\echo Finish Table l_pprice 
\echo . 
\echo Loading Table l_quote 
\copy na4.l_quote from '/usr1/dump-MT1/CSV/l-quote.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_quote__recid_seq', (SELECT MAX(_recid) FROM na4.l_quote));
update na4.l_quote set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table l_quote 
\echo . 
\echo Loading Table l_segment 
\copy na4.l_segment from '/usr1/dump-MT1/CSV/l-segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_segment__recid_seq', (SELECT MAX(_recid) FROM na4.l_segment));
\echo Finish Table l_segment 
\echo . 
\echo Loading Table l_umsatz 
\copy na4.l_umsatz from '/usr1/dump-MT1/CSV/l-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_umsatz__recid_seq', (SELECT MAX(_recid) FROM na4.l_umsatz));
\echo Finish Table l_umsatz 
\echo . 
\echo Loading Table l_untergrup 
\copy na4.l_untergrup from '/usr1/dump-MT1/CSV/l-untergrup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_untergrup__recid_seq', (SELECT MAX(_recid) FROM na4.l_untergrup));
\echo Finish Table l_untergrup 
\echo . 
\echo Loading Table l_verbrauch 
\copy na4.l_verbrauch from '/usr1/dump-MT1/CSV/l-verbrauch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_verbrauch__recid_seq', (SELECT MAX(_recid) FROM na4.l_verbrauch));
\echo Finish Table l_verbrauch 
\echo . 
\echo Loading Table l_zahlbed 
\copy na4.l_zahlbed from '/usr1/dump-MT1/CSV/l-zahlbed.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.l_zahlbed__recid_seq', (SELECT MAX(_recid) FROM na4.l_zahlbed));
\echo Finish Table l_zahlbed 
\echo . 
\echo Loading Table landstat 
\copy na4.landstat from '/usr1/dump-MT1/CSV/landstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.landstat__recid_seq', (SELECT MAX(_recid) FROM na4.landstat));
\echo Finish Table landstat 
\echo . 
\echo Loading Table masseur 
\copy na4.masseur from '/usr1/dump-MT1/CSV/masseur.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.masseur__recid_seq', (SELECT MAX(_recid) FROM na4.masseur));
\echo Finish Table masseur 
\echo . 
\echo Loading Table mast_art 
\copy na4.mast_art from '/usr1/dump-MT1/CSV/mast-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mast_art__recid_seq', (SELECT MAX(_recid) FROM na4.mast_art));
\echo Finish Table mast_art 
\echo . 
\echo Loading Table master 
\copy na4.master from '/usr1/dump-MT1/CSV/master.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.master__recid_seq', (SELECT MAX(_recid) FROM na4.master));
\echo Finish Table master 
\echo . 
\echo Loading Table mathis 
\copy na4.mathis from '/usr1/dump-MT1/CSV/mathis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mathis__recid_seq', (SELECT MAX(_recid) FROM na4.mathis));
\echo Finish Table mathis 
\echo . 
\echo Loading Table mc_aclub 
\copy na4.mc_aclub from '/usr1/dump-MT1/CSV/mc-aclub.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mc_aclub__recid_seq', (SELECT MAX(_recid) FROM na4.mc_aclub));
\echo Finish Table mc_aclub 
\echo . 
\echo Loading Table mc_cardhis 
\copy na4.mc_cardhis from '/usr1/dump-MT1/CSV/mc-cardhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mc_cardhis__recid_seq', (SELECT MAX(_recid) FROM na4.mc_cardhis));
\echo Finish Table mc_cardhis 
\echo . 
\echo Loading Table mc_disc 
\copy na4.mc_disc from '/usr1/dump-MT1/CSV/mc-disc.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mc_disc__recid_seq', (SELECT MAX(_recid) FROM na4.mc_disc));
\echo Finish Table mc_disc 
\echo . 
\echo Loading Table mc_fee 
\copy na4.mc_fee from '/usr1/dump-MT1/CSV/mc-fee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mc_fee__recid_seq', (SELECT MAX(_recid) FROM na4.mc_fee));
\echo Finish Table mc_fee 
\echo . 
\echo Loading Table mc_guest 
\copy na4.mc_guest from '/usr1/dump-MT1/CSV/mc-guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mc_guest__recid_seq', (SELECT MAX(_recid) FROM na4.mc_guest));
\echo Finish Table mc_guest 
\echo . 
\echo Loading Table mc_types 
\copy na4.mc_types from '/usr1/dump-MT1/CSV/mc-types.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mc_types__recid_seq', (SELECT MAX(_recid) FROM na4.mc_types));
\echo Finish Table mc_types 
\echo . 
\echo Loading Table mealcoup 
\copy na4.mealcoup from '/usr1/dump-MT1/CSV/mealcoup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mealcoup__recid_seq', (SELECT MAX(_recid) FROM na4.mealcoup));
\echo Finish Table mealcoup 
\echo . 
\echo Loading Table messages 
\copy na4.messages from '/usr1/dump-MT1/CSV/messages.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.messages__recid_seq', (SELECT MAX(_recid) FROM na4.messages));
update na4.messages set messtext = array_replace(messtext,NULL,''); 
\echo Finish Table messages 
\echo . 
\echo Loading Table messe 
\copy na4.messe from '/usr1/dump-MT1/CSV/messe.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.messe__recid_seq', (SELECT MAX(_recid) FROM na4.messe));
\echo Finish Table messe 
\echo . 
\echo Loading Table mhis_line 
\copy na4.mhis_line from '/usr1/dump-MT1/CSV/mhis-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.mhis_line__recid_seq', (SELECT MAX(_recid) FROM na4.mhis_line));
\echo Finish Table mhis_line 
\echo . 
\echo Loading Table nation 
\copy na4.nation from '/usr1/dump-MT1/CSV/nation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.nation__recid_seq', (SELECT MAX(_recid) FROM na4.nation));
\echo Finish Table nation 
\echo . 
\echo Loading Table nationstat 
\copy na4.nationstat from '/usr1/dump-MT1/CSV/nationstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.nationstat__recid_seq', (SELECT MAX(_recid) FROM na4.nationstat));
\echo Finish Table nationstat 
\echo . 
\echo Loading Table natstat1 
\copy na4.natstat1 from '/usr1/dump-MT1/CSV/natstat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.natstat1__recid_seq', (SELECT MAX(_recid) FROM na4.natstat1));
\echo Finish Table natstat1 
\echo . 
\echo Loading Table nebenst 
\copy na4.nebenst from '/usr1/dump-MT1/CSV/nebenst.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.nebenst__recid_seq', (SELECT MAX(_recid) FROM na4.nebenst));
\echo Finish Table nebenst 
\echo . 
\echo Loading Table nightaudit 
\copy na4.nightaudit from '/usr1/dump-MT1/CSV/nightaudit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.nightaudit__recid_seq', (SELECT MAX(_recid) FROM na4.nightaudit));
\echo Finish Table nightaudit 
\echo . 
\echo Loading Table nitehist 
\copy na4.nitehist from '/usr1/dump-MT1/CSV/nitehist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.nitehist__recid_seq', (SELECT MAX(_recid) FROM na4.nitehist));
\echo Finish Table nitehist 
\echo . 
\echo Loading Table nitestor 
\copy na4.nitestor from '/usr1/dump-MT1/CSV/nitestor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.nitestor__recid_seq', (SELECT MAX(_recid) FROM na4.nitestor));
\echo Finish Table nitestor 
\echo . 
\echo Loading Table notes 
\copy na4.notes from '/usr1/dump-MT1/CSV/notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.notes__recid_seq', (SELECT MAX(_recid) FROM na4.notes));
update na4.notes set note = array_replace(note,NULL,''); 
\echo Finish Table notes 
\echo . 
\echo Loading Table outorder 
\copy na4.outorder from '/usr1/dump-MT1/CSV/outorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.outorder__recid_seq', (SELECT MAX(_recid) FROM na4.outorder));
\echo Finish Table outorder 
\echo . 
\echo Loading Table package 
\copy na4.package from '/usr1/dump-MT1/CSV/package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.package__recid_seq', (SELECT MAX(_recid) FROM na4.package));
\echo Finish Table package 
\echo . 
\echo Loading Table parameters 
\copy na4.parameters from '/usr1/dump-MT1/CSV/parameters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.parameters__recid_seq', (SELECT MAX(_recid) FROM na4.parameters));
\echo Finish Table parameters 
\echo . 
\echo Loading Table paramtext 
\copy na4.paramtext from '/usr1/dump-MT1/CSV/paramtext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.paramtext__recid_seq', (SELECT MAX(_recid) FROM na4.paramtext));
\echo Finish Table paramtext 
\echo . 
\echo Loading Table pricecod 
\copy na4.pricecod from '/usr1/dump-MT1/CSV/pricecod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.pricecod__recid_seq', (SELECT MAX(_recid) FROM na4.pricecod));
\echo Finish Table pricecod 
\echo . 
\echo Loading Table pricegrp 
\copy na4.pricegrp from '/usr1/dump-MT1/CSV/pricegrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.pricegrp__recid_seq', (SELECT MAX(_recid) FROM na4.pricegrp));
\echo Finish Table pricegrp 
\echo . 
\echo Loading Table printcod 
\copy na4.printcod from '/usr1/dump-MT1/CSV/printcod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.printcod__recid_seq', (SELECT MAX(_recid) FROM na4.printcod));
\echo Finish Table printcod 
\echo . 
\echo Loading Table printer 
\copy na4.printer from '/usr1/dump-MT1/CSV/printer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.printer__recid_seq', (SELECT MAX(_recid) FROM na4.printer));
\echo Finish Table printer 
\echo . 
\echo Loading Table prmarket 
\copy na4.prmarket from '/usr1/dump-MT1/CSV/prmarket.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.prmarket__recid_seq', (SELECT MAX(_recid) FROM na4.prmarket));
\echo Finish Table prmarket 
\echo . 
\echo Loading Table progcat 
\copy na4.progcat from '/usr1/dump-MT1/CSV/progcat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.progcat__recid_seq', (SELECT MAX(_recid) FROM na4.progcat));
\echo Finish Table progcat 
\echo . 
\echo Loading Table progfile 
\copy na4.progfile from '/usr1/dump-MT1/CSV/progfile.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.progfile__recid_seq', (SELECT MAX(_recid) FROM na4.progfile));
\echo Finish Table progfile 
\echo . 
\echo Loading Table prtable 
\copy na4.prtable from '/usr1/dump-MT1/CSV/prtable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.prtable__recid_seq', (SELECT MAX(_recid) FROM na4.prtable));
\echo Finish Table prtable 
\echo . 
\echo Loading Table queasy 
\copy na4.queasy from '/usr1/dump-MT1/CSV/queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.queasy__recid_seq', (SELECT MAX(_recid) FROM na4.queasy));
\echo Finish Table queasy 
\echo . 
\echo Loading Table ratecode 
\copy na4.ratecode from '/usr1/dump-MT1/CSV/ratecode.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.ratecode__recid_seq', (SELECT MAX(_recid) FROM na4.ratecode));
update na4.ratecode set char1 = array_replace(char1,NULL,''); 
\echo Finish Table ratecode 
\echo . 
\echo Loading Table raum 
\copy na4.raum from '/usr1/dump-MT1/CSV/raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.raum__recid_seq', (SELECT MAX(_recid) FROM na4.raum));
\echo Finish Table raum 
\echo . 
\echo Loading Table res_history 
\copy na4.res_history from '/usr1/dump-MT1/CSV/res-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.res_history__recid_seq', (SELECT MAX(_recid) FROM na4.res_history));
\echo Finish Table res_history 
\echo . 
\echo Loading Table res_line 
\copy na4.res_line from '/usr1/dump-MT1/CSV/res-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.res_line__recid_seq', (SELECT MAX(_recid) FROM na4.res_line));
\echo Finish Table res_line 
\echo . 
\echo Loading Table reservation 
\copy na4.reservation from '/usr1/dump-MT1/CSV/reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.reservation__recid_seq', (SELECT MAX(_recid) FROM na4.reservation));
\echo Finish Table reservation 
\echo . 
\echo Loading Table reslin_queasy 
\copy na4.reslin_queasy from '/usr1/dump-MT1/CSV/reslin-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.reslin_queasy__recid_seq', (SELECT MAX(_recid) FROM na4.reslin_queasy));
\echo Finish Table reslin_queasy 
\echo . 
\echo Loading Table resplan 
\copy na4.resplan from '/usr1/dump-MT1/CSV/resplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.resplan__recid_seq', (SELECT MAX(_recid) FROM na4.resplan));
\echo Finish Table resplan 
\echo . 
\echo Loading Table rg_reports 
\copy na4.rg_reports from '/usr1/dump-MT1/CSV/rg-reports.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.rg_reports__recid_seq', (SELECT MAX(_recid) FROM na4.rg_reports));
update na4.rg_reports set metadata = array_replace(metadata,NULL,''); 
update na4.rg_reports set slice_name = array_replace(slice_name,NULL,''); 
update na4.rg_reports set view_name = array_replace(view_name,NULL,''); 
\echo Finish Table rg_reports 
\echo . 
\echo Loading Table rmbudget 
\copy na4.rmbudget from '/usr1/dump-MT1/CSV/rmbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.rmbudget__recid_seq', (SELECT MAX(_recid) FROM na4.rmbudget));
update na4.rmbudget set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table rmbudget 
\echo . 
\echo Loading Table sales 
\copy na4.sales from '/usr1/dump-MT1/CSV/sales.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sales__recid_seq', (SELECT MAX(_recid) FROM na4.sales));
\echo Finish Table sales 
\echo . 
\echo Loading Table salesbud 
\copy na4.salesbud from '/usr1/dump-MT1/CSV/salesbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.salesbud__recid_seq', (SELECT MAX(_recid) FROM na4.salesbud));
\echo Finish Table salesbud 
\echo . 
\echo Loading Table salestat 
\copy na4.salestat from '/usr1/dump-MT1/CSV/salestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.salestat__recid_seq', (SELECT MAX(_recid) FROM na4.salestat));
\echo Finish Table salestat 
\echo . 
\echo Loading Table salestim 
\copy na4.salestim from '/usr1/dump-MT1/CSV/salestim.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.salestim__recid_seq', (SELECT MAX(_recid) FROM na4.salestim));
\echo Finish Table salestim 
\echo . 
\echo Loading Table segment 
\copy na4.segment from '/usr1/dump-MT1/CSV/segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.segment__recid_seq', (SELECT MAX(_recid) FROM na4.segment));
\echo Finish Table segment 
\echo . 
\echo Loading Table segmentstat 
\copy na4.segmentstat from '/usr1/dump-MT1/CSV/segmentstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.segmentstat__recid_seq', (SELECT MAX(_recid) FROM na4.segmentstat));
\echo Finish Table segmentstat 
\echo . 
\echo Loading Table sms_bcaster 
\copy na4.sms_bcaster from '/usr1/dump-MT1/CSV/sms-bcaster.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sms_bcaster__recid_seq', (SELECT MAX(_recid) FROM na4.sms_bcaster));
\echo Finish Table sms_bcaster 
\echo . 
\echo Loading Table sms_broadcast 
\copy na4.sms_broadcast from '/usr1/dump-MT1/CSV/sms-broadcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sms_broadcast__recid_seq', (SELECT MAX(_recid) FROM na4.sms_broadcast));
\echo Finish Table sms_broadcast 
\echo . 
\echo Loading Table sms_group 
\copy na4.sms_group from '/usr1/dump-MT1/CSV/sms-group.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sms_group__recid_seq', (SELECT MAX(_recid) FROM na4.sms_group));
\echo Finish Table sms_group 
\echo . 
\echo Loading Table sms_groupmbr 
\copy na4.sms_groupmbr from '/usr1/dump-MT1/CSV/sms-groupmbr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sms_groupmbr__recid_seq', (SELECT MAX(_recid) FROM na4.sms_groupmbr));
\echo Finish Table sms_groupmbr 
\echo . 
\echo Loading Table sms_received 
\copy na4.sms_received from '/usr1/dump-MT1/CSV/sms-received.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sms_received__recid_seq', (SELECT MAX(_recid) FROM na4.sms_received));
\echo Finish Table sms_received 
\echo . 
\echo Loading Table sourccod 
\copy na4.sourccod from '/usr1/dump-MT1/CSV/Sourccod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sourccod__recid_seq', (SELECT MAX(_recid) FROM na4.sourccod));
\echo Finish Table sourccod 
\echo . 
\echo Loading Table sources 
\copy na4.sources from '/usr1/dump-MT1/CSV/sources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sources__recid_seq', (SELECT MAX(_recid) FROM na4.sources));
\echo Finish Table sources 
\echo . 
\echo Loading Table sourcetext 
\copy na4.sourcetext from '/usr1/dump-MT1/CSV/sourcetext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.sourcetext__recid_seq', (SELECT MAX(_recid) FROM na4.sourcetext));
\echo Finish Table sourcetext 
\echo . 
\echo Loading Table telephone 
\copy na4.telephone from '/usr1/dump-MT1/CSV/telephone.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.telephone__recid_seq', (SELECT MAX(_recid) FROM na4.telephone));
\echo Finish Table telephone 
\echo . 
\echo Loading Table texte 
\copy na4.texte from '/usr1/dump-MT1/CSV/texte.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.texte__recid_seq', (SELECT MAX(_recid) FROM na4.texte));
\echo Finish Table texte 
\echo . 
\echo Loading Table tisch 
\copy na4.tisch from '/usr1/dump-MT1/CSV/tisch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.tisch__recid_seq', (SELECT MAX(_recid) FROM na4.tisch));
\echo Finish Table tisch 
\echo . 
\echo Loading Table tisch_res 
\copy na4.tisch_res from '/usr1/dump-MT1/CSV/tisch-res.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.tisch_res__recid_seq', (SELECT MAX(_recid) FROM na4.tisch_res));
\echo Finish Table tisch_res 
\echo . 
\echo Loading Table uebertrag 
\copy na4.uebertrag from '/usr1/dump-MT1/CSV/uebertrag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.uebertrag__recid_seq', (SELECT MAX(_recid) FROM na4.uebertrag));
\echo Finish Table uebertrag 
\echo . 
\echo Loading Table umsatz 
\copy na4.umsatz from '/usr1/dump-MT1/CSV/umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.umsatz__recid_seq', (SELECT MAX(_recid) FROM na4.umsatz));
\echo Finish Table umsatz 
\echo . 
\echo Loading Table waehrung 
\copy na4.waehrung from '/usr1/dump-MT1/CSV/waehrung.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.waehrung__recid_seq', (SELECT MAX(_recid) FROM na4.waehrung));
\echo Finish Table waehrung 
\echo . 
\echo Loading Table wakeup 
\copy na4.wakeup from '/usr1/dump-MT1/CSV/wakeup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.wakeup__recid_seq', (SELECT MAX(_recid) FROM na4.wakeup));
\echo Finish Table wakeup 
\echo . 
\echo Loading Table wgrpdep 
\copy na4.wgrpdep from '/usr1/dump-MT1/CSV/wgrpdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.wgrpdep__recid_seq', (SELECT MAX(_recid) FROM na4.wgrpdep));
\echo Finish Table wgrpdep 
\echo . 
\echo Loading Table wgrpgen 
\copy na4.wgrpgen from '/usr1/dump-MT1/CSV/wgrpgen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.wgrpgen__recid_seq', (SELECT MAX(_recid) FROM na4.wgrpgen));
\echo Finish Table wgrpgen 
\echo . 
\echo Loading Table zimkateg 
\copy na4.zimkateg from '/usr1/dump-MT1/CSV/zimkateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zimkateg__recid_seq', (SELECT MAX(_recid) FROM na4.zimkateg));
\echo Finish Table zimkateg 
\echo . 
\echo Loading Table zimmer 
\copy na4.zimmer from '/usr1/dump-MT1/CSV/zimmer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zimmer__recid_seq', (SELECT MAX(_recid) FROM na4.zimmer));
update na4.zimmer set verbindung = array_replace(verbindung,NULL,''); 
\echo Finish Table zimmer 
\echo . 
\echo Loading Table zimmer_book 
\copy na4.zimmer_book from '/usr1/dump-MT1/CSV/zimmer-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zimmer_book__recid_seq', (SELECT MAX(_recid) FROM na4.zimmer_book));
\echo Finish Table zimmer_book 
\echo . 
\echo Loading Table zimmer_book_line 
\copy na4.zimmer_book_line from '/usr1/dump-MT1/CSV/zimmer-book-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zimmer_book_line__recid_seq', (SELECT MAX(_recid) FROM na4.zimmer_book_line));
\echo Finish Table zimmer_book_line 
\echo . 
\echo Loading Table zimplan 
\copy na4.zimplan from '/usr1/dump-MT1/CSV/zimplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zimplan__recid_seq', (SELECT MAX(_recid) FROM na4.zimplan));
\echo Finish Table zimplan 
\echo . 
\echo Loading Table zimpreis 
\copy na4.zimpreis from '/usr1/dump-MT1/CSV/zimpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zimpreis__recid_seq', (SELECT MAX(_recid) FROM na4.zimpreis));
\echo Finish Table zimpreis 
\echo . 
\echo Loading Table zinrstat 
\copy na4.zinrstat from '/usr1/dump-MT1/CSV/zinrstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zinrstat__recid_seq', (SELECT MAX(_recid) FROM na4.zinrstat));
\echo Finish Table zinrstat 
\echo . 
\echo Loading Table zkstat 
\copy na4.zkstat from '/usr1/dump-MT1/CSV/zkstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zkstat__recid_seq', (SELECT MAX(_recid) FROM na4.zkstat));
\echo Finish Table zkstat 
\echo . 
\echo Loading Table zwkum 
\copy na4.zwkum from '/usr1/dump-MT1/CSV/zwkum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('na4.zwkum__recid_seq', (SELECT MAX(_recid) FROM na4.zwkum));
\echo Finish Table zwkum 
\echo . 
