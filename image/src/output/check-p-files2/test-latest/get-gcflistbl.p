
DEF TEMP-TABLE t-guest
  FIELD akt-gastnr      AS INTEGER
  FIELD karteityp       AS INTEGER
  FIELD master-gastnr   AS INTEGER
  FIELD pr-flag         AS INTEGER INITIAL 0   /* contRate   */
  FIELD mc-flag         AS LOGICAL INITIAL NO   /* membership */
  FIELD gname           AS CHAR    FORMAT "x(34)" COLUMN-LABEL "Name"
  FIELD adresse         AS CHAR    FORMAT "x(21)" COLUMN-LABEL "Address"
  FIELD steuernr        AS CHAR    FORMAT "x(36)" COLUMN-LABEL "Ref-No"
  FIELD firma           AS CHAR    FORMAT "x(34)" COLUMN-LABEL "Company"
  FIELD namekontakt     AS CHAR    FORMAT "x(24)" COLUMN-LABEL "Name Contact"
  FIELD phonetik3       AS CHAR    FORMAT "x(4)"  COLUMN-LABEL "Sales-ID" 
  FIELD rabatt          AS DECIMAL FORMAT ">9.99" COLUMN-LABEL "Disc(%("
  FIELD endperiode      AS DATE                   COLUMN-LABEL "Expired Date" 
  FIELD firmen-nr       LIKE guest.firmen-nr      COLUMN-LABEL "Comp-No"
  FIELD land            LIKE guest.land
  FIELD wohnort         LIKE guest.wohnort
  FIELD telefon         LIKE guest.telefon
  FIELD plz             LIKE guest.plz
  FIELD geschlecht      LIKE guest.geschlecht
  FIELD ausweis-nr1     LIKE guest.ausweis-nr1
  FIELD gastnr          LIKE guest.gastnr
  FIELD zahlungsart     LIKE guest.zahlungsart FORMAT ">>>>>" 
  FIELD kreditlimit     LIKE guest.kreditlimit
  FIELD bezeich         LIKE segment.bezeich INIT ""
  FIELD alertbox        AS LOGICAL INIT NO
  FIELD warningbox      AS LOGICAL INIT NO
  .

DEF INPUT  PARAMETER case-type      AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER sorttype       AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER lname          AS CHAR             NO-UNDO.
DEF INPUT  PARAMETER fname          AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER first-gastnr   AS INTEGER INIT ?   NO-UNDO.
DEF OUTPUT PARAMETER current-lname  AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER current-fname  AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER TABLE          FOR t-guest.

IF case-type EQ 1 THEN
DO:
    FOR EACH t-guest:
        DELETE t-guest.
    END.
    RUN gcf-listbl.p (1, sorttype, "", "", ?, 
                      OUTPUT first-gastnr, OUTPUT current-lname, 
                      OUTPUT current-fname, OUTPUT TABLE t-guest). 
END.
ELSE
DO:
    RUN gcf-listbl.p (2, sorttype, lname, "", 0,   
                      OUTPUT first-gastnr, OUTPUT current-lname, 
                      OUTPUT current-fname, OUTPUT TABLE t-guest).  
END.
