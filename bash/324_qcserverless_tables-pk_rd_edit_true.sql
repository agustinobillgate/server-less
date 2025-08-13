SET search_path='qcserverless4',public;

CREATE COLLATION case_insensitive (
    provider = icu,
    locale = 'und-u-ks-level2',
    deterministic = true
);

CREATE TABLE absen (
	gastnr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anrede CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	abstatus INT DEFAULT 0,
	ci_date DATE,
	ci_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	co_date DATE,
	co_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	box_no CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gtype INT DEFAULT 0,
	carnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	total_adult INT[2] DEFAULT ARRAY[0,0],
	total_child INT[2] DEFAULT ARRAY[0,0],
	total_infant INT[2] DEFAULT ARRAY[0,0],
	ci_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	co_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	resline INT DEFAULT 1,
	_recid serial PRIMARY KEY
);
CREATE INDEX absen_abstatus_ix ON absen (abstatus);
CREATE INDEX absen_car_ix ON absen (carnr COLLATE case_insensitive,abstatus);
CREATE INDEX absen_ci_car_ix ON absen (carnr COLLATE case_insensitive,ci_date);
CREATE INDEX absen_ci_ix ON absen (ci_date);
CREATE INDEX absen_ci_name_car_ix ON absen (name COLLATE case_insensitive,carnr COLLATE case_insensitive,ci_date);
CREATE INDEX absen_ci_name_ix ON absen (name COLLATE case_insensitive,ci_date);
CREATE INDEX absen_co_car_ix ON absen (carnr COLLATE case_insensitive,co_date);
CREATE INDEX absen_co_ix ON absen (co_date);
CREATE INDEX absen_co_name_car_ix ON absen (name COLLATE case_insensitive,carnr COLLATE case_insensitive,co_date);
CREATE INDEX absen_co_name_ix ON absen (name COLLATE case_insensitive,co_date);
CREATE INDEX absen_name_car_ix ON absen (name COLLATE case_insensitive,carnr COLLATE case_insensitive,abstatus);
CREATE INDEX absen_name_ix ON absen (name COLLATE case_insensitive,abstatus);
CREATE INDEX absen_res_status_ix ON absen (resnr,resline,abstatus);
CREATE TABLE akt_code (
	aktionscode INT DEFAULT 0,
	aktiongrup INT DEFAULT 1,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	korrespondenz BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	wertigkeit INT DEFAULT 0,
	flag INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX akt_code_aktbez_ix ON akt_code (bezeich COLLATE case_insensitive);
CREATE INDEX akt_code_aktion_ix ON akt_code (betriebsnr,aktiongrup,aktionscode);
CREATE TABLE akt_cust (
	gastnr INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	c_init CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX akt_cust_gast_ix ON akt_cust (gastnr);
CREATE INDEX akt_cust_init_ix ON akt_cust (userinit COLLATE case_insensitive);
CREATE TABLE akt_kont (
	gastnr INT DEFAULT 0,
	Kategorie INT DEFAULT 0,
	kontakt_nr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	funktion CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	abteilung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sprachcode INT DEFAULT 1,
	anrede CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nation2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ausweis_art CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ausweis_nr1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	geburtdatum1 DATE,
	geburt_ort1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	pass_aust1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	durchwahl CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	hauptkontakt BOOLEAN DEFAULT False,
	pers_bez INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	email_adr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	v_titel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	a_titel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	briefanrede CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telefon_privat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fax_privat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX akt_kont_kontakt_ix ON akt_kont (gastnr,kontakt_nr);
CREATE INDEX akt_kont_name_ix ON akt_kont (name COLLATE case_insensitive,vorname COLLATE case_insensitive);
CREATE TABLE akt_line (
	aktnr INT DEFAULT 0,
	aktionscode INT DEFAULT 0,
	datum DATE,
	dauer INT DEFAULT 0,
	briefnr INT DEFAULT 0,
	fname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chg_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chg_datum DATE,
	kontakt_nr INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zeit INT DEFAULT 0,
	prioritaet INT DEFAULT 0,
	kontakt CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	regard CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	location CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	linenr INT DEFAULT 0,
	flag INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	results CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	grupnr INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	int4 INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX akt_line_aktnr_ix ON akt_line (aktnr);
CREATE INDEX akt_line_date_ix ON akt_line (datum);
CREATE INDEX akt_line_linenr_ix ON akt_line (linenr);
CREATE INDEX akt_line_usrdate_ix ON akt_line (datum,userinit COLLATE case_insensitive);
CREATE TABLE akthdr (
	aktnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	kontakt_nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	t_betrag DECIMAL DEFAULT 0,
	prioritaet INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	chg_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chg_datum DATE,
	next_datum DATE,
	next_zeit INT DEFAULT 0,
	stichwort CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	erledigt BOOLEAN DEFAULT False,
	erl_datum DATE,
	flag INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	stufe INT DEFAULT 0,
	prozent INT DEFAULT 0,
	amount DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	product INT[4] DEFAULT ARRAY[0,0,0,0],
	referred INT DEFAULT 0,
	grund INT DEFAULT 0,
	mitbewerber INT[3] DEFAULT ARRAY[0,0,0],
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX akthdr_aktnr_ix ON akthdr (aktnr,flag);
CREATE INDEX akthdr_datum_ix ON akthdr (userinit COLLATE case_insensitive,chg_id COLLATE case_insensitive,flag);
CREATE INDEX akthdr_flag_ix ON akthdr (erledigt,flag);
CREATE INDEX akthdr_gastnr_ix ON akthdr (gastnr,erledigt,flag);
CREATE INDEX akthdr_init_ix ON akthdr (userinit COLLATE case_insensitive,erledigt,flag);
CREATE INDEX akthdr_kont_ix ON akthdr (gastnr,kontakt_nr,flag);
CREATE INDEX akthdr_next_ix ON akthdr (userinit COLLATE case_insensitive,next_datum,flag);
CREATE TABLE aktion (
	gastnr INT DEFAULT 0,
	aktionscode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bediener_nr INT DEFAULT 0,
	aktion_datum DATE,
	modif_datum DATE,
	wiederv_datum DATE,
	erledigt BOOLEAN DEFAULT False,
	kontakt_nr INT DEFAULT 0,
	briefnr INT DEFAULT 0,
	erled_datum DATE,
	user_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	texte CHARACTER VARYING [19] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','',''],
	lfd_nr INT DEFAULT 0,
	rec_status INT DEFAULT 0,
	rec_status_user CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betrag DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	aktion_zeit INT DEFAULT 0,
	erled_zeit INT DEFAULT 0,
	modif_zeit INT DEFAULT 0,
	wiederv_zeit INT DEFAULT 0,
	wertigkeit INT DEFAULT 0,
	dauer INT DEFAULT 0,
	potential DECIMAL DEFAULT 0,
	abschlussdatum DATE,
	abschluss_zeit INT DEFAULT 0,
	aufg_beginn_datum DATE,
	aufg_beginn_zeit INT DEFAULT 0,
	aufg_faellig_datum DATE,
	aufg_faellig_zeit INT DEFAULT 0,
	prioritat INT DEFAULT 0,
	a_status INT DEFAULT 0,
	beurteilung INT DEFAULT 0,
	mitbewerber INT DEFAULT 0,
	anz_entscheider INT DEFAULT 0,
	potential_typ CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX aktion_aktion_ix ON aktion (gastnr,aktion_datum,aktion_zeit,betriebsnr);
CREATE INDEX aktion_potential_ix ON aktion (user_code COLLATE case_insensitive,potential_typ COLLATE case_insensitive);
CREATE INDEX aktion_status_ix ON aktion (rec_status,aktion_datum);
CREATE INDEX aktion_wiederv_ix ON aktion (wiederv_datum);
CREATE TABLE ap_journal (
	lief_nr INT DEFAULT 0,
	rgdatum DATE,
	rechnr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lscheinnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	netto DECIMAL DEFAULT 0,
	zahlkonto INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX ap_journal_docu_nr ON ap_journal (docu_nr COLLATE case_insensitive,lscheinnr COLLATE case_insensitive);
CREATE INDEX ap_journal_id_ix ON ap_journal (userinit COLLATE case_insensitive);
CREATE INDEX ap_journal_lief_ix ON ap_journal (lief_nr);
CREATE INDEX ap_journal_liefdoc_ix ON ap_journal (lief_nr,docu_nr COLLATE case_insensitive,lscheinnr COLLATE case_insensitive);
CREATE INDEX ap_journal_sdate_ix ON ap_journal (sysdate);
CREATE INDEX ap_journal_userdate_ix ON ap_journal (userinit COLLATE case_insensitive,sysdate);
CREATE TABLE apt_bill (
	rechnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	periode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	e_pkwh DECIMAL DEFAULT 0,
	e_begin DECIMAL DEFAULT 0,
	e_ende DECIMAL DEFAULT 0,
	e_ppju DECIMAL DEFAULT 0,
	e_miete DECIMAL DEFAULT 0,
	e_admin DECIMAL DEFAULT 0,
	w_pm3 DECIMAL DEFAULT 0,
	w_begin DECIMAL DEFAULT 0,
	w_ende DECIMAL DEFAULT 0,
	w_miete DECIMAL DEFAULT 0,
	wartung_betrag DECIMAL DEFAULT 0,
	service_betrag DECIMAL DEFAULT 0,
	total_betrag DECIMAL DEFAULT 0,
	res_deci DECIMAL[3] DEFAULT ARRAY[0,0,0],
	res_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created DATE,
	zeit INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX apt_bill_period_ix ON apt_bill (periode COLLATE case_insensitive);
CREATE INDEX apt_bill_period_zinr_ix ON apt_bill (periode COLLATE case_insensitive,zinr COLLATE case_insensitive,rechnr COLLATE case_insensitive);
CREATE INDEX apt_bill_rechnr_ix ON apt_bill (rechnr COLLATE case_insensitive);
CREATE INDEX apt_bill_zinr_ix ON apt_bill (zinr COLLATE case_insensitive);
CREATE TABLE archieve (
	key CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	datum DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX archieve_key_ix ON archieve (key COLLATE case_insensitive);
CREATE INDEX archieve_keydat_ix ON archieve (key COLLATE case_insensitive,datum);
CREATE INDEX archieve_keynum12_ix ON archieve (key COLLATE case_insensitive,num1,num2);
CREATE INDEX archieve_keynum3_ix ON archieve (key COLLATE case_insensitive,num3);
CREATE INDEX archieve_keynum_ix ON archieve (key COLLATE case_insensitive,num1);
CREATE TABLE argt_line (
	argtnr INT DEFAULT 0,
	erwachs BOOLEAN DEFAULT False,
	kind1 BOOLEAN DEFAULT False,
	kind2 BOOLEAN DEFAULT False,
	gratis BOOLEAN DEFAULT True,
	vt_percnt DECIMAL DEFAULT 0.00,
	betrag DECIMAL DEFAULT 0,
	argt_artnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	fakt_modus INT DEFAULT 1,
	intervall INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX argt_line_arno_index ON argt_line (argtnr);
CREATE TABLE argtcost (
	datum DATE,
	gastnrmember INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	artnrfront INT DEFAULT 0,
	artnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	costbetrag DECIMAL DEFAULT 0,
	nettobetrag DECIMAL DEFAULT 0,
	mealcoupon INT DEFAULT 0,
	shift INT DEFAULT 0,
	res_deci DECIMAL[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	res_int INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	res_logic BOOLEAN[9] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false],
	res_char CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	res_date DATE[9] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	_recid serial PRIMARY KEY
);
CREATE INDEX argtcost_artdat1_ix ON argtcost (datum,artnr,departement,mealcoupon,shift);
CREATE INDEX argtcost_artdat_ix ON argtcost (datum,artnr,departement);
CREATE INDEX argtcost_artnrFront1_ix ON argtcost (datum,artnrfront,departement,mealcoupon,shift);
CREATE INDEX argtcost_artnrFront_ix ON argtcost (datum,artnrfront,departement);
CREATE INDEX argtcost_dat_ix ON argtcost (datum);
CREATE INDEX argtcost_gastnrmember_ix ON argtcost (datum,gastnrmember,zinr COLLATE case_insensitive,artnr,departement,mealcoupon,shift);
CREATE TABLE argtstat (
	datum DATE,
	argtnr INT DEFAULT 0,
	AIflag BOOLEAN DEFAULT False,
	gastnrmember INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	artnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	netto DECIMAL DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	res_deci DECIMAL[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	res_int INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	res_logic BOOLEAN[9] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false],
	res_char CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	res_date DATE[9] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	_recid serial PRIMARY KEY
);
CREATE INDEX argtstat_AI_ix ON argtstat (AIflag);
CREATE INDEX argtstat_AIdat_ix ON argtstat (datum);
CREATE INDEX argtstat_argt_ix ON argtstat (argtnr);
CREATE INDEX argtstat_argtdat_ix ON argtstat (datum,argtnr);
CREATE INDEX argtstat_artnr_ix ON argtstat (artnr,departement);
CREATE INDEX argtstat_datart_ix ON argtstat (datum,artnr,departement);
CREATE INDEX argtstat_datum_ix ON argtstat (datum);
CREATE INDEX argtstat_gastnrmember_ix ON argtstat (datum,gastnrmember,zinr COLLATE case_insensitive,artnr,departement);
CREATE TABLE arrangement (
	argtnr INT DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	argt_bez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	argt_rgbez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	artnr_logis INT DEFAULT 0,
	fakt_modus INT DEFAULT 1,
	intervall INT DEFAULT 0,
	ventil BOOLEAN DEFAULT False,
	zuordnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fixpreisargt BOOLEAN DEFAULT False,
	argt_preis DECIMAL DEFAULT 0,
	logis_proz DECIMAL DEFAULT 0,
	logis_preis DECIMAL DEFAULT 0,
	mwstsplit BOOLEAN DEFAULT False,
	argt_artikelnr INT DEFAULT 0,
	arrangement_art INT DEFAULT 0,
	waeschewechsel INT DEFAULT 0,
	handtuch INT DEFAULT 0,
	argt_typ INT DEFAULT 0,
	weeksplit BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	options CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	argt_rgbez2 CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	_recid serial PRIMARY KEY
);
CREATE INDEX arrangement_argt_index ON arrangement (arrangement COLLATE case_insensitive);
CREATE INDEX arrangement_arno_index ON arrangement (argtnr);
CREATE INDEX arrangement_typ_argt_ix ON arrangement (argt_typ,arrangement COLLATE case_insensitive);
CREATE TABLE artikel (
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zwkum INT DEFAULT 0,
	endkum INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	artart INT DEFAULT 0,
	autosaldo BOOLEAN DEFAULT False,
	kassarapport BOOLEAN DEFAULT False,
	bezaendern BOOLEAN DEFAULT False,
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mwst_code INT DEFAULT 0,
	service_code INT DEFAULT 0,
	umsatzart INT DEFAULT 0,
	bezeich1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	aposit INT DEFAULT 0,
	anzpunkte DECIMAL DEFAULT 0,
	artgrp INT DEFAULT 0,
	position CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reservieren BOOLEAN DEFAULT False,
	blockcheck BOOLEAN DEFAULT False,
	resart BOOLEAN DEFAULT False,
	masseurres BOOLEAN DEFAULT False,
	autofakt BOOLEAN DEFAULT False,
	preistabelle BOOLEAN DEFAULT False,
	anwdauer INT DEFAULT 0,
	ruhedauer INT DEFAULT 0,
	reinigung INT DEFAULT 0,
	anwtage INT[7] DEFAULT ARRAY[0,0,0,0,0,0,0],
	anwkab INT[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	anwpreis DECIMAL[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	frontbuchung BOOLEAN DEFAULT False,
	prozent DECIMAL DEFAULT 0,
	anzahl INT DEFAULT 0,
	mansteuer BOOLEAN DEFAULT False,
	prov_code INT DEFAULT 0,
	eigentuemer BOOLEAN DEFAULT False,
	activeflag BOOLEAN DEFAULT False,
	mwst_incl BOOLEAN DEFAULT False,
	serv_incl BOOLEAN DEFAULT False,
	quittung BOOLEAN DEFAULT False,
	abbuchung INT DEFAULT 0,
	artnrlager INT DEFAULT 0,
	lagernr INT DEFAULT 0,
	booktyp INT DEFAULT 0,
	pricetab BOOLEAN DEFAULT False,
	comment BOOLEAN DEFAULT False,
	kassabuch BOOLEAN DEFAULT False,
	e_gueltig DATE,
	s_gueltig DATE,
	rg_position BOOLEAN DEFAULT False,
	abrart INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	artnrrezept INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX artikel_art_index ON artikel (artnr);
CREATE INDEX artikel_artart_ix ON artikel (departement,artart);
CREATE INDEX artikel_artbez_index ON artikel (bezeich COLLATE case_insensitive);
CREATE INDEX artikel_artnrlg_ix ON artikel (artnrlager);
CREATE INDEX artikel_betr_depart_ix ON artikel (betriebsnr,departement,artnr);
CREATE INDEX artikel_depart_index ON artikel (departement,artnr);
CREATE TABLE artprice (
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	epreis DECIMAL DEFAULT 0,
	start_time INT DEFAULT 0,
	end_time INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX artprice_artprice_ix ON artprice (artnr,departement,start_time,end_time);
CREATE INDEX artprice_price_betr_ix ON artprice (betriebsnr,departement,artnr,start_time,end_time);
CREATE TABLE b_history (
	Anlass CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Rechnungsanschrift CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	Datum DATE,
	Uhrzeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Wochentag CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Personen INT DEFAULT 0,
	Bestellt__durch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Kontaktperson CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Telefax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Raeume CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Zweck CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Uhrzeiten CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Personen2 CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Tischform CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Raummiete CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Dekoration CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Ape__getraenke CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	ape__speisen CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Weine CHARACTER VARYING [20] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','','',''],
	Menue CHARACTER VARYING [20] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','','',''],
	Digestif CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Kaffee CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Nachtverpflegung CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	ndessen CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	sonst__bewirt CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Fotograf CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Musik CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Technik CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Kartentext CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Nachtzuschlag CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Hotelzimmer CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Tischplan CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Tischordnung CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Nadkarte CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Sonstiges CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	adurch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vgeschrieben CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vkontrolliert CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Gaestebuch CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Preismenu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	auf__datum DATE,
	Tischreden CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Menuekarten CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Geschenk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Deko2 CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Va_Ablauf CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Garderobe CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	VIP CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Service CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	GEMA CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Kuenstler CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	veran_nr INT DEFAULT 0,
	veran_seite INT DEFAULT 0,
	resnr INT[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	artikel_zg1 BOOLEAN[8] DEFAULT ARRAY[false,false,false,false,false,false,false,false],
	artikel_glob BOOLEAN DEFAULT False,
	rpreis DECIMAL[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	rpersonen INT[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	artikel_zg2 BOOLEAN[8] DEFAULT ARRAY[false,false,false,false,false,false,false,false],
	artikel_zg3 BOOLEAN[8] DEFAULT ARRAY[false,false,false,false,false,false,false,false],
	Veranstalteranschrift CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	v_Kontaktperson CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	v_Telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	v_Telefax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resstatus INT DEFAULT 0,
	Bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	raumbezeichnung CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	r_resstatus INT[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	c_resstatus CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	bis_datum DATE,
	bediener_nr INT DEFAULT 0,
	arrival CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	dinner CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	f_no CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	f_menu CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	Hotel_yes CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	hotel_no CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	abreise CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	price CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Dance CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	deposit DECIMAL DEFAULT 0,
	deposit_payment DECIMAL[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	payment_date DATE[9] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	total_paid DECIMAL DEFAULT 0,
	payment_userinit CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	limit_date DATE,
	last_paid_date DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX b_history_resnr_ix ON b_history (veran_nr,veran_seite);
CREATE TABLE b_oorder (
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	gespende DATE,
	gespgrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gespstart DATE,
	bis_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	von_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX b_oorder_artikel_index ON b_oorder (departement,artnr,gespstart);
CREATE INDEX b_oorder_raum_index ON b_oorder (raum COLLATE case_insensitive,gespstart);
CREATE TABLE b_storno (
	bankettnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	breslinnr INT DEFAULT 0,
	datum DATE,
	grund CHARACTER VARYING [18] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','',''],
	usercode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bediener_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX b_storno_bankettnr_index ON b_storno (bankettnr,breslinnr,datum);
CREATE TABLE ba_rset (
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	setup_id INT DEFAULT 0,
	personen INT DEFAULT 0,
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX ba_rset_raumsetup_ix ON ba_rset (raum COLLATE case_insensitive,setup_id);
CREATE TABLE ba_setup (
	setup_id INT DEFAULT 0,
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX ba_setup_setup_ix ON ba_setup (setup_id);
CREATE TABLE ba_typ (
	typ_id INT DEFAULT 0,
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX ba_typ_bankettyp_ix ON ba_typ (typ_id);
CREATE TABLE bankrep (
	Verteiler BOOLEAN[10] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false,false],
	Anlass CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Rechnungsanschrift CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	Datum DATE,
	Uhrzeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Wochentag CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Personen INT DEFAULT 0,
	Bestellt__durch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Kontaktperson CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Telefax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Raeume CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Zweck CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Uhrzeiten CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Personen2 CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Tischform CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Raummiete CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Dekoration CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Ape__getraenke CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	ape__speisen CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	Weine CHARACTER VARYING [17] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','',''],
	Menue CHARACTER VARYING [17] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','',''],
	Digestif CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Kaffee CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Nachtverpflegung CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	ndessen CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	sonst__bewirt CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Fotograf CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Musik CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Technik CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Kartentext CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	Nachtzuschlag CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Hotelzimmer CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Tischplan CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Tischordnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Nadkarte CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Sonstiges CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	adurch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	art BOOLEAN[3] DEFAULT ARRAY[false,false,false],
	vgeschrieben CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vkontrolliert CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Gaestebuch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Preismenu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	auf__datum DATE,
	Tischreden CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	Menuekarten CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	bankettnr INT DEFAULT 0,
	seite INT DEFAULT 0,
	Geschenk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bankrep_Pk ON bankrep (bankettnr,seite);
CREATE TABLE bankres (
	bankettnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	gastnrres INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	resdat DATE,
	anlass CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	useridanlage CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	useridmutat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kontaktdat DATE,
	kontaktfirst DATE,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	stoerung BOOLEAN DEFAULT False,
	notizen CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	activeflag INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	tafel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kontnr_ver INT DEFAULT 0,
	Bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Kontnr_res INT DEFAULT 0,
	Durchgehend BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	betrieb_gastres INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bankres_bankresnr_ix ON bankres (bankettnr);
CREATE INDEX bankres_gastnr_ix ON bankres (activeflag,gastnr,bankettnr);
CREATE TABLE bediener (
	nr INT DEFAULT 0,
	usercode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	username CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	user_group INT DEFAULT 0,
	permissions CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	kassenbest DECIMAL DEFAULT 0,
	flag INT DEFAULT 0,
	mapi_profile CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mapi_password CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX bediener_active_ix ON bediener (flag,usercode COLLATE case_insensitive);
CREATE INDEX bediener_betr_code_ix ON bediener (betriebsnr,usercode COLLATE case_insensitive);
CREATE INDEX bediener_betr_nr_ix ON bediener (betriebsnr,nr);
CREATE INDEX bediener_code_ix ON bediener (usercode COLLATE case_insensitive);
CREATE INDEX bediener_name_ix ON bediener (username COLLATE case_insensitive);
CREATE INDEX bediener_nr_ix ON bediener (nr);
CREATE TABLE bill (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	flag INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	logisumsatz DECIMAL DEFAULT 0,
	arrangemdat DATE,
	rgdruck INT DEFAULT 0,
	logiernachte INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	argtumsatz DECIMAL DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	billnr INT DEFAULT 1,
	firstper BOOLEAN DEFAULT True,
	billkur BOOLEAN DEFAULT False,
	logidat DATE,
	bilname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	teleinheit INT DEFAULT 0,
	telsumme DECIMAL DEFAULT 0,
	segmentcode INT DEFAULT 0,
	printnr INT DEFAULT 0,
	billbankett BOOLEAN DEFAULT False,
	service DECIMAL[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	mwst DECIMAL[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	umleit_zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	billmaster BOOLEAN DEFAULT False,
	datum DATE,
	taxsumme DECIMAL DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	billtyp INT DEFAULT 0,
	parent_nr INT DEFAULT 0,
	restargt DECIMAL DEFAULT 0,
	init_argt DECIMAL DEFAULT 0,
	rest_tage INT DEFAULT 0,
	ums_kurz DECIMAL DEFAULT 0,
	ums_lang DECIMAL DEFAULT 0,
	nextargt_bookdate DATE,
	roomcharge BOOLEAN DEFAULT False,
	oldzinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	t_rechnr INT DEFAULT 0,
	rechnr2 INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	vesrdep DECIMAL DEFAULT 0,
	vesrdat DATE,
	vesrdepot CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vesrdepot2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vesrcod CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	verstat INT DEFAULT 0,
	kontakt_nr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	billref INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bill_bet_res_ix ON bill (betriebsnr,resnr);
CREATE INDEX bill_bill_rechnr2_ix ON bill (rechnr2);
CREATE INDEX bill_billnr_index ON bill (zinr COLLATE case_insensitive,gastnr,billnr);
CREATE INDEX bill_billref_ix ON bill (betriebsnr,billref);
CREATE INDEX bill_flagdat_ix ON bill (flag,datum);
CREATE INDEX bill_flrech_index ON bill (flag,billtyp,rechnr,name COLLATE case_insensitive,gastnr,billnr);
CREATE INDEX bill_flzinr_ix ON bill (flag,billtyp,zinr COLLATE case_insensitive,name COLLATE case_insensitive,gastnr,billnr,rechnr);
CREATE INDEX bill_gastnr_index ON bill (gastnr);
CREATE INDEX bill_rechnr_index ON bill (rechnr);
CREATE INDEX bill_reserv_index ON bill (resnr,reslinnr);
CREATE INDEX bill_resrec_index ON bill (flag,resnr,billnr,reslinnr);
CREATE INDEX bill_t_rechnr_ix ON bill (flag,t_rechnr);
CREATE INDEX bill_type_index ON bill (flag,billtyp,name COLLATE case_insensitive,gastnr,billnr,rechnr);
CREATE INDEX bill_vers3_ix ON bill (vesrdepot2 COLLATE case_insensitive);
CREATE INDEX bill_vesr1_ix ON bill (vesrcod COLLATE case_insensitive,vesrdepot COLLATE case_insensitive,vesrdepot2 COLLATE case_insensitive);
CREATE INDEX bill_vesr2_ix ON bill (vesrdepot COLLATE case_insensitive);
CREATE INDEX bill_zinrfl_index ON bill (zinr COLLATE case_insensitive,flag);
CREATE TABLE bill_lin_tax (
	betriebsnr INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	billin_nr INT DEFAULT 0,
	steuercode INT DEFAULT 0,
	stererpct DECIMAL DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	steuer_betrag DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bill_lin_tax_rechnr_linnr_ix ON bill_lin_tax (betriebsnr,rechnr,billin_nr,steuercode);
CREATE TABLE bill_line (
	rechnr INT DEFAULT 0,
	bill_datum DATE,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	steuercode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fremdwbetrag DECIMAL DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zeit INT DEFAULT 0,
	waehrungsnr INT DEFAULT 0,
	sysdate DATE,
	departement INT DEFAULT 0,
	prtflag INT DEFAULT 0,
	printflag INT DEFAULT 0,
	nettobetrag DECIMAL DEFAULT 0,
	typ INT DEFAULT 0,
	massnr INT DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mwstsplit BOOLEAN DEFAULT False,
	gastnr INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	orts_tax DECIMAL DEFAULT 0,
	origin_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	billin_nr INT DEFAULT 0,
	tax_booked BOOLEAN DEFAULT False,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bill_line_artnr_ix ON bill_line (rechnr,artnr,sysdate,zeit);
CREATE INDEX bill_line_bet_rech_ix ON bill_line (betriebsnr,rechnr,billin_nr);
CREATE INDEX bill_line_bildat_index ON bill_line (rechnr,bill_datum,zeit);
CREATE INDEX bill_line_billinnr_ix ON bill_line (bediener_nr,rechnr,billin_nr);
CREATE INDEX bill_line_dep_art_dat_ix ON bill_line (bediener_nr,departement,artnr,bill_datum);
CREATE INDEX bill_line_rechnr_index ON bill_line (rechnr,sysdate,zeit);
CREATE INDEX bill_line_zinr_index ON bill_line (rechnr,zinr COLLATE case_insensitive,sysdate,zeit);
CREATE TABLE billhis (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rechnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	reslinnr INT DEFAULT 1,
	billnr INT DEFAULT 1,
	mwst DECIMAL[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	datum DATE,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	parent_nr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX billhis_gastnr_ix ON billhis (gastnr);
CREATE INDEX billhis_rechnr_ix ON billhis (rechnr);
CREATE INDEX billhis_res_reslin_ix ON billhis (resnr,reslinnr);
CREATE INDEX billhis_zinr_gastnr_ix ON billhis (zinr COLLATE case_insensitive,gastnr);
CREATE INDEX billhis_zinr_ix ON billhis (zinr COLLATE case_insensitive);
CREATE TABLE billjournal (
	rechnr INT DEFAULT 0,
	bill_datum DATE,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	steuercode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	zeit INT DEFAULT 0,
	kassarapport BOOLEAN DEFAULT False,
	waehrungcode INT DEFAULT 0,
	stornogrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bediener_nr INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	waehrungsnr INT DEFAULT 0,
	wabkurz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ankauf DECIMAL DEFAULT 0,
	verkauf DECIMAL DEFAULT 0,
	fremdwaehrng DECIMAL DEFAULT 0,
	sysdate DATE,
	kassabuch BOOLEAN DEFAULT False,
	comment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	subtime INT DEFAULT 0,
	nachbuchen BOOLEAN DEFAULT False,
	kassabuch_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	card_details CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	billin_nr INT DEFAULT 0,
	steuer_percent DECIMAL DEFAULT 0,
	service_code INT DEFAULT 0,
	service_percent DECIMAL DEFAULT 0,
	billjou_ref INT DEFAULT 0,
	billtype INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX billjournal_artdate_ix ON billjournal (departement,artnr,bill_datum,zeit,subtime);
CREATE INDEX billjournal_billjref_ix ON billjournal (betriebsnr,rechnr,billjou_ref);
CREATE INDEX billjournal_chrono_index ON billjournal (bill_datum,departement,sysdate,zeit,subtime);
CREATE INDEX billjournal_dateart_ix ON billjournal (bill_datum,artnr,zeit,subtime);
CREATE INDEX billjournal_dateid_ix ON billjournal (bill_datum,bediener_nr,zeit,subtime);
CREATE INDEX billjournal_depdate_ix ON billjournal (departement,bill_datum,zeit,subtime);
CREATE INDEX billjournal_iddate_ix ON billjournal (bediener_nr,bill_datum,zeit,subtime);
CREATE INDEX billjournal_kassenbuch_ix ON billjournal (kassabuch,bill_datum);
CREATE INDEX billjournal_nachbuch_ix ON billjournal (nachbuchen);
CREATE INDEX billjournal_wahnr_index ON billjournal (bill_datum,waehrungsnr);
CREATE INDEX billjournal_zinrdat_ix ON billjournal (zinr COLLATE case_insensitive,bill_datum,zeit,subtime);
CREATE TABLE bk_beleg (
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	veran_nr INT[48] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	veran_resnr INT[48] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	resstatus INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	resart CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_beleg_bk_beleg_ix ON bk_beleg (raum COLLATE case_insensitive,datum,resstatus);
CREATE TABLE bk_fsdef (
	fsname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fs_field_name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fs_field_length INT DEFAULT 0,
	fs_field_active BOOLEAN DEFAULT False,
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_fsdef_prim_ix ON bk_fsdef (fsname COLLATE case_insensitive,fs_field_name COLLATE case_insensitive);
CREATE TABLE bk_func (
	Anlass CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Rechnungsanschrift CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	Datum DATE,
	Uhrzeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Wochentag CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Personen INT DEFAULT 0,
	Bestellt__durch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Kontaktperson CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	Telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Telefax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Raeume CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Zweck CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Uhrzeiten CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Personen2 CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Tischform CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Raummiete CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Dekoration CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	Ape__getraenke CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	ape__speisen CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Weine CHARACTER VARYING [20] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','','',''],
	Menue CHARACTER VARYING [20] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','','',''],
	Digestif CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Kaffee CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Nachtverpflegung CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	ndessen CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	sonst__bewirt CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Fotograf CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Musik CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Technik CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Kartentext CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Nachtzuschlag CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Hotelzimmer CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Tischplan CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Tischordnung CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Nadkarte CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Sonstiges CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	adurch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vgeschrieben CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vkontrolliert CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Gaestebuch CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Preismenu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	auf__datum DATE,
	Tischreden CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Menuekarten CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Geschenk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Deko2 CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Va_Ablauf CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Garderobe CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	VIP CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	Service CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	GEMA CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Kuenstler CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	veran_nr INT DEFAULT 0,
	veran_seite INT DEFAULT 0,
	resnr INT[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	artikel_zg1 BOOLEAN[8] DEFAULT ARRAY[false,false,false,false,false,false,false,false],
	artikel_glob BOOLEAN DEFAULT False,
	rpreis DECIMAL[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	rpersonen INT[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	artikel_zg2 BOOLEAN[8] DEFAULT ARRAY[false,false,false,false,false,false,false,false],
	artikel_zg3 BOOLEAN[8] DEFAULT ARRAY[false,false,false,false,false,false,false,false],
	Veranstalteranschrift CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	v_Kontaktperson CHARACTER VARYING [2] COLLATE case_insensitive DEFAULT ARRAY['',''],
	v_Telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	v_Telefax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resstatus INT DEFAULT 0,
	Bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	raumbezeichnung CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	r_resstatus INT[8] DEFAULT ARRAY[0,0,0,0,0,0,0,0],
	c_resstatus CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	bis_datum DATE,
	bediener_nr INT DEFAULT 0,
	arrival CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	dinner CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	f_no CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	f_menu CHARACTER VARYING [4] COLLATE case_insensitive DEFAULT ARRAY['','','',''],
	Hotel_yes CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	hotel_no CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	abreise CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	price CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Dance CHARACTER VARYING [8] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','',''],
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_func_datum_ix ON bk_func (Datum);
CREATE INDEX bk_func_vernr_ix ON bk_func (veran_nr);
CREATE INDEX bk_func_vernr_pg_ix ON bk_func (veran_nr,veran_seite);
CREATE TABLE bk_package (
	veran_nr INT DEFAULT 0,
	veran_resnr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	bis_datum DATE,
	bis_i INT DEFAULT 0,
	bis_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Datum DATE,
	departement INT DEFAULT 0,
	fakturiert INT DEFAULT 0,
	notizen CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	personen INT DEFAULT 0,
	preis DECIMAL DEFAULT 0,
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	von_i INT DEFAULT 0,
	von_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	artnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betrag DECIMAL DEFAULT 0,
	gastnrver INT DEFAULT 0,
	arrangemdat DATE,
	anzahl INT DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	deci1 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	number1 INT DEFAULT 0,
	raum_bez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betrieb_gastver INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_package_art_ix ON bk_package (Datum,departement,artnr,von_i);
CREATE INDEX bk_package_dat_zeit_ix ON bk_package (Datum,von_i);
CREATE INDEX bk_package_gastnrver_ix ON bk_package (gastnrver,veran_nr,Datum,von_i);
CREATE INDEX bk_package_verannr_ix ON bk_package (veran_nr,veran_resnr);
CREATE TABLE bk_pause (
	von_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bis_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	veran_nr INT DEFAULT 0,
	veran_seite INT DEFAULT 0,
	veran_resnr INT DEFAULT 0,
	von_i INT DEFAULT 0,
	bis_i INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	p_nr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	Datum DATE,
	bis_datum DATE,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE TABLE bk_rart (
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	setup CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	preis DECIMAL DEFAULT 0,
	Bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	veran_typ INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	veran_artnr INT DEFAULT 0,
	zwkum INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	setup_id INT DEFAULT 0,
	veran_nr INT DEFAULT 0,
	von_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	veran_seite INT DEFAULT 0,
	veran_resnr INT DEFAULT 0,
	buchstatus BOOLEAN DEFAULT False,
	departement INT DEFAULT 0,
	fakturiert INT DEFAULT 0,
	resstatus INT DEFAULT 0,
	anzeigen BOOLEAN DEFAULT True,
	segmentcode INT DEFAULT 0,
	Standardequipment BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_rart_nr_artnr_ix ON bk_rart (veran_nr,veran_seite,veran_artnr);
CREATE INDEX bk_rart_nr_pg_ug_ix ON bk_rart (veran_nr,veran_seite,zwkum);
CREATE TABLE bk_raum (
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	groesse INT DEFAULT 0,
	Preis DECIMAL DEFAULT 0,
	nebenstelle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	personen INT DEFAULT 0,
	vorbereit INT DEFAULT 0,
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lu_raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Reihenfolge INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	nachlauf INT DEFAULT 0,
	bname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_raum_bez_ix ON bk_raum (bezeich COLLATE case_insensitive);
CREATE INDEX bk_raum_qm_ix ON bk_raum (groesse,bezeich COLLATE case_insensitive);
CREATE INDEX bk_raum_raum_ix ON bk_raum (raum COLLATE case_insensitive);
CREATE INDEX bk_raum_reihenfolge_ix ON bk_raum (Reihenfolge);
CREATE TABLE bk_reser (
	von_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bis_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	typ CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	personen INT DEFAULT 0,
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	setup CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	preis DECIMAL DEFAULT 0,
	notizen CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	limitdate DATE,
	fakturiert INT DEFAULT 0,
	briefnr INT DEFAULT 0,
	fname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resstatus INT DEFAULT 0,
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	veran_nr INT DEFAULT 0,
	veran_seite INT DEFAULT 0,
	veran_resnr INT DEFAULT 0,
	Datum DATE,
	veran_typ INT DEFAULT 0,
	setup_id INT DEFAULT 0,
	von_i INT DEFAULT 0,
	bis_i INT DEFAULT 0,
	art_res BOOLEAN DEFAULT False,
	veran_artnr INT DEFAULT 0,
	Gruppenname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Dekoration CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bis_datum DATE,
	bediener_nr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	Vorbereitungszeit INT DEFAULT 0,
	Nachlaufzeit INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_reser_datumzeit_ix ON bk_reser (veran_nr,Datum,von_zeit COLLATE case_insensitive);
CREATE INDEX bk_reser_raumdat_ix ON bk_reser (raum COLLATE case_insensitive,Datum);
CREATE INDEX bk_reser_veran_nr_ix ON bk_reser (veran_nr,veran_resnr);
CREATE INDEX bk_reser_vernr_ix ON bk_reser (veran_nr);
CREATE INDEX bk_reser_vernr_pg_ix ON bk_reser (veran_nr,veran_seite);
CREATE INDEX bk_reser_vernr_pg_rs_ix ON bk_reser (veran_nr,veran_seite,veran_resnr);
CREATE INDEX bk_reser_zeit_ix ON bk_reser (Datum,von_zeit COLLATE case_insensitive);
CREATE TABLE bk_rset (
	rset_nr INT DEFAULT 0,
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	setup_id INT DEFAULT 0,
	personen INT DEFAULT 0,
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	groesse INT DEFAULT 0,
	preis DECIMAL DEFAULT 0,
	nebenstelle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorbereit INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	nachlauf INT DEFAULT 0,
	bname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_rset_rset_nr_ix ON bk_rset (rset_nr);
CREATE TABLE bk_setup (
	setup_id INT DEFAULT 0,
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	vorbereit INT DEFAULT 0,
	nachlauf INT DEFAULT 0,
	bname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_setup_setup_ix ON bk_setup (setup_id);
CREATE TABLE bk_stat (
	room CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	isStatus INT DEFAULT 0,
	salesID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rm_rev DECIMAL DEFAULT 0,
	fb_rev DECIMAL DEFAULT 0,
	bev_rev DECIMAL DEFAULT 0,
	other_rev DECIMAL DEFAULT 0,
	resstatus INT DEFAULT 0,
	cancel_date DATE,
	pax INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_int INT DEFAULT 0,
	reserve_dec INT DEFAULT 0,
	event_nr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_stat_cancdate_ix ON bk_stat (isStatus,cancel_date);
CREATE INDEX bk_stat_datestat_ix ON bk_stat (datum,isStatus);
CREATE INDEX bk_stat_evdate_ix ON bk_stat (isStatus,datum,event_nr);
CREATE INDEX bk_stat_gast_ix ON bk_stat (gastnr,isStatus);
CREATE INDEX bk_stat_resnr_ix ON bk_stat (isStatus,resnr);
CREATE INDEX bk_stat_rmdat_ix ON bk_stat (room COLLATE case_insensitive,datum,isStatus);
CREATE INDEX bk_stat_rmdatrestat_ix ON bk_stat (room COLLATE case_insensitive,datum,resnr,reslinnr,isStatus);
CREATE INDEX bk_stat_salesdat_ix ON bk_stat (salesID COLLATE case_insensitive,datum,isStatus);
CREATE TABLE bk_veran (
	veran_nr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	gastnrver INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	resdat DATE,
	anlass CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	useridanlage CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	useridmutat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kontaktdat DATE,
	kontaktfirst DATE,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	stoerung BOOLEAN DEFAULT False,
	activeflag INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	Infotafel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kontnr_ver INT DEFAULT 0,
	Bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Kontnr_res INT DEFAULT 0,
	resstatus INT DEFAULT 0,
	resnr INT DEFAULT 0,
	Art INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	betrieb_gastver INT DEFAULT 0,
	deposit DECIMAL DEFAULT 0,
	deposit_payment DECIMAL[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	payment_date DATE[9] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	total_paid DECIMAL DEFAULT 0,
	payment_userinit CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	limit_date DATE,
	last_paid_date DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX bk_veran_gastnr_ix ON bk_veran (gastnr);
CREATE INDEX bk_veran_lastpaid_ix ON bk_veran (last_paid_date);
CREATE INDEX bk_veran_limitdate_ix ON bk_veran (limit_date);
CREATE INDEX bk_veran_veran_rechnr_ix ON bk_veran (rechnr);
CREATE INDEX bk_veran_vernr_ix ON bk_veran (veran_nr);
CREATE TABLE bl_dates (
	gespgrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gespstart DATE,
	gespende DATE,
	zikatnr INT DEFAULT 0,
	zimmeranz INT DEFAULT 1,
	user_group INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bl_dates_zikatdat_ix ON bl_dates (zikatnr,gespstart);
CREATE INDEX bl_dates_zikatnr_ix ON bl_dates (zikatnr);
CREATE TABLE blinehis (
	rechnr INT DEFAULT 0,
	bill_datum DATE,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fremdwbetrag DECIMAL DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zeit INT DEFAULT 0,
	waehrungsnr INT DEFAULT 0,
	sysdate DATE,
	departement INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX blinehis_art_dep_dat_ix ON blinehis (artnr,bill_datum,departement);
CREATE INDEX blinehis_rechnr_ix ON blinehis (rechnr);
CREATE TABLE bresline (
	bankettnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	breslinnr INT DEFAULT 0,
	datum DATE,
	von_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bis_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	buchstatus BOOLEAN DEFAULT False,
	typ CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	personen INT DEFAULT 0,
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	setup CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	artnr INT DEFAULT 0,
	preis DECIMAL DEFAULT 0,
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	notizen CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	texte CHARACTER VARYING [19] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','',''],
	zwkum INT DEFAULT 0,
	limitdate DATE,
	fakturiert INT DEFAULT 0,
	Information CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	briefnr INT DEFAULT 0,
	fname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	r_status INT DEFAULT 0,
	raum_line INT DEFAULT 0,
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	von_equipnr INT DEFAULT 0,
	zu_equipnr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX bresline_breslin2_ix ON bresline (bankettnr,breslinnr);
CREATE INDEX bresline_breslinnr_ix ON bresline (bankettnr);
CREATE INDEX bresline_datumzeit_ix ON bresline (bankettnr,datum,von_zeit COLLATE case_insensitive);
CREATE INDEX bresline_raumdat_ix ON bresline (raum COLLATE case_insensitive,datum,zwkum);
CREATE INDEX bresline_zeit_ix ON bresline (datum,von_zeit COLLATE case_insensitive);
CREATE TABLE brief (
	briefnr INT DEFAULT 0,
	briefkateg INT DEFAULT 1,
	briefbezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sprachcode INT DEFAULT 1,
	tabulator INT[30] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	fname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ftyp INT DEFAULT 0,
	etk_anzahl INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX brief_briefbez_ix ON brief (briefkateg,briefbezeich COLLATE case_insensitive);
CREATE INDEX brief_briefnr_ix ON brief (briefnr);
CREATE TABLE brieftmp (
	briefnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	copies INT DEFAULT 1,
	datum DATE,
	zeit INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	mahnbeginn INT DEFAULT 0,
	mahnende INT DEFAULT 0,
	kortyp INT DEFAULT 0,
	kontakt_nr INT DEFAULT 0,
	resart INT DEFAULT 1,
	refdatum DATE,
	millisek INT DEFAULT 0,
	flag INT DEFAULT 0,
	drucken BOOLEAN DEFAULT False,
	lfd__nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX brieftmp_brief_ix ON brieftmp (flag,briefnr);
CREATE INDEX brieftmp_chrono_ix ON brieftmp (flag,kortyp,datum,zeit,millisek);
CREATE INDEX brieftmp_gastnr_ix ON brieftmp (gastnr,flag,datum,zeit,millisek);
CREATE INDEX brieftmp_print_ix ON brieftmp (drucken,datum,zeit,millisek);
CREATE TABLE briefzei (
	briefnr INT DEFAULT 0,
	briefzeilnr INT DEFAULT 0,
	texte CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX briefzei_briefzei_ix ON briefzei (briefnr,briefzeilnr);
CREATE TABLE budget (
	artnr INT DEFAULT 0,
	datum DATE,
	betrag DECIMAL DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX budget_betr_budg_ix ON budget (betriebsnr,departement,artnr,datum);
CREATE INDEX budget_budget_ix ON budget (departement,artnr,datum);
CREATE TABLE calls (
	nebenstelle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	zeit INT DEFAULT 0,
	rufnummer CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	impulse INT DEFAULT 0,
	pabxbetrag DECIMAL DEFAULT 0,
	aufschlag DECIMAL DEFAULT 0,
	gastbetrag DECIMAL DEFAULT 0,
	dauer INT DEFAULT 0,
	leitung INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	buchflag INT DEFAULT 0,
	sequence INT DEFAULT 0,
	key INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	transdatum DATE,
	transzeit INT DEFAULT 0,
	satz_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX calls_buzinr_ix ON calls (buchflag,zinr COLLATE case_insensitive,datum,zeit);
CREATE INDEX calls_datum_ix ON calls (datum,zeit);
CREATE INDEX calls_key_book_date_ix ON calls (key,buchflag,datum,zeit);
CREATE INDEX calls_key_book_nebst_ix ON calls (key,buchflag,nebenstelle COLLATE case_insensitive,datum,zeit);
CREATE INDEX calls_key_book_zinr_ix ON calls (key,buchflag,zinr COLLATE case_insensitive,datum,zeit);
CREATE INDEX calls_key_date_ix ON calls (key,datum,zeit);
CREATE INDEX calls_key_nebst_ix ON calls (key,nebenstelle COLLATE case_insensitive,datum,zeit);
CREATE INDEX calls_nebenst_ix ON calls (nebenstelle COLLATE case_insensitive,datum,zeit);
CREATE INDEX calls_satz_ix ON calls (betriebsnr,satz_id COLLATE case_insensitive);
CREATE TABLE cl_bonus (
	key INT DEFAULT 0,
	datum DATE,
	datum1 DATE,
	datum2 DATE,
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	disc_proz DECIMAL DEFAULT 0,
	disc_days INT DEFAULT 0,
	disc_amt DECIMAL DEFAULT 0,
	memtype INT DEFAULT 0,
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zeit INT DEFAULT 0,
	nr INT DEFAULT 0,
	exp_date1 DATE,
	exp_date2 DATE,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	date3 DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_bonus_key_ix ON cl_bonus (key);
CREATE INDEX cl_bonus_keycodate_ix ON cl_bonus (key,codenum COLLATE case_insensitive,datum);
CREATE INDEX cl_bonus_keycode_ix ON cl_bonus (key,codenum COLLATE case_insensitive);
CREATE INDEX cl_bonus_keydat_ix ON cl_bonus (key,datum);
CREATE INDEX cl_bonus_keynr_ix ON cl_bonus (key,nr);
CREATE INDEX cl_bonus_keytype_ix ON cl_bonus (key,memtype);
CREATE TABLE cl_book (
	datum DATE,
	loc_nr INT DEFAULT 0,
	hour INT[48] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_book_locdate_ix ON cl_book (datum,loc_nr);
CREATE TABLE cl_checkin (
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	card_num CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	startime INT DEFAULT 0,
	endtime INT DEFAULT 0,
	activeflag BOOLEAN DEFAULT False,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	voucherno CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	rechnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_checkin_card_ix ON cl_checkin (card_num COLLATE case_insensitive);
CREATE INDEX cl_checkin_ccds_ix ON cl_checkin (codenum COLLATE case_insensitive,card_num COLLATE case_insensitive,datum,startime);
CREATE INDEX cl_checkin_code_ix ON cl_checkin (codenum COLLATE case_insensitive);
CREATE INDEX cl_checkin_date_ix ON cl_checkin (datum);
CREATE TABLE cl_class (
	nr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	location_nr INT DEFAULT 0,
	instructor INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	start_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000',
	end_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000',
	start_date DATE,
	end_date DATE,
	week_day BOOLEAN[7] DEFAULT ARRAY[false,false,false,false,false,false,false],
	capacity INT DEFAULT 0,
	activeflag BOOLEAN DEFAULT True,
	fee1 DECIMAL DEFAULT 0,
	fee2 DECIMAL DEFAULT 0,
	paymode INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_class_location_ix ON cl_class (location_nr);
CREATE INDEX cl_class_name_ix ON cl_class (name COLLATE case_insensitive);
CREATE INDEX cl_class_nr_ix ON cl_class (nr);
CREATE TABLE cl_enroll (
	nr INT DEFAULT 0,
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	enrolldate DATE,
	enrollflag BOOLEAN DEFAULT False,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_enroll_code_ix ON cl_enroll (codenum COLLATE case_insensitive);
CREATE INDEX cl_enroll_nr_ix ON cl_enroll (nr);
CREATE INDEX cl_enroll_nrcode_ix ON cl_enroll (nr,codenum COLLATE case_insensitive);
CREATE TABLE cl_free (
	itype INT DEFAULT 0,
	nr INT DEFAULT 0,
	from_date DATE,
	to_date DATE,
	from_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000',
	to_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '2400',
	offdays BOOLEAN[7] DEFAULT ARRAY[false,false,false,false,false,false,false],
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_free_nr_ix ON cl_free (itype,nr);
CREATE TABLE cl_histci (
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	starttime INT DEFAULT 0,
	endtime INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	card_num CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	voucherno CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_histci_code_ix ON cl_histci (codenum COLLATE case_insensitive);
CREATE INDEX cl_histci_codedate_ix ON cl_histci (codenum COLLATE case_insensitive,datum);
CREATE INDEX cl_histci_date_ix ON cl_histci (codenum COLLATE case_insensitive);
CREATE TABLE cl_histpay (
	key INT DEFAULT 0,
	datum DATE,
	datum1 DATE,
	datum2 DATE,
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gastnr INT DEFAULT 0,
	billgastnr INT DEFAULT 0,
	memtype INT DEFAULT 0,
	amount DECIMAL DEFAULT 0,
	paid DECIMAL DEFAULT 0,
	balance DECIMAL DEFAULT 0,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	rechnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_histpay_key_ix ON cl_histpay (key);
CREATE INDEX cl_histpay_keybill_ix ON cl_histpay (key,billgastnr);
CREATE INDEX cl_histpay_keycodat_ix ON cl_histpay (key,datum,codenum COLLATE case_insensitive);
CREATE INDEX cl_histpay_keycode_ix ON cl_histpay (key,codenum COLLATE case_insensitive);
CREATE INDEX cl_histpay_keydat_ix ON cl_histpay (key,datum);
CREATE INDEX cl_histpay_keydatyp_ix ON cl_histpay (key,datum,memtype);
CREATE INDEX cl_histpay_keygas_ix ON cl_histpay (key,gastnr);
CREATE INDEX cl_histpay_keyrechnr_ix ON cl_histpay (key,rechnr);
CREATE TABLE cl_histstatus (
	datum DATE,
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	memstatus INT DEFAULT 0,
	memtype1 INT DEFAULT 0,
	memtype2 INT DEFAULT 0,
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	user_init CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zeit INT DEFAULT 0,
	datum1 DATE,
	datum2 DATE,
	num1 INT DEFAULT 0,
	num2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	freeze_for INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_histstatus_code_ix ON cl_histstatus (codenum COLLATE case_insensitive);
CREATE INDEX cl_histstatus_datum_ix ON cl_histstatus (datum);
CREATE INDEX cl_histstatus_datype2_ix ON cl_histstatus (datum,memtype2);
CREATE INDEX cl_histstatus_idat_ix ON cl_histstatus (datum,user_init COLLATE case_insensitive);
CREATE INDEX cl_histstatus_statdate_ix ON cl_histstatus (datum,memstatus);
CREATE INDEX cl_histstatus_status_ix ON cl_histstatus (memstatus);
CREATE TABLE cl_histtrain (
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	starttime INT DEFAULT 0,
	endtime INT DEFAULT 0,
	class INT DEFAULT 0,
	trainer INT DEFAULT 0,
	remain INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	voucherno CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_histtrain_class_ix ON cl_histtrain (class,datum);
CREATE INDEX cl_histtrain_code_ix ON cl_histtrain (codenum COLLATE case_insensitive);
CREATE INDEX cl_histtrain_codedate_ix ON cl_histtrain (codenum COLLATE case_insensitive,datum);
CREATE INDEX cl_histtrain_date_ix ON cl_histtrain (datum);
CREATE TABLE cl_histvisit (
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	starttime INT DEFAULT 0,
	endtime INT DEFAULT 0,
	service INT DEFAULT 0,
	trainflag BOOLEAN DEFAULT False,
	rechnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_histvisit_code_ix ON cl_histvisit (codenum COLLATE case_insensitive);
CREATE INDEX cl_histvisit_codedate_ix ON cl_histvisit (codenum COLLATE case_insensitive,datum);
CREATE INDEX cl_histvisit_cosetr_ix ON cl_histvisit (codenum COLLATE case_insensitive,service,endtime,trainflag);
CREATE INDEX cl_histvisit_date_ix ON cl_histvisit (codenum COLLATE case_insensitive);
CREATE INDEX cl_histvisit_scdtime_ix ON cl_histvisit (codenum COLLATE case_insensitive,datum,service,endtime);
CREATE INDEX cl_histvisit_serv_ix ON cl_histvisit (datum,service);
CREATE INDEX cl_histvisit_tscdtime_ix ON cl_histvisit (codenum COLLATE case_insensitive,datum,endtime,service,trainflag);
CREATE TABLE cl_home (
	nr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zip CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	city CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	phone CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Fax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	email CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	banner CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	cflag BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_home_name_ix ON cl_home (name COLLATE case_insensitive);
CREATE INDEX cl_home_nr_ix ON cl_home (nr);
CREATE TABLE cl_location (
	nr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	from_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000',
	to_time CHARACTER VARYING COLLATE case_insensitive DEFAULT '2400',
	activeflag BOOLEAN DEFAULT False,
	parent INT DEFAULT 0,
	child_num INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_location_nr_ix ON cl_location (nr);
CREATE TABLE cl_locker (
	location INT DEFAULT 0,
	locknum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	from_date DATE,
	to_date DATE,
	from_time INT DEFAULT 0,
	to_time INT DEFAULT 0,
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	towel INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	towel_out INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	towel_in INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	card_num CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	valid_flag BOOLEAN DEFAULT True,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_locker_flaglock_ix ON cl_locker (locknum COLLATE case_insensitive,valid_flag);
CREATE INDEX cl_locker_locdate_ix ON cl_locker (location,from_date,to_date);
CREATE INDEX cl_locker_locmem_ix ON cl_locker (location,from_date,to_date,codenum COLLATE case_insensitive);
CREATE INDEX cl_locker_locnum_ix ON cl_locker (location,locknum COLLATE case_insensitive,from_date,to_date);
CREATE TABLE cl_log (
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	zeit INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	user_init CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_log_codate_ix ON cl_log (codenum COLLATE case_insensitive,datum);
CREATE INDEX cl_log_datum_ix ON cl_log (datum);
CREATE INDEX cl_log_usrdate_ix ON cl_log (user_init COLLATE case_insensitive,datum);
CREATE TABLE cl_member (
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	agreenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gastnr INT DEFAULT 0,
	emergency_nm CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	emergency_ph CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	membertype INT DEFAULT 0,
	homeclub INT DEFAULT 0,
	memstatus INT DEFAULT 0,
	group_nm CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	income DECIMAL DEFAULT 0,
	medicalnote CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	locker INT DEFAULT 0,
	lock_num CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lockerdate DATE,
	source INT DEFAULT 0,
	trainer INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	salesID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	join_date DATE,
	expired_date DATE,
	last_renewed DATE,
	main_gastnr INT DEFAULT 0,
	relation INT DEFAULT 0,
	paysched INT DEFAULT 0,
	numfreeze INT DEFAULT 1,
	billcycle INT DEFAULT 0,
	nextbill DATE,
	lastbill DATE,
	billgastnr INT DEFAULT 0,
	pict_file CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	load_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_update DATE,
	last_visit DATE,
	checked_in BOOLEAN DEFAULT False,
	ci_time INT DEFAULT 0,
	co_time INT DEFAULT 0,
	created_date DATE,
	user_init CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_changed DATE,
	user_init1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	disc DECIMAL DEFAULT 0,
	freezeto DATE,
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	segment INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_member_agree_ix ON cl_member (agreenum COLLATE case_insensitive);
CREATE INDEX cl_member_codenum_ix ON cl_member (codenum COLLATE case_insensitive);
CREATE INDEX cl_member_codestat_ix ON cl_member (codenum COLLATE case_insensitive,memstatus);
CREATE INDEX cl_member_gastnr_ix ON cl_member (gastnr);
CREATE INDEX cl_member_home_ix ON cl_member (homeclub);
CREATE INDEX cl_member_locker_ix ON cl_member (locker);
CREATE INDEX cl_member_locknum_ix ON cl_member (lock_num COLLATE case_insensitive);
CREATE INDEX cl_member_maingast_ix ON cl_member (main_gastnr);
CREATE INDEX cl_member_mtype_ix ON cl_member (membertype);
CREATE INDEX cl_member_sales_ix ON cl_member (salesID COLLATE case_insensitive);
CREATE INDEX cl_member_status_ix ON cl_member (memstatus);
CREATE TABLE cl_memtype (
	nr INT DEFAULT 0,
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	descript CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	iservice INT[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	serviceflag BOOLEAN[99] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false],
	activeflag BOOLEAN DEFAULT True,
	fdate DATE,
	tdate DATE,
	all_flag BOOLEAN DEFAULT False,
	max_adult INT DEFAULT 1,
	max_children INT DEFAULT 0,
	fee INT DEFAULT 0,
	dauer INT DEFAULT 0,
	fee1 DECIMAL DEFAULT 0,
	fee2 DECIMAL DEFAULT 0,
	fee3 DECIMAL DEFAULT 0,
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_memtype_code_ix ON cl_memtype (code COLLATE case_insensitive);
CREATE INDEX cl_memtype_desc_ix ON cl_memtype (descript COLLATE case_insensitive);
CREATE INDEX cl_memtype_nr_ix ON cl_memtype (nr);
CREATE TABLE cl_paysched (
	nr INT DEFAULT 0,
	descript CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	paynum INT DEFAULT 0,
	payint INT DEFAULT 0,
	period INT DEFAULT 0,
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_paysched_name_ix ON cl_paysched (descript COLLATE case_insensitive);
CREATE INDEX cl_paysched_nr_ix ON cl_paysched (nr);
CREATE TABLE cl_stat (
	key INT DEFAULT 0,
	datum DATE,
	datum1 DATE,
	typenr INT DEFAULT 0,
	revenue1 DECIMAL DEFAULT 0,
	revenue2 DECIMAL DEFAULT 0,
	revenue3 DECIMAL DEFAULT 0,
	processed INT DEFAULT 0,
	active1 INT DEFAULT 0,
	active2 INT DEFAULT 0,
	Freeze1 INT DEFAULT 0,
	Terminate INT DEFAULT 0,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_stat_key_ix ON cl_stat (key);
CREATE INDEX cl_stat_keydat_ix ON cl_stat (key,datum);
CREATE INDEX cl_stat_keydattyp_ix ON cl_stat (key,datum,typenr);
CREATE INDEX cl_stat_keytype_ix ON cl_stat (key,typenr);
CREATE TABLE cl_stat1 (
	key INT DEFAULT 0,
	datum DATE,
	class_nr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	date1 DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_stat1_key_ix ON cl_stat1 (key);
CREATE INDEX cl_stat1_keydat_ix ON cl_stat1 (key,datum);
CREATE INDEX cl_stat1_keydatnr_ix ON cl_stat1 (key,datum,class_nr);
CREATE TABLE cl_towel (
	servnr INT DEFAULT 0,
	towelnum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	booked INT DEFAULT 0,
	activeflag BOOLEAN DEFAULT True,
	toweltype INT DEFAULT 0,
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_towel_booked_ix ON cl_towel (booked,servnr);
CREATE INDEX cl_towel_nr_ix ON cl_towel (servnr);
CREATE INDEX cl_towel_nrnum_ix ON cl_towel (servnr,toweltype,towelnum COLLATE case_insensitive);
CREATE TABLE cl_trainer (
	nr INT DEFAULT 0,
	Name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gender CHARACTER VARYING COLLATE case_insensitive DEFAULT 'M',
	Adresse1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	city CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zip CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	phone CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	email CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	birthdate DATE,
	startdate DATE,
	certificate CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT True,
	offdays BOOLEAN[7] DEFAULT ARRAY[false,false,false,false,false,false,false],
	salary DECIMAL DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	date1 DATE,
	date2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX cl_trainer_name_ix ON cl_trainer (Name COLLATE case_insensitive);
CREATE INDEX cl_trainer_nr_ix ON cl_trainer (nr);
CREATE TABLE cl_upgrade (
	key INT DEFAULT 0,
	codenum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	frtype INT DEFAULT 0,
	totype INT DEFAULT 0,
	datum DATE,
	old_members CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	new_members CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	refund DECIMAL DEFAULT 0,
	new_fee DECIMAL DEFAULT 0,
	fdate DATE,
	tdate DATE,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE TABLE costbudget (
	datum DATE,
	departement INT DEFAULT 0,
	zwkum INT DEFAULT 0,
	artnr INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX costbudget_depart_ix ON costbudget (datum,departement,zwkum,artnr);
CREATE INDEX costbudget_group_ix ON costbudget (datum,zwkum,artnr);
CREATE TABLE counters (
	counter_no INT DEFAULT 0,
	counter_bez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	counter INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX counters_betr_counter_ix ON counters (betriebsnr,counter_no);
CREATE INDEX counters_counte_index ON counters (counter_no);
CREATE TABLE crm_campaign (
	cnr INT DEFAULT 0,
	datum DATE,
	zeit INT DEFAULT 0,
	usrID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	action INT DEFAULT 0,
	guesttype CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	NAT CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	country CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rmnight CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	revenue CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	age CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sex CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	City CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Birthday CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	MOB CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Inhouse CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Arrival CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	stay CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	repeater CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	numstay CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	relatives CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char6 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char7 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_campaign_cnr_index ON crm_campaign (cnr);
CREATE INDEX crm_campaign_datID_ix ON crm_campaign (datum,usrID COLLATE case_insensitive);
CREATE TABLE crm_category (
	hno INT DEFAULT 0,
	dept_nr INT DEFAULT 0,
	event_nr INT DEFAULT 0,
	categ_nr INT DEFAULT 0,
	categname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT True,
	hiddenFlag BOOLEAN DEFAULT False,
	warning CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date2 DATE,
	date3 DATE,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	sentflag BOOLEAN DEFAULT False,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	date4 DATE,
	date5 DATE,
	number4 INT DEFAULT 0,
	number5 INT DEFAULT 0,
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	confirmflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_category_cat_ix ON crm_category (dept_nr,event_nr,categ_nr);
CREATE INDEX crm_category_categ_index ON crm_category (dept_nr,event_nr,categ_nr,hno);
CREATE INDEX crm_category_catname_ix ON crm_category (categname COLLATE case_insensitive);
CREATE INDEX crm_category_dept_ix ON crm_category (dept_nr);
CREATE INDEX crm_category_event_ix ON crm_category (dept_nr,event_nr);
CREATE TABLE crm_dept (
	dept_nr INT DEFAULT 0,
	dname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	hno INT DEFAULT 0,
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sentflag BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	date4 DATE,
	date5 DATE,
	number4 INT DEFAULT 0,
	number5 INT DEFAULT 0,
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	confirmflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_dept_department_index ON crm_dept (dept_nr,hno);
CREATE INDEX crm_dept_dept_index ON crm_dept (dept_nr);
CREATE INDEX crm_dept_dname_ix ON crm_dept (dname COLLATE case_insensitive);
CREATE TABLE crm_dtl (
	trans_nr INT DEFAULT 0,
	categ_nr INT DEFAULT 0,
	qst_nr INT DEFAULT 0,
	answtype CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userpoint1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userpoint2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	number4 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	sentflag BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	date5 DATE,
	number5 INT DEFAULT 0,
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	confirmflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	webtransnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_dtl_Detail_index ON crm_dtl (trans_nr,categ_nr,qst_nr);
CREATE INDEX crm_dtl_webindex ON crm_dtl (trans_nr,webtransnr);
CREATE TABLE crm_email (
	cnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	email CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	subject CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	body CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	attachment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	guestname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	zeit INT DEFAULT 0,
	s_status INT DEFAULT 0,
	usrID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_email_cgast_index ON crm_email (cnr,gastnr);
CREATE INDEX crm_email_datum_ix ON crm_email (datum);
CREATE INDEX crm_email_gastnr_ix ON crm_email (gastnr);
CREATE TABLE crm_event (
	hno INT DEFAULT 0,
	dept_nr INT DEFAULT 0,
	event_nr INT DEFAULT 0,
	ename CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT True,
	FrDate DATE,
	ToDate DATE,
	Score CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	confirmflag BOOLEAN DEFAULT False,
	sentflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	finishlabel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	picturehotel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	date3 DATE,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	linktemplate INT DEFAULT 0,
	greetingtemplate INT DEFAULT 0,
	btn_back CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	btn_next CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	btn_finish CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	btn_close CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	txt_start CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	txt_finish CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_event_dept_ix ON crm_event (dept_nr);
CREATE INDEX crm_event_dname_ix ON crm_event (dept_nr,ename COLLATE case_insensitive);
CREATE INDEX crm_event_ename_ix ON crm_event (ename COLLATE case_insensitive);
CREATE INDEX crm_event_event_index ON crm_event (dept_nr,event_nr,hno);
CREATE INDEX crm_event_evt_index ON crm_event (dept_nr,event_nr);
CREATE TABLE crm_feedhdr (
	hno INT DEFAULT 0,
	trans_nr INT DEFAULT 0,
	dept_nr INT DEFAULT 0,
	event_nr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	guestname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	emailaddress CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Datum DATE,
	CreatedTime INT DEFAULT 0,
	CreatedDate DATE,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Age INT DEFAULT 0,
	Userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	finishflag BOOLEAN DEFAULT False,
	sentflag BOOLEAN DEFAULT False,
	confirmflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	Lastpage INT DEFAULT 0,
	gender CHARACTER VARYING COLLATE case_insensitive DEFAULT 'M',
	webtransnr INT DEFAULT 0,
	activeflag BOOLEAN DEFAULT True,
	sentthxflag BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_feedhdr_event_ix ON crm_feedhdr (dept_nr,event_nr);
CREATE INDEX crm_feedhdr_trans_index ON crm_feedhdr (trans_nr,hno);
CREATE INDEX crm_feedhdr_trans_ix ON crm_feedhdr (trans_nr);
CREATE INDEX crm_feedhdr_webindex ON crm_feedhdr (hno,trans_nr,webtransnr);
CREATE TABLE crm_fnlresult (
	range1 INT DEFAULT 0,
	range2 INT DEFAULT 0,
	description CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_fnlresult_range_ix ON crm_fnlresult (range1,range2);
CREATE TABLE crm_language (
	Language_nr INT DEFAULT 0,
	Description CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ShortDesc CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Defaults BOOLEAN DEFAULT False,
	hno INT DEFAULT 0,
	confirmflag BOOLEAN DEFAULT False,
	sentflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_language_desc_index ON crm_language (Language_nr,Description COLLATE case_insensitive);
CREATE INDEX crm_language_lang_ix ON crm_language (Language_nr,hno);
CREATE INDEX crm_language_language_index ON crm_language (Language_nr);
CREATE TABLE crm_question (
	hno INT DEFAULT 0,
	dept_nr INT DEFAULT 0,
	event_nr INT DEFAULT 0,
	categ_nr INT DEFAULT 0,
	Idquestion INT DEFAULT 0,
	qst_nr INT DEFAULT 0,
	qst CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	qst2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	qst3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	score INT DEFAULT 1,
	scoreflag INT DEFAULT 0,
	remarkflag INT DEFAULT 0,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	scoreansw CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	scoreansw2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	scoreansw3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	answtype CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	PageFlag BOOLEAN DEFAULT False,
	BoldFLag BOOLEAN DEFAULT False,
	showflag BOOLEAN DEFAULT False,
	widgetnum1 INT DEFAULT 0,
	pagenum INT DEFAULT 0,
	pagenum1 INT DEFAULT 0,
	linenum1 INT DEFAULT 0,
	linenum INT DEFAULT 0,
	rownum INT DEFAULT 0,
	rownum1 INT DEFAULT 0,
	linkqst CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	link CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	qsttype CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	linkexist BOOLEAN DEFAULT False,
	text_plus CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sametype BOOLEAN DEFAULT False,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	sentflag BOOLEAN DEFAULT False,
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number4 INT DEFAULT 0,
	number5 INT DEFAULT 0,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	confirmflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	validation CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_question_categ_ix ON crm_question (dept_nr,event_nr,categ_nr);
CREATE INDEX crm_question_dept_ix ON crm_question (dept_nr);
CREATE INDEX crm_question_event_ix ON crm_question (dept_nr,event_nr);
CREATE INDEX crm_question_quest_index ON crm_question (dept_nr,event_nr,categ_nr,qst_nr);
CREATE INDEX crm_question_question_index ON crm_question (dept_nr,event_nr,categ_nr,Idquestion,qst_nr,hno);
CREATE TABLE crm_tamplang (
	Language_nr INT DEFAULT 0,
	dept_nr INT DEFAULT 0,
	event_nr INT DEFAULT 0,
	categ_nr INT DEFAULT 0,
	qst_nr INT DEFAULT 0,
	finishlabel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	categname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	warning CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Qst CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	scoreansw CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	confirmflag BOOLEAN DEFAULT False,
	sentflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	btn_back CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	btn_next CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	btn_finish CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	btn_close CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	txt_start CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	txt_finish CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char6 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char7 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	int4 INT DEFAULT 0,
	int5 INT DEFAULT 0,
	int6 INT DEFAULT 0,
	int7 INT DEFAULT 0,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	logi6 BOOLEAN DEFAULT False,
	logi7 BOOLEAN DEFAULT False,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	deci4 DECIMAL DEFAULT 0,
	deci5 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_tamplang_tamp_index ON crm_tamplang (Language_nr,dept_nr,event_nr,categ_nr,qst_nr);
CREATE INDEX crm_tamplang_tamp_ix ON crm_tamplang (Language_nr,dept_nr,event_nr,categ_nr,qst_nr);
CREATE TABLE crm_template (
	Idtemplate INT DEFAULT 0,
	Language_nr INT DEFAULT 0,
	templatename CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	taghtml1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	taghtml1_1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	taghtml1_2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	taghtml1_3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	taghtml1_4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	confirmflag BOOLEAN DEFAULT False,
	statusflag INT DEFAULT 0,
	webconfirmflag BOOLEAN DEFAULT False,
	websentflag BOOLEAN DEFAULT False,
	webstatusflag INT DEFAULT 0,
	senttime INT DEFAULT 0,
	sentdate DATE,
	sentflag BOOLEAN DEFAULT False,
	templatetype INT DEFAULT 0,
	hno INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	deci4 DECIMAL DEFAULT 0,
	deci5 DECIMAL DEFAULT 0,
	Int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	int4 INT DEFAULT 0,
	int5 INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX crm_template_temp_ix ON crm_template (Idtemplate,Language_nr,hno);
CREATE INDEX crm_template_template_ix ON crm_template (Idtemplate,Language_nr);
CREATE TABLE cross_DTL (
	vhp_tableID INT DEFAULT 0,
	variant_DB INT DEFAULT 0,
	vhp_fieldNM CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vhp_fieldtype CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vhp_fieldwidth CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vhp_fielddefault CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vhp_fieldisNull BOOLEAN DEFAULT False,
	vhp_fieldcomments CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vhp_fieldorder INT DEFAULT 0,
	others_fieldNM CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	others_fieldtype CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	others_fieldwidth CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	others_fielddefault CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	others_fieldisNull BOOLEAN DEFAULT False,
	others_fieldcomments CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	isKey BOOLEAN DEFAULT False,
	isSend BOOLEAN DEFAULT False,
	isAutoInc BOOLEAN DEFAULT False,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	deci4 DECIMAL DEFAULT 0,
	deci5 DECIMAL DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	int4 INT DEFAULT 0,
	int5 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE TABLE cross_HDR (
	vhp_tableID INT DEFAULT 0,
	vhp_tableNM CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	variant_DB INT DEFAULT 0,
	others_tableNM CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	deci4 DECIMAL DEFAULT 0,
	deci5 DECIMAL DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	int4 INT DEFAULT 0,
	int5 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE TABLE debitor (
	artnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	rgdatum DATE,
	opart INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	gastnrmember INT DEFAULT 0,
	versanddat DATE,
	zahlkonto INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bediener_nr INT DEFAULT 0,
	counter INT DEFAULT 0,
	mahnstufe INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	transzeit INT DEFAULT 0,
	kontakt_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	vesrdep DECIMAL DEFAULT 0,
	vesrdat DATE,
	vesrdepot CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vesrdepot2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vesrcod CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	verstat INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	betrieb_gastmem INT DEFAULT 0,
	debref INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX debitor_artdat_ix ON debitor (artnr,rgdatum,opart);
CREATE INDEX debitor_artgast_ix ON debitor (artnr,name COLLATE case_insensitive,gastnr,rgdatum);
CREATE INDEX debitor_betr_ref_ix ON debitor (betriebsnr,rechnr,artnr,debref);
CREATE INDEX debitor_counter_ix ON debitor (counter,opart);
CREATE INDEX debitor_deb_rechnr_ix ON debitor (rechnr,opart,counter);
CREATE INDEX debitor_gastnr_ix ON debitor (opart,artnr,name COLLATE case_insensitive,gastnr);
CREATE INDEX debitor_gastrgdat_ix ON debitor (opart,artnr,rgdatum,name COLLATE case_insensitive,gastnr);
CREATE INDEX debitor_gnr_ix ON debitor (gastnr,opart);
CREATE INDEX debitor_gnrmbr_ix ON debitor (gastnrmember,rechnr);
CREATE INDEX debitor_rech_count_ix ON debitor (rechnr,counter);
CREATE INDEX debitor_rechnr_ix ON debitor (opart,artnr,rechnr);
CREATE INDEX debitor_rgdat_ix ON debitor (rgdatum);
CREATE INDEX debitor_rgsaldo_ix ON debitor (opart,artnr,saldo,name COLLATE case_insensitive,gastnr);
CREATE INDEX debitor_vesr1_ix ON debitor (vesrcod COLLATE case_insensitive,vesrdepot COLLATE case_insensitive,vesrdepot2 COLLATE case_insensitive);
CREATE INDEX debitor_vesr2_ix ON debitor (vesrdepot COLLATE case_insensitive);
CREATE INDEX debitor_vesr3_ix ON debitor (vesrdepot2 COLLATE case_insensitive);
CREATE TABLE debthis (
	artnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	rgdatum DATE,
	rechnr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	gastnrmember INT DEFAULT 0,
	zahlkonto INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bediener_nr INT DEFAULT 0,
	counter INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vesrdep DECIMAL DEFAULT 0,
	vesrcod CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	verstat INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX debthis_art_counter_ix ON debthis (artnr,counter);
CREATE INDEX debthis_art_dat_gast_ix ON debthis (artnr,gastnr,rgdatum);
CREATE INDEX debthis_art_dat_zahl_ix ON debthis (artnr,rgdatum,zahlkonto);
CREATE INDEX debthis_art_dat_ix ON debthis (artnr,rgdatum);
CREATE INDEX debthis_art_gast_zahl_ix ON debthis (artnr,gastnr,zahlkonto);
CREATE INDEX debthis_art_gast_ix ON debthis (artnr,gastnr);
CREATE INDEX debthis_art_rechn_ix ON debthis (artnr,rechnr);
CREATE INDEX debthis_counter_ix ON debthis (counter);
CREATE TABLE desttext (
	refcode INT DEFAULT 0,
	lang INT DEFAULT 0,
	dtext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX desttext_idx_ref ON desttext (refcode,lang);
CREATE TABLE dml_art (
	datum DATE,
	artnr INT DEFAULT 0,
	anzahl DECIMAL DEFAULT 0,
	einzelpreis DECIMAL DEFAULT 0,
	geliefert DECIMAL DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX dml_art_datart_ix ON dml_art (datum,artnr);
CREATE INDEX dml_art_datum_ix ON dml_art (datum);
CREATE TABLE dml_artdep (
	departement INT DEFAULT 0,
	datum DATE,
	artnr INT DEFAULT 0,
	anzahl DECIMAL DEFAULT 0,
	einzelpreis DECIMAL DEFAULT 0,
	geliefert DECIMAL DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX dml_artdep_departdat_ix ON dml_artdep (departement,datum,artnr);
CREATE INDEX dml_artdep_deptdat_ix ON dml_artdep (departement,datum);
CREATE TABLE dml_rate (
	artnr INT DEFAULT 0,
	lief_nr INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	einzelpreis DECIMAL DEFAULT 0,
	in_liefunit BOOLEAN DEFAULT False,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	number1 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX dml_rate_artdat_ix ON dml_rate (artnr,date1,date2);
CREATE INDEX dml_rate_artlief_ix ON dml_rate (artnr,lief_nr);
CREATE INDEX dml_rate_artliefdat_ix ON dml_rate (artnr,lief_nr,date1,date2);
CREATE INDEX dml_rate_artnr_ix ON dml_rate (artnr);
CREATE TABLE eg_action (
	actionnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	maintask INT DEFAULT 0,
	comment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	interval INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	Usefor INT DEFAULT 0,
	create_date DATE,
	create_time INT DEFAULT 0,
	create_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_action_interval_ix ON eg_action (interval);
CREATE INDEX eg_action_maintask_ix ON eg_action (maintask);
CREATE INDEX eg_action_nr_index ON eg_action (actionnr);
CREATE TABLE eg_Alert (
	create_date DATE,
	create_time INT DEFAULT 0,
	create_by INT DEFAULT 0,
	Reqnr INT DEFAULT 0,
	msg CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	sendNr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	msgStatus INT DEFAULT 0,
	sendto INT DEFAULT 0,
	FromFile CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE TABLE eg_budget (
	nr INT DEFAULT 0,
	year INT DEFAULT 0,
	month INT DEFAULT 0,
	received_date DATE,
	score DECIMAL DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	closeflag BOOLEAN DEFAULT False,
	close_date DATE,
	close_time INT DEFAULT 0,
	close_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_budget_date_ix ON eg_budget (received_date);
CREATE INDEX eg_budget_nym_index ON eg_budget (nr,year,month);
CREATE TABLE eg_cost (
	datum DATE,
	resource_nr INT DEFAULT 0,
	usage INT DEFAULT 0,
	price DECIMAL DEFAULT 0,
	cost DECIMAL DEFAULT 0,
	created_date DATE,
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	year INT DEFAULT 0,
	Month INT DEFAULT 0,
	closeflag BOOLEAN DEFAULT False,
	close_date DATE,
	close_time INT DEFAULT 0,
	close_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_cost_ymr_ix ON eg_cost (year,Month,resource_nr);
CREATE TABLE eg_Duration (
	Duration_nr INT DEFAULT 0,
	days INT DEFAULT 0,
	hour INT DEFAULT 0,
	minute INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE TABLE eg_location (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	building INT DEFAULT 0,
	floor CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	GuestFlag BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_location_build_ix ON eg_location (building);
CREATE INDEX eg_location_floor_ix ON eg_location (floor COLLATE case_insensitive);
CREATE INDEX eg_location_nr_index ON eg_location (nr);
CREATE TABLE eg_MainStat (
	MainStatus INT DEFAULT 0,
	estworkdate DATE,
	workdate DATE,
	donedate DATE,
	frequency INT DEFAULT 0,
	location INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ObjectItem INT DEFAULT 0,
	Category INT DEFAULT 0,
	Object INT DEFAULT 0,
	PIC INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_MainStat_CatOb_ix ON eg_MainStat (Category,Object);
CREATE INDEX eg_MainStat_CatObjtem_ix ON eg_MainStat (Category,Object,ObjectItem);
CREATE INDEX eg_MainStat_EstStat_ix ON eg_MainStat (estworkdate,MainStatus);
CREATE INDEX eg_MainStat_itemLocZin_ix ON eg_MainStat (Category,Object,location,zinr COLLATE case_insensitive,ObjectItem);
CREATE INDEX eg_MainStat_locZin_ix ON eg_MainStat (location,zinr COLLATE case_insensitive);
CREATE INDEX eg_MainStat_WorkStat_ix ON eg_MainStat (MainStatus,workdate);
CREATE TABLE eg_maintain (
	maintainnr INT DEFAULT 0,
	year INT DEFAULT 0,
	month INT DEFAULT 0,
	week INT DEFAULT 0,
	donedate DATE,
	maintask INT DEFAULT 0,
	type INT DEFAULT 0,
	propertynr INT DEFAULT 0,
	workdate DATE,
	comments CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_date DATE,
	estWorkDate DATE,
	typework INT DEFAULT 0,
	Location INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	PIC INT DEFAULT 0,
	delete_flag BOOLEAN DEFAULT False,
	category INT DEFAULT 0,
	memo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	smsflag BOOLEAN DEFAULT False,
	cancel_date DATE,
	cancel_time INT DEFAULT 0,
	cancel_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_maintain_Cat_ix ON eg_maintain (category);
CREATE INDEX eg_maintain_CatObTem_ix ON eg_maintain (category,maintask,propertynr);
CREATE INDEX eg_maintain_loczin_ix ON eg_maintain (Location,zinr COLLATE case_insensitive);
CREATE INDEX eg_maintain_nr_ix ON eg_maintain (maintainnr);
CREATE INDEX eg_maintain_ObItem_ix ON eg_maintain (propertynr);
CREATE INDEX eg_maintain_Object_ix ON eg_maintain (maintask);
CREATE INDEX eg_maintain_ym_ix ON eg_maintain (year,month);
CREATE TABLE eg_mdetail (
	key INT DEFAULT 0,
	maintainnr INT DEFAULT 0,
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number4 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	type INT DEFAULT 0,
	create_date DATE,
	create_time INT DEFAULT 0,
	create_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_mdetail_keym_ix ON eg_mdetail (key,maintainnr);
CREATE INDEX eg_mdetail_keynr_index ON eg_mdetail (key,maintainnr,nr);
CREATE INDEX eg_mdetail_knr_ix ON eg_mdetail (key,nr);
CREATE TABLE eg_MessageNo (
	nr INT DEFAULT 0,
	Name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	MobileNo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Position CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE TABLE eg_mobileNr (
	nr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	position CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mobileNr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	activeflag BOOLEAN DEFAULT True,
	_recid serial PRIMARY KEY
);
CREATE TABLE eg_moveProperty (
	datum DATE,
	Property_nr INT DEFAULT 0,
	fr_Location INT DEFAULT 0,
	to_Location INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	fr_Room CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	to_Room CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE TABLE eg_property (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	location INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	brand CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	capacity CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dimension CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	type CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	maintask INT DEFAULT 0,
	datum DATE,
	price DECIMAL DEFAULT 0,
	spec CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	asset CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	ActiveFlag BOOLEAN DEFAULT True,
	MeterRec BOOLEAN DEFAULT False,
	MeterMax INT DEFAULT 0,
	HourMax INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_property_asset_ix ON eg_property (asset COLLATE case_insensitive);
CREATE INDEX eg_property_bez_ix ON eg_property (bezeich COLLATE case_insensitive);
CREATE INDEX eg_property_location_ix ON eg_property (location);
CREATE INDEX eg_property_maintask_ix ON eg_property (maintask);
CREATE INDEX eg_property_mtloc_x ON eg_property (maintask,location);
CREATE INDEX eg_property_mtloczin_x ON eg_property (maintask,location,zinr COLLATE case_insensitive);
CREATE INDEX eg_property_mtzinr_ix ON eg_property (maintask,zinr COLLATE case_insensitive);
CREATE INDEX eg_property_nr_index ON eg_property (nr);
CREATE INDEX eg_property_zinr_ix ON eg_property (zinr COLLATE case_insensitive);
CREATE TABLE eg_propMeter (
	Propertynr INT DEFAULT 0,
	rec_Date DATE,
	rec_time INT DEFAULT 0,
	rec_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	val_Meter INT DEFAULT 0,
	val_hour INT DEFAULT 0,
	create_date DATE,
	create_time INT DEFAULT 0,
	nr INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_propMeter_nr_ix ON eg_propMeter (Propertynr);
CREATE TABLE eg_queasy (
	key INT DEFAULT 0,
	reqnr INT DEFAULT 0,
	stock_nr INT DEFAULT 0,
	stock_qty INT DEFAULT 0,
	attachment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	att_desc CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	hist_nr INT DEFAULT 0,
	hist_fdate DATE,
	usr_nr INT DEFAULT 0,
	number1 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	date1 DATE,
	deci1 DECIMAL DEFAULT 0,
	hist_time INT DEFAULT 0,
	price DECIMAL DEFAULT 0,
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date2 DATE,
	date3 DATE,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_queasy_key_ix ON eg_queasy (key);
CREATE INDEX eg_queasy_keynrstock_ix ON eg_queasy (key,reqnr,stock_nr);
CREATE INDEX eg_queasy_keyreq_ix ON eg_queasy (key,reqnr);
CREATE INDEX eg_queasy_keystock_ix ON eg_queasy (key,stock_nr);
CREATE TABLE eg_reqDetail (
	reqnr INT DEFAULT 0,
	actionnr INT DEFAULT 0,
	comment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	create_date DATE,
	create_time INT DEFAULT 0,
	create_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	EstFinishDate DATE,
	EstFinishTime INT DEFAULT 0,
	action CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE TABLE eg_reqif (
	reqnr INT DEFAULT 0,
	sent_date DATE,
	sent_time INT DEFAULT 0,
	usr_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rstatus INT DEFAULT 0,
	type INT DEFAULT 0,
	task_def CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	task_solution CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	to_dept CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	source CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	request_date DATE,
	sub_taskdesc CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	to_usr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	frm_usr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	email CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	pager CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mobile_ph CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_int INT DEFAULT 0,
	reserve_char CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_log BOOLEAN DEFAULT False,
	reserve_date DATE,
	category CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	frm_dept CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_reqif_req_ix ON eg_reqif (reqnr);
CREATE INDEX eg_reqif_stat_ix ON eg_reqif (rstatus);
CREATE INDEX eg_reqif_stattype_ix ON eg_reqif (rstatus,type);
CREATE TABLE eg_ReqStat (
	reqfrom INT DEFAULT 0,
	Deptnum INT DEFAULT 0,
	Location INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Category INT DEFAULT 0,
	Object INT DEFAULT 0,
	ObjectItem INT DEFAULT 0,
	ObjectTask CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	PIC INT DEFAULT 0,
	reqStat INT DEFAULT 0,
	estFinishDate DATE,
	estfinishtime INT DEFAULT 0,
	urgency INT DEFAULT 0,
	opendate DATE,
	opentime INT DEFAULT 0,
	processdate DATE,
	processtime INT DEFAULT 0,
	donedate DATE,
	donetime INT DEFAULT 0,
	closedate DATE,
	closetime INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_ReqStat_CatObjectItem_ix ON eg_ReqStat (Category,Object,ObjectItem);
CREATE INDEX eg_ReqStat_DeptLocItem_ix ON eg_ReqStat (Deptnum,Location,zinr COLLATE case_insensitive,Category,Object,ObjectItem);
CREATE INDEX eg_ReqStat_DeptPic_ix ON eg_ReqStat (Deptnum,PIC);
CREATE INDEX eg_ReqStat_FromDept ON eg_ReqStat (reqfrom,Deptnum);
CREATE INDEX eg_ReqStat_LocZin_ix ON eg_ReqStat (Location,zinr COLLATE case_insensitive);
CREATE TABLE eg_request (
	reqnr INT DEFAULT 0,
	opened_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	opened_date DATE,
	process_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	process_date DATE,
	closed_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	closed_date DATE,
	reqStatus INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gastnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	maintask INT DEFAULT 0,
	sub_task CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deptnum INT DEFAULT 0,
	category INT DEFAULT 0,
	source INT DEFAULT 0,
	task_def CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	task_solv CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_date DATE,
	from_dept INT DEFAULT 0,
	assign_to2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_int INT DEFAULT 0,
	reserve_char CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_date DATE,
	reserve_log BOOLEAN DEFAULT False,
	opened_time INT DEFAULT 0,
	process_time INT DEFAULT 0,
	closed_time INT DEFAULT 0,
	urgency INT DEFAULT 0,
	ex_finishdate DATE,
	memo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sppart_cost DECIMAL DEFAULT 0,
	other_cost DECIMAL DEFAULT 0,
	reslinnr INT DEFAULT 0,
	from_date DATE,
	propertynr INT DEFAULT 0,
	to_date DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	date3 DATE,
	deci3 DECIMAL DEFAULT 0,
	assign_to INT DEFAULT 0,
	location INT DEFAULT 0,
	Done_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Done_date DATE,
	Done_time INT DEFAULT 0,
	ex_finishTime INT DEFAULT 0,
	outsourceFlag BOOLEAN DEFAULT False,
	ReasonStatus CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ReasonDoneTime CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Delete_Flag BOOLEAN DEFAULT False,
	ex_finishdate1 DATE,
	ex_finishTime1 INT DEFAULT 0,
	cancel_date DATE,
	cancel_time INT DEFAULT 0,
	cancel_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Source_name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	subtask_bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	subtask_duration CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_request_catstat_ix ON eg_request (category,reqStatus);
CREATE INDEX eg_request_depstat_ix ON eg_request (deptnum,reqStatus);
CREATE INDEX eg_request_dept_ix ON eg_request (deptnum);
CREATE INDEX eg_request_gastnr_ix ON eg_request (gastnr);
CREATE INDEX eg_request_mdept_ix ON eg_request (maintask,deptnum);
CREATE INDEX eg_request_mstatdpt_ix ON eg_request (maintask,reqStatus,deptnum);
CREATE INDEX eg_request_mzidept_ix ON eg_request (maintask,zinr COLLATE case_insensitive,deptnum);
CREATE INDEX eg_request_mzistatdpt_ix ON eg_request (zinr COLLATE case_insensitive,reqStatus,maintask,deptnum);
CREATE INDEX eg_request_op_gast_ix ON eg_request (opened_date,gastnr);
CREATE INDEX eg_request_opdate_pic_ix ON eg_request (opened_date,assign_to2 COLLATE case_insensitive);
CREATE INDEX eg_request_opdate_ix ON eg_request (opened_date);
CREATE INDEX eg_request_prop_ix ON eg_request (propertynr);
CREATE INDEX eg_request_req_ix ON eg_request (reqnr);
CREATE INDEX eg_request_reslin_ix ON eg_request (resnr,reslinnr);
CREATE INDEX eg_request_statsource_ix ON eg_request (source,reqStatus);
CREATE INDEX eg_request_zidpt_ix ON eg_request (zinr COLLATE case_insensitive,deptnum);
CREATE INDEX eg_request_zinr_ix ON eg_request (zinr COLLATE case_insensitive);
CREATE INDEX eg_request_zistatdpt_ix ON eg_request (zinr COLLATE case_insensitive,reqStatus,deptnum);
CREATE TABLE eg_resources (
	nr INT DEFAULT 0,
	type INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	unit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	price DECIMAL DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	dailyRec BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_resources_nr_index ON eg_resources (nr);
CREATE INDEX eg_resources_type_ix ON eg_resources (type);
CREATE TABLE eg_staff (
	nr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	position CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	usergroup INT DEFAULT 0,
	vhpuser INT DEFAULT 0,
	activeFlag BOOLEAN DEFAULT False,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mobile CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Skill CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_staff_group_ix ON eg_staff (usergroup);
CREATE INDEX eg_staff_name_ix ON eg_staff (name COLLATE case_insensitive);
CREATE INDEX eg_staff_nr_index ON eg_staff (nr);
CREATE TABLE eg_stat (
	datum DATE,
	dept INT DEFAULT 0,
	category INT DEFAULT 0,
	source INT DEFAULT 0,
	maintask INT DEFAULT 0,
	sub_task CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	qty INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	assign_to CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sppart_cost DECIMAL DEFAULT 0,
	other_cost DECIMAL DEFAULT 0,
	reserve_num1 INT DEFAULT 0,
	reserve_num2 INT DEFAULT 0,
	reserve_num3 INT DEFAULT 0,
	reserve_char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_date1 DATE,
	reserve_deci1 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_stat_d_cat_pic_ix ON eg_stat (datum,category,assign_to COLLATE case_insensitive);
CREATE INDEX eg_stat_d_dpt_cat_ix ON eg_stat (datum,dept,category);
CREATE INDEX eg_stat_d_dpt_mt_ix ON eg_stat (datum,maintask,dept);
CREATE INDEX eg_stat_d_dpt_sour_ix ON eg_stat (datum,dept,source);
CREATE INDEX eg_stat_d_dptcts_ix ON eg_stat (datum,dept,category,source);
CREATE INDEX eg_stat_d_dptctspic_ix ON eg_stat (datum,dept,category,source,assign_to COLLATE case_insensitive);
CREATE INDEX eg_stat_dat_cat_ix ON eg_stat (datum,category);
CREATE INDEX eg_stat_dat_dpt_ix ON eg_stat (datum,dept);
CREATE INDEX eg_stat_dat_gast_ix ON eg_stat (datum,gastnr);
CREATE INDEX eg_stat_dat_mt_ix ON eg_stat (datum,maintask);
CREATE INDEX eg_stat_dat_pic_ix ON eg_stat (datum,assign_to COLLATE case_insensitive);
CREATE INDEX eg_stat_dat_source_ix ON eg_stat (datum,source);
CREATE INDEX eg_stat_dat_sub_ix ON eg_stat (datum,sub_task COLLATE case_insensitive);
CREATE INDEX eg_stat_dat_zin_ix ON eg_stat (datum,zinr COLLATE case_insensitive);
CREATE INDEX eg_stat_datum_ix ON eg_stat (datum);
CREATE TABLE eg_subtask (
	sub_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dept_nr INT DEFAULT 0,
	main_nr INT DEFAULT 0,
	dur_nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_int INT DEFAULT 0,
	reserve_char CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_date DATE,
	reserve_log BOOLEAN DEFAULT False,
	create_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	create_date DATE,
	create_time INT DEFAULT 0,
	sourceForm CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	OthersFlag BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX eg_subtask_code_ix ON eg_subtask (sub_code COLLATE case_insensitive);
CREATE INDEX eg_subtask_dept_ix ON eg_subtask (dept_nr);
CREATE INDEX eg_subtask_dur_ix ON eg_subtask (dur_nr);
CREATE INDEX eg_subtask_main_ix ON eg_subtask (main_nr);
CREATE INDEX eg_subtask_maindept_ix ON eg_subtask (main_nr,dept_nr);
CREATE TABLE eg_vendor (
	vendor_nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	address CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	phone CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	website CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	email CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	contact_person CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	activeflag BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE TABLE eg_vperform (
	vendor_nr INT DEFAULT 0,
	reqnr INT DEFAULT 0,
	startdate DATE,
	finishdate DATE,
	price DECIMAL DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	pic CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	estFinishDate DATE,
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_date DATE,
	created_time INT DEFAULT 0,
	perform_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	documentNo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE TABLE ekum (
	eknr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX ekum_betr_eknr_ix ON ekum (betriebsnr,eknr);
CREATE INDEX ekum_bez_ix ON ekum (bezeich COLLATE case_insensitive,eknr);
CREATE INDEX ekum_eknr ON ekum (eknr);
CREATE TABLE employee (
	id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	birthdate DATE,
	Address1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	address2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	city CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zipcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nation CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gender INT DEFAULT 0,
	religion INT DEFAULT 0,
	position CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	estat INT DEFAULT 0,
	mstat INT DEFAULT 0,
	degree INT DEFAULT 0,
	bsalary DECIMAL DEFAULT 0,
	imgfile CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT False,
	Telephone CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dept INT DEFAULT 0,
	AccNo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Bank CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Branch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	hdate DATE,
	idcard CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ben_eat DECIMAL DEFAULT 0,
	ben_trans DECIMAL DEFAULT 0,
	Doct DECIMAL DEFAULT 0,
	pbirth DATE,
	Partner CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Tdate DATE,
	Child CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	Allowance BOOLEAN[6] DEFAULT ARRAY[false,false,false,false,false,false],
	cbirth DATE[5] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	_recid serial PRIMARY KEY
);
CREATE INDEX employee_bdate_ix ON employee (birthdate,activeflag);
CREATE INDEX employee_deg_ix ON employee (degree,activeflag);
CREATE INDEX employee_estat_ix ON employee (estat,activeflag);
CREATE INDEX employee_id_index ON employee (id COLLATE case_insensitive);
CREATE INDEX employee_mstat_ix ON employee (mstat,activeflag);
CREATE INDEX employee_name_ix ON employee (Name COLLATE case_insensitive);
CREATE INDEX employee_namflag_ix ON employee (Name COLLATE case_insensitive,activeflag);
CREATE INDEX employee_nat_ix ON employee (nation COLLATE case_insensitive,activeflag);
CREATE INDEX employee_pos_ix ON employee (position COLLATE case_insensitive,activeflag);
CREATE INDEX employee_relig_ix ON employee (religion,activeflag);
CREATE TABLE equiplan (
	artnr INT DEFAULT 0,
	datum DATE,
	anzahl INT[48] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX equiplan_equiplan_ix ON equiplan (datum,artnr,departement);
CREATE TABLE exrate (
	datum DATE,
	artnr INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX exrate_artdat_ix ON exrate (artnr,datum);
CREATE INDEX exrate_date_ix ON exrate (datum);
CREATE TABLE fa_artikel (
	nr INT DEFAULT 0,
	p_nr INT DEFAULT 0,
	katnr INT DEFAULT 0,
	gnr INT DEFAULT 0,
	subgrp INT DEFAULT 0,
	lief_nr INT DEFAULT 0,
	anzahl INT DEFAULT 1,
	anz100 INT DEFAULT 0,
	warenwert DECIMAL DEFAULT 0,
	book_wert DECIMAL DEFAULT 0,
	depn_wert DECIMAL DEFAULT 0,
	first_depn DATE,
	next_depn DATE,
	last_depn DATE,
	anz_depn INT DEFAULT 0,
	loeschflag INT DEFAULT 0,
	ID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	CID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created DATE,
	changed DATE,
	credit_fibu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	debit_fibu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	posted BOOLEAN DEFAULT False,
	DID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deleted DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_artikel_datflag_ix ON fa_artikel (loeschflag,deleted);
CREATE INDEX fa_artikel_flag_ix ON fa_artikel (loeschflag);
CREATE INDEX fa_artikel_ndatflag_ix ON fa_artikel (loeschflag,next_depn);
CREATE INDEX fa_artikel_nr_ix ON fa_artikel (nr);
CREATE INDEX fa_artikel_postdatflag_ix ON fa_artikel (next_depn,loeschflag,posted);
CREATE TABLE fa_Counter (
	count_type INT DEFAULT 0,
	yy INT DEFAULT 0,
	mm INT DEFAULT 0,
	dd INT DEFAULT 0,
	counters INT DEFAULT 0,
	docu_type INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE TABLE fa_DP (
	Order_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Pay_Date DATE,
	Pay_Time INT DEFAULT 0,
	Create_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	change_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	change_date DATE,
	change_time INT DEFAULT 0,
	Pay_type CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Po_flag CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	number4 INT DEFAULT 0,
	number5 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	dec4 DECIMAL DEFAULT 0,
	dec5 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE TABLE fa_grup (
	gnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	flag INT DEFAULT 0,
	credit_fibu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	debit_fibu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_grup_gnr_ix ON fa_grup (gnr);
CREATE INDEX fa_grup_nrflag_ix ON fa_grup (gnr,flag);
CREATE TABLE fa_kateg (
	katnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nutzjahr INT DEFAULT 0,
	rate DECIMAL DEFAULT 0,
	methode INT DEFAULT 0,
	num INT[3] DEFAULT ARRAY[0,0,0],
	deci DECIMAL[3] DEFAULT ARRAY[0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_kateg_katnr_ix ON fa_kateg (katnr);
CREATE TABLE fa_lager (
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lager_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_lager_bezeich_ix ON fa_lager (bezeich COLLATE case_insensitive);
CREATE INDEX fa_lager_lager_ix ON fa_lager (lager_nr);
CREATE TABLE fa_op (
	nr INT DEFAULT 0,
	opart INT DEFAULT 0,
	datum DATE,
	sysdate DATE,
	zeit INT DEFAULT 0,
	einzelpreis DECIMAL DEFAULT 0,
	anzahl INT DEFAULT 0,
	warenwert DECIMAL DEFAULT 0,
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	loeschflag INT DEFAULT 0,
	ID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	CID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created DATE,
	changed DATE,
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lscheinnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lief_nr INT DEFAULT 0,
	retour_reason CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_op_date_ix ON fa_op (datum);
CREATE INDEX fa_op_datflag_ix ON fa_op (datum,loeschflag);
CREATE INDEX fa_op_datopart_ix ON fa_op (opart,datum);
CREATE INDEX fa_op_datopflag_ix ON fa_op (opart,datum,loeschflag);
CREATE INDEX fa_op_docdatflag_ix ON fa_op (datum,docu_nr COLLATE case_insensitive,loeschflag);
CREATE INDEX fa_op_flag_ix ON fa_op (loeschflag);
CREATE INDEX fa_op_liefdflag_ix ON fa_op (lief_nr,lscheinnr COLLATE case_insensitive,loeschflag);
CREATE INDEX fa_op_scheinflag_ix ON fa_op (datum,lscheinnr COLLATE case_insensitive,loeschflag);
CREATE TABLE fa_Order (
	Order_Nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Fa_Nr INT DEFAULT 0,
	PR_Flag BOOLEAN DEFAULT False,
	Order_Qty INT DEFAULT 0,
	Order_Price DECIMAL DEFAULT 0,
	Order_Amount DECIMAL DEFAULT 0,
	Discount1 DECIMAL DEFAULT 0,
	Discount2 DECIMAL DEFAULT 0,
	VAT DECIMAL DEFAULT 0,
	ExchangeRate DECIMAL DEFAULT 0,
	Currency INT DEFAULT 0,
	Fa_remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Activeflag INT DEFAULT 0,
	ActiveReason CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Cancel_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Cancel_Date DATE,
	Cancel_Time INT DEFAULT 0,
	Delete_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Delete_Date DATE,
	Delete_Time INT DEFAULT 0,
	Create_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Create_Date DATE,
	Create_Time INT DEFAULT 0,
	Change_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Change_Date DATE,
	Change_Time INT DEFAULT 0,
	CloseFlag BOOLEAN DEFAULT False,
	Close_Date DATE,
	Close_Time INT DEFAULT 0,
	statFlag INT DEFAULT 0,
	Fa_Pos INT DEFAULT 0,
	op_art INT DEFAULT 0,
	delivered_qty INT DEFAULT 0,
	delivered_date DATE,
	delivered_price DECIMAL DEFAULT 0,
	delivered_amount DECIMAL DEFAULT 0,
	last_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_Order_faActive ON fa_Order (Order_Nr COLLATE case_insensitive,Activeflag,Fa_Nr);
CREATE INDEX fa_Order_OrdFa_nr ON fa_Order (Order_Nr COLLATE case_insensitive,Fa_Nr);
CREATE TABLE fa_OrdHeader (
	Order_Nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	PR_Nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	PR_Flag BOOLEAN DEFAULT False,
	Order_Date DATE,
	Order_Type CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Order_Name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Order_Desc CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Supplier_Nr INT DEFAULT 0,
	Dept_Nr INT DEFAULT 0,
	Currency INT DEFAULT 0,
	Credit_Term INT DEFAULT 0,
	PaymentDate DATE,
	Expected_Delivery DATE,
	Approved_1 BOOLEAN DEFAULT False,
	Approved_1_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Approved_1_Date DATE,
	Approved_1_time INT DEFAULT 0,
	Approved_2 BOOLEAN DEFAULT False,
	Approved_2_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Approved_2_Date DATE,
	Approved_2_time INT DEFAULT 0,
	Approved_3 BOOLEAN DEFAULT False,
	Approved_3_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Approved_3_Date DATE,
	Approved_3_Time INT DEFAULT 0,
	Released_Flag BOOLEAN DEFAULT False,
	Released_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Released_Date DATE,
	Released_Time INT DEFAULT 0,
	Created_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Created_Date DATE,
	Created_Time INT DEFAULT 0,
	ActiveFlag INT DEFAULT 0,
	Cancel_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Cancel_Date DATE,
	Cancel_Time INT DEFAULT 0,
	Delete_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Delete_Date DATE,
	Delete_Time INT DEFAULT 0,
	statFlag INT DEFAULT 0,
	printed DATE,
	Modified_By CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Modified_Date DATE,
	Modified_Time INT DEFAULT 0,
	Total_Amount DECIMAL DEFAULT 0,
	PrintedTime INT DEFAULT 0,
	close_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	close_date DATE,
	close_time INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_OrdHeader_datumActive ON fa_OrdHeader (Order_Date,ActiveFlag);
CREATE INDEX fa_OrdHeader_datumactiveorder ON fa_OrdHeader (Order_Date,ActiveFlag,Order_Nr COLLATE case_insensitive);
CREATE INDEX fa_OrdHeader_datumactiveSupp ON fa_OrdHeader (Order_Date,ActiveFlag,Supplier_Nr);
CREATE INDEX fa_OrdHeader_OrdDateSupp ON fa_OrdHeader (Order_Nr COLLATE case_insensitive,Order_Date,Supplier_Nr);
CREATE TABLE fa_QuoDetail (
	quotation_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Fa_nr INT DEFAULT 0,
	min_qty INT DEFAULT 0,
	price DECIMAL DEFAULT 0,
	disc1 DECIMAL DEFAULT 0,
	disc2 DECIMAL DEFAULT 0,
	vat DECIMAL DEFAULT 0,
	remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	delivery_date DATE,
	time_Deliver INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	number4 INT DEFAULT 0,
	number5 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	dec4 DECIMAL DEFAULT 0,
	dec5 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE TABLE fa_quotation (
	quotation_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	supplier_nr INT DEFAULT 0,
	valid_date DATE,
	contact_person CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Attachment1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	attachment2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	attachment3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	attachment4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	attachment5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	DP CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Remarks CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	number4 INT DEFAULT 0,
	number5 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	date4 DATE,
	date5 DATE,
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	dec4 DECIMAL DEFAULT 0,
	dec5 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	logi4 BOOLEAN DEFAULT False,
	logi5 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE TABLE fa_user (
	nr INT DEFAULT 0,
	rcvID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rcvName CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anzahl INT DEFAULT 0,
	vom_datum DATE,
	bis_datum DATE,
	fa_status INT DEFAULT 0,
	released DATE,
	created DATE,
	createdID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	modifed DATE,
	chgID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	res_int INT[3] DEFAULT ARRAY[0,0,0],
	res_logi BOOLEAN[3] DEFAULT ARRAY[false,false,false],
	res_date DATE[3] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date],
	res_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	_recid serial PRIMARY KEY
);
CREATE INDEX fa_user_nr_date_ix ON fa_user (nr,vom_datum);
CREATE INDEX fa_user_nr_ix ON fa_user (nr);
CREATE INDEX fa_user_rcvdate_ix ON fa_user (rcvName COLLATE case_insensitive,vom_datum);
CREATE INDEX fa_user_rcvname_ix ON fa_user (rcvName COLLATE case_insensitive);
CREATE INDEX fa_user_stat_ix ON fa_user (fa_status);
CREATE INDEX fa_user_statdat_ix ON fa_user (fa_status,vom_datum);
CREATE TABLE fbstat (
	datum DATE,
	departement INT DEFAULT 0,
	food_grev DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	bev_grev DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	other_grev DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	food_wrev DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	bev_wrev DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	other_wrev DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	food_gpax INT[4] DEFAULT ARRAY[0,0,0,0],
	bev_gpax INT[4] DEFAULT ARRAY[0,0,0,0],
	other_gpax INT[4] DEFAULT ARRAY[0,0,0,0],
	food_wpax INT[4] DEFAULT ARRAY[0,0,0,0],
	bev_wpax INT[4] DEFAULT ARRAY[0,0,0,0],
	other_wpax INT[4] DEFAULT ARRAY[0,0,0,0],
	food_gcost DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	bev_gcost DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	other_gcost DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	food_wcost DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	bev_wcost DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	other_wcost DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX fbstat_datdept_ix ON fbstat (datum,departement);
CREATE INDEX fbstat_date_ix ON fbstat (datum);
CREATE INDEX fbstat_dept_ix ON fbstat (departement);
CREATE TABLE feiertag (
	datum DATE,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	aktiv BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX feiertag_feiertag_ix ON feiertag (datum);
CREATE TABLE ffont (
	emu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Contcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	make CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX ffont_ffont ON ffont (emu COLLATE case_insensitive,make COLLATE case_insensitive,code COLLATE case_insensitive);
CREATE TABLE fixleist (
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	artnr INT DEFAULT 0,
	number INT DEFAULT 1,
	sequenz INT DEFAULT 1,
	dekade INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	lfakt DATE,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Persons INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX fixleist_betr_fix_ix ON fixleist (betriebsnr,resnr,reslinnr,departement,artnr);
CREATE INDEX fixleist_fix_index ON fixleist (resnr,reslinnr,number);
CREATE TABLE gc_giro (
	bankname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gironum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	giro_status INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	dueDate DATE,
	postedDate DATE,
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created DATE,
	changed DATE,
	CID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	res_int INT[3] DEFAULT ARRAY[0,0,0],
	res_dec DECIMAL[3] DEFAULT ARRAY[0,0,0],
	res_date DATE[3] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date],
	res_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	res_logi BOOLEAN[3] DEFAULT ARRAY[false,false,false],
	_recid serial PRIMARY KEY
);
CREATE INDEX gc_giro_bank_ix ON gc_giro (bankname COLLATE case_insensitive);
CREATE INDEX gc_giro_banknum_ix ON gc_giro (bankname COLLATE case_insensitive,gironum COLLATE case_insensitive);
CREATE INDEX gc_giro_bankstat_ix ON gc_giro (bankname COLLATE case_insensitive,giro_status);
CREATE INDEX gc_giro_num_ix ON gc_giro (gironum COLLATE case_insensitive);
CREATE TABLE gc_jouhdr (
	datum DATE,
	refno CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	debit DECIMAL DEFAULT 0,
	credit DECIMAL DEFAULT 0,
	remain DECIMAL DEFAULT 0,
	jnr INT DEFAULT 0,
	activeflag INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gc_jouhdr_bezeich_ix ON gc_jouhdr (bezeich COLLATE case_insensitive,activeflag);
CREATE INDEX gc_jouhdr_datum_ix ON gc_jouhdr (datum,activeflag);
CREATE INDEX gc_jouhdr_jnr_ix ON gc_jouhdr (refno COLLATE case_insensitive,activeflag);
CREATE INDEX gc_jouhdr_ref_ix ON gc_jouhdr (refno COLLATE case_insensitive,datum,activeflag);
CREATE INDEX gc_jouhdr_refno_ix ON gc_jouhdr (refno COLLATE case_insensitive);
CREATE TABLE gc_journal (
	artnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	jnr INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	debit DECIMAL DEFAULT 0,
	credit DECIMAL DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	activeflag INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gc_journal_artnr_ix ON gc_journal (artnr,departement);
CREATE INDEX gc_journal_artnrflag_ix ON gc_journal (artnr,departement,activeflag);
CREATE INDEX gc_journal_jnr_ix ON gc_journal (jnr);
CREATE INDEX gc_journal_jnrflag_ix ON gc_journal (jnr,activeflag);
CREATE TABLE gc_PI (
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	docu_nr2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rcvID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rcvName CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	DeptNo INT DEFAULT 0,
	datum DATE,
	datum2 DATE,
	betrag DECIMAL DEFAULT 0,
	returnAmt DECIMAL DEFAULT 0,
	return_fibu CHARACTER VARYING COLLATE case_insensitive DEFAULT '000000000000',
	add_amt_flag BOOLEAN DEFAULT False,
	PI_type INT DEFAULT 0,
	PI_status INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	debit_fibu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	credit_fibu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	pay_type INT DEFAULT 1,
	pay_datum DATE,
	chequeNo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bankName CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dueDate DATE,
	PostDate DATE,
	created DATE,
	CID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	modified DATE,
	MID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	approved1 BOOLEAN[3] DEFAULT ARRAY[false,false,false],
	approved2 BOOLEAN[3] DEFAULT ARRAY[false,false,false],
	printed1 BOOLEAN DEFAULT False,
	printed1A BOOLEAN DEFAULT False,
	printed2 BOOLEAN DEFAULT False,
	printed2A BOOLEAN DEFAULT False,
	cancelDate DATE,
	cancelID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	cancelzeit INT DEFAULT 0,
	res_int INT[3] DEFAULT ARRAY[0,0,0],
	res_deci DECIMAL[3] DEFAULT ARRAY[0,0,0],
	res_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	res_logi BOOLEAN[3] DEFAULT ARRAY[false,false,false],
	bez_array CHARACTER VARYING [10] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','',''],
	amount_array DECIMAL[10] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX gc_PI_date_ix ON gc_PI (datum);
CREATE INDEX gc_PI_docu2_ix ON gc_PI (docu_nr2 COLLATE case_insensitive);
CREATE INDEX gc_PI_docu_ix ON gc_PI (docu_nr COLLATE case_insensitive);
CREATE INDEX gc_PI_name_ix ON gc_PI (rcvName COLLATE case_insensitive);
CREATE INDEX gc_PI_namedat_ix ON gc_PI (rcvName COLLATE case_insensitive,datum);
CREATE INDEX gc_PI_namestat_ix ON gc_PI (rcvName COLLATE case_insensitive,PI_status);
CREATE INDEX gc_PI_namstatdat_ix ON gc_PI (rcvName COLLATE case_insensitive,datum,PI_status);
CREATE INDEX gc_PI_status_ix ON gc_PI (PI_status);
CREATE TABLE gc_piacct (
	nr INT DEFAULT 0,
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gc_piacct_acct_ix ON gc_piacct (fibukonto COLLATE case_insensitive);
CREATE INDEX gc_piacct_bezeich_ix ON gc_piacct (bezeich COLLATE case_insensitive);
CREATE TABLE gc_PIbline (
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	supplier CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	invoice_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lief_nr INT DEFAULT 0,
	inv_acctNo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	inv_bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	inv_amount DECIMAL DEFAULT 0,
	inv_bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created DATE,
	zeit INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gc_PIbline_docu_ix ON gc_PIbline (docu_nr COLLATE case_insensitive);
CREATE TABLE gc_piType (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	activeflag INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gc_piType_bez_ix ON gc_piType (bezeich COLLATE case_insensitive);
CREATE INDEX gc_piType_nr_ix ON gc_piType (nr);
CREATE TABLE genfcast (
	datum DATE,
	gastnr INT DEFAULT 0,
	gastnrmember INT DEFAULT 0,
	ratecode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logis DECIMAL DEFAULT 0,
	zipreis DECIMAL DEFAULT 0,
	rateLocal DECIMAL DEFAULT 0,
	wahrungsnr INT DEFAULT 0,
	markno INT DEFAULT 0,
	erwachs INT DEFAULT 0,
	gratis INT DEFAULT 0,
	kind1 INT DEFAULT 0,
	kind2 INT DEFAULT 0,
	Kind3 INT DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	ankunft DATE,
	abreise DATE,
	cancelled DATE,
	noshow BOOLEAN DEFAULT False,
	spaetabreise BOOLEAN DEFAULT False,
	zikatnr INT DEFAULT 0,
	Argt CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	source INT DEFAULT 0,
	nationnr INT DEFAULT 0,
	resident INT DEFAULT 0,
	domestic INT DEFAULT 0,
	kontcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	karteityp INT DEFAULT 0,
	resstatus INT DEFAULT 0,
	sales_init CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	res_deci DECIMAL[5] DEFAULT ARRAY[0,0,0,0,0],
	res_int INT[5] DEFAULT ARRAY[0,0,0,0,0],
	res_logic BOOLEAN[5] DEFAULT ARRAY[false,false,false,false,false],
	res_char CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	res_date DATE[5] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	groupname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX genfcast_abreise_ix ON genfcast (abreise);
CREATE INDEX genfcast_datank_ix ON genfcast (datum,ankunft,abreise);
CREATE INDEX genfcast_datgastnr_ix ON genfcast (datum,gastnr);
CREATE INDEX genfcast_datresnr_ix ON genfcast (datum,resnr,reslinnr);
CREATE INDEX genfcast_datum_ix ON genfcast (datum);
CREATE TABLE genlayout (
	key CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	inte_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	deci_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	logi_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	date_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	char_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	activeflag BOOLEAN DEFAULT True,
	tinte_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	tdeci_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	tlogi_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	tdate_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	tchar_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	frame_title CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	frame_width DECIMAL DEFAULT 0,
	frame_height DECIMAL DEFAULT 0,
	canc_width DECIMAL DEFAULT 0,
	canc_height DECIMAL DEFAULT 0,
	exit_width DECIMAL DEFAULT 0,
	exit_height DECIMAL DEFAULT 0,
	add_width DECIMAL DEFAULT 0,
	add_height DECIMAL DEFAULT 0,
	del_width DECIMAL DEFAULT 0,
	del_height DECIMAL DEFAULT 0,
	string_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	button_ext CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	combo_ext CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	_recid serial PRIMARY KEY
);
CREATE INDEX genlayout_key_ix ON genlayout (key COLLATE case_insensitive);
CREATE TABLE genstat (
	datum DATE,
	gastnr INT DEFAULT 0,
	gastnrmember INT DEFAULT 0,
	logis DECIMAL DEFAULT 0,
	zipreis DECIMAL DEFAULT 0,
	rateLocal DECIMAL DEFAULT 0,
	wahrungsnr INT DEFAULT 0,
	erwachs INT DEFAULT 0,
	gratis INT DEFAULT 0,
	kind1 INT DEFAULT 0,
	kind2 INT DEFAULT 0,
	Kind3 INT DEFAULT 0,
	resnr INT DEFAULT 0,
	ankflag BOOLEAN DEFAULT False,
	zikatnr INT DEFAULT 0,
	Argt CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	source INT DEFAULT 0,
	nationnr INT DEFAULT 0,
	resident INT DEFAULT 0,
	domestic INT DEFAULT 0,
	kontcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	karteityp INT DEFAULT 0,
	resstatus INT DEFAULT 0,
	res_deci DECIMAL[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	res_int INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	res_logic BOOLEAN[9] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false],
	res_char CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	res_date DATE[9] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	_recid serial PRIMARY KEY
);
CREATE INDEX genstat_argt_ix ON genstat (datum,Argt COLLATE case_insensitive);
CREATE INDEX genstat_arrival_ix ON genstat (datum,ankflag);
CREATE INDEX genstat_date_ix ON genstat (datum);
CREATE INDEX genstat_domestic ON genstat (datum,domestic);
CREATE INDEX genstat_gastnr_ix ON genstat (datum,gastnrmember);
CREATE INDEX genstat_gastnrmem_ix ON genstat (datum,gastnrmember);
CREATE INDEX genstat_gastnrmember_ix ON genstat (datum,gastnrmember,zinr COLLATE case_insensitive);
CREATE INDEX genstat_kartei_ix ON genstat (datum,karteityp);
CREATE INDEX genstat_nat_ix ON genstat (datum,nationnr);
CREATE INDEX genstat_resident_ix ON genstat (datum,resident);
CREATE INDEX genstat_segm_ix ON genstat (datum,segmentcode);
CREATE INDEX genstat_source_ix ON genstat (datum,source);
CREATE INDEX genstat_zikat_ix ON genstat (datum,zikatnr);
CREATE TABLE gentable (
	key CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	inte_ext INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	deci_ext DECIMAL[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	logi_ext BOOLEAN[9] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false],
	date_ext DATE[9] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	char_ext CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	activeflag BOOLEAN DEFAULT True,
	combo_ext CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	_recid serial PRIMARY KEY
);
CREATE INDEX gentable_key_ix ON gentable (key COLLATE case_insensitive);
CREATE INDEX gentable_keychar2_ix ON gentable (key COLLATE case_insensitive,char1 COLLATE case_insensitive,char2 COLLATE case_insensitive);
CREATE INDEX gentable_keychar_ix ON gentable (key COLLATE case_insensitive,char1 COLLATE case_insensitive);
CREATE INDEX gentable_keynum_ix ON gentable (key COLLATE case_insensitive,number1,number2,number3);
CREATE TABLE gk_field (
	karteityp INT DEFAULT 0,
	Field_Name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	flag INT DEFAULT 0,
	Compulsory BOOLEAN DEFAULT False,
	Field_Column DECIMAL DEFAULT 0,
	Field_Row DECIMAL DEFAULT 0,
	Field_Height DECIMAL DEFAULT 1,
	Field_Width DECIMAL DEFAULT 0,
	Default_Width DECIMAL DEFAULT 0,
	Field_Order INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	label_pos INT DEFAULT 0,
	Updateable BOOLEAN DEFAULT False,
	feldtyp CHARACTER VARYING COLLATE case_insensitive DEFAULT 'fill-in',
	private_data CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX gk_field_active_ix ON gk_field (flag,karteityp,Field_Name COLLATE case_insensitive);
CREATE INDEX gk_field_name_ix ON gk_field (karteityp,Field_Name COLLATE case_insensitive);
CREATE INDEX gk_field_order_ix ON gk_field (karteityp,flag,Field_Order);
CREATE TABLE gk_label (
	karteityp INT DEFAULT 0,
	Field_Name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	language INT DEFAULT 0,
	Display_Name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Field_label CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Field_help CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Display_help CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gk_label_field_ix ON gk_label (language,karteityp,Field_Name COLLATE case_insensitive);
CREATE TABLE gk_notes (
	gastnr INT DEFAULT 0,
	page_nr INT DEFAULT 0,
	notes CHARACTER VARYING [18] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','',''],
	program INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	e_notes CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gk_notes_betr_notes_ix ON gk_notes (betriebsnr,program,gastnr,resnr,reslinnr,page_nr);
CREATE INDEX gk_notes_notes_index ON gk_notes (program,gastnr,resnr,reslinnr,page_nr);
CREATE TABLE gl_acct (
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000000000000',
	main_nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	b_flag BOOLEAN DEFAULT False,
	acc_type INT DEFAULT 0,
	actual DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fs_type INT DEFAULT 0,
	last_yr DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	budget DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	deptnr INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	c_date DATE,
	m_date DATE,
	modifiable BOOLEAN DEFAULT True,
	activeflag BOOLEAN DEFAULT False,
	ly_budget DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	debit DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	credit DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_acct_active_ix ON gl_acct (activeflag);
CREATE INDEX gl_acct_actype_ix ON gl_acct (main_nr);
CREATE INDEX gl_acct_bezeich_ix ON gl_acct (main_nr,bezeich COLLATE case_insensitive);
CREATE INDEX gl_acct_dept_ix ON gl_acct (deptnr);
CREATE INDEX gl_acct_dtype_ix ON gl_acct (deptnr);
CREATE INDEX gl_acct_fbactive_ix ON gl_acct (fibukonto COLLATE case_insensitive,activeflag);
CREATE INDEX gl_acct_fibu_ix ON gl_acct (fibukonto COLLATE case_insensitive);
CREATE INDEX gl_acct_fs_ix ON gl_acct (main_nr,fs_type);
CREATE INDEX gl_acct_mtype_ix ON gl_acct (main_nr,acc_type);
CREATE INDEX gl_acct_type_ix ON gl_acct (acc_type);
CREATE TABLE gl_accthis (
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000000000',
	main_nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	b_flag BOOLEAN DEFAULT False,
	acc_type INT DEFAULT 0,
	actual DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fs_type INT DEFAULT 0,
	last_yr DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	budget DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	deptnr INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	c_date DATE,
	m_date DATE,
	modifiable BOOLEAN DEFAULT True,
	activeflag BOOLEAN DEFAULT False,
	ly_budget DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	debit DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	credit DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	year INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_accthis_active_ix ON gl_accthis (activeflag);
CREATE INDEX gl_accthis_actype_ix ON gl_accthis (main_nr);
CREATE INDEX gl_accthis_bezeich_ix ON gl_accthis (main_nr,bezeich COLLATE case_insensitive);
CREATE INDEX gl_accthis_dept_ix ON gl_accthis (deptnr);
CREATE INDEX gl_accthis_dtype_ix ON gl_accthis (deptnr);
CREATE INDEX gl_accthis_fbactive_ix ON gl_accthis (fibukonto COLLATE case_insensitive,activeflag);
CREATE INDEX gl_accthis_fibu_ix ON gl_accthis (fibukonto COLLATE case_insensitive);
CREATE INDEX gl_accthis_fibuyear_ix ON gl_accthis (fibukonto COLLATE case_insensitive,year);
CREATE INDEX gl_accthis_fs_ix ON gl_accthis (main_nr,fs_type);
CREATE INDEX gl_accthis_mtype_ix ON gl_accthis (main_nr,acc_type);
CREATE INDEX gl_accthis_type_ix ON gl_accthis (acc_type);
CREATE INDEX gl_accthis_year_ix ON gl_accthis (year);
CREATE TABLE gl_coa (
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000000000',
	main_nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	b_flag BOOLEAN DEFAULT False,
	acc_type INT DEFAULT 0,
	actual DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fs_type INT DEFAULT 0,
	last_yr DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	budget DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	deptnr INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	c_date DATE,
	m_date DATE,
	modifiable BOOLEAN DEFAULT True,
	activeflag BOOLEAN DEFAULT False,
	ly_budget DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	debit DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	credit DECIMAL[12] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_coa_acct_ix ON gl_coa (fibukonto COLLATE case_insensitive,betriebsnr);
CREATE INDEX gl_coa_active_ix ON gl_coa (activeflag,betriebsnr);
CREATE INDEX gl_coa_dept_ix ON gl_coa (deptnr,betriebsnr);
CREATE INDEX gl_coa_main_ix ON gl_coa (main_nr,betriebsnr);
CREATE INDEX gl_coa_type_ix ON gl_coa (acc_type,betriebsnr);
CREATE TABLE gl_cost (
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	f_betrag DECIMAL DEFAULT 0,
	b_betrag DECIMAL DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_cost_date_ix ON gl_cost (datum);
CREATE INDEX gl_cost_fibu_ix ON gl_cost (fibukonto COLLATE case_insensitive,datum);
CREATE TABLE gl_department (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fodept INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_department_bezeich_ix ON gl_department (bezeich COLLATE case_insensitive);
CREATE INDEX gl_department_nr_ix ON gl_department (nr);
CREATE TABLE gl_fstype (
	nr INT DEFAULT 0,
	kurzbez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_fstype_nr_ix ON gl_fstype (nr);
CREATE TABLE gl_htljournal (
	htl_jnr INT DEFAULT 0,
	jnr INT DEFAULT 0,
	datum DATE,
	htl_license CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vstring CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_htljournal_htljnr_ix ON gl_htljournal (htl_jnr,htl_license COLLATE case_insensitive);
CREATE INDEX gl_htljournal_jnr_ix ON gl_htljournal (jnr);
CREATE INDEX gl_htljournal_licdate_ix ON gl_htljournal (htl_license COLLATE case_insensitive,datum);
CREATE TABLE gl_jhdrhis (
	datum DATE,
	refno CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	debit DECIMAL DEFAULT 0,
	credit DECIMAL DEFAULT 0,
	remain DECIMAL DEFAULT 0,
	jnr INT DEFAULT 0,
	jtype INT DEFAULT 0,
	activeflag INT DEFAULT 0,
	batch BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_jhdrhis_batch_ix ON gl_jhdrhis (activeflag,batch);
CREATE INDEX gl_jhdrhis_bezeich_ix ON gl_jhdrhis (bezeich COLLATE case_insensitive,activeflag);
CREATE INDEX gl_jhdrhis_datum_ix ON gl_jhdrhis (datum,activeflag);
CREATE INDEX gl_jhdrhis_datype_ix ON gl_jhdrhis (datum,jtype,activeflag,batch);
CREATE INDEX gl_jhdrhis_jnr_ix ON gl_jhdrhis (jnr,activeflag);
CREATE INDEX gl_jhdrhis_ref_ix ON gl_jhdrhis (refno COLLATE case_insensitive,datum,activeflag);
CREATE INDEX gl_jhdrhis_refno_ix ON gl_jhdrhis (refno COLLATE case_insensitive);
CREATE INDEX gl_jhdrhis_type_ix ON gl_jhdrhis (jtype,activeflag,batch);
CREATE TABLE gl_jouhdr (
	datum DATE,
	refno CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	debit DECIMAL DEFAULT 0,
	credit DECIMAL DEFAULT 0,
	remain DECIMAL DEFAULT 0,
	jnr INT DEFAULT 0,
	jtype INT DEFAULT 0,
	activeflag INT DEFAULT 0,
	batch BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_jouhdr_batch_ix ON gl_jouhdr (activeflag,batch);
CREATE INDEX gl_jouhdr_bezeich_ix ON gl_jouhdr (bezeich COLLATE case_insensitive,activeflag);
CREATE INDEX gl_jouhdr_datum_ix ON gl_jouhdr (datum,activeflag);
CREATE INDEX gl_jouhdr_datype_ix ON gl_jouhdr (datum,jtype,activeflag,batch);
CREATE INDEX gl_jouhdr_jnr_ix ON gl_jouhdr (jnr,activeflag);
CREATE INDEX gl_jouhdr_ref_ix ON gl_jouhdr (refno COLLATE case_insensitive,datum,activeflag);
CREATE INDEX gl_jouhdr_refno_ix ON gl_jouhdr (refno COLLATE case_insensitive);
CREATE INDEX gl_jouhdr_type_ix ON gl_jouhdr (jtype,activeflag,batch);
CREATE TABLE gl_jourhis (
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	jnr INT DEFAULT 0,
	debit DECIMAL DEFAULT 0,
	credit DECIMAL DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	activeflag INT DEFAULT 0,
	datum DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_jourhis_date_ix ON gl_jourhis (datum);
CREATE INDEX gl_jourhis_fibu_ix ON gl_jourhis (fibukonto COLLATE case_insensitive);
CREATE INDEX gl_jourhis_fibudate_ix ON gl_jourhis (fibukonto COLLATE case_insensitive,datum);
CREATE INDEX gl_jourhis_fibuflag_ix ON gl_jourhis (fibukonto COLLATE case_insensitive,activeflag);
CREATE INDEX gl_jourhis_jnr_ix ON gl_jourhis (jnr);
CREATE INDEX gl_jourhis_jnrflag_ix ON gl_jourhis (jnr,activeflag);
CREATE TABLE gl_journal (
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	jnr INT DEFAULT 0,
	debit DECIMAL DEFAULT 0,
	credit DECIMAL DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	activeflag INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_journal_fibu_ix ON gl_journal (fibukonto COLLATE case_insensitive);
CREATE INDEX gl_journal_fibuflag_ix ON gl_journal (fibukonto COLLATE case_insensitive,activeflag);
CREATE INDEX gl_journal_jnr_ix ON gl_journal (jnr);
CREATE INDEX gl_journal_jnrflag_ix ON gl_journal (jnr,activeflag);
CREATE TABLE gl_main (
	nr INT DEFAULT 0,
	code INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	type_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX gl_main_code_ix ON gl_main (code);
CREATE INDEX gl_main_nr_ix ON gl_main (nr);
CREATE INDEX gl_main_type_ix ON gl_main (type_code COLLATE case_insensitive);
CREATE TABLE golf_caddie (
	nr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nickname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gender CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	MaritalStatus INT DEFAULT 0,
	CaddieStatus INT DEFAULT 0,
	adresse1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	city CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zip CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	phone CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	email CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	birthdate DATE,
	startdate DATE,
	active BOOLEAN DEFAULT False,
	offdays BOOLEAN[7] DEFAULT ARRAY[false,false,false,false,false,false,false],
	bank_acct CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bank_no CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	chgid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	zeit INT DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_caddie_name_ix ON golf_caddie (name COLLATE case_insensitive);
CREATE INDEX golf_caddie_nr_ix ON golf_caddie (nr);
CREATE TABLE golf_caddie_assignment (
	caddie_nr INT DEFAULT 0,
	assignment_nr INT DEFAULT 0,
	user_init CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_caddie_assignment_assignmentnr_ix ON golf_caddie_assignment (assignment_nr);
CREATE TABLE golf_course (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	tt_start INT DEFAULT 0,
	tt_end INT DEFAULT 0,
	tt_interval INT DEFAULT 0,
	tot_hole INT DEFAULT 0,
	expected_duration INT DEFAULT 0,
	away_flag BOOLEAN DEFAULT False,
	avail_days BOOLEAN[9] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false],
	ip_addr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ip_port INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_course_nr_ix ON golf_course (nr);
CREATE TABLE golf_flight_reservation (
	groupnr INT DEFAULT 0,
	flightnr INT DEFAULT 0,
	datum DATE,
	booking_time INT DEFAULT 0,
	total_player INT DEFAULT 0,
	shiftnr INT DEFAULT 0,
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	teebox INT DEFAULT 0,
	extra_round BOOLEAN DEFAULT False,
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chg_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_changed DATE,
	zeit INT DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_flight_reservation_booking_time_ix ON golf_flight_reservation (booking_time,datum,groupnr,flightnr);
CREATE INDEX golf_flight_reservation_datum_ix ON golf_flight_reservation (datum,groupnr,flightnr,booking_time);
CREATE INDEX golf_flight_reservation_groupnr_ix ON golf_flight_reservation (groupnr,flightnr);
CREATE TABLE golf_flight_reservation_hist (
	groupnr INT DEFAULT 0,
	flightnr INT DEFAULT 0,
	datum DATE,
	booking_time INT DEFAULT 0,
	total_player INT DEFAULT 0,
	shiftnr INT DEFAULT 0,
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	teebox INT DEFAULT 0,
	extra_round BOOLEAN DEFAULT False,
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_changed DATE,
	zeit INT DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_flight_reservation_hist_booking_time_ix ON golf_flight_reservation_hist (booking_time,datum,groupnr,flightnr);
CREATE INDEX golf_flight_reservation_hist_datum_ix ON golf_flight_reservation_hist (datum,groupnr,flightnr,booking_time);
CREATE INDEX golf_flight_reservation_hist_groupnr_ix ON golf_flight_reservation_hist (groupnr,flightnr);
CREATE TABLE golf_golfer_reservation (
	groupnr INT DEFAULT 0,
	flightnr INT DEFAULT 0,
	golfernr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nr INT DEFAULT 0,
	member_flag BOOLEAN DEFAULT False,
	caddienr INT DEFAULT 0,
	caddienr2 INT DEFAULT 0,
	split_flag BOOLEAN DEFAULT False,
	bagnr INT DEFAULT 0,
	lockernr INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	artnr INT DEFAULT 0,
	accompanied BOOLEAN DEFAULT False,
	actual_status INT DEFAULT 0,
	register_time INT DEFAULT 0,
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_changed DATE,
	zeit INT DEFAULT 0,
	last_change_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_golfer_reservation_groupnr_ix ON golf_golfer_reservation (groupnr,flightnr,nr);
CREATE INDEX golf_golfer_reservation_member_flag_ix ON golf_golfer_reservation (member_flag,groupnr,flightnr,nr);
CREATE INDEX golf_golfer_reservation_nr_ix ON golf_golfer_reservation (nr,groupnr,flightnr);
CREATE TABLE golf_golfer_reservation_hist (
	groupnr INT DEFAULT 0,
	flightnr INT DEFAULT 0,
	golfernr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nr INT DEFAULT 0,
	member_flag BOOLEAN DEFAULT False,
	caddienr INT DEFAULT 0,
	caddienr2 INT DEFAULT 0,
	split_flag BOOLEAN DEFAULT False,
	bagnr INT DEFAULT 0,
	lockernr INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	artnr INT DEFAULT 0,
	accompanied BOOLEAN DEFAULT False,
	actual_status INT DEFAULT 0,
	register_time INT DEFAULT 0,
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_changed DATE,
	zeit INT DEFAULT 0,
	last_change_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_golfer_reservation_hist_groupnr_ix ON golf_golfer_reservation_hist (groupnr,flightnr,nr);
CREATE INDEX golf_golfer_reservation_hist_member_flag_ix ON golf_golfer_reservation_hist (member_flag,groupnr,flightnr,nr);
CREATE INDEX golf_golfer_reservation_hist_nr_ix ON golf_golfer_reservation_hist (nr,groupnr,flightnr);
CREATE TABLE golf_holiday (
	datum DATE,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	every_year BOOLEAN DEFAULT False,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	chgid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	zeit INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_holiday_datum_ix ON golf_holiday (datum);
CREATE TABLE golf_main_reservation (
	groupnr INT DEFAULT 0,
	member_join BOOLEAN DEFAULT False,
	course_nr INT DEFAULT 0,
	reserve_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	contact_no CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	total_flight INT DEFAULT 0,
	total_player INT DEFAULT 0,
	memberid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	new_memberid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	noshow_hb BOOLEAN DEFAULT False,
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_date DATE,
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_changed DATE,
	zeit INT DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_main_reservation_group_nr_ix ON golf_main_reservation (groupnr);
CREATE TABLE golf_main_reservation_hist (
	groupnr INT DEFAULT 0,
	member_join BOOLEAN DEFAULT False,
	course_nr INT DEFAULT 0,
	reserve_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	contact_no CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	total_flight INT DEFAULT 0,
	total_player INT DEFAULT 0,
	memberid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	new_memberid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	noshow_hb BOOLEAN DEFAULT False,
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_date DATE,
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_changed DATE,
	zeit INT DEFAULT 0,
	int1 INT DEFAULT 0,
	int2 INT DEFAULT 0,
	int3 INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	dec1 DECIMAL DEFAULT 0,
	dec2 DECIMAL DEFAULT 0,
	dec3 DECIMAL DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_main_reservation_hist_group_nr_ix ON golf_main_reservation_hist (groupnr);
CREATE TABLE golf_rate (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	shiftnr INT DEFAULT 0,
	member_flag BOOLEAN DEFAULT False,
	member_join BOOLEAN DEFAULT False,
	extra_round BOOLEAN DEFAULT False,
	day_list BOOLEAN[8] DEFAULT ARRAY[false,false,false,false,false,false,false,false],
	from_date DATE,
	to_date DATE,
	artnr INT DEFAULT 0,
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	chgdate DATE,
	zeit INT DEFAULT 0,
	chgid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_rate_nr_ix ON golf_rate (nr);
CREATE TABLE golf_shift (
	shiftnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	from_time INT DEFAULT 0,
	to_time INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	chginit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	zeit INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_shift_shift_nr_ix ON golf_shift (shiftnr);
CREATE TABLE golf_transfer (
	groupnr INT DEFAULT 0,
	flight_nr INT DEFAULT 0,
	golfer_nr INT DEFAULT 0,
	golfer_gastnr INT DEFAULT 0,
	from_date DATE,
	to_date DATE,
	from_time INT DEFAULT 0,
	to_time INT DEFAULT 0,
	from_teebox INT DEFAULT 0,
	to_teebox INT DEFAULT 0,
	from_flight INT DEFAULT 0,
	to_flight INT DEFAULT 0,
	to_groupnr INT DEFAULT 0,
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	transfer_type INT DEFAULT 0,
	usrid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zeit INT DEFAULT 0,
	to_golfernr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX golf_transfer_groupnr_ix ON golf_transfer (groupnr,flight_nr,golfer_nr);
CREATE TABLE guest (
	gastnr INT DEFAULT 0,
	karteityp INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anredefirma CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	namekontakt CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorname1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorname2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anrede1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anrede2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	land CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	plz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	wohnort CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nation1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nation2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	beruf CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ausweis_art CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ausweis_nr1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ausweis_nr2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	geburtdatum1 DATE,
	geburtdatum2 DATE,
	geburt_ort1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	geburt_ort2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	interessen CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	autonr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	pass_aust1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	pass_aust2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	geburtkind DATE[6] DEFAULT ARRAY[NULL::date,NULL::date,NULL::date,NULL::date,NULL::date,NULL::date],
	vornamekind CHARACTER VARYING [6] COLLATE case_insensitive DEFAULT ARRAY['','','','','',''],
	aufenthalte INT DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	logiernachte INT DEFAULT 0,
	stornos INT DEFAULT 0,
	noshows INT DEFAULT 0,
	erstaufent DATE,
	zahlungsart INT DEFAULT 0,
	kreditlimit_old INT DEFAULT 0,
	segment1 INT DEFAULT 0,
	segment2 INT DEFAULT 0,
	segment3 INT DEFAULT 0,
	adresse1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	cardnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gesamtumsatz_old INT DEFAULT 0,
	fax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telex CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anlage_datum DATE,
	modif_datum DATE,
	trans_datum DATE,
	preis_einzel DECIMAL DEFAULT 0,
	argt_einzel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	preis_doppel DECIMAL DEFAULT 0,
	argt_doppel CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rabatt DECIMAL DEFAULT 0,
	zimmer_min INT DEFAULT 0,
	logier_min INT DEFAULT 0,
	startperiode DATE,
	endperiode DATE,
	erste_res DATE,
	letzte_res DATE,
	naechste_res DATE,
	kontaktdat DATE,
	notizen CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	logisumsatz DECIMAL DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	com_logis DECIMAL DEFAULT 0,
	com_argt DECIMAL DEFAULT 0,
	com_f_b DECIMAL DEFAULT 0,
	com_sonst DECIMAL DEFAULT 0,
	resflag INT DEFAULT 0,
	credablauf DATE,
	geschlecht CHARACTER VARYING COLLATE case_insensitive DEFAULT 'M',
	startkur CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000',
	endkur CHARACTER VARYING COLLATE case_insensitive DEFAULT '0000',
	sprachcode INT DEFAULT 1,
	groesse INT DEFAULT 0,
	gewicht INT DEFAULT 0,
	massnr INT DEFAULT 0,
	geschlecht2 CHARACTER VARYING COLLATE case_insensitive DEFAULT 'W',
	groesse2 INT DEFAULT 0,
	gewicht2 INT DEFAULT 0,
	massnr2 INT DEFAULT 0,
	mahnsperre INT DEFAULT 0,
	blumen BOOLEAN DEFAULT False,
	champagner BOOLEAN DEFAULT False,
	arzt1 INT DEFAULT 0,
	arzt2 INT DEFAULT 0,
	point_gastnr INT DEFAULT 0,
	tv_see_bill BOOLEAN DEFAULT True,
	tv_checkout BOOLEAN DEFAULT True,
	tv_pay BOOLEAN DEFAULT True,
	betriebsnr INT DEFAULT 0,
	steuernr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	finanzamt CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	master_gastnr INT DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	kreditlimit DECIMAL DEFAULT 0,
	firmen_nr INT DEFAULT 0,
	phonetik1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	phonetik2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	phonetik3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	briefanrede CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mobil_telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	email_adr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	letzte_abreise DATE,
	vorname_haupt CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telefon_privat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sternzeichen CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betrieb_gastmaster INT DEFAULT 0,
	betrieb_gastpoint INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX guest_betr_nr_ix ON guest (betriebsnr,gastnr);
CREATE INDEX guest_firmennr_ix ON guest (firmen_nr);
CREATE INDEX guest_ganame_index ON guest (name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE INDEX guest_gast_master_ix ON guest (master_gastnr);
CREATE INDEX guest_gastnr_index ON guest (gastnr);
CREATE INDEX guest_ort_ix ON guest (wohnort COLLATE case_insensitive,land COLLATE case_insensitive,plz COLLATE case_insensitive,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE INDEX guest_phon1_ix ON guest (phonetik1 COLLATE case_insensitive);
CREATE INDEX guest_phon2_ix ON guest (phonetik2 COLLATE case_insensitive);
CREATE INDEX guest_phon3_ix ON guest (phonetik3 COLLATE case_insensitive);
CREATE INDEX guest_plz_ix ON guest (betriebsnr,land COLLATE case_insensitive,plz COLLATE case_insensitive,name COLLATE case_insensitive,gastnr);
CREATE INDEX guest_point_index ON guest (point_gastnr);
CREATE INDEX guest_res_index ON guest (resflag,name COLLATE case_insensitive);
CREATE INDEX guest_strasse_ix ON guest (adresse1 COLLATE case_insensitive);
CREATE INDEX guest_telefon_ix ON guest (telefon COLLATE case_insensitive,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE INDEX guest_typ_wohn_name_ix ON guest (karteityp,wohnort COLLATE case_insensitive,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE INDEX guest_typenam_ix ON guest (karteityp,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE INDEX guest_typeort_ix ON guest (karteityp,wohnort COLLATE case_insensitive,land COLLATE case_insensitive,plz COLLATE case_insensitive,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE INDEX guest_typeplz_ix ON guest (karteityp,land COLLATE case_insensitive,plz COLLATE case_insensitive,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive);
CREATE INDEX guest_typetelefon_ix ON guest (karteityp,telefon COLLATE case_insensitive,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE INDEX guest_typevorname_ix ON guest (karteityp,vorname1 COLLATE case_insensitive,name COLLATE case_insensitive,gastnr);
CREATE INDEX guest_vorname_ix ON guest (vorname1 COLLATE case_insensitive,name COLLATE case_insensitive,gastnr);
CREATE INDEX guest_wohn_name_ix ON guest (wohnort COLLATE case_insensitive,name COLLATE case_insensitive,vorname1 COLLATE case_insensitive,gastnr);
CREATE TABLE guest_pr (
	gastnr INT DEFAULT 0,
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kurzbez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX guest_pr_guest_pr_ix ON guest_pr (gastnr,code COLLATE case_insensitive,kurzbez COLLATE case_insensitive);
CREATE TABLE guest_queasy (
	betriebsnr INT DEFAULT 0,
	key CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gastnr INT DEFAULT 0,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX guest_queasy_b_char_ix ON guest_queasy (betriebsnr,key COLLATE case_insensitive,char1 COLLATE case_insensitive,number1,date1,deci1,logi1,char2 COLLATE case_insensitive);
CREATE INDEX guest_queasy_b_date_ix ON guest_queasy (betriebsnr,key COLLATE case_insensitive,date1,char1 COLLATE case_insensitive,number1,deci1,logi1,date2);
CREATE INDEX guest_queasy_b_deci_ix ON guest_queasy (betriebsnr,key COLLATE case_insensitive,deci1,number1,date1,logi1,char1 COLLATE case_insensitive,deci2);
CREATE INDEX guest_queasy_b_g_char_ix ON guest_queasy (betriebsnr,gastnr,key COLLATE case_insensitive,char1 COLLATE case_insensitive,logi1,deci1,date1,number1,char2 COLLATE case_insensitive,char3 COLLATE case_insensitive);
CREATE INDEX guest_queasy_b_g_chr2_ix ON guest_queasy (betriebsnr,gastnr,key COLLATE case_insensitive,char2 COLLATE case_insensitive,number2,deci2,logi2,date2);
CREATE INDEX guest_queasy_b_g_date_ix ON guest_queasy (betriebsnr,gastnr,key COLLATE case_insensitive,date1,char1 COLLATE case_insensitive,number1,deci1,logi1,date2);
CREATE INDEX guest_queasy_b_g_deci_ix ON guest_queasy (betriebsnr,gastnr,key COLLATE case_insensitive,deci1,logi1,date1,number1,char1 COLLATE case_insensitive,deci2);
CREATE INDEX guest_queasy_b_g_int_ix ON guest_queasy (betriebsnr,gastnr,key COLLATE case_insensitive,number1,date1,char1 COLLATE case_insensitive,deci1,logi1);
CREATE INDEX guest_queasy_b_g_logi_ix ON guest_queasy (betriebsnr,gastnr,key COLLATE case_insensitive,logi1,char1 COLLATE case_insensitive,deci1,date1,number1,logi2);
CREATE INDEX guest_queasy_b_int_ix ON guest_queasy (betriebsnr,key COLLATE case_insensitive,number1,date1,char1 COLLATE case_insensitive,deci1,logi1);
CREATE INDEX guest_queasy_b_logi_ix ON guest_queasy (betriebsnr,key COLLATE case_insensitive,logi1,char1 COLLATE case_insensitive,date1,number1,deci1,logi2);
CREATE TABLE guest_remark (
	gastnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	codenum INT DEFAULT 0,
	datum DATE,
	zeit INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	CID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	chgtime INT DEFAULT 0,
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	display_flag BOOLEAN DEFAULT False,
	res_integer INT[3] DEFAULT ARRAY[0,0,0],
	res_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	_recid serial PRIMARY KEY
);
CREATE INDEX guest_remark_gastcode_ix ON guest_remark (gastnr,codenum);
CREATE INDEX guest_remark_gastdate_ix ON guest_remark (gastnr,datum);
CREATE INDEX guest_remark_gastdisp_ix ON guest_remark (gastnr,display_flag);
CREATE INDEX guest_remark_gastnr_ix ON guest_remark (gastnr);
CREATE INDEX guest_remark_gastresnr_ix ON guest_remark (gastnr,resnr,reslinnr);
CREATE TABLE guestat (
	gastnr INT DEFAULT 0,
	jahr INT DEFAULT 0,
	monat INT DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	logisumsatz DECIMAL DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	room_nights INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX guestat_gastnr_ix ON guestat (gastnr,monat,jahr);
CREATE TABLE guestat1 (
	gastnr INT DEFAULT 0,
	datum DATE,
	logis DECIMAL DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	persanz INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX guestat1_date_ix ON guestat1 (datum);
CREATE INDEX guestat1_gast_ix ON guestat1 (gastnr,datum);
CREATE TABLE guestbook (
	gastnr INT DEFAULT 0,
	imagefile BYTEA,
	infostr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created DATE,
	zeit INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	orig_infostr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	changed DATE,
	CID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	reserve_int INT[3] DEFAULT ARRAY[0,0,0],
	reserve_logic BOOLEAN[3] DEFAULT ARRAY[false,false,false],
	_recid serial PRIMARY KEY
);
CREATE INDEX guestbook_date_ix ON guestbook (created);
CREATE INDEX guestbook_gastdat_ix ON guestbook (gastnr,created,zeit);
CREATE INDEX guestbook_gastnr_ix ON guestbook (gastnr);
CREATE TABLE guestbud (
	gastnr INT DEFAULT 0,
	jahr INT DEFAULT 0,
	monat INT DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	logisumsatz DECIMAL DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	room_nights INT DEFAULT 0,
	bed_nights INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	tag INT DEFAULT 0,
	bis_tag INT DEFAULT 0,
	bis_monat INT DEFAULT 0,
	bis_jahr INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX guestbud_betr_gastnr_ix ON guestbud (betriebsnr,gastnr,jahr,monat,tag);
CREATE INDEX guestbud_guestbud_ix ON guestbud (gastnr,jahr,monat);
CREATE TABLE guestseg (
	gastnr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	reihenfolge INT DEFAULT 0,
	datum DATE,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX guestseg_betr_gastnr_ix ON guestseg (betriebsnr,gastnr,segmentcode,reihenfolge);
CREATE INDEX guestseg_gastnr_ix ON guestseg (gastnr,segmentcode,reihenfolge);
CREATE INDEX guestseg_segment_ix ON guestseg (segmentcode,gastnr);
CREATE TABLE h_artcost (
	artnr INT DEFAULT 0,
	datum DATE,
	cost DECIMAL[31] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	lm_cost DECIMAL[31] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	anzahl DECIMAL[31] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	lm_anzahl DECIMAL[31] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_artcost_art_ix ON h_artcost (artnr);
CREATE TABLE h_artikel (
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zwkum INT DEFAULT 0,
	endkum INT DEFAULT 0,
	epreis1 DECIMAL DEFAULT 0,
	artart INT DEFAULT 0,
	autosaldo BOOLEAN DEFAULT False,
	bezaendern BOOLEAN DEFAULT False,
	mwst_code INT DEFAULT 0,
	prozent DECIMAL DEFAULT 0,
	epreis2 DECIMAL DEFAULT 0,
	lagernr INT DEFAULT 0,
	abbuchung INT DEFAULT 0,
	bondruckernr INT[4] DEFAULT ARRAY[0,0,0,0],
	aenderwunsch BOOLEAN DEFAULT False,
	artnrfront INT DEFAULT 0,
	artnrlager INT DEFAULT 0,
	artnrrezept INT DEFAULT 0,
	gang INT DEFAULT 0,
	service_code INT DEFAULT 0,
	activeflag BOOLEAN DEFAULT False,
	s_gueltig DATE,
	e_gueltig DATE,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_artikel_art_index ON h_artikel (artnr);
CREATE INDEX h_artikel_artbez_ix ON h_artikel (departement,bezeich COLLATE case_insensitive);
CREATE INDEX h_artikel_artgrp_ix ON h_artikel (departement,zwkum,bezeich COLLATE case_insensitive);
CREATE INDEX h_artikel_depart_index ON h_artikel (departement,artnr);
CREATE INDEX h_artikel_lagerart_ix ON h_artikel (artnrlager);
CREATE INDEX h_artikel_rezeptnr_ix ON h_artikel (artnrrezept);
CREATE TABLE h_bill (
	tischnr INT DEFAULT 0,
	flag INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	rgdruck INT DEFAULT 0,
	billnr INT DEFAULT 1,
	reslinnr INT DEFAULT 1,
	bilname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	kellner_nr INT DEFAULT 0,
	belegung INT DEFAULT 0,
	departement INT DEFAULT 0,
	service DECIMAL[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	mwst DECIMAL[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	resnr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_bill_billnr_ix ON h_bill (tischnr,billnr);
CREATE INDEX h_bill_dept1_ix ON h_bill (flag,departement,kellner_nr);
CREATE INDEX h_bill_dept_ix ON h_bill (flag,departement);
CREATE INDEX h_bill_rechnr_ix ON h_bill (rechnr);
CREATE INDEX h_bill_tableflag_ix ON h_bill (tischnr,flag);
CREATE TABLE h_bill_line (
	rechnr INT DEFAULT 0,
	bill_datum DATE,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	steuercode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fremdwbetrag DECIMAL DEFAULT 0,
	zeit INT DEFAULT 0,
	waehrungsnr INT DEFAULT 0,
	sysdate DATE,
	departement INT DEFAULT 0,
	prtflag INT DEFAULT 0,
	tischnr INT DEFAULT 0,
	kellner_nr INT DEFAULT 0,
	nettobetrag DECIMAL DEFAULT 0,
	paid_flag INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	transferred BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_bill_line_bildat_index ON h_bill_line (rechnr,bill_datum,zeit);
CREATE INDEX h_bill_line_rechnr_index ON h_bill_line (rechnr,sysdate,zeit);
CREATE TABLE h_compli (
	datum DATE,
	departement INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	p_artnr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_compli_artdat_ix ON h_compli (datum,departement,artnr);
CREATE INDEX h_compli_dat_ix ON h_compli (datum);
CREATE INDEX h_compli_datdept_ix ON h_compli (datum,departement);
CREATE TABLE h_cost (
	datum DATE,
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	flag INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_cost_cost_index ON h_cost (datum,departement,artnr,flag);
CREATE INDEX h_cost_date_ix ON h_cost (datum);
CREATE TABLE h_journal (
	rechnr INT DEFAULT 0,
	bill_datum DATE,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	steuercode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	zeit INT DEFAULT 0,
	waehrungcode INT DEFAULT 0,
	stornogrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	waehrungsnr INT DEFAULT 0,
	wabkurz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ankauf DECIMAL DEFAULT 0,
	verkauf DECIMAL DEFAULT 0,
	fremdwaehrng DECIMAL DEFAULT 0,
	sysdate DATE,
	tischnr INT DEFAULT 0,
	artnrlager INT DEFAULT 0,
	artnrfront INT DEFAULT 0,
	aendertext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gang INT DEFAULT 0,
	trinkgeld DECIMAL DEFAULT 0,
	bondruckernr INT DEFAULT 0,
	artart INT DEFAULT 0,
	bon_nr INT DEFAULT 0,
	endbon INT DEFAULT 0,
	prtflag INT DEFAULT 0,
	kellner_nr INT DEFAULT 0,
	artnrrezept INT DEFAULT 0,
	buchflag INT DEFAULT 0,
	lager_nr INT DEFAULT 0,
	schankbuch INT DEFAULT 0,
	nachbuchen BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	steuer_percent DECIMAL DEFAULT 0,
	service_code INT DEFAULT 0,
	service_percent DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_journal_bondruck_ix ON h_journal (prtflag,bon_nr,endbon,gang);
CREATE INDEX h_journal_chrono_ix ON h_journal (bill_datum,sysdate,zeit);
CREATE INDEX h_journal_kellner_ix ON h_journal (bill_datum,departement,kellner_nr,zeit);
CREATE INDEX h_journal_nachbuch_ix ON h_journal (nachbuchen);
CREATE INDEX h_journal_segment_ix ON h_journal (bill_datum,departement,segmentcode,zeit);
CREATE TABLE h_menu (
	departement INT DEFAULT 0,
	nr INT DEFAULT 0,
	artnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_menu_artnr_ix ON h_menu (departement,nr,artnr);
CREATE INDEX h_menu_nr_ix ON h_menu (departement,nr);
CREATE TABLE h_mjourn (
	departement INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	nr INT DEFAULT 0,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	h_artnr INT DEFAULT 0,
	zeit INT DEFAULT 0,
	request CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	bill_datum DATE,
	kellner_nr INT DEFAULT 0,
	tischnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_mjourn_date_ix ON h_mjourn (bill_datum);
CREATE INDEX h_mjourn_deptdate_ix ON h_mjourn (departement,bill_datum);
CREATE INDEX h_mjourn_h_art_ix ON h_mjourn (departement,rechnr,h_artnr,bill_datum,sysdate,zeit);
CREATE INDEX h_mjourn_rechart_ix ON h_mjourn (departement,rechnr,h_artnr,artnr,zeit);
CREATE TABLE h_oldjou (
	rechnr INT DEFAULT 0,
	bill_datum DATE,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	steuercode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	zeit INT DEFAULT 0,
	waehrungcode INT DEFAULT 0,
	stornogrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	waehrungsnr INT DEFAULT 0,
	wabkurz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ankauf DECIMAL DEFAULT 0,
	verkauf DECIMAL DEFAULT 0,
	fremdwaehrng DECIMAL DEFAULT 0,
	sysdate DATE,
	tischnr INT DEFAULT 0,
	artnrlager INT DEFAULT 0,
	artnrfront INT DEFAULT 0,
	aendertext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gang INT DEFAULT 0,
	trinkgeld DECIMAL DEFAULT 0,
	bondruckernr INT DEFAULT 0,
	artart INT DEFAULT 0,
	bon_nr INT DEFAULT 0,
	endbon INT DEFAULT 0,
	prtflag INT DEFAULT 0,
	kellner_nr INT DEFAULT 0,
	artnrrezept INT DEFAULT 0,
	buchflag INT DEFAULT 0,
	lager_nr INT DEFAULT 0,
	schankbuch INT DEFAULT 0,
	nachbuchen BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	steuer_percent DECIMAL DEFAULT 0,
	service_code INT DEFAULT 0,
	service_percent DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_oldjou_chrono_ix ON h_oldjou (bill_datum,sysdate,zeit);
CREATE INDEX h_oldjou_kellner_ix ON h_oldjou (bill_datum,departement,kellner_nr,zeit);
CREATE INDEX h_oldjou_nachbuch_ix ON h_oldjou (nachbuchen);
CREATE INDEX h_oldjou_segment_ix ON h_oldjou (bill_datum,departement,segmentcode,zeit);
CREATE TABLE h_order (
	order_nr INT DEFAULT 0,
	bill_datum DATE,
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	request CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_int INT[3] DEFAULT ARRAY[0,0,0],
	reserve_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	order_flag BOOLEAN DEFAULT False,
	cancelanz INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	zeit2 INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_order_order_ix ON h_order (order_nr,departement);
CREATE INDEX h_order_orderflag_date_ix ON h_order (order_nr,bill_datum,departement,order_flag);
CREATE INDEX h_order_orderflag_ix ON h_order (order_nr,departement,order_flag);
CREATE TABLE h_queasy (
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	billno INT DEFAULT 0,
	datum DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_queasy_date_ix ON h_queasy (datum);
CREATE INDEX h_queasy_num1_ix ON h_queasy (number1);
CREATE INDEX h_queasy_num_ix ON h_queasy (number1,number2,billno);
CREATE TABLE h_rezept (
	artnrrezept INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kategorie INT DEFAULT 0,
	portion INT DEFAULT 1,
	datumanlage DATE,
	datummod DATE,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_rezept_bezeich_ix ON h_rezept (bezeich COLLATE case_insensitive);
CREATE INDEX h_rezept_kategorie_ix ON h_rezept (kategorie,bezeich COLLATE case_insensitive);
CREATE INDEX h_rezept_rezeptnr_ix ON h_rezept (artnrrezept);
CREATE TABLE h_rezlin (
	artnrrezept INT DEFAULT 0,
	artnrlager INT DEFAULT 0,
	menge DECIMAL DEFAULT 0,
	lostfact DECIMAL DEFAULT 0,
	recipe_flag BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_rezlin_lagerart_ix ON h_rezlin (artnrlager);
CREATE INDEX h_rezlin_rezeptnr_ix ON h_rezlin (artnrrezept);
CREATE TABLE h_storno (
	rechnr INT DEFAULT 0,
	bill_datum DATE,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	steuercode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	zeit INT DEFAULT 0,
	waehrungcode INT DEFAULT 0,
	stornogrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	waehrungsnr INT DEFAULT 0,
	sysdate DATE,
	tischnr INT DEFAULT 0,
	artnrfront INT DEFAULT 0,
	aendertext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	trinkgeld DECIMAL DEFAULT 0,
	artart INT DEFAULT 0,
	kellner_nr INT DEFAULT 0,
	buchflag INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_storno_chrono_ix ON h_storno (departement,sysdate,zeit);
CREATE INDEX h_storno_dep_art_ix ON h_storno (departement,artnr,sysdate,zeit);
CREATE INDEX h_storno_kellner_ix ON h_storno (departement,kellner_nr,sysdate,zeit);
CREATE TABLE h_umsatz (
	datum DATE,
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	epreis DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	nettobetrag DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX h_umsatz_hrartatz_ix ON h_umsatz (artnr,departement,datum,epreis);
CREATE INDEX h_umsatz_hrumsatz_ix ON h_umsatz (datum,departement,artnr,epreis);
CREATE INDEX h_umsatz_hrumsdat_ix ON h_umsatz (departement,artnr,datum,epreis);
CREATE TABLE history (
	gastnr INT DEFAULT 0,
	ankunft DATE,
	abreise DATE,
	zimmeranz INT DEFAULT 0,
	zikateg CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	erwachs INT DEFAULT 0,
	kind INT[2] DEFAULT ARRAY[0,0],
	gratis INT DEFAULT 0,
	zipreis DECIMAL DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '000',
	gesamtumsatz DECIMAL DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logisumsatz DECIMAL DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	gastinfo CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zahlungsart INT DEFAULT 0,
	com_logis DECIMAL DEFAULT 0,
	com_argt DECIMAL DEFAULT 0,
	com_f_b DECIMAL DEFAULT 0,
	com_sonst DECIMAL DEFAULT 0,
	guestnrcom INT DEFAULT 0,
	abreisezeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segmentcode INT DEFAULT 0,
	zi_wechsel BOOLEAN DEFAULT False,
	resnr INT DEFAULT 0,
	ums_kurz DECIMAL DEFAULT 0,
	ums_lang DECIMAL DEFAULT 0,
	reslinnr INT DEFAULT 1,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX history_betr_hist_ix ON history (betriebsnr,gastnr,ankunft);
CREATE INDEX history_hist_index ON history (gastnr,abreise);
CREATE INDEX history_res_ix ON history (resnr,reslinnr);
CREATE TABLE hoteldpt (
	num INT DEFAULT 0,
	depart CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	defult BOOLEAN DEFAULT False,
	Bankettfsnr INT DEFAULT 0,
	Tagungfsnr INT DEFAULT 0,
	Bankettp2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Bankettp3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Bankettp4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Tagungp2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Tagungp3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Tagungp4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Departtyp INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	konto_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX hoteldpt_betr_num_ix ON hoteldpt (betriebsnr,num);
CREATE INDEX hoteldpt_depart ON hoteldpt (depart COLLATE case_insensitive);
CREATE INDEX hoteldpt_num ON hoteldpt (num);
CREATE TABLE hrbeleg (
	datum DATE,
	intervall INT DEFAULT 0,
	couverts100 INT DEFAULT 0,
	couverts_eff INT DEFAULT 0,
	tischbel100 INT DEFAULT 0,
	tischbel_eff INT DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	umsatzanw DECIMAL DEFAULT 0,
	departement INT DEFAULT 0,
	hour INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX hrbeleg_hour_ix ON hrbeleg (datum,departement,intervall,hour);
CREATE TABLE hrsegement (
	datum DATE,
	segmentcode INT DEFAULT 0,
	couverts_eff INT DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	tischanz INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX hrsegement_hrseg_ix ON hrsegement (datum,segmentcode);
CREATE TABLE htparam (
	paramnr INT DEFAULT 0,
	paramgruppe INT DEFAULT 0,
	reihenfolge INT DEFAULT 0,
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	feldtyp INT DEFAULT 0,
	finteger INT DEFAULT 0,
	fdecimal DECIMAL DEFAULT 0,
	fdate DATE,
	flogical BOOLEAN DEFAULT False,
	fchar CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lupdate DATE,
	fdefault CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	htp_help CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX htparam_betr_group_ix ON htparam (betriebsnr,paramgruppe,reihenfolge);
CREATE INDEX htparam_betr_nr_ix ON htparam (betriebsnr,paramnr);
CREATE INDEX htparam_group_ix ON htparam (paramgruppe,reihenfolge);
CREATE INDEX htparam_paramnr_ix ON htparam (paramnr);
CREATE TABLE htreport (
	repnr INT DEFAULT 0,
	sprache INT DEFAULT 0,
	libpath CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Libname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Repname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	conparam CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	wintitle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX htreport_PK ON htreport (repnr,sprache);
CREATE TABLE iftable (
	waiter_id INT DEFAULT 0,
	credit_nr INT[5] DEFAULT ARRAY[0,0,0,0,0],
	departement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mwst INT[5] DEFAULT ARRAY[0,0,0,0,0],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX iftable_waiter_id_ix ON iftable (waiter_id);
CREATE TABLE interface (
	key INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '1',
	nebenstelle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	action BOOLEAN DEFAULT False,
	parameters CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	intfield INT DEFAULT 0,
	decfield DECIMAL DEFAULT 0,
	intdate DATE,
	int_time INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	zinr_old CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX interface_key_date_time ON interface (key,intdate,int_time);
CREATE INDEX interface_key_nebenst_ix ON interface (key,nebenstelle COLLATE case_insensitive,parameters COLLATE case_insensitive,action,intfield,decfield,zinr COLLATE case_insensitive);
CREATE INDEX interface_key_zinr_ix ON interface (key,zinr COLLATE case_insensitive,nebenstelle COLLATE case_insensitive,parameters COLLATE case_insensitive,action);
CREATE TABLE k_history (
	gastnr INT DEFAULT 0,
	resnr INT DEFAULT 0,
	from_date DATE,
	to_date DATE,
	info1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	info2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Treatment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	comment CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gwish CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	doctor_adv CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	diet_adv CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX k_history_gasdate_ix ON k_history (gastnr,from_date,to_date);
CREATE INDEX k_history_gasres_ix ON k_history (gastnr,resnr);
CREATE INDEX k_history_gastnr_ix ON k_history (gastnr);
CREATE INDEX k_history_resnr_ix ON k_history (resnr);
CREATE TABLE kabine (
	kabnr INT DEFAULT 0,
	kabbez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	offenab CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	offenbis CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	pauseab CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	pausebis CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	massnr INT DEFAULT 0,
	anzpers INT DEFAULT 1,
	gesperrt BOOLEAN DEFAULT False,
	grund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	oooab CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	ooobis CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	fdate DATE,
	tdate DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX kabine_kabnr_ix ON kabine (kabnr);
CREATE TABLE kalender (
	dept CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	note CHARACTER VARYING [19] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','',''],
	datum DATE,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kalender_kalender_ix ON kalender (dept COLLATE case_insensitive,datum);
CREATE TABLE kasse (
	kassen_nr INT DEFAULT 0,
	kassenbez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kland CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kplz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kwohnort CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kadresse1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kadresse2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ktelefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	artnr INT DEFAULT 0,
	preiskat INT DEFAULT 0,
	kgastnr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gastk INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kasse_kass_bez_ix ON kasse (kassenbez COLLATE case_insensitive,kwohnort COLLATE case_insensitive);
CREATE INDEX kasse_kassen_nr_ix ON kasse (kassen_nr);
CREATE TABLE katpreis (
	zikatnr INT DEFAULT 0,
	argtnr INT DEFAULT 0,
	startperiode DATE,
	endperiode DATE,
	perspreis DECIMAL[6] DEFAULT ARRAY[0,0,0,0,0,0],
	kindpreis DECIMAL[2] DEFAULT ARRAY[0,0],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX katpreis_katpr_indx ON katpreis (zikatnr,argtnr,startperiode);
CREATE TABLE kellne1 (
	departement INT DEFAULT 0,
	kumsatz_nr INT DEFAULT 0,
	kzahl_nr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	kellner_nr INT DEFAULT 1,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kellne1_kellner_ix ON kellne1 (departement,kellner_nr);
CREATE TABLE kellner (
	departement INT DEFAULT 0,
	kumsatz_nr INT DEFAULT 0,
	kcredit_nr INT DEFAULT 0,
	kzahl_nr INT DEFAULT 0,
	kellnername CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	updatedatum DATE,
	saldo DECIMAL DEFAULT 0,
	kellner_nr INT DEFAULT 1,
	sprachcode INT DEFAULT 1,
	masterkey BOOLEAN DEFAULT False,
	nullbon BOOLEAN DEFAULT False,
	ignore_pers BOOLEAN DEFAULT False,
	kel_unique BOOLEAN DEFAULT False,
	storno_begruendung BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kellner_kellner_ix ON kellner (departement,kumsatz_nr);
CREATE INDEX kellner_kellnr_ix ON kellner (kellner_nr,departement);
CREATE TABLE kontakt (
	bankettnr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anrede CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	abteilung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sprachcode INT DEFAULT 1,
	durchwahl CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	hauptkontakt BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kontakt_kontak_ix ON kontakt (bankettnr);
CREATE TABLE kontline (
	bediener_nr INT DEFAULT 0,
	kontignr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	gastnrpay INT DEFAULT 0,
	ankunft DATE,
	anztage INT DEFAULT 1,
	abreise DATE,
	zimmeranz INT DEFAULT 1,
	zikatnr INT DEFAULT 0,
	erwachs INT DEFAULT 0,
	gratis INT DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zipreis DECIMAL DEFAULT 0,
	kontstatus INT DEFAULT 1,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kind1 INT DEFAULT 0,
	kind2 INT DEFAULT 0,
	ankzeit INT DEFAULT 0,
	adrflag BOOLEAN DEFAULT False,
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	rueckdatum DATE,
	ruecktage INT DEFAULT 0,
	kontcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ansprech CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	overbooking INT DEFAULT 0,
	useridanlage CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resdat DATE,
	pr_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Day_setting INT[7] DEFAULT ARRAY[0,0,0,0,0,0,0],
	kontakt_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	betrieb_gastpay INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kontline_betr_kontnr_ix ON kontline (betriebsnr,kontignr);
CREATE INDEX kontline_gastnr_ix ON kontline (gastnr,ankunft);
CREATE INDEX kontline_kontcode_ix ON kontline (kontstatus,code COLLATE case_insensitive);
CREATE INDEX kontline_kontnr_ix ON kontline (kontignr);
CREATE INDEX kontline_kontstat_ix ON kontline (kontstatus);
CREATE TABLE kontlink (
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	gastnr INT DEFAULT 0,
	gastnr_kont INT DEFAULT 0,
	kontakt_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	betrieb_gastkont INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kontlink_betr_link_ix ON kontlink (betriebsnr,resnr,reslinnr);
CREATE INDEX kontlink_kontlink_ix ON kontlink (resnr,reslinnr);
CREATE TABLE kontplan (
	kontignr INT DEFAULT 0,
	datum DATE,
	anzkont INT DEFAULT 0,
	anzconf INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX kontplan_betr_kontplan_ix ON kontplan (betriebsnr,kontignr,datum);
CREATE INDEX kontplan_kontplan_ix ON kontplan (kontignr,datum);
CREATE TABLE kontstat (
	gastnr INT DEFAULT 0,
	kontcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	zikatnr INT DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	erwachs INT DEFAULT 0,
	kind1 INT DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	overbook INT DEFAULT 0,
	belegt INT DEFAULT 0,
	personen INT DEFAULT 0,
	reserve_int INT[3] DEFAULT ARRAY[0,0,0],
	reserve_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	reserve_dec DECIMAL[3] DEFAULT ARRAY[0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX kontstat_codedat_ix ON kontstat (gastnr,kontcode COLLATE case_insensitive,datum);
CREATE INDEX kontstat_date_ix ON kontstat (datum);
CREATE INDEX kontstat_gastcode_ix ON kontstat (gastnr,kontcode COLLATE case_insensitive);
CREATE INDEX kontstat_gastdat_ix ON kontstat (gastnr,datum);
CREATE INDEX kontstat_gastnr_ix ON kontstat (gastnr);
CREATE TABLE kresline (
	gastnr INT DEFAULT 0,
	firstper BOOLEAN DEFAULT True,
	kurresnr INT DEFAULT 0,
	kreslinr INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	datum DATE,
	artnr INT DEFAULT 0,
	anz INT DEFAULT 0,
	massnr INT DEFAULT 0,
	massfest BOOLEAN DEFAULT False,
	kabnr INT DEFAULT 0,
	zeitanw CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	buchart INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lupdate CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX kresline_datzeit_ix ON kresline (kurresnr,datum,zeitanw COLLATE case_insensitive);
CREATE INDEX kresline_kreslinnr_ix ON kresline (kurresnr,kreslinr);
CREATE INDEX kresline_kurresnr_ix ON kresline (kurresnr);
CREATE TABLE l_artikel (
	artnr INT DEFAULT 0,
	zwkum INT DEFAULT 0,
	endkum INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	jahrgang INT DEFAULT 0,
	min_bestand DECIMAL DEFAULT 0,
	lieferfrist INT DEFAULT 0,
	inhalt DECIMAL DEFAULT 1,
	lief_einheit DECIMAL DEFAULT 1,
	masseinheit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	herkunft CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	erfass_art BOOLEAN DEFAULT False,
	bestellt BOOLEAN DEFAULT False,
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	alkoholgrad DECIMAL DEFAULT 0,
	traubensorte CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lief_nr1 INT DEFAULT 0,
	lief_nr2 INT DEFAULT 0,
	lief_nr3 INT DEFAULT 0,
	letz_eingang DATE,
	letz_ausgang DATE,
	anzverbrauch DECIMAL DEFAULT 0,
	ek_aktuell DECIMAL DEFAULT 0,
	ek_letzter DECIMAL DEFAULT 0,
	wert_verbrau DECIMAL DEFAULT 0,
	vk_preis DECIMAL DEFAULT 0,
	lief_artnr CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_artikel_artgrp_ix ON l_artikel (zwkum,bezeich COLLATE case_insensitive);
CREATE INDEX l_artikel_artgrpnum_ix ON l_artikel (zwkum,artnr);
CREATE INDEX l_artikel_artnr_ix ON l_artikel (artnr);
CREATE INDEX l_artikel_bezeich_ix ON l_artikel (bezeich COLLATE case_insensitive);
CREATE TABLE l_bestand (
	artnr INT DEFAULT 0,
	lager_nr INT DEFAULT 0,
	anf_best_dat DATE,
	anz_anf_best DECIMAL DEFAULT 0,
	val_anf_best DECIMAL DEFAULT 0,
	anz_eingang DECIMAL DEFAULT 0,
	wert_eingang DECIMAL DEFAULT 0,
	anz_ausgang DECIMAL DEFAULT 0,
	wert_ausgang DECIMAL DEFAULT 0,
	kumrezept DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_bestand_artnrlag_ix ON l_bestand (lager_nr,artnr);
CREATE TABLE l_besthis (
	artnr INT DEFAULT 0,
	lager_nr INT DEFAULT 0,
	anf_best_dat DATE,
	anz_anf_best DECIMAL DEFAULT 0,
	val_anf_best DECIMAL DEFAULT 0,
	anz_eingang DECIMAL DEFAULT 0,
	wert_eingang DECIMAL DEFAULT 0,
	anz_ausgang DECIMAL DEFAULT 0,
	wert_ausgang DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_besthis_artnrlag_ix ON l_besthis (anf_best_dat,lager_nr,artnr);
CREATE TABLE l_hauptgrp (
	endkum INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_hauptgrp_hauptgrp_ix ON l_hauptgrp (endkum);
CREATE TABLE l_kredit (
	lief_nr INT DEFAULT 0,
	rgdatum DATE,
	datum DATE,
	rechnr INT DEFAULT 0,
	saldo DECIMAL DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	counter INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	skonto DECIMAL DEFAULT 0,
	rabatt DECIMAL DEFAULT 0,
	ziel INT DEFAULT 0,
	lscheinnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	steuercode INT DEFAULT 0,
	mwstbetrag DECIMAL DEFAULT 0,
	netto DECIMAL DEFAULT 0,
	skontobetrag DECIMAL DEFAULT 0,
	rabattbetrag DECIMAL DEFAULT 0,
	zahlkonto INT DEFAULT 0,
	opart INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_kredit_betrag_ix ON l_kredit (opart,saldo,name COLLATE case_insensitive,lief_nr);
CREATE INDEX l_kredit_counter_ix ON l_kredit (counter,opart);
CREATE INDEX l_kredit_liefnr2_ix ON l_kredit (opart,name COLLATE case_insensitive,lief_nr);
CREATE INDEX l_kredit_liefnr3_ix ON l_kredit (lief_nr,opart);
CREATE INDEX l_kredit_liefnr_ix ON l_kredit (lief_nr,rgdatum,opart);
CREATE INDEX l_kredit_liefsch_ix ON l_kredit (lscheinnr COLLATE case_insensitive);
CREATE INDEX l_kredit_name_ix ON l_kredit (name COLLATE case_insensitive,lief_nr,rgdatum);
CREATE INDEX l_kredit_rechnr_ix ON l_kredit (opart,rechnr);
CREATE TABLE l_lager (
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lager_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_lager_lager_nr_ix ON l_lager (lager_nr);
CREATE TABLE l_lieferant (
	firma CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lief_nr INT DEFAULT 0,
	anredefirma CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	namekontakt CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorname1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anrede1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	land CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	PLZ CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	wohnort CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telex CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	segment1 INT DEFAULT 0,
	lieferdatum DATE,
	skonto DECIMAL DEFAULT 0,
	rabatt DECIMAL DEFAULT 0,
	notizen CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	ziel INT DEFAULT 0,
	bank CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	blz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kontonr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	z_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX l_lieferant_betr_nr_ix ON l_lieferant (betriebsnr,lief_nr);
CREATE INDEX l_lieferant_liefnr_ix ON l_lieferant (lief_nr);
CREATE INDEX l_lieferant_name_ix ON l_lieferant (firma COLLATE case_insensitive);
CREATE INDEX l_lieferant_segm_ix ON l_lieferant (segment1,firma COLLATE case_insensitive);
CREATE TABLE l_liefumsatz (
	lief_nr INT DEFAULT 0,
	datum DATE,
	gesamtumsatz DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_liefumsatz_liefums_ix ON l_liefumsatz (lief_nr,datum);
CREATE TABLE l_op (
	artnr INT DEFAULT 0,
	datum DATE,
	zeit INT DEFAULT 0,
	lief_nr INT DEFAULT 0,
	lager_nr INT DEFAULT 0,
	anzahl DECIMAL DEFAULT 0,
	einzelpreis DECIMAL DEFAULT 0,
	warenwert DECIMAL DEFAULT 0,
	op_art INT DEFAULT 0,
	herkunftflag INT DEFAULT 0,
	loeschflag INT DEFAULT 0,
	fuellflag INT DEFAULT 0,
	reorgflag INT DEFAULT 0,
	rueckgabegrund INT DEFAULT 0,
	flag BOOLEAN DEFAULT False,
	stornogrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lscheinnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	pos INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	deci1 DECIMAL[4] DEFAULT ARRAY[0,0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX l_op_artnrlag_ix ON l_op (lager_nr,artnr,datum,zeit);
CREATE INDEX l_op_artopart_ix ON l_op (lager_nr,artnr,op_art,datum);
CREATE INDEX l_op_journal_ix ON l_op (datum,lager_nr,lief_nr,op_art);
CREATE INDEX l_op_lief_ix ON l_op (lief_nr,op_art,datum);
CREATE INDEX l_op_lscheinnr_ix ON l_op (lscheinnr COLLATE case_insensitive,loeschflag,pos);
CREATE INDEX l_op_umsatz_ix ON l_op (datum,artnr,op_art,herkunftflag);
CREATE TABLE l_ophdr (
	datum DATE,
	lager_nr INT DEFAULT 0,
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lscheinnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	op_typ CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX l_ophdr_l_ophdr_dat ON l_ophdr (op_typ COLLATE case_insensitive,datum);
CREATE INDEX l_ophdr_l_ophdr_i ON l_ophdr (op_typ COLLATE case_insensitive,lscheinnr COLLATE case_insensitive);
CREATE INDEX l_ophdr_l_ophdr_lg ON l_ophdr (op_typ COLLATE case_insensitive,lager_nr);
CREATE TABLE l_ophhis (
	datum DATE,
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lscheinnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	op_typ CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX l_ophhis_dat_typ_ix ON l_ophhis (datum,op_typ COLLATE case_insensitive);
CREATE INDEX l_ophhis_schein_typ_ix ON l_ophhis (lscheinnr COLLATE case_insensitive,op_typ COLLATE case_insensitive);
CREATE TABLE l_ophis (
	artnr INT DEFAULT 0,
	datum DATE,
	lief_nr INT DEFAULT 0,
	lager_nr INT DEFAULT 0,
	anzahl DECIMAL DEFAULT 0,
	einzelpreis DECIMAL DEFAULT 0,
	warenwert DECIMAL DEFAULT 0,
	op_art INT DEFAULT 0,
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lscheinnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX l_ophis_art_dat_op_ix ON l_ophis (artnr,datum,op_art);
CREATE INDEX l_ophis_l_art_dat_op_ix ON l_ophis (artnr,datum,lager_nr,op_art);
CREATE INDEX l_ophis_lief_op_dat_ix ON l_ophis (lief_nr,op_art,datum);
CREATE INDEX l_ophis_schein_op_ix ON l_ophis (lscheinnr COLLATE case_insensitive,op_art);
CREATE TABLE l_order (
	artnr INT DEFAULT 0,
	bestelldatum DATE,
	zeit INT DEFAULT 0,
	lief_nr INT DEFAULT 0,
	lager_nr INT DEFAULT 0,
	anzahl DECIMAL DEFAULT 0,
	einzelpreis DECIMAL DEFAULT 0,
	warenwert DECIMAL DEFAULT 0,
	op_art INT DEFAULT 0,
	herkunftflag INT DEFAULT 0,
	loeschflag INT DEFAULT 0,
	rueckgabegrund INT DEFAULT 0,
	flag BOOLEAN DEFAULT False,
	stornogrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	besteller CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lieferdatum DATE,
	lieferdatum_eff DATE,
	bestellart CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	quality CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	geliefert DECIMAL DEFAULT 0,
	rechnungspreis DECIMAL DEFAULT 0,
	rechnungswert DECIMAL DEFAULT 0,
	angebot_lief INT[3] DEFAULT ARRAY[0,0,0],
	gedruckt DATE,
	gefaxt DATE,
	lief_fax CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	txtnr INT DEFAULT 1,
	pos INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_order_artnr_index ON l_order (op_art,artnr,bestelldatum);
CREATE INDEX l_order_lief_index ON l_order (op_art,lief_nr,bestelldatum,artnr);
CREATE INDEX l_order_order_ix ON l_order (docu_nr COLLATE case_insensitive,pos);
CREATE TABLE l_orderhdr (
	bestelldatum DATE,
	lief_nr INT DEFAULT 0,
	besteller CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lieferdatum DATE,
	bestellart CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	angebot_lief INT[3] DEFAULT ARRAY[0,0,0],
	gedruckt DATE,
	gefaxt DATE,
	lief_fax CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	txtnr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_orderhdr_l_orderhdr_dat ON l_orderhdr (bestelldatum);
CREATE INDEX l_orderhdr_l_orderhdr_i ON l_orderhdr (docu_nr COLLATE case_insensitive);
CREATE INDEX l_orderhdr_l_orderhdr_lief ON l_orderhdr (lief_nr);
CREATE INDEX l_orderhdr_l_orderhdr_liefdat ON l_orderhdr (lieferdatum);
CREATE TABLE l_pprice (
	artnr INT DEFAULT 0,
	bestelldatum DATE,
	lief_nr INT DEFAULT 0,
	anzahl DECIMAL DEFAULT 0,
	einzelpreis DECIMAL DEFAULT 0,
	warenwert DECIMAL DEFAULT 0,
	counter INT DEFAULT 0,
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_pprice_artdat_ix ON l_pprice (artnr,bestelldatum);
CREATE INDEX l_pprice_artnr_ix ON l_pprice (artnr);
CREATE INDEX l_pprice_counter_ix ON l_pprice (artnr,counter);
CREATE TABLE l_quote (
	artnr INT DEFAULT 0,
	from_date DATE,
	to_date DATE,
	lief_nr INT DEFAULT 0,
	docu_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	unitprice DECIMAL DEFAULT 0,
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	filname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT True,
	reserve_char CHARACTER VARYING [5] COLLATE case_insensitive DEFAULT ARRAY['','','','',''],
	reserve_deci DECIMAL[5] DEFAULT ARRAY[0,0,0,0,0],
	reserve_logic BOOLEAN[5] DEFAULT ARRAY[false,false,false,false,false],
	reserve_int INT[5] DEFAULT ARRAY[0,0,0,0,0],
	createID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	createDate DATE,
	createTime INT DEFAULT 0,
	chgID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	chgdate DATE,
	chgtime INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_quote_act_date_ix ON l_quote (chgdate,activeflag);
CREATE INDEX l_quote_art_dat_flag_ix ON l_quote (artnr,to_date,activeflag);
CREATE INDEX l_quote_artnr_dat_ix ON l_quote (artnr,to_date);
CREATE INDEX l_quote_artnr_lief_ix ON l_quote (artnr,lief_nr);
CREATE INDEX l_quote_artnr_ix ON l_quote (artnr);
CREATE INDEX l_quote_docu_ix ON l_quote (docu_nr COLLATE case_insensitive);
CREATE INDEX l_quote_lief_docu_ix ON l_quote (lief_nr,docu_nr COLLATE case_insensitive);
CREATE INDEX l_quote_liefnr_ix ON l_quote (lief_nr);
CREATE TABLE l_segment (
	l_segmentcode INT DEFAULT 0,
	l_segmentgrup INT DEFAULT 1,
	l_bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	l_bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_segment_segbez_ix ON l_segment (l_bezeich COLLATE case_insensitive);
CREATE INDEX l_segment_segm_ix ON l_segment (l_segmentcode);
CREATE TABLE l_umsatz (
	datum DATE,
	zwkum INT DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	endkum INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_umsatz_umsatz_ix ON l_umsatz (zwkum,endkum,datum);
CREATE TABLE l_untergrup (
	zwkum INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_untergrup_untergrup_ix ON l_untergrup (zwkum);
CREATE TABLE l_verbrauch (
	artnr INT DEFAULT 0,
	datum DATE,
	anz_verbrau DECIMAL DEFAULT 0,
	wert_verbrau DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX l_verbrauch_verbrauch_ix ON l_verbrauch (artnr,datum);
CREATE TABLE l_zahlbed (
	betriebsnr INT DEFAULT 0,
	z_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zahl_ziel INT DEFAULT 0,
	skonto_perc DECIMAL DEFAULT 0,
	skonto_tage INT DEFAULT 0,
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX l_zahlbed_z_code_ix ON l_zahlbed (betriebsnr,z_code COLLATE case_insensitive);
CREATE TABLE landstat (
	nationnr INT DEFAULT 0,
	datum DATE,
	logis DECIMAL DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	persanz INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX landstat_date_ix ON landstat (datum);
CREATE INDEX landstat_nat_ix ON landstat (nationnr,datum);
CREATE TABLE masseur (
	massnr INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sex BOOLEAN DEFAULT False,
	pausebeg CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	pauseend CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	commission DECIMAL DEFAULT 0,
	dayoff BOOLEAN DEFAULT False,
	oooab CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	ooobis CHARACTER VARYING COLLATE case_insensitive DEFAULT '00:00',
	fdate DATE,
	tdate DATE,
	grund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX masseur_massnr_ix ON masseur (massnr);
CREATE INDEX masseur_name_ix ON masseur (name COLLATE case_insensitive);
CREATE INDEX masseur_sex_ix ON masseur (sex,name COLLATE case_insensitive);
CREATE TABLE mast_art (
	resnr INT DEFAULT 0,
	artnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX mast_art_resart_ix ON mast_art (resnr,reslinnr,artnr);
CREATE TABLE master (
	resnr INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	gastnrpay INT DEFAULT 0,
	active BOOLEAN DEFAULT False,
	rechnrstart INT DEFAULT 0,
	rechnrend INT DEFAULT 0,
	flag INT DEFAULT 0,
	umsatzart BOOLEAN[4] DEFAULT ARRAY[false,false,false,false],
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	betrieb_gastpay INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX master_betr_master_ix ON master (betriebsnr,flag,resnr);
CREATE INDEX master_mast_gastnr_ix ON master (gastnr);
CREATE INDEX master_mast_pay_ix ON master (gastnrpay);
CREATE INDEX master_mast_res_ix ON master (resnr);
CREATE INDEX master_master_ix ON master (flag,resnr);
CREATE INDEX master_mastnam_ix ON master (flag,name COLLATE case_insensitive,resnr);
CREATE INDEX master_mastrech_ix ON master (flag,rechnr);
CREATE TABLE mathis (
	nr INT DEFAULT 0,
	datum DATE,
	supplier CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	model CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	asset CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	spec CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	location CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	price DECIMAL DEFAULT 0,
	fname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	flag INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX mathis_flag_ix ON mathis (flag,name COLLATE case_insensitive);
CREATE INDEX mathis_locate_ix ON mathis (location COLLATE case_insensitive);
CREATE INDEX mathis_name_ix ON mathis (name COLLATE case_insensitive);
CREATE INDEX mathis_nr_ix ON mathis (nr);
CREATE TABLE mc_aclub (
	key INT DEFAULT 0,
	cardnum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	SYSDate DATE,
	zeit INT DEFAULT 0,
	billdatum DATE,
	billtype INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	artnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	nettobetrag DECIMAL DEFAULT 0,
	incl_flag INT DEFAULT 1,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 0,
	vat DECIMAL DEFAULT 0,
	service DECIMAL DEFAULT 0,
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	num4 INT DEFAULT 0,
	num5 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	deci4 DECIMAL DEFAULT 0,
	deci5 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char4 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char5 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX mc_aclub_incl_ix ON mc_aclub (key,incl_flag);
CREATE INDEX mc_aclub_keynum_ix ON mc_aclub (key,cardnum COLLATE case_insensitive);
CREATE INDEX mc_aclub_rechnrtype_ix ON mc_aclub (key,rechnr,billtype);
CREATE INDEX mc_aclub_sysdate_ix ON mc_aclub (key,SYSDate);
CREATE TABLE mc_cardhis (
	gastnr INT DEFAULT 0,
	old_card CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	new_card CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	old_nr INT DEFAULT 0,
	new_nr INT DEFAULT 0,
	datum DATE,
	zeit INT DEFAULT 0,
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX mc_cardhis_date_ix ON mc_cardhis (datum);
CREATE INDEX mc_cardhis_gastnr_ix ON mc_cardhis (gastnr);
CREATE INDEX mc_cardhis_newcard_ix ON mc_cardhis (new_card COLLATE case_insensitive);
CREATE INDEX mc_cardhis_newnr_ix ON mc_cardhis (new_nr,datum);
CREATE INDEX mc_cardhis_oldcard_ix ON mc_cardhis (old_card COLLATE case_insensitive);
CREATE INDEX mc_cardhis_oldnr_ix ON mc_cardhis (old_nr,datum);
CREATE TABLE mc_disc (
	nr INT DEFAULT 0,
	departement INT DEFAULT 0,
	artnrfront INT DEFAULT 0,
	discount DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX mc_disc_nr_ix ON mc_disc (nr);
CREATE INDEX mc_disc_nrart_ix ON mc_disc (nr,departement,artnrfront);
CREATE TABLE mc_fee (
	key INT DEFAULT 0,
	nr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	von_datum DATE,
	bis_datum DATE,
	bezahlt DECIMAL DEFAULT 0,
	bezahlt2 DECIMAL DEFAULT 0,
	bez_datum DATE,
	bez_datum2 DATE,
	usr_init CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	usr_init2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	artnr INT DEFAULT 0,
	artnr2 INT DEFAULT 0,
	activeflag INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX mc_fee_gast_ix ON mc_fee (key,nr,gastnr,bis_datum);
CREATE INDEX mc_fee_kdate_ix ON mc_fee (key,bis_datum);
CREATE INDEX mc_fee_keynr_ix ON mc_fee (key,nr);
CREATE INDEX mc_fee_kgast_ix ON mc_fee (key,gastnr);
CREATE INDEX mc_fee_kgastdat_ix ON mc_fee (key,gastnr,bis_datum);
CREATE INDEX mc_fee_kpay_ix ON mc_fee (key,bezahlt,activeflag);
CREATE INDEX mc_fee_kpaydat_ix ON mc_fee (key,bis_datum,bezahlt,activeflag);
CREATE TABLE mc_guest (
	nr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	cardnum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fdate DATE,
	tdate DATE,
	sales_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT False,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	changed CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_date DATE,
	date1 DATE,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX mc_guest_act_crdate_ix ON mc_guest (activeflag,created_date);
CREATE INDEX mc_guest_cardnum_ix ON mc_guest (cardnum COLLATE case_insensitive);
CREATE INDEX mc_guest_crdate_ix ON mc_guest (created_date);
CREATE INDEX mc_guest_gast_ix ON mc_guest (gastnr);
CREATE INDEX mc_guest_gastact_ix ON mc_guest (gastnr,activeflag);
CREATE INDEX mc_guest_nr_ix ON mc_guest (nr,activeflag);
CREATE TABLE mc_types (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	joinfee DECIMAL DEFAULT 0,
	renewal_fee DECIMAL DEFAULT 0,
	dauer INT DEFAULT 0,
	rm_compli INT DEFAULT 0,
	rm_disc DECIMAL DEFAULT 0,
	food_disc DECIMAL DEFAULT 0,
	bev_disc DECIMAL DEFAULT 0,
	prepaid DECIMAL DEFAULT 0,
	numstay INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT True,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX mc_types_nr_ix ON mc_types (nr);
CREATE TABLE mealcoup (
	resnr INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anzahl INT DEFAULT 0,
	verbrauch INT[32] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	ankunft DATE,
	abreise DATE,
	activeflag BOOLEAN DEFAULT True,
	_recid serial PRIMARY KEY
);
CREATE INDEX mealcoup_resnr_ix ON mealcoup (resnr);
CREATE INDEX mealcoup_reszinr_ix ON mealcoup (resnr,zinr COLLATE case_insensitive);
CREATE INDEX mealcoup_zinr_ix ON mealcoup (zinr COLLATE case_insensitive);
CREATE INDEX mealcoup_zinrflag_ix ON mealcoup (zinr COLLATE case_insensitive,activeflag);
CREATE TABLE messages (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	zeit INT DEFAULT 0,
	messtext CHARACTER VARYING [10] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','',''],
	usre CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	Present_guest BOOLEAN DEFAULT False,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gastnr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX messages_gastnr_ix ON messages (gastnr);
CREATE INDEX messages_name_ix ON messages (name COLLATE case_insensitive,gastnr,datum,zeit);
CREATE INDEX messages_resnr_ix ON messages (resnr,reslinnr,datum,zeit);
CREATE INDEX messages_zinr_ix ON messages (zinr COLLATE case_insensitive,resnr,reslinnr,datum,zeit);
CREATE TABLE messe (
	mdatum DATE,
	mtext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	notes CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX messe_dat_index ON messe (mdatum);
CREATE TABLE mhis_line (
	nr INT DEFAULT 0,
	datum DATE,
	remark CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	cost DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX mhis_line_nr_ix ON mhis_line (nr);
CREATE TABLE nation (
	nationnr INT DEFAULT 0,
	kurzbez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	natcode INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	untergruppe INT DEFAULT 1,
	hauptgruppe INT DEFAULT 1,
	language INT DEFAULT 0,
	in_stat BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX nation_natbez_index ON nation (kurzbez COLLATE case_insensitive);
CREATE INDEX nation_nationnr_ix ON nation (nationnr);
CREATE TABLE nationstat (
	nationnr INT DEFAULT 0,
	datum DATE,
	ankerwachs INT DEFAULT 0,
	ankkind1 INT DEFAULT 0,
	ankkind2 INT DEFAULT 0,
	ankgratis INT DEFAULT 0,
	logerwachs INT DEFAULT 0,
	logkind1 INT DEFAULT 0,
	logkind2 INT DEFAULT 0,
	loggratis INT DEFAULT 0,
	dankerwachs INT DEFAULT 0,
	dankkind1 INT DEFAULT 0,
	dankkind2 INT DEFAULT 0,
	dankgratis INT DEFAULT 0,
	dlogerwachs INT DEFAULT 0,
	dlogkind1 INT DEFAULT 0,
	dlogkind2 INT DEFAULT 0,
	dloggratis INT DEFAULT 0,
	argtart INT DEFAULT 2,
	abrerwachs INT DEFAULT 0,
	abrgratis INT DEFAULT 0,
	abrkind1 INT DEFAULT 0,
	abrkind2 INT DEFAULT 0,
	dankzimmer INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX nationstat_betr_nat_ix ON nationstat (betriebsnr,nationnr,datum,argtart);
CREATE INDEX nationstat_haupt ON nationstat (nationnr,datum,argtart);
CREATE TABLE natstat1 (
	nationnr INT DEFAULT 0,
	datum DATE,
	logis DECIMAL DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	persanz INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX natstat1_date_ix ON natstat1 (datum);
CREATE INDEX natstat1_nat_ix ON natstat1 (nationnr,datum);
CREATE TABLE nebenst (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nebenstelle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nebstart INT DEFAULT 0,
	nebst_type INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	vipnr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	rechnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX nebenst_nebst_art_ix ON nebenst (nebenstelle COLLATE case_insensitive,nebstart);
CREATE INDEX nebenst_zinr_art_ix ON nebenst (zinr COLLATE case_insensitive,nebstart);
CREATE TABLE nightaudit (
	reportnr INT DEFAULT 0,
	reihenfolge INT DEFAULT 0,
	abschlussart BOOLEAN DEFAULT False,
	selektion BOOLEAN DEFAULT False,
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sequenz INT DEFAULT 1,
	dekade INT DEFAULT 0,
	anzkopien INT DEFAULT 1,
	programm CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lastrun DATE,
	hogarest INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX nightaudit_nidisp_ndx ON nightaudit (selektion,reihenfolge);
CREATE INDEX nightaudit_night_ndx ON nightaudit (abschlussart,reihenfolge);
CREATE TABLE nitehist (
	datum DATE,
	reihenfolge INT DEFAULT 0,
	line_nr INT DEFAULT 0,
	line CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX nitehist_date_ix ON nitehist (datum);
CREATE INDEX nitehist_datenr_ix ON nitehist (datum,reihenfolge);
CREATE INDEX nitehist_datline_ix ON nitehist (datum,reihenfolge,line_nr);
CREATE TABLE nitestor (
	night_type INT DEFAULT 0,
	reihenfolge INT DEFAULT 0,
	line_nr INT DEFAULT 0,
	line CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX nitestor_betr_nite_ix ON nitestor (betriebsnr,night_type,reihenfolge,line_nr);
CREATE INDEX nitestor_grp_ix ON nitestor (night_type,reihenfolge,line_nr);
CREATE TABLE notes (
	dept CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	note CHARACTER VARYING [19] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','',''],
	betriebsnr INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	departement INT DEFAULT 0,
	page_nr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX notes_bed_ix ON notes (bediener_nr,page_nr);
CREATE INDEX notes_dep_ix ON notes (departement,page_nr);
CREATE INDEX notes_dept ON notes (dept COLLATE case_insensitive);
CREATE TABLE outorder (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gespgrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gespstart DATE,
	gespende DATE,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX outorder_gespende_ix ON outorder (gespende);
CREATE INDEX outorder_zinr_ix ON outorder (zinr COLLATE case_insensitive);
CREATE INDEX outorder_zinrdat_ix ON outorder (zinr COLLATE case_insensitive,gespstart);
CREATE TABLE package (
	gastnr INT DEFAULT 0,
	buchtage INT DEFAULT 0,
	fakttage INT DEFAULT 0,
	beginn DATE,
	ende DATE,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX package_gastnr_ix ON package (gastnr,beginn);
CREATE TABLE parameters (
	progname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	section CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	varname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vtype INT DEFAULT 0,
	vstring CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX parameters_param_ix ON parameters (progname COLLATE case_insensitive,section COLLATE case_insensitive,varname COLLATE case_insensitive);
CREATE TABLE paramtext (
	ptexte CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	txtnr INT DEFAULT 0,
	notes CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sprachcode INT DEFAULT 0,
	number INT DEFAULT 0,
	passwort CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	wert BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX paramtext_param_index ON paramtext (txtnr,sprachcode,number);
CREATE TABLE pricecod (
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	marknr INT DEFAULT 0,
	argtnr INT DEFAULT 0,
	zikatnr INT DEFAULT 0,
	endperiode DATE,
	perspreis DECIMAL[6] DEFAULT ARRAY[0,0,0,0,0,0],
	kindpreis DECIMAL[2] DEFAULT ARRAY[0,0],
	startperiode DATE,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX pricecod_market_ix ON pricecod (marknr);
CREATE INDEX pricecod_pricecod_ix ON pricecod (code COLLATE case_insensitive,argtnr,zikatnr,startperiode,endperiode);
CREATE TABLE pricegrp (
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	argtnr INT DEFAULT 0,
	endperiode DATE,
	perspreis DECIMAL[6] DEFAULT ARRAY[0,0,0,0,0,0],
	kindpreis DECIMAL[2] DEFAULT ARRAY[0,0],
	startperiode DATE,
	betriebsnr INT DEFAULT 0,
	rueckdatum DATE,
	ruecktage INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX pricegrp_pricegrp_ix ON pricegrp (betriebsnr,code COLLATE case_insensitive,argtnr,startperiode,endperiode);
CREATE TABLE printcod (
	emu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Contcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX printcod_Print_index ON printcod (emu COLLATE case_insensitive,code COLLATE case_insensitive);
CREATE TABLE printer (
	nr INT DEFAULT 0,
	path CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	copies INT DEFAULT 1,
	make CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	emu CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	position CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	pglen INT DEFAULT 0,
	spooled BOOLEAN DEFAULT False,
	bondrucker BOOLEAN DEFAULT False,
	opsysname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX printer_prnr_index ON printer (nr);
CREATE TABLE prmarket (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX prmarket_nr_ix ON prmarket (nr);
CREATE TABLE progcat (
	nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	password CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX progcat_name_ix ON progcat (bezeich COLLATE case_insensitive);
CREATE INDEX progcat_nr_ix ON progcat (nr);
CREATE TABLE progfile (
	catnr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	password CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	filename CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX progfile_name_ix ON progfile (bezeich COLLATE case_insensitive);
CREATE INDEX progfile_nr_ix ON progfile (catnr);
CREATE TABLE prtable (
	nr INT DEFAULT 0,
	marknr INT DEFAULT 0,
	zikatnr INT[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	argtnr INT[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	prcode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	product INT[99] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX prtable_markcode_ix ON prtable (marknr,prcode COLLATE case_insensitive);
CREATE INDEX prtable_market_ix ON prtable (marknr);
CREATE INDEX prtable_nr_ix ON prtable (nr);
CREATE TABLE queasy (
	key INT DEFAULT 0,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX queasy_b_char_ix ON queasy (betriebsnr,key,char1 COLLATE case_insensitive,deci1,logi1,date1,number1,char2 COLLATE case_insensitive);
CREATE INDEX queasy_b_dat_ix ON queasy (betriebsnr,key,date1,char1 COLLATE case_insensitive,number1,deci1,logi1,date2);
CREATE INDEX queasy_b_deci_ix ON queasy (betriebsnr,key,deci1,char1 COLLATE case_insensitive,logi1,number1,date1,deci2);
CREATE INDEX queasy_b_log_ix ON queasy (betriebsnr,key,logi1,char1 COLLATE case_insensitive,number1,date1,deci1,logi2);
CREATE INDEX queasy_b_num_ix ON queasy (betriebsnr,key,number1,date1,char1 COLLATE case_insensitive,deci1,logi1,number2);
CREATE INDEX queasy_queasychr2_ix ON queasy (key,char2 COLLATE case_insensitive,number2,date2,deci2,logi2);
CREATE INDEX queasy_queasychr_ix ON queasy (key,char1 COLLATE case_insensitive,number1,deci1,date1);
CREATE INDEX queasy_queasydat_ix ON queasy (key,date1,logi1,number1,char1 COLLATE case_insensitive,deci1);
CREATE INDEX queasy_queasydec_ix ON queasy (key,deci1,number1,date1,char1 COLLATE case_insensitive);
CREATE INDEX queasy_queasyint_ix ON queasy (key,number1,logi1,date1,char1 COLLATE case_insensitive,deci1);
CREATE INDEX queasy_queasylog_ix ON queasy (key,logi1,number1,deci1,date1,char1 COLLATE case_insensitive);
CREATE INDEX queasy_rbill_ix ON queasy (key,number1,number2,deci2);
CREATE TABLE ratecode (
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	marknr INT DEFAULT 0,
	argtnr INT DEFAULT 0,
	zikatnr INT DEFAULT 0,
	endperiode DATE,
	startperiode DATE,
	wday INT DEFAULT 0,
	erwachs INT DEFAULT 0,
	kind1 INT DEFAULT 0,
	kind2 INT DEFAULT 0,
	zipreis DECIMAL DEFAULT 0,
	ch1preis DECIMAL DEFAULT 0,
	ch2preis DECIMAL DEFAULT 0,
	char1 CHARACTER VARYING [99] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
	deci1 DECIMAL[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	num1 INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	logi1 BOOLEAN[9] DEFAULT ARRAY[false,false,false,false,false,false,false,false,false],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX ratecode_code_ix ON ratecode (code COLLATE case_insensitive);
CREATE INDEX ratecode_rate_ix ON ratecode (code COLLATE case_insensitive,marknr,argtnr,zikatnr,endperiode,startperiode,wday,erwachs,kind1,kind2);
CREATE TABLE raum (
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	groesse INT DEFAULT 0,
	preis DECIMAL DEFAULT 0,
	nebenstelle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	personen INT DEFAULT 0,
	vorbereit INT DEFAULT 0,
	user_group INT DEFAULT 0,
	sortierfolge INT DEFAULT 0,
	vname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX raum_raum_ix ON raum (raum COLLATE case_insensitive);
CREATE INDEX raum_sort_ix ON raum (sortierfolge);
CREATE TABLE res_history (
	nr INT DEFAULT 0,
	datum DATE,
	zeit INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	resnr INT DEFAULT 0,
	aenderung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	action CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX res_history_action_ix ON res_history (action COLLATE case_insensitive,datum);
CREATE INDEX res_history_bediener_time_date_ix ON res_history (nr,datum,zeit);
CREATE INDEX res_history_date_time_ix ON res_history (datum,zeit);
CREATE INDEX res_history_res_ix ON res_history (resnr,reslinnr,datum,zeit);
CREATE TABLE res_line (
	resnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	gastnrmember INT DEFAULT 0,
	gastnrpay INT DEFAULT 0,
	ankunft DATE,
	anztage INT DEFAULT 1,
	abreise DATE,
	zimmeranz INT DEFAULT 1,
	zikatnr INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	erwachs INT DEFAULT 1,
	gratis INT DEFAULT 0,
	arrangement CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zipreis DECIMAL DEFAULT 0,
	resstatus INT DEFAULT 1,
	bestaet_bis DATE,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kind1 INT DEFAULT 0,
	kind2 INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	grpflag BOOLEAN DEFAULT False,
	ankzeit INT DEFAULT 0,
	abreisezeit INT DEFAULT 0,
	adrflag BOOLEAN DEFAULT False,
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kontignr INT DEFAULT 0,
	voucher_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zimmerfix BOOLEAN DEFAULT False,
	pseudofix BOOLEAN DEFAULT False,
	ziwechseldat DATE,
	ziwech_zeit INT DEFAULT 0,
	l_zuordnung INT[5] DEFAULT ARRAY[0,0,0,0,0],
	setup INT DEFAULT 0,
	cancelled DATE,
	handtuch INT DEFAULT 0,
	waeschewechsel INT DEFAULT 0,
	cancelled_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	changed DATE,
	changed_id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resflag INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	active_flag INT DEFAULT 0,
	argt_typ INT DEFAULT 2,
	storno_nr INT DEFAULT 0,
	zimmer_wunsch CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	stornogrund CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	reserve_int INT DEFAULT 0,
	reserve_dec DECIMAL DEFAULT 0,
	reserve_char CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kontakt_nr INT DEFAULT 0,
	resname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	flight_nr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnext INT DEFAULT 0,
	resprev INT DEFAULT 0,
	prov_till DATE,
	memozinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	memodatum DATE,
	memousercode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	memozeit INT DEFAULT 0,
	was_status INT DEFAULT 0,
	pin_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	share_connect CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	wabkurz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	old_zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betrieb_gast INT DEFAULT 0,
	betrieb_gastmem INT DEFAULT 0,
	betrieb_gastpay INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX res_line_abr_resnam_ix ON res_line (abreise,resname COLLATE case_insensitive,gastnr,resnr,name COLLATE case_insensitive,gastnrmember,reslinnr);
CREATE INDEX res_line_act_ank_resnam_ix ON res_line (active_flag,ankunft,resname COLLATE case_insensitive,gastnr,resnr,name COLLATE case_insensitive,gastnrmember,reslinnr);
CREATE INDEX res_line_ank_resname_ix ON res_line (ankunft,resname COLLATE case_insensitive,gastnr,resnr,name COLLATE case_insensitive,gastnrmember,reslinnr);
CREATE INDEX res_line_ankunf_ix ON res_line (ankunft,name COLLATE case_insensitive,gastnrmember,resnr,reslinnr);
CREATE INDEX res_line_belop1_index ON res_line (zimmerfix,zinr COLLATE case_insensitive,ankunft,abreise);
CREATE INDEX res_line_belop2_index ON res_line (zinr COLLATE case_insensitive,abreise);
CREATE INDEX res_line_betr_resnr_ix ON res_line (betriebsnr,resnr,reslinnr);
CREATE INDEX res_line_gmemb_ix ON res_line (gastnrmember,resnr,zinr COLLATE case_insensitive,reslinnr);
CREATE INDEX res_line_gnrank_ix ON res_line (gastnr,ankunft,resstatus);
CREATE INDEX res_line_gnrpay_index ON res_line (gastnrpay);
CREATE INDEX res_line_Grp_index ON res_line (grpflag,resnr);
CREATE INDEX res_line_kontnr_ix ON res_line (kontignr,ankunft,resnr,reslinnr);
CREATE INDEX res_line_nameres_ix ON res_line (name COLLATE case_insensitive,gastnrmember,resnr,reslinnr);
CREATE INDEX res_line_pin_ix ON res_line (active_flag,pin_code COLLATE case_insensitive);
CREATE INDEX res_line_relinr_index ON res_line (resnr,reslinnr);
CREATE INDEX res_line_res_abr_ix ON res_line (active_flag,abreise,name COLLATE case_insensitive,gastnrmember,resnr,reslinnr);
CREATE INDEX res_line_res_ank_ix ON res_line (active_flag,ankunft,name COLLATE case_insensitive,gastnrmember,resnr,reslinnr);
CREATE INDEX res_line_res_name_ix ON res_line (active_flag,name COLLATE case_insensitive,gastnrmember,resnr,reslinnr);
CREATE INDEX res_line_res_resnr_ix ON res_line (active_flag,resnr,reslinnr);
CREATE INDEX res_line_res_zinr_ix ON res_line (active_flag,zinr COLLATE case_insensitive,name COLLATE case_insensitive,gastnrmember);
CREATE INDEX res_line_resname_ix ON res_line (resname COLLATE case_insensitive,gastnr,resnr,name COLLATE case_insensitive,gastnrmember,reslinnr);
CREATE INDEX res_line_zinr_index ON res_line (zinr COLLATE case_insensitive,resstatus);
CREATE TABLE reservation (
	resnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	resart INT DEFAULT 1,
	briefnr INT DEFAULT 0,
	refdatum DATE,
	useridanlage CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	useridmutat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mutdat DATE,
	resdat DATE,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	depositgef DECIMAL DEFAULT 0,
	limitdate DATE,
	depositbez DECIMAL DEFAULT 0,
	zahldatum DATE,
	zahlkonto INT DEFAULT 0,
	deptrans DATE,
	ankzeit INT DEFAULT 0,
	segmentcode INT DEFAULT 0,
	guestnrcom INT[3] DEFAULT ARRAY[0,0,0],
	groupname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gastnrherk INT DEFAULT 0,
	herkunft CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	point_resnr INT DEFAULT 0,
	grpflag BOOLEAN DEFAULT False,
	source_code INT DEFAULT 0,
	kontakt_nr INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	deposit_type INT DEFAULT 0,
	depositgef2 DECIMAL DEFAULT 0,
	depositbez2 DECIMAL DEFAULT 0,
	limitdate2 DATE,
	zahldatum2 DATE,
	zahlkonto2 INT DEFAULT 0,
	bestat_datum DATE,
	total_price DECIMAL DEFAULT 0,
	insurance BOOLEAN DEFAULT False,
	insurance_pct DECIMAL DEFAULT 0,
	vesrdepot CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vesrdepot2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vesrcod CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	verstat INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	betrieb_gastherk INT DEFAULT 0,
	betrieb_gastcomm INT[3] DEFAULT ARRAY[0,0,0],
	_recid serial PRIMARY KEY
);
CREATE INDEX reservation_astname_ix ON reservation (activeflag,name COLLATE case_insensitive,gastnr);
CREATE INDEX reservation_betr_resnr_ix ON reservation (betriebsnr,resnr);
CREATE INDEX reservation_deposit_ix ON reservation (depositgef,deptrans,depositbez);
CREATE INDEX reservation_gastnr_index ON reservation (activeflag,gastnr,resnr);
CREATE INDEX reservation_group_ix ON reservation (activeflag,grpflag,name COLLATE case_insensitive,gastnr);
CREATE INDEX reservation_herk_ix ON reservation (activeflag,herkunft COLLATE case_insensitive,gastnrherk);
CREATE INDEX reservation_herknr_ix ON reservation (gastnrherk);
CREATE INDEX reservation_herkres_ix ON reservation (herkunft COLLATE case_insensitive,gastnrherk,resnr);
CREATE INDEX reservation_point_ix ON reservation (point_resnr);
CREATE INDEX reservation_resnr_index ON reservation (resnr);
CREATE INDEX reservation_rnr_ix ON reservation (activeflag,resnr);
CREATE INDEX reservation_segcode_ix ON reservation (activeflag,segmentcode);
CREATE INDEX reservation_segment_ix ON reservation (segmentcode,resnr);
CREATE TABLE reslin_queasy (
	betriebsnr INT DEFAULT 0,
	key CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	reslinnr INT DEFAULT 1,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX reslin_queasy_argt1_ix ON reslin_queasy (key COLLATE case_insensitive,resnr,reslinnr,number1,number2,number3,date1,date2,char1 COLLATE case_insensitive);
CREATE INDEX reslin_queasy_argt_ix ON reslin_queasy (key COLLATE case_insensitive,reslinnr,number1,number2,char1 COLLATE case_insensitive);
CREATE INDEX reslin_queasy_k_char_ix ON reslin_queasy (betriebsnr,key COLLATE case_insensitive,char1 COLLATE case_insensitive,deci1,logi1,date1,number1,char2 COLLATE case_insensitive);
CREATE INDEX reslin_queasy_k_date_ix ON reslin_queasy (betriebsnr,key COLLATE case_insensitive,date1,char1 COLLATE case_insensitive,number1,deci1,logi1,date2);
CREATE INDEX reslin_queasy_k_int_ix ON reslin_queasy (betriebsnr,key COLLATE case_insensitive,number1,date1,char1 COLLATE case_insensitive,deci1,logi1,number2);
CREATE INDEX reslin_queasy_k_logi_ix ON reslin_queasy (betriebsnr,key COLLATE case_insensitive,logi1,deci1,char1 COLLATE case_insensitive,date1,number1,logi2);
CREATE INDEX reslin_queasy_r_char_ix ON reslin_queasy (betriebsnr,resnr,reslinnr,key COLLATE case_insensitive,char1 COLLATE case_insensitive,logi1,deci1,number1,date1,char2 COLLATE case_insensitive);
CREATE INDEX reslin_queasy_r_date_ix ON reslin_queasy (betriebsnr,resnr,reslinnr,key COLLATE case_insensitive,date1,char1 COLLATE case_insensitive,logi1,deci1,number1,date2);
CREATE INDEX reslin_queasy_r_int_ix ON reslin_queasy (betriebsnr,resnr,reslinnr,key COLLATE case_insensitive,number1,date1,char1 COLLATE case_insensitive,deci1,logi1,number2);
CREATE INDEX reslin_queasy_r_logi_ix ON reslin_queasy (betriebsnr,resnr,reslinnr,key COLLATE case_insensitive,logi1,deci1,char1 COLLATE case_insensitive,date1,number1,logi2);
CREATE TABLE resplan (
	zikatnr INT DEFAULT 0,
	datum DATE,
	anzzim INT[13] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0,0,0,0,0],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX resplan_betr_katdat_ix ON resplan (betriebsnr,zikatnr,datum);
CREATE INDEX resplan_katdat_index ON resplan (zikatnr,datum);
CREATE TABLE rg_reports (
	reportnr INT DEFAULT 0,
	report_group INT DEFAULT 0,
	report_sub INT DEFAULT 0,
	report_title CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	row_dim CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	col_dim CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	out_dim CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	facts_dim CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	form_dim CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	metadata CHARACTER VARYING [20] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','','','','','','','','','','','','',''],
	slice_name CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	view_name CHARACTER VARYING [9] COLLATE case_insensitive DEFAULT ARRAY['','','','','','','','',''],
	created_date DATE,
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag INT DEFAULT 0,
	usr_access CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	overwrite_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	last_updated DATE,
	updated_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	visible_to_group CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ovwrite_by_group CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	usercode CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	num1 INT DEFAULT 0,
	num2 INT DEFAULT 0,
	num3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	_recid serial PRIMARY KEY
);
CREATE INDEX rg_reports_created_ix ON rg_reports (created_by COLLATE case_insensitive);
CREATE INDEX rg_reports_GroupBy_ix ON rg_reports (report_group,created_by COLLATE case_insensitive);
CREATE INDEX rg_reports_Nr_index ON rg_reports (reportnr);
CREATE INDEX rg_reports_nr_ix ON rg_reports (reportnr);
CREATE INDEX rg_reports_NrSubGr_ix ON rg_reports (reportnr,report_sub,report_group);
CREATE INDEX rg_reports_subGr_ix ON rg_reports (report_group,report_sub);
CREATE INDEX rg_reports_subGrBy_ix ON rg_reports (report_group,report_sub,created_by COLLATE case_insensitive);
CREATE INDEX rg_reports_title_ix ON rg_reports (report_title COLLATE case_insensitive);
CREATE INDEX rg_reports_type_ix ON rg_reports (report_group);
CREATE TABLE rmbudget (
	datum DATE,
	zikatnr INT DEFAULT 0,
	logis DECIMAL DEFAULT 0,
	currency CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zimmeranz INT DEFAULT 0,
	res_int INT[3] DEFAULT ARRAY[0,0,0],
	res_char CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	res_deci DECIMAL[3] DEFAULT ARRAY[0,0,0],
	userinit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	sysdate DATE,
	zeit INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX rmbudget_date_ix ON rmbudget (datum);
CREATE INDEX rmbudget_datzikat_ix ON rmbudget (datum,zikatnr);
CREATE TABLE sales (
	gastnr INT DEFAULT 0,
	karteityp INT DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	room_nights INT DEFAULT 0,
	bed_nights INT DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	logisumsatz DECIMAL DEFAULT 0,
	sort_nr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	betrieb_gast INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX sales_argtumsatz ON sales (argtumsatz,sort_nr);
CREATE INDEX sales_bed_nights ON sales (bed_nights,sort_nr);
CREATE INDEX sales_f_b_umsatz ON sales (f_b_umsatz,sort_nr);
CREATE INDEX sales_gastnr ON sales (gastnr,betriebsnr);
CREATE INDEX sales_gesamtumsatz ON sales (gesamtumsatz,sort_nr);
CREATE INDEX sales_logisumsatz ON sales (logisumsatz,sort_nr);
CREATE INDEX sales_room_nights ON sales (room_nights,sort_nr);
CREATE INDEX sales_sonst_umsatz ON sales (sonst_umsatz,sort_nr);
CREATE TABLE salesbud (
	bediener_nr INT DEFAULT 0,
	jahr INT DEFAULT 0,
	monat INT DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	logisumsatz DECIMAL DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	room_nights INT DEFAULT 0,
	id CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX salesbud_user_ix ON salesbud (bediener_nr,jahr,monat);
CREATE TABLE salestat (
	bediener_nr INT DEFAULT 0,
	jahr INT DEFAULT 0,
	monat INT DEFAULT 0,
	logisumsatz DECIMAL DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	f_b_umsatz DECIMAL DEFAULT 0,
	sonst_umsatz DECIMAL DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	room_nights INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX salestat_user_ix ON salestat (bediener_nr,jahr,monat);
CREATE TABLE salestim (
	ber_datum DATE,
	ber_zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	von_monat INT DEFAULT 0,
	von_jahr INT DEFAULT 0,
	bis_monat INT DEFAULT 0,
	bis_jahr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE TABLE segment (
	segmentcode INT DEFAULT 0,
	segmentgrup INT DEFAULT 1,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	vip_level INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX segment_segbez_index ON segment (bezeich COLLATE case_insensitive);
CREATE INDEX segment_segment_index ON segment (betriebsnr,segmentcode);
CREATE TABLE segmentstat (
	segmentcode INT DEFAULT 0,
	datum DATE,
	logis DECIMAL DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	persanz INT DEFAULT 0,
	kind1 INT DEFAULT 0,
	kind2 INT DEFAULT 0,
	gratis INT DEFAULT 0,
	budlogis DECIMAL DEFAULT 0,
	budzimmeranz INT DEFAULT 0,
	budpersanz INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX segmentstat_segment_ix ON segmentstat (betriebsnr,segmentcode,datum);
CREATE TABLE sms_bcaster (
	usrnr INT DEFAULT 0,
	activeflag BOOLEAN DEFAULT False,
	fdate DATE,
	tdate DATE,
	total_point DECIMAL DEFAULT 0,
	used_point DECIMAL DEFAULT 0,
	remain DECIMAL DEFAULT 0,
	sysdate DATE,
	systime INT DEFAULT 0,
	ID INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	logi1 BOOLEAN DEFAULT False,
	date1 DATE,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX sms_bcaster_date_ix ON sms_bcaster (fdate,tdate);
CREATE INDEX sms_bcaster_usedactive_ix ON sms_bcaster (used_point,activeflag);
CREATE INDEX sms_bcaster_usractive_index ON sms_bcaster (usrnr,activeflag);
CREATE TABLE sms_broadcast (
	key INT DEFAULT 0,
	datum DATE,
	zeit INT DEFAULT 0,
	UsrID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	grpnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	phnumber CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	broadcast_msg CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mstatus INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	logi3 BOOLEAN DEFAULT False,
	deci1 DECIMAL DEFAULT 0,
	deci2 DECIMAL DEFAULT 0,
	deci3 DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX sms_broadcast_gastnr_ix ON sms_broadcast (gastnr);
CREATE INDEX sms_broadcast_grp_ix ON sms_broadcast (grpnr);
CREATE INDEX sms_broadcast_id_ix ON sms_broadcast (UsrID COLLATE case_insensitive);
CREATE INDEX sms_broadcast_pr_index ON sms_broadcast (key,datum,zeit,UsrID COLLATE case_insensitive,grpnr,gastnr,phnumber COLLATE case_insensitive);
CREATE TABLE sms_group (
	key INT DEFAULT 0,
	grpnr INT DEFAULT 0,
	grpname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT False,
	fdate DATE,
	tdate DATE,
	ID CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	_recid serial PRIMARY KEY
);
CREATE INDEX sms_group_keyact_ix ON sms_group (key,activeflag);
CREATE INDEX sms_group_keydate_ix ON sms_group (key,fdate,tdate);
CREATE INDEX sms_group_keygr_index ON sms_group (key,grpnr);
CREATE INDEX sms_group_keyid_ix ON sms_group (key,ID COLLATE case_insensitive);
CREATE TABLE sms_groupmbr (
	key INT DEFAULT 0,
	grpnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	Fdate DATE,
	Tdate DATE,
	created_by CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	activeflag BOOLEAN DEFAULT False,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	createdDate DATE,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	logi2 BOOLEAN DEFAULT False,
	date1 DATE,
	date2 DATE,
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX sms_groupmbr_keyact_ix ON sms_groupmbr (key,activeflag);
CREATE INDEX sms_groupmbr_keycreated_ix ON sms_groupmbr (key,createdDate);
CREATE INDEX sms_groupmbr_keydate_ix ON sms_groupmbr (key,Fdate,Tdate);
CREATE INDEX sms_groupmbr_keygrpgast_ix ON sms_groupmbr (key,grpnr,gastnr);
CREATE TABLE sms_received (
	key CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mobile_phone CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	origin_msg CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	firstname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	arrival DATE,
	departure DATE,
	email CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	qty INT DEFAULT 0,
	rmcat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	flag INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	char3 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	number1 INT DEFAULT 0,
	number2 INT DEFAULT 0,
	number3 INT DEFAULT 0,
	date1 DATE,
	date2 DATE,
	date3 DATE,
	zeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	room_str CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	reply_str CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	_recid serial PRIMARY KEY
);
CREATE INDEX sms_received_datum_ix ON sms_received (datum);
CREATE INDEX sms_received_key_ph_flag_ix ON sms_received (key COLLATE case_insensitive,mobile_phone COLLATE case_insensitive,flag);
CREATE INDEX sms_received_key_ix ON sms_received (key COLLATE case_insensitive);
CREATE INDEX sms_received_keydatum_ix ON sms_received (key COLLATE case_insensitive,datum);
CREATE INDEX sms_received_keyphone_ix ON sms_received (key COLLATE case_insensitive,mobile_phone COLLATE case_insensitive);
CREATE TABLE Sourccod (
	source_code INT DEFAULT 0,
	sourcegrup INT DEFAULT 1,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerkung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	vip_level INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX Sourccod_sourcbez_ix ON Sourccod (betriebsnr,bezeich COLLATE case_insensitive);
CREATE INDEX Sourccod_sourccod_index ON Sourccod (betriebsnr,source_code);
CREATE TABLE sources (
	datum DATE,
	logis DECIMAL DEFAULT 0,
	zimmeranz INT DEFAULT 0,
	persanz INT DEFAULT 0,
	budlogis DECIMAL DEFAULT 0,
	budzimmeranz INT DEFAULT 0,
	budpersanz INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	source_code INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX sources_source_ix ON sources (betriebsnr,source_code,datum);
CREATE TABLE sourcetext (
	reftext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	refcontext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	refcode INT DEFAULT 0,
	flag1 INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX sourcetext_idx_code ON sourcetext (refcode);
CREATE INDEX sourcetext_idx_ref ON sourcetext (refcontext COLLATE case_insensitive,reftext COLLATE case_insensitive);
CREATE TABLE telephone (
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	adresse2 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	land CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	wohnort CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	prefix CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telephone CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	anrede CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	Dept CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	vorname CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fax_prefix CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fax CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fax_ext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mobil_prefix CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	mobil_telefon CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	privat_prefix CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telefon_privat CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telex_prefix CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telex CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	telex_ext CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	land_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	departement INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX telephone_bed_ix ON telephone (bediener_nr,name COLLATE case_insensitive,vorname COLLATE case_insensitive);
CREATE INDEX telephone_dep_ix ON telephone (departement,name COLLATE case_insensitive,vorname COLLATE case_insensitive);
CREATE INDEX telephone_name ON telephone (name COLLATE case_insensitive);
CREATE TABLE texte (
	nr INT DEFAULT 1,
	bez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	notes CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	lupdate DATE,
	language INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX texte_lang_nr_ix ON texte (language,nr);
CREATE INDEX texte_nr_index ON texte (nr,language);
CREATE INDEX texte_update_index ON texte (lupdate,nr,language);
CREATE TABLE tisch (
	tischnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	normalbeleg INT DEFAULT 1,
	kellner_nr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	roomcharge BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX tisch_tischnr_ix ON tisch (departement,tischnr);
CREATE TABLE tisch_res (
	tischnr INT DEFAULT 0,
	departement INT DEFAULT 0,
	raum CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	persanz INT DEFAULT 1,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	bis_dat DATE,
	von_dat DATE,
	deci1 DECIMAL DEFAULT 0,
	zeit INT DEFAULT 0,
	bis_zeit INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resnr INT DEFAULT 0,
	char1 CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	logi1 BOOLEAN DEFAULT False,
	number1 INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX tisch_res_dept_date_name_ix ON tisch_res (departement,datum,name COLLATE case_insensitive,zeit);
CREATE INDEX tisch_res_dept_date_raum_name_ix ON tisch_res (departement,datum,raum COLLATE case_insensitive,name COLLATE case_insensitive,zeit);
CREATE INDEX tisch_res_dept_date_razm_ix ON tisch_res (departement,datum,raum COLLATE case_insensitive,tischnr,zeit);
CREATE INDEX tisch_res_dept_date_tisch_ix ON tisch_res (departement,datum,tischnr,zeit);
CREATE INDEX tisch_res_dept_date_zeit_ix ON tisch_res (departement,datum,zeit,name COLLATE case_insensitive);
CREATE INDEX tisch_res_resnr_ix ON tisch_res (resnr,datum,zeit);
CREATE TABLE uebertrag (
	datum DATE,
	betrag DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX uebertrag_betr_date_ix ON uebertrag (betriebsnr,datum);
CREATE INDEX uebertrag_ueber_index ON uebertrag (datum);
CREATE TABLE umsatz (
	datum DATE,
	departement INT DEFAULT 0,
	artnr INT DEFAULT 0,
	anzahl INT DEFAULT 0,
	betrag DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	nettobetrag DECIMAL DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX umsatz_betr_date_ix ON umsatz (betriebsnr,datum,departement,artnr);
CREATE INDEX umsatz_umdate_index ON umsatz (datum,departement,artnr);
CREATE INDEX umsatz_umsatz_index ON umsatz (artnr,departement,datum);
CREATE TABLE waehrung (
	waehrungsnr INT DEFAULT 0,
	wabkurz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ankauf DECIMAL DEFAULT 0,
	verkauf DECIMAL DEFAULT 0,
	geaendert DATE,
	einheit INT DEFAULT 1,
	travelers_chk DECIMAL DEFAULT 0,
	cash_comm DECIMAL DEFAULT 0,
	cheque_comm DECIMAL DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX waehrung_betr_waehr_ix ON waehrung (betriebsnr,wabkurz COLLATE case_insensitive);
CREATE INDEX waehrung_waehr_index ON waehrung (wabkurz COLLATE case_insensitive);
CREATE TABLE wakeup (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	zeit INT DEFAULT 0,
	usre CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	weckdatum DATE,
	weckzeit CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	wakeupdone INT DEFAULT 0,
	language_code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	language INT DEFAULT 0,
	weckzeit_int INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	moddatum DATE,
	moduser INT DEFAULT 0,
	bediener_nr INT DEFAULT 0,
	modzeit INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX wakeup_wake_done_date_time_ix ON wakeup (wakeupdone,weckdatum,weckzeit_int);
CREATE INDEX wakeup_wake_zinr_done_datum_ix ON wakeup (zinr COLLATE case_insensitive,wakeupdone,datum,weckzeit_int);
CREATE INDEX wakeup_weckzeit_ix ON wakeup (weckdatum,weckzeit_int);
CREATE INDEX wakeup_zinr_ix ON wakeup (zinr COLLATE case_insensitive);
CREATE TABLE wgrpdep (
	zknr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX wgrpdep_wgrpdep_zknr_ix ON wgrpdep (departement,zknr);
CREATE TABLE wgrpgen (
	eknr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX wgrpgen_wgrpgen_ix ON wgrpgen (eknr);
CREATE TABLE zimkateg (
	zikatnr INT DEFAULT 0,
	kurzbez CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeichnung CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	maxzimanz INT DEFAULT 1,
	normalbeleg INT DEFAULT 1,
	overbooking INT DEFAULT 0,
	zimanzargt INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	typ INT DEFAULT 0,
	verfuegbarkeit BOOLEAN DEFAULT False,
	zibelstat BOOLEAN DEFAULT False,
	global_kat BOOLEAN DEFAULT False,
	active BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX zimkateg_betr_kurz_ix ON zimkateg (betriebsnr,kurzbez COLLATE case_insensitive);
CREATE INDEX zimkateg_betr_zikatnr_ix ON zimkateg (betriebsnr,zikatnr);
CREATE INDEX zimkateg_kurzbez_ix ON zimkateg (kurzbez COLLATE case_insensitive);
CREATE INDEX zimkateg_zikatnr_ix ON zimkateg (zikatnr);
CREATE TABLE zimmer (
	code CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '1',
	zikatnr INT DEFAULT 0,
	zistatus INT DEFAULT 0,
	zikennz CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	kbezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	himmelsr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	verbindung CHARACTER VARYING [3] COLLATE case_insensitive DEFAULT ARRAY['','',''],
	etage INT DEFAULT 0,
	prioritaet INT DEFAULT 1,
	nebenstelle CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	nebstflag INT DEFAULT 0,
	sollflag INT DEFAULT 0,
	typ INT DEFAULT 0,
	setup INT DEFAULT 0,
	personen INT DEFAULT 0,
	sleeping BOOLEAN DEFAULT False,
	owner_nr INT DEFAULT 0,
	vid_request INT DEFAULT 0,
	vid_actuel INT DEFAULT 0,
	reihenfolge INT DEFAULT 0,
	personal BOOLEAN DEFAULT False,
	wertigkeit INT DEFAULT 1,
	flag1 INT DEFAULT 0,
	flag2 INT DEFAULT 0,
	flag3 INT DEFAULT 0,
	flag4 INT DEFAULT 0,
	fixpreis BOOLEAN DEFAULT False,
	betriebsnr INT DEFAULT 0,
	build CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bediener_nr_stat INT DEFAULT 0,
	features CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	house_status INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX zimmer_betr_zinr_ix ON zimmer (betriebsnr,zinr COLLATE case_insensitive);
CREATE INDEX zimmer_etage_ix ON zimmer (etage,zinr COLLATE case_insensitive);
CREATE INDEX zimmer_features_ix ON zimmer (features COLLATE case_insensitive);
CREATE INDEX zimmer_himmel_index ON zimmer (himmelsr COLLATE case_insensitive,zinr COLLATE case_insensitive);
CREATE INDEX zimmer_katnr_index ON zimmer (zikatnr,zinr COLLATE case_insensitive);
CREATE INDEX zimmer_katpri_index ON zimmer (zikatnr,prioritaet,zinr COLLATE case_insensitive);
CREATE INDEX zimmer_kurz_index ON zimmer (zikennz COLLATE case_insensitive,zinr COLLATE case_insensitive);
CREATE INDEX zimmer_nebst_index ON zimmer (nebenstelle COLLATE case_insensitive);
CREATE INDEX zimmer_soll_index ON zimmer (sollflag,nebstflag);
CREATE INDEX zimmer_type_index ON zimmer (typ,zinr COLLATE case_insensitive);
CREATE INDEX zimmer_vid_actuel_ix ON zimmer (vid_actuel,vid_request);
CREATE INDEX zimmer_vid_request_ix ON zimmer (vid_request,vid_actuel);
CREATE INDEX zimmer_zinr_index ON zimmer (zinr COLLATE case_insensitive);
CREATE TABLE zimmer_book (
	booknr INT DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	ov_date DATE,
	gastnr INT DEFAULT 0,
	active_flag INT DEFAULT 1,
	resstatus INT DEFAULT 2,
	pc_date DATE,
	_recid serial PRIMARY KEY
);
CREATE TABLE zimmer_book_line (
	booknr INT DEFAULT 0,
	ci_date DATE,
	co_date DATE,
	booklinnr INT DEFAULT 0,
	gastnr INT DEFAULT 0,
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	created_date DATE,
	_recid serial PRIMARY KEY
);
CREATE TABLE zimplan (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	datum DATE,
	res_recid INT DEFAULT 0,
	res_recid2 INT DEFAULT 0,
	res_rowid CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	gastnrmember INT DEFAULT 0,
	name CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bemerk CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	resstatus INT DEFAULT 1,
	betriebsnr INT DEFAULT 0,
	ankunft DATE,
	betrieb_gastmem INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX zimplan_betr_zidat_ix ON zimplan (betriebsnr,zinr COLLATE case_insensitive,datum);
CREATE INDEX zimplan_zidat_index ON zimplan (zinr COLLATE case_insensitive,datum);
CREATE TABLE zimpreis (
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	argtnr INT DEFAULT 0,
	startperiode DATE,
	endperiode DATE,
	perspreis DECIMAL[6] DEFAULT ARRAY[0,0,0,0,0,0],
	kindpreis DECIMAL[2] DEFAULT ARRAY[0,0],
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX zimpreis_zipr_indx ON zimpreis (zinr COLLATE case_insensitive,argtnr,startperiode);
CREATE TABLE zinrstat (
	datum DATE,
	zimmeranz INT DEFAULT 0,
	personen INT DEFAULT 0,
	logisumsatz DECIMAL DEFAULT 0,
	gesamtumsatz DECIMAL DEFAULT 0,
	argtumsatz DECIMAL DEFAULT 0,
	zinr CHARACTER VARYING COLLATE case_insensitive DEFAULT '1',
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX zinrstat_betr_zinrdat_ix ON zinrstat (betriebsnr,zinr COLLATE case_insensitive,datum);
CREATE INDEX zinrstat_zinrdat_ix ON zinrstat (datum,zinr COLLATE case_insensitive);
CREATE TABLE zkstat (
	zikatnr INT DEFAULT 0,
	datum DATE,
	zimmeranz INT DEFAULT 0,
	anz100 INT DEFAULT 0,
	personen INT DEFAULT 0,
	arrangement_art INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	anz100argtart INT[9] DEFAULT ARRAY[0,0,0,0,0,0,0,0,0],
	anz_ankunft INT DEFAULT 0,
	anz_abr INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX zkstat_betr_kat_ix ON zkstat (betriebsnr,zikatnr,datum);
CREATE INDEX zkstat_datum_index ON zkstat (datum,zikatnr);
CREATE INDEX zkstat_zikatstat_ix ON zkstat (zikatnr,datum);
CREATE TABLE zwkum (
	zknr INT DEFAULT 0,
	bezeich CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	fibukonto CHARACTER VARYING COLLATE case_insensitive DEFAULT '',
	bankett BOOLEAN DEFAULT False,
	mwstsplit BOOLEAN DEFAULT False,
	hotelrest BOOLEAN DEFAULT False,
	steuercod1 INT DEFAULT 0,
	steuercod2 INT DEFAULT 0,
	departement INT DEFAULT 0,
	betriebsnr INT DEFAULT 0,
	_recid serial PRIMARY KEY
);
CREATE INDEX zwkum_betr_zknr_ix ON zwkum (betriebsnr,departement,zknr);
CREATE INDEX zwkum_zkbez_ix ON zwkum (departement,bezeich COLLATE case_insensitive);
CREATE INDEX zwkum_zknr_ix ON zwkum (departement,zknr);
