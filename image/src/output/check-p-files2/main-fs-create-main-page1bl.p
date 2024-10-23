
DEFINE TEMP-TABLE glist 
  FIELD gastnr          LIKE guest.gastnr 
  FIELD karteityp       LIKE guest.karteityp 
  FIELD name            AS CHAR FORMAT "x(40)" 
  FIELD telefon         LIKE guest.telefon 
  FIELD land            LIKE guest.land 
  FIELD plz             LIKE guest.plz 
  FIELD wohnort         LIKE guest.wohnort 
  FIELD adresse1        LIKE guest.adresse1 
  FIELD adresse2        LIKE guest.adresse1 
  FIELD adresse3        LIKE guest.adresse1 
  FIELD namekontakt     LIKE guest.namekontakt 
  FIELD von-datum       LIKE bk-reser.datum 
  FIELD bis-datum       LIKE bk-reser.bis-datum 
  FIELD von-zeit        LIKE bk-reser.von-zeit 
  FIELD bis-zeit        LIKE bk-reser.bis-zeit 
  FIELD rstatus         AS INTEGER
  FIELD fax             LIKE guest.fax
  FIELD firmen-nr       LIKE guest.firmen-nr. 

DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER b1-resline     AS INT.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER recid-bk-veran AS INT.
DEF OUTPUT PARAMETER resnr          AS INT.
DEF OUTPUT PARAMETER resline        AS INT.
DEF OUTPUT PARAMETER search-str     AS CHAR.
DEF OUTPUT PARAMETER guestsort      AS INT.
DEF OUTPUT PARAMETER curr-gastnr    AS INT.
DEF OUTPUT PARAMETER readEquipment  AS LOGICAL INIT NO.

DEFINE BUFFER veranb FOR bk-veran.
DEFINE buffer htparam-date FOR htparam.

DEFINE VARIABLE name-contact LIKE guest.name. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE ind AS INTEGER INITIAL 0. 

FOR EACH glist: 
    DELETE glist. 
END. 

FIND FIRST bk-veran WHERE RECID(bk-veran) = recid-bk-veran.
IF b1-resnr NE 0 THEN 
DO: 
    resnr = b1-resnr. 
    resline = b1-resline. 
    FIND FIRST veranb WHERE veranb.veran-nr = resnr NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = veranb.gastnr NO-LOCK. 
 
    search-str = guest.name. 
    guestsort = guest.karteityp. 
    curr-gastnr = guest.gastnr. 

    FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE akt-kont THEN name-contact = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 
    ELSE name-contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
    FIND FIRST glist WHERE glist.gastnr = veranb.gastnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE glist THEN 
    DO: 
      CREATE glist. 
      glist.gastnr = guest.gastnr. 
      glist.karteityp = guest.karteityp. 
      glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
      glist.adresse1 = guest.adresse1. 
      glist.adresse2 = guest.adresse2. 
      glist.adresse3 = guest.adresse3. 
      glist.telefon = guest.telefon. 
      glist.land = guest.land. 
      glist.plz = guest.plz. 
      glist.wohnort = guest.wohnort. 
      glist.namekontakt = name-contact. 
      glist.rstatus = veranb.resstatus.
      glist.fax = guest.fax.
      glist.firmen-nr = guest.firmen-nr.
    END. 
    readEquipment = YES. 
    RETURN. 
END. 

FOR EACH veranb WHERE veranb.limit-date LE to-date 
    AND veranb.activeflag = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = veranb.gastnr USE-INDEX gastnr_index 
    NO-LOCK, 
    FIRST bk-reser WHERE bk-reser.veran-nr = veranb.veran-nr 
    AND bk-reser.resstatus LE 3 USE-INDEX vernr-ix NO-LOCK 
    BY guest.karteityp BY guest.name: 
 
    ind = ind + 1. 
 
    IF ind = 1 THEN 
    DO: 
      resnr = veranb.veran-nr. 
      resline = bk-reser.veran-seite. 
    END. 
 
    FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE akt-kont THEN name-contact = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 
    ELSE name-contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
    FIND FIRST glist WHERE glist.gastnr = veranb.gastnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE glist THEN 
    DO: 
      guestsort = guest.karteityp. 
      CREATE glist. 
      glist.gastnr = guest.gastnr. 
      glist.karteityp = guest.karteityp. 
      glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
      glist.adresse1 = guest.adresse1. 
      glist.adresse2 = guest.adresse2. 
      glist.adresse3 = guest.adresse3. 
      glist.telefon = guest.telefon. 
      glist.land = guest.land. 
      glist.plz = guest.plz. 
      glist.wohnort = guest.wohnort. 
      glist.namekontakt = name-contact. 
      glist.rstatus = bk-veran.resstatus.
      glist.fax = guest.fax.
      glist.firmen-nr = guest.firmen-nr.
    END. 
END. 

readEquipment = YES.
 
FIND FIRST veranb WHERE veranb.veran-nr = resnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE veranb THEN RETURN. 
FIND FIRST guest WHERE guest.gastnr = veranb.gastnr NO-LOCK. 
FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
    AND bk-func.veran-seite = resline NO-LOCK. 
FIND FIRST bk-reser WHERE bk-reser.veran-nr = veranb.veran-nr 
    AND bk-reser.veran-seite = resline USE-INDEX vernr-ix NO-LOCK. 
