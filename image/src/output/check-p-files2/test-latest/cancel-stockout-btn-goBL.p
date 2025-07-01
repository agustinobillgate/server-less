
DEFINE WORKFILE s-list 
  FIELD fibu        AS CHAR 
  FIELD cost-center AS CHAR FORMAT "x(24)" 
  FIELD bezeich     AS CHAR 
  FIELD cost        AS DECIMAL. 

DEFINE TEMP-TABLE str-list 
  FIELD fibu        AS CHAR 
  FIELD other-fibu  AS LOGICAL 
  FIELD op-recid    AS INTEGER 
  FIELD lscheinnr   AS CHAR 
  FIELD s           AS CHAR FORMAT "x(164)". 

DEF INPUT  PARAMETER from-grp AS INT.
DEF INPUT  PARAMETER mi-alloc-chk AS LOGICAL.
DEF INPUT  PARAMETER mi-article-chk AS LOGICAL.
DEF INPUT  PARAMETER mi-docu-chk AS LOGICAL.
DEF INPUT  PARAMETER mi-date-chk AS LOGICAL.

DEF INPUT  PARAMETER from-lager AS INT.
DEF INPUT  PARAMETER to-lager   AS INT.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER from-art   AS INT.
DEF INPUT  PARAMETER to-art     AS INT.
DEF INPUT  PARAMETER show-price AS LOGICAL.
DEF INPUT  PARAMETER cost-acct  AS CHAR.
DEF INPUT  PARAMETER mattype    AS INT.

DEF OUTPUT PARAMETER it-exist AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE tot-anz     AS DECIMAL.
DEFINE VARIABLE tot-amount  AS DECIMAL.
DEFINE VARIABLE preis       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE wert        AS DECIMAL INITIAL 0. 

DEFINE VARIABLE long-digit  AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

IF from-grp = 0 THEN 
DO: 
    IF mi-alloc-chk = YES THEN RUN create-list.
    ELSE IF mi-article-chk = YES 
      THEN RUN create-listA. 
    ELSE IF mi-docu-chk = YES 
      THEN RUN create-listB. 
    ELSE IF mi-date-chk = YES 
      THEN RUN create-listC. 
END. 
ELSE 
DO: 
    IF mi-alloc-chk = YES THEN RUN create-list1. 
    ELSE IF mi-article-chk = YES 
      THEN RUN create-list1A. 
    ELSE IF mi-docu-chk = YES 
      THEN RUN create-list1B. 
    ELSE IF mi-date-chk = YES 
      THEN RUN create-list1C. 
END. 


PROCEDURE create-listA: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE buffer gl-acct1 FOR gl-acct. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.
 
status default "Processing...". 
 
it-exist = NO. 
FOR EACH str-list: 
  delete str-list. 
END. 
FOR EACH s-list: 
  delete s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 
    usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2  NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
      BY l-artikel.bezeich BY l-op.datum 
      BY SUBSTR(l-op.lscheinnr,4,12): 

      FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".

      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.
 
      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF lschein = "" THEN lschein = l-op.lscheinnr. 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF curr-artnr = 0 THEN curr-artnr = l-op.artnr. 
      IF (curr-artnr NE l-op.artnr) AND t-anz NE 0 THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        curr-artnr = l-op.artnr. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
         create s-list. 
         s-list.fibu = fibukonto. 
         s-list.bezeich = cost-bezeich. 
         IF cc-code NE 0 THEN s-list.bezeich = 
           STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.fibu = fibukonto. 
        str-list.other-fibu = other-fibu. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
        ELSE str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">,>>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-listB: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE buffer gl-acct1 FOR gl-acct. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.
 
STATUS default "Processing...". 
 
it-exist = NO. 
FOR EACH str-list: 
  delete str-list. 
END. 
FOR EACH s-list: 
  delete s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 
    usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2  NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
      BY SUBSTR(l-op.lscheinnr,4,12) BY l-artikel.bezeich: 
        
      FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".
           
      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.

      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF lschein = "" THEN lschein = l-op.lscheinnr. 
      IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        curr-artnr = l-op.artnr. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
         create s-list. 
         s-list.fibu = fibukonto. 
         s-list.bezeich = cost-bezeich. 
         IF cc-code NE 0 THEN s-list.bezeich = 
           STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.fibu = fibukonto. 
        str-list.other-fibu = other-fibu. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
        ELSE str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>,>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)").
      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 14: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-listC: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE buffer gl-acct1 FOR gl-acct. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.
 
status default "Processing...". 
 
it-exist = NO. 
FOR EACH str-list: 
  delete str-list. 
END. 
FOR EACH s-list: 
  delete s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 
    usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2  NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
      BY l-op.datum BY l-artikel.bezeich: 
 
      FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".
           
      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.

      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF datum = ? THEN datum = l-op.datum. 
      IF (datum NE l-op.datum) AND t-anz NE 0 THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        datum = l-op.datum. 
        curr-artnr = l-op.artnr. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
         create s-list. 
         s-list.fibu = fibukonto. 
         s-list.bezeich = cost-bezeich. 
         IF cc-code NE 0 THEN s-list.bezeich = 
           STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.fibu = fibukonto. 
        str-list.other-fibu = other-fibu. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
        ELSE str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>,>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE buffer gl-acct1 FOR gl-acct. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE curr-fibu AS CHAR INITIAL "". 

DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.
status default "Processing...". 
 
it-exist = NO. 
FOR EACH str-list: 
  delete str-list. 
END. 
FOR EACH s-list: 
  delete s-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".
/*  calculate the outgoing stocks within the given periods */ 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2  NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
      BY l-op.stornogrund BY l-ophdr.fibukonto BY l-artikel.bezeich 
      BY l-op.datum: 
 
        FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".
           
      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.

      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF lschein = "" THEN lschein = l-op.lscheinnr. 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF curr-fibu = "" THEN curr-fibu = fibukonto. 
      IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
/*    IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        curr-fibu = fibukonto. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(24)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
         create s-list. 
         s-list.fibu = fibukonto. 
         s-list.bezeich = cost-bezeich. 
         IF cc-code NE 0 THEN s-list.bezeich = 
           STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.fibu = fibukonto. 
        str-list.other-fibu = other-fibu. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 

        ELSE str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>,>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
DEFINE VARIABLE curr-fibu AS CHAR INITIAL "".

DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.
DEFINE buffer gl-acct1 FOR gl-acct. 
 
status default "Processing...". 
 
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 
    usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum EQ from-grp NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
      AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
      NO-LOCK BY l-op.stornogrund BY l-ophdr.fibukonto 
      BY l-op.datum BY l-artikel.bezeich: 
 
      FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".
           
      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.

      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF lschein = "" THEN lschein = l-op.lscheinnr. 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF curr-fibu = "" THEN curr-fibu = fibukonto. 
      IF curr-fibu NE fibukonto AND t-anz NE 0 THEN 
/*    IF (lschein NE l-op.lscheinnr) AND t-anz NE 0 THEN */ 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        curr-fibu = fibukonto. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.fibu = fibukonto. 
          s-list.bezeich = cost-bezeich. 
          IF cc-code NE 0 THEN s-list.bezeich = 
            STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.other-fibu = other-fibu. 
        str-list.fibu = fibukonto. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>,>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1A: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
DEFINE VARIABLE grp2 AS INTEGER INITIAL 1.
DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.

DEFINE buffer gl-acct1 FOR gl-acct. 
    
status default "Processing...". 
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 
    usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".

    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum EQ from-grp NO-LOCK, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
      AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
      NO-LOCK BY l-op.datum BY l-artikel.bezeich 
      BY SUBSTR(l-op.lscheinnr,4,12): 
 
      FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".
           
      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.

      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF lschein = "" THEN lschein = l-op.lscheinnr. 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF curr-artnr = 0 THEN curr-artnr = l-op.artnr. 
      IF curr-artnr NE l-op.artnr AND t-anz NE 0 THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        curr-artnr = l-op.artnr. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.fibu = fibukonto. 
          s-list.bezeich = cost-bezeich. 
          IF cc-code NE 0 THEN s-list.bezeich = 
            STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.other-fibu = other-fibu. 
        str-list.fibu = fibukonto. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>,>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1B: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 

DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.
DEFINE buffer gl-acct1 FOR gl-acct. 
  
  status default "Processing...". 
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 
     usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum EQ from-grp NO-LOCK, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
      AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
      BY SUBSTR(l-op.lscheinnr,4,12) BY l-artikel.bezeich: 

      FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".
           
      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.
 
      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF lschein = "" THEN lschein = l-op.lscheinnr. 
      IF lschein NE l-op.lscheinnr AND t-anz NE 0 THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        curr-artnr = l-op.artnr. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.fibu = fibukonto. 
          s-list.bezeich = cost-bezeich. 
          IF cc-code NE 0 THEN s-list.bezeich = 
            STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.other-fibu = other-fibu. 
        str-list.fibu = fibukonto. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>,>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 

      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1C: 
DEFINE VARIABLE t-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lschein AS CHAR INITIAL "". 
DEFINE VARIABLE datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(30)". 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE cc-code AS INTEGER FORMAT "9999 ". 
DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 

DEFINE VARIABLE usrid  AS CHAR.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE reason AS CHAR.
DEFINE VARIABLE str-time AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE acct-no AS CHAR.
DEFINE BUFFER usr FOR bediener.
DEFINE buffer gl-acct1 FOR gl-acct. 

status default "Processing...". 
  it-exist = NO. 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  tot-anz = 0. 
  tot-amount = 0. 
/*  calculate the outgoing stocks within the given periods */ 
    do-it = YES. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    do-it = YES. 
    curr-artnr = 0. 
    usrid = "".
    reason = "".
    str-time = "".
    acct-no = "".

    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.anzahl NE 0 AND l-op.op-art = 3 
      AND l-op.loeschflag = 2 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum EQ from-grp NO-LOCK, 
      FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
      AND l-ophdr.lscheinnr = l-op.lscheinnr 
      AND l-ophdr.fibukonto NE "" NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
      AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
      BY l-op.datum BY l-artikel.bezeich: 
 
      FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
      IF AVAILABLE usr THEN usrid = usr.userinit.
      ELSE usrid = "??".
           
      DO i = 1 TO NUM-ENTRIES(l-op.stornogrund, ";"):
          str1 = ENTRY(i, l-op.stornogrund, ";").
          IF ENTRY(1, str1, ":") = "Reason" THEN
              reason = ENTRY(2, str1, ":").
          ELSE IF ENTRY(1, str1, ":") = "Time" THEN
              str-time = STRING(INTEGER(ENTRY(2, str1, ":")), "HH:MM:SS").
          ELSE
              acct-no = str1.
      END.

      IF show-price THEN 
      DO: 
        preis = l-op.einzelpreis. 
        wert = l-op.warenwert. 
      END. 
 
      it-exist = YES. 
      other-fibu = NO. 
      IF acct-no NE "" THEN 
      DO: 
        FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
      END. 
      IF other-fibu THEN 
        RUN get-costcenter-code(gl-acct1.fibukonto, OUTPUT cc-code). 
      ELSE RUN get-costcenter-code(gl-acct.fibukonto, OUTPUT cc-code). 
 
      IF other-fibu THEN 
      DO: 
        fibukonto = gl-acct1.fibukonto. 
        cost-bezeich = gl-acct1.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
      ELSE 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-bezeich = gl-acct.bezeich. 
        IF cost-acct = "" THEN create-it = YES. 
        ELSE create-it = (cost-acct = fibukonto). 
      END. 
 
      IF datum = ? THEN datum = l-op.datum. 
      IF datum NE l-op.datum AND t-anz NE 0 THEN 
      DO: 
        create str-list. 
        DO i = 1 TO 45: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + "Subtotal ". 
        DO i = 1 TO 23: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
        DO i = 1 TO 14: 
          str-list.s = str-list.s + " ". 
        END. 
        IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
        t-anz = 0. 
        t-val = 0. 
        create str-list. 
        lschein = l-op.lscheinnr. 
        datum = l-op.datum. 
        curr-artnr = l-op.artnr. 
      END. 
 
      IF do-it THEN 
      DO: 
        create str-list. 
        create str-list. 
        str-list.s = STRING("", "x(8)") + STRING(l-lager.bezeich, "x(30)"). 
        create str-list. 
        do-it = NO. 
      END. 
 
      IF create-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.fibu = fibukonto NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.fibu = fibukonto. 
          s-list.bezeich = cost-bezeich. 
          IF cc-code NE 0 THEN s-list.bezeich = 
            STRING(cc-code,"9999 ") + s-list.bezeich. 
        END. 
        s-list.cost = s-list.cost + wert. 
        t-anz = t-anz + l-op.anzahl. 
        t-val = t-val + wert. 
        tot-anz = tot-anz + l-op.anzahl. 
        tot-amount = tot-amount + wert. 
        create str-list. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.other-fibu = other-fibu. 
        str-list.fibu = fibukonto. 
        str-list.op-recid = RECID(l-op). 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>>,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
        ELSE 
        str-list.s = STRING(l-op.datum) 
                 + STRING(s-list.bezeich, "x(30)") 
                 + STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(32)") 
                 + STRING(l-op.anzahl, "->,>>>,>>9.999") 
                 + STRING(preis, ">>,>>>,>>>,>>9") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(l-op.lscheinnr, "x(12)")
                 + STRING(usrid, "x(2)")
                 + STRING(str-time, "x(8)")
                 + STRING(reason, "x(24)"). 
      END. 
    END. 
  END. 
 
  IF t-anz NE 0 THEN 
  DO: 
    create str-list. 
    DO i = 1 TO 45: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + "Subtotal ". 
    DO i = 1 TO 23: 
      str-list.s = str-list.s + " ". 
    END. 
    str-list.s = str-list.s + STRING(t-anz, "->,>>>,>>9.999"). 
    DO i = 1 TO 14: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>9.99"). 
    ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>9"). 
    create str-list. 
  END. 
 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 23: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING(tot-anz, "->,>>>,>>9.999"). 
  DO i = 1 TO 12: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
 
  create str-list. 
  create str-list. 
  create str-list. 
  str-list.s = STRING("","x(8)") 
    + STRING("SUMMARY OF EXPENSES", "x(30)"). 
  tot-amount = 0. 
  FOR EACH s-list BY s-list.bezeich: 
    create str-list. 
    IF NOT long-digit THEN 
    str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->>,>>>,>>9.99"). 
    ELSE str-list.s = STRING("","x(8)") 
      + STRING("", "x(30)") 
      + STRING("", "x(7)") 
      + STRING(s-list.bezeich, "x(32)") 
      + STRING(0, "->>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>") 
      + STRING(s-list.cost, "->,>>>,>>>,>>9"). 
    tot-amount = tot-amount + s-list.cost. 
  END. 
  create str-list. 
  DO i = 1 TO 45: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + "T O T A L". 
  DO i = 1 TO 49: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
  str-list.s = str-list.s + STRING(tot-amount, "->>,>>>,>>9.99"). 
  ELSE str-list.s = str-list.s + STRING(tot-amount, "->,>>>,>>>,>>9"). 
END. 


PROCEDURE get-costcenter-code: 
DEFINE INPUT PARAMETER fibukonto AS CHAR. 
DEFINE OUTPUT PARAMETER cc-code AS INTEGER INITIAL 0. 
  FIND FIRST PARAMETERs WHERE progname = "CostCenter" 
    AND section = "Alloc" AND varname GT "" 
    AND PARAMETERs.vstring = fibukonto NO-LOCK NO-ERROR. 
  IF AVAILABLE PARAMETERs THEN cc-code = INTEGER(PARAMETERs.varname). 
END. 

