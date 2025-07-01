
DEFINE TEMP-TABLE c-list 
  FIELD nr       AS INTEGER 
  FIELD datum    AS DATE LABEL "Date" 
  FIELD dept     AS INTEGER 
  FIELD rechnr   AS INTEGER FORMAT ">>>>>>>" LABEL " BillNo" 
  FIELD name     AS CHAR FORMAT "x(32)" LABEL "GuestName" 
  FIELD p-artnr  AS INTEGER FORMAT ">>>>>" LABEL "P-Art" 
  FIELD bezeich  AS CHAR   FORMAT "x(24)" LABEL "Description" 
  FIELD betrag   AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "  Bill-Amount" 
  FIELD t-cost   AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "Cost-of-Sales" 
  FIELD deptname AS CHAR FORMAT "x(24)" LABEL "Department". 
 
DEFINE TEMP-TABLE c1-list LIKE c-list. 

DEF INPUT PARAMETER foreign-nr AS INT.
DEF INPUT PARAMETER sorttype AS INT.
DEF INPUT PARAMETER from-dept AS INT.
DEF INPUT PARAMETER to-dept AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR c-list.

DEFINE VARIABLE it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE n AS INTEGER. 

IF sorttype = 2 THEN RUN journal-list1.
ELSE IF sorttype = 3 THEN RUN journal-list2. 

/**************************** PROCEDURES **************************************/ 
PROCEDURE journal-list1: 
DEFINE VARIABLE amount AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amount AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-amount AS DECIMAL. 
DEFINE VARIABLE rechnr AS INTEGER. 
DEFINE VARIABLE dept AS INTEGER INITIAL -1. 
DEFINE VARIABLE p-artnr AS INTEGER. 
DEFINE VARIABLE depart AS CHAR. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE artnr AS INTEGER. 
DEFINE VARIABLE datum AS DATE INITIAL ?. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
 
DEFINE buffer h-art FOR h-artikel. 
DEFINE buffer fr-art FOR artikel. 
 
DEFINE VARIABLE cost AS DECIMAL. 
DEFINE VARIABLE t-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tt-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tt-betrag AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE curr-artnr AS INTEGER. 
DEFINE VARIABLE nr AS INTEGER. 
 
  FOR EACH c-list: 
    delete c-list. 
  END. 
  FOR EACH c1-list: 
    delete c1-list. 
  END. 
  it-exist = NO. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.departement = hoteldpt.num 
      AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
        BY h-compli.rechnr: 
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr 
          = foreign-nr AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        ELSE FIND FIRST exrate WHERE exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate.
      END. 
 
      FIND FIRST c1-list WHERE c1-list.datum = h-compli.datum 
        AND c1-list.dept = h-compli.departement 
        AND c1-list.rechnr = h-compli.rechnr 
        AND c1-list.p-artnr = h-compli.p-artnr NO-ERROR. 
 
      IF NOT AVAILABLE c1-list THEN 
      DO: 
        create c1-list. 
        c1-list.datum = h-compli.datum. 
        c1-list.dept = h-compli.departement. 
        c1-list.deptname = hoteldpt.depart. 
        c1-list.rechnr = h-compli.rechnr. 
        c1-list.p-artnr = h-compli.p-artnr. 
        FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr 
          AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN c1-list.name = h-bill.bilname. 
        c1-list.bezeich = h-art.bezeich. 
      END. 
 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
        AND h-artikel.departement = h-compli.departement NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-compli.departement NO-LOCK. 
 
      cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        cost = h-compli.anzahl * h-cost.betrag. 
        tt-cost = tt-cost + cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
      END. 
 
      IF (NOT AVAILABLE h-cost AND h-compli.datum LT billdate)
        OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
      DO: 
        cost = h-compli.anzahl * h-compli.epreis 
          * h-artikel.prozent / 100 * rate. 
        tt-cost = tt-cost + cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
      END. 
 
/** Bill Amount  **/ 
      c1-list.betrag = c1-list.betrag 
        + h-compli.anzahl * h-compli.epreis * rate. 
      tt-betrag = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
    END. 
  END. 
 
  curr-artnr = 0. 
  FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.p-artnr 
    BY c1-list.dept: 
    IF curr-artnr = 0 THEN curr-artnr = c1-list.p-artnr. 
    IF curr-artnr NE c1-list.p-artnr THEN 
    DO: 
      create c-list. 
      nr = nr + 1. 
      c-list.nr = nr. 
      c-list.bezeich = "T O T A L". 
      c-list.t-cost = t-cost. 
      c-list.betrag = t-betrag. 
      curr-artnr = c1-list.p-artnr. 
      t-cost = 0. 
      t-betrag = 0. 
    END. 
    t-cost = t-cost + c1-list.t-cost. 
    t-betrag = t-betrag + c1-list.betrag. 
    create c-list. 
    nr = nr + 1. 
    c-list.nr = nr. 
    c-list.datum = c1-list.datum. 
    c-list.dept = c1-list.dept. 
    c-list.deptname = c1-list.deptname. 
    c-list.rechnr = c1-list.rechnr. 
    c-list.p-artnr = c1-list.p-artnr. 
    c-list.bezeich = c1-list.bezeich. 
    c-list.betrag = c1-list.betrag. 
    c-list.t-cost = c1-list.t-cost. 
    c-list.name = c1-list.name. 
  END. 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich = "T O T A L". 
  c-list.t-cost = t-cost. 
  c-list.betrag = t-betrag. 
 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich = "GRAND TOTAL". 
  c-list.t-cost = tt-cost. 
  c-list.betrag = tt-betrag. 
END. 
 
PROCEDURE journal-list2: 
DEFINE VARIABLE amount AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amount AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-amount AS DECIMAL. 
DEFINE VARIABLE rechnr AS INTEGER. 
DEFINE VARIABLE dept AS INTEGER INITIAL -1. 
DEFINE VARIABLE p-artnr AS INTEGER. 
DEFINE VARIABLE depart AS CHAR. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE artnr AS INTEGER. 
DEFINE VARIABLE datum AS DATE INITIAL ?. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
 
DEFINE buffer h-art FOR h-artikel. 
DEFINE buffer fr-art FOR artikel. 
 
DEFINE VARIABLE cost AS DECIMAL. 
DEFINE VARIABLE t-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tt-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tt-betrag AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE curr-name AS CHAR. 
DEFINE VARIABLE nr AS INTEGER. 
 
  FOR EACH c-list: 
    delete c-list. 
  END. 
  FOR EACH c1-list: 
    delete c1-list. 
  END. 
  it-exist = NO. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.departement = hoteldpt.num 
      AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
        /* BY h-compli.p-artnr */ BY h-compli.rechnr: 
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr 
          = foreign-nr AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        ELSE FIND FIRST exrate WHERE exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
 
      FIND FIRST c1-list WHERE c1-list.datum = h-compli.datum 
        AND c1-list.dept = h-compli.departement 
        AND c1-list.rechnr = h-compli.rechnr 
        AND c1-list.p-artnr = h-compli.p-artnr NO-ERROR. 
 
      IF NOT AVAILABLE c1-list THEN 
      DO: 
        create c1-list. 
        c1-list.datum = h-compli.datum. 
        c1-list.dept = h-compli.departement. 
        c1-list.deptname = hoteldpt.depart. 
        c1-list.rechnr = h-compli.rechnr. 
        c1-list.p-artnr = h-compli.p-artnr. 
        FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr 
          AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN c1-list.name = h-bill.bilname. 
        c1-list.bezeich = h-art.bezeich. 
      END. 
 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
        AND h-artikel.departement = h-compli.departement NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-compli.departement NO-LOCK. 
 
      cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        cost = h-compli.anzahl * h-cost.betrag. 
        tt-cost = tt-cost + cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
      END. 
      IF (NOT AVAILABLE h-cost AND h-compli.datum LT billdate) 
        OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
      DO: 
        cost = h-compli.anzahl * h-compli.epreis 
          * h-artikel.prozent / 100 * rate. 
        tt-cost = tt-cost + cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
      END. 
 
/** Bill Amount  **/ 
      c1-list.betrag = c1-list.betrag 
        + h-compli.anzahl * h-compli.epreis * rate. 
      tt-betrag = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
    END. 
  END. 
 
  curr-name = "". 
  FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.name: 
    IF curr-name = "" THEN curr-name = c1-list.name. 
    IF curr-name NE c1-list.name THEN 
    DO: 
      create c-list. 
      nr = nr + 1. 
      c-list.nr = nr. 
      c-list.bezeich = "T O T A L". 
      c-list.t-cost = t-cost. 
      c-list.betrag = t-betrag. 
      curr-name = c1-list.name. 
      t-cost = 0. 
      t-betrag = 0. 
    END. 
    t-cost = t-cost + c1-list.t-cost. 
    t-betrag = t-betrag + c1-list.betrag. 
    create c-list. 
    nr = nr + 1. 
    c-list.nr = nr. 
    c-list.datum = c1-list.datum. 
    c-list.dept = c1-list.dept. 
    c-list.deptname = c1-list.deptname. 
    c-list.rechnr = c1-list.rechnr. 
    c-list.p-artnr = c1-list.p-artnr. 
    c-list.bezeich = c1-list.bezeich. 
    c-list.betrag = c1-list.betrag. 
    c-list.t-cost = c1-list.t-cost. 
    c-list.name = c1-list.name. 
  END. 
 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich = "T O T A L". 
  c-list.t-cost = t-cost. 
  c-list.betrag = t-betrag. 
 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich = "GRAND TOTAL". 
  c-list.t-cost = tt-cost. 
  c-list.betrag = tt-betrag. 
END. 

