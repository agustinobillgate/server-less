DEFINE TEMP-TABLE str-list 
  FIELD artnr       AS INTEGER 
  FIELD qty         AS DECIMAL 
  FIELD warenwert   AS DECIMAL 
  FIELD munit       AS CHAR FORMAT "x(4)"
  FIELD s           AS CHAR FORMAT "x(135)" 
  FIELD fibu        AS CHAR FORMAT "x(12)"
  FIELD fibu-ze     AS CHAR FORMAT "x(40)"
  FIELD addvat-value  AS DECIMAL
  . 


DEF INPUT  PARAMETER pvILanguage    AS INT  NO-UNDO.
DEF INPUT  PARAMETER docu-nr        AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER po-nr          AS CHAR.
DEF INPUT  PARAMETER lief-nr        AS INT.
DEF INPUT  PARAMETER store          AS INT.
DEF INPUT  PARAMETER to-date        AS DATE. 
DEF OUTPUT PARAMETER show-price     AS LOGICAL.
DEF OUTPUT PARAMETER crterm         AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER d-purchase     AS LOGICAL.
DEF OUTPUT PARAMETER unit-price     AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER l-lieferant-firma AS CHAR.
DEF OUTPUT PARAMETER avail-l-lager  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER t-lager-nr     LIKE l-lager.lager-nr.
DEF OUTPUT PARAMETER t-bezeich      LIKE l-lager.bezeich.
DEF OUTPUT PARAMETER TABLE FOR str-list.

/*
DEFINE VARIABLE pvILanguage    AS INT  NO-UNDO.
DEFINE VARIABLE docu-nr        AS CHAR INIT "I100102014".
DEFINE VARIABLE user-init      AS CHAR.
DEFINE VARIABLE po-nr          AS CHAR INIT "P091030006".
DEFINE VARIABLE lief-nr        AS INT INIT 114.
DEFINE VARIABLE store          AS INT.
DEFINE VARIABLE to-date        AS DATE. 
DEFINE VARIABLE show-price     AS LOGICAL.
DEFINE VARIABLE crterm         AS INTEGER INITIAL 0.
DEFINE VARIABLE d-purchase     AS LOGICAL.
DEFINE VARIABLE unit-price     AS DECIMAL INITIAL 0.
DEFINE VARIABLE l-lieferant-firma AS CHAR.
DEFINE VARIABLE avail-l-lager  AS LOGICAL INIT NO.
DEFINE VARIABLE t-lager-nr     LIKE l-lager.lager-nr.
DEFINE VARIABLE t-bezeich      LIKE l-lager.bezeich.
*/

DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-amount AS DECIMAL. 


{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "print-receiving1".

FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
 
FIND FIRST l-orderhdr WHERE l-orderhdr.lief-nr = lief-nr 
  AND l-orderhdr.docu-nr = po-nr NO-LOCK NO-ERROR. 
IF AVAILABLE l-orderhdr THEN crterm = l-orderhdr.angebot-lief[2]. 
 
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
IF AVAILABLE l-lieferant THEN l-lieferant-firma = l-lieferant.firma.
IF store = 0 THEN RUN create-list.
ELSE RUN create-list1. 
 

PROCEDURE create-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE create-it AS LOGICAL.
DEFINE BUFFER b-lop FOR l-op.
 
FOR EACH str-list: 
  delete str-list. 
END. 
  
  tot-anz = 0. 
  tot-amount = 0. 
  i = 0. 
  d-purchase = NO. 
  FIND FIRST b-lop WHERE b-lop.datum EQ to-date 
    AND b-lop.lief-nr = lief-nr AND b-lop.op-art = 1 
    AND b-lop.loeschflag LE 1 AND b-lop.anzahl NE 0 
    AND b-lop.lscheinnr = docu-nr NO-LOCK NO-ERROR.
  IF AVAILABLE b-lop THEN
  DO:
    FOR EACH l-op WHERE l-op.datum EQ to-date 
    AND l-op.lief-nr = lief-nr AND l-op.op-art = 1 
    AND l-op.loeschflag LE 1 AND l-op.anzahl NE 0 
    AND l-op.lscheinnr = docu-nr NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.pos BY l-op.zeit BY l-artikel.bezeich: 
    i = i + 1. 
    IF l-op.docu-nr = l-op.lscheinnr THEN d-purchase = YES. 
    IF i = 1 THEN FIND FIRST l-lager WHERE l-lager.lager-nr 
      = l-op.lager-nr NO-LOCK. 
    tot-anz = tot-anz + l-op.anzahl. 
    IF show-price THEN tot-amount = tot-amount + l-op.warenwert. 
    IF show-price THEN unit-price = l-op.einzelpreis. 
    IF l-op.stornogrund NE "" THEN create-it = YES. 
    ELSE 
    DO: 
      FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR. 
      create-it = NOT AVAILABLE str-list. 
    END. 
    IF NOT create-it THEN 
    DO: 
      str-list.qty = str-list.qty + l-op.anzahl. 
      IF show-price THEN 
        str-list.warenwert = str-list.warenwert + l-op.warenwert. 
      SUBSTR(str-list.s, 32, 15) = STRING(str-list.qty, "->>>,>>>,>>9.99"). 
      SUBSTR(str-list.s, 47, 15) = STRING(str-list.warenwert, "->>>,>>>,>>9.99"). 
    END. 
    ELSE 
    DO: 
      CREATE str-list.
      ASSIGN
        str-list.qty = l-op.anzahl
        str-list.munit = l-artikel.masseinheit
      .

      FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr
             AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN DO:
            ASSIGN str-list.addvat-value = queasy.deci1
            .
      END.

      IF show-price THEN str-list.warenwert = l-op.warenwert. 
      str-list.s = STRING(l-artikel.artnr, "9999999") 
        + STRING(l-artikel.bezeich, "x(24)") 
        + STRING(unit-price, "->>>,>>>,>>9.99") 
        + STRING(l-op.anzahl, "->>,>>9.99") 
        + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
        + STRING(l-op.lscheinnr, "x(20)"). 
      RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-ze). 
    END. 
    END.
  END.
  ELSE
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum EQ to-date 
    AND l-ophis.lief-nr = lief-nr 
    AND l-ophis.op-art = 1 
    /*AND l-ophis.loeschflag LE 1*/ 
    AND l-ophis.anzahl NE 0 
    AND l-ophis.lscheinnr = docu-nr 
    AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    NO-LOCK /*BY l-op.pos BY l-ophis.zeit*/ BY l-artikel.bezeich:
    i = i + 1. 
    IF l-ophis.docu-nr = l-ophis.lscheinnr THEN d-purchase = YES. 
    IF i = 1 THEN FIND FIRST l-lager WHERE l-lager.lager-nr 
      = l-ophis.lager-nr NO-LOCK. 
    tot-anz = tot-anz + l-ophis.anzahl. 
    IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
    IF show-price THEN unit-price = l-ophis.einzelpreis. 
   
    FIND FIRST str-list WHERE str-list.artnr = l-ophis.artnr NO-ERROR. 
    create-it = NOT AVAILABLE str-list. 
    IF NOT create-it THEN 
    DO: 
      str-list.qty = str-list.qty + l-ophis.anzahl. 
      IF show-price THEN 
        str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
      SUBSTR(str-list.s, 32, 15) = STRING(str-list.qty, "->>>,>>>,>>9.99"). 
      SUBSTR(str-list.s, 47, 15) = STRING(str-list.warenwert, "->>>,>>>,>>9.99"). 
    END. 
    ELSE 
    DO: 
      CREATE str-list.
      ASSIGN
        str-list.qty = l-ophis.anzahl
        str-list.munit = l-artikel.masseinheit
      .

      FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr
             AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN DO:
            ASSIGN str-list.addvat-value = queasy.deci1
            .
      END.

      IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
      str-list.s = STRING(l-artikel.artnr, "9999999") 
        + STRING(l-artikel.bezeich, "x(24)") 
        + STRING(unit-price, "->>>,>>>,>>9.99") 
        + STRING(l-ophis.anzahl, "->>,>>9.99") 
        + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
        + STRING(l-ophis.lscheinnr, "x(20)"). 
      RUN convert-fibu(l-ophis.fibukonto, OUTPUT str-list.fibu, OUTPUT str-list.fibu-ze). 
    END. 
  END.
  END.
   
  CREATE str-list. 
  DO i = 1 TO 7: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + translateExtended ("T O T A L",lvCAREA,""). 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 

  IF AVAILABLE l-lager THEN
  ASSIGN
      avail-l-lager = YES
      t-lager-nr = l-lager.lager-nr
      t-bezeich = l-lager.bezeich.
  
END.

PROCEDURE create-list1: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE BUFFER b-lop FOR l-op.
 
FOR EACH str-list: 
  delete str-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  i = 0. 
  d-purchase = NO. 
  FIND FIRST b-lop WHERE b-lop.datum EQ to-date 
  AND b-lop.lief-nr = lief-nr AND b-lop.op-art = 1 
  AND b-lop.loeschflag LE 1 AND b-lop.anzahl NE 0 
  AND b-lop.lager-nr = store 
  AND b-lop.lscheinnr = docu-nr NO-LOCK NO-ERROR.
  IF AVAILABLE b-lop THEN
  DO:
    FOR EACH l-op WHERE l-op.datum EQ to-date 
    AND l-op.lief-nr = lief-nr AND l-op.op-art = 1 
    AND l-op.loeschflag LE 1 AND l-op.anzahl NE 0 
    AND l-op.lager-nr = store 
    AND l-op.lscheinnr = docu-nr NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.pos BY l-op.zeit BY l-artikel.bezeich: 
    i = i + 1. 
    IF l-op.docu-nr = l-op.lscheinnr THEN d-purchase = YES. 
    IF i = 1 THEN FIND FIRST l-lager WHERE l-lager.lager-nr 
      = l-op.lager-nr NO-LOCK. 
    tot-anz = tot-anz + l-op.anzahl. 
    IF show-price THEN tot-amount = tot-amount + l-op.warenwert. 
    IF show-price THEN unit-price = l-op.einzelpreis. 
    IF l-op.stornogrund NE "" THEN create-it = YES. 
    ELSE 
    DO: 
      FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR. 
      create-it = NOT AVAILABLE str-list. 
    END. 
    IF NOT create-it THEN 
    DO: 
      str-list.qty = str-list.qty + l-op.anzahl. 
      IF show-price THEN 
        str-list.warenwert = str-list.warenwert + l-op.warenwert. 
      SUBSTR(str-list.s, 32, 15) = STRING(str-list.qty, "->>>,>>>,>>9.99"). 
      SUBSTR(str-list.s, 47, 14) = STRING(str-list.warenwert, "->>,>>>,>>9.99"). 
    END. 
    ELSE 
    DO: 
      CREATE str-list. 
      ASSIGN
        str-list.qty = l-op.anzahl
        str-list.munit = l-artikel.masseinheit
      .
      FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr
             AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN DO:
            ASSIGN str-list.addvat-value = queasy.deci1
            .
      END.
      IF show-price THEN str-list.warenwert = l-op.warenwert. 
      str-list.s = STRING(l-artikel.artnr, "9999999") 
        + STRING(l-artikel.bezeich, "x(24)") 
        + STRING(unit-price, "->>>,>>>,>>9.99") 
        + STRING(l-op.anzahl, "->>,>>9.99") 
        + STRING(str-list.warenwert, "->>,>>>,>>9.99") 
        + STRING(l-op.lscheinnr, "x(20)"). 
      RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-ze).
    END.
    END.
  END.
  ELSE
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum EQ to-date 
    AND l-ophis.lief-nr = lief-nr 
    AND l-ophis.op-art = 1 
    /*AND l-ophis.loeschflag LE 1*/ 
    AND l-ophis.anzahl NE 0 
    AND l-ophis.lscheinnr = docu-nr 
    AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    NO-LOCK /*BY l-op.pos BY l-ophis.zeit*/ BY l-artikel.bezeich:
    i = i + 1. 
    IF l-ophis.docu-nr = l-ophis.lscheinnr THEN d-purchase = YES. 
    IF i = 1 THEN FIND FIRST l-lager WHERE l-lager.lager-nr 
      = l-ophis.lager-nr NO-LOCK. 
    tot-anz = tot-anz + l-ophis.anzahl. 
    IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
    IF show-price THEN unit-price = l-ophis.einzelpreis.  
    
    FIND FIRST str-list WHERE str-list.artnr = l-ophis.artnr NO-ERROR. 
    create-it = NOT AVAILABLE str-list. 
    IF NOT create-it THEN 
    DO: 
      str-list.qty = str-list.qty + l-ophis.anzahl. 
      IF show-price THEN 
        str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
      SUBSTR(str-list.s, 32, 15) = STRING(str-list.qty, "->>>,>>>,>>9.99"). 
      SUBSTR(str-list.s, 47, 14) = STRING(str-list.warenwert, "->>,>>>,>>9.99"). 
    END. 
    ELSE 
    DO: 
      CREATE str-list. 
      ASSIGN
        str-list.qty = l-ophis.anzahl
        str-list.munit = l-artikel.masseinheit
      .
      FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr
             AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN DO:
            ASSIGN str-list.addvat-value = queasy.deci1
            .
      END.
      IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
      str-list.s = STRING(l-artikel.artnr, "9999999") 
        + STRING(l-artikel.bezeich, "x(24)") 
        + STRING(unit-price, "->>>,>>>,>>9.99") 
        + STRING(l-ophis.anzahl, "->>,>>9.99") 
        + STRING(str-list.warenwert, "->>,>>>,>>9.99") 
        + STRING(l-ophis.lscheinnr, "x(20)"). 
      RUN convert-fibu(l-ophis.fibukonto, OUTPUT str-list.fibu, OUTPUT str-list.fibu-ze).
    END.
  END.
  END.
   
  CREATE str-list. 
  DO i = 1 TO 7: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + translateExtended ("T O T A L",lvCAREA,""). 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
    str-list.qty = tot-anz. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>9.99"). 

  IF AVAILABLE l-lager THEN
  ASSIGN
      avail-l-lager = YES
      t-lager-nr = l-lager.lager-nr
      t-bezeich = l-lager.bezeich.
END. 

PROCEDURE convert-fibu: 
DEFINE INPUT PARAMETER konto AS CHAR. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "".
DEFINE OUTPUT PARAMETER bezeich AS CHAR INITIAL "".
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER.

  FIND FIRST gl-acct WHERE gl-acct.fibukonto = konto NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN RETURN. 
  
  bezeich = gl-acct.bezeich.        /*agung req for web*/

  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO length(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 

