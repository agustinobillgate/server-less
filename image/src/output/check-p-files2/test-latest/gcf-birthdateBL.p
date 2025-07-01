
DEFINE TEMP-TABLE birth-list 
  FIELD name2       AS CHAR FORMAT "x(36)" 
  FIELD geburtdatum AS DATE FORMAT "99/99/9999" 
  FIELD ankunft1    AS DATE 
  FIELD abreise1    AS DATE 
  FIELD zinr        LIKE zimmer.zinr
  FIELD adresse     AS CHAR FORMAT "x(40)" 
  FIELD wohnort     AS CHAR FORMAT "x(32)". 

DEF INPUT PARAMETER from-date AS INTEGER NO-UNDO.
DEF INPUT PARAMETER to-date   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-age  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER to-age    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER sorttype  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR birth-list.

RUN age-list.

PROCEDURE age-list: 
  IF sorttype = 1 THEN 
  DO: 
    FOR EACH guest WHERE guest.karteityp = 0 AND guest.gastnr GT 0 
      AND guest.name GT "" AND guest.vorname1 GE "" 
      AND geburtdatum1 NE ? NO-LOCK USE-INDEX ganame_index: 
      IF (MONTH(geburtdatum1) * 100 + DAY(geburtdatum1)) GE from-date 
        AND (MONTH(geburtdatum1) * 100 + DAY(geburtdatum1)) LE to-date 
        AND (- YEAR(geburtdatum1) + YEAR(today)) GE from-age 
        AND (- YEAR(geburtdatum1) + YEAR(today)) LE to-age THEN 
      DO: 
        CREATE birth-list. 
        ASSIGN
          birth-list.name        = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1
          birth-list.geburtdatum = guest.geburtdatum1 
          birth-list.adresse     = guest.adresse1 + " " + guest.adresse2 
            + " " + guest.adresse3 + CHR(3) + guest.email-adr  + CHR(3) + guest.telefon + CHR(3) + guest.mobil-telefon  /*Eko*/
          birth-list.wohnort     = guest.land + " - " + guest.plz 
            + " " + guest.wohnort
        . 
        IF guest.resflag = 2 THEN 
        DO: 
          FIND FIRST res-line WHERE res-line.gastnrmember = guest.gastnr 
            AND (res-line.resstatus = 6 OR res-line.resstatus = 13) NO-LOCK NO-ERROR. 
          IF AVAILABLE res-line THEN 
          ASSIGN 
            birth-list.ankunft = res-line.ankunft
            birth-list.abreise = res-line.abreise 
            birth-list.zinr    = res-line.zinr
          . 
        END. 
      END. 
    END. 
  END. 
  ELSE
  FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
    AND res-line.active-flag = 1 NO-LOCK: 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
      AND guest.geburtdatum1 NE ? NO-LOCK NO-ERROR. 
    IF AVAILABLE guest THEN 
    DO: 
      IF (MONTH(geburtdatum1) * 100 + DAY(geburtdatum1)) GE from-date 
        AND (MONTH(geburtdatum1) * 100 + DAY(geburtdatum1)) LE to-date 
        AND (- YEAR(geburtdatum1) + YEAR(TODAY)) GE from-age 
        AND (- YEAR(geburtdatum1) + YEAR(TODAY)) LE to-age THEN 
      DO: 
        CREATE birth-list. 
        ASSIGN
            birth-list.name    = guest.name + ", " + guest.vorname1 
              + " " + guest.anrede1
            birth-list.geburtdatum = guest.geburtdatum1 
            birth-list.adresse = guest.adresse1 + " " + guest.adresse2 
              + " " + guest.adresse3 + CHR(3) + guest.email-adr + CHR(3) + guest.telefon + CHR(3) + guest.mobil-telefon  /*Eko*/
            birth-list.wohnort = guest.land + " - " + guest.plz 
              + " " + guest.wohnort 
            birth-list.ankunft = res-line.ankunft
            birth-list.abreise = res-line.abreise 
            birth-list.zinr = res-line.zinr
        . 
      END. 
    END. 
  END.
END. 
