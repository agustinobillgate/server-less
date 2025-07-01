
.
DEFINE TEMP-TABLE t-bill LIKE bill
    FIELD bl-recid       AS INTEGER.

DEFINE TEMP-TABLE t-guest LIKE guest.

DEF TEMP-TABLE f-foinv
    FIELD price-decimal     AS INTEGER
    FIELD briefnr2314       AS INTEGER
    FIELD param60           AS INTEGER
    FIELD param145          AS INTEGER
    FIELD param487          AS INTEGER
    FIELD tel-rechnr        AS INTEGER
    FIELD pos1              AS INTEGER
    FIELD pos2              AS INTEGER
    FIELD ba-dept           AS INTEGER INIT -1

    FIELD exchg-rate        AS DECIMAL
    FIELD max-price         AS DECIMAL

    FIELD param132          AS CHAR
    FIELD ext-char          AS CHAR
    FIELD curr-local        AS CHAR
    FIELD curr-foreign      AS CHAR
    FIELD b-title           AS CHAR
    FIELD gname             AS CHAR
    
    FIELD param219          AS LOGICAL
    FIELD double-currency   AS LOGICAL
    FIELD foreign-rate      AS LOGICAL
    FIELD banquet-flag      AS LOGICAL
    FIELD mc-flag           AS LOGICAL
.

DEFINE INPUT  PARAMETER inp-rechnr AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER curr-department AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR f-foinv.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-guest.
DEFINE INPUT-OUTPUT PARAMETER combo-pf-file1 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-pf-file2 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-gastnr   AS INTEGER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-ledger   AS INTEGER NO-UNDO.

DEFINE VARIABLE golf-license AS CHAR NO-UNDO INIT "NO".

IF combo-gastnr = ? THEN
DO:
    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 155 NO-LOCK. 
    combo-gastnr = vhp.htparam.finteger.
    IF combo-gastnr GT 0 THEN
    DO:
        FIND FIRST guest WHERE guest.gastnr = combo-gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE guest THEN combo-gastnr = 0.
        ELSE ASSIGN combo-ledger = guest.zahlungsart.
        IF combo-ledger GT 0 THEN
        DO:
            FIND FIRST artikel WHERE artikel.artnr = combo-ledger
                AND artikel.departement = 0
                AND artikel.artart = 2 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE artikel THEN
            ASSIGN
                combo-gastnr = 0
                combo-ledger = 0
            .
        END.
        ELSE combo-gastnr = 0.
    END.
    ELSE combo-gastnr = 0.
END.
IF combo-gastnr GT 0 THEN
DO:

    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 339 NO-LOCK. 
    combo-pf-file1 = vhp.htparam.fchar. 
    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 340 NO-LOCK. 
    combo-pf-file2 = vhp.htparam.fchar. 
END.

CREATE f-foinv.
 
FIND FIRST htparam WHERE paramnr = 148 no-lock.  /* Extended CHAR FOR GCF Prog */ 
f-foinv.ext-char = htparam.fchar. 

FIND FIRST htparam WHERE htparam.paramnr = 453 NO-LOCK.
IF htparam.feldtyp = 5 AND htparam.fchar NE "" THEN
    ASSIGN f-foinv.ext-char = f-foinv.ext-char + ";" + htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
f-foinv.price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN f-foinv.double-currency = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
f-foinv.foreign-rate = htparam.flogical.  
IF f-foinv.foreign-rate OR f-foinv.double-currency THEN /* Malik Serverless : foreign-rate OR double-currency -> f-foinv.foreign-rate OR f-foinv.double-currency */
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN f-foinv.exchg-rate = waehrung.ankauf / waehrung.einheit. 
END. 
 
RUN htpdec.p (1086, OUTPUT f-foinv.max-price).

RUN htplogic.p (168, OUTPUT mc-flag).
IF mc-flag THEN
DO:
  RUN htpint.p (337, OUTPUT pos1).
  RUN htpint.p (338, OUTPUT pos2).
  IF pos1 = 0 THEN pos1 = 1. 
END.

FIND FIRST htparam WHERE htparam.paramnr = 985 NO-LOCK.
IF htparam.flogical THEN RUN htpint.p (900, OUTPUT f-foinv.ba-dept).

RUN htpchar.p (152, OUTPUT f-foinv.curr-local).
RUN htpchar.p (144, OUTPUT f-foinv.curr-foreign).
RUN htpchar.p (132, OUTPUT f-foinv.param132).
   
RUN htplogic.p (219, OUTPUT f-foinv.param219).

RUN htpint.p (60, OUTPUT f-foinv.param60).
RUN htpint.p (145, OUTPUT f-foinv.param145).





FIND FIRST htparam WHERE paramnr = 2314 NO-LOCK. 
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN f-foinv.briefnr2314 = htparam.finteger. 
END. 

FIND FIRST htparam WHERE paramnr = 487 NO-LOCK. /* single line opt */
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN f-foinv.param487 = htparam.finteger. 
END. 

FIND FIRST hoteldpt WHERE hoteldpt.num = curr-department NO-LOCK. 
f-foinv.b-title = hoteldpt.depart.

/* SY 14 Sept 2015: golf license */
FIND FIRST htparam WHERE htparam.paramnr = 299 NO-LOCK.
IF htparam.paramgr = 99 AND htparam.flogical THEN golf-license = "YES".
f-foinv.gname = golf-license + CHR(2).

IF inp-rechnr NE 0 THEN 
DO: 
  FIND FIRST bill WHERE bill.rechnr = inp-rechnr NO-LOCK. 
  CREATE t-bill.
  BUFFER-COPY bill TO t-bill.
  ASSIGN t-bill.bl-recid = INTEGER(RECID(bill)).

  FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR.
  IF AVAILABLE guest THEN 
  DO: 
      CREATE t-guest.
      BUFFER-COPY guest TO t-guest.
      f-foinv.gname = f-foinv.gname + guest.NAME. 
  END.
END. 
