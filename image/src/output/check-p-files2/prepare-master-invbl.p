
DEF TEMP-TABLE t-artikel LIKE artikel.
DEFINE TEMP-TABLE t-bill LIKE bill
    FIELD bl-recid       AS INTEGER.

DEFINE TEMP-TABLE t-guest LIKE guest.

DEF TEMP-TABLE f-foinv
    FIELD price-decimal     AS INTEGER
    FIELD briefnr415        AS INTEGER
    FIELD briefnr688        AS INTEGER
    FIELD briefnr2315       AS INTEGER
    FIELD param60           AS INTEGER
    FIELD param145          AS INTEGER
    FIELD param497          AS INTEGER

    FIELD exchg-rate        AS DECIMAL

    FIELD param132          AS CHAR
    FIELD param173          AS CHAR
    FIELD ext-char          AS CHAR
    FIELD curr-local        AS CHAR
    FIELD curr-foreign      AS CHAR
    FIELD b-title           AS CHAR
    FIELD gname             AS CHAR
    
    FIELD param146          AS LOGICAL
    FIELD param199          AS LOGICAL
    FIELD param219          AS LOGICAL
    FIELD double-currency   AS LOGICAL
    FIELD change-date       AS LOGICAL
    FIELD foreign-rate      AS LOGICAL

.

DEF INPUT  PARAMETER inp-rechnr AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER dept       AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR f-foinv.
DEF OUTPUT PARAMETER TABLE FOR t-bill.
DEF OUTPUT PARAMETER TABLE FOR t-guest.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

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
 
FIND FIRST htparam WHERE htparam.paramnr = 219 NO-LOCK.
f-foinv.change-date = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
f-foinv.foreign-rate = htparam.flogical.  
IF foreign-rate OR double-currency THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN f-foinv.exchg-rate = waehrung.ankauf / waehrung.einheit. 
END. 
 
RUN htpchar.p (152, OUTPUT f-foinv.curr-local).
RUN htpchar.p (144, OUTPUT f-foinv.curr-foreign).

RUN htpchar.p (132, OUTPUT f-foinv.param132).
RUN htpchar.p (173, OUTPUT f-foinv.param173).
   
RUN htplogic.p (146, OUTPUT f-foinv.param146).
RUN htplogic.p (199, OUTPUT f-foinv.param199).
RUN htplogic.p (219, OUTPUT f-foinv.param219).

RUN htpint.p (60, OUTPUT f-foinv.param60).
RUN htpint.p (145, OUTPUT f-foinv.param145).

RUN htpint.p (2315, OUTPUT f-foinv.briefnr2315).

FIND FIRST htparam WHERE paramnr = 497 no-lock. 
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN f-foinv.param497 = htparam.finteger. 
END. 

FIND FIRST htparam WHERE paramnr = 2315 no-lock. 
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN f-foinv.briefnr2315 = htparam.finteger. 
END. 

FIND FIRST htparam WHERE paramnr = 415 no-lock. 
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN f-foinv.briefnr415 = htparam.finteger. 
END. 

FIND FIRST htparam WHERE paramnr = 688 no-lock. 
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN f-foinv.briefnr688 = htparam.finteger. 
END. 

FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK. 
f-foinv.b-title = hoteldpt.depart.

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
      f-foinv.gname = guest.NAME. 
  END.
END. 

FOR EACH artikel WHERE 
    artikel.departement = dept 
    AND (
    (artikel.artart = 0 OR artikel.artart = 8 OR artikel.artart = 9)
    OR
    (artikel.artart = 2 OR artikel.artart = 6 OR artikel.artart = 7)
    )
    /*AND 
    (artikel.artart = 0 OR artikel.artart = 8 
    OR (artikel.artart = 9 AND artikel.artgrp NE 0)) */
    AND artikel.activeflag = YES NO-LOCK BY artikel.artnr:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.
