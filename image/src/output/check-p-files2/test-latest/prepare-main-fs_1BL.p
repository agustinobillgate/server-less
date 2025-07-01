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

DEFINE TEMP-TABLE t-htparam
    FIELD paramnr       AS INT
    FIELD paramgr       AS INT
    FIELD reihenfolge   AS INT
    FIELD bezeich       AS CHAR
    FIELD fieldtyp      AS INT
    FIELD finteger      AS INT
    FIELD fdecimal      AS DECIMAL
    FIELD fdate         AS DATE
    FIELD flogical      AS LOGICAL
    FIELD fchar         AS CHAR
    FIELD lupdate       AS DATE
    FIELD fdefault      AS CHAR
    /*FIELD betriebsnr    AS INT*/ /*MNAufal 181023 - fix bugs t-htparam already exists*/
    FIELD htp-help      AS CHAR.

/*DEFINE TEMP-TABLE t-htparam LIKE htparam.*/

DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER b1-resline     AS INT.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER bis-datum      AS DATE.
DEF OUTPUT PARAMETER curr-date      AS DATE.
DEF OUTPUT PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER p-900          AS INT.
DEF OUTPUT PARAMETER rsvsort        AS INT.
DEF OUTPUT PARAMETER resnr          AS INT.
DEF OUTPUT PARAMETER resline        AS INT.
DEF OUTPUT PARAMETER search-str     AS CHAR.
DEF OUTPUT PARAMETER guestsort      AS INT.
DEF OUTPUT PARAMETER curr-gastnr    AS INT.
DEF OUTPUT PARAMETER readEquipment  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER bk-func-recid  AS INT.
DEF OUTPUT PARAMETER avail-bk-veran AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER bk-veran-recid AS INT.
DEF OUTPUT PARAMETER bk-veran-resstatus AS INT.
DEF OUTPUT PARAMETER TABLE FOR glist.
DEF OUTPUT PARAMETER TABLE FOR t-htparam.

DEFINE BUFFER b-htparam FOR htparam.
    
IF b1-resnr > 0 THEN 
FOR EACH bk-reser WHERE bk-reser.veran-nr = b1-resnr NO-LOCK BY 
  bk-reser.datum: 
  bis-datum = bk-reser.datum. 
END. 
ELSE bis-datum = to-date. 

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN curr-date = htparam.fdate.                    /* Rulita 180225 | Fixing serverless if avail htparam issue git 606 */
 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN ci-date = htparam.fdate.                      /* Rulita 180225 | Fixing serverless if avail htparam issue git 606 */       

FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN p-900 = htparam.finteger.                     /* Rulita 180225 | Fixing serverless if avail htparam issue git 606 */          

FOR EACH t-htparam:
    DELETE t-htparam.
END.

FOR EACH b-htparam NO-LOCK:
    CREATE t-htparam.
    /*MESSAGE htparam.paramnr
        VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    BUFFER-COPY b-htparam TO t-htparam.
END.

IF b1-resnr NE 0 THEN 
DO: 
  FIND FIRST bk-reser WHERE bk-reser.veran-nr = b1-resnr 
    AND bk-reser.veran-resnr = b1-resline NO-LOCK NO-ERROR. 
  IF AVAILABLE bk-reser THEN rsvsort = bk-reser.resstatus.                        /* Rulita 180225 | Fixing serverless if avail bk-reser issue git 606 */
END. 

RUN create-main-page. 

IF AVAILABLE bk-veran THEN 
    ASSIGN
        avail-bk-veran = YES
        bk-veran-recid = RECID(bk-veran)
        bk-veran-resstatus = bk-veran.resstatus.

IF AVAILABLE bk-func THEN 
    ASSIGN
        bk-func-recid  = RECID(bk-func).


PROCEDURE create-main-page: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE ind AS INTEGER INITIAL 0. 
DEFINE VARIABLE name-contact LIKE guest.name. 
DEFINE buffer htparam-date FOR htparam. 
  FOR EACH glist: 
    DELETE glist. 
  END. 
  
  IF b1-resnr NE 0 THEN 
  DO: 
    resnr = b1-resnr. 
    resline = b1-resline. 
    FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-veran THEN                                                    /* Rulita 180225 | Fixing serverless if avail bk-veran issue git 606 */
    DO:
      FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR. 
  
      search-str = guest.name. 
      guestsort = guest.karteityp. 
      curr-gastnr = guest.gastnr. 
      FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
      IF AVAILABLE akt-kont THEN name-contact = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 
      ELSE name-contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
      FIND FIRST glist WHERE glist.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR. 
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
        glist.rstatus = bk-veran.resstatus.
        glist.fax = guest.fax.
        glist.firmen-nr = guest.firmen-nr.
      END. 
      readEquipment = YES.
      RETURN.
    END.
  END. 
  
  FOR EACH bk-veran WHERE bk-veran.limit-date LE to-date 
    AND bk-veran.activeflag = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = bk-veran.gastnr USE-INDEX gastnr_index 
    NO-LOCK, 
    FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
    AND bk-reser.resstatus LE 3 USE-INDEX vernr-ix NO-LOCK 
    BY guest.karteityp BY guest.name: 
    
    ind = ind + 1. 
 
    IF ind = 1 THEN 
    DO: 
      resnr = bk-veran.veran-nr. 
      resline = bk-reser.veran-seite. 
    END. 
 
    FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE akt-kont THEN name-contact = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 
    ELSE name-contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
    FIND FIRST glist WHERE glist.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR. 
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
 
  FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE bk-veran THEN RETURN. 
  FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK. 
  FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
    AND bk-func.veran-seite = resline NO-LOCK. 
  FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
    AND bk-reser.veran-seite = resline USE-INDEX vernr-ix NO-LOCK.
  
END. 
