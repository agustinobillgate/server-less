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
  FIELD firmen-nr       LIKE guest.firmen-nr. . 

DEFINE TEMP-TABLE ol 
  FIELD STR AS CHAR FORMAT "x(120)". 

DEF INPUT  PARAMETER TABLE FOR glist.
DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER b1-resline     AS INT.
DEF INPUT  PARAMETER search-str     AS CHAR.
DEF INPUT  PARAMETER curr-gastnr    AS INT.
DEF INPUT  PARAMETER guestsort      AS INT.
DEF INPUT  PARAMETER rsvsort        AS INT.
DEF INPUT  PARAMETER to-name        AS CHAR.
DEF OUTPUT PARAMETER op-flag        AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR ol.

FOR EACH ol: 
    DELETE ol. 
END. 
FIND FIRST bk-reser WHERE bk-reser.veran-nr = b1-resnr 
    AND bk-reser.veran-resnr = b1-resline NO-LOCK. 
IF b1-resnr NE 0 THEN 
DO: 
    FIND FIRST bk-veran WHERE bk-veran.veran-nr = b1-resnr NO-LOCK. 
    FIND FIRST glist WHERE glist.gastnr = bk-veran.gastnr NO-LOCK. 
    CREATE ol. 
    ol.str = STRING(glist.name,"x(40)") + STRING(glist.telefon,"x(15)") + 
      STRING(bk-reser.datum,"99/99/9999") + STRING(bk-reser.bis-datum,"99/99/9999") + 
      STRING(bk-reser.von-zeit,"99:99") + STRING(bk-reser.bis-zeit,"99:99"). 
    op-flag = 1.
    RETURN. 
END. 
IF search-str = "" AND curr-gastnr = 0 THEN 
DO: 
    IF guestsort LT 3 THEN 
    DO: 
      FOR EACH glist WHERE glist.karteityp = guestsort NO-LOCK BY glist.name: 
        FOR EACH bk-veran WHERE bk-veran.gastnr = glist.gastnr 
          AND bk-veran.activeflag = 0 USE-INDEX gastnr_ix NO-LOCK: 
          FOR EACH bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr AND bk-reser.resstatus = rsvsort 
          USE-INDEX vernr-ix NO-LOCK: 
            CREATE ol. 
            ol.str = STRING(glist.name,"x(40)") + STRING(glist.telefon,"x(15)") + 
                     STRING(bk-reser.datum,"99/99/9999") + STRING(bk-reser.bis-datum,"99/99/9999") + 
                     STRING(bk-reser.von-zeit,"99:99") + STRING(bk-reser.bis-zeit,"99:99"). 
          END. 
        END. 
      END. 
    END. 
    op-flag = 2.
END. 
ELSE IF search-str NE "" AND curr-gastnr = 0 THEN 
DO: 
    FOR EACH glist WHERE glist.karteityp = guestsort AND 
    glist.name GE search-str AND glist.name LE to-name NO-LOCK BY glist.name: 
      FOR EACH bk-veran WHERE bk-veran.gastnr = glist.gastnr 
        AND bk-veran.activeflag = 0 USE-INDEX gastnr_ix NO-LOCK: 
        FOR EACH bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr AND bk-reser.resstatus = rsvsort 
        USE-INDEX vernr-ix NO-LOCK: 
          CREATE ol. 
          ol.str = STRING(glist.name,"x(40)") + STRING(glist.telefon,"x(15)") + 
                   STRING(bk-reser.datum,"99/99/9999") + STRING(bk-reser.bis-datum,"99/99/9999") + 
                   STRING(bk-reser.von-zeit,"99:99") + STRING(bk-reser.bis-zeit,"99:99"). 
        END. 
      END. 
    END. 
    op-flag = 3.
END. 
ELSE IF curr-gastnr NE 0 THEN 
DO: 
    FOR EACH glist WHERE glist.karteityp = guestsort AND glist.gastnr GE curr-gastnr 
    NO-LOCK BY glist.name: 
      FOR EACH bk-veran WHERE bk-veran.gastnr = glist.gastnr 
        AND bk-veran.activeflag = 0 USE-INDEX gastnr_ix NO-LOCK: 
        FOR EACH bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr AND bk-reser.resstatus = rsvsort 
        USE-INDEX vernr-ix NO-LOCK: 
          CREATE ol. 
          ol.str = STRING(glist.name,"x(40)") + STRING(glist.telefon,"x(15)") + 
                   STRING(bk-reser.datum,"99/99/9999") + STRING(bk-reser.bis-datum,"99/99/9999") + 
                   STRING(bk-reser.von-zeit,"99:99") + STRING(bk-reser.bis-zeit,"99:99"). 
        END. 
      END. 
    END. 
    op-flag = 4.
END. 
