\echo Loading Table absen 
\copy qcserverless2.absen from '/usr1/dump-qcserverless2-20250714/absen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.absen__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.absen));
\echo Finish Table absen 
\echo . 
\echo Loading Table akt_code 
\copy qcserverless2.akt_code from '/usr1/dump-qcserverless2-20250714/akt-code.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.akt_code__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.akt_code));
\echo Finish Table akt_code 
\echo . 
\echo Loading Table akt_cust 
\copy qcserverless2.akt_cust from '/usr1/dump-qcserverless2-20250714/akt-cust.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.akt_cust__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.akt_cust));
\echo Finish Table akt_cust 
\echo . 
\echo Loading Table akt_kont 
\copy qcserverless2.akt_kont from '/usr1/dump-qcserverless2-20250714/akt-kont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.akt_kont__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.akt_kont));
\echo Finish Table akt_kont 
\echo . 
\echo Loading Table akt_line 
\copy qcserverless2.akt_line from '/usr1/dump-qcserverless2-20250714/akt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.akt_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.akt_line));
\echo Finish Table akt_line 
\echo . 
\echo Loading Table akthdr 
\copy qcserverless2.akthdr from '/usr1/dump-qcserverless2-20250714/akthdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.akthdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.akthdr));
\echo Finish Table akthdr 
\echo . 
\echo Loading Table aktion 
\copy qcserverless2.aktion from '/usr1/dump-qcserverless2-20250714/aktion.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.aktion__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.aktion));
update qcserverless2.aktion set texte = array_replace(texte,NULL,''); 
\echo Finish Table aktion 
\echo . 
\echo Loading Table ap_journal 
\copy qcserverless2.ap_journal from '/usr1/dump-qcserverless2-20250714/ap-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.ap_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.ap_journal));
\echo Finish Table ap_journal 
\echo . 
\echo Loading Table apt_bill 
\copy qcserverless2.apt_bill from '/usr1/dump-qcserverless2-20250714/apt-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.apt_bill__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.apt_bill));
update qcserverless2.apt_bill set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table apt_bill 
\echo . 
\echo Loading Table archieve 
\copy qcserverless2.archieve from '/usr1/dump-qcserverless2-20250714/archieve.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.archieve__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.archieve));
update qcserverless2.archieve set char = array_replace(char,NULL,''); 
\echo Finish Table archieve 
\echo . 
\echo Loading Table argt_line 
\copy qcserverless2.argt_line from '/usr1/dump-qcserverless2-20250714/argt-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.argt_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.argt_line));
\echo Finish Table argt_line 
\echo . 
\echo Loading Table argtcost 
\copy qcserverless2.argtcost from '/usr1/dump-qcserverless2-20250714/argtcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.argtcost__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.argtcost));
update qcserverless2.argtcost set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtcost 
\echo . 
\echo Loading Table argtstat 
\copy qcserverless2.argtstat from '/usr1/dump-qcserverless2-20250714/argtstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.argtstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.argtstat));
update qcserverless2.argtstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table argtstat 
\echo . 
\echo Loading Table arrangement 
\copy qcserverless2.arrangement from '/usr1/dump-qcserverless2-20250714/arrangement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.arrangement__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.arrangement));
update qcserverless2.arrangement set argt_rgbez2 = array_replace(argt_rgbez2,NULL,''); 
\echo Finish Table arrangement 
\echo . 
\echo Loading Table artikel 
\copy qcserverless2.artikel from '/usr1/dump-qcserverless2-20250714/artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.artikel));
\echo Finish Table artikel 
\echo . 
\echo Loading Table artprice 
\copy qcserverless2.artprice from '/usr1/dump-qcserverless2-20250714/artprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.artprice__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.artprice));
\echo Finish Table artprice 
\echo . 
\echo Loading Table b_history 
\copy qcserverless2.b_history from '/usr1/dump-qcserverless2-20250714/b-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.b_history__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.b_history));
update qcserverless2.b_history set anlass = array_replace(anlass,NULL,''); 
update qcserverless2.b_history set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update qcserverless2.b_history set ape__speisen = array_replace(ape__speisen,NULL,''); 
update qcserverless2.b_history set arrival = array_replace(arrival,NULL,''); 
update qcserverless2.b_history set c_resstatus = array_replace(c_resstatus,NULL,''); 
update qcserverless2.b_history set dance = array_replace(dance,NULL,''); 
update qcserverless2.b_history set deko2 = array_replace(deko2,NULL,''); 
update qcserverless2.b_history set dekoration = array_replace(dekoration,NULL,''); 
update qcserverless2.b_history set digestif = array_replace(digestif,NULL,''); 
update qcserverless2.b_history set dinner = array_replace(dinner,NULL,''); 
update qcserverless2.b_history set f_menu = array_replace(f_menu,NULL,''); 
update qcserverless2.b_history set f_no = array_replace(f_no,NULL,''); 
update qcserverless2.b_history set fotograf = array_replace(fotograf,NULL,''); 
update qcserverless2.b_history set gaestebuch = array_replace(gaestebuch,NULL,''); 
update qcserverless2.b_history set garderobe = array_replace(garderobe,NULL,''); 
update qcserverless2.b_history set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update qcserverless2.b_history set kaffee = array_replace(kaffee,NULL,''); 
update qcserverless2.b_history set kartentext = array_replace(kartentext,NULL,''); 
update qcserverless2.b_history set kontaktperson = array_replace(kontaktperson,NULL,''); 
update qcserverless2.b_history set kuenstler = array_replace(kuenstler,NULL,''); 
update qcserverless2.b_history set menue = array_replace(menue,NULL,''); 
update qcserverless2.b_history set menuekarten = array_replace(menuekarten,NULL,''); 
update qcserverless2.b_history set musik = array_replace(musik,NULL,''); 
update qcserverless2.b_history set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update qcserverless2.b_history set nadkarte = array_replace(nadkarte,NULL,''); 
update qcserverless2.b_history set ndessen = array_replace(ndessen,NULL,''); 
update qcserverless2.b_history set payment_userinit = array_replace(payment_userinit,NULL,''); 
update qcserverless2.b_history set personen2 = array_replace(personen2,NULL,''); 
update qcserverless2.b_history set raeume = array_replace(raeume,NULL,''); 
update qcserverless2.b_history set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update qcserverless2.b_history set raummiete = array_replace(raummiete,NULL,''); 
update qcserverless2.b_history set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update qcserverless2.b_history set service = array_replace(service,NULL,''); 
update qcserverless2.b_history set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update qcserverless2.b_history set sonstiges = array_replace(sonstiges,NULL,''); 
update qcserverless2.b_history set technik = array_replace(technik,NULL,''); 
update qcserverless2.b_history set tischform = array_replace(tischform,NULL,''); 
update qcserverless2.b_history set tischordnung = array_replace(tischordnung,NULL,''); 
update qcserverless2.b_history set tischplan = array_replace(tischplan,NULL,''); 
update qcserverless2.b_history set tischreden = array_replace(tischreden,NULL,''); 
update qcserverless2.b_history set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update qcserverless2.b_history set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update qcserverless2.b_history set va_ablauf = array_replace(va_ablauf,NULL,''); 
update qcserverless2.b_history set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update qcserverless2.b_history set vip = array_replace(vip,NULL,''); 
update qcserverless2.b_history set weine = array_replace(weine,NULL,''); 
update qcserverless2.b_history set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table b_history 
\echo . 
\echo Loading Table b_oorder 
\copy qcserverless2.b_oorder from '/usr1/dump-qcserverless2-20250714/b-oorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.b_oorder__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.b_oorder));
\echo Finish Table b_oorder 
\echo . 
\echo Loading Table b_storno 
\copy qcserverless2.b_storno from '/usr1/dump-qcserverless2-20250714/b-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.b_storno__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.b_storno));
update qcserverless2.b_storno set grund = array_replace(grund,NULL,''); 
\echo Finish Table b_storno 
\echo . 
\echo Loading Table ba_rset 
\copy qcserverless2.ba_rset from '/usr1/dump-qcserverless2-20250714/ba-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.ba_rset__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.ba_rset));
\echo Finish Table ba_rset 
\echo . 
\echo Loading Table ba_setup 
\copy qcserverless2.ba_setup from '/usr1/dump-qcserverless2-20250714/ba-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.ba_setup__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.ba_setup));
\echo Finish Table ba_setup 
\echo . 
\echo Loading Table ba_typ 
\copy qcserverless2.ba_typ from '/usr1/dump-qcserverless2-20250714/ba-typ.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.ba_typ__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.ba_typ));
\echo Finish Table ba_typ 
\echo . 
\echo Loading Table bankrep 
\copy qcserverless2.bankrep from '/usr1/dump-qcserverless2-20250714/bankrep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bankrep__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bankrep));
update qcserverless2.bankrep set anlass = array_replace(anlass,NULL,''); 
update qcserverless2.bankrep set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update qcserverless2.bankrep set ape__speisen = array_replace(ape__speisen,NULL,''); 
update qcserverless2.bankrep set dekoration = array_replace(dekoration,NULL,''); 
update qcserverless2.bankrep set digestif = array_replace(digestif,NULL,''); 
update qcserverless2.bankrep set fotograf = array_replace(fotograf,NULL,''); 
update qcserverless2.bankrep set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update qcserverless2.bankrep set kartentext = array_replace(kartentext,NULL,''); 
update qcserverless2.bankrep set kontaktperson = array_replace(kontaktperson,NULL,''); 
update qcserverless2.bankrep set menue = array_replace(menue,NULL,''); 
update qcserverless2.bankrep set menuekarten = array_replace(menuekarten,NULL,''); 
update qcserverless2.bankrep set musik = array_replace(musik,NULL,''); 
update qcserverless2.bankrep set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update qcserverless2.bankrep set ndessen = array_replace(ndessen,NULL,''); 
update qcserverless2.bankrep set personen2 = array_replace(personen2,NULL,''); 
update qcserverless2.bankrep set raeume = array_replace(raeume,NULL,''); 
update qcserverless2.bankrep set raummiete = array_replace(raummiete,NULL,''); 
update qcserverless2.bankrep set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update qcserverless2.bankrep set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update qcserverless2.bankrep set sonstiges = array_replace(sonstiges,NULL,''); 
update qcserverless2.bankrep set technik = array_replace(technik,NULL,''); 
update qcserverless2.bankrep set tischform = array_replace(tischform,NULL,''); 
update qcserverless2.bankrep set tischreden = array_replace(tischreden,NULL,''); 
update qcserverless2.bankrep set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update qcserverless2.bankrep set weine = array_replace(weine,NULL,''); 
update qcserverless2.bankrep set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bankrep 
\echo . 
\echo Loading Table bankres 
\copy qcserverless2.bankres from '/usr1/dump-qcserverless2-20250714/bankres.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bankres__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bankres));
update qcserverless2.bankres set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table bankres 
\echo . 
\echo Loading Table bediener 
\copy qcserverless2.bediener from '/usr1/dump-qcserverless2-20250714/bediener.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bediener__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bediener));
\echo Finish Table bediener 
\echo . 
\echo Loading Table bill 
\copy qcserverless2.bill from '/usr1/dump-qcserverless2-20250714/bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bill__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bill));
\echo Finish Table bill 
\echo . 
\echo Loading Table bill_lin_tax 
\copy qcserverless2.bill_lin_tax from '/usr1/dump-qcserverless2-20250714/bill-lin-tax.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bill_lin_tax__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bill_lin_tax));
\echo Finish Table bill_lin_tax 
\echo . 
\echo Loading Table bill_line 
\copy qcserverless2.bill_line from '/usr1/dump-qcserverless2-20250714/bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bill_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bill_line));
\echo Finish Table bill_line 
\echo . 
\echo Loading Table billhis 
\copy qcserverless2.billhis from '/usr1/dump-qcserverless2-20250714/billhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.billhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.billhis));
\echo Finish Table billhis 
\echo . 
\echo Loading Table billjournal 
\copy qcserverless2.billjournal from '/usr1/dump-qcserverless2-20250714/billjournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.billjournal__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.billjournal));
\echo Finish Table billjournal 
\echo . 
\echo Loading Table bk_beleg 
\copy qcserverless2.bk_beleg from '/usr1/dump-qcserverless2-20250714/bk-beleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_beleg__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_beleg));
\echo Finish Table bk_beleg 
\echo . 
\echo Loading Table bk_fsdef 
\copy qcserverless2.bk_fsdef from '/usr1/dump-qcserverless2-20250714/bk-fsdef.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_fsdef__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_fsdef));
\echo Finish Table bk_fsdef 
\echo . 
\echo Loading Table bk_func 
\copy qcserverless2.bk_func from '/usr1/dump-qcserverless2-20250714/bk-func.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_func__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_func));
update qcserverless2.bk_func set anlass = array_replace(anlass,NULL,''); 
update qcserverless2.bk_func set ape__getraenke = array_replace(ape__getraenke,NULL,''); 
update qcserverless2.bk_func set ape__speisen = array_replace(ape__speisen,NULL,''); 
update qcserverless2.bk_func set arrival = array_replace(arrival,NULL,''); 
update qcserverless2.bk_func set c_resstatus = array_replace(c_resstatus,NULL,''); 
update qcserverless2.bk_func set dance = array_replace(dance,NULL,''); 
update qcserverless2.bk_func set deko2 = array_replace(deko2,NULL,''); 
update qcserverless2.bk_func set dekoration = array_replace(dekoration,NULL,''); 
update qcserverless2.bk_func set digestif = array_replace(digestif,NULL,''); 
update qcserverless2.bk_func set dinner = array_replace(dinner,NULL,''); 
update qcserverless2.bk_func set f_menu = array_replace(f_menu,NULL,''); 
update qcserverless2.bk_func set f_no = array_replace(f_no,NULL,''); 
update qcserverless2.bk_func set fotograf = array_replace(fotograf,NULL,''); 
update qcserverless2.bk_func set gaestebuch = array_replace(gaestebuch,NULL,''); 
update qcserverless2.bk_func set garderobe = array_replace(garderobe,NULL,''); 
update qcserverless2.bk_func set hotelzimmer = array_replace(hotelzimmer,NULL,''); 
update qcserverless2.bk_func set kaffee = array_replace(kaffee,NULL,''); 
update qcserverless2.bk_func set kartentext = array_replace(kartentext,NULL,''); 
update qcserverless2.bk_func set kontaktperson = array_replace(kontaktperson,NULL,''); 
update qcserverless2.bk_func set kuenstler = array_replace(kuenstler,NULL,''); 
update qcserverless2.bk_func set menue = array_replace(menue,NULL,''); 
update qcserverless2.bk_func set menuekarten = array_replace(menuekarten,NULL,''); 
update qcserverless2.bk_func set musik = array_replace(musik,NULL,''); 
update qcserverless2.bk_func set nachtverpflegung = array_replace(nachtverpflegung,NULL,''); 
update qcserverless2.bk_func set nadkarte = array_replace(nadkarte,NULL,''); 
update qcserverless2.bk_func set ndessen = array_replace(ndessen,NULL,''); 
update qcserverless2.bk_func set personen2 = array_replace(personen2,NULL,''); 
update qcserverless2.bk_func set raeume = array_replace(raeume,NULL,''); 
update qcserverless2.bk_func set raumbezeichnung = array_replace(raumbezeichnung,NULL,''); 
update qcserverless2.bk_func set raummiete = array_replace(raummiete,NULL,''); 
update qcserverless2.bk_func set rechnungsanschrift = array_replace(rechnungsanschrift,NULL,''); 
update qcserverless2.bk_func set service = array_replace(service,NULL,''); 
update qcserverless2.bk_func set sonst__bewirt = array_replace(sonst__bewirt,NULL,''); 
update qcserverless2.bk_func set sonstiges = array_replace(sonstiges,NULL,''); 
update qcserverless2.bk_func set technik = array_replace(technik,NULL,''); 
update qcserverless2.bk_func set tischform = array_replace(tischform,NULL,''); 
update qcserverless2.bk_func set tischordnung = array_replace(tischordnung,NULL,''); 
update qcserverless2.bk_func set tischplan = array_replace(tischplan,NULL,''); 
update qcserverless2.bk_func set tischreden = array_replace(tischreden,NULL,''); 
update qcserverless2.bk_func set uhrzeiten = array_replace(uhrzeiten,NULL,''); 
update qcserverless2.bk_func set v_kontaktperson = array_replace(v_kontaktperson,NULL,''); 
update qcserverless2.bk_func set va_ablauf = array_replace(va_ablauf,NULL,''); 
update qcserverless2.bk_func set veranstalteranschrift = array_replace(veranstalteranschrift,NULL,''); 
update qcserverless2.bk_func set vip = array_replace(vip,NULL,''); 
update qcserverless2.bk_func set weine = array_replace(weine,NULL,''); 
update qcserverless2.bk_func set zweck = array_replace(zweck,NULL,''); 
\echo Finish Table bk_func 
\echo . 
\echo Loading Table bk_package 
\copy qcserverless2.bk_package from '/usr1/dump-qcserverless2-20250714/bk-package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_package__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_package));
\echo Finish Table bk_package 
\echo . 
\echo Loading Table bk_pause 
\copy qcserverless2.bk_pause from '/usr1/dump-qcserverless2-20250714/bk-pause.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_pause__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_pause));
\echo Finish Table bk_pause 
\echo . 
\echo Loading Table bk_rart 
\copy qcserverless2.bk_rart from '/usr1/dump-qcserverless2-20250714/bk-rart.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_rart__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_rart));
\echo Finish Table bk_rart 
\echo . 
\echo Loading Table bk_raum 
\copy qcserverless2.bk_raum from '/usr1/dump-qcserverless2-20250714/bk-raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_raum__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_raum));
\echo Finish Table bk_raum 
\echo . 
\echo Loading Table bk_reser 
\copy qcserverless2.bk_reser from '/usr1/dump-qcserverless2-20250714/bk-reser.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_reser__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_reser));
\echo Finish Table bk_reser 
\echo . 
\echo Loading Table bk_rset 
\copy qcserverless2.bk_rset from '/usr1/dump-qcserverless2-20250714/bk-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_rset__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_rset));
\echo Finish Table bk_rset 
\echo . 
\echo Loading Table bk_setup 
\copy qcserverless2.bk_setup from '/usr1/dump-qcserverless2-20250714/bk-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_setup__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_setup));
\echo Finish Table bk_setup 
\echo . 
\echo Loading Table bk_stat 
\copy qcserverless2.bk_stat from '/usr1/dump-qcserverless2-20250714/bk-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_stat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_stat));
\echo Finish Table bk_stat 
\echo . 
\echo Loading Table bk_veran 
\copy qcserverless2.bk_veran from '/usr1/dump-qcserverless2-20250714/bk-veran.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bk_veran__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bk_veran));
update qcserverless2.bk_veran set payment_userinit = array_replace(payment_userinit,NULL,''); 
\echo Finish Table bk_veran 
\echo . 
\echo Loading Table bl_dates 
\copy qcserverless2.bl_dates from '/usr1/dump-qcserverless2-20250714/bl-dates.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bl_dates__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bl_dates));
\echo Finish Table bl_dates 
\echo . 
\echo Loading Table blinehis 
\copy qcserverless2.blinehis from '/usr1/dump-qcserverless2-20250714/blinehis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.blinehis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.blinehis));
\echo Finish Table blinehis 
\echo . 
\echo Loading Table bresline 
\copy qcserverless2.bresline from '/usr1/dump-qcserverless2-20250714/bresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.bresline__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.bresline));
update qcserverless2.bresline set texte = array_replace(texte,NULL,''); 
\echo Finish Table bresline 
\echo . 
\echo Loading Table brief 
\copy qcserverless2.brief from '/usr1/dump-qcserverless2-20250714/brief.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.brief__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.brief));
\echo Finish Table brief 
\echo . 
\echo Loading Table brieftmp 
\copy qcserverless2.brieftmp from '/usr1/dump-qcserverless2-20250714/brieftmp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.brieftmp__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.brieftmp));
\echo Finish Table brieftmp 
\echo . 
\echo Loading Table briefzei 
\copy qcserverless2.briefzei from '/usr1/dump-qcserverless2-20250714/briefzei.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.briefzei__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.briefzei));
\echo Finish Table briefzei 
\echo . 
\echo Loading Table budget 
\copy qcserverless2.budget from '/usr1/dump-qcserverless2-20250714/budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.budget__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.budget));
\echo Finish Table budget 
\echo . 
\echo Loading Table calls 
\copy qcserverless2.calls from '/usr1/dump-qcserverless2-20250714/calls.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.calls__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.calls));
\echo Finish Table calls 
\echo . 
\echo Loading Table cl_bonus 
\copy qcserverless2.cl_bonus from '/usr1/dump-qcserverless2-20250714/cl-bonus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_bonus__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_bonus));
\echo Finish Table cl_bonus 
\echo . 
\echo Loading Table cl_book 
\copy qcserverless2.cl_book from '/usr1/dump-qcserverless2-20250714/cl-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_book__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_book));
\echo Finish Table cl_book 
\echo . 
\echo Loading Table cl_checkin 
\copy qcserverless2.cl_checkin from '/usr1/dump-qcserverless2-20250714/cl-checkin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_checkin__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_checkin));
\echo Finish Table cl_checkin 
\echo . 
\echo Loading Table cl_class 
\copy qcserverless2.cl_class from '/usr1/dump-qcserverless2-20250714/cl-class.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_class__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_class));
\echo Finish Table cl_class 
\echo . 
\echo Loading Table cl_enroll 
\copy qcserverless2.cl_enroll from '/usr1/dump-qcserverless2-20250714/cl-enroll.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_enroll__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_enroll));
\echo Finish Table cl_enroll 
\echo . 
\echo Loading Table cl_free 
\copy qcserverless2.cl_free from '/usr1/dump-qcserverless2-20250714/cl-free.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_free__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_free));
\echo Finish Table cl_free 
\echo . 
\echo Loading Table cl_histci 
\copy qcserverless2.cl_histci from '/usr1/dump-qcserverless2-20250714/cl-histci.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_histci__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_histci));
\echo Finish Table cl_histci 
\echo . 
\echo Loading Table cl_histpay 
\copy qcserverless2.cl_histpay from '/usr1/dump-qcserverless2-20250714/cl-histpay.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_histpay__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_histpay));
\echo Finish Table cl_histpay 
\echo . 
\echo Loading Table cl_histstatus 
\copy qcserverless2.cl_histstatus from '/usr1/dump-qcserverless2-20250714/cl-histstatus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_histstatus__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_histstatus));
\echo Finish Table cl_histstatus 
\echo . 
\echo Loading Table cl_histtrain 
\copy qcserverless2.cl_histtrain from '/usr1/dump-qcserverless2-20250714/cl-histtrain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_histtrain__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_histtrain));
\echo Finish Table cl_histtrain 
\echo . 
\echo Loading Table cl_histvisit 
\copy qcserverless2.cl_histvisit from '/usr1/dump-qcserverless2-20250714/cl-histvisit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_histvisit__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_histvisit));
\echo Finish Table cl_histvisit 
\echo . 
\echo Loading Table cl_home 
\copy qcserverless2.cl_home from '/usr1/dump-qcserverless2-20250714/cl-home.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_home__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_home));
\echo Finish Table cl_home 
\echo . 
\echo Loading Table cl_location 
\copy qcserverless2.cl_location from '/usr1/dump-qcserverless2-20250714/cl-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_location__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_location));
\echo Finish Table cl_location 
\echo . 
\echo Loading Table cl_locker 
\copy qcserverless2.cl_locker from '/usr1/dump-qcserverless2-20250714/cl-locker.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_locker__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_locker));
\echo Finish Table cl_locker 
\echo . 
\echo Loading Table cl_log 
\copy qcserverless2.cl_log from '/usr1/dump-qcserverless2-20250714/cl-log.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_log__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_log));
\echo Finish Table cl_log 
\echo . 
\echo Loading Table cl_member 
\copy qcserverless2.cl_member from '/usr1/dump-qcserverless2-20250714/cl-member.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_member__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_member));
\echo Finish Table cl_member 
\echo . 
\echo Loading Table cl_memtype 
\copy qcserverless2.cl_memtype from '/usr1/dump-qcserverless2-20250714/cl-memtype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_memtype__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_memtype));
\echo Finish Table cl_memtype 
\echo . 
\echo Loading Table cl_paysched 
\copy qcserverless2.cl_paysched from '/usr1/dump-qcserverless2-20250714/cl-paysched.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_paysched__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_paysched));
\echo Finish Table cl_paysched 
\echo . 
\echo Loading Table cl_stat 
\copy qcserverless2.cl_stat from '/usr1/dump-qcserverless2-20250714/cl-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_stat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_stat));
\echo Finish Table cl_stat 
\echo . 
\echo Loading Table cl_stat1 
\copy qcserverless2.cl_stat1 from '/usr1/dump-qcserverless2-20250714/cl-stat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_stat1__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_stat1));
\echo Finish Table cl_stat1 
\echo . 
\echo Loading Table cl_towel 
\copy qcserverless2.cl_towel from '/usr1/dump-qcserverless2-20250714/cl-towel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_towel__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_towel));
\echo Finish Table cl_towel 
\echo . 
\echo Loading Table cl_trainer 
\copy qcserverless2.cl_trainer from '/usr1/dump-qcserverless2-20250714/cl-trainer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_trainer__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_trainer));
\echo Finish Table cl_trainer 
\echo . 
\echo Loading Table cl_upgrade 
\copy qcserverless2.cl_upgrade from '/usr1/dump-qcserverless2-20250714/cl-upgrade.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cl_upgrade__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cl_upgrade));
\echo Finish Table cl_upgrade 
\echo . 
\echo Loading Table costbudget 
\copy qcserverless2.costbudget from '/usr1/dump-qcserverless2-20250714/costbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.costbudget__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.costbudget));
\echo Finish Table costbudget 
\echo . 
\echo Loading Table counters 
\copy qcserverless2.counters from '/usr1/dump-qcserverless2-20250714/counters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.counters__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.counters));
\echo Finish Table counters 
\echo . 
\echo Loading Table crm_campaign 
\copy qcserverless2.crm_campaign from '/usr1/dump-qcserverless2-20250714/crm-campaign.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_campaign__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_campaign));
\echo Finish Table crm_campaign 
\echo . 
\echo Loading Table crm_category 
\copy qcserverless2.crm_category from '/usr1/dump-qcserverless2-20250714/crm-category.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_category__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_category));
\echo Finish Table crm_category 
\echo . 
\echo Loading Table crm_dept 
\copy qcserverless2.crm_dept from '/usr1/dump-qcserverless2-20250714/crm-dept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_dept__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_dept));
\echo Finish Table crm_dept 
\echo . 
\echo Loading Table crm_dtl 
\copy qcserverless2.crm_dtl from '/usr1/dump-qcserverless2-20250714/crm-dtl.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_dtl__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_dtl));
\echo Finish Table crm_dtl 
\echo . 
\echo Loading Table crm_email 
\copy qcserverless2.crm_email from '/usr1/dump-qcserverless2-20250714/crm-email.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_email__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_email));
\echo Finish Table crm_email 
\echo . 
\echo Loading Table crm_event 
\copy qcserverless2.crm_event from '/usr1/dump-qcserverless2-20250714/crm-event.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_event__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_event));
\echo Finish Table crm_event 
\echo . 
\echo Loading Table crm_feedhdr 
\copy qcserverless2.crm_feedhdr from '/usr1/dump-qcserverless2-20250714/crm-feedhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_feedhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_feedhdr));
\echo Finish Table crm_feedhdr 
\echo . 
\echo Loading Table crm_fnlresult 
\copy qcserverless2.crm_fnlresult from '/usr1/dump-qcserverless2-20250714/crm-fnlresult.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_fnlresult__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_fnlresult));
\echo Finish Table crm_fnlresult 
\echo . 
\echo Loading Table crm_language 
\copy qcserverless2.crm_language from '/usr1/dump-qcserverless2-20250714/crm-language.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_language__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_language));
\echo Finish Table crm_language 
\echo . 
\echo Loading Table crm_question 
\copy qcserverless2.crm_question from '/usr1/dump-qcserverless2-20250714/crm-question.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_question__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_question));
\echo Finish Table crm_question 
\echo . 
\echo Loading Table crm_tamplang 
\copy qcserverless2.crm_tamplang from '/usr1/dump-qcserverless2-20250714/crm-tamplang.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_tamplang__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_tamplang));
\echo Finish Table crm_tamplang 
\echo . 
\echo Loading Table crm_template 
\copy qcserverless2.crm_template from '/usr1/dump-qcserverless2-20250714/crm-template.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.crm_template__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.crm_template));
\echo Finish Table crm_template 
\echo . 
\echo Loading Table cross_dtl 
\copy qcserverless2.cross_dtl from '/usr1/dump-qcserverless2-20250714/cross-DTL.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cross_dtl__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cross_dtl));
\echo Finish Table cross_dtl 
\echo . 
\echo Loading Table cross_hdr 
\copy qcserverless2.cross_hdr from '/usr1/dump-qcserverless2-20250714/cross-HDR.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.cross_hdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.cross_hdr));
\echo Finish Table cross_hdr 
\echo . 
\echo Loading Table debitor 
\copy qcserverless2.debitor from '/usr1/dump-qcserverless2-20250714/debitor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.debitor__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.debitor));
\echo Finish Table debitor 
\echo . 
\echo Loading Table debthis 
\copy qcserverless2.debthis from '/usr1/dump-qcserverless2-20250714/debthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.debthis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.debthis));
\echo Finish Table debthis 
\echo . 
\echo Loading Table desttext 
\copy qcserverless2.desttext from '/usr1/dump-qcserverless2-20250714/desttext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.desttext__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.desttext));
\echo Finish Table desttext 
\echo . 
\echo Loading Table dml_art 
\copy qcserverless2.dml_art from '/usr1/dump-qcserverless2-20250714/dml-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.dml_art__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.dml_art));
\echo Finish Table dml_art 
\echo . 
\echo Loading Table dml_artdep 
\copy qcserverless2.dml_artdep from '/usr1/dump-qcserverless2-20250714/dml-artdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.dml_artdep__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.dml_artdep));
\echo Finish Table dml_artdep 
\echo . 
\echo Loading Table dml_rate 
\copy qcserverless2.dml_rate from '/usr1/dump-qcserverless2-20250714/dml-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.dml_rate__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.dml_rate));
\echo Finish Table dml_rate 
\echo . 
\echo Loading Table eg_action 
\copy qcserverless2.eg_action from '/usr1/dump-qcserverless2-20250714/eg-action.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_action__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_action));
\echo Finish Table eg_action 
\echo . 
\echo Loading Table eg_alert 
\copy qcserverless2.eg_alert from '/usr1/dump-qcserverless2-20250714/eg-Alert.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_alert__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_alert));
\echo Finish Table eg_alert 
\echo . 
\echo Loading Table eg_budget 
\copy qcserverless2.eg_budget from '/usr1/dump-qcserverless2-20250714/eg-budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_budget__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_budget));
\echo Finish Table eg_budget 
\echo . 
\echo Loading Table eg_cost 
\copy qcserverless2.eg_cost from '/usr1/dump-qcserverless2-20250714/eg-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_cost__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_cost));
\echo Finish Table eg_cost 
\echo . 
\echo Loading Table eg_duration 
\copy qcserverless2.eg_duration from '/usr1/dump-qcserverless2-20250714/eg-Duration.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_duration__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_duration));
\echo Finish Table eg_duration 
\echo . 
\echo Loading Table eg_location 
\copy qcserverless2.eg_location from '/usr1/dump-qcserverless2-20250714/eg-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_location__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_location));
\echo Finish Table eg_location 
\echo . 
\echo Loading Table eg_mainstat 
\copy qcserverless2.eg_mainstat from '/usr1/dump-qcserverless2-20250714/eg-MainStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_mainstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_mainstat));
\echo Finish Table eg_mainstat 
\echo . 
\echo Loading Table eg_maintain 
\copy qcserverless2.eg_maintain from '/usr1/dump-qcserverless2-20250714/eg-maintain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_maintain__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_maintain));
\echo Finish Table eg_maintain 
\echo . 
\echo Loading Table eg_mdetail 
\copy qcserverless2.eg_mdetail from '/usr1/dump-qcserverless2-20250714/eg-mdetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_mdetail__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_mdetail));
\echo Finish Table eg_mdetail 
\echo . 
\echo Loading Table eg_messageno 
\copy qcserverless2.eg_messageno from '/usr1/dump-qcserverless2-20250714/eg-MessageNo.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_messageno__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_messageno));
\echo Finish Table eg_messageno 
\echo . 
\echo Loading Table eg_mobilenr 
\copy qcserverless2.eg_mobilenr from '/usr1/dump-qcserverless2-20250714/eg-mobileNr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_mobilenr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_mobilenr));
\echo Finish Table eg_mobilenr 
\echo . 
\echo Loading Table eg_moveproperty 
\copy qcserverless2.eg_moveproperty from '/usr1/dump-qcserverless2-20250714/eg-moveProperty.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_moveproperty__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_moveproperty));
\echo Finish Table eg_moveproperty 
\echo . 
\echo Loading Table eg_property 
\copy qcserverless2.eg_property from '/usr1/dump-qcserverless2-20250714/eg-property.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_property__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_property));
\echo Finish Table eg_property 
\echo . 
\echo Loading Table eg_propmeter 
\copy qcserverless2.eg_propmeter from '/usr1/dump-qcserverless2-20250714/eg-propMeter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_propmeter__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_propmeter));
\echo Finish Table eg_propmeter 
\echo . 
\echo Loading Table eg_queasy 
\copy qcserverless2.eg_queasy from '/usr1/dump-qcserverless2-20250714/eg-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_queasy));
\echo Finish Table eg_queasy 
\echo . 
\echo Loading Table eg_reqdetail 
\copy qcserverless2.eg_reqdetail from '/usr1/dump-qcserverless2-20250714/eg-reqDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_reqdetail__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_reqdetail));
\echo Finish Table eg_reqdetail 
\echo . 
\echo Loading Table eg_reqif 
\copy qcserverless2.eg_reqif from '/usr1/dump-qcserverless2-20250714/eg-reqif.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_reqif__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_reqif));
\echo Finish Table eg_reqif 
\echo . 
\echo Loading Table eg_reqstat 
\copy qcserverless2.eg_reqstat from '/usr1/dump-qcserverless2-20250714/eg-ReqStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_reqstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_reqstat));
\echo Finish Table eg_reqstat 
\echo . 
\echo Loading Table eg_request 
\copy qcserverless2.eg_request from '/usr1/dump-qcserverless2-20250714/eg-request.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_request__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_request));
\echo Finish Table eg_request 
\echo . 
\echo Loading Table eg_resources 
\copy qcserverless2.eg_resources from '/usr1/dump-qcserverless2-20250714/eg-resources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_resources__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_resources));
\echo Finish Table eg_resources 
\echo . 
\echo Loading Table eg_staff 
\copy qcserverless2.eg_staff from '/usr1/dump-qcserverless2-20250714/eg-staff.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_staff__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_staff));
\echo Finish Table eg_staff 
\echo . 
\echo Loading Table eg_stat 
\copy qcserverless2.eg_stat from '/usr1/dump-qcserverless2-20250714/eg-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_stat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_stat));
\echo Finish Table eg_stat 
\echo . 
\echo Loading Table eg_subtask 
\copy qcserverless2.eg_subtask from '/usr1/dump-qcserverless2-20250714/eg-subtask.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_subtask__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_subtask));
\echo Finish Table eg_subtask 
\echo . 
\echo Loading Table eg_vendor 
\copy qcserverless2.eg_vendor from '/usr1/dump-qcserverless2-20250714/eg-vendor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_vendor__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_vendor));
\echo Finish Table eg_vendor 
\echo . 
\echo Loading Table eg_vperform 
\copy qcserverless2.eg_vperform from '/usr1/dump-qcserverless2-20250714/eg-vperform.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.eg_vperform__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.eg_vperform));
\echo Finish Table eg_vperform 
\echo . 
\echo Loading Table ekum 
\copy qcserverless2.ekum from '/usr1/dump-qcserverless2-20250714/ekum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.ekum__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.ekum));
\echo Finish Table ekum 
\echo . 
\echo Loading Table employee 
\copy qcserverless2.employee from '/usr1/dump-qcserverless2-20250714/employee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.employee__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.employee));
update qcserverless2.employee set child = array_replace(child,NULL,''); 
\echo Finish Table employee 
\echo . 
\echo Loading Table equiplan 
\copy qcserverless2.equiplan from '/usr1/dump-qcserverless2-20250714/equiplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.equiplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.equiplan));
\echo Finish Table equiplan 
\echo . 
\echo Loading Table exrate 
\copy qcserverless2.exrate from '/usr1/dump-qcserverless2-20250714/exrate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.exrate__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.exrate));
\echo Finish Table exrate 
\echo . 
\echo Loading Table fa_artikel 
\copy qcserverless2.fa_artikel from '/usr1/dump-qcserverless2-20250714/fa-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_artikel));
\echo Finish Table fa_artikel 
\echo . 
\echo Loading Table fa_counter 
\copy qcserverless2.fa_counter from '/usr1/dump-qcserverless2-20250714/fa-Counter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_counter__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_counter));
\echo Finish Table fa_counter 
\echo . 
\echo Loading Table fa_dp 
\copy qcserverless2.fa_dp from '/usr1/dump-qcserverless2-20250714/fa-DP.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_dp__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_dp));
\echo Finish Table fa_dp 
\echo . 
\echo Loading Table fa_grup 
\copy qcserverless2.fa_grup from '/usr1/dump-qcserverless2-20250714/fa-grup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_grup__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_grup));
\echo Finish Table fa_grup 
\echo . 
\echo Loading Table fa_kateg 
\copy qcserverless2.fa_kateg from '/usr1/dump-qcserverless2-20250714/fa-kateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_kateg__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_kateg));
\echo Finish Table fa_kateg 
\echo . 
\echo Loading Table fa_lager 
\copy qcserverless2.fa_lager from '/usr1/dump-qcserverless2-20250714/fa-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_lager__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_lager));
\echo Finish Table fa_lager 
\echo . 
\echo Loading Table fa_op 
\copy qcserverless2.fa_op from '/usr1/dump-qcserverless2-20250714/fa-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_op__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_op));
\echo Finish Table fa_op 
\echo . 
\echo Loading Table fa_order 
\copy qcserverless2.fa_order from '/usr1/dump-qcserverless2-20250714/fa-Order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_order__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_order));
\echo Finish Table fa_order 
\echo . 
\echo Loading Table fa_ordheader 
\copy qcserverless2.fa_ordheader from '/usr1/dump-qcserverless2-20250714/fa-OrdHeader.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_ordheader__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_ordheader));
\echo Finish Table fa_ordheader 
\echo . 
\echo Loading Table fa_quodetail 
\copy qcserverless2.fa_quodetail from '/usr1/dump-qcserverless2-20250714/fa-QuoDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_quodetail__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_quodetail));
\echo Finish Table fa_quodetail 
\echo . 
\echo Loading Table fa_quotation 
\copy qcserverless2.fa_quotation from '/usr1/dump-qcserverless2-20250714/fa-quotation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_quotation__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_quotation));
\echo Finish Table fa_quotation 
\echo . 
\echo Loading Table fa_user 
\copy qcserverless2.fa_user from '/usr1/dump-qcserverless2-20250714/fa-user.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fa_user__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fa_user));
update qcserverless2.fa_user set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table fa_user 
\echo . 
\echo Loading Table fbstat 
\copy qcserverless2.fbstat from '/usr1/dump-qcserverless2-20250714/fbstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fbstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fbstat));
\echo Finish Table fbstat 
\echo . 
\echo Loading Table feiertag 
\copy qcserverless2.feiertag from '/usr1/dump-qcserverless2-20250714/feiertag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.feiertag__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.feiertag));
\echo Finish Table feiertag 
\echo . 
\echo Loading Table ffont 
\copy qcserverless2.ffont from '/usr1/dump-qcserverless2-20250714/ffont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.ffont__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.ffont));
\echo Finish Table ffont 
\echo . 
\echo Loading Table fixleist 
\copy qcserverless2.fixleist from '/usr1/dump-qcserverless2-20250714/fixleist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.fixleist__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.fixleist));
\echo Finish Table fixleist 
\echo . 
\echo Loading Table gc_giro 
\copy qcserverless2.gc_giro from '/usr1/dump-qcserverless2-20250714/gc-giro.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gc_giro__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gc_giro));
update qcserverless2.gc_giro set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_giro 
\echo . 
\echo Loading Table gc_jouhdr 
\copy qcserverless2.gc_jouhdr from '/usr1/dump-qcserverless2-20250714/gc-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gc_jouhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gc_jouhdr));
\echo Finish Table gc_jouhdr 
\echo . 
\echo Loading Table gc_journal 
\copy qcserverless2.gc_journal from '/usr1/dump-qcserverless2-20250714/gc-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gc_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gc_journal));
\echo Finish Table gc_journal 
\echo . 
\echo Loading Table gc_pi 
\copy qcserverless2.gc_pi from '/usr1/dump-qcserverless2-20250714/gc-PI.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gc_pi__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gc_pi));
update qcserverless2.gc_pi set bez_array = array_replace(bez_array,NULL,''); 
update qcserverless2.gc_pi set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_pi 
\echo . 
\echo Loading Table gc_piacct 
\copy qcserverless2.gc_piacct from '/usr1/dump-qcserverless2-20250714/gc-piacct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gc_piacct__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gc_piacct));
\echo Finish Table gc_piacct 
\echo . 
\echo Loading Table gc_pibline 
\copy qcserverless2.gc_pibline from '/usr1/dump-qcserverless2-20250714/gc-PIbline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gc_pibline__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gc_pibline));
\echo Finish Table gc_pibline 
\echo . 
\echo Loading Table gc_pitype 
\copy qcserverless2.gc_pitype from '/usr1/dump-qcserverless2-20250714/gc-piType.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gc_pitype__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gc_pitype));
\echo Finish Table gc_pitype 
\echo . 
\echo Loading Table genfcast 
\copy qcserverless2.genfcast from '/usr1/dump-qcserverless2-20250714/genfcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.genfcast__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.genfcast));
update qcserverless2.genfcast set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genfcast 
\echo . 
\echo Loading Table genlayout 
\copy qcserverless2.genlayout from '/usr1/dump-qcserverless2-20250714/genlayout.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.genlayout__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.genlayout));
update qcserverless2.genlayout set button_ext = array_replace(button_ext,NULL,''); 
update qcserverless2.genlayout set char_ext = array_replace(char_ext,NULL,''); 
update qcserverless2.genlayout set combo_ext = array_replace(combo_ext,NULL,''); 
update qcserverless2.genlayout set date_ext = array_replace(date_ext,NULL,''); 
update qcserverless2.genlayout set deci_ext = array_replace(deci_ext,NULL,''); 
update qcserverless2.genlayout set inte_ext = array_replace(inte_ext,NULL,''); 
update qcserverless2.genlayout set logi_ext = array_replace(logi_ext,NULL,''); 
update qcserverless2.genlayout set string_ext = array_replace(string_ext,NULL,''); 
update qcserverless2.genlayout set tchar_ext = array_replace(tchar_ext,NULL,''); 
update qcserverless2.genlayout set tdate_ext = array_replace(tdate_ext,NULL,''); 
update qcserverless2.genlayout set tdeci_ext = array_replace(tdeci_ext,NULL,''); 
update qcserverless2.genlayout set tinte_ext = array_replace(tinte_ext,NULL,''); 
update qcserverless2.genlayout set tlogi_ext = array_replace(tlogi_ext,NULL,''); 
\echo Finish Table genlayout 
\echo . 
\echo Loading Table genstat 
\copy qcserverless2.genstat from '/usr1/dump-qcserverless2-20250714/genstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.genstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.genstat));
update qcserverless2.genstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genstat 
\echo . 
\echo Loading Table gentable 
\copy qcserverless2.gentable from '/usr1/dump-qcserverless2-20250714/gentable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gentable__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gentable));
update qcserverless2.gentable set char_ext = array_replace(char_ext,NULL,''); 
update qcserverless2.gentable set combo_ext = array_replace(combo_ext,NULL,''); 
\echo Finish Table gentable 
\echo . 
\echo Loading Table gk_field 
\copy qcserverless2.gk_field from '/usr1/dump-qcserverless2-20250714/gk-field.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gk_field__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gk_field));
\echo Finish Table gk_field 
\echo . 
\echo Loading Table gk_label 
\copy qcserverless2.gk_label from '/usr1/dump-qcserverless2-20250714/gk-label.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gk_label__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gk_label));
\echo Finish Table gk_label 
\echo . 
\echo Loading Table gk_notes 
\copy qcserverless2.gk_notes from '/usr1/dump-qcserverless2-20250714/gk-notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gk_notes__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gk_notes));
update qcserverless2.gk_notes set notes = array_replace(notes,NULL,''); 
\echo Finish Table gk_notes 
\echo . 
\echo Loading Table gl_acct 
\copy qcserverless2.gl_acct from '/usr1/dump-qcserverless2-20250714/gl-acct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_acct__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_acct));
\echo Finish Table gl_acct 
\echo . 
\echo Loading Table gl_accthis 
\copy qcserverless2.gl_accthis from '/usr1/dump-qcserverless2-20250714/gl-accthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_accthis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_accthis));
\echo Finish Table gl_accthis 
\echo . 
\echo Loading Table gl_coa 
\copy qcserverless2.gl_coa from '/usr1/dump-qcserverless2-20250714/gl-coa.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_coa__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_coa));
\echo Finish Table gl_coa 
\echo . 
\echo Loading Table gl_cost 
\copy qcserverless2.gl_cost from '/usr1/dump-qcserverless2-20250714/gl-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_cost__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_cost));
\echo Finish Table gl_cost 
\echo . 
\echo Loading Table gl_department 
\copy qcserverless2.gl_department from '/usr1/dump-qcserverless2-20250714/gl-department.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_department__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_department));
\echo Finish Table gl_department 
\echo . 
\echo Loading Table gl_fstype 
\copy qcserverless2.gl_fstype from '/usr1/dump-qcserverless2-20250714/gl-fstype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_fstype__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_fstype));
\echo Finish Table gl_fstype 
\echo . 
\echo Loading Table gl_htljournal 
\copy qcserverless2.gl_htljournal from '/usr1/dump-qcserverless2-20250714/gl-htljournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_htljournal__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_htljournal));
\echo Finish Table gl_htljournal 
\echo . 
\echo Loading Table gl_jhdrhis 
\copy qcserverless2.gl_jhdrhis from '/usr1/dump-qcserverless2-20250714/gl-jhdrhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_jhdrhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_jhdrhis));
\echo Finish Table gl_jhdrhis 
\echo . 
\echo Loading Table gl_jouhdr 
\copy qcserverless2.gl_jouhdr from '/usr1/dump-qcserverless2-20250714/gl-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_jouhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_jouhdr));
\echo Finish Table gl_jouhdr 
\echo . 
\echo Loading Table gl_jourhis 
\copy qcserverless2.gl_jourhis from '/usr1/dump-qcserverless2-20250714/gl-jourhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_jourhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_jourhis));
\echo Finish Table gl_jourhis 
\echo . 
\echo Loading Table gl_journal 
\copy qcserverless2.gl_journal from '/usr1/dump-qcserverless2-20250714/gl-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_journal));
\echo Finish Table gl_journal 
\echo . 
\echo Loading Table gl_main 
\copy qcserverless2.gl_main from '/usr1/dump-qcserverless2-20250714/gl-main.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.gl_main__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.gl_main));
\echo Finish Table gl_main 
\echo . 
\echo Loading Table golf_caddie 
\copy qcserverless2.golf_caddie from '/usr1/dump-qcserverless2-20250714/golf-caddie.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_caddie__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_caddie));
\echo Finish Table golf_caddie 
\echo . 
\echo Loading Table golf_caddie_assignment 
\copy qcserverless2.golf_caddie_assignment from '/usr1/dump-qcserverless2-20250714/golf-caddie-assignment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_caddie_assignment__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_caddie_assignment));
\echo Finish Table golf_caddie_assignment 
\echo . 
\echo Loading Table golf_course 
\copy qcserverless2.golf_course from '/usr1/dump-qcserverless2-20250714/golf-course.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_course__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_course));
\echo Finish Table golf_course 
\echo . 
\echo Loading Table golf_flight_reservation 
\copy qcserverless2.golf_flight_reservation from '/usr1/dump-qcserverless2-20250714/golf-flight-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_flight_reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_flight_reservation));
\echo Finish Table golf_flight_reservation 
\echo . 
\echo Loading Table golf_flight_reservation_hist 
\copy qcserverless2.golf_flight_reservation_hist from '/usr1/dump-qcserverless2-20250714/golf-flight-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_flight_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_flight_reservation_hist));
\echo Finish Table golf_flight_reservation_hist 
\echo . 
\echo Loading Table golf_golfer_reservation 
\copy qcserverless2.golf_golfer_reservation from '/usr1/dump-qcserverless2-20250714/golf-golfer-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_golfer_reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_golfer_reservation));
\echo Finish Table golf_golfer_reservation 
\echo . 
\echo Loading Table golf_golfer_reservation_hist 
\copy qcserverless2.golf_golfer_reservation_hist from '/usr1/dump-qcserverless2-20250714/golf-golfer-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_golfer_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_golfer_reservation_hist));
\echo Finish Table golf_golfer_reservation_hist 
\echo . 
\echo Loading Table golf_holiday 
\copy qcserverless2.golf_holiday from '/usr1/dump-qcserverless2-20250714/golf-holiday.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_holiday__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_holiday));
\echo Finish Table golf_holiday 
\echo . 
\echo Loading Table golf_main_reservation 
\copy qcserverless2.golf_main_reservation from '/usr1/dump-qcserverless2-20250714/golf-main-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_main_reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_main_reservation));
\echo Finish Table golf_main_reservation 
\echo . 
\echo Loading Table golf_main_reservation_hist 
\copy qcserverless2.golf_main_reservation_hist from '/usr1/dump-qcserverless2-20250714/golf-main-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_main_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_main_reservation_hist));
\echo Finish Table golf_main_reservation_hist 
\echo . 
\echo Loading Table golf_rate 
\copy qcserverless2.golf_rate from '/usr1/dump-qcserverless2-20250714/golf-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_rate__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_rate));
\echo Finish Table golf_rate 
\echo . 
\echo Loading Table golf_shift 
\copy qcserverless2.golf_shift from '/usr1/dump-qcserverless2-20250714/golf-shift.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_shift__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_shift));
\echo Finish Table golf_shift 
\echo . 
\echo Loading Table golf_transfer 
\copy qcserverless2.golf_transfer from '/usr1/dump-qcserverless2-20250714/golf-transfer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.golf_transfer__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.golf_transfer));
\echo Finish Table golf_transfer 
\echo . 
\echo Loading Table guest 
\copy qcserverless2.guest from '/usr1/dump-qcserverless2-20250714/guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guest__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guest));
update qcserverless2.guest set notizen = array_replace(notizen,NULL,''); 
update qcserverless2.guest set vornamekind = array_replace(vornamekind,NULL,''); 
\echo Finish Table guest 
\echo . 
\echo Loading Table guest_pr 
\copy qcserverless2.guest_pr from '/usr1/dump-qcserverless2-20250714/guest-pr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guest_pr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guest_pr));
\echo Finish Table guest_pr 
\echo . 
\echo Loading Table guest_queasy 
\copy qcserverless2.guest_queasy from '/usr1/dump-qcserverless2-20250714/guest-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guest_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guest_queasy));
\echo Finish Table guest_queasy 
\echo . 
\echo Loading Table guest_remark 
\copy qcserverless2.guest_remark from '/usr1/dump-qcserverless2-20250714/guest-remark.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guest_remark__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guest_remark));
update qcserverless2.guest_remark set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table guest_remark 
\echo . 
\echo Loading Table guestat 
\copy qcserverless2.guestat from '/usr1/dump-qcserverless2-20250714/guestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guestat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guestat));
\echo Finish Table guestat 
\echo . 
\echo Loading Table guestat1 
\copy qcserverless2.guestat1 from '/usr1/dump-qcserverless2-20250714/guestat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guestat1__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guestat1));
\echo Finish Table guestat1 
\echo . 
\echo Loading Table guestbook 
\copy qcserverless2.guestbook from '/usr1/dump-qcserverless2-20250714/guestbook.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guestbook__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guestbook));
update qcserverless2.guestbook set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table guestbook 
\echo . 
\echo Loading Table guestbud 
\copy qcserverless2.guestbud from '/usr1/dump-qcserverless2-20250714/guestbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guestbud__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guestbud));
\echo Finish Table guestbud 
\echo . 
\echo Loading Table guestseg 
\copy qcserverless2.guestseg from '/usr1/dump-qcserverless2-20250714/guestseg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.guestseg__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.guestseg));
\echo Finish Table guestseg 
\echo . 
\echo Loading Table h_artcost 
\copy qcserverless2.h_artcost from '/usr1/dump-qcserverless2-20250714/h-artcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_artcost__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_artcost));
\echo Finish Table h_artcost 
\echo . 
\echo Loading Table h_artikel 
\copy qcserverless2.h_artikel from '/usr1/dump-qcserverless2-20250714/h-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_artikel));
\echo Finish Table h_artikel 
\echo . 
\echo Loading Table h_bill 
\copy qcserverless2.h_bill from '/usr1/dump-qcserverless2-20250714/h-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_bill__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_bill));
\echo Finish Table h_bill 
\echo . 
\echo Loading Table h_bill_line 
\copy qcserverless2.h_bill_line from '/usr1/dump-qcserverless2-20250714/h-bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_bill_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_bill_line));
\echo Finish Table h_bill_line 
\echo . 
\echo Loading Table h_compli 
\copy qcserverless2.h_compli from '/usr1/dump-qcserverless2-20250714/h-compli.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_compli__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_compli));
\echo Finish Table h_compli 
\echo . 
\echo Loading Table h_cost 
\copy qcserverless2.h_cost from '/usr1/dump-qcserverless2-20250714/h-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_cost__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_cost));
\echo Finish Table h_cost 
\echo . 
\echo Loading Table h_journal 
\copy qcserverless2.h_journal from '/usr1/dump-qcserverless2-20250714/h-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_journal__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_journal));
\echo Finish Table h_journal 
\echo . 
\echo Loading Table h_menu 
\copy qcserverless2.h_menu from '/usr1/dump-qcserverless2-20250714/h-menu.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_menu__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_menu));
\echo Finish Table h_menu 
\echo . 
\echo Loading Table h_mjourn 
\copy qcserverless2.h_mjourn from '/usr1/dump-qcserverless2-20250714/h-mjourn.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_mjourn__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_mjourn));
\echo Finish Table h_mjourn 
\echo . 
\echo Loading Table h_oldjou 
\copy qcserverless2.h_oldjou from '/usr1/dump-qcserverless2-20250714/h-oldjou.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_oldjou__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_oldjou));
\echo Finish Table h_oldjou 
\echo . 
\echo Loading Table h_order 
\copy qcserverless2.h_order from '/usr1/dump-qcserverless2-20250714/h-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_order__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_order));
update qcserverless2.h_order set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table h_order 
\echo . 
\echo Loading Table h_queasy 
\copy qcserverless2.h_queasy from '/usr1/dump-qcserverless2-20250714/h-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_queasy));
\echo Finish Table h_queasy 
\echo . 
\echo Loading Table h_rezept 
\copy qcserverless2.h_rezept from '/usr1/dump-qcserverless2-20250714/h-rezept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_rezept__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_rezept));
\echo Finish Table h_rezept 
\echo . 
\echo Loading Table h_rezlin 
\copy qcserverless2.h_rezlin from '/usr1/dump-qcserverless2-20250714/h-rezlin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_rezlin__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_rezlin));
\echo Finish Table h_rezlin 
\echo . 
\echo Loading Table h_storno 
\copy qcserverless2.h_storno from '/usr1/dump-qcserverless2-20250714/h-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_storno__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_storno));
\echo Finish Table h_storno 
\echo . 
\echo Loading Table h_umsatz 
\copy qcserverless2.h_umsatz from '/usr1/dump-qcserverless2-20250714/h-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.h_umsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.h_umsatz));
\echo Finish Table h_umsatz 
\echo . 
\echo Loading Table history 
\copy qcserverless2.history from '/usr1/dump-qcserverless2-20250714/history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.history__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.history));
\echo Finish Table history 
\echo . 
\echo Loading Table hoteldpt 
\copy qcserverless2.hoteldpt from '/usr1/dump-qcserverless2-20250714/hoteldpt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.hoteldpt__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.hoteldpt));
\echo Finish Table hoteldpt 
\echo . 
\echo Loading Table hrbeleg 
\copy qcserverless2.hrbeleg from '/usr1/dump-qcserverless2-20250714/hrbeleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.hrbeleg__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.hrbeleg));
\echo Finish Table hrbeleg 
\echo . 
\echo Loading Table hrsegement 
\copy qcserverless2.hrsegement from '/usr1/dump-qcserverless2-20250714/hrsegement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.hrsegement__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.hrsegement));
\echo Finish Table hrsegement 
\echo . 
\echo Loading Table htparam 
\copy qcserverless2.htparam from '/usr1/dump-qcserverless2-20250714/htparam.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.htparam__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.htparam));
\echo Finish Table htparam 
\echo . 
\echo Loading Table htreport 
\copy qcserverless2.htreport from '/usr1/dump-qcserverless2-20250714/htreport.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.htreport__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.htreport));
\echo Finish Table htreport 
\echo . 
\echo Loading Table iftable 
\copy qcserverless2.iftable from '/usr1/dump-qcserverless2-20250714/iftable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.iftable__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.iftable));
\echo Finish Table iftable 
\echo . 
\echo Loading Table interface 
\copy qcserverless2.interface from '/usr1/dump-qcserverless2-20250714/interface.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.interface__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.interface));
\echo Finish Table interface 
\echo . 
\echo Loading Table k_history 
\copy qcserverless2.k_history from '/usr1/dump-qcserverless2-20250714/k-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.k_history__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.k_history));
\echo Finish Table k_history 
\echo . 
\echo Loading Table kabine 
\copy qcserverless2.kabine from '/usr1/dump-qcserverless2-20250714/kabine.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kabine__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kabine));
\echo Finish Table kabine 
\echo . 
\echo Loading Table kalender 
\copy qcserverless2.kalender from '/usr1/dump-qcserverless2-20250714/kalender.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kalender__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kalender));
update qcserverless2.kalender set note = array_replace(note,NULL,''); 
\echo Finish Table kalender 
\echo . 
\echo Loading Table kasse 
\copy qcserverless2.kasse from '/usr1/dump-qcserverless2-20250714/kasse.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kasse__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kasse));
\echo Finish Table kasse 
\echo . 
\echo Loading Table katpreis 
\copy qcserverless2.katpreis from '/usr1/dump-qcserverless2-20250714/katpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.katpreis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.katpreis));
\echo Finish Table katpreis 
\echo . 
\echo Loading Table kellne1 
\copy qcserverless2.kellne1 from '/usr1/dump-qcserverless2-20250714/kellne1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kellne1__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kellne1));
\echo Finish Table kellne1 
\echo . 
\echo Loading Table kellner 
\copy qcserverless2.kellner from '/usr1/dump-qcserverless2-20250714/kellner.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kellner__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kellner));
\echo Finish Table kellner 
\echo . 
\echo Loading Table kontakt 
\copy qcserverless2.kontakt from '/usr1/dump-qcserverless2-20250714/kontakt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kontakt__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kontakt));
\echo Finish Table kontakt 
\echo . 
\echo Loading Table kontline 
\copy qcserverless2.kontline from '/usr1/dump-qcserverless2-20250714/kontline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kontline__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kontline));
\echo Finish Table kontline 
\echo . 
\echo Loading Table kontlink 
\copy qcserverless2.kontlink from '/usr1/dump-qcserverless2-20250714/kontlink.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kontlink__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kontlink));
\echo Finish Table kontlink 
\echo . 
\echo Loading Table kontplan 
\copy qcserverless2.kontplan from '/usr1/dump-qcserverless2-20250714/kontplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kontplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kontplan));
\echo Finish Table kontplan 
\echo . 
\echo Loading Table kontstat 
\copy qcserverless2.kontstat from '/usr1/dump-qcserverless2-20250714/kontstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kontstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kontstat));
update qcserverless2.kontstat set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table kontstat 
\echo . 
\echo Loading Table kresline 
\copy qcserverless2.kresline from '/usr1/dump-qcserverless2-20250714/kresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.kresline__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.kresline));
\echo Finish Table kresline 
\echo . 
\echo Loading Table l_artikel 
\copy qcserverless2.l_artikel from '/usr1/dump-qcserverless2-20250714/l-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_artikel__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_artikel));
update qcserverless2.l_artikel set lief_artnr = array_replace(lief_artnr,NULL,''); 
\echo Finish Table l_artikel 
\echo . 
\echo Loading Table l_bestand 
\copy qcserverless2.l_bestand from '/usr1/dump-qcserverless2-20250714/l-bestand.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_bestand__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_bestand));
\echo Finish Table l_bestand 
\echo . 
\echo Loading Table l_besthis 
\copy qcserverless2.l_besthis from '/usr1/dump-qcserverless2-20250714/l-besthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_besthis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_besthis));
\echo Finish Table l_besthis 
\echo . 
\echo Loading Table l_hauptgrp 
\copy qcserverless2.l_hauptgrp from '/usr1/dump-qcserverless2-20250714/l-hauptgrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_hauptgrp__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_hauptgrp));
\echo Finish Table l_hauptgrp 
\echo . 
\echo Loading Table l_kredit 
\copy qcserverless2.l_kredit from '/usr1/dump-qcserverless2-20250714/l-kredit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_kredit__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_kredit));
\echo Finish Table l_kredit 
\echo . 
\echo Loading Table l_lager 
\copy qcserverless2.l_lager from '/usr1/dump-qcserverless2-20250714/l-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_lager__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_lager));
\echo Finish Table l_lager 
\echo . 
\echo Loading Table l_lieferant 
\copy qcserverless2.l_lieferant from '/usr1/dump-qcserverless2-20250714/l-lieferant.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_lieferant__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_lieferant));
update qcserverless2.l_lieferant set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table l_lieferant 
\echo . 
\echo Loading Table l_liefumsatz 
\copy qcserverless2.l_liefumsatz from '/usr1/dump-qcserverless2-20250714/l-liefumsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_liefumsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_liefumsatz));
\echo Finish Table l_liefumsatz 
\echo . 
\echo Loading Table l_op 
\copy qcserverless2.l_op from '/usr1/dump-qcserverless2-20250714/l-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_op__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_op));
\echo Finish Table l_op 
\echo . 
\echo Loading Table l_ophdr 
\copy qcserverless2.l_ophdr from '/usr1/dump-qcserverless2-20250714/l-ophdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_ophdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_ophdr));
\echo Finish Table l_ophdr 
\echo . 
\echo Loading Table l_ophhis 
\copy qcserverless2.l_ophhis from '/usr1/dump-qcserverless2-20250714/l-ophhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_ophhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_ophhis));
\echo Finish Table l_ophhis 
\echo . 
\echo Loading Table l_ophis 
\copy qcserverless2.l_ophis from '/usr1/dump-qcserverless2-20250714/l-ophis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_ophis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_ophis));
\echo Finish Table l_ophis 
\echo . 
\echo Loading Table l_order 
\copy qcserverless2.l_order from '/usr1/dump-qcserverless2-20250714/l-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_order__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_order));
update qcserverless2.l_order set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_order 
\echo . 
\echo Loading Table l_orderhdr 
\copy qcserverless2.l_orderhdr from '/usr1/dump-qcserverless2-20250714/l-orderhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_orderhdr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_orderhdr));
update qcserverless2.l_orderhdr set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_orderhdr 
\echo . 
\echo Loading Table l_pprice 
\copy qcserverless2.l_pprice from '/usr1/dump-qcserverless2-20250714/l-pprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_pprice__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_pprice));
\echo Finish Table l_pprice 
\echo . 
\echo Loading Table l_quote 
\copy qcserverless2.l_quote from '/usr1/dump-qcserverless2-20250714/l-quote.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_quote__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_quote));
update qcserverless2.l_quote set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table l_quote 
\echo . 
\echo Loading Table l_segment 
\copy qcserverless2.l_segment from '/usr1/dump-qcserverless2-20250714/l-segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_segment__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_segment));
\echo Finish Table l_segment 
\echo . 
\echo Loading Table l_umsatz 
\copy qcserverless2.l_umsatz from '/usr1/dump-qcserverless2-20250714/l-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_umsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_umsatz));
\echo Finish Table l_umsatz 
\echo . 
\echo Loading Table l_untergrup 
\copy qcserverless2.l_untergrup from '/usr1/dump-qcserverless2-20250714/l-untergrup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_untergrup__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_untergrup));
\echo Finish Table l_untergrup 
\echo . 
\echo Loading Table l_verbrauch 
\copy qcserverless2.l_verbrauch from '/usr1/dump-qcserverless2-20250714/l-verbrauch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_verbrauch__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_verbrauch));
\echo Finish Table l_verbrauch 
\echo . 
\echo Loading Table l_zahlbed 
\copy qcserverless2.l_zahlbed from '/usr1/dump-qcserverless2-20250714/l-zahlbed.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.l_zahlbed__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.l_zahlbed));
\echo Finish Table l_zahlbed 
\echo . 
\echo Loading Table landstat 
\copy qcserverless2.landstat from '/usr1/dump-qcserverless2-20250714/landstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.landstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.landstat));
\echo Finish Table landstat 
\echo . 
\echo Loading Table masseur 
\copy qcserverless2.masseur from '/usr1/dump-qcserverless2-20250714/masseur.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.masseur__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.masseur));
\echo Finish Table masseur 
\echo . 
\echo Loading Table mast_art 
\copy qcserverless2.mast_art from '/usr1/dump-qcserverless2-20250714/mast-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mast_art__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mast_art));
\echo Finish Table mast_art 
\echo . 
\echo Loading Table master 
\copy qcserverless2.master from '/usr1/dump-qcserverless2-20250714/master.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.master__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.master));
\echo Finish Table master 
\echo . 
\echo Loading Table mathis 
\copy qcserverless2.mathis from '/usr1/dump-qcserverless2-20250714/mathis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mathis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mathis));
\echo Finish Table mathis 
\echo . 
\echo Loading Table mc_aclub 
\copy qcserverless2.mc_aclub from '/usr1/dump-qcserverless2-20250714/mc-aclub.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mc_aclub__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mc_aclub));
\echo Finish Table mc_aclub 
\echo . 
\echo Loading Table mc_cardhis 
\copy qcserverless2.mc_cardhis from '/usr1/dump-qcserverless2-20250714/mc-cardhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mc_cardhis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mc_cardhis));
\echo Finish Table mc_cardhis 
\echo . 
\echo Loading Table mc_disc 
\copy qcserverless2.mc_disc from '/usr1/dump-qcserverless2-20250714/mc-disc.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mc_disc__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mc_disc));
\echo Finish Table mc_disc 
\echo . 
\echo Loading Table mc_fee 
\copy qcserverless2.mc_fee from '/usr1/dump-qcserverless2-20250714/mc-fee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mc_fee__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mc_fee));
\echo Finish Table mc_fee 
\echo . 
\echo Loading Table mc_guest 
\copy qcserverless2.mc_guest from '/usr1/dump-qcserverless2-20250714/mc-guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mc_guest__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mc_guest));
\echo Finish Table mc_guest 
\echo . 
\echo Loading Table mc_types 
\copy qcserverless2.mc_types from '/usr1/dump-qcserverless2-20250714/mc-types.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mc_types__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mc_types));
\echo Finish Table mc_types 
\echo . 
\echo Loading Table mealcoup 
\copy qcserverless2.mealcoup from '/usr1/dump-qcserverless2-20250714/mealcoup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mealcoup__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mealcoup));
\echo Finish Table mealcoup 
\echo . 
\echo Loading Table messages 
\copy qcserverless2.messages from '/usr1/dump-qcserverless2-20250714/messages.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.messages__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.messages));
update qcserverless2.messages set messtext = array_replace(messtext,NULL,''); 
\echo Finish Table messages 
\echo . 
\echo Loading Table messe 
\copy qcserverless2.messe from '/usr1/dump-qcserverless2-20250714/messe.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.messe__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.messe));
\echo Finish Table messe 
\echo . 
\echo Loading Table mhis_line 
\copy qcserverless2.mhis_line from '/usr1/dump-qcserverless2-20250714/mhis-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.mhis_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.mhis_line));
\echo Finish Table mhis_line 
\echo . 
\echo Loading Table nation 
\copy qcserverless2.nation from '/usr1/dump-qcserverless2-20250714/nation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.nation__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.nation));
\echo Finish Table nation 
\echo . 
\echo Loading Table nationstat 
\copy qcserverless2.nationstat from '/usr1/dump-qcserverless2-20250714/nationstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.nationstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.nationstat));
\echo Finish Table nationstat 
\echo . 
\echo Loading Table natstat1 
\copy qcserverless2.natstat1 from '/usr1/dump-qcserverless2-20250714/natstat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.natstat1__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.natstat1));
\echo Finish Table natstat1 
\echo . 
\echo Loading Table nebenst 
\copy qcserverless2.nebenst from '/usr1/dump-qcserverless2-20250714/nebenst.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.nebenst__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.nebenst));
\echo Finish Table nebenst 
\echo . 
\echo Loading Table nightaudit 
\copy qcserverless2.nightaudit from '/usr1/dump-qcserverless2-20250714/nightaudit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.nightaudit__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.nightaudit));
\echo Finish Table nightaudit 
\echo . 
\echo Loading Table nitehist 
\copy qcserverless2.nitehist from '/usr1/dump-qcserverless2-20250714/nitehist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.nitehist__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.nitehist));
\echo Finish Table nitehist 
\echo . 
\echo Loading Table nitestor 
\copy qcserverless2.nitestor from '/usr1/dump-qcserverless2-20250714/nitestor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.nitestor__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.nitestor));
\echo Finish Table nitestor 
\echo . 
\echo Loading Table notes 
\copy qcserverless2.notes from '/usr1/dump-qcserverless2-20250714/notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.notes__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.notes));
update qcserverless2.notes set note = array_replace(note,NULL,''); 
\echo Finish Table notes 
\echo . 
\echo Loading Table outorder 
\copy qcserverless2.outorder from '/usr1/dump-qcserverless2-20250714/outorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.outorder__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.outorder));
\echo Finish Table outorder 
\echo . 
\echo Loading Table package 
\copy qcserverless2.package from '/usr1/dump-qcserverless2-20250714/package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.package__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.package));
\echo Finish Table package 
\echo . 
\echo Loading Table parameters 
\copy qcserverless2.parameters from '/usr1/dump-qcserverless2-20250714/parameters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.parameters__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.parameters));
\echo Finish Table parameters 
\echo . 
\echo Loading Table paramtext 
\copy qcserverless2.paramtext from '/usr1/dump-qcserverless2-20250714/paramtext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.paramtext__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.paramtext));
\echo Finish Table paramtext 
\echo . 
\echo Loading Table pricecod 
\copy qcserverless2.pricecod from '/usr1/dump-qcserverless2-20250714/pricecod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.pricecod__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.pricecod));
\echo Finish Table pricecod 
\echo . 
\echo Loading Table pricegrp 
\copy qcserverless2.pricegrp from '/usr1/dump-qcserverless2-20250714/pricegrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.pricegrp__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.pricegrp));
\echo Finish Table pricegrp 
\echo . 
\echo Loading Table printcod 
\copy qcserverless2.printcod from '/usr1/dump-qcserverless2-20250714/printcod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.printcod__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.printcod));
\echo Finish Table printcod 
\echo . 
\echo Loading Table printer 
\copy qcserverless2.printer from '/usr1/dump-qcserverless2-20250714/printer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.printer__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.printer));
\echo Finish Table printer 
\echo . 
\echo Loading Table prmarket 
\copy qcserverless2.prmarket from '/usr1/dump-qcserverless2-20250714/prmarket.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.prmarket__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.prmarket));
\echo Finish Table prmarket 
\echo . 
\echo Loading Table progcat 
\copy qcserverless2.progcat from '/usr1/dump-qcserverless2-20250714/progcat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.progcat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.progcat));
\echo Finish Table progcat 
\echo . 
\echo Loading Table progfile 
\copy qcserverless2.progfile from '/usr1/dump-qcserverless2-20250714/progfile.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.progfile__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.progfile));
\echo Finish Table progfile 
\echo . 
\echo Loading Table prtable 
\copy qcserverless2.prtable from '/usr1/dump-qcserverless2-20250714/prtable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.prtable__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.prtable));
\echo Finish Table prtable 
\echo . 
\echo Loading Table queasy 
\copy qcserverless2.queasy from '/usr1/dump-qcserverless2-20250714/queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.queasy));
\echo Finish Table queasy 
\echo . 
\echo Loading Table ratecode 
\copy qcserverless2.ratecode from '/usr1/dump-qcserverless2-20250714/ratecode.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.ratecode__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.ratecode));
update qcserverless2.ratecode set char1 = array_replace(char1,NULL,''); 
\echo Finish Table ratecode 
\echo . 
\echo Loading Table raum 
\copy qcserverless2.raum from '/usr1/dump-qcserverless2-20250714/raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.raum__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.raum));
\echo Finish Table raum 
\echo . 
\echo Loading Table res_history 
\copy qcserverless2.res_history from '/usr1/dump-qcserverless2-20250714/res-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.res_history__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.res_history));
\echo Finish Table res_history 
\echo . 
\echo Loading Table res_line 
\copy qcserverless2.res_line from '/usr1/dump-qcserverless2-20250714/res-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.res_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.res_line));
\echo Finish Table res_line 
\echo . 
\echo Loading Table reservation 
\copy qcserverless2.reservation from '/usr1/dump-qcserverless2-20250714/reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.reservation__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.reservation));
\echo Finish Table reservation 
\echo . 
\echo Loading Table reslin_queasy 
\copy qcserverless2.reslin_queasy from '/usr1/dump-qcserverless2-20250714/reslin-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.reslin_queasy__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.reslin_queasy));
\echo Finish Table reslin_queasy 
\echo . 
\echo Loading Table resplan 
\copy qcserverless2.resplan from '/usr1/dump-qcserverless2-20250714/resplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.resplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.resplan));
\echo Finish Table resplan 
\echo . 
\echo Loading Table rg_reports 
\copy qcserverless2.rg_reports from '/usr1/dump-qcserverless2-20250714/rg-reports.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.rg_reports__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.rg_reports));
update qcserverless2.rg_reports set metadata = array_replace(metadata,NULL,''); 
update qcserverless2.rg_reports set slice_name = array_replace(slice_name,NULL,''); 
update qcserverless2.rg_reports set view_name = array_replace(view_name,NULL,''); 
\echo Finish Table rg_reports 
\echo . 
\echo Loading Table rmbudget 
\copy qcserverless2.rmbudget from '/usr1/dump-qcserverless2-20250714/rmbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.rmbudget__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.rmbudget));
update qcserverless2.rmbudget set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table rmbudget 
\echo . 
\echo Loading Table sales 
\copy qcserverless2.sales from '/usr1/dump-qcserverless2-20250714/sales.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sales__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sales));
\echo Finish Table sales 
\echo . 
\echo Loading Table salesbud 
\copy qcserverless2.salesbud from '/usr1/dump-qcserverless2-20250714/salesbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.salesbud__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.salesbud));
\echo Finish Table salesbud 
\echo . 
\echo Loading Table salestat 
\copy qcserverless2.salestat from '/usr1/dump-qcserverless2-20250714/salestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.salestat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.salestat));
\echo Finish Table salestat 
\echo . 
\echo Loading Table salestim 
\copy qcserverless2.salestim from '/usr1/dump-qcserverless2-20250714/salestim.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.salestim__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.salestim));
\echo Finish Table salestim 
\echo . 
\echo Loading Table segment 
\copy qcserverless2.segment from '/usr1/dump-qcserverless2-20250714/segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.segment__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.segment));
\echo Finish Table segment 
\echo . 
\echo Loading Table segmentstat 
\copy qcserverless2.segmentstat from '/usr1/dump-qcserverless2-20250714/segmentstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.segmentstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.segmentstat));
\echo Finish Table segmentstat 
\echo . 
\echo Loading Table sms_bcaster 
\copy qcserverless2.sms_bcaster from '/usr1/dump-qcserverless2-20250714/sms-bcaster.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sms_bcaster__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sms_bcaster));
\echo Finish Table sms_bcaster 
\echo . 
\echo Loading Table sms_broadcast 
\copy qcserverless2.sms_broadcast from '/usr1/dump-qcserverless2-20250714/sms-broadcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sms_broadcast__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sms_broadcast));
\echo Finish Table sms_broadcast 
\echo . 
\echo Loading Table sms_group 
\copy qcserverless2.sms_group from '/usr1/dump-qcserverless2-20250714/sms-group.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sms_group__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sms_group));
\echo Finish Table sms_group 
\echo . 
\echo Loading Table sms_groupmbr 
\copy qcserverless2.sms_groupmbr from '/usr1/dump-qcserverless2-20250714/sms-groupmbr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sms_groupmbr__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sms_groupmbr));
\echo Finish Table sms_groupmbr 
\echo . 
\echo Loading Table sms_received 
\copy qcserverless2.sms_received from '/usr1/dump-qcserverless2-20250714/sms-received.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sms_received__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sms_received));
\echo Finish Table sms_received 
\echo . 
\echo Loading Table sourccod 
\copy qcserverless2.sourccod from '/usr1/dump-qcserverless2-20250714/Sourccod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sourccod__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sourccod));
\echo Finish Table sourccod 
\echo . 
\echo Loading Table sources 
\copy qcserverless2.sources from '/usr1/dump-qcserverless2-20250714/sources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sources__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sources));
\echo Finish Table sources 
\echo . 
\echo Loading Table sourcetext 
\copy qcserverless2.sourcetext from '/usr1/dump-qcserverless2-20250714/sourcetext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.sourcetext__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.sourcetext));
\echo Finish Table sourcetext 
\echo . 
\echo Loading Table telephone 
\copy qcserverless2.telephone from '/usr1/dump-qcserverless2-20250714/telephone.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.telephone__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.telephone));
\echo Finish Table telephone 
\echo . 
\echo Loading Table texte 
\copy qcserverless2.texte from '/usr1/dump-qcserverless2-20250714/texte.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.texte__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.texte));
\echo Finish Table texte 
\echo . 
\echo Loading Table tisch 
\copy qcserverless2.tisch from '/usr1/dump-qcserverless2-20250714/tisch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.tisch__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.tisch));
\echo Finish Table tisch 
\echo . 
\echo Loading Table tisch_res 
\copy qcserverless2.tisch_res from '/usr1/dump-qcserverless2-20250714/tisch-res.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.tisch_res__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.tisch_res));
\echo Finish Table tisch_res 
\echo . 
\echo Loading Table uebertrag 
\copy qcserverless2.uebertrag from '/usr1/dump-qcserverless2-20250714/uebertrag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.uebertrag__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.uebertrag));
\echo Finish Table uebertrag 
\echo . 
\echo Loading Table umsatz 
\copy qcserverless2.umsatz from '/usr1/dump-qcserverless2-20250714/umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.umsatz__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.umsatz));
\echo Finish Table umsatz 
\echo . 
\echo Loading Table waehrung 
\copy qcserverless2.waehrung from '/usr1/dump-qcserverless2-20250714/waehrung.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.waehrung__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.waehrung));
\echo Finish Table waehrung 
\echo . 
\echo Loading Table wakeup 
\copy qcserverless2.wakeup from '/usr1/dump-qcserverless2-20250714/wakeup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.wakeup__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.wakeup));
\echo Finish Table wakeup 
\echo . 
\echo Loading Table wgrpdep 
\copy qcserverless2.wgrpdep from '/usr1/dump-qcserverless2-20250714/wgrpdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.wgrpdep__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.wgrpdep));
\echo Finish Table wgrpdep 
\echo . 
\echo Loading Table wgrpgen 
\copy qcserverless2.wgrpgen from '/usr1/dump-qcserverless2-20250714/wgrpgen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.wgrpgen__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.wgrpgen));
\echo Finish Table wgrpgen 
\echo . 
\echo Loading Table zimkateg 
\copy qcserverless2.zimkateg from '/usr1/dump-qcserverless2-20250714/zimkateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zimkateg__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zimkateg));
\echo Finish Table zimkateg 
\echo . 
\echo Loading Table zimmer 
\copy qcserverless2.zimmer from '/usr1/dump-qcserverless2-20250714/zimmer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zimmer__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zimmer));
update qcserverless2.zimmer set verbindung = array_replace(verbindung,NULL,''); 
\echo Finish Table zimmer 
\echo . 
\echo Loading Table zimmer_book 
\copy qcserverless2.zimmer_book from '/usr1/dump-qcserverless2-20250714/zimmer-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zimmer_book__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zimmer_book));
\echo Finish Table zimmer_book 
\echo . 
\echo Loading Table zimmer_book_line 
\copy qcserverless2.zimmer_book_line from '/usr1/dump-qcserverless2-20250714/zimmer-book-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zimmer_book_line__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zimmer_book_line));
\echo Finish Table zimmer_book_line 
\echo . 
\echo Loading Table zimplan 
\copy qcserverless2.zimplan from '/usr1/dump-qcserverless2-20250714/zimplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zimplan__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zimplan));
\echo Finish Table zimplan 
\echo . 
\echo Loading Table zimpreis 
\copy qcserverless2.zimpreis from '/usr1/dump-qcserverless2-20250714/zimpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zimpreis__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zimpreis));
\echo Finish Table zimpreis 
\echo . 
\echo Loading Table zinrstat 
\copy qcserverless2.zinrstat from '/usr1/dump-qcserverless2-20250714/zinrstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zinrstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zinrstat));
\echo Finish Table zinrstat 
\echo . 
\echo Loading Table zkstat 
\copy qcserverless2.zkstat from '/usr1/dump-qcserverless2-20250714/zkstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zkstat__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zkstat));
\echo Finish Table zkstat 
\echo . 
\echo Loading Table zwkum 
\copy qcserverless2.zwkum from '/usr1/dump-qcserverless2-20250714/zwkum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcserverless2.zwkum__recid_seq', (SELECT MAX(_recid) FROM qcserverless2.zwkum));
\echo Finish Table zwkum 
\echo . 
