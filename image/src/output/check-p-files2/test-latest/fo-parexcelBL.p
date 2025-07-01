DEFINE TEMP-TABLE w1 
  FIELD nr          AS INTEGER 
  FIELD varname     AS CHAR 
  FIELD main-code   AS INTEGER   /* eg. 805 FOR AVAILABLE room */ 
  FIELD artnr       AS INTEGER 
  FIELD s-artnr     AS CHARACTER 
  FIELD dept        AS INTEGER 
  FIELD grpflag     AS INTEGER INITIAL 0 
  FIELD done        AS LOGICAL INITIAL NO 
  FIELD bezeich     AS CHAR 
  FIELD int-flag    AS LOGICAL INITIAL NO 
 
  FIELD tday        AS DECIMAL INITIAL 0 
  FIELD saldo       AS DECIMAL INITIAL 0 
  FIELD lastmon     AS DECIMAL INITIAL 0 
  FIELD lastyr      AS DECIMAL INITIAL 0 
  FIELD lytoday     AS DECIMAL INITIAL 0 
  FIELD ytd-saldo   AS DECIMAL INITIAL 0 
  FIELD lytd-saldo  AS DECIMAL INITIAL 0 
 
  FIELD tbudget     AS DECIMAL INITIAL 0 
  FIELD budget      AS DECIMAL INITIAL 0 
  FIELD lm-budget   AS DECIMAL INITIAL 0 
  FIELD ly-budget   AS DECIMAL INITIAL 0 
  FIELD ytd-budget  AS DECIMAL INITIAL 0 
  FIELD lytd-budget AS DECIMAL INITIAL 0. 
 
DEFINE TEMP-TABLE w2 
  FIELD val-sign    AS INTEGER INITIAL 1 
  FIELD nr1         AS INTEGER 
  FIELD nr2         AS INTEGER. 


DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER ytd-flag     AS LOGICAL.
DEFINE INPUT PARAMETER jan1         AS DATE.
DEFINE INPUT PARAMETER Ljan1        AS DATE.
DEFINE INPUT PARAMETER Lfrom-date   AS DATE.
DEFINE INPUT PARAMETER Lto-date     AS DATE.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER start-date   AS DATE.
DEFINE INPUT PARAMETER lytd-flag    AS LOGICAL.
DEFINE INPUT PARAMETER lmtd-flag    AS LOGICAL.
DEFINE INPUT PARAMETER pmtd-flag    AS LOGICAL.
DEFINE INPUT PARAMETER Pfrom-date   AS DATE.
DEFINE INPUT PARAMETER Pto-date     AS DATE.
DEFINE INPUT PARAMETER lytoday-flag AS LOGICAL.
DEFINE INPUT PARAMETER lytoday      AS DATE.
DEFINE INPUT PARAMETER foreign-flag AS LOGICAL.
DEFINE INPUT PARAMETER budget-flag  AS LOGICAL.

DEFINE OUTPUT PARAMETER error-nr       AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str        AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR w1.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR w2.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fo-parexcel".

DEFINE VARIABLE frate           AS DECIMAL INITIAL 1.
DEFINE VARIABLE prog-error      AS LOGICAL INITIAL NO.
DEFINE VARIABLE serv-vat        AS LOGICAL. 
DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE buffer segmbuff FOR segmentstat. 

FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
serv-vat = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

RUN fill-value.

PROCEDURE fill-value: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE buffer curr-child FOR w1. 
DEFINE VARIABLE val-sign AS INTEGER. 
DEFINE buffer ww1 FOR w1. 
DEFINE buffer ww2 FOR w1. 
 
  FOR EACH ww1 WHERE ww1.grpflag = 0: 
    FIND FIRST ww2 WHERE ww2.varname = ww1.varname 
      AND RECID(ww1) NE RECID(ww2) NO-LOCK NO-ERROR. 
    IF AVAILABLE ww2 THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Duplicate name found : ",lvCAREA,"") + ww2.varname.
      error-nr = -1. 
      RETURN. 
    END. 
  END. 
 
  FOR EACH ww1 WHERE ww1.grpflag = 0: 
    FIND FIRST ww2 WHERE ww2.varname = ww1.varname 
      AND RECID(ww1) NE RECID(ww2) NO-LOCK NO-ERROR. 
    IF AVAILABLE ww2 THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Duplicate name found : ",lvCAREA,"") + ww2.varname.
      error-nr = -1. 
      RETURN. 
    END. 
    ELSE IF ww1.main-code = 288 THEN RUN fill-totroom(RECID(ww1)). 
    IF ww1.main-code = 805 THEN RUN fill-rmavail(RECID(ww1)). 
    ELSE IF ww1.main-code = 122 THEN RUN fill-ooo(RECID(ww1), "ooo"). 
    ELSE IF ww1.main-code = 752 THEN RUN fill-ooo(RECID(ww1), "oos"). 
 
    ELSE IF ww1.main-code = 192 THEN RUN fill-cover(RECID(ww1)). 
    ELSE IF ww1.main-code = 197 THEN RUN fill-cover(RECID(ww1)). 
    ELSE IF ww1.main-code = 552 THEN RUN fill-cover(RECID(ww1)). 
    
    ELSE IF ww1.main-code = 1921 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1922 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1923 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1924 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1971 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1972 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1973 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1974 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1991 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1992 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1993 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1994 THEN RUN fill-cover-shift(RECID(ww1)).

    ELSE IF ww1.main-code = 85
      THEN RUN fill-arrdep(RECID(ww1), "arrival-RSV", 85, 86, 0). 
    ELSE IF ww1.main-code = 86 
      THEN RUN fill-arrdep(RECID(ww1), "arrival-RSV", 85, 86, 0). 

    ELSE IF ww1.main-code = 106
      THEN RUN fill-arrdep(RECID(ww1), "arrival-WIG", 106, 107, 0). 
    ELSE IF ww1.main-code = 107 
      THEN RUN fill-arrdep(RECID(ww1), "arrival-WIG", 106, 107, 0). 
    
    ELSE IF ww1.main-code = 187 
      THEN RUN fill-arrdep(RECID(ww1), "arrival", 187, 188, 0). 
    ELSE IF ww1.main-code = 188 
      THEN RUN fill-arrdep(RECID(ww1), "arrival", 187, 188, 0).

    ELSE IF ww1.main-code = 9188 
      THEN RUN fill-arrdep(RECID(ww1), "arrival", 0, 0, 9188).
 
    ELSE IF ww1.main-code = 189 
      THEN RUN fill-arrdep(RECID(ww1), "departure", 189, 190, 0). 
    ELSE IF ww1.main-code = 190 
      THEN RUN fill-arrdep(RECID(ww1), "departure", 189, 190, 0). 

    ELSE IF ww1.main-code = 9190 
      THEN RUN fill-arrdep(RECID(ww1), "departure", 0, 9190, 0).
 
    ELSE IF ww1.main-code = 191 
      THEN RUN fill-arrdep(RECID(ww1), "VIP", 0, 191, 0, 0). 
 
    ELSE IF ww1.main-code = 193 
      THEN RUN fill-arrdep(RECID(ww1), "NewRes", 193, 0, 0). 
 
    ELSE IF ww1.main-code = 194 
      THEN RUN fill-arrdep(RECID(ww1), "CancRes", 194, 0, 0). 

    ELSE IF ww1.main-code = 7194 
      THEN RUN fill-canc-room-night(RECID(ww1)). 
 
    ELSE IF ww1.main-code = 195 
      THEN RUN fill-avrgstay(RECID(ww1), "Avrg-Stay", 195). 
 
    ELSE IF ww1.main-code = 211 
      THEN RUN fill-arrdep(RECID(ww1), "ArrTmrw", 211, 231, 0). 
    ELSE IF ww1.main-code = 231 
      THEN RUN fill-arrdep(RECID(ww1), "ArrTmrw", 211, 231, 0). 
 
    ELSE IF ww1.main-code = 742 
      THEN RUN fill-arrdep(RECID(ww1), "Early-CO", 742, 0, 0). 
 
    ELSE IF ww1.main-code = 750 
      THEN RUN fill-arrdep(RECID(ww1), "DepTmrw", 750, 751, 0). 
    ELSE IF ww1.main-code = 751 
      THEN RUN fill-arrdep(RECID(ww1), "DepTmrw", 750, 751, 0). 
 
    ELSE IF ww1.main-code = 969 
      THEN RUN fill-arrdep(RECID(ww1), "No-Show", 969, 0, 0). 
 
    ELSE IF ww1.main-code = 806 THEN 
    DO: 
      RUN fill-rmocc (RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 182 THEN 
    DO: 
      RUN fill-gledger(RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 183 THEN 
    DO: 
      RUN fill-comprooms(RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 807 THEN 
    DO: 
      RUN fill-rmocc%(RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 808 THEN 
    DO: 
      RUN fill-docc%(RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 1008 THEN RUN fill-fbcost(RECID(ww1)). 
    ELSE IF ww1.main-code = 1084 THEN RUN fill-quantity(RECID(ww1)). 
    ELSE IF ww1.main-code = 809 THEN RUN fill-revenue(RECID(ww1)). 
    ELSE IF ww1.main-code = 810 THEN RUN fill-persocc(RECID(ww1)). 
    ELSE IF ww1.main-code = 811 THEN RUN fill-avrgrate(RECID(ww1)). 
    ELSE IF ww1.main-code = 812 THEN RUN fill-avrgLrate(RECID(ww1)). 
    ELSE IF ww1.main-code = 842 THEN RUN fill-avrglodg(RECID(ww1)). 
    ELSE IF ww1.main-code = 46 THEN RUN fill-avrgLlodge(RECID(ww1)). 
    ELSE IF ww1.main-code = 92 OR ww1.main-code = 813 
      OR ww1.main-code = 814 THEN RUN fill-segment(RECID(ww1), ww1.main-code). 
    ELSE IF ww1.main-code = 179 THEN RUN fill-rmcatstat(RECID(ww1), ww1.main-code). 
    ELSE IF ww1.main-code = 180 OR ww1.main-code = 181 
      OR ww1.main-code = 800 THEN RUN fill-zinrstat(RECID(ww1), ww1.main-code). 
  END. 
 
  FOR EACH w1 WHERE w1.grpflag GE 1 AND w1.grpflag NE 9 BY w1.nr: 
    FOR EACH w2 WHERE w2.nr1 = w1.nr NO-LOCK: 
      FIND FIRST curr-child WHERE curr-child.nr = w2.nr2 NO-LOCK. 
      RUN fill-value1(RECID(w1), RECID(curr-child), w2.val-sign). 
    END. 
  END. 
  /*MTvalue-filled = YES. */
END.



/*********************************************************************/

PROCEDURE fill-totroom: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE VARIABLE anz AS INTEGER. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  anz = 0. 
  FOR EACH zimmer NO-LOCK: 
    anz = anz + 1. 
  END. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
 
  DO datum = datum1 TO to-date: 
    IF datum = to-date THEN w1.tday = w1.tday + anz. 
    IF start-date NE ? THEN
    DO:
      IF (datum LT from-date) AND (datum GE start-date) 
        THEN w1.ytd-saldo = w1.ytd-saldo + anz. 
      ELSE 
      DO: 
        IF (datum GE start-date) THEN w1.saldo = w1.saldo + anz. 
        IF ytd-flag AND (datum GE start-date) 
          THEN w1.ytd-saldo = w1.ytd-saldo + anz. 
      END.
    END.
    ELSE
    DO:
      IF (datum LT from-date) THEN w1.ytd-saldo = w1.ytd-saldo + anz. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + anz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + anz. 
      END.
    END.
  END. 
 
  IF (lytd-flag OR lmtd-flag) THEN 
  DO: 
    IF lytd-flag THEN datum2 = Ljan1. 
    ELSE datum2 = Lfrom-date. 
    DO datum = datum2 TO Lto-date: 
      IF start-date NE ? THEN
      DO:
        IF (datum LT Lfrom-date) AND (datum GE start-date) 
          THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        ELSE IF (datum GE start-date) THEN 
        DO: 
          w1.lastyr = w1.lastyr + anz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        END.
      END. 
      ELSE
      DO:
        IF (datum LT Lfrom-date) THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + anz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        END.
      END.
    END. 
  END. 
 
  IF pmtd-flag THEN /* previous MTD */ 
  DO datum = Pfrom-date TO Pto-date: 
    IF start-date NE ? THEN
    DO:
      IF (datum GE start-date) THEN w1.lastmon = w1.lastmon + anz. 
    END.
    ELSE w1.lastmon = w1.lastmon + anz. 
  END.
  w1.done = YES. 
END. 


PROCEDURE fill-rmavail: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  FOR EACH zimkateg NO-LOCK: 
    FOR EACH zkstat WHERE zkstat.datum GE datum1 AND zkstat.datum LE to-date 
      AND zkstat.zikatnr = zimkateg.zikatnr NO-LOCK: 
      IF zkstat.datum = to-date THEN w1.tday = w1.tday + zkstat.anz100. 
      IF zkstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + zkstat.anz100. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zkstat.anz100. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + zkstat.anz100. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum2 = Ljan1. 
      ELSE datum2 = Lfrom-date. 
      FOR EACH zkstat WHERE zkstat.datum GE datum2 AND zkstat.datum LE Lto-date 
        AND zkstat.zikatnr = zimkateg.zikatnr NO-LOCK: 
        IF zkstat.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + zkstat.anz100. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + zkstat.anz100. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + zkstat.anz100. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zkstat WHERE zkstat.datum GE Pfrom-date 
      AND zkstat.datum LE Pto-date 
      AND zkstat.zikatnr = zimkateg.zikatnr NO-LOCK: 
      w1.lastmon = w1.lastmon + zkstat.anz100. 
    END. 
  END. 
  w1.done = YES. 
END. 


PROCEDURE fill-ooo: 
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF INPUT PARAMETER key-word AS CHAR. 
DEF VARIABLE datum1 AS DATE. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      IF zinrstat.datum = to-date THEN w1.tday = w1.tday + zinrstat.zimmeranz. 
      IF zinrstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.zimmeranz. 
    END. 
  END. 
  w1.done = YES. 
END. 


PROCEDURE fill-cover: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEF BUFFER w11 FOR w1. 
DEF BUFFER w12 FOR w1. 
DEF BUFFER w13 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  RELEASE w11. 
  RELEASE w12. 
  RELEASE w13. 
  FIND FIRST w11 WHERE w11.main-code = 552 AND w11.dept = w1.dept NO-ERROR. 
  FIND FIRST w12 WHERE w12.main-code = 192 AND w12.dept = w1.dept NO-ERROR. 
  FIND FIRST w13 WHERE w13.main-code = 197 AND w13.dept = w1.dept NO-ERROR. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 AND h-umsatz.datum LE to-date 
    AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
    AND h-umsatz.betriebsnr = w1.dept NO-LOCK: 
    IF h-umsatz.datum = to-date AND AVAILABLE w11 THEN w11.tday = w11.tday + h-umsatz.anzahl. 
    IF h-umsatz.datum = to-date AND AVAILABLE w12 THEN w12.tday = w12.tday + h-umsatz.betrag. 
    IF h-umsatz.datum = to-date AND AVAILABLE w13 THEN w13.tday = w13.tday + h-umsatz.nettobetrag. 
 
    IF h-umsatz.datum LT from-date THEN 
    DO: 
      IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo + h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.ytd-saldo = w12.ytd-saldo + h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.ytd-saldo = w13.ytd-saldo + h-umsatz.nettobetrag. 
    END. 
    ELSE 
    DO: 
      IF AVAILABLE w11 THEN w11.saldo = w11.saldo + h-umsatz.anzahl. 
      IF ytd-flag AND AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo + h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.saldo = w12.saldo + h-umsatz.betrag. 
      IF ytd-flag AND AVAILABLE w12 THEN w12.ytd-saldo = w12.ytd-saldo + h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.saldo = w13.saldo + h-umsatz.nettobetrag. 
      IF ytd-flag AND AVAILABLE w13 THEN w13.ytd-saldo = w13.ytd-saldo + h-umsatz.nettobetrag. 
    END. 
  END. 
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 
      AND h-umsatz.datum LE Lto-date 
      AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
      AND h-umsatz.betriebsnr = w1.dept NO-LOCK: 
      IF h-umsatz.datum LT Lfrom-date THEN 
      DO: 
        IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo + h-umsatz.anzahl. 
        IF AVAILABLE w12 THEN w12.lytd-saldo = w12.lytd-saldo + h-umsatz.betrag. 
        IF AVAILABLE w13 THEN w13.lytd-saldo = w13.lytd-saldo + h-umsatz.nettobetrag. 
      END. 
      ELSE 
      DO: 
        IF AVAILABLE w11 THEN w11.lastyr = w11.lastyr + h-umsatz.anzahl. /* LAST year MTD */ 
        IF lytd-flag AND AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo + h-umsatz.anzahl. 
        IF AVAILABLE w12 THEN w12.lastyr = w12.lastyr + h-umsatz.betrag. 
        IF lytd-flag AND AVAILABLE w12 THEN w12.lytd-saldo = w12.lytd-saldo + h-umsatz.betrag. 
        IF AVAILABLE w13 THEN w13.lastyr = w13.lastyr + h-umsatz.nettobetrag. 
        IF lytd-flag AND AVAILABLE w13 THEN w13.lytd-saldo = w13.lytd-saldo + h-umsatz.nettobetrag. 
      END. 
    END. 
  END. 
  IF pmtd-flag THEN /* previous MTD */ 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE Pfrom-date 
    AND h-umsatz.datum LE Pto-date 
    AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
    AND h-umsatz.betriebsnr = w1.dept NO-LOCK: 
    IF AVAILABLE w11 THEN w11.lastmon = w11.lastmon + h-umsatz.anzahl. 
    IF AVAILABLE w12 THEN w12.lastmon = w12.lastmon + h-umsatz.betrag. 
    IF AVAILABLE w13 THEN w13.lastmon = w13.lastmon + h-umsatz.nettobetrag. 
  END. 
  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w12 THEN w12.done = YES. 
  IF AVAILABLE w13 THEN w13.done = YES. 
END. 


PROCEDURE fill-arrdep: 
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF INPUT PARAMETER key-word AS CHAR. 
DEF INPUT PARAMETER number1 AS INTEGER. 
DEF INPUT PARAMETER number2 AS INTEGER. 
DEF INPUT PARAMETER number3 AS INTEGER. 
DEF VAR datum1 AS DATE. 
DEF BUFFER w11 FOR w1. 
DEF BUFFER w12 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  RELEASE w11. 
  RELEASE w12. 
  IF number1 NE 0 THEN 
    FIND FIRST w11 WHERE w11.main-code = number1 AND NOT w11.done NO-ERROR. 
  IF number2 NE 0 THEN 
    FIND FIRST w12 WHERE w12.main-code = number2 AND NOT w12.done NO-ERROR. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
          IF AVAILABLE w11 THEN w11.tday = w11.tday + zinrstat.zimmeranz. 
          IF AVAILABLE w12 THEN w12.tday = w12.tday + zinrstat.personen. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        IF AVAILABLE w11 THEN 
            w11.ytd-saldo = w11.ytd-saldo + zinrstat.zimmeranz. 
        IF AVAILABLE w12 THEN 
            w12.ytd-saldo = w12.ytd-saldo + zinrstat.personen. 
      END. 
      ELSE 
      DO: 
        IF AVAILABLE w11 THEN 
            w11.saldo = w11.saldo + zinrstat.zimmeranz. 
        IF ytd-flag AND AVAILABLE w11 
            THEN w11.ytd-saldo = w11.ytd-saldo + zinrstat.zimmeranz. 
        IF AVAILABLE w12 THEN w12.saldo = w12.saldo + zinrstat.personen. 
        IF ytd-flag AND AVAILABLE w12 
            THEN w12.ytd-saldo = w12.ytd-saldo + zinrstat.personen. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          IF AVAILABLE w11 THEN 
              w11.lytd-saldo = w11.lytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w12 THEN 
              w12.lytd-saldo = w12.lytd-saldo + zinrstat.personen. 
        END. 
        ELSE 
        DO: 
          IF AVAILABLE w11 THEN 
              w11.lastyr = w11.lastyr + zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag AND AVAILABLE w11 
              THEN w11.lytd-saldo = w11.lytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w12 THEN 
              w12.lastyr = w12.lastyr + zinrstat.personen. /* LAST year MTD */ 
          IF lytd-flag AND AVAILABLE w12 
              THEN w12.lytd-saldo = w12.lytd-saldo + zinrstat.personen. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      IF AVAILABLE w11 THEN 
          w11.lastmon = w11.lastmon + zinrstat.zimmeranz. 
      IF AVAILABLE w12 THEN 
          w12.lastmon = w12.lastmon + zinrstat.personen. 
    END. 
  END. 
  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w12 THEN w12.done = YES. 
END. 


PROCEDURE fill-avrgstay: 
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF INPUT PARAMETER key-word AS CHAR. 
DEF INPUT PARAMETER number1 AS INTEGER. 
DEF VAR datum1 AS DATE. 
DEF BUFFER w11 FOR w1. 
DEF BUFFER tbuff FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF number1 NE 0 THEN FIND FIRST w11 WHERE w11.main-code = number1 
    AND NOT w11.done NO-ERROR. 
  IF NOT AVAILABLE w11 THEN RETURN. 
 
  CREATE tbuff. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date AND zinrstat.zinr = key-word NO-LOCK: 
 
      IF zinrstat.datum = to-date THEN 
        w11.tday = w11.tday + zinrstat.personen / zinrstat.zimmeranz. 
 
      IF (zinrstat.datum LT from-date) THEN 
      DO: 
        w11.ytd-saldo = w11.ytd-saldo + zinrstat.personen. 
        tbuff.ytd-saldo = tbuff.ytd-saldo + zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w11.saldo = w11.saldo + zinrstat.personen. 
        tbuff.saldo = tbuff.saldo + zinrstat.zimmeranz. 
        IF ytd-flag THEN 
        DO: 
          w11.ytd-saldo = w11.ytd-saldo + zinrstat.personen. 
          tbuff.ytd-saldo = tbuff.ytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w11.lytd-saldo = w11.lytd-saldo + zinrstat.personen. 
          tbuff.lytd-saldo = tbuff.lytd-saldo + zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w11.lastyr = w11.lastyr + zinrstat.personen. /* LAST year MTD */ 
          tbuff.lastyr = tbuff.lastyr + zinrstat.zimmeranz. 
          IF lytd-flag THEN 
          DO: 
            w11.lytd-saldo = w11.lytd-saldo + zinrstat.personen. 
            tbuff.lytd-saldo = tbuff.lytd-saldo + zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date AND zinrstat.zinr = key-word NO-LOCK: 
      w11.lastmon = w11.lastmon + zinrstat.personen. 
      tbuff.lastmon = tbuff.lastmon + zinrstat.zimmeranz. 
    END. 
  END. 
 
  IF tbuff.saldo NE 0 THEN w11.saldo = w11.saldo / tbuff.saldo. 
  IF tbuff.ytd-saldo NE 0 THEN w11.ytd-saldo = w11.ytd-saldo / tbuff.ytd-saldo. 
  IF tbuff.lytd-saldo NE 0 THEN w11.lytd-saldo = w11.lytd-saldo / tbuff.lytd-saldo. 
  IF tbuff.lastyr NE 0 THEN w11.lastyr = w11.lastyr / tbuff.lastyr. 
  IF tbuff.lastmon NE 0 THEN w11.lastmon = w11.lastmon / tbuff.lastmon. 
 
  w11.done = YES. 
  DELETE tbuff. 
END. 


PROCEDURE fill-rmocc: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE buffer w1a FOR w1. 
DEFINE buffer w11 FOR w1. 
DEFINE buffer w12 FOR w1. 
DEFINE buffer w13 FOR w1. 
DEFINE buffer w22 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w1a WHERE w1a.main-code = 810 NO-ERROR. 
  IF AVAILABLE w1a AND w1a.done THEN release w1a. 
 
  FIND FIRST w22 WHERE w22.main-code = 183 NO-ERROR. 
  IF AVAILABLE w22 AND w22.done THEN release w22. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
 
  lytoday-flag = (lytd-flag OR lmtd-flag) AND (month(to-date) NE 2 
    OR day(to-date) NE 29). 
 
  FOR EACH segment NO-LOCK: 
    FIND FIRST w11 WHERE w11.main-code = 92 
      AND w11.artnr = segment.segmentcode NO-ERROR. 
    IF AVAILABLE w11 AND w11.done THEN release w11. 
    FIND FIRST w12 WHERE w12.main-code = 813 
      AND w12.artnr = segment.segmentcode NO-ERROR. 
    IF AVAILABLE w12 AND w12.done THEN release w12. 
    FIND FIRST w13 WHERE w13.main-code = 814 
      AND w13.artnr = segment.segmentcode NO-ERROR. 
    IF AVAILABLE w13 AND w13.done THEN release w13. 
 
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF segmentstat.datum = to-date THEN 
      DO: 
        release segmbuff. 
        IF lytoday-flag THEN 
        DO: 
          lytoday = to-date - 365. 
          FIND FIRST segmbuff WHERE segmbuff.datum = lytoday 
            AND segmbuff.segmentcode = segment.segmentcode NO-LOCK NO-ERROR. 
        END. 
        w1.tday = w1.tday + segmentstat.zimmeranz. 
        w1.tbudget = w1.tbudget + segmentstat.budzimmeranz. 
        IF AVAILABLE segmbuff THEN 
          w1.lytoday = w1.lytoday + segmbuff.zimmeranz. 
 
        IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
        DO: 
          w22.tday = w22.tday + segmentstat.betriebsnr. 
          IF AVAILABLE segmbuff THEN 
            w22.lytoday = w22.lytoday + segmbuff.betriebsnr. 
        END. 
 
        IF AVAILABLE w1a THEN 
        DO: 
          w1a.tday = w1a.tday + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1a.tbudget = w1a.tbudget + segmentstat.budpersanz. 
          IF AVAILABLE segmbuff THEN 
            w1a.lytoday = w1a.lytoday + segmbuff.persanz 
              + segmbuff.kind1 + segmbuff.kind2 + segmbuff.gratis. 
        END. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.tday = w11.tday + segmentstat.logis / frate. 
          w11.tbudget = w11.tbudget + segmentstat.budlogis. 
          IF AVAILABLE segmbuff THEN 
            w11.lytoday = w11.lytoday + segmbuff.logis / frate. 
        END. 
        IF AVAILABLE w12 THEN 
        DO: 
          w12.tday = w12.tday + segmentstat.zimmeranz. 
          w12.tbudget = w12.tbudget + segmentstat.budzimmeranz. 
          IF AVAILABLE segmbuff THEN 
            w12.lytoday = w12.lytoday + segmbuff.zimmeranz. 
        END. 
        IF AVAILABLE w13 THEN 
        DO: 
          w13.tday = w13.tday + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w13.tbudget = w13.tbudget + segmentstat.budpersanz. 
          IF AVAILABLE segmbuff THEN 
            w13.lytoday = w13.lytoday + segmbuff.persanz 
              + segmbuff.kind1 + segmbuff.kind2 + segmbuff.gratis. 
        END. 
      END. 
 
      IF segmentstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + segmentstat.zimmeranz. 
        w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
 
        IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
        DO: 
          w22.ytd-saldo = w22.ytd-saldo + segmentstat.betriebsnr. 
        END. 
 
        IF AVAILABLE w1a THEN 
        DO: 
          w1a.ytd-saldo = w1a.ytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1a.ytd-budget = w1a.ytd-budget + segmentstat.budpersanz. 
        END. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
          w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
        END. 
        IF AVAILABLE w12 THEN 
        DO: 
          w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
          w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
        END. 
        IF AVAILABLE w13 THEN 
        DO: 
          w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
        END. 
      END. 
 
      ELSE DO: 
        w1.saldo = w1.saldo + segmentstat.zimmeranz. 
        w1.budget = w1.budget + segmentstat.budzimmeranz. 
        IF ytd-flag THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.zimmeranz. 
          w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
        END. 
 
        IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
        DO: 
          w22.saldo = w22.saldo + segmentstat.betriebsnr. 
          IF ytd-flag THEN 
          w22.ytd-saldo = w22.ytd-saldo + segmentstat.betriebsnr. 
        END. 
 
        IF AVAILABLE w1a THEN 
        DO: 
          w1a.saldo = w1a.saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1a.budget = w1a.budget + segmentstat.budpersanz. 
          IF ytd-flag THEN 
          DO: 
            w1a.ytd-saldo = w1a.ytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1a.ytd-budget = w1a.ytd-budget + segmentstat.budpersanz. 
          END. 
        END. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + segmentstat.logis / frate. 
          w11.budget = w11.budget + segmentstat.budlogis. 
          IF ytd-flag THEN 
          DO: 
            w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
            w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
          END. 
        END. 
        IF AVAILABLE w12 THEN 
        DO: 
          w12.saldo = w12.saldo + segmentstat.zimmeranz. 
          w12.budget = w12.budget + segmentstat.budzimmeranz. 
          IF ytd-flag THEN 
          DO: 
            w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
            w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
          END. 
        END. 
        IF AVAILABLE w13 THEN 
        DO: 
          w13.saldo = w13.saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w13.budget = w13.budget + segmentstat.budpersanz. 
          IF ytd-flag THEN 
          DO: 
            w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
          END. 
        END. 
      END. 
    END. 
 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum2 = Ljan1. 
      ELSE datum2 = Lfrom-date. 
      FOR EACH segmentstat WHERE segmentstat.datum GE datum2 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF segmentstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo + segmentstat.zimmeranz. 
          w1.lytd-budget = w1.lytd-budget + segmentstat.budzimmeranz. 
 
          IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
          DO: 
            w22.lytd-saldo = w22.lytd-saldo + segmentstat.betriebsnr. 
          END. 
 
          IF AVAILABLE w1a THEN 
          DO: 
            w1a.lytd-saldo = w1a.lytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1a.lytd-budget = w1a.lytd-budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
            w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
          END. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
            w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
          END. 
        END. 
 
        ELSE DO: 
          w1.lastyr = w1.lastyr + segmentstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + segmentstat.zimmeranz. 
          w1.ly-budget = w1.ly-budget + segmentstat.budzimmeranz. 
          IF lytd-flag THEN w1.lytd-budget = w1.lytd-budget 
            + segmentstat.budzimmeranz. 
 
          IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
          DO: 
            w22.lastyr = w22.lastyr + segmentstat.betriebsnr. 
            IF lytd-flag THEN 
            w22.lytd-saldo = w22.lytd-saldo + segmentstat.betriebsnr. 
          END. 
 
          IF AVAILABLE w1a THEN 
          DO: 
            w1a.lastyr = w1a.lastyr + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1a.ly-budget = w1a.ly-budget + segmentstat.budpersanz. 
            IF lytd-flag THEN 
            DO: 
              w1a.lytd-saldo = w1a.lytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w1a.lytd-budget = w1a.lytd-budget + segmentstat.budpersanz. 
            END. 
          END. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr + segmentstat.logis / frate. 
            w11.ly-budget = w11.ly-budget + segmentstat.budlogis. 
            IF lytd-flag THEN 
            DO: 
              w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
              w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
            END. 
          END. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.lastyr = w12.lastyr + segmentstat.zimmeranz. 
            w12.ly-budget = w12.ly-budget + segmentstat.budzimmeranz. 
            IF lytd-flag THEN 
            DO: 
              w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
              w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
            END. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.lastyr = w13.lastyr + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.ly-budget = w13.ly-budget + segmentstat.budpersanz. 
            IF lytd-flag THEN 
            DO: 
              w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
            END. 
          END. 
 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + segmentstat.zimmeranz. 
      w1.lm-budget = w1.lm-budget + segmentstat.budzimmeranz. 
 
      IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
      DO: 
        w22.lastmon = w22.lastmon + segmentstat.betriebsnr. 
      END. 
 
      IF AVAILABLE w1a THEN 
      DO: 
        w1a.lastmon = w1a.lastmon + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1a.lm-budget = w1a.lm-budget + segmentstat.budpersanz. 
      END. 
      IF AVAILABLE w11 THEN 
      DO: 
        w11.lastmon = w11.lastmon + segmentstat.logis / frate. 
        w11.lm-budget = w11.lm-budget + segmentstat.budlogis. 
      END. 
      IF AVAILABLE w12 THEN 
      DO: 
        w12.lastmon = w12.lastmon + segmentstat.zimmeranz. 
        w12.lm-budget = w12.lm-budget + segmentstat.budzimmeranz. 
      END. 
      IF AVAILABLE w13 THEN 
      DO: 
        w13.lastmon = w13.lastmon + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w13.lm-budget = w13.lm-budget + segmentstat.budpersanz. 
      END. 
 
    END. 
    IF AVAILABLE w11 THEN w11.done = YES. 
    IF AVAILABLE w12 THEN w12.done = YES. 
    IF AVAILABLE w13 THEN w13.done = YES. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w1a THEN w1a.done = YES. 
  IF AVAILABLE w22 THEN w22.done = YES. 
END. 


PROCEDURE fill-gledger: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
DEFINE buffer w12 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST uebertrag WHERE uebertrag.datum = to-date - 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE uebertrag THEN 
  DO: 
    w1.tday = uebertrag.betrag. 
    w1.done = YES. 
  END. 
END. 


PROCEDURE fill-comprooms: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
/* 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
*/ 
 
  lytoday-flag = (lytd-flag OR lmtd-flag) AND (month(to-date) NE 2 
    OR day(to-date) NE 29). 
  datum1 = from-date. 
 
  FOR EACH segment WHERE segment.betriebsnr = 0 NO-LOCK: /* paying segments */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segment.segmentcode 
      AND segmentstat.betriebsnr GT 0 NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
 
      IF segmentstat.datum = to-date THEN 
      DO: 
        release segmbuff. 
        IF lytoday-flag THEN 
        DO: 
          lytoday = to-date - 365. 
          FIND FIRST segmbuff WHERE segmbuff.datum = lytoday 
            AND segmbuff.segmentcode = segment.segmentcode NO-LOCK NO-ERROR. 
        END. 
        w1.tday = w1.tday + segmentstat.betriebsnr. 
        IF AVAILABLE segmbuff THEN w1.lytoday = w1.lytoday + segmbuff.betriebsnr. 
      END. 
 
      IF segmentstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + segmentstat.betriebsnr. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + segmentstat.betriebsnr. 
        IF ytd-flag THEN 
        w1.ytd-saldo = w1.ytd-saldo + segmentstat.betriebsnr. 
      END. 
    END. 
/* 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF segmentstat.datum LT Lfrom-date THEN 
          w1.lytd-saldo = w1.lytd-saldo + segmentstat.betriebsnr. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + segmentstat.betriebsnr. 
          IF lytd-flag THEN 
          w1.lytd-saldo = w1.lytd-saldo + segmentstat.betriebsnr. 
        END. 
      END. 
    END. 
 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + segmentstat.betriebsnr. 
    END. 
*/ 
  END. 
  w1.done = YES. 
END. 


PROCEDURE fill-rmocc%: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
DEFINE buffer w12 FOR w1. 
 
  FIND FIRST w11 WHERE w11.main-code = 805 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w11 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Room Availablity not defined,",lvCAREA,"")
            + CHR(10)
            + translateExtended ("which is necessary for calculating of room occupancy.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  FIND FIRST w12 WHERE w12.main-code = 806 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w12 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Occupied Rooms not defined,",lvCAREA,"")
            + CHR(10)
            + translateExtended ("which is necessary for calculating of room occupancy in %.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  IF NOT w11.done THEN RUN fill-rmavail(RECID(w11)). 
  IF NOT w12.done THEN RUN fill-rmocc(RECID(w12)). 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF w11.tday NE 0 THEN w1.tday = w12.tday / w11.tday * 100. 
  IF w11.saldo NE 0 THEN w1.saldo = w12.saldo / w11.saldo * 100. 
  IF w11.ytd-saldo NE 0 THEN w1.ytd-saldo = w12.ytd-saldo / w11.ytd-saldo * 100. 
  IF w11.lytd-saldo NE 0 THEN w1.lytd-saldo = w12.lytd-saldo / w11.lytd-saldo 
    * 100. 
  IF w11.lastyr NE 0 THEN w1.lastyr = w12.lastyr / w11.lastyr * 100. 
  IF w11.lastmon NE 0 THEN w1.lastmon = w12.lastmon / w11.lastmon * 100. 
  w1.done = YES. 
END. 


PROCEDURE fill-docc%: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
DEFINE buffer w12 FOR w1. 
  FIND FIRST w11 WHERE w11.main-code = 806 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w11 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Occupied Rooms not defined,",lvCAREA,"") 
            + CHR(10)
            + translateExtended ("which is necessary for calculating of double room occupancy.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  FIND FIRST w12 WHERE w12.main-code = 810 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w12 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Occupied Persons not defined,",lvCAREA,"")
            + CHR(10)
            + translateExtended ("which is necessary for calculating of double room occupancy.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  IF NOT w11.done THEN RUN fill-rmocc(RECID(w11)). 
  IF NOT w12.done THEN RUN fill-persocc(RECID(w12)). 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF w11.tday NE 0 THEN w1.tday = (w12.tday - w11.tday) / w11.tday * 100. 
  IF w11.saldo NE 0 THEN w1.saldo = (w12.saldo - w11.saldo) / w11.saldo * 100. 
  IF w11.ytd-saldo NE 0 THEN w1.ytd-saldo 
    = (w12.ytd-saldo - w11.ytd-saldo) / w11.ytd-saldo * 100. 
  IF w11.lytd-saldo NE 0 THEN w1.lytd-saldo 
    = (w12.lytd-saldo - w11.lytd-saldo) / w11.lytd-saldo * 100. 
  IF w11.lastyr NE 0 THEN w1.lastyr 
    = (w12.lastyr - w11.lastyr) / w11.lastyr * 100. 
  IF w11.lastmon NE 0 THEN w1.lastmon 
    = (w12.lastmon - w11.lastmon) / w11.lastmon * 100. 
  w1.done = YES. 
END. 



PROCEDURE fill-fbcost: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE VARIABLE cost AS DECIMAL. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST artikel WHERE artikel.artnr = w1.artnr 
    AND artikel.departement = w1.dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Article for Cost-variable not found : ",lvCAREA,"") + w1.varname.
    error-nr = -1. 
    RETURN. 
  END. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 AND h-umsatz.datum LE to-date 
    AND h-umsatz.departement = w1.dept NO-LOCK, 
    FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
    AND h-artikel.departement = h-umsatz.departement 
    AND h-artikel.artnrfront = artikel.artnr NO-LOCK: 
    RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
      OUTPUT cost). 
    IF h-umsatz.datum = to-date THEN 
      w1.tday = w1.tday + cost. 
    IF h-umsatz.datum LT from-date THEN 
      w1.ytd-saldo = w1.ytd-saldo + cost. 
    ELSE 
    DO: 
      w1.saldo = w1.saldo + cost. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + cost. 
    END. 
  END. 
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 
      AND h-umsatz.datum LE Lto-date AND h-umsatz.departement = w1.dept NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
      AND h-artikel.departement = h-umsatz.departement 
      AND h-artikel.artnrfront = artikel.artnr NO-LOCK: 
      RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
        OUTPUT cost). 
      IF h-umsatz.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + cost. 
      ELSE 
      DO: 
        w1.lastyr = w1.lastyr + cost. /* LAST year MTD */ 
        IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + cost. 
      END. 
    END. 
  END. 
  IF pmtd-flag THEN /* previous MTD */ 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE Pfrom-date 
    AND h-umsatz.datum LE Pto-date AND h-umsatz.departement = w1.dept NO-LOCK, 
    FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
    AND h-artikel.departement = h-umsatz.departement 
    AND h-artikel.artnrfront = artikel.artnr NO-LOCK: 
    RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
      OUTPUT cost). 
    w1.lastmon = w1.lastmon + cost. 
  END. 
  w1.done = YES. 
END. 


PROCEDURE fill-quantity: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST artikel WHERE artikel.artnr = w1.artnr 
    AND artikel.departement = w1.dept NO-LOCK NO-ERROR. 
 
  IF NOT AVAILABLE artikel THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Noch such article number : ",lvCAREA,"") + STRING(w1.artnr)
            + " " + translateExtended ("Dept",lvCAREA,"") + " " + STRING(w1.dept).
    RETURN. 
  END. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  FOR EACH umsatz WHERE umsatz.datum GE datum1 AND umsatz.datum LE to-date 
    AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK: 
    IF umsatz.datum = to-date THEN 
    DO: 
      w1.tday = w1.tday + umsatz.anzahl. 
    END. 
    IF umsatz.datum LT from-date THEN 
    DO: 
      w1.ytd-saldo = w1.ytd-saldo + umsatz.anzahl. 
    END. 
    ELSE 
    DO: 
      w1.saldo = w1.saldo + umsatz.anzahl. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + umsatz.anzahl. 
    END. 
  END. 
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum2 = Ljan1. 
    ELSE datum2 = Lfrom-date. 
    FOR EACH umsatz WHERE umsatz.datum GE datum2 AND umsatz.datum LE Lto-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK: 
      IF umsatz.datum LT Lfrom-date THEN 
      DO: 
        w1.lytd-saldo = w1.lytd-saldo + umsatz.anzahl. 
      END. 
      ELSE 
      DO: 
        w1.lastyr = w1.lastyr + umsatz.anzahl. /* LAST year MTD */ 
        IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + umsatz.anzahl. 
      END. 
    END. 
  END. 
  IF pmtd-flag THEN /* previous MTD */ 
  FOR EACH umsatz WHERE umsatz.datum GE Pfrom-date 
    AND umsatz.datum LE Pto-date 
    AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK: 
    w1.lastmon = w1.lastmon + umsatz.anzahl. 
  END. 
  w1.done = YES. 
END. 



PROCEDURE fill-revenue: 
DEFINE INPUT PARAMETER rec-w1   AS INTEGER  NO-UNDO. 
DEFINE VARIABLE curr-date       AS DATE     NO-UNDO. 
DEFINE VARIABLE datum1          AS DATE     NO-UNDO. 
DEFINE VARIABLE serv            AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE vat             AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE vat2            AS DECIMAL  NO-UNDO.
DEFINE VARIABLE fact            AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE n-betrag        AS DECIMAL  NO-UNDO. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST artikel WHERE artikel.artnr = w1.artnr 
    AND artikel.departement = w1.dept NO-LOCK NO-ERROR. 
 
  IF NOT AVAILABLE artikel THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Noch such article number : ",lvCAREA,"") + STRING(w1.artnr)
            + " " + translateExtended ("Dept",lvCAREA,"") + " " + STRING(w1.dept).
    RETURN. 
  END. 
 
/*
  serv = 0. 
  vat = 0. 
  IF artikel.service-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
      serv = htparam.fdecimal / 100. 
  END. 
  IF artikel.mwst-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
      vat = htparam.fdecimal / 100. 
      IF serv-vat THEN vat = vat + vat * serv. 
/*    vat = round(vat, 2).   */ 
    END. 
  END. 
  fact = 1.00 + serv + vat. 
*/ 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO curr-date = datum1 TO to-date: 
    FIND FIRST umsatz WHERE umsatz.datum = curr-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK 
      NO-ERROR. 
    n-betrag = 0. 
    IF AVAILABLE umsatz THEN 
    DO: 

/* SY AUG 13 2017 */
      RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
        curr-date, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(curr-date). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      n-betrag = umsatz.betrag / (fact * frate). 
      IF price-decimal = 0 THEN n-betrag = round(n-betrag, 0). 
    END. 
    IF budget-flag THEN FIND FIRST budget WHERE budget.artnr = w1.artnr 
      AND budget.departement = w1.dept 
      AND budget.datum = curr-date NO-LOCK NO-ERROR. 
    IF curr-date = to-date THEN 
    DO: 
      IF AVAILABLE umsatz THEN w1.tday = w1.tday + n-betrag. 
      IF AVAILABLE budget THEN w1.tbudget = w1.tbudget + budget.betrag. 
    END. 
    IF curr-date LT from-date THEN 
    DO: 
      IF AVAILABLE umsatz THEN w1.ytd-saldo = w1.ytd-saldo + n-betrag. 
      IF AVAILABLE budget THEN w1.ytd-budget = w1.ytd-budget 
        + budget.betrag. 
    END. 
    ELSE 
    DO: 
      IF AVAILABLE umsatz THEN 
      DO: 
        w1.saldo = w1.saldo + n-betrag. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + n-betrag. 
      END. 
      IF AVAILABLE budget THEN 
      DO: 
        w1.budget = w1.budget + budget.betrag. 
        IF ytd-flag THEN w1.ytd-budget = w1.ytd-budget + budget.betrag. 
      END. 
    END. 
  END. 
 
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    DO curr-date = datum1 TO Lto-date: 
      FIND FIRST umsatz WHERE umsatz.datum = curr-date 
        AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK 
        NO-ERROR. 
      n-betrag = 0. 
      IF AVAILABLE umsatz THEN 
      DO: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(curr-date). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        n-betrag = umsatz.betrag / (fact * frate). 
        IF price-decimal = 0 THEN n-betrag = round(n-betrag, 0). 
      END. 
      IF budget-flag THEN FIND FIRST budget WHERE budget.artnr = w1.artnr 
        AND budget.departement = w1.dept 
        AND budget.datum = curr-date NO-LOCK NO-ERROR. 
      IF curr-date LT Lfrom-date THEN 
      DO: 
        IF AVAILABLE umsatz THEN w1.lytd-saldo = w1.lytd-saldo + n-betrag. 
        IF AVAILABLE budget THEN w1.lytd-budget = w1.lytd-budget + budget.betrag. 
      END. 
      ELSE 
      DO: 
        IF AVAILABLE umsatz THEN 
        DO: 
          w1.lastyr = w1.lastyr + n-betrag. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + n-betrag. 
        END. 
        IF AVAILABLE budget THEN 
        DO: 
          w1.ly-budget = w1.ly-budget + budget.betrag. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-budget = w1.lytd-budget + budget.betrag. 
        END. 
      END. 
    END. 
  END. 
 
  IF pmtd-flag THEN /* previous MTD */ 
  DO curr-date = Pfrom-date TO Pto-date: 
    FIND FIRST umsatz WHERE umsatz.datum = curr-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK 
      NO-ERROR. 
    n-betrag = 0. 
    IF AVAILABLE umsatz THEN 
    DO: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(curr-date). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      n-betrag = umsatz.betrag / (fact * frate). 
      IF price-decimal = 0 THEN n-betrag = round(n-betrag, 0). 
    END. 
    IF budget-flag THEN FIND FIRST budget WHERE budget.artnr = w1.artnr 
      AND budget.departement = w1.dept 
      AND budget.datum = curr-date NO-LOCK NO-ERROR. 
    IF AVAILABLE umsatz THEN w1.lastmon = w1.lastmon + n-betrag. 
    IF AVAILABLE budget THEN w1.lm-budget = w1.lm-budget + budget.betrag. 
  END. 
 
  w1.done = YES. 
END. 


PROCEDURE fill-persocc: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE buffer w11 FOR w1. 
DEFINE buffer w22 FOR w1. 
DEFINE buffer w753 FOR w1. 
DEFINE buffer w754 FOR w1. 
DEFINE buffer w755 FOR w1. 
 
  lytoday-flag = (lytd-flag OR lmtd-flag) AND (month(to-date) NE 2 
    OR day(to-date) NE 29). 
 
  FIND FIRST w11 WHERE w11.main-code = 806 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  FIND FIRST w22 WHERE w22.main-code = 183 NO-ERROR. 
  IF AVAILABLE w22 AND w22.done THEN release w22. 
 
  FIND FIRST w753 WHERE w753.main-code = 753 AND NOT w753.done NO-ERROR. 
  FIND FIRST w754 WHERE w754.main-code = 754 AND NOT w754.done NO-ERROR. 
  FIND FIRST w755 WHERE w755.main-code = 755 AND NOT w755.done NO-ERROR. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  IF lytd-flag THEN datum2 = Ljan1. 
  ELSE datum2 = Lfrom-date. 
  FOR EACH segment NO-LOCK: 
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF segmentstat.datum = to-date THEN 
      DO: 
        release segmbuff. 
        IF lytoday-flag THEN 
        DO: 
          lytoday = to-date - 365. 
          FIND FIRST segmbuff WHERE segmbuff.datum = lytoday 
            AND segmbuff.segmentcode = segment.segmentcode NO-LOCK NO-ERROR. 
        END. 
        w1.tday = w1.tday + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1.tbudget = w1.tbudget + segmentstat.budpersanz. 
        IF AVAILABLE segmbuff THEN 
          w1.lytoday = w1.lytoday + segmbuff.persanz 
            + segmbuff.kind1 + segmbuff.kind2 + segmbuff.gratis. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.tday = w11.tday + segmentstat.zimmeranz. 
          w11.tbudget = w11.tbudget + segmentstat.budzimmeranz. 
          IF AVAILABLE segmbuff THEN 
            w11.lytoday = w11.lytoday + segmbuff.zimmeranz. 
        END. 
        IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
        DO: 
          w22.tday = w22.tday + segmentstat.betriebsnr. 
          IF AVAILABLE segmbuff THEN 
            w22.lytoday = w22.lytoday + segmbuff.betriebsnr. 
        END. 
        IF AVAILABLE w753 THEN 
        DO: 
          w753.tday = w753.tday + segmentstat.persanz. 
          IF AVAILABLE segmbuff THEN 
            w753.lytoday = w753.lytoday + segmbuff.persanz. 
        END. 
        IF AVAILABLE w754 THEN 
        DO: 
          w754.tday = w754.tday + segmentstat.kind1. 
          IF AVAILABLE segmbuff THEN 
            w754.lytoday = w754.lytoday + segmbuff.kind1. 
        END. 
        IF AVAILABLE w755 THEN 
        DO: 
          w755.tday = w755.tday + segmentstat.kind2. 
          IF AVAILABLE segmbuff THEN 
            w755.lytoday = w755.lytoday + segmbuff.kind2. 
        END. 
      END. 
 
      IF segmentstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.ytd-saldo = w11.ytd-saldo + segmentstat.zimmeranz. 
          w11.ytd-budget = w11.ytd-budget + segmentstat.budzimmeranz. 
        END. 
        IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
        DO: 
          w22.ytd-saldo = w22.ytd-saldo + segmentstat.betriebsnr. 
        END. 
        IF AVAILABLE w753 THEN 
        DO: 
          w753.ytd-saldo = w753.ytd-saldo + segmentstat.persanz. 
        END. 
        IF AVAILABLE w754 THEN 
        DO: 
          w754.ytd-saldo = w754.ytd-saldo + segmentstat.kind1. 
        END. 
        IF AVAILABLE w755 THEN 
        DO: 
          w755.ytd-saldo = w755.ytd-saldo + segmentstat.kind2. 
        END. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1.budget = w1.budget + segmentstat.budpersanz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + segmentstat.zimmeranz. 
          w11.budget = w11.budget + segmentstat.budzimmeranz. 
        END. 
        IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
        DO: 
          w22.saldo = w22.saldo + segmentstat.betriebsnr. 
        END. 
        IF AVAILABLE w753 THEN 
        DO: 
          w753.saldo = w753.saldo + segmentstat.persanz. 
        END. 
        IF AVAILABLE w754 THEN 
        DO: 
          w754.saldo = w754.saldo + segmentstat.kind1. 
        END. 
        IF AVAILABLE w755 THEN 
        DO: 
          w755.saldo = w755.saldo + segmentstat.kind2. 
        END. 
 
        IF ytd-flag THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.ytd-saldo = w11.ytd-saldo + segmentstat.zimmeranz. 
            w11.ytd-budget = w11.ytd-budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
          DO: 
            w22.ytd-saldo = w22.ytd-saldo + segmentstat.betriebsnr. 
          END. 
          IF AVAILABLE w753 THEN 
          DO: 
            w753.ytd-saldo = w753.ytd-saldo + segmentstat.persanz. 
          END. 
          IF AVAILABLE w754 THEN 
          DO: 
            w754.ytd-saldo = w754.ytd-saldo + segmentstat.kind1. 
          END. 
          IF AVAILABLE w755 THEN 
          DO: 
            w755.ytd-saldo = w755.ytd-saldo + segmentstat.kind2. 
          END. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      FOR EACH segmentstat WHERE segmentstat.datum GE datum2 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF segmentstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lytd-saldo = w11.lytd-saldo + segmentstat.zimmeranz. 
            w11.lytd-budget = w11.lytd-budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
          DO: 
            w22.lytd-saldo = w11.lytd-saldo + segmentstat.betriebsnr. 
          END. 
          IF AVAILABLE w753 THEN 
          DO: 
            w753.lytd-saldo = w753.lytd-saldo + segmentstat.persanz. 
          END. 
          IF AVAILABLE w754 THEN 
          DO: 
            w754.lytd-saldo = w754.lytd-saldo + segmentstat.kind1. 
          END. 
          IF AVAILABLE w755 THEN 
          DO: 
            w755.lytd-saldo = w755.lytd-saldo + segmentstat.kind2. 
          END. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + segmentstat.persanz /* LAST year MTD */ 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.ly-budget = w1.ly-budget + segmentstat.budpersanz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr + segmentstat.zimmeranz. 
            w11.ly-budget = w11.ly-budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
          DO: 
            w22.lastyr = w22.lastyr + segmentstat.betriebsnr. 
          END. 
          IF AVAILABLE w753 THEN 
          DO: 
            w753.lastyr = w753.lastyr + segmentstat.persanz. 
          END. 
          IF AVAILABLE w754 THEN 
          DO: 
            w754.lastyr = w754.lastyr + segmentstat.kind1. 
          END. 
          IF AVAILABLE w755 THEN 
          DO: 
            w755.lastyr = w755.lastyr + segmentstat.kind2. 
          END. 
 
          IF lytd-flag THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
            IF AVAILABLE w11 THEN 
            DO: 
              w11.lytd-saldo = w11.lytd-saldo + segmentstat.zimmeranz. 
              w11.lytd-budget = w11.lytd-budget + segmentstat.budzimmeranz. 
            END. 
            IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
            DO: 
              w22.lytd-saldo = w22.lytd-saldo + segmentstat.betriebsnr. 
            END. 
            IF AVAILABLE w753 THEN 
            DO: 
              w753.lytd-saldo = w753.lytd-saldo + segmentstat.persanz. 
            END. 
            IF AVAILABLE w754 THEN 
            DO: 
              w754.lytd-saldo = w754.lytd-saldo + segmentstat.kind1. 
            END. 
            IF AVAILABLE w755 THEN 
            DO: 
              w755.lytd-saldo = w755.lytd-saldo + segmentstat.kind2. 
            END. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + segmentstat.persanz 
        + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
      w1.lm-budget = w1.lm-budget + segmentstat.budpersanz. 
      IF AVAILABLE w11 THEN 
      DO: 
        w11.lastmon = w11.lastmon + segmentstat.zimmeranz. 
        w11.lm-budget = w11.lm-budget + segmentstat.budzimmeranz. 
      END. 
      IF AVAILABLE w22 AND segment.betriebsnr = 0 THEN 
      DO: 
        w22.lastmon = w22.lastmon + segmentstat.betriebsnr. 
      END. 
      IF AVAILABLE w753 THEN 
      DO: 
         w753.lastmon = w753.lastmon + segmentstat.persanz. 
      END. 
      IF AVAILABLE w754 THEN 
      DO: 
        w754.lastmon = w754.lastmon + segmentstat.kind1. 
      END. 
      IF AVAILABLE w755 THEN 
      DO: 
        w755.lastmon = w755.lastmon + segmentstat.kind2. 
      END. 
    END. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w22 THEN w22.done = YES. 
  IF AVAILABLE w753 THEN w753.done = YES. 
  IF AVAILABLE w754 THEN w754.done = YES. 
  IF AVAILABLE w755 THEN w755.done = YES. 
END. 


PROCEDURE fill-avrgrate: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w11 WHERE w11.main-code = 842 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zinrstat.argtumsatz. 
        IF AVAILABLE w11 THEN w11.tday = w11.tday 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF ytd-flag THEN w11.ytd-saldo = w11.ytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "avrgrate" NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
            IF lytd-flag THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      IF AVAILABLE w11 THEN 
        w11.lastmon = w11.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz. 
    END. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
END. 


PROCEDURE fill-avrgLrate: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w11 WHERE w11.main-code = 46 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zinrstat.argtumsatz. 
        IF AVAILABLE w11 THEN w11.tday = w11.tday 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF ytd-flag THEN w11.ytd-saldo = w11.ytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
            IF lytd-flag THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      IF AVAILABLE w11 THEN 
        w11.lastmon = w11.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz. 
    END. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
END. 


PROCEDURE fill-avrglodge: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w11 WHERE w11.main-code = 811 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zinrstat.logisumsatz. 
        IF AVAILABLE w11 THEN w11.tday = w11.tday 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF ytd-flag THEN w11.ytd-saldo = w11.ytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "avrgrate" NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
            IF lytd-flag THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(zinrstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      IF AVAILABLE w11 THEN 
        w11.lastmon = w11.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz. 
    END. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
END. 



PROCEDURE fill-segment: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 
DEFINE VARIABLE segm AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
DEFINE buffer w12 FOR w1. 
DEFINE buffer w13 FOR w1. 
DEFINE buffer w756 FOR w1. 
DEFINE buffer w757 FOR w1. 
DEFINE buffer w758 FOR w1. 
 
  lytoday-flag = (lytd-flag OR lmtd-flag) AND (month(to-date) NE 2 
    OR day(to-date) NE 29). 
 
  IF main-nr = 92 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    segm = w1.artnr. 
    FIND FIRST w12 WHERE w12.main-code = 813 AND w12.artnr = segm 
      AND NOT w12.done NO-ERROR. 
    FIND FIRST w13 WHERE w13.main-code = 814 AND w13.artnr = segm 
      AND NOT w13.done NO-ERROR. 
    FIND FIRST w756 WHERE w756.main-code = 756 AND w756.artnr = segm 
      AND NOT w756.done NO-ERROR. 
    FIND FIRST w757 WHERE w757.main-code = 757 AND w757.artnr = segm 
      AND NOT w757.done NO-ERROR. 
    FIND FIRST w758 WHERE w758.main-code = 758 AND w758.artnr = segm 
      AND NOT w758.done NO-ERROR. 
  END. 
  ELSE IF main-nr = 813 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    segm = w1.artnr. 
    FIND FIRST w11 WHERE w11.main-code = 92 AND w11.artnr = segm 
      AND NOT w11.done NO-ERROR. 
    FIND FIRST w13 WHERE w13.main-code = 814 AND w13.artnr = segm 
      AND NOT w13.done NO-ERROR. 
    FIND FIRST w757 WHERE w757.main-code = 757 AND w757.artnr = segm 
      AND NOT w757.done NO-ERROR. 
    FIND FIRST w758 WHERE w758.main-code = 758 AND w758.artnr = segm 
      AND NOT w758.done NO-ERROR. 
  END. 
  ELSE IF main-nr = 814 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    segm = w1.artnr. 
    FIND FIRST w11 WHERE w11.main-code = 92 AND w11.artnr = segm 
      AND NOT w11.done NO-ERROR. 
    FIND FIRST w12 WHERE w12.main-code = 813 AND w12.artnr = segm 
      AND NOT w12.done NO-ERROR. 
    FIND FIRST w757 WHERE w757.main-code = 757 AND w757.artnr = segm 
      AND NOT w757.done NO-ERROR. 
    FIND FIRST w758 WHERE w758.main-code = 758 AND w758.artnr = segm 
      AND NOT w758.done NO-ERROR. 
  END. 
 
  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segm NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF segmentstat.datum = to-date THEN 
      DO: 
        release segmbuff. 
        IF lytoday-flag THEN 
        DO: 
          lytoday = to-date - 365. 
          FIND FIRST segmbuff WHERE segmbuff.datum = lytoday 
            AND segmbuff.segmentcode = segment.segmentcode NO-LOCK NO-ERROR. 
        END. 
        IF main-nr = 92 THEN 
        DO: 
          w1.tday = w1.tday + segmentstat.logis / frate. 
          w1.tbudget = w1.tbudget + segmentstat.budlogis. 
          IF AVAILABLE segmbuff THEN 
            w1.lytoday = w1.lytoday + segmbuff.logis / frate. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.tday = w12.tday + segmentstat.zimmeranz. 
            w12.tbudget = w12.tbudget + segmentstat.budzimmeranz. 
            IF AVAILABLE segmbuff THEN 
              w12.lytoday = w12.lytoday + segmbuff.zimmeranz. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.tday = w13.tday + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.tbudget = w13.tbudget + segmentstat.budpersanz. 
            IF AVAILABLE segmbuff THEN 
              w13.lytoday = w13.lytoday + segmbuff.persanz 
              + segmbuff.kind1 + segmbuff.kind2 + segmbuff.gratis. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.tday = w756.tday + segmentstat.persanz. 
            w756.tbudget = w756.tbudget + segmentstat.budpersanz. 
            IF AVAILABLE segmbuff THEN 
              w756.lytoday = w756.lytoday + segmbuff.persanz. 
          END. 
          IF AVAILABLE w757 THEN 
          DO: 
            w757.tday = w757.tday + segmentstat.kind1. 
            IF AVAILABLE segmbuff THEN 
              w757.lytoday = w757.lytoday + segmbuff.kind1. 
          END. 
          IF AVAILABLE w758 THEN 
          DO: 
            w758.tday = w758.tday + segmentstat.kind2. 
            IF AVAILABLE segmbuff THEN 
              w758.lytoday = w758.lytoday + segmbuff.kind2. 
          END. 
        END. 
        ELSE IF main-nr = 813 THEN 
        DO: 
          w1.tday = w1.tday + segmentstat.zimmeranz. 
          w1.tbudget = w1.tbudget + segmentstat.budzimmeranz. 
          IF AVAILABLE segmbuff THEN 
            w1.lytoday = w1.lytoday + segmbuff.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.tday = w11.tday + segmentstat.logis / frate. 
            w11.tbudget = w11.tbudget + segmentstat.budlogis. 
            IF AVAILABLE segmbuff THEN 
              w11.lytoday = w11.lytoday + segmbuff.logis / frate. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.tday = w13.tday + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.tbudget = w13.tbudget + segmentstat.budpersanz. 
            IF AVAILABLE segmbuff THEN 
              w13.lytoday = w13.lytoday + segmbuff.persanz 
              + segmbuff.kind1 + segmbuff.kind2 + segmbuff.gratis. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.tday = w756.tday + segmentstat.persanz. 
            w756.tbudget = w756.tbudget + segmentstat.budpersanz. 
            IF AVAILABLE segmbuff THEN 
              w756.lytoday = w756.lytoday + segmbuff.persanz. 
          END. 
          IF AVAILABLE w757 THEN 
          DO: 
            w757.tday = w757.tday + segmentstat.kind1. 
            IF AVAILABLE segmbuff THEN 
              w757.lytoday = w757.lytoday + segmbuff.kind1. 
          END. 
          IF AVAILABLE w758 THEN 
          DO: 
            w758.tday = w758.tday + segmentstat.kind2. 
            IF AVAILABLE segmbuff THEN 
              w758.lytoday = w758.lytoday + segmbuff.kind2. 
          END. 
          END. 
        END. 
        ELSE IF main-nr = 814 THEN 
        DO: 
          w1.tday = w1.tday + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.tbudget = w1.tbudget + segmentstat.budpersanz. 
          IF AVAILABLE segmbuff THEN 
            w1.lytoday = w1.lytoday + segmbuff.persanz 
              + segmbuff.kind1 + segmbuff.kind2 + segmbuff.gratis. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.tday = w11.tday + segmentstat.logis / frate. 
            w11.tbudget = w11.tbudget + segmentstat.budlogis. 
            IF AVAILABLE segmbuff THEN 
              w1.lytoday = w1.lytoday + segmbuff.logis / frate. 
          END. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.tday = w12.tday + segmentstat.zimmeranz. 
            w12.tbudget = w12.tbudget + segmentstat.budzimmeranz. 
            IF AVAILABLE segmbuff THEN 
              w12.lytoday = w12.lytoday + segmbuff.zimmeranz. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.tday = w756.tday + segmentstat.persanz. 
            w756.tbudget = w756.tbudget + segmentstat.budpersanz. 
            IF AVAILABLE segmbuff THEN 
              w756.lytoday = w756.lytoday + segmbuff.persanz. 
          END. 
          IF AVAILABLE w757 THEN 
          DO: 
            w757.tday = w757.tday + segmentstat.kind1. 
            IF AVAILABLE segmbuff THEN 
              w757.lytoday = w757.lytoday + segmbuff.kind1. 
          END. 
          IF AVAILABLE w758 THEN 
          DO: 
            w758.tday = w758.tday + segmentstat.kind2. 
            IF AVAILABLE segmbuff THEN 
              w758.lytoday = w758.lytoday + segmbuff.kind2. 
          END. 
        END. 
      END. 
 
      IF segmentstat.datum LT from-date THEN 
      DO: 
        IF main-nr = 92 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.logis / frate. 
          w1.ytd-budget = w1.ytd-budget + segmentstat.budlogis. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
            w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.ytd-saldo = w756.ytd-saldo + segmentstat.persanz. 
            w756.ytd-budget = w756.ytd-budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w757 THEN 
            w757.ytd-saldo = w757.ytd-saldo + segmentstat.kind1. 
          IF AVAILABLE w758 THEN 
            w758.ytd-saldo = w758.ytd-saldo + segmentstat.kind2. 
        END. 
        ELSE IF main-nr = 813 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.zimmeranz. 
          w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
            w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.ytd-saldo = w756.ytd-saldo + segmentstat.persanz. 
            w756.ytd-budget = w756.ytd-budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w757 THEN 
            w757.ytd-saldo = w757.ytd-saldo + segmentstat.kind1. 
          IF AVAILABLE w758 THEN 
            w758.ytd-saldo = w758.ytd-saldo + segmentstat.kind2. 
        END. 
        ELSE IF main-nr = 814 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
            w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
          END. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
            w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.ytd-saldo = w756.ytd-saldo + segmentstat.persanz. 
            w756.ytd-budget = w756.ytd-budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w757 THEN 
            w757.ytd-saldo = w757.ytd-saldo + segmentstat.kind1. 
          IF AVAILABLE w758 THEN 
            w758.ytd-saldo = w758.ytd-saldo + segmentstat.kind2. 
        END. 
      END. 
      ELSE 
      DO: 
        IF main-nr = 92 THEN 
        DO: 
          w1.saldo = w1.saldo + segmentstat.logis / frate. 
          w1.budget = w1.budget + segmentstat.budlogis. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.saldo = w12.saldo + segmentstat.zimmeranz. 
            w12.budget = w12.budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.saldo = w13.saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.budget = w13.budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.saldo = w756.saldo + segmentstat.persanz. 
            w756.budget = w756.budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w757 THEN 
            w757.saldo = w757.saldo + segmentstat.kind1. 
          IF AVAILABLE w758 THEN 
            w758.saldo = w758.saldo + segmentstat.kind2. 
        END. 
        ELSE IF main-nr = 813 THEN 
        DO: 
          w1.saldo = w1.saldo + segmentstat.zimmeranz. 
          w1.budget = w1.budget + segmentstat.budzimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.saldo = w11.saldo + segmentstat.logis / frate. 
            w11.budget = w11.budget + segmentstat.budlogis. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.saldo = w13.saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.budget = w13.budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.saldo = w756.saldo + segmentstat.persanz. 
            w756.budget = w756.budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w757 THEN 
            w757.saldo = w757.saldo + segmentstat.kind1. 
          IF AVAILABLE w758 THEN 
            w758.saldo = w758.saldo + segmentstat.kind2. 
        END. 
        ELSE IF main-nr = 814 THEN 
        DO: 
          w1.saldo = w1.saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.budget = w1.budget + segmentstat.budpersanz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.saldo = w11.saldo + segmentstat.logis / frate. 
            w11.budget = w11.budget + segmentstat.budlogis. 
          END. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.saldo = w12.saldo + segmentstat.zimmeranz. 
            w12.budget = w12.budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w756 THEN 
          DO: 
            w756.saldo = w756.saldo + segmentstat.persanz. 
            w756.budget = w756.budget + segmentstat.budpersanz. 
          END. 
          IF AVAILABLE w757 THEN 
            w757.saldo = w757.saldo + segmentstat.kind1. 
          IF AVAILABLE w758 THEN 
            w758.saldo = w758.saldo + segmentstat.kind2. 
        END. 
 
        IF ytd-flag THEN 
        DO: 
          IF main-nr = 92 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + segmentstat.logis / frate. 
            w1.ytd-budget = w1.ytd-budget + segmentstat.budlogis. 
            IF AVAILABLE w12 THEN 
            DO: 
              w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
              w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
            END. 
            IF AVAILABLE w13 THEN 
            DO: 
              w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.ytd-saldo = w756.ytd-saldo + segmentstat.persanz. 
              w756.ytd-budget = w756.ytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.ytd-saldo = w757.ytd-saldo + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.ytd-saldo = w758.ytd-saldo + segmentstat.kind2. 
          END. 
          ELSE IF main-nr = 813 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + segmentstat.zimmeranz. 
            w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
            IF AVAILABLE w11 THEN 
            DO: 
              w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
              w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
            END. 
            IF AVAILABLE w13 THEN 
            DO: 
              w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.ytd-saldo = w756.ytd-saldo + segmentstat.persanz. 
              w756.ytd-budget = w756.ytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.ytd-saldo = w757.ytd-saldo + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.ytd-saldo = w758.ytd-saldo + segmentstat.kind2. 
          END. 
          ELSE IF main-nr = 814 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
            IF AVAILABLE w11 THEN 
            DO: 
              w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
              w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
            END. 
            IF AVAILABLE w12 THEN 
            DO: 
              w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
              w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.ytd-saldo = w756.ytd-saldo + segmentstat.persanz. 
              w756.ytd-budget = w756.ytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.ytd-saldo = w757.ytd-saldo + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.ytd-saldo = w758.ytd-saldo + segmentstat.kind2. 
          END. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segm NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF segmentstat.datum LT Lfrom-date THEN 
        DO: 
          IF main-nr = 92 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + segmentstat.logis / frate. 
            w1.lytd-budget = w1.lytd-budget + segmentstat.budlogis. 
            IF AVAILABLE w12 THEN 
            DO: 
              w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
              w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
            END. 
            IF AVAILABLE w13 THEN 
            DO: 
              w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.lytd-saldo = w756.lytd-saldo + segmentstat.persanz. 
              w756.lytd-budget = w756.lytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.lytd-saldo = w757.lytd-saldo + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.lytd-saldo = w758.lytd-saldo + segmentstat.kind2. 
          END. 
          ELSE IF main-nr = 813 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + segmentstat.zimmeranz. 
            w1.lytd-budget = w1.lytd-budget + segmentstat.budzimmeranz. 
            IF AVAILABLE w11 THEN 
            DO: 
              w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
              w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
            END. 
            IF AVAILABLE w13 THEN 
            DO: 
              w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.lytd-saldo = w756.lytd-saldo + segmentstat.persanz. 
              w756.lytd-budget = w756.lytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.lytd-saldo = w757.lytd-saldo + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.lytd-saldo = w758.lytd-saldo + segmentstat.kind2. 
          END. 
          ELSE IF main-nr = 814 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + segmentstat.persanz 
               + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
            IF AVAILABLE w11 THEN 
            DO: 
              w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
              w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
            END. 
            IF AVAILABLE w12 THEN 
            DO: 
              w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
              w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.lytd-saldo = w756.lytd-saldo + segmentstat.persanz. 
              w756.lytd-budget = w756.lytd-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.lytd-saldo = w757.lytd-saldo + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.lytd-saldo = w758.lytd-saldo + segmentstat.kind2. 
          END. 
        END. 
        ELSE 
        DO: /* LAST year MTD */ 
          IF main-nr = 92 THEN 
          DO: 
            w1.lastyr = w1.lastyr + segmentstat.logis / frate. 
            w1.ly-budget = w1.ly-budget + segmentstat.budlogis. 
            IF AVAILABLE w12 THEN 
            DO: 
              w12.lastyr = w12.lastyr + segmentstat.zimmeranz. 
              w12.ly-budget = w12.ly-budget + segmentstat.budzimmeranz. 
            END. 
            IF AVAILABLE w13 THEN 
            DO: 
              w13.lastyr = w13.lastyr + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.ly-budget = w13.ly-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.lastyr = w756.lastyr + segmentstat.persanz. 
              w756.ly-budget = w756.ly-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.lastyr = w757.lastyr + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.lastyr = w758.lastyr + segmentstat.kind2. 
          END. 
          ELSE IF main-nr = 813 THEN 
          DO: 
            w1.lastyr = w1.lastyr + segmentstat.zimmeranz. 
            w1.ly-budget = w1.ly-budget + segmentstat.budzimmeranz. 
            IF AVAILABLE w11 THEN 
            DO: 
              w11.lastyr = w11.lastyr + segmentstat.logis / frate. 
              w11.ly-budget = w11.ly-budget + segmentstat.budlogis. 
            END. 
            IF AVAILABLE w13 THEN 
            DO: 
              w13.lastyr = w13.lastyr + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.ly-budget = w13.ly-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.lastyr = w756.lastyr + segmentstat.persanz. 
              w756.ly-budget = w756.ly-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.lastyr = w757.lastyr + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.lastyr = w758.lastyr + segmentstat.kind2. 
          END. 
          ELSE IF main-nr = 814 THEN 
          DO: 
            w1.lastyr = w1.lastyr + segmentstat.persanz 
               + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1.ly-budget = w1.ly-budget + segmentstat.budpersanz. 
            IF AVAILABLE w11 THEN 
            DO: 
              w11.lastyr = w11.lastyr + segmentstat.logis / frate. 
              w11.ly-budget = w11.ly-budget + segmentstat.budlogis. 
            END. 
            IF AVAILABLE w12 THEN 
            DO: 
              w12.lastyr = w12.lastyr + segmentstat.zimmeranz. 
              w12.ly-budget = w12.ly-budget + segmentstat.budzimmeranz. 
            END. 
            IF AVAILABLE w756 THEN 
            DO: 
              w756.lastyr = w756.lastyr + segmentstat.persanz. 
              w756.ly-budget = w756.ly-budget + segmentstat.budpersanz. 
            END. 
            IF AVAILABLE w757 THEN 
              w757.lastyr = w757.lastyr + segmentstat.kind1. 
            IF AVAILABLE w758 THEN 
              w758.lastyr = w758.lastyr + segmentstat.kind2. 
          END. 
 
          IF lytd-flag THEN 
          DO: 
            IF main-nr = 92 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + segmentstat.logis / frate. 
              w1.lytd-budget = w1.lytd-budget + segmentstat.budlogis. 
              IF AVAILABLE w12 THEN 
              DO: 
                w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
                w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
              END. 
              IF AVAILABLE w13 THEN 
              DO: 
                w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
                  + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
                w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
              END. 
              IF AVAILABLE w756 THEN 
              DO: 
                w756.lytd-saldo = w756.lytd-saldo + segmentstat.persanz. 
                w756.lytd-budget = w756.lytd-budget + segmentstat.budpersanz. 
              END. 
              IF AVAILABLE w757 THEN 
                w757.lytd-saldo = w757.lytd-saldo + segmentstat.kind1. 
              IF AVAILABLE w758 THEN 
                w758.lytd-saldo = w758.lytd-saldo + segmentstat.kind2. 
            END. 
            ELSE IF main-nr = 813 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + segmentstat.zimmeranz. 
              w1.lytd-budget = w1.lytd-budget + segmentstat.budzimmeranz. 
              IF AVAILABLE w11 THEN 
              DO: 
                w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
                w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
              END. 
              IF AVAILABLE w13 THEN 
              DO: 
                w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
                  + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
                w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
              END. 
              IF AVAILABLE w756 THEN 
              DO: 
                w756.lytd-saldo = w756.lytd-saldo + segmentstat.persanz. 
                w756.lytd-budget = w756.lytd-budget + segmentstat.budpersanz. 
              END. 
              IF AVAILABLE w757 THEN 
                w757.lytd-saldo = w757.lytd-saldo + segmentstat.kind1. 
              IF AVAILABLE w758 THEN 
                w758.lytd-saldo = w758.lytd-saldo + segmentstat.kind2. 
            END. 
            ELSE IF main-nr = 814 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
              IF AVAILABLE w11 THEN 
              DO: 
                w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
                w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
              END. 
              IF AVAILABLE w12 THEN 
              DO: 
                w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
                w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
              END. 
              IF AVAILABLE w756 THEN 
              DO: 
                w756.lytd-saldo = w756.lytd-saldo + segmentstat.persanz. 
                w756.lytd-budget = w756.lytd-budget + segmentstat.budpersanz. 
              END. 
              IF AVAILABLE w757 THEN 
                w757.lytd-saldo = w757.lytd-saldo + segmentstat.kind1. 
              IF AVAILABLE w758 THEN 
                w758.lytd-saldo = w758.lytd-saldo + segmentstat.kind2. 
            END. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segm NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF main-nr = 92 THEN 
      DO: 
        w1.lastmon = w1.lastmon + segmentstat.logis / frate. 
        w1.lm-budget = w1.lm-budget + segmentstat.budlogis. 
        IF AVAILABLE w12 THEN 
        DO: 
          w12.lastmon = w12.lastmon + segmentstat.zimmeranz. 
          w12.lm-budget = w12.lm-budget + segmentstat.budzimmeranz. 
        END. 
        IF AVAILABLE w13 THEN 
        DO: 
          w13.lastmon = w13.lastmon + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w13.lm-budget = w13.lm-budget + segmentstat.budpersanz. 
        END. 
        IF AVAILABLE w756 THEN 
        DO: 
          w756.lastmon = w756.lastmon + segmentstat.persanz. 
          w756.lm-budget = w756.lm-budget + segmentstat.budpersanz. 
        END. 
        IF AVAILABLE w757 THEN 
          w757.lastmon = w757.lastmon + segmentstat.kind1. 
        IF AVAILABLE w758 THEN 
          w758.lastmon = w758.lastmon + segmentstat.kind2. 
      END. 
      ELSE IF main-nr = 813 THEN 
      DO: 
        w1.lastmon = w1.lastmon + segmentstat.zimmeranz. 
        w1.lm-budget = w1.lm-budget + segmentstat.budzimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.lastmon = w11.lastmon + segmentstat.logis / frate. 
          w11.lm-budget = w11.lm-budget + segmentstat.budlogis. 
        END. 
        IF AVAILABLE w13 THEN 
        DO: 
          w13.lastmon = w13.lastmon + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w13.lm-budget = w13.lm-budget + segmentstat.budpersanz. 
        END. 
        IF AVAILABLE w756 THEN 
        DO: 
          w756.lastmon = w756.lastmon + segmentstat.persanz. 
          w756.lm-budget = w756.lm-budget + segmentstat.budpersanz. 
        END. 
        IF AVAILABLE w757 THEN 
          w757.lastmon = w757.lastmon + segmentstat.kind1. 
        IF AVAILABLE w758 THEN 
          w758.lastmon = w758.lastmon + segmentstat.kind2. 
      END. 
      ELSE IF main-nr = 814 THEN 
      DO: 
        w1.lastmon = w1.lastmon + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1.lm-budget = w1.lm-budget + segmentstat.budpersanz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.lastmon = w11.lastmon + segmentstat.logis / frate. 
          w11.lm-budget = w11.lm-budget + segmentstat.budlogis. 
        END. 
        IF AVAILABLE w12 THEN 
        DO: 
          w12.lastmon = w12.lastmon + segmentstat.zimmeranz. 
          w12.lm-budget = w12.lm-budget + segmentstat.budzimmeranz. 
        END. 
        IF AVAILABLE w756 THEN 
        DO: 
          w756.lastmon = w756.lastmon + segmentstat.persanz. 
          w756.lm-budget = w756.lm-budget + segmentstat.budpersanz. 
        END. 
        IF AVAILABLE w757 THEN 
          w757.lastmon = w757.lastmon + segmentstat.kind1. 
        IF AVAILABLE w758 THEN 
          w758.lastmon = w758.lastmon + segmentstat.kind2. 
      END. 
    END. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w12 THEN w12.done = YES. 
  IF AVAILABLE w13 THEN w13.done = YES. 
  IF AVAILABLE w756 THEN w756.done = YES. 
  IF AVAILABLE w757 THEN w757.done = YES. 
  IF AVAILABLE w758 THEN w758.done = YES. 
END. 


PROCEDURE fill-rmcatstat: 
DEFINE INPUT PARAMETER rec-w1   AS INTEGER. 
DEFINE INPUT PARAMETER main-nr  AS INTEGER. 
DEFINE VARIABLE zikatno         AS INTEGER. 
DEFINE VARIABLE datum1          AS DATE. 
 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    zikatno = w1.artnr. 

    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH zkstat WHERE zkstat.datum GE datum1 
      AND zkstat.datum LE to-date AND zkstat.zikatnr = zikatno NO-LOCK: 
      IF zkstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zkstat.zimmeranz 
          - zkstat.betriebsnr + zkstat.arrangement-art[1].
      END. 
      IF zkstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zkstat.zimmeranz
          - zkstat.betriebsnr + zkstat.arrangement-art[1].
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zkstat.zimmeranz
          - zkstat.betriebsnr + zkstat.arrangement-art[1].
        IF ytd-flag THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zkstat.zimmeranz 
            - zkstat.betriebsnr + zkstat.arrangement-art[1].
        END. 
      END. 
    END. 
    
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zkstat WHERE zkstat.datum GE datum1 
        AND zkstat.datum LE Lto-date AND zkstat.zikatnr = zikatno NO-LOCK: 
        IF zkstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo + zkstat.zimmeranz
            - zkstat.betriebsnr + zkstat.arrangement-art[1].
        END. 
        ELSE 
        DO: /* LAST year MTD */ 
          w1.lastyr = w1.lastyr + zkstat.zimmeranz
            - zkstat.betriebsnr + zkstat.arrangement-art[1].
          IF lytd-flag THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zkstat.zimmeranz
              - zkstat.betriebsnr + zkstat.arrangement-art[1].
          END. 
        END. 
      END. 
    END.     
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zkstat WHERE zkstat.datum GE Pfrom-date AND zkstat.datum 
      LE Pto-date AND zkstat.zikatnr = zikatno NO-LOCK: 
      w1.lastmon = w1.lastmon + zkstat.zimmeranz
        - zkstat.betriebsnr + zkstat.arrangement-art[1].
    END.  
    w1.done = YES. 
END. 


PROCEDURE fill-zinrstat: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 
DEFINE VARIABLE rmno AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE buffer w11 FOR w1. 
DEFINE buffer w12 FOR w1. 
DEFINE buffer w13 FOR w1. 
 
  IF main-nr = 800 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    rmno = w1.artnr. 
    FIND FIRST w12 WHERE w12.main-code = 180 AND w12.artnr = rmno NO-ERROR. 
    FIND FIRST w13 WHERE w13.main-code = 181 AND w13.artnr = rmno NO-ERROR. 
  END. 
  ELSE IF main-nr = 180 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    rmno = w1.artnr. 
    FIND FIRST w11 WHERE w11.main-code = 800 AND w11.artnr = rmno NO-ERROR. 
    FIND FIRST w13 WHERE w13.main-code = 181 AND w13.artnr = rmno NO-ERROR. 
  END. 
  ELSE IF main-nr = 181 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    rmno = w1.artnr. 
    FIND FIRST w11 WHERE w11.main-code = 800 AND w11.artnr = rmno NO-ERROR. 
    FIND FIRST w12 WHERE w12.main-code = 180 AND w12.artnr = rmno NO-ERROR. 
  END. 
 
  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = STRING(rmno) NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(zinrstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF zinrstat.datum = to-date THEN 
      DO: 
        IF main-nr = 800 THEN 
        DO: 
          w1.tday = w1.tday + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN w12.tday = w12.tday + zinrstat.zimmeranz. 
          IF AVAILABLE w13 THEN w13.tday = w13.tday + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 180 THEN 
        DO: 
          w1.tday = w1.tday + zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.tday = w11.tday + zinrstat.logisumsatz 
            / frate. 
          IF AVAILABLE w13 THEN w13.tday = w13.tday + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 181 THEN 
        DO: 
          w1.tday = w1.tday + zinrstat.personen. 
          IF AVAILABLE w11 THEN w11.tday = w11.tday + zinrstat.logisumsatz 
            / frate. 
          IF AVAILABLE w12 THEN w12.tday = w12.tday + zinrstat.zimmeranz. 
        END. 
      END. 
 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        IF main-nr = 800 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w13 THEN 
            w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 180 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
            w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w13 THEN 
            w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 181 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zinrstat.personen. 
          IF AVAILABLE w11 THEN 
            w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
      ELSE 
      DO: 
        IF main-nr = 800 THEN 
        DO: 
          w1.saldo = w1.saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.saldo = w12.saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w13 THEN 
            w13.saldo = w13.saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 180 THEN 
        DO: 
          w1.saldo = w1.saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
            w11.saldo = w11.saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w13 THEN 
            w13.saldo = w13.saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 181 THEN 
        DO: 
          w1.saldo = w1.saldo + zinrstat.personen. 
          IF AVAILABLE w11 THEN 
            w11.saldo = w11.saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.saldo = w12.saldo + zinrstat.zimmeranz. 
        END. 
 
        IF ytd-flag THEN 
        DO: 
          IF main-nr = 800 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w13 THEN 
              w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 180 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w11 THEN 
              w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w13 THEN 
              w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 181 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + zinrstat.personen. 
            IF AVAILABLE w11 THEN 
              w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = STRING(rmno) NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(zinrstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          IF main-nr = 800 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w13 THEN 
              w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 180 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w11 THEN 
              w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w13 THEN 
              w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 181 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zinrstat.personen. 
            IF AVAILABLE w11 THEN 
              w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
          END. 
        END. 
        ELSE 
        DO: /* LAST year MTD */ 
          IF main-nr = 800 THEN 
          DO: 
            w1.lastyr = w1.lastyr + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lastyr = w12.lastyr + zinrstat.zimmeranz. 
            IF AVAILABLE w13 THEN 
              w13.lastyr = w13.lastyr + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 180 THEN 
          DO: 
            w1.lastyr = w1.lastyr + zinrstat.zimmeranz. 
            IF AVAILABLE w11 THEN 
              w11.lastyr = w11.lastyr + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w13 THEN 
              w13.lastyr = w13.lastyr + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 181 THEN 
          DO: 
            w1.lastyr = w1.lastyr + zinrstat.personen. 
            IF AVAILABLE w11 THEN 
              w11.lastyr = w11.lastyr + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lastyr = w12.lastyr + zinrstat.zimmeranz. 
          END. 
 
          IF lytd-flag THEN 
          DO: 
            IF main-nr = 800 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + zinrstat.logisumsatz / frate. 
              IF AVAILABLE w12 THEN 
                w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
              IF AVAILABLE w13 THEN 
                w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
            END. 
            ELSE IF main-nr = 180 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
              IF AVAILABLE w11 THEN 
                w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
              IF AVAILABLE w13 THEN 
                w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
            END. 
            ELSE IF main-nr = 181 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + zinrstat.personen. 
              IF AVAILABLE w11 THEN 
                w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
              IF AVAILABLE w12 THEN 
                w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
            END. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = STRING(rmno) NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(zinrstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF main-nr = 800 THEN 
      DO: 
        w1.lastmon = w1.lastmon + zinrstat.logisumsatz / frate. 
        IF AVAILABLE w12 THEN 
          w12.lastmon = w12.lastmon + zinrstat.zimmeranz. 
        IF AVAILABLE w13 THEN 
          w13.lastmon = w13.lastmon + zinrstat.personen. 
      END. 
      ELSE IF main-nr = 180 THEN 
      DO: 
        w1.lastmon = w1.lastmon + zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
          w11.lastmon = w11.lastmon + zinrstat.logisumsatz / frate. 
        IF AVAILABLE w13 THEN 
          w13.lastmon = w13.lastmon + zinrstat.personen. 
      END. 
      ELSE IF main-nr = 181 THEN 
      DO: 
        w1.lastmon = w1.lastmon + zinrstat.personen. 
        IF AVAILABLE w11 THEN 
          w11.lastmon = w11.lastmon + zinrstat.logisumsatz / frate. 
        IF AVAILABLE w12 THEN 
          w12.lastmon = w12.lastmon + zinrstat.zimmeranz. 
      END. 
    END. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w12 THEN w12.done = YES. 
  IF AVAILABLE w13 THEN w13.done = YES. 
END. 


PROCEDURE fill-value1: 
DEFINE INPUT PARAMETER recid1-w1 AS INTEGER. 
DEFINE INPUT PARAMETER recid2-w1 AS INTEGER. 
DEFINE INPUT PARAMETER val-sign AS INTEGER. 
DEFINE VARIABLE sign1 AS INTEGER. 
DEFINE buffer parent FOR w1. 
DEFINE buffer child FOR w1. 
DEFINE buffer curr-child FOR w1. 
DEFINE buffer curr-w2 FOR w2. 
DEFINE VARIABLE texte AS CHAR. 
DEFINE VARIABLE n AS INTEGER. 
  FIND FIRST parent WHERE RECID(parent) = recid1-w1. 
  FIND FIRST child WHERE RECID(child) = recid2-w1. 
  DO: 
    parent.tday = parent.tday + val-sign * child.tday. 
    parent.tbudget = parent.tbudget + val-sign * child.tbudget. 
 
    parent.saldo = parent.saldo + val-sign * child.saldo. 
    parent.budget = parent.budget + val-sign * child.budget. 
 
    parent.lastmon = parent.lastmon + val-sign * child.lastmon. 
    parent.lm-budget = parent.lm-budget + val-sign * child.lm-budget. 
 
    parent.lastyr = parent.lastyr + val-sign * child.lastyr. 
    parent.ly-budget = parent.ly-budget + val-sign * child.ly-budget. 
 
    parent.ytd-saldo = parent.ytd-saldo + val-sign * child.ytd-saldo. 
    parent.ytd-budget = parent.ytd-budget + val-sign * child.ytd-budget. 
 
    parent.lytd-saldo = parent.lytd-saldo + val-sign * child.lytd-saldo. 
    parent.lytd-budget = parent.lytd-budget + val-sign * child.lytd-budget. 
  END. 
END. 

