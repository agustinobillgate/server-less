
DEFINE TEMP-TABLE str-list 
  FIELD h-recid     AS INTEGER INITIAL 0 
  FIELD l-recid     AS INTEGER INITIAL 0 
  FIELD lief-nr     AS INTEGER 
  FIELD billdate    AS DATE 
  FIELD artnr       AS INTEGER 
  FIELD lager-nr    AS INTEGER 
  FIELD docu-nr     AS CHAR 
  FIELD lscheinnr   AS CHAR INITIAL "" 
  FIELD invoice-nr  AS CHAR FORMAT "x(16)" INITIAL "" LABEL "Invoice No" 
  FIELD qty         AS DECIMAL 
  FIELD epreis      AS DECIMAL 
  FIELD warenwert   AS DECIMAL 
  FIELD deci1-3     AS DECIMAL 
  FIELD s           AS CHAR FORMAT "x(135)". 

DEF INPUT  PARAMETER pvILanguage AS INT  NO-UNDO.
DEF INPUT  PARAMETER all-supp    AS LOGICAL.
DEF INPUT  PARAMETER sorttype    AS INT.
DEF INPUT  PARAMETER from-grp    AS INT.
DEF INPUT  PARAMETER store       AS INT.
DEF INPUT  PARAMETER from-date   AS DATE.
DEF INPUT  PARAMETER to-date     AS DATE.
DEF INPUT  PARAMETER show-price  AS LOGICAL.
DEF INPUT  PARAMETER from-supp   AS CHARACTER. /* Add by Michael @ 11/12/2019 for adding search by supplier */
DEF OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-amount AS DECIMAL. 
DEFINE VARIABLE i          AS INTEGER.
DEFINE VARIABLE unit-price AS DECIMAL INITIAL 0.
DEFINE VARIABLE long-digit AS LOGICAL. 

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "cancel-stockin".
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK.
long-digit = htparam.flogical.

IF all-supp AND sorttype = 1 THEN 
DO: 
    IF from-grp = 0 THEN RUN create-list1. 
    ELSE RUN create-list11. 
END. 
ELSE IF NOT all-supp AND sorttype = 1 THEN 
DO: 
    IF from-grp = 0 THEN RUN create-list2. 
    ELSE RUN create-list22. 
END. 
 
ELSE IF all-supp AND sorttype = 2 THEN 
DO: 
    IF from-grp = 0 THEN RUN create-list1a. 
    ELSE RUN create-list11a. 
END. 
ELSE IF NOT all-supp AND sorttype = 2 THEN 
DO: 
    IF from-grp = 0 THEN RUN create-list2a. 
    ELSE RUN create-list22a. 
END. 
 
ELSE IF all-supp AND sorttype = 3 THEN 
DO: 
    IF from-grp = 0 THEN RUN create-list1b. 
    ELSE RUN create-list11b. 
END. 
ELSE IF NOT all-supp AND sorttype = 3 THEN 
DO: 
    IF from-grp = 0 THEN RUN create-list2b. 
    ELSE RUN create-list22b. 
END. 




PROCEDURE create-list1: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    NO-LOCK USE-INDEX lief-op-dat_ix,
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
  
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
      IF lief-nr = 0 THEN lief-nr = l-lieferant.lief-nr. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        lief-nr = l-lieferant.lief-nr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
  
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN 
            ASSIGN
            str-list.warenwert = l-ophis.warenwert
            str-list.deci1-3 = 0.
            /*l-op.deci1[3]. TANYA DULU*/
  
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)").
        
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""), "x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
  
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    AND l-ophis.lager-nr = store 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
  
      IF lief-nr = 0 THEN lief-nr = l-lieferant.lief-nr. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        lief-nr = l-lieferant.lief-nr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
  
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
  
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
  
         str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 29: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1a: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 

DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0  
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    AND l-ophis.lager-nr = store 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
   
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
         str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
  
         str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
  
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 29: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1b: 
DEFINE VARIABLE t-anz     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr   AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR    INITIAL "". 

DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.


  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.artnr BY l-ophis.datum: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
   
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END.
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 AND l-ophis.lager-nr = store NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
         str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
  DO i = 1 TO 6: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list11: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 

DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lief-nr = 0 THEN lief-nr = l-lieferant.lief-nr. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        lief-nr = l-lieferant.lief-nr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    AND l-ophis.lager-nr = store 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lief-nr = 0 THEN lief-nr = l-lieferant.lief-nr. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        lief-nr = l-lieferant.lief-nr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 29: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list11a: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 

DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    AND l-ophis.lager-nr = store 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.

      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
         str-list.s = str-list.s + STRING(usrtime, "x(26)")
            + STRING(reason, "x(24)"). 
  
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 29: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
    + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
    + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list11b: 
DEFINE VARIABLE t-anz     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr   AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR    INITIAL "". 

DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.artnr BY l-ophis.datum: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
   
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr GT 0 AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 AND l-ophis.lager-nr = store NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
         str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
  
         str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
  DO i = 1 TO 6: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list2:        
    DEF VAR    usrid AS CHAR.
    DEF VAR    reason AS CHAR.
    DEF VAR    str1   AS CHAR.
    DEF VAR    usrtime AS CHAR.
    DEF BUFFER usr FOR bediener.
    
  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 

  FIND FIRST l-lieferant WHERE l-lieferant.firma EQ from-supp NO-ERROR. 

  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    NO-LOCK BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      tot-anz = tot-anz + l-ophis.anzahl. 
      tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN  str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.lager-nr = store 
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    NO-LOCK BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      tot-anz = tot-anz + l-ophis.anzahl. 
      tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9").    END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
        + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "G R T T L". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list2a: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 

DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  FIND FIRST l-lieferant WHERE l-lieferant.firma EQ from-supp NO-ERROR. /* Add by Michael @ 11/12/2019 for adding search by supplier */
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
   
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN  str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9").
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
  
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 AND l-ophis.lager-nr = store NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN  str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
  
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 29: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list2b: 
DEFINE VARIABLE t-anz     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr   AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR    INITIAL "". 
DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
 
  FIND FIRST l-lieferant WHERE l-lieferant.firma EQ from-supp NO-ERROR. /* Add by Michael @ 11/12/2019 for adding search by supplier */
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.artnr BY l-ophis.datum: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
   
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
  
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 AND l-ophis.lager-nr = store NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
         str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
         str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
  DO i = 1 TO 6: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list22: 
    DEF VAR    usrid AS CHAR.
    DEF VAR    reason AS CHAR.
    DEF VAR    str1   AS CHAR.
    DEF VAR    usrtime AS CHAR.
    DEF BUFFER usr FOR bediener.
    
  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  FIND FIRST l-lieferant WHERE l-lieferant.firma EQ from-supp NO-ERROR. /* Add by Michael @ 11/12/2019 for adding search by supplier */
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END. 
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      tot-anz = tot-anz + l-ophis.anzahl. 
      tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>9.99"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)").
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.lager-nr = store 
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      tot-anz = tot-anz + l-ophis.anzahl. 
      tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)") 
         + STRING(l-ophis.docu-nr, "x(16)") 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9").
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
  
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list22a: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "".
DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  FIND FIRST l-lieferant WHERE l-lieferant.firma EQ from-supp NO-ERROR. /* Add by Michael @ 11/12/2019 for adding search by supplier */
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
       + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr 
    AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 
    AND l-ophis.lager-nr = store 
    NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK 
    BY l-ophis.datum BY l-ophis.lscheinnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-ophis.lscheinnr. 
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "T O T A L". 
        DO i = 1 TO 29: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
  
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 29: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list22b: 
DEFINE VARIABLE t-anz     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr   AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR    INITIAL "". 

DEF VAR    usrid AS CHAR.
DEF VAR    reason AS CHAR.
DEF VAR    str1   AS CHAR.
DEF VAR    usrtime AS CHAR.
DEF BUFFER usr FOR bediener.

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
 
  FIND FIRST l-lieferant WHERE l-lieferant.firma EQ from-supp NO-ERROR. /* Add by Michael @ 11/12/2019 for adding search by supplier */
 
  IF store = 0 THEN 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.artnr BY l-ophis.datum:
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
   
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
   
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
          str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  ELSE 
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
    AND l-ophis.lief-nr = l-lieferant.lief-nr AND LENGTH(l-ophis.fibukonto) GT 0
    AND l-ophis.op-art = 1 AND l-ophis.lager-nr = store NO-LOCK USE-INDEX lief-op-dat_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-untergrup.bezeich BY l-ophis.datum BY l-ophis.artnr: 
    IF ENTRY(NUM-ENTRIES(l-ophis.fibukonto, ";"),l-ophis.fibukonto,";") EQ "CANCELLED" THEN
    DO:
      reason = "".
      str1   = "".
      usrtime = "".
      DO i = 1 TO NUM-ENTRIES(l-ophis.fibukonto, ";") - 1:
          str1 = ENTRY(i, l-ophis.fibukonto, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE 
            usrtime = str1.
      END.
  
      FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STI" AND l-ophhis.lscheinnr 
        = l-ophis.lscheinnr AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
      IF lscheinnr NE l-untergrup.bezeich THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 17: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
        DO i = 1 TO 6: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.qty = t-anz. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
               + STRING(t-amt, "->>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
        lscheinnr = l-untergrup.bezeich. 
   
        t-anz = 0. 
        t-amt = 0. 
        create str-list. 
      END. 
   
      t-anz = t-anz + l-ophis.anzahl. 
      IF show-price THEN t-amt = t-amt + l-ophis.warenwert. 
      tot-anz = tot-anz + l-ophis.anzahl. 
      IF show-price THEN tot-amount = tot-amount + l-ophis.warenwert. 
      IF show-price THEN unit-price = l-ophis.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-ophis.docu-nr 
        AND str-list.lscheinnr = l-ophis.lscheinnr 
        AND str-list.lager-nr = l-ophis.lager-nr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.artnr = l-ophis.artnr 
        AND str-list.epreis = l-ophis.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-ophis.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert. 
        SUBSTR(str-list.s, 56, 13) = STRING(str-list.qty,"->,>>>,>>9.99"). 
        IF NOT long-digit THEN 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>>,>>>,>>9.99"). 
        ELSE 
        SUBSTR(str-list.s, 69, 15) = STRING(str-list.warenwert,"->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        create str-list. 
        IF AVAILABLE l-ophhis THEN 
        DO: 
          str-list.invoice-nr = l-ophhis.fibukonto. 
         str-list.h-recid = RECID(l-ophhis). 
        END. 
        str-list.l-recid = RECID(l-ophis). 
        str-list.lief-nr = l-ophis.lief-nr. 
        str-list.billdate = l-ophis.datum. 
        str-list.artnr = l-ophis.artnr. 
        str-list.lager-nr = l-ophis.lager-nr. 
        str-list.docu-nr = l-ophis.docu-nr. 
        str-list.lscheinnr = l-ophis.lscheinnr. 
        str-list.qty = l-ophis.anzahl. 
        str-list.epreis = l-ophis.einzelpreis. 
        IF show-price THEN str-list.warenwert = l-ophis.warenwert. 
   
        IF NOT long-digit THEN 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>>,>>>,>>9.99") 
         + STRING(l-lieferant.firma, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-ophis.datum) 
         + STRING(l-ophis.lager-nr, "99") 
         + STRING(l-artikel.artnr, "9999999") 
         + STRING(l-artikel.bezeich, "x(32)") 
         + STRING(l-artikel.traubensort, "x(6)") 
         + STRING(l-ophis.anzahl, "->,>>>,>>9.99") 
         + STRING(str-list.warenwert, "->>,>>>,>>>,>>9") 
         + STRING(l-lieferant.firma, "x(24)"). 
   
        IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.s = str-list.s 
            + STRING(translateExtended ("Direct Pchase   ",lvCAREA,""),"x(16)"). 
        ELSE str-list.s = str-list.s + STRING(l-ophis.docu-nr, "x(16)"). 
        IF NOT long-digit THEN 
        str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s 
         + STRING(l-ophis.lscheinnr, "x(20)") 
         + STRING(unit-price, ">>,>>>,>>>,>>9"). 
        str-list.s = str-list.s + STRING(usrtime, "x(26)")
         + STRING(reason, "x(24)"). 
      END. 
    END.
  END. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(lscheinnr, "x(32)"). 
  DO i = 1 TO 6: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = t-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.99") 
         + STRING(t-amt, "->>,>>>,>>>,>>9"). 
  str-list.s = str-list.s + STRING("T O T A L", "x(18)"). 
 
  create str-list. 
 
  create str-list. 
  DO i = 1 TO 17: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "GRAND TOTAL". 
  DO i = 1 TO 27: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.qty = tot-anz. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>>,>>>,>>9.99"). 
  ELSE 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(tot-amount, "->>,>>>,>>>,>>9"). 
END. 
