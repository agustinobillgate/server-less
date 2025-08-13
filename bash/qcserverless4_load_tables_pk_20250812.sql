\echo Loading Table absen 
\copy qcserverless4.absen from '/usr1/dump-qcserverless4-20250812/absen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.absen__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.absen));
\echo Finish Table absen 
\echo . 
\echo Loading Table akt_code 
\copy qcserverless4.akt_code from '/usr1/dump-qcserverless4-20250812/akt-code.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.akt_code__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.akt_code));
\echo Finish Table akt_code 
\echo . 
\echo Loading Table akt_cust 
\copy qcserverless4.akt_cust from '/usr1/dump-qcserverless4-20250812/akt-cust.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.akt_cust__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.akt_cust));
\echo Finish Table akt_cust 
\echo . 
\echo Loading Table akt_kont 
\copy qcserverless4.akt_kont from '/usr1/dump-qcserverless4-20250812/akt-kont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.akt_kont__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.akt_kont));
\echo Finish Table akt_kont 
\echo . 
\echo Loading Table akt_line 
\copy qcserverless4.akt_line from '/usr1/dump-qcserverless4-20250812/akt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.akt_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.akt_line));
\echo Finish Table akt_line 
\echo . 
\echo Loading Table akthdr 
\copy qcserverless4.akthdr from '/usr1/dump-qcserverless4-20250812/akthdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.akthdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.akthdr));
\echo Finish Table akthdr 
\echo . 
\echo Loading Table aktion 
\copy qcserverless4.aktion from '/usr1/dump-qcserverless4-20250812/aktion.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.aktion__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.aktion));
update qcserverless4.aktion set texte = array_replace(texte,NULL,''); 
\echo Finish Table aktion 
\echo . 
\echo Loading Table ap_journal 
\copy qcserverless4.ap_journal from '/usr1/dump-qcserverless4-20250812/ap-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.ap_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.ap_journal));
\echo Finish Table ap_journal 
\echo . 
\echo Loading Table apt_bill 
\copy qcserverless4.apt_bill from '/usr1/dump-qcserverless4-20250812/apt-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.apt_bill__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.apt_bill));
update qcserverless4.apt_bill set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table apt_bill 
\echo . 
\echo Loading Table archieve 
\copy qcserverless4.archieve from '/usr1/dump-qcserverless4-20250812/archieve.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.archieve__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.archieve));
update qcserverless4.archieve set char = array_replace(char,NULL,''); 
\echo Finish Table archieve 
\echo . 
\echo Loading Table argt_line 
\copy qcserverless4.argt_line from '/usr1/dump-qcserverless4-20250812/argt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.argt_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.argt_line));
\echo Finish Table argt_line 
\echo . 
\echo Loading Table argtcost 
\copy qcserverless4.argtcost from '/usr1/dump-qcserverless4-20250812/argtcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.argtcost__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.argtcost));
update qcserverless4.argtcost set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtcost 
\echo . 
\echo Loading Table argtstat 
\copy qcserverless4.argtstat from '/usr1/dump-qcserverless4-20250812/argtstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.argtstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.argtstat));
update qcserverless4.argtstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtstat 
\echo . 
\echo Loading Table arrangement 
\copy qcserverless4.arrangement from '/usr1/dump-qcserverless4-20250812/arrangement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.arrangement__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.arrangement));
update qcserverless4.arrangement set argt_rgbez2 = array_replace(argt_rgbez2,NULL,''); 
\echo Finish Table arrangement 
\echo . 
\echo Loading Table artikel 
\copy qcserverless4.artikel from '/usr1/dump-qcserverless4-20250812/artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.artikel));
\echo Finish Table artikel 
\echo . 
\echo Loading Table artprice 
\copy qcserverless4.artprice from '/usr1/dump-qcserverless4-20250812/artprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.artprice__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.artprice));
\echo Finish Table artprice 
\echo . 
\echo Loading Table b_history 
\copy qcserverless4.b_history from '/usr1/dump-qcserverless4-20250812/b-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.b_history__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.b_history));
update qcserverless4.b_history set anlass = array_replace(anlass,NULL,''); 
update qcserverless4.b_history set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update qcserverless4.b_history set ape__speisen = array_replace(ape__speisen,NULL,''); 
update qcserverless4.b_history set arrival = array_replace(arrival,NULL,''); 
update qcserverless4.b_history set c_resstatus = array_replace(c_resstatus,NULL,''); 
update qcserverless4.b_history set dance = array_replace(dance,NULL,''); 
update qcserverless4.b_history set deko2 = array_replace(deko2,NULL,''); 
update qcserverless4.b_history set dekoration = array_replace(dekoration,NULL,''); 
update qcserverless4.b_history set digestif = array_replace(digestif,NULL,''); 
update qcserverless4.b_history set dinner = array_replace(dinner,NULL,''); 
update qcserverless4.b_history set f_menu = array_replace(f_menu,NULL,''); 
update qcserverless4.b_history set f_no = array_replace(f_no,NULL,''); 
update qcserverless4.b_history set fotograf = array_replace(fotograf,NULL,''); 
update qcserverless4.b_history set gaestebuch = array_replace(gaestebuch,NULL,''); 
update qcserverless4.b_history set garderobe = array_replace(garderobe,NULL,''); 
update qcserverless4.b_history set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update qcserverless4.b_history set kaffee = array_replace(kaffee,NULL,''); 
update qcserverless4.b_history set kartentext = array_replace(kartentext,NULL,''); 
update qcserverless4.b_history set kontaktperson = array_replace(kontaktperson,NULL,''); 
update qcserverless4.b_history set kuenstler = array_replace(kuenstler,NULL,''); 
update qcserverless4.b_history set menue = array_replace(menue,NULL,''); 
update qcserverless4.b_history set menuekarten = array_replace(menuekarten,NULL,''); 
update qcserverless4.b_history set musik = array_replace(musik,NULL,''); 
update qcserverless4.b_history set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update qcserverless4.b_history set nadkarte = array_replace(nadkarte,NULL,''); 
update qcserverless4.b_history set ndessen = array_replace(ndessen,NULL,''); 
update qcserverless4.b_history set payment_userinit = array_replace(payment_userinit,NULL,''); 
update qcserverless4.b_history set personen2 = array_replace(personen2,NULL,''); 
update qcserverless4.b_history set raeume = array_replace(raeume,NULL,''); 
update qcserverless4.b_history set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update qcserverless4.b_history set raummiete = array_replace(raummiete,NULL,''); 
update qcserverless4.b_history set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update qcserverless4.b_history set service = array_replace(service,NULL,''); 
update qcserverless4.b_history set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update qcserverless4.b_history set sonstiges = array_replace(sonstiges,NULL,''); 
update qcserverless4.b_history set technik = array_replace(technik,NULL,''); 
update qcserverless4.b_history set tischform = array_replace(tischform,NULL,''); 
update qcserverless4.b_history set tischordnung = array_replace(tischordnung,NULL,''); 
update qcserverless4.b_history set tischplan = array_replace(tischplan,NULL,''); 
update qcserverless4.b_history set tischreden = array_replace(tischreden,NULL,''); 
update qcserverless4.b_history set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update qcserverless4.b_history set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update qcserverless4.b_history set va_ablauf = array_replace(va_ablauf,NULL,''); 
update qcserverless4.b_history set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update qcserverless4.b_history set vip = array_replace(vip,NULL,''); 
update qcserverless4.b_history set weine = array_replace(weine,NULL,''); 
update qcserverless4.b_history set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table b_history 
\echo . 
\echo Loading Table b_oorder 
\copy qcserverless4.b_oorder from '/usr1/dump-qcserverless4-20250812/b-oorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.b_oorder__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.b_oorder));
\echo Finish Table b_oorder 
\echo . 
\echo Loading Table b_storno 
\copy qcserverless4.b_storno from '/usr1/dump-qcserverless4-20250812/b-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.b_storno__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.b_storno));
update qcserverless4.b_storno set grund = array_replace(grund,NULL,''); 
\echo Finish Table b_storno 
\echo . 
\echo Loading Table ba_rset 
\copy qcserverless4.ba_rset from '/usr1/dump-qcserverless4-20250812/ba-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.ba_rset__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.ba_rset));
\echo Finish Table ba_rset 
\echo . 
\echo Loading Table ba_setup 
\copy qcserverless4.ba_setup from '/usr1/dump-qcserverless4-20250812/ba-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.ba_setup__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.ba_setup));
\echo Finish Table ba_setup 
\echo . 
\echo Loading Table ba_typ 
\copy qcserverless4.ba_typ from '/usr1/dump-qcserverless4-20250812/ba-typ.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.ba_typ__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.ba_typ));
\echo Finish Table ba_typ 
\echo . 
\echo Loading Table bankrep 
\copy qcserverless4.bankrep from '/usr1/dump-qcserverless4-20250812/bankrep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bankrep__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bankrep));
update qcserverless4.bankrep set anlass = array_replace(anlass,NULL,''); 
update qcserverless4.bankrep set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update qcserverless4.bankrep set ape__speisen = array_replace(ape__speisen,NULL,''); 
update qcserverless4.bankrep set dekoration = array_replace(dekoration,NULL,''); 
update qcserverless4.bankrep set digestif = array_replace(digestif,NULL,''); 
update qcserverless4.bankrep set fotograf = array_replace(fotograf,NULL,''); 
update qcserverless4.bankrep set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update qcserverless4.bankrep set kartentext = array_replace(kartentext,NULL,''); 
update qcserverless4.bankrep set kontaktperson = array_replace(kontaktperson,NULL,''); 
update qcserverless4.bankrep set menue = array_replace(menue,NULL,''); 
update qcserverless4.bankrep set menuekarten = array_replace(menuekarten,NULL,''); 
update qcserverless4.bankrep set musik = array_replace(musik,NULL,''); 
update qcserverless4.bankrep set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update qcserverless4.bankrep set ndessen = array_replace(ndessen,NULL,''); 
update qcserverless4.bankrep set personen2 = array_replace(personen2,NULL,''); 
update qcserverless4.bankrep set raeume = array_replace(raeume,NULL,''); 
update qcserverless4.bankrep set raummiete = array_replace(raummiete,NULL,''); 
update qcserverless4.bankrep set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update qcserverless4.bankrep set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update qcserverless4.bankrep set sonstiges = array_replace(sonstiges,NULL,''); 
update qcserverless4.bankrep set technik = array_replace(technik,NULL,''); 
update qcserverless4.bankrep set tischform = array_replace(tischform,NULL,''); 
update qcserverless4.bankrep set tischreden = array_replace(tischreden,NULL,''); 
update qcserverless4.bankrep set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update qcserverless4.bankrep set weine = array_replace(weine,NULL,''); 
update qcserverless4.bankrep set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bankrep 
\echo . 
\echo Loading Table bankres 
\copy qcserverless4.bankres from '/usr1/dump-qcserverless4-20250812/bankres.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bankres__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bankres));
update qcserverless4.bankres set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table bankres 
\echo . 
\echo Loading Table bediener 
\copy qcserverless4.bediener from '/usr1/dump-qcserverless4-20250812/bediener.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bediener__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bediener));
\echo Finish Table bediener 
\echo . 
\echo Loading Table bill 
\copy qcserverless4.bill from '/usr1/dump-qcserverless4-20250812/bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bill__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bill));
\echo Finish Table bill 
\echo . 
\echo Loading Table bill_lin_tax 
\copy qcserverless4.bill_lin_tax from '/usr1/dump-qcserverless4-20250812/bill-lin-tax.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bill_lin_tax__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bill_lin_tax));
\echo Finish Table bill_lin_tax 
\echo . 
\echo Loading Table bill_line 
\copy qcserverless4.bill_line from '/usr1/dump-qcserverless4-20250812/bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bill_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bill_line));
\echo Finish Table bill_line 
\echo . 
\echo Loading Table billhis 
\copy qcserverless4.billhis from '/usr1/dump-qcserverless4-20250812/billhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.billhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.billhis));
\echo Finish Table billhis 
\echo . 
\echo Loading Table billjournal 
\copy qcserverless4.billjournal from '/usr1/dump-qcserverless4-20250812/billjournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.billjournal__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.billjournal));
\echo Finish Table billjournal 
\echo . 
\echo Loading Table bk_beleg 
\copy qcserverless4.bk_beleg from '/usr1/dump-qcserverless4-20250812/bk-beleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_beleg__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_beleg));
\echo Finish Table bk_beleg 
\echo . 
\echo Loading Table bk_fsdef 
\copy qcserverless4.bk_fsdef from '/usr1/dump-qcserverless4-20250812/bk-fsdef.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_fsdef__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_fsdef));
\echo Finish Table bk_fsdef 
\echo . 
\echo Loading Table bk_func 
\copy qcserverless4.bk_func from '/usr1/dump-qcserverless4-20250812/bk-func.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_func__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_func));
update qcserverless4.bk_func set anlass = array_replace(anlass,NULL,''); 
update qcserverless4.bk_func set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update qcserverless4.bk_func set ape__speisen = array_replace(ape__speisen,NULL,''); 
update qcserverless4.bk_func set arrival = array_replace(arrival,NULL,''); 
update qcserverless4.bk_func set c_resstatus = array_replace(c_resstatus,NULL,''); 
update qcserverless4.bk_func set dance = array_replace(dance,NULL,''); 
update qcserverless4.bk_func set deko2 = array_replace(deko2,NULL,''); 
update qcserverless4.bk_func set dekoration = array_replace(dekoration,NULL,''); 
update qcserverless4.bk_func set digestif = array_replace(digestif,NULL,''); 
update qcserverless4.bk_func set dinner = array_replace(dinner,NULL,''); 
update qcserverless4.bk_func set f_menu = array_replace(f_menu,NULL,''); 
update qcserverless4.bk_func set f_no = array_replace(f_no,NULL,''); 
update qcserverless4.bk_func set fotograf = array_replace(fotograf,NULL,''); 
update qcserverless4.bk_func set gaestebuch = array_replace(gaestebuch,NULL,''); 
update qcserverless4.bk_func set garderobe = array_replace(garderobe,NULL,''); 
update qcserverless4.bk_func set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update qcserverless4.bk_func set kaffee = array_replace(kaffee,NULL,''); 
update qcserverless4.bk_func set kartentext = array_replace(kartentext,NULL,''); 
update qcserverless4.bk_func set kontaktperson = array_replace(kontaktperson,NULL,''); 
update qcserverless4.bk_func set kuenstler = array_replace(kuenstler,NULL,''); 
update qcserverless4.bk_func set menue = array_replace(menue,NULL,''); 
update qcserverless4.bk_func set menuekarten = array_replace(menuekarten,NULL,''); 
update qcserverless4.bk_func set musik = array_replace(musik,NULL,''); 
update qcserverless4.bk_func set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update qcserverless4.bk_func set nadkarte = array_replace(nadkarte,NULL,''); 
update qcserverless4.bk_func set ndessen = array_replace(ndessen,NULL,''); 
update qcserverless4.bk_func set personen2 = array_replace(personen2,NULL,''); 
update qcserverless4.bk_func set raeume = array_replace(raeume,NULL,''); 
update qcserverless4.bk_func set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update qcserverless4.bk_func set raummiete = array_replace(raummiete,NULL,''); 
update qcserverless4.bk_func set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update qcserverless4.bk_func set service = array_replace(service,NULL,''); 
update qcserverless4.bk_func set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update qcserverless4.bk_func set sonstiges = array_replace(sonstiges,NULL,''); 
update qcserverless4.bk_func set technik = array_replace(technik,NULL,''); 
update qcserverless4.bk_func set tischform = array_replace(tischform,NULL,''); 
update qcserverless4.bk_func set tischordnung = array_replace(tischordnung,NULL,''); 
update qcserverless4.bk_func set tischplan = array_replace(tischplan,NULL,''); 
update qcserverless4.bk_func set tischreden = array_replace(tischreden,NULL,''); 
update qcserverless4.bk_func set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update qcserverless4.bk_func set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update qcserverless4.bk_func set va_ablauf = array_replace(va_ablauf,NULL,''); 
update qcserverless4.bk_func set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update qcserverless4.bk_func set vip = array_replace(vip,NULL,''); 
update qcserverless4.bk_func set weine = array_replace(weine,NULL,''); 
update qcserverless4.bk_func set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bk_func 
\echo . 
\echo Loading Table bk_package 
\copy qcserverless4.bk_package from '/usr1/dump-qcserverless4-20250812/bk-package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_package__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_package));
\echo Finish Table bk_package 
\echo . 
\echo Loading Table bk_pause 
\copy qcserverless4.bk_pause from '/usr1/dump-qcserverless4-20250812/bk-pause.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_pause__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_pause));
\echo Finish Table bk_pause 
\echo . 
\echo Loading Table bk_rart 
\copy qcserverless4.bk_rart from '/usr1/dump-qcserverless4-20250812/bk-rart.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_rart__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_rart));
\echo Finish Table bk_rart 
\echo . 
\echo Loading Table bk_raum 
\copy qcserverless4.bk_raum from '/usr1/dump-qcserverless4-20250812/bk-raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_raum__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_raum));
\echo Finish Table bk_raum 
\echo . 
\echo Loading Table bk_reser 
\copy qcserverless4.bk_reser from '/usr1/dump-qcserverless4-20250812/bk-reser.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_reser__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_reser));
\echo Finish Table bk_reser 
\echo . 
\echo Loading Table bk_rset 
\copy qcserverless4.bk_rset from '/usr1/dump-qcserverless4-20250812/bk-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_rset__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_rset));
\echo Finish Table bk_rset 
\echo . 
\echo Loading Table bk_setup 
\copy qcserverless4.bk_setup from '/usr1/dump-qcserverless4-20250812/bk-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_setup__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_setup));
\echo Finish Table bk_setup 
\echo . 
\echo Loading Table bk_stat 
\copy qcserverless4.bk_stat from '/usr1/dump-qcserverless4-20250812/bk-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_stat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_stat));
\echo Finish Table bk_stat 
\echo . 
\echo Loading Table bk_veran 
\copy qcserverless4.bk_veran from '/usr1/dump-qcserverless4-20250812/bk-veran.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bk_veran__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bk_veran));
update qcserverless4.bk_veran set payment_userinit = array_replace(payment_userinit,NULL,''); 
\echo Finish Table bk_veran 
\echo . 
\echo Loading Table bl_dates 
\copy qcserverless4.bl_dates from '/usr1/dump-qcserverless4-20250812/bl-dates.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bl_dates__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bl_dates));
\echo Finish Table bl_dates 
\echo . 
\echo Loading Table blinehis 
\copy qcserverless4.blinehis from '/usr1/dump-qcserverless4-20250812/blinehis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.blinehis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.blinehis));
\echo Finish Table blinehis 
\echo . 
\echo Loading Table bresline 
\copy qcserverless4.bresline from '/usr1/dump-qcserverless4-20250812/bresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.bresline__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.bresline));
update qcserverless4.bresline set texte = array_replace(texte,NULL,''); 
\echo Finish Table bresline 
\echo . 
\echo Loading Table brief 
\copy qcserverless4.brief from '/usr1/dump-qcserverless4-20250812/brief.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.brief__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.brief));
\echo Finish Table brief 
\echo . 
\echo Loading Table brieftmp 
\copy qcserverless4.brieftmp from '/usr1/dump-qcserverless4-20250812/brieftmp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.brieftmp__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.brieftmp));
\echo Finish Table brieftmp 
\echo . 
\echo Loading Table briefzei 
\copy qcserverless4.briefzei from '/usr1/dump-qcserverless4-20250812/briefzei.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.briefzei__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.briefzei));
\echo Finish Table briefzei 
\echo . 
\echo Loading Table budget 
\copy qcserverless4.budget from '/usr1/dump-qcserverless4-20250812/budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.budget__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.budget));
\echo Finish Table budget 
\echo . 
\echo Loading Table calls 
\copy qcserverless4.calls from '/usr1/dump-qcserverless4-20250812/calls.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.calls__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.calls));
\echo Finish Table calls 
\echo . 
\echo Loading Table cl_bonus 
\copy qcserverless4.cl_bonus from '/usr1/dump-qcserverless4-20250812/cl-bonus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_bonus__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_bonus));
\echo Finish Table cl_bonus 
\echo . 
\echo Loading Table cl_book 
\copy qcserverless4.cl_book from '/usr1/dump-qcserverless4-20250812/cl-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_book__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_book));
\echo Finish Table cl_book 
\echo . 
\echo Loading Table cl_checkin 
\copy qcserverless4.cl_checkin from '/usr1/dump-qcserverless4-20250812/cl-checkin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_checkin__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_checkin));
\echo Finish Table cl_checkin 
\echo . 
\echo Loading Table cl_class 
\copy qcserverless4.cl_class from '/usr1/dump-qcserverless4-20250812/cl-class.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_class__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_class));
\echo Finish Table cl_class 
\echo . 
\echo Loading Table cl_enroll 
\copy qcserverless4.cl_enroll from '/usr1/dump-qcserverless4-20250812/cl-enroll.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_enroll__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_enroll));
\echo Finish Table cl_enroll 
\echo . 
\echo Loading Table cl_free 
\copy qcserverless4.cl_free from '/usr1/dump-qcserverless4-20250812/cl-free.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_free__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_free));
\echo Finish Table cl_free 
\echo . 
\echo Loading Table cl_histci 
\copy qcserverless4.cl_histci from '/usr1/dump-qcserverless4-20250812/cl-histci.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_histci__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_histci));
\echo Finish Table cl_histci 
\echo . 
\echo Loading Table cl_histpay 
\copy qcserverless4.cl_histpay from '/usr1/dump-qcserverless4-20250812/cl-histpay.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_histpay__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_histpay));
\echo Finish Table cl_histpay 
\echo . 
\echo Loading Table cl_histstatus 
\copy qcserverless4.cl_histstatus from '/usr1/dump-qcserverless4-20250812/cl-histstatus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_histstatus__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_histstatus));
\echo Finish Table cl_histstatus 
\echo . 
\echo Loading Table cl_histtrain 
\copy qcserverless4.cl_histtrain from '/usr1/dump-qcserverless4-20250812/cl-histtrain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_histtrain__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_histtrain));
\echo Finish Table cl_histtrain 
\echo . 
\echo Loading Table cl_histvisit 
\copy qcserverless4.cl_histvisit from '/usr1/dump-qcserverless4-20250812/cl-histvisit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_histvisit__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_histvisit));
\echo Finish Table cl_histvisit 
\echo . 
\echo Loading Table cl_home 
\copy qcserverless4.cl_home from '/usr1/dump-qcserverless4-20250812/cl-home.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_home__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_home));
\echo Finish Table cl_home 
\echo . 
\echo Loading Table cl_location 
\copy qcserverless4.cl_location from '/usr1/dump-qcserverless4-20250812/cl-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_location__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_location));
\echo Finish Table cl_location 
\echo . 
\echo Loading Table cl_locker 
\copy qcserverless4.cl_locker from '/usr1/dump-qcserverless4-20250812/cl-locker.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_locker__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_locker));
\echo Finish Table cl_locker 
\echo . 
\echo Loading Table cl_log 
\copy qcserverless4.cl_log from '/usr1/dump-qcserverless4-20250812/cl-log.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_log__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_log));
\echo Finish Table cl_log 
\echo . 
\echo Loading Table cl_member 
\copy qcserverless4.cl_member from '/usr1/dump-qcserverless4-20250812/cl-member.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_member__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_member));
\echo Finish Table cl_member 
\echo . 
\echo Loading Table cl_memtype 
\copy qcserverless4.cl_memtype from '/usr1/dump-qcserverless4-20250812/cl-memtype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_memtype__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_memtype));
\echo Finish Table cl_memtype 
\echo . 
\echo Loading Table cl_paysched 
\copy qcserverless4.cl_paysched from '/usr1/dump-qcserverless4-20250812/cl-paysched.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_paysched__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_paysched));
\echo Finish Table cl_paysched 
\echo . 
\echo Loading Table cl_stat 
\copy qcserverless4.cl_stat from '/usr1/dump-qcserverless4-20250812/cl-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_stat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_stat));
\echo Finish Table cl_stat 
\echo . 
\echo Loading Table cl_stat1 
\copy qcserverless4.cl_stat1 from '/usr1/dump-qcserverless4-20250812/cl-stat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_stat1__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_stat1));
\echo Finish Table cl_stat1 
\echo . 
\echo Loading Table cl_towel 
\copy qcserverless4.cl_towel from '/usr1/dump-qcserverless4-20250812/cl-towel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_towel__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_towel));
\echo Finish Table cl_towel 
\echo . 
\echo Loading Table cl_trainer 
\copy qcserverless4.cl_trainer from '/usr1/dump-qcserverless4-20250812/cl-trainer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_trainer__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_trainer));
\echo Finish Table cl_trainer 
\echo . 
\echo Loading Table cl_upgrade 
\copy qcserverless4.cl_upgrade from '/usr1/dump-qcserverless4-20250812/cl-upgrade.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cl_upgrade__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cl_upgrade));
\echo Finish Table cl_upgrade 
\echo . 
\echo Loading Table costbudget 
\copy qcserverless4.costbudget from '/usr1/dump-qcserverless4-20250812/costbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.costbudget__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.costbudget));
\echo Finish Table costbudget 
\echo . 
\echo Loading Table counters 
\copy qcserverless4.counters from '/usr1/dump-qcserverless4-20250812/counters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.counters__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.counters));
\echo Finish Table counters 
\echo . 
\echo Loading Table crm_campaign 
\copy qcserverless4.crm_campaign from '/usr1/dump-qcserverless4-20250812/crm-campaign.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_campaign__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_campaign));
\echo Finish Table crm_campaign 
\echo . 
\echo Loading Table crm_category 
\copy qcserverless4.crm_category from '/usr1/dump-qcserverless4-20250812/crm-category.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_category__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_category));
\echo Finish Table crm_category 
\echo . 
\echo Loading Table crm_dept 
\copy qcserverless4.crm_dept from '/usr1/dump-qcserverless4-20250812/crm-dept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_dept__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_dept));
\echo Finish Table crm_dept 
\echo . 
\echo Loading Table crm_dtl 
\copy qcserverless4.crm_dtl from '/usr1/dump-qcserverless4-20250812/crm-dtl.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_dtl__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_dtl));
\echo Finish Table crm_dtl 
\echo . 
\echo Loading Table crm_email 
\copy qcserverless4.crm_email from '/usr1/dump-qcserverless4-20250812/crm-email.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_email__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_email));
\echo Finish Table crm_email 
\echo . 
\echo Loading Table crm_event 
\copy qcserverless4.crm_event from '/usr1/dump-qcserverless4-20250812/crm-event.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_event__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_event));
\echo Finish Table crm_event 
\echo . 
\echo Loading Table crm_feedhdr 
\copy qcserverless4.crm_feedhdr from '/usr1/dump-qcserverless4-20250812/crm-feedhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_feedhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_feedhdr));
\echo Finish Table crm_feedhdr 
\echo . 
\echo Loading Table crm_fnlresult 
\copy qcserverless4.crm_fnlresult from '/usr1/dump-qcserverless4-20250812/crm-fnlresult.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_fnlresult__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_fnlresult));
\echo Finish Table crm_fnlresult 
\echo . 
\echo Loading Table crm_language 
\copy qcserverless4.crm_language from '/usr1/dump-qcserverless4-20250812/crm-language.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_language__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_language));
\echo Finish Table crm_language 
\echo . 
\echo Loading Table crm_question 
\copy qcserverless4.crm_question from '/usr1/dump-qcserverless4-20250812/crm-question.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_question__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_question));
\echo Finish Table crm_question 
\echo . 
\echo Loading Table crm_tamplang 
\copy qcserverless4.crm_tamplang from '/usr1/dump-qcserverless4-20250812/crm-tamplang.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_tamplang__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_tamplang));
\echo Finish Table crm_tamplang 
\echo . 
\echo Loading Table crm_template 
\copy qcserverless4.crm_template from '/usr1/dump-qcserverless4-20250812/crm-template.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.crm_template__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.crm_template));
\echo Finish Table crm_template 
\echo . 
\echo Loading Table cross_dtl 
\copy qcserverless4.cross_dtl from '/usr1/dump-qcserverless4-20250812/cross-DTL.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cross_dtl__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cross_dtl));
\echo Finish Table cross_dtl 
\echo . 
\echo Loading Table cross_hdr 
\copy qcserverless4.cross_hdr from '/usr1/dump-qcserverless4-20250812/cross-HDR.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.cross_hdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.cross_hdr));
\echo Finish Table cross_hdr 
\echo . 
\echo Loading Table debitor 
\copy qcserverless4.debitor from '/usr1/dump-qcserverless4-20250812/debitor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.debitor__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.debitor));
\echo Finish Table debitor 
\echo . 
\echo Loading Table debthis 
\copy qcserverless4.debthis from '/usr1/dump-qcserverless4-20250812/debthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.debthis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.debthis));
\echo Finish Table debthis 
\echo . 
\echo Loading Table desttext 
\copy qcserverless4.desttext from '/usr1/dump-qcserverless4-20250812/desttext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.desttext__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.desttext));
\echo Finish Table desttext 
\echo . 
\echo Loading Table dml_art 
\copy qcserverless4.dml_art from '/usr1/dump-qcserverless4-20250812/dml-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.dml_art__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.dml_art));
\echo Finish Table dml_art 
\echo . 
\echo Loading Table dml_artdep 
\copy qcserverless4.dml_artdep from '/usr1/dump-qcserverless4-20250812/dml-artdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.dml_artdep__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.dml_artdep));
\echo Finish Table dml_artdep 
\echo . 
\echo Loading Table dml_rate 
\copy qcserverless4.dml_rate from '/usr1/dump-qcserverless4-20250812/dml-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.dml_rate__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.dml_rate));
\echo Finish Table dml_rate 
\echo . 
\echo Loading Table eg_action 
\copy qcserverless4.eg_action from '/usr1/dump-qcserverless4-20250812/eg-action.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_action__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_action));
\echo Finish Table eg_action 
\echo . 
\echo Loading Table eg_alert 
\copy qcserverless4.eg_alert from '/usr1/dump-qcserverless4-20250812/eg-Alert.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_alert__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_alert));
\echo Finish Table eg_alert 
\echo . 
\echo Loading Table eg_budget 
\copy qcserverless4.eg_budget from '/usr1/dump-qcserverless4-20250812/eg-budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_budget__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_budget));
\echo Finish Table eg_budget 
\echo . 
\echo Loading Table eg_cost 
\copy qcserverless4.eg_cost from '/usr1/dump-qcserverless4-20250812/eg-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_cost__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_cost));
\echo Finish Table eg_cost 
\echo . 
\echo Loading Table eg_duration 
\copy qcserverless4.eg_duration from '/usr1/dump-qcserverless4-20250812/eg-Duration.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_duration__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_duration));
\echo Finish Table eg_duration 
\echo . 
\echo Loading Table eg_location 
\copy qcserverless4.eg_location from '/usr1/dump-qcserverless4-20250812/eg-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_location__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_location));
\echo Finish Table eg_location 
\echo . 
\echo Loading Table eg_mainstat 
\copy qcserverless4.eg_mainstat from '/usr1/dump-qcserverless4-20250812/eg-MainStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_mainstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_mainstat));
\echo Finish Table eg_mainstat 
\echo . 
\echo Loading Table eg_maintain 
\copy qcserverless4.eg_maintain from '/usr1/dump-qcserverless4-20250812/eg-maintain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_maintain__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_maintain));
\echo Finish Table eg_maintain 
\echo . 
\echo Loading Table eg_mdetail 
\copy qcserverless4.eg_mdetail from '/usr1/dump-qcserverless4-20250812/eg-mdetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_mdetail__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_mdetail));
\echo Finish Table eg_mdetail 
\echo . 
\echo Loading Table eg_messageno 
\copy qcserverless4.eg_messageno from '/usr1/dump-qcserverless4-20250812/eg-MessageNo.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_messageno__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_messageno));
\echo Finish Table eg_messageno 
\echo . 
\echo Loading Table eg_mobilenr 
\copy qcserverless4.eg_mobilenr from '/usr1/dump-qcserverless4-20250812/eg-mobileNr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_mobilenr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_mobilenr));
\echo Finish Table eg_mobilenr 
\echo . 
\echo Loading Table eg_moveproperty 
\copy qcserverless4.eg_moveproperty from '/usr1/dump-qcserverless4-20250812/eg-moveProperty.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_moveproperty__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_moveproperty));
\echo Finish Table eg_moveproperty 
\echo . 
\echo Loading Table eg_property 
\copy qcserverless4.eg_property from '/usr1/dump-qcserverless4-20250812/eg-property.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_property__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_property));
\echo Finish Table eg_property 
\echo . 
\echo Loading Table eg_propmeter 
\copy qcserverless4.eg_propmeter from '/usr1/dump-qcserverless4-20250812/eg-propMeter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_propmeter__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_propmeter));
\echo Finish Table eg_propmeter 
\echo . 
\echo Loading Table eg_queasy 
\copy qcserverless4.eg_queasy from '/usr1/dump-qcserverless4-20250812/eg-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_queasy));
\echo Finish Table eg_queasy 
\echo . 
\echo Loading Table eg_reqdetail 
\copy qcserverless4.eg_reqdetail from '/usr1/dump-qcserverless4-20250812/eg-reqDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_reqdetail__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_reqdetail));
\echo Finish Table eg_reqdetail 
\echo . 
\echo Loading Table eg_reqif 
\copy qcserverless4.eg_reqif from '/usr1/dump-qcserverless4-20250812/eg-reqif.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_reqif__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_reqif));
\echo Finish Table eg_reqif 
\echo . 
\echo Loading Table eg_reqstat 
\copy qcserverless4.eg_reqstat from '/usr1/dump-qcserverless4-20250812/eg-ReqStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_reqstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_reqstat));
\echo Finish Table eg_reqstat 
\echo . 
\echo Loading Table eg_request 
\copy qcserverless4.eg_request from '/usr1/dump-qcserverless4-20250812/eg-request.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_request__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_request));
\echo Finish Table eg_request 
\echo . 
\echo Loading Table eg_resources 
\copy qcserverless4.eg_resources from '/usr1/dump-qcserverless4-20250812/eg-resources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_resources__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_resources));
\echo Finish Table eg_resources 
\echo . 
\echo Loading Table eg_staff 
\copy qcserverless4.eg_staff from '/usr1/dump-qcserverless4-20250812/eg-staff.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_staff__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_staff));
\echo Finish Table eg_staff 
\echo . 
\echo Loading Table eg_stat 
\copy qcserverless4.eg_stat from '/usr1/dump-qcserverless4-20250812/eg-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_stat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_stat));
\echo Finish Table eg_stat 
\echo . 
\echo Loading Table eg_subtask 
\copy qcserverless4.eg_subtask from '/usr1/dump-qcserverless4-20250812/eg-subtask.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_subtask__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_subtask));
\echo Finish Table eg_subtask 
\echo . 
\echo Loading Table eg_vendor 
\copy qcserverless4.eg_vendor from '/usr1/dump-qcserverless4-20250812/eg-vendor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_vendor__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_vendor));
\echo Finish Table eg_vendor 
\echo . 
\echo Loading Table eg_vperform 
\copy qcserverless4.eg_vperform from '/usr1/dump-qcserverless4-20250812/eg-vperform.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.eg_vperform__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.eg_vperform));
\echo Finish Table eg_vperform 
\echo . 
\echo Loading Table ekum 
\copy qcserverless4.ekum from '/usr1/dump-qcserverless4-20250812/ekum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.ekum__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.ekum));
\echo Finish Table ekum 
\echo . 
\echo Loading Table employee 
\copy qcserverless4.employee from '/usr1/dump-qcserverless4-20250812/employee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.employee__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.employee));
update qcserverless4.employee set child = array_replace(child,NULL,''); 
\echo Finish Table employee 
\echo . 
\echo Loading Table equiplan 
\copy qcserverless4.equiplan from '/usr1/dump-qcserverless4-20250812/equiplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.equiplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.equiplan));
\echo Finish Table equiplan 
\echo . 
\echo Loading Table exrate 
\copy qcserverless4.exrate from '/usr1/dump-qcserverless4-20250812/exrate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.exrate__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.exrate));
\echo Finish Table exrate 
\echo . 
\echo Loading Table fa_artikel 
\copy qcserverless4.fa_artikel from '/usr1/dump-qcserverless4-20250812/fa-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_artikel));
\echo Finish Table fa_artikel 
\echo . 
\echo Loading Table fa_counter 
\copy qcserverless4.fa_counter from '/usr1/dump-qcserverless4-20250812/fa-Counter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_counter__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_counter));
\echo Finish Table fa_counter 
\echo . 
\echo Loading Table fa_dp 
\copy qcserverless4.fa_dp from '/usr1/dump-qcserverless4-20250812/fa-DP.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_dp__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_dp));
\echo Finish Table fa_dp 
\echo . 
\echo Loading Table fa_grup 
\copy qcserverless4.fa_grup from '/usr1/dump-qcserverless4-20250812/fa-grup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_grup__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_grup));
\echo Finish Table fa_grup 
\echo . 
\echo Loading Table fa_kateg 
\copy qcserverless4.fa_kateg from '/usr1/dump-qcserverless4-20250812/fa-kateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_kateg__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_kateg));
\echo Finish Table fa_kateg 
\echo . 
\echo Loading Table fa_lager 
\copy qcserverless4.fa_lager from '/usr1/dump-qcserverless4-20250812/fa-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_lager__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_lager));
\echo Finish Table fa_lager 
\echo . 
\echo Loading Table fa_op 
\copy qcserverless4.fa_op from '/usr1/dump-qcserverless4-20250812/fa-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_op__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_op));
\echo Finish Table fa_op 
\echo . 
\echo Loading Table fa_order 
\copy qcserverless4.fa_order from '/usr1/dump-qcserverless4-20250812/fa-Order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_order__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_order));
\echo Finish Table fa_order 
\echo . 
\echo Loading Table fa_ordheader 
\copy qcserverless4.fa_ordheader from '/usr1/dump-qcserverless4-20250812/fa-OrdHeader.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_ordheader__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_ordheader));
\echo Finish Table fa_ordheader 
\echo . 
\echo Loading Table fa_quodetail 
\copy qcserverless4.fa_quodetail from '/usr1/dump-qcserverless4-20250812/fa-QuoDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_quodetail__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_quodetail));
\echo Finish Table fa_quodetail 
\echo . 
\echo Loading Table fa_quotation 
\copy qcserverless4.fa_quotation from '/usr1/dump-qcserverless4-20250812/fa-quotation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_quotation__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_quotation));
\echo Finish Table fa_quotation 
\echo . 
\echo Loading Table fa_user 
\copy qcserverless4.fa_user from '/usr1/dump-qcserverless4-20250812/fa-user.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fa_user__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fa_user));
update qcserverless4.fa_user set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table fa_user 
\echo . 
\echo Loading Table fbstat 
\copy qcserverless4.fbstat from '/usr1/dump-qcserverless4-20250812/fbstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fbstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fbstat));
\echo Finish Table fbstat 
\echo . 
\echo Loading Table feiertag 
\copy qcserverless4.feiertag from '/usr1/dump-qcserverless4-20250812/feiertag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.feiertag__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.feiertag));
\echo Finish Table feiertag 
\echo . 
\echo Loading Table ffont 
\copy qcserverless4.ffont from '/usr1/dump-qcserverless4-20250812/ffont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.ffont__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.ffont));
\echo Finish Table ffont 
\echo . 
\echo Loading Table fixleist 
\copy qcserverless4.fixleist from '/usr1/dump-qcserverless4-20250812/fixleist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.fixleist__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.fixleist));
\echo Finish Table fixleist 
\echo . 
\echo Loading Table gc_giro 
\copy qcserverless4.gc_giro from '/usr1/dump-qcserverless4-20250812/gc-giro.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gc_giro__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gc_giro));
update qcserverless4.gc_giro set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_giro 
\echo . 
\echo Loading Table gc_jouhdr 
\copy qcserverless4.gc_jouhdr from '/usr1/dump-qcserverless4-20250812/gc-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gc_jouhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gc_jouhdr));
\echo Finish Table gc_jouhdr 
\echo . 
\echo Loading Table gc_journal 
\copy qcserverless4.gc_journal from '/usr1/dump-qcserverless4-20250812/gc-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gc_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gc_journal));
\echo Finish Table gc_journal 
\echo . 
\echo Loading Table gc_pi 
\copy qcserverless4.gc_pi from '/usr1/dump-qcserverless4-20250812/gc-PI.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gc_pi__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gc_pi));
update qcserverless4.gc_pi set bez_array = array_replace(bez_array,NULL,''); 
update qcserverless4.gc_pi set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_pi 
\echo . 
\echo Loading Table gc_piacct 
\copy qcserverless4.gc_piacct from '/usr1/dump-qcserverless4-20250812/gc-piacct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gc_piacct__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gc_piacct));
\echo Finish Table gc_piacct 
\echo . 
\echo Loading Table gc_pibline 
\copy qcserverless4.gc_pibline from '/usr1/dump-qcserverless4-20250812/gc-PIbline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gc_pibline__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gc_pibline));
\echo Finish Table gc_pibline 
\echo . 
\echo Loading Table gc_pitype 
\copy qcserverless4.gc_pitype from '/usr1/dump-qcserverless4-20250812/gc-piType.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gc_pitype__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gc_pitype));
\echo Finish Table gc_pitype 
\echo . 
\echo Loading Table genfcast 
\copy qcserverless4.genfcast from '/usr1/dump-qcserverless4-20250812/genfcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.genfcast__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.genfcast));
update qcserverless4.genfcast set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genfcast 
\echo . 
\echo Loading Table genlayout 
\copy qcserverless4.genlayout from '/usr1/dump-qcserverless4-20250812/genlayout.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.genlayout__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.genlayout));
update qcserverless4.genlayout set button_ext = array_replace(button_ext,NULL,''); 
update qcserverless4.genlayout set char_ext = array_replace(char_ext,NULL,''); 
update qcserverless4.genlayout set combo_ext = array_replace(combo_ext,NULL,''); 
update qcserverless4.genlayout set date_ext = array_replace(date_ext,NULL,''); 
update qcserverless4.genlayout set deci_ext = array_replace(deci_ext,NULL,''); 
update qcserverless4.genlayout set inte_ext = array_replace(inte_ext,NULL,''); 
update qcserverless4.genlayout set logi_ext = array_replace(logi_ext,NULL,''); 
update qcserverless4.genlayout set string_ext = array_replace(string_ext,NULL,''); 
update qcserverless4.genlayout set tchar_ext = array_replace(tchar_ext,NULL,''); 
update qcserverless4.genlayout set tdate_ext = array_replace(tdate_ext,NULL,''); 
update qcserverless4.genlayout set tdeci_ext = array_replace(tdeci_ext,NULL,''); 
update qcserverless4.genlayout set tinte_ext = array_replace(tinte_ext,NULL,''); 
update qcserverless4.genlayout set tlogi_ext = array_replace(tlogi_ext,NULL,''); 
\echo Finish Table genlayout 
\echo . 
\echo Loading Table genstat 
\copy qcserverless4.genstat from '/usr1/dump-qcserverless4-20250812/genstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.genstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.genstat));
update qcserverless4.genstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genstat 
\echo . 
\echo Loading Table gentable 
\copy qcserverless4.gentable from '/usr1/dump-qcserverless4-20250812/gentable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gentable__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gentable));
update qcserverless4.gentable set char_ext = array_replace(char_ext,NULL,''); 
update qcserverless4.gentable set combo_ext = array_replace(combo_ext,NULL,''); 
\echo Finish Table gentable 
\echo . 
\echo Loading Table gk_field 
\copy qcserverless4.gk_field from '/usr1/dump-qcserverless4-20250812/gk-field.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gk_field__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gk_field));
\echo Finish Table gk_field 
\echo . 
\echo Loading Table gk_label 
\copy qcserverless4.gk_label from '/usr1/dump-qcserverless4-20250812/gk-label.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gk_label__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gk_label));
\echo Finish Table gk_label 
\echo . 
\echo Loading Table gk_notes 
\copy qcserverless4.gk_notes from '/usr1/dump-qcserverless4-20250812/gk-notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gk_notes__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gk_notes));
update qcserverless4.gk_notes set notes = array_replace(notes,NULL,''); 
\echo Finish Table gk_notes 
\echo . 
\echo Loading Table gl_acct 
\copy qcserverless4.gl_acct from '/usr1/dump-qcserverless4-20250812/gl-acct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_acct__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_acct));
\echo Finish Table gl_acct 
\echo . 
\echo Loading Table gl_accthis 
\copy qcserverless4.gl_accthis from '/usr1/dump-qcserverless4-20250812/gl-accthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_accthis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_accthis));
\echo Finish Table gl_accthis 
\echo . 
\echo Loading Table gl_coa 
\copy qcserverless4.gl_coa from '/usr1/dump-qcserverless4-20250812/gl-coa.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_coa__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_coa));
\echo Finish Table gl_coa 
\echo . 
\echo Loading Table gl_cost 
\copy qcserverless4.gl_cost from '/usr1/dump-qcserverless4-20250812/gl-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_cost__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_cost));
\echo Finish Table gl_cost 
\echo . 
\echo Loading Table gl_department 
\copy qcserverless4.gl_department from '/usr1/dump-qcserverless4-20250812/gl-department.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_department__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_department));
\echo Finish Table gl_department 
\echo . 
\echo Loading Table gl_fstype 
\copy qcserverless4.gl_fstype from '/usr1/dump-qcserverless4-20250812/gl-fstype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_fstype__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_fstype));
\echo Finish Table gl_fstype 
\echo . 
\echo Loading Table gl_htljournal 
\copy qcserverless4.gl_htljournal from '/usr1/dump-qcserverless4-20250812/gl-htljournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_htljournal__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_htljournal));
\echo Finish Table gl_htljournal 
\echo . 
\echo Loading Table gl_jhdrhis 
\copy qcserverless4.gl_jhdrhis from '/usr1/dump-qcserverless4-20250812/gl-jhdrhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_jhdrhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_jhdrhis));
\echo Finish Table gl_jhdrhis 
\echo . 
\echo Loading Table gl_jouhdr 
\copy qcserverless4.gl_jouhdr from '/usr1/dump-qcserverless4-20250812/gl-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_jouhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_jouhdr));
\echo Finish Table gl_jouhdr 
\echo . 
\echo Loading Table gl_jourhis 
\copy qcserverless4.gl_jourhis from '/usr1/dump-qcserverless4-20250812/gl-jourhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_jourhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_jourhis));
\echo Finish Table gl_jourhis 
\echo . 
\echo Loading Table gl_journal 
\copy qcserverless4.gl_journal from '/usr1/dump-qcserverless4-20250812/gl-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_journal));
\echo Finish Table gl_journal 
\echo . 
\echo Loading Table gl_main 
\copy qcserverless4.gl_main from '/usr1/dump-qcserverless4-20250812/gl-main.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.gl_main__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.gl_main));
\echo Finish Table gl_main 
\echo . 
\echo Loading Table golf_caddie 
\copy qcserverless4.golf_caddie from '/usr1/dump-qcserverless4-20250812/golf-caddie.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_caddie__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_caddie));
\echo Finish Table golf_caddie 
\echo . 
\echo Loading Table golf_caddie_assignment 
\copy qcserverless4.golf_caddie_assignment from '/usr1/dump-qcserverless4-20250812/golf-caddie-assignment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_caddie_assignment__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_caddie_assignment));
\echo Finish Table golf_caddie_assignment 
\echo . 
\echo Loading Table golf_course 
\copy qcserverless4.golf_course from '/usr1/dump-qcserverless4-20250812/golf-course.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_course__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_course));
\echo Finish Table golf_course 
\echo . 
\echo Loading Table golf_flight_reservation 
\copy qcserverless4.golf_flight_reservation from '/usr1/dump-qcserverless4-20250812/golf-flight-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_flight_reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_flight_reservation));
\echo Finish Table golf_flight_reservation 
\echo . 
\echo Loading Table golf_flight_reservation_hist 
\copy qcserverless4.golf_flight_reservation_hist from '/usr1/dump-qcserverless4-20250812/golf-flight-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_flight_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_flight_reservation_hist));
\echo Finish Table golf_flight_reservation_hist 
\echo . 
\echo Loading Table golf_golfer_reservation 
\copy qcserverless4.golf_golfer_reservation from '/usr1/dump-qcserverless4-20250812/golf-golfer-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_golfer_reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_golfer_reservation));
\echo Finish Table golf_golfer_reservation 
\echo . 
\echo Loading Table golf_golfer_reservation_hist 
\copy qcserverless4.golf_golfer_reservation_hist from '/usr1/dump-qcserverless4-20250812/golf-golfer-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_golfer_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_golfer_reservation_hist));
\echo Finish Table golf_golfer_reservation_hist 
\echo . 
\echo Loading Table golf_holiday 
\copy qcserverless4.golf_holiday from '/usr1/dump-qcserverless4-20250812/golf-holiday.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_holiday__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_holiday));
\echo Finish Table golf_holiday 
\echo . 
\echo Loading Table golf_main_reservation 
\copy qcserverless4.golf_main_reservation from '/usr1/dump-qcserverless4-20250812/golf-main-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_main_reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_main_reservation));
\echo Finish Table golf_main_reservation 
\echo . 
\echo Loading Table golf_main_reservation_hist 
\copy qcserverless4.golf_main_reservation_hist from '/usr1/dump-qcserverless4-20250812/golf-main-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_main_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_main_reservation_hist));
\echo Finish Table golf_main_reservation_hist 
\echo . 
\echo Loading Table golf_rate 
\copy qcserverless4.golf_rate from '/usr1/dump-qcserverless4-20250812/golf-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_rate__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_rate));
\echo Finish Table golf_rate 
\echo . 
\echo Loading Table golf_shift 
\copy qcserverless4.golf_shift from '/usr1/dump-qcserverless4-20250812/golf-shift.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_shift__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_shift));
\echo Finish Table golf_shift 
\echo . 
\echo Loading Table golf_transfer 
\copy qcserverless4.golf_transfer from '/usr1/dump-qcserverless4-20250812/golf-transfer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.golf_transfer__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.golf_transfer));
\echo Finish Table golf_transfer 
\echo . 
\echo Loading Table guest 
\copy qcserverless4.guest from '/usr1/dump-qcserverless4-20250812/guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guest__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guest));
update qcserverless4.guest set notizen = array_replace(notizen,NULL,''); 
update qcserverless4.guest set vornamekind = array_replace(vornamekind,NULL,''); 
\echo Finish Table guest 
\echo . 
\echo Loading Table guest_pr 
\copy qcserverless4.guest_pr from '/usr1/dump-qcserverless4-20250812/guest-pr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guest_pr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guest_pr));
\echo Finish Table guest_pr 
\echo . 
\echo Loading Table guest_queasy 
\copy qcserverless4.guest_queasy from '/usr1/dump-qcserverless4-20250812/guest-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guest_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guest_queasy));
\echo Finish Table guest_queasy 
\echo . 
\echo Loading Table guest_remark 
\copy qcserverless4.guest_remark from '/usr1/dump-qcserverless4-20250812/guest-remark.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guest_remark__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guest_remark));
update qcserverless4.guest_remark set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table guest_remark 
\echo . 
\echo Loading Table guestat 
\copy qcserverless4.guestat from '/usr1/dump-qcserverless4-20250812/guestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guestat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guestat));
\echo Finish Table guestat 
\echo . 
\echo Loading Table guestat1 
\copy qcserverless4.guestat1 from '/usr1/dump-qcserverless4-20250812/guestat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guestat1__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guestat1));
\echo Finish Table guestat1 
\echo . 
\echo Loading Table guestbook 
\copy qcserverless4.guestbook from '/usr1/dump-qcserverless4-20250812/guestbook.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guestbook__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guestbook));
update qcserverless4.guestbook set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table guestbook 
\echo . 
\echo Loading Table guestbud 
\copy qcserverless4.guestbud from '/usr1/dump-qcserverless4-20250812/guestbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guestbud__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guestbud));
\echo Finish Table guestbud 
\echo . 
\echo Loading Table guestseg 
\copy qcserverless4.guestseg from '/usr1/dump-qcserverless4-20250812/guestseg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.guestseg__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.guestseg));
\echo Finish Table guestseg 
\echo . 
\echo Loading Table h_artcost 
\copy qcserverless4.h_artcost from '/usr1/dump-qcserverless4-20250812/h-artcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_artcost__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_artcost));
\echo Finish Table h_artcost 
\echo . 
\echo Loading Table h_artikel 
\copy qcserverless4.h_artikel from '/usr1/dump-qcserverless4-20250812/h-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_artikel));
\echo Finish Table h_artikel 
\echo . 
\echo Loading Table h_bill 
\copy qcserverless4.h_bill from '/usr1/dump-qcserverless4-20250812/h-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_bill__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_bill));
\echo Finish Table h_bill 
\echo . 
\echo Loading Table h_bill_line 
\copy qcserverless4.h_bill_line from '/usr1/dump-qcserverless4-20250812/h-bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_bill_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_bill_line));
\echo Finish Table h_bill_line 
\echo . 
\echo Loading Table h_compli 
\copy qcserverless4.h_compli from '/usr1/dump-qcserverless4-20250812/h-compli.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_compli__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_compli));
\echo Finish Table h_compli 
\echo . 
\echo Loading Table h_cost 
\copy qcserverless4.h_cost from '/usr1/dump-qcserverless4-20250812/h-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_cost__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_cost));
\echo Finish Table h_cost 
\echo . 
\echo Loading Table h_journal 
\copy qcserverless4.h_journal from '/usr1/dump-qcserverless4-20250812/h-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_journal));
\echo Finish Table h_journal 
\echo . 
\echo Loading Table h_menu 
\copy qcserverless4.h_menu from '/usr1/dump-qcserverless4-20250812/h-menu.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_menu__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_menu));
\echo Finish Table h_menu 
\echo . 
\echo Loading Table h_mjourn 
\copy qcserverless4.h_mjourn from '/usr1/dump-qcserverless4-20250812/h-mjourn.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_mjourn__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_mjourn));
\echo Finish Table h_mjourn 
\echo . 
\echo Loading Table h_oldjou 
\copy qcserverless4.h_oldjou from '/usr1/dump-qcserverless4-20250812/h-oldjou.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_oldjou__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_oldjou));
\echo Finish Table h_oldjou 
\echo . 
\echo Loading Table h_order 
\copy qcserverless4.h_order from '/usr1/dump-qcserverless4-20250812/h-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_order__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_order));
update qcserverless4.h_order set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table h_order 
\echo . 
\echo Loading Table h_queasy 
\copy qcserverless4.h_queasy from '/usr1/dump-qcserverless4-20250812/h-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_queasy));
\echo Finish Table h_queasy 
\echo . 
\echo Loading Table h_rezept 
\copy qcserverless4.h_rezept from '/usr1/dump-qcserverless4-20250812/h-rezept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_rezept__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_rezept));
\echo Finish Table h_rezept 
\echo . 
\echo Loading Table h_rezlin 
\copy qcserverless4.h_rezlin from '/usr1/dump-qcserverless4-20250812/h-rezlin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_rezlin__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_rezlin));
\echo Finish Table h_rezlin 
\echo . 
\echo Loading Table h_storno 
\copy qcserverless4.h_storno from '/usr1/dump-qcserverless4-20250812/h-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_storno__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_storno));
\echo Finish Table h_storno 
\echo . 
\echo Loading Table h_umsatz 
\copy qcserverless4.h_umsatz from '/usr1/dump-qcserverless4-20250812/h-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.h_umsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.h_umsatz));
\echo Finish Table h_umsatz 
\echo . 
\echo Loading Table history 
\copy qcserverless4.history from '/usr1/dump-qcserverless4-20250812/history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.history__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.history));
\echo Finish Table history 
\echo . 
\echo Loading Table hoteldpt 
\copy qcserverless4.hoteldpt from '/usr1/dump-qcserverless4-20250812/hoteldpt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.hoteldpt__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.hoteldpt));
\echo Finish Table hoteldpt 
\echo . 
\echo Loading Table hrbeleg 
\copy qcserverless4.hrbeleg from '/usr1/dump-qcserverless4-20250812/hrbeleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.hrbeleg__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.hrbeleg));
\echo Finish Table hrbeleg 
\echo . 
\echo Loading Table hrsegement 
\copy qcserverless4.hrsegement from '/usr1/dump-qcserverless4-20250812/hrsegement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.hrsegement__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.hrsegement));
\echo Finish Table hrsegement 
\echo . 
\echo Loading Table htparam 
\copy qcserverless4.htparam from '/usr1/dump-qcserverless4-20250812/htparam.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.htparam__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.htparam));
\echo Finish Table htparam 
\echo . 
\echo Loading Table htreport 
\copy qcserverless4.htreport from '/usr1/dump-qcserverless4-20250812/htreport.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.htreport__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.htreport));
\echo Finish Table htreport 
\echo . 
\echo Loading Table iftable 
\copy qcserverless4.iftable from '/usr1/dump-qcserverless4-20250812/iftable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.iftable__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.iftable));
\echo Finish Table iftable 
\echo . 
\echo Loading Table interface 
\copy qcserverless4.interface from '/usr1/dump-qcserverless4-20250812/interface.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.interface__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.interface));
\echo Finish Table interface 
\echo . 
\echo Loading Table k_history 
\copy qcserverless4.k_history from '/usr1/dump-qcserverless4-20250812/k-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.k_history__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.k_history));
\echo Finish Table k_history 
\echo . 
\echo Loading Table kabine 
\copy qcserverless4.kabine from '/usr1/dump-qcserverless4-20250812/kabine.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kabine__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kabine));
\echo Finish Table kabine 
\echo . 
\echo Loading Table kalender 
\copy qcserverless4.kalender from '/usr1/dump-qcserverless4-20250812/kalender.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kalender__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kalender));
update qcserverless4.kalender set note = array_replace(note,NULL,''); 
\echo Finish Table kalender 
\echo . 
\echo Loading Table kasse 
\copy qcserverless4.kasse from '/usr1/dump-qcserverless4-20250812/kasse.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kasse__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kasse));
\echo Finish Table kasse 
\echo . 
\echo Loading Table katpreis 
\copy qcserverless4.katpreis from '/usr1/dump-qcserverless4-20250812/katpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.katpreis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.katpreis));
\echo Finish Table katpreis 
\echo . 
\echo Loading Table kellne1 
\copy qcserverless4.kellne1 from '/usr1/dump-qcserverless4-20250812/kellne1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kellne1__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kellne1));
\echo Finish Table kellne1 
\echo . 
\echo Loading Table kellner 
\copy qcserverless4.kellner from '/usr1/dump-qcserverless4-20250812/kellner.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kellner__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kellner));
\echo Finish Table kellner 
\echo . 
\echo Loading Table kontakt 
\copy qcserverless4.kontakt from '/usr1/dump-qcserverless4-20250812/kontakt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kontakt__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kontakt));
\echo Finish Table kontakt 
\echo . 
\echo Loading Table kontline 
\copy qcserverless4.kontline from '/usr1/dump-qcserverless4-20250812/kontline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kontline__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kontline));
\echo Finish Table kontline 
\echo . 
\echo Loading Table kontlink 
\copy qcserverless4.kontlink from '/usr1/dump-qcserverless4-20250812/kontlink.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kontlink__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kontlink));
\echo Finish Table kontlink 
\echo . 
\echo Loading Table kontplan 
\copy qcserverless4.kontplan from '/usr1/dump-qcserverless4-20250812/kontplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kontplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kontplan));
\echo Finish Table kontplan 
\echo . 
\echo Loading Table kontstat 
\copy qcserverless4.kontstat from '/usr1/dump-qcserverless4-20250812/kontstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kontstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kontstat));
update qcserverless4.kontstat set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table kontstat 
\echo . 
\echo Loading Table kresline 
\copy qcserverless4.kresline from '/usr1/dump-qcserverless4-20250812/kresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.kresline__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.kresline));
\echo Finish Table kresline 
\echo . 
\echo Loading Table l_artikel 
\copy qcserverless4.l_artikel from '/usr1/dump-qcserverless4-20250812/l-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_artikel));
update qcserverless4.l_artikel set lief_artnr = array_replace(lief_artnr,NULL,''); 
\echo Finish Table l_artikel 
\echo . 
\echo Loading Table l_bestand 
\copy qcserverless4.l_bestand from '/usr1/dump-qcserverless4-20250812/l-bestand.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_bestand__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_bestand));
\echo Finish Table l_bestand 
\echo . 
\echo Loading Table l_besthis 
\copy qcserverless4.l_besthis from '/usr1/dump-qcserverless4-20250812/l-besthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_besthis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_besthis));
\echo Finish Table l_besthis 
\echo . 
\echo Loading Table l_hauptgrp 
\copy qcserverless4.l_hauptgrp from '/usr1/dump-qcserverless4-20250812/l-hauptgrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_hauptgrp__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_hauptgrp));
\echo Finish Table l_hauptgrp 
\echo . 
\echo Loading Table l_kredit 
\copy qcserverless4.l_kredit from '/usr1/dump-qcserverless4-20250812/l-kredit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_kredit__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_kredit));
\echo Finish Table l_kredit 
\echo . 
\echo Loading Table l_lager 
\copy qcserverless4.l_lager from '/usr1/dump-qcserverless4-20250812/l-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_lager__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_lager));
\echo Finish Table l_lager 
\echo . 
\echo Loading Table l_lieferant 
\copy qcserverless4.l_lieferant from '/usr1/dump-qcserverless4-20250812/l-lieferant.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_lieferant__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_lieferant));
update qcserverless4.l_lieferant set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table l_lieferant 
\echo . 
\echo Loading Table l_liefumsatz 
\copy qcserverless4.l_liefumsatz from '/usr1/dump-qcserverless4-20250812/l-liefumsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_liefumsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_liefumsatz));
\echo Finish Table l_liefumsatz 
\echo . 
\echo Loading Table l_op 
\copy qcserverless4.l_op from '/usr1/dump-qcserverless4-20250812/l-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_op__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_op));
\echo Finish Table l_op 
\echo . 
\echo Loading Table l_ophdr 
\copy qcserverless4.l_ophdr from '/usr1/dump-qcserverless4-20250812/l-ophdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_ophdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_ophdr));
\echo Finish Table l_ophdr 
\echo . 
\echo Loading Table l_ophhis 
\copy qcserverless4.l_ophhis from '/usr1/dump-qcserverless4-20250812/l-ophhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_ophhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_ophhis));
\echo Finish Table l_ophhis 
\echo . 
\echo Loading Table l_ophis 
\copy qcserverless4.l_ophis from '/usr1/dump-qcserverless4-20250812/l-ophis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_ophis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_ophis));
\echo Finish Table l_ophis 
\echo . 
\echo Loading Table l_order 
\copy qcserverless4.l_order from '/usr1/dump-qcserverless4-20250812/l-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_order__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_order));
update qcserverless4.l_order set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_order 
\echo . 
\echo Loading Table l_orderhdr 
\copy qcserverless4.l_orderhdr from '/usr1/dump-qcserverless4-20250812/l-orderhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_orderhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_orderhdr));
update qcserverless4.l_orderhdr set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_orderhdr 
\echo . 
\echo Loading Table l_pprice 
\copy qcserverless4.l_pprice from '/usr1/dump-qcserverless4-20250812/l-pprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_pprice__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_pprice));
\echo Finish Table l_pprice 
\echo . 
\echo Loading Table l_quote 
\copy qcserverless4.l_quote from '/usr1/dump-qcserverless4-20250812/l-quote.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_quote__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_quote));
update qcserverless4.l_quote set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table l_quote 
\echo . 
\echo Loading Table l_segment 
\copy qcserverless4.l_segment from '/usr1/dump-qcserverless4-20250812/l-segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_segment__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_segment));
\echo Finish Table l_segment 
\echo . 
\echo Loading Table l_umsatz 
\copy qcserverless4.l_umsatz from '/usr1/dump-qcserverless4-20250812/l-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_umsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_umsatz));
\echo Finish Table l_umsatz 
\echo . 
\echo Loading Table l_untergrup 
\copy qcserverless4.l_untergrup from '/usr1/dump-qcserverless4-20250812/l-untergrup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_untergrup__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_untergrup));
\echo Finish Table l_untergrup 
\echo . 
\echo Loading Table l_verbrauch 
\copy qcserverless4.l_verbrauch from '/usr1/dump-qcserverless4-20250812/l-verbrauch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_verbrauch__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_verbrauch));
\echo Finish Table l_verbrauch 
\echo . 
\echo Loading Table l_zahlbed 
\copy qcserverless4.l_zahlbed from '/usr1/dump-qcserverless4-20250812/l-zahlbed.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.l_zahlbed__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.l_zahlbed));
\echo Finish Table l_zahlbed 
\echo . 
\echo Loading Table landstat 
\copy qcserverless4.landstat from '/usr1/dump-qcserverless4-20250812/landstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.landstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.landstat));
\echo Finish Table landstat 
\echo . 
\echo Loading Table masseur 
\copy qcserverless4.masseur from '/usr1/dump-qcserverless4-20250812/masseur.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.masseur__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.masseur));
\echo Finish Table masseur 
\echo . 
\echo Loading Table mast_art 
\copy qcserverless4.mast_art from '/usr1/dump-qcserverless4-20250812/mast-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mast_art__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mast_art));
\echo Finish Table mast_art 
\echo . 
\echo Loading Table master 
\copy qcserverless4.master from '/usr1/dump-qcserverless4-20250812/master.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.master__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.master));
\echo Finish Table master 
\echo . 
\echo Loading Table mathis 
\copy qcserverless4.mathis from '/usr1/dump-qcserverless4-20250812/mathis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mathis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mathis));
\echo Finish Table mathis 
\echo . 
\echo Loading Table mc_aclub 
\copy qcserverless4.mc_aclub from '/usr1/dump-qcserverless4-20250812/mc-aclub.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mc_aclub__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mc_aclub));
\echo Finish Table mc_aclub 
\echo . 
\echo Loading Table mc_cardhis 
\copy qcserverless4.mc_cardhis from '/usr1/dump-qcserverless4-20250812/mc-cardhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mc_cardhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mc_cardhis));
\echo Finish Table mc_cardhis 
\echo . 
\echo Loading Table mc_disc 
\copy qcserverless4.mc_disc from '/usr1/dump-qcserverless4-20250812/mc-disc.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mc_disc__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mc_disc));
\echo Finish Table mc_disc 
\echo . 
\echo Loading Table mc_fee 
\copy qcserverless4.mc_fee from '/usr1/dump-qcserverless4-20250812/mc-fee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mc_fee__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mc_fee));
\echo Finish Table mc_fee 
\echo . 
\echo Loading Table mc_guest 
\copy qcserverless4.mc_guest from '/usr1/dump-qcserverless4-20250812/mc-guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mc_guest__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mc_guest));
\echo Finish Table mc_guest 
\echo . 
\echo Loading Table mc_types 
\copy qcserverless4.mc_types from '/usr1/dump-qcserverless4-20250812/mc-types.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mc_types__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mc_types));
\echo Finish Table mc_types 
\echo . 
\echo Loading Table mealcoup 
\copy qcserverless4.mealcoup from '/usr1/dump-qcserverless4-20250812/mealcoup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mealcoup__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mealcoup));
\echo Finish Table mealcoup 
\echo . 
\echo Loading Table messages 
\copy qcserverless4.messages from '/usr1/dump-qcserverless4-20250812/messages.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.messages__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.messages));
update qcserverless4.messages set messtext = array_replace(messtext,NULL,''); 
\echo Finish Table messages 
\echo . 
\echo Loading Table messe 
\copy qcserverless4.messe from '/usr1/dump-qcserverless4-20250812/messe.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.messe__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.messe));
\echo Finish Table messe 
\echo . 
\echo Loading Table mhis_line 
\copy qcserverless4.mhis_line from '/usr1/dump-qcserverless4-20250812/mhis-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.mhis_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.mhis_line));
\echo Finish Table mhis_line 
\echo . 
\echo Loading Table nation 
\copy qcserverless4.nation from '/usr1/dump-qcserverless4-20250812/nation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.nation__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.nation));
\echo Finish Table nation 
\echo . 
\echo Loading Table nationstat 
\copy qcserverless4.nationstat from '/usr1/dump-qcserverless4-20250812/nationstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.nationstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.nationstat));
\echo Finish Table nationstat 
\echo . 
\echo Loading Table natstat1 
\copy qcserverless4.natstat1 from '/usr1/dump-qcserverless4-20250812/natstat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.natstat1__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.natstat1));
\echo Finish Table natstat1 
\echo . 
\echo Loading Table nebenst 
\copy qcserverless4.nebenst from '/usr1/dump-qcserverless4-20250812/nebenst.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.nebenst__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.nebenst));
\echo Finish Table nebenst 
\echo . 
\echo Loading Table nightaudit 
\copy qcserverless4.nightaudit from '/usr1/dump-qcserverless4-20250812/nightaudit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.nightaudit__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.nightaudit));
\echo Finish Table nightaudit 
\echo . 
\echo Loading Table nitehist 
\copy qcserverless4.nitehist from '/usr1/dump-qcserverless4-20250812/nitehist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.nitehist__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.nitehist));
\echo Finish Table nitehist 
\echo . 
\echo Loading Table nitestor 
\copy qcserverless4.nitestor from '/usr1/dump-qcserverless4-20250812/nitestor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.nitestor__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.nitestor));
\echo Finish Table nitestor 
\echo . 
\echo Loading Table notes 
\copy qcserverless4.notes from '/usr1/dump-qcserverless4-20250812/notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.notes__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.notes));
update qcserverless4.notes set note = array_replace(note,NULL,''); 
\echo Finish Table notes 
\echo . 
\echo Loading Table outorder 
\copy qcserverless4.outorder from '/usr1/dump-qcserverless4-20250812/outorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.outorder__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.outorder));
\echo Finish Table outorder 
\echo . 
\echo Loading Table package 
\copy qcserverless4.package from '/usr1/dump-qcserverless4-20250812/package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.package__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.package));
\echo Finish Table package 
\echo . 
\echo Loading Table parameters 
\copy qcserverless4.parameters from '/usr1/dump-qcserverless4-20250812/parameters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.parameters__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.parameters));
\echo Finish Table parameters 
\echo . 
\echo Loading Table paramtext 
\copy qcserverless4.paramtext from '/usr1/dump-qcserverless4-20250812/paramtext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.paramtext__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.paramtext));
\echo Finish Table paramtext 
\echo . 
\echo Loading Table pricecod 
\copy qcserverless4.pricecod from '/usr1/dump-qcserverless4-20250812/pricecod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.pricecod__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.pricecod));
\echo Finish Table pricecod 
\echo . 
\echo Loading Table pricegrp 
\copy qcserverless4.pricegrp from '/usr1/dump-qcserverless4-20250812/pricegrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.pricegrp__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.pricegrp));
\echo Finish Table pricegrp 
\echo . 
\echo Loading Table printcod 
\copy qcserverless4.printcod from '/usr1/dump-qcserverless4-20250812/printcod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.printcod__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.printcod));
\echo Finish Table printcod 
\echo . 
\echo Loading Table printer 
\copy qcserverless4.printer from '/usr1/dump-qcserverless4-20250812/printer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.printer__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.printer));
\echo Finish Table printer 
\echo . 
\echo Loading Table prmarket 
\copy qcserverless4.prmarket from '/usr1/dump-qcserverless4-20250812/prmarket.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.prmarket__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.prmarket));
\echo Finish Table prmarket 
\echo . 
\echo Loading Table progcat 
\copy qcserverless4.progcat from '/usr1/dump-qcserverless4-20250812/progcat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.progcat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.progcat));
\echo Finish Table progcat 
\echo . 
\echo Loading Table progfile 
\copy qcserverless4.progfile from '/usr1/dump-qcserverless4-20250812/progfile.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.progfile__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.progfile));
\echo Finish Table progfile 
\echo . 
\echo Loading Table prtable 
\copy qcserverless4.prtable from '/usr1/dump-qcserverless4-20250812/prtable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.prtable__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.prtable));
\echo Finish Table prtable 
\echo . 
\echo Loading Table queasy 
\copy qcserverless4.queasy from '/usr1/dump-qcserverless4-20250812/queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.queasy));
\echo Finish Table queasy 
\echo . 
\echo Loading Table ratecode 
\copy qcserverless4.ratecode from '/usr1/dump-qcserverless4-20250812/ratecode.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.ratecode__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.ratecode));
update qcserverless4.ratecode set char1 = array_replace(char1,NULL,''); 
\echo Finish Table ratecode 
\echo . 
\echo Loading Table raum 
\copy qcserverless4.raum from '/usr1/dump-qcserverless4-20250812/raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.raum__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.raum));
\echo Finish Table raum 
\echo . 
\echo Loading Table res_history 
\copy qcserverless4.res_history from '/usr1/dump-qcserverless4-20250812/res-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.res_history__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.res_history));
\echo Finish Table res_history 
\echo . 
\echo Loading Table res_line 
\copy qcserverless4.res_line from '/usr1/dump-qcserverless4-20250812/res-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.res_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.res_line));
\echo Finish Table res_line 
\echo . 
\echo Loading Table reservation 
\copy qcserverless4.reservation from '/usr1/dump-qcserverless4-20250812/reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.reservation));
\echo Finish Table reservation 
\echo . 
\echo Loading Table reslin_queasy 
\copy qcserverless4.reslin_queasy from '/usr1/dump-qcserverless4-20250812/reslin-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.reslin_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.reslin_queasy));
\echo Finish Table reslin_queasy 
\echo . 
\echo Loading Table resplan 
\copy qcserverless4.resplan from '/usr1/dump-qcserverless4-20250812/resplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.resplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.resplan));
\echo Finish Table resplan 
\echo . 
\echo Loading Table rg_reports 
\copy qcserverless4.rg_reports from '/usr1/dump-qcserverless4-20250812/rg-reports.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.rg_reports__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.rg_reports));
update qcserverless4.rg_reports set metadata = array_replace(metadata,NULL,''); 
update qcserverless4.rg_reports set slice_name = array_replace(slice_name,NULL,''); 
update qcserverless4.rg_reports set view_name = array_replace(view_name,NULL,''); 
\echo Finish Table rg_reports 
\echo . 
\echo Loading Table rmbudget 
\copy qcserverless4.rmbudget from '/usr1/dump-qcserverless4-20250812/rmbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.rmbudget__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.rmbudget));
update qcserverless4.rmbudget set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table rmbudget 
\echo . 
\echo Loading Table sales 
\copy qcserverless4.sales from '/usr1/dump-qcserverless4-20250812/sales.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sales__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sales));
\echo Finish Table sales 
\echo . 
\echo Loading Table salesbud 
\copy qcserverless4.salesbud from '/usr1/dump-qcserverless4-20250812/salesbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.salesbud__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.salesbud));
\echo Finish Table salesbud 
\echo . 
\echo Loading Table salestat 
\copy qcserverless4.salestat from '/usr1/dump-qcserverless4-20250812/salestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.salestat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.salestat));
\echo Finish Table salestat 
\echo . 
\echo Loading Table salestim 
\copy qcserverless4.salestim from '/usr1/dump-qcserverless4-20250812/salestim.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.salestim__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.salestim));
\echo Finish Table salestim 
\echo . 
\echo Loading Table segment 
\copy qcserverless4.segment from '/usr1/dump-qcserverless4-20250812/segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.segment__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.segment));
\echo Finish Table segment 
\echo . 
\echo Loading Table segmentstat 
\copy qcserverless4.segmentstat from '/usr1/dump-qcserverless4-20250812/segmentstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.segmentstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.segmentstat));
\echo Finish Table segmentstat 
\echo . 
\echo Loading Table sms_bcaster 
\copy qcserverless4.sms_bcaster from '/usr1/dump-qcserverless4-20250812/sms-bcaster.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sms_bcaster__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sms_bcaster));
\echo Finish Table sms_bcaster 
\echo . 
\echo Loading Table sms_broadcast 
\copy qcserverless4.sms_broadcast from '/usr1/dump-qcserverless4-20250812/sms-broadcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sms_broadcast__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sms_broadcast));
\echo Finish Table sms_broadcast 
\echo . 
\echo Loading Table sms_group 
\copy qcserverless4.sms_group from '/usr1/dump-qcserverless4-20250812/sms-group.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sms_group__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sms_group));
\echo Finish Table sms_group 
\echo . 
\echo Loading Table sms_groupmbr 
\copy qcserverless4.sms_groupmbr from '/usr1/dump-qcserverless4-20250812/sms-groupmbr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sms_groupmbr__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sms_groupmbr));
\echo Finish Table sms_groupmbr 
\echo . 
\echo Loading Table sms_received 
\copy qcserverless4.sms_received from '/usr1/dump-qcserverless4-20250812/sms-received.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sms_received__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sms_received));
\echo Finish Table sms_received 
\echo . 
\echo Loading Table sourccod 
\copy qcserverless4.sourccod from '/usr1/dump-qcserverless4-20250812/Sourccod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sourccod__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sourccod));
\echo Finish Table sourccod 
\echo . 
\echo Loading Table sources 
\copy qcserverless4.sources from '/usr1/dump-qcserverless4-20250812/sources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sources__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sources));
\echo Finish Table sources 
\echo . 
\echo Loading Table sourcetext 
\copy qcserverless4.sourcetext from '/usr1/dump-qcserverless4-20250812/sourcetext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.sourcetext__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.sourcetext));
\echo Finish Table sourcetext 
\echo . 
\echo Loading Table telephone 
\copy qcserverless4.telephone from '/usr1/dump-qcserverless4-20250812/telephone.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.telephone__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.telephone));
\echo Finish Table telephone 
\echo . 
\echo Loading Table texte 
\copy qcserverless4.texte from '/usr1/dump-qcserverless4-20250812/texte.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.texte__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.texte));
\echo Finish Table texte 
\echo . 
\echo Loading Table tisch 
\copy qcserverless4.tisch from '/usr1/dump-qcserverless4-20250812/tisch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.tisch__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.tisch));
\echo Finish Table tisch 
\echo . 
\echo Loading Table tisch_res 
\copy qcserverless4.tisch_res from '/usr1/dump-qcserverless4-20250812/tisch-res.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.tisch_res__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.tisch_res));
\echo Finish Table tisch_res 
\echo . 
\echo Loading Table uebertrag 
\copy qcserverless4.uebertrag from '/usr1/dump-qcserverless4-20250812/uebertrag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.uebertrag__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.uebertrag));
\echo Finish Table uebertrag 
\echo . 
\echo Loading Table umsatz 
\copy qcserverless4.umsatz from '/usr1/dump-qcserverless4-20250812/umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.umsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.umsatz));
\echo Finish Table umsatz 
\echo . 
\echo Loading Table waehrung 
\copy qcserverless4.waehrung from '/usr1/dump-qcserverless4-20250812/waehrung.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.waehrung__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.waehrung));
\echo Finish Table waehrung 
\echo . 
\echo Loading Table wakeup 
\copy qcserverless4.wakeup from '/usr1/dump-qcserverless4-20250812/wakeup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.wakeup__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.wakeup));
\echo Finish Table wakeup 
\echo . 
\echo Loading Table wgrpdep 
\copy qcserverless4.wgrpdep from '/usr1/dump-qcserverless4-20250812/wgrpdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.wgrpdep__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.wgrpdep));
\echo Finish Table wgrpdep 
\echo . 
\echo Loading Table wgrpgen 
\copy qcserverless4.wgrpgen from '/usr1/dump-qcserverless4-20250812/wgrpgen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.wgrpgen__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.wgrpgen));
\echo Finish Table wgrpgen 
\echo . 
\echo Loading Table zimkateg 
\copy qcserverless4.zimkateg from '/usr1/dump-qcserverless4-20250812/zimkateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zimkateg__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zimkateg));
\echo Finish Table zimkateg 
\echo . 
\echo Loading Table zimmer 
\copy qcserverless4.zimmer from '/usr1/dump-qcserverless4-20250812/zimmer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zimmer__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zimmer));
update qcserverless4.zimmer set verbindung = array_replace(verbindung,NULL,''); 
\echo Finish Table zimmer 
\echo . 
\echo Loading Table zimmer_book 
\copy qcserverless4.zimmer_book from '/usr1/dump-qcserverless4-20250812/zimmer-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zimmer_book__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zimmer_book));
\echo Finish Table zimmer_book 
\echo . 
\echo Loading Table zimmer_book_line 
\copy qcserverless4.zimmer_book_line from '/usr1/dump-qcserverless4-20250812/zimmer-book-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zimmer_book_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zimmer_book_line));
\echo Finish Table zimmer_book_line 
\echo . 
\echo Loading Table zimplan 
\copy qcserverless4.zimplan from '/usr1/dump-qcserverless4-20250812/zimplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zimplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zimplan));
\echo Finish Table zimplan 
\echo . 
\echo Loading Table zimpreis 
\copy qcserverless4.zimpreis from '/usr1/dump-qcserverless4-20250812/zimpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zimpreis__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zimpreis));
\echo Finish Table zimpreis 
\echo . 
\echo Loading Table zinrstat 
\copy qcserverless4.zinrstat from '/usr1/dump-qcserverless4-20250812/zinrstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zinrstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zinrstat));
\echo Finish Table zinrstat 
\echo . 
\echo Loading Table zkstat 
\copy qcserverless4.zkstat from '/usr1/dump-qcserverless4-20250812/zkstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zkstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zkstat));
\echo Finish Table zkstat 
\echo . 
\echo Loading Table zwkum 
\copy qcserverless4.zwkum from '/usr1/dump-qcserverless4-20250812/zwkum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless4.zwkum__recid_seq', (SELECT MAX(_recid) FROM qcserverless4.zwkum));
\echo Finish Table zwkum 
\echo . 
