DEFINE WORKFILE h-list 
  FIELD rechnr      AS INTEGER 
  FIELD departement AS INTEGER 
  FIELD datum       AS DATE 
  FIELD betrag      AS DECIMAL
  FIELD bezeich     AS CHAR. 
 
DEFINE TEMP-TABLE c-list 
  FIELD nr          AS INTEGER 
  FIELD datum       AS DATE LABEL "Date" 
  FIELD dept        AS INTEGER 
  FIELD deptname    AS CHAR FORMAT "x(16)" LABEL "Department" 
  FIELD rechnr      AS INTEGER FORMAT ">>>>>>>" LABEL " BillNo" 
  FIELD pax         AS INTEGER FORMAT ">>>" LABEL "Pax" 
/* 
  FIELD name AS CHAR FORMAT "x(20)" LABEL "GuestName" 
  FIELD p-artnr AS INTEGER FORMAT ">>>>>" LABEL "P-Art" 
*/ 
  FIELD bezeich     AS CHAR   FORMAT "x(20)" LABEL "Description" 
  FIELD f-betrag    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "  Food Amount" 
  FIELD f-cost      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "    Food-Cost" 
  FIELD b-betrag    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "Bevrge Amount" 
  FIELD b-cost      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "Beverage-Cost" 
  FIELD betrag      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "  Bill-Amount" 
  FIELD t-cost      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "Cost-of-Sales" 
  FIELD o-cost      AS DECIMAL FORMAT "->>,>>>,>>9.99"   LABEL " Other-Cost"
  FIELD usr-id      AS CHARACTER.
 
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER foreign-nr AS INT.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER from-dept AS INT.
DEF INPUT PARAMETER to-dept AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR c-list.

/*DEF VAR double-currency AS LOGICAL INIT NO.
DEF VAR foreign-nr AS INT INIT 0.
DEF VAR exchg-rate AS DECIMAL INIT 1.
DEF VAR billdate AS DATE INIT "01/14/19".
DEF VAR from-dept AS INT INIT 1.
DEF VAR to-dept AS INT INIT 20.
DEF VAR from-date AS DATE INIT "01/01/19".
DEF VAR to-date AS DATE INIT "01/20/19".*/

DEFINE VARIABLE it-exist AS LOGICAL INITIAL NO. 
RUN create-mplist. 
RUN journal-list. 
/*FOR EACH c-list:
    DISP c-list.
END.*/

PROCEDURE create-mplist: 
  FOR EACH h-list: 
    delete h-list. 
  END. 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    FOR EACH h-journal WHERE h-journal.bill-datum GE from-date 
      AND h-journal.bill-datum LE to-date 
      AND h-journal.departement = hoteldpt.num 
      NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr 
      AND h-artikel.departement = hoteldpt.num AND h-artikel.artart = 12 
      NO-LOCK BY h-journal.rechnr: 
      FIND FIRST h-list WHERE h-list.rechnr = h-journal.rechnr 
        AND h-list.departement = h-journal.departement 
        AND h-list.datum = h-journal.bill-datum AND h-list.bezeich = h-journal.bezeich NO-ERROR. 
      IF NOT AVAILABLE h-list THEN 
      DO: 
        create h-list. 
        h-list.rechnr = h-journal.rechnr. 
        h-list.departement = h-journal.departement. 
        h-list.datum = h-journal.bill-datum. 
        h-list.bezeich = h-journal.bezeich. /*bernatd*/
      END. 
      h-list.betrag = h-list.betrag + h-journal.betrag. 
    END. 
  END. 
  FOR EACH h-list WHERE h-list.betrag = 0: 
    delete h-list. 
  END. 
END. 


PROCEDURE journal-list: 
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
 
DEFINE VARIABLE f-cost AS DECIMAL. 
DEFINE VARIABLE b-cost AS DECIMAL. 
DEFINE VARIABLE o-cost AS DECIMAL. 
DEFINE VARIABLE cost AS DECIMAL. 
 
DEFINE VARIABLE t-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE t-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-betrag AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tt-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tto-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tt-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-betrag AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE b-endkum AS INTEGER. 
DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
 
  FOR EACH c-list: 
    delete c-list. 
  END. 
  it-exist = NO. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    t-cost = 0. 
    tf-cost = 0. 
    tb-cost = 0. 
    to-cost = 0. 
    t-betrag = 0. 
    FOR EACH h-list WHERE h-list.datum GE from-date AND h-list.datum LE to-date 
      AND h-list.departement = hoteldpt.num NO-LOCK BY h-list.rechnr: 
 
      IF double-currency AND curr-datum NE h-list.datum THEN 
      DO: 
        curr-datum = h-list.datum. 
        IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr 
          = foreign-nr AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        ELSE FIND FIRST exrate WHERE exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
      FIND FIRST h-bill WHERE h-bill.rechnr = h-list.rechnr 
        AND h-bill.departement = h-list.departement NO-LOCK NO-ERROR. 
      FIND FIRST c-list WHERE c-list.datum = h-list.datum 
        AND c-list.dept = h-list.departement 
        AND c-list.rechnr = h-list.rechnr NO-ERROR. 
      IF NOT AVAILABLE c-list THEN 
      DO: 
        create c-list. 
        nr = nr + 1. 
        c-list.nr = nr. 
        c-list.datum = h-list.datum. 
        c-list.dept = h-list.departement. 
        c-list.deptname = hoteldpt.depart. 
        c-list.rechnr = h-list.rechnr.
        c-list.bezeich = h-list.bezeich. /*bernatd*/ 
        IF AVAILABLE h-bill THEN 
        DO:
            FIND FIRST kellner WHERE kellner.kellner-nr = h-bill.kellner-nr NO-LOCK NO-ERROR.
            IF AVAILABLE kellner THEN
            DO:
                c-list.usr-id   = kellner.kellnername.
            END.
            ELSE
            DO:
                c-list.usr-id   = "".
            END.
            c-list.pax      = h-bill.belegung.
        END.
            
      END. 
 
      FOR EACH h-bill-line WHERE h-bill-line.rechnr = h-list.rechnr 
        AND h-bill-line.departement = h-list.departement 
        AND h-bill-line.bill-datum = h-list.datum NO-LOCK, 
        FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr 
        AND h-artikel.departement = h-list.departement 
        AND h-artikel.artart = 0 NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-artikel.departement NO-LOCK: 
 
        cost = 0. 
        f-cost = 0. 
        b-cost = 0. 
        o-cost = 0. 
 
        FIND FIRST h-cost WHERE h-cost.artnr = h-artikel.artnr 
          AND h-cost.departement = h-artikel.departement 
          AND h-cost.datum = h-list.datum 
          AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
        DO: 
          cost = h-bill-line.anzahl * h-cost.betrag. 
          t-cost = t-cost + cost. 
          tt-cost = tt-cost + cost. 
          IF artikel.endkum = f-endkum THEN 
          DO: 
            f-cost = cost. 
            tf-cost = tf-cost + f-cost. 
            ttf-cost = ttf-cost + f-cost. 
          END. 
          ELSE IF artikel.endkum = b-endkum THEN 
          DO: 
            b-cost = cost. 
            tb-cost = tb-cost + b-cost. 
            ttb-cost = ttb-cost + b-cost. 
          END. 
          c-list.f-cost = c-list.f-cost + f-cost. 
          c-list.b-cost = c-list.b-cost + b-cost. 
          c-list.o-cost = c-list.o-cost + o-cost. 
          c-list.t-cost = c-list.t-cost + cost. 
        END. 
        IF (NOT AVAILABLE h-cost AND h-list.datum LE billdate) 
          OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
        DO: 
          cost = h-bill-line.anzahl * h-bill-line.epreis 
            * h-artikel.prozent / 100 * rate. 
          t-cost = t-cost + cost. 
          tt-cost = tt-cost + cost. 
          IF artikel.endkum = f-endkum THEN 
          DO: 
            f-cost = cost. 
            tf-cost = tf-cost + cost. 
            ttf-cost = ttf-cost + cost. 
          END. 
          ELSE IF artikel.endkum = b-endkum THEN 
          DO: 
            b-cost = cost. 
            tb-cost = tb-cost + cost. 
            ttb-cost = ttb-cost + cost. 
          END. 
          c-list.f-cost = c-list.f-cost + f-cost. 
          c-list.b-cost = c-list.b-cost + b-cost. 
          c-list.o-cost = c-list.o-cost + o-cost. 
          c-list.t-cost = c-list.t-cost + cost. 
        END. 
 
/** Bill Betrag **/ 
        c-list.betrag = c-list.betrag 
          + h-bill-line.anzahl * h-bill-line.epreis * rate. 
        t-betrag = t-betrag + h-bill-line.anzahl 
          * h-bill-line.epreis * rate. 
        tt-betrag = tt-betrag + h-bill-line.anzahl * h-bill-line.epreis * rate. 
 
/** Food Betrag **/ 
        IF artikel.endkum = f-endkum THEN 
        DO: 
          c-list.f-betrag = c-list.f-betrag 
            + h-bill-line.anzahl * h-bill-line.epreis * rate. 
          tf-betrag = tf-betrag + h-bill-line.anzahl * h-bill-line.epreis * rate. 
          ttf-betrag = ttf-betrag + h-bill-line.anzahl 
            * h-bill-line.epreis * rate. 
        END. 
 
/** Beverage Betrag **/ 
        ELSE IF artikel.endkum = b-endkum THEN 
        DO: 
          c-list.b-betrag = c-list.b-betrag 
            + h-bill-line.anzahl * h-bill-line.epreis * rate. 
          tb-betrag = tb-betrag + h-bill-line.anzahl 
            * h-bill-line.epreis * rate. 
          ttb-betrag = ttb-betrag + h-bill-line.anzahl 
            * h-bill-line.epreis * rate. 
        END. 
      END. 
    END. 
    IF t-betrag NE 0 THEN 
    DO: 
      create c-list. 
      nr = nr + 1. 
      c-list.nr = nr. 
      c-list.bezeich = "T O T A L". 
      c-list.f-cost = tf-cost. 
      c-list.b-cost = tb-cost. 
      c-list.o-cost = to-cost. 
      c-list.t-cost = t-cost. 
      c-list.betrag = t-betrag. 
      c-list.f-betrag = tf-betrag. 
      c-list.b-betrag = tb-betrag. 
    END. 
  END. 
 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich = "GRAND TOTAL". 
  c-list.f-cost = ttf-cost. 
  c-list.b-cost = ttb-cost. 
  c-list.o-cost = tto-cost. 
  c-list.t-cost = tt-cost. 
  c-list.betrag = tt-betrag. 
  c-list.f-betrag = ttf-betrag. 
  c-list.b-betrag = ttb-betrag. 
 
  FOR EACH c-list: 
    IF c-list.betrag = 0 THEN delete c-list. 
  END. 
END. 

