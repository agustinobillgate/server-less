DEFINE WORKFILE c-list 
  FIELD datum       AS DATE LABEL "Date" 
  FIELD dept        AS INTEGER 
  FIELD bemerk      AS CHAR 
  FIELD add-note    AS CHAR 
  FIELD fibukonto   LIKE gl-acct.fibukonto 
  FIELD f-acct      AS CHAR 
  FIELD b-acct      AS CHAR 
  FIELD o-acct      AS CHAR 
  FIELD rechnr      AS INTEGER FORMAT ">>>>>>>" LABEL " BillNo" 
  FIELD p-artnr     AS INTEGER FORMAT ">>>>" LABEL "P-Art" 
  FIELD f-cost      AS DECIMAL 
  FIELD b-cost      AS DECIMAL 
  FIELD o-cost      AS DECIMAL 
  FIELD t-cost      AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "Cost-of-Sales". 

DEFINE TEMP-TABLE s-list 
  FIELD fibukonto   LIKE gl-acct.fibukonto 
  FIELD bezeich     AS CHAR    FORMAT "x(28)" 
  FIELD credit      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" 
  FIELD debit       AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99". 

DEFINE TEMP-TABLE g-list 
  FIELD docu-nr     AS CHAR 
  FIELD lscheinnr   AS CHAR 
  FIELD jnr         LIKE gl-journal.jnr 
  FIELD fibukonto   LIKE gl-journal.fibukonto 
  FIELD debit       LIKE gl-journal.debit 
  FIELD credit      LIKE gl-journal.credit 
  FIELD bemerk      AS CHAR FORMAT "x(32)" 
  FIELD userinit    LIKE gl-journal.userinit 
  FIELD sysdate     LIKE gl-journal.sysdate INITIAL today 
  FIELD zeit        LIKE gl-journal.zeit 
  FIELD chginit     LIKE gl-journal.chginit 
  FIELD chgdate     LIKE gl-journal.chgdate INITIAL ? 
  FIELD add-note    AS CHAR 
  FIELD duplicate   AS LOGICAL INITIAL YES
  FIELD acct-fibukonto  LIKE gl-acct.fibukonto
  FIELD bezeich    LIKE gl-acct.bezeich.
DEFINE TEMP-TABLE t-g-list LIKE g-list.

DEF INPUT  PARAMETER pvILanguage        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER from-date          AS DATE.
DEF INPUT  PARAMETER to-date            AS DATE.
DEF INPUT  PARAMETER double-currency    AS LOGICAL.
DEF INPUT  PARAMETER foreign-nr         AS INTEGER.
DEF INPUT  PARAMETER exchg-rate         AS DECIMAL.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF OUTPUT PARAMETER curr-anz           AS INTEGER.
DEF OUTPUT PARAMETER debits             AS DECIMAL.
DEF OUTPUT PARAMETER credits            AS DECIMAL.
DEF OUTPUT PARAMETER remains            AS DECIMAL.
DEF OUTPUT PARAMETER msg-str            AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-g-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE curr-i AS INTEGER INITIAL 0. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkcompli".

RUN step-two.
RUN disp-it. 

PROCEDURE step-two: 
DEFINE buffer h-art FOR h-artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEFINE VARIABLE cost-account    AS CHAR. 
DEFINE VARIABLE cost-value      AS DECIMAL. 
DEFINE VARIABLE cost            AS DECIMAL. 
DEFINE VARIABLE rate            AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum      AS DATE INITIAL ?. 
DEFINE VARIABLE f-endkum        AS INTEGER. 
DEFINE VARIABLE b-endkum        AS INTEGER. 
DEFINE VARIABLE ldry            AS INTEGER INITIAL 0. 
DEFINE VARIABLE dstore          AS INTEGER. 
DEFINE VARIABLE transfer-ldry   AS LOGICAL. 
 
  FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
  ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
  dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE paramnr = 1106 NO-LOCK. 
  transfer-ldry = flogical. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  FOR EACH hoteldpt WHERE /* hoteldpt.num NE ldry AND */ 
    hoteldpt.num NE dstore NO-LOCK BY hoteldpt.num: 
    IF transfer-ldry OR (NOT transfer-ldry AND hoteldpt.num NE ldry) THEN 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.departement = hoteldpt.num 
      AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
        /* BY h-compli.p-artnr */ BY h-compli.rechnr: 
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
          AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        ELSE FIND FIRST exrate WHERE exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
 
      FIND FIRST c-list WHERE c-list.datum = h-compli.datum 
        AND c-list.dept = h-compli.departement 
        AND c-list.rechnr = h-compli.rechnr 
        AND c-list.p-artnr = h-compli.p-artnr NO-ERROR. 
      IF NOT AVAILABLE c-list THEN 
      DO: 
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.p-artnr 
          AND h-artikel.departement = h-compli.departement NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
          AND artikel.departement = 0 NO-LOCK. 
 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
          msg-str = msg-str + CHR(2)
                  + translateExtended ("G/L Account not found :",lvCAREA,"") + " " + artikel.fibukonto
                  + CHR(10)
                  + translateExtended ("Dept",lvCAREA,"") + " " + STRING(h-artikel.departement,"99") + " - " 
                  + STRING(h-artikel.artnr) + " " + h-artikel.bezeich
                  + CHR(10)
                  + translateExtended ("Check F/O Article :",lvCAREA,"") + " " + STRING(artikel.artnr) + " " 
                  + artikel.bezeich.
        END. 
 
        create c-list. 
        c-list.datum = h-compli.datum. 
        c-list.dept = h-compli.departement. 
        c-list.rechnr = h-compli.rechnr. 
        c-list.p-artnr = h-compli.p-artnr. 
        c-list.fibukonto = artikel.fibukonto. 
        c-list.bemerk = "*" + STRING(h-compli.rechnr) 
          + " - " + hoteldpt.depart. 
        c-list.add-note = ";&&4;" + STRING(h-compli.departement,"99") + ";" 
          + STRING(h-compli.rechnr) + ";". 
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
          AND h-artikel.departement = h-compli.departement NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
          AND artikel.departement = h-artikel.departement NO-LOCK. 
      END. 
 
      cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        cost = h-compli.anzahl * h-cost.betrag. 
        RUN cost-correction(INPUT-OUTPUT cost).
        cost = ROUND(cost,2).

        c-list.t-cost = c-list.t-cost + cost. 
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-cost.artnr 
          AND h-artikel.departement = h-cost.departement NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
          AND artikel.departement = h-artikel.departement NO-LOCK. 
 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.bezeich1 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
          msg-str = msg-str + CHR(2)
                  + translateExtended ("COST Account not found :",lvCAREA,"") + " " + artikel.bezeich1 
                  + CHR(10)
                  + translateExtended ("Dept",lvCAREA,"") + " " + STRING(h-artikel.departement,"99") + " - " 
                  + STRING(h-artikel.artnr) + " " + h-artikel.bezeich 
                  + CHR(10)
                  + translateExtended ("Check F/O Article :",lvCAREA,"") + " " + STRING(artikel.artnr) + " " 
                  + artikel.bezeich.
        END. 
 
        IF artikel.umsatzart = 6 THEN 
        DO: 
          c-list.b-cost = c-list.b-cost + cost. 
          c-list.b-acct = artikel.bezeich1. 
        END. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
        DO: 
          c-list.f-cost = c-list.f-cost + cost. 
          c-list.f-acct = artikel.bezeich1. 
        END. 
        ELSE 
        DO: 
          c-list.o-cost = c-list.o-cost + cost. 
          c-list.o-acct = artikel.bezeich1. 
        END. 
      END. 
      IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
      DO: 
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
          AND h-artikel.departement = h-compli.departement NO-LOCK. 
        
        cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
        RUN cost-correction(INPUT-OUTPUT cost).
        cost = ROUND(cost,2).
        
        c-list.t-cost = c-list.t-cost + cost. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
          AND artikel.departement = h-artikel.departement NO-LOCK. 
 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.bezeich1 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
          msg-str = msg-str + CHR(2)
                  + translateExtended ("COST Account not found :",lvCAREA,"") + " " + artikel.bezeich1 
                  + CHR(10)
                  + translateExtended ("Dept",lvCAREA,"") + " " + STRING(h-artikel.departement,"99") + " - " 
                  + STRING(h-artikel.artnr) + " " + h-artikel.bezeich 
                  + CHR(10)
                  + translateExtended ("Check F/O Article :",lvCAREA,"") + " " + STRING(artikel.artnr) + " " 
                  + artikel.bezeich.
        END. 
 
        IF artikel.umsatzart = 6 THEN 
        DO: 
          c-list.b-cost = c-list.b-cost + cost. 
          c-list.b-acct = artikel.bezeich1. 
        END. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
        DO: 
          c-list.f-cost = c-list.f-cost + cost. 
          c-list.f-acct = artikel.bezeich1. 
        END. 
        ELSE 
        DO: 
          c-list.o-cost = c-list.o-cost + cost. 
          c-list.o-acct = artikel.bezeich1. 
        END. 
      END. 
    END. 
  END. 
 
  FOR EACH c-list WHERE c-list.t-cost NE 0 BY c-list.dept BY c-list.rechnr: 
    RUN add-list. 
  END.
END. 


PROCEDURE disp-it:
  FOR EACH g-list NO-LOCK,
      FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto NO-LOCK 
      BY g-list.zeit:
      CREATE t-g-list.
      BUFFER-COPY g-list TO t-g-list.
      ASSIGN
        t-g-list.acct-fibukonto  = gl-acct.fibukonto
        t-g-list.bezeich    = gl-acct.bezeich.
  END.
END. 


PROCEDURE add-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FIND FIRST s-list WHERE s-list.fibukonto = c-list.fibukonto 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE s-list THEN 
  DO: 
    FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = c-list.fibukonto NO-LOCK. 
    create s-list. 
    s-list.fibukonto = gl-acct1.fibukonto. 
    s-list.bezeich = gl-acct1.bezeich. 
  END. 
 
  curr-anz = curr-anz + 1. 
  create g-list. 
  g-list.fibukonto = c-list.fibukonto. 
  g-list.bemerk = c-list.bemerk. 
  g-list.add-note = c-list.add-note. 
  IF c-list.t-cost GT 0 THEN 
  DO: 
    g-list.debit = g-list.debit + c-list.t-cost. 
    debits = debits + c-list.t-cost. 
    s-list.debit = s-list.debit + c-list.t-cost. 
  END. 
  ELSE 
  DO: 
    g-list.credit = g-list.credit - c-list.t-cost. 
    credits = credits - c-list.t-cost. 
    s-list.credit = s-list.credit - c-list.t-cost. 
  END. 
  g-list.userinit = user-init. 
  g-list.zeit = time + curr-i. 
  g-list.duplicate = NO. 
 
  IF c-list.f-acct NE "" THEN 
  DO: 
    FIND FIRST s-list WHERE s-list.fibukonto = c-list.f-acct 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = c-list.f-acct NO-LOCK. 
      create s-list. 
      s-list.fibukonto = gl-acct1.fibukonto. 
      s-list.bezeich = gl-acct1.bezeich. 
    END. 
 
    create g-list. 
    g-list.fibukonto = c-list.f-acct. 
    g-list.bemerk = c-list.bemerk. 
    g-list.add-note = c-list.add-note. 
    IF c-list.f-cost LT 0 THEN 
    DO: 
      g-list.debit = g-list.debit - c-list.f-cost. 
      debits = debits - c-list.f-cost. 
      s-list.debit = s-list.debit - c-list.f-cost. 
    END. 
    ELSE 
    DO: 
      g-list.credit = g-list.credit + c-list.f-cost. 
      credits = credits + c-list.f-cost. 
      s-list.credit = s-list.credit + c-list.f-cost. 
    END. 
    curr-i = curr-i + 1. 
    g-list.userinit = user-init. 
    g-list.zeit = time + curr-i. 
    g-list.duplicate = NO. 
  END. 
 
  IF c-list.b-acct NE "" THEN 
  DO: 
    FIND FIRST s-list WHERE s-list.fibukonto = c-list.b-acct 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = c-list.b-acct NO-LOCK. 
      create s-list. 
      s-list.fibukonto = gl-acct1.fibukonto. 
      s-list.bezeich = gl-acct1.bezeich. 
    END. 
 
    create g-list. 
    g-list.fibukonto = c-list.b-acct. 
    g-list.bemerk = c-list.bemerk. 
    g-list.add-note = c-list.add-note. 
    IF c-list.b-cost LT 0 THEN 
    DO: 
      g-list.debit = g-list.debit - c-list.b-cost. 
      debits = debits - c-list.b-cost. 
      s-list.debit = s-list.debit - c-list.b-cost. 
    END. 
    ELSE 
    DO: 
      g-list.credit = g-list.credit + c-list.b-cost. 
      credits = credits + c-list.b-cost. 
      s-list.credit = s-list.credit + c-list.b-cost. 
    END. 
    curr-i = curr-i + 1. 
    g-list.userinit = user-init. 
    g-list.zeit = time + curr-i. 
    g-list.duplicate = NO. 
  END. 
 
  IF c-list.o-acct NE "" THEN 
  DO: 
    FIND FIRST s-list WHERE s-list.fibukonto = c-list.o-acct 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = c-list.o-acct NO-LOCK. 
      create s-list. 
      s-list.fibukonto = gl-acct1.fibukonto. 
      s-list.bezeich = gl-acct1.bezeich. 
    END. 
 
    create g-list. 
    g-list.fibukonto = c-list.o-acct. 
    g-list.bemerk = c-list.bemerk. 
    g-list.add-note = c-list.add-note. 
    IF c-list.o-cost LT 0 THEN 
    DO: 
      g-list.debit = g-list.debit - c-list.o-cost. 
      debits = debits - c-list.o-cost. 
      s-list.debit = s-list.debit - c-list.o-cost. 
    END. 
    ELSE 
    DO: 
      g-list.credit = g-list.credit + c-list.o-cost. 
      credits = credits + c-list.o-cost. 
      s-list.credit = s-list.credit + c-list.o-cost. 
    END. 
    curr-i = curr-i + 1. 
    g-list.userinit = user-init. 
    g-list.zeit = time + curr-i. 
    g-list.duplicate = NO. 
  END. 
 
  remains = debits - credits. 
END. 

PROCEDURE cost-correction:
DEF INPUT-OUTPUT PARAMETER cost AS DECIMAL.
  FIND FIRST h-bill-line WHERE h-bill-line.rechnr = h-compli.rechnr
    AND h-bill-line.bill-datum  = h-compli.datum
    AND h-bill-line.departement = h-compli.departement
    AND h-bill-line.artnr       = h-compli.artnr
    AND h-bill-line.epreis      = h-compli.epreis NO-LOCK NO-ERROR.
  IF AVAILABLE h-bill-line AND 
    SUBSTR(h-bill-line.bezeich, LENGTH(h-bill-line.bezeich), 1) = "*" 
    AND h-bill-line.epreis NE 0 THEN
  DO:
    FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
        AND h-artikel.departement = h-bill-line.departement
        NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel AND h-artikel.artart = 0
      AND h-artikel.epreis1 GT h-bill-line.epreis THEN
     cost = cost * h-bill-line.epreis / h-artikel.epreis1.
  END.
END.

