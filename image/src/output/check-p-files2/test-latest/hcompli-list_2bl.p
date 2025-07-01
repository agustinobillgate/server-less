DEFINE TEMP-TABLE c-list 
  FIELD flag        AS INTEGER 
  FIELD nr          AS INTEGER 
  FIELD datum       AS DATE LABEL "Date" 
  FIELD dept        AS INTEGER 
  FIELD deptname    AS CHAR FORMAT "x(20)"                  LABEL "Department" 
  FIELD rechnr      AS INTEGER FORMAT ">>>>>>"              LABEL " BillNo" 
  FIELD name        AS CHAR FORMAT "x(15)"                  LABEL "GuestName" 
  FIELD artnr       AS INTEGER 
  FIELD p-artnr     AS INTEGER FORMAT ">>>>>"               LABEL "P-Art" 
  FIELD bezeich     AS CHAR   FORMAT "x(20)"                LABEL "Description"
  FIELD qty         AS INTEGER FORMAT "->>>>>>"                LABEL "Quantity"      /* Add By Gerald 21012020 for Robot n Co*/  /*william add - to format e76aa1*/
  FIELD betrag      AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "    Bill-Amount" 
  FIELD f-betrag    AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "    Food Amount" 
  FIELD f-cost      AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "      Food-Cost" 
  FIELD b-betrag    AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "Beverage Amount" 
  FIELD b-cost      AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "  Beverage-Cost" 
  FIELD o-betrag    AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "   Other Amount" /*FD Nov 03, 2022 => Ticket 856047*/ 
  FIELD o-cost      AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "     Other-Cost" /*FD Nov 03, 2022 => Ticket 856047*/ 
  FIELD t-cost      AS DECIMAL FORMAT "->>>,>>>,>>9.99"     LABEL "  Cost-of-Sales"
  FIELD creditlimit AS DECIMAL 
  FIELD officer     AS CHAR 
  FIELD detailed    AS LOGICAL INITIAL NO 
. 

DEFINE TEMP-TABLE c1-list LIKE c-list.
DEFINE BUFFER c2-list FOR c1-list. 

DEFINE INPUT PARAMETER pvILanguage          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER gname                AS CHAR.
DEFINE INPUT PARAMETER sorttype             AS INTEGER.
DEFINE INPUT PARAMETER from-dept            AS INTEGER.
DEFINE INPUT PARAMETER to-dept              AS INTEGER.
DEFINE INPUT PARAMETER from-date            AS DATE.
DEFINE INPUT PARAMETER to-date              AS DATE.
DEFINE INPUT PARAMETER double-currency      AS LOGICAL.
DEFINE INPUT PARAMETER exchg-rate           AS DECIMAL.
DEFINE INPUT PARAMETER billdate             AS DATE.
DEFINE INPUT PARAMETER mi-detail1           AS LOGICAL.
DEFINE INPUT PARAMETER sm-disp1             AS LOGICAL.
DEFINE INPUT PARAMETER foreign-nr           AS INTEGER.
DEFINE INPUT PARAMETER artnr                AS INTEGER.

DEFINE OUTPUT PARAMETER TABLE FOR c-list.

DEFINE VARIABLE it-exist            AS LOGICAL INITIAL NO. 
DEFINE VARIABLE curr-name           AS CHAR. 
DEFINE VARIABLE guestname           AS CHAR. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hcompli-list". 

RUN journal-list.

PROCEDURE journal-list: 
DEFINE VARIABLE amount          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amount        AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-amount      AS DECIMAL. 
DEFINE VARIABLE rechnr          AS INTEGER. 
DEFINE VARIABLE dept            AS INTEGER INITIAL -1. 
DEFINE VARIABLE p-artnr         AS INTEGER. 
DEFINE VARIABLE depart          AS CHAR. 
DEFINE VARIABLE bezeich         AS CHAR. 
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE artnr           AS INTEGER. 
DEFINE VARIABLE datum           AS DATE INITIAL ?. 
DEFINE VARIABLE curr-datum      AS DATE INITIAL ?. 
DEFINE VARIABLE rate            AS DECIMAL INITIAL 1.

DEFINE VARIABLE qty      AS INTEGER INITIAL 0.
DEFINE VARIABLE t-qty    AS INTEGER INITIAL 0.
DEFINE VARIABLE tt-qty   AS INTEGER INITIAL 0.

DEFINE VARIABLE f-cost  AS DECIMAL. 
DEFINE VARIABLE b-cost  AS DECIMAL. 
DEFINE VARIABLE o-cost  AS DECIMAL. 
DEFINE VARIABLE cost    AS DECIMAL. 
    
DEFINE VARIABLE t-cost  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE t-betrag    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-betrag   AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-betrag   AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-betrag   AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE tt-cost     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-cost    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-cost    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tto-cost    AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tt-betrag   AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tto-betrag  AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE f-endkum    AS INTEGER. 
DEFINE VARIABLE b-endkum    AS INTEGER.
DEFINE VARIABLE curr-name   AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE it-exist    AS LOGICAL INITIAL NO. 

DEFINE VARIABLE flag-artnr  AS CHARACTER NO-UNDO INITIAL "". /*Alder - Ticket 45BD01*/

DEFINE buffer s-list    FOR c-list.
DEFINE buffer h-art     FOR h-artikel. 

  IF gname NE "" THEN 
  DO: 
    RUN journal-gname. 
    RETURN. 
  END. 
 
  IF sorttype = 2 THEN 
  DO: 
    RUN journal-list1. 
    RETURN. 
  END. 
 
  IF sorttype = 3 THEN 
  DO: 
    RUN journal-list2. 
    RETURN. 
  END. 
 
  /*FOR EACH c-list: 
    delete c-list. 
  END. 

  it-exist = NO. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    ASSIGN
      t-cost    = 0 
      tf-cost   = 0 
      tb-cost   = 0 
      to-cost   = 0 
      t-betrag  = 0 
      tf-betrag = 0 
      tb-betrag = 0
    . 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.departement = hoteldpt.num 
      AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
        /* BY h-compli.p-artnr */ BY h-compli.rechnr: 
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        RUN find-exrate(curr-datum). 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
 
      FIND FIRST c-list WHERE c-list.datum = h-compli.datum 
        AND c-list.dept = h-compli.departement 
        AND c-list.rechnr = h-compli.rechnr 
        AND c-list.p-artnr = h-compli.p-artnr NO-ERROR. 
      IF NOT AVAILABLE c-list THEN 
      DO: 
        create c-list. 
        nr = nr + 1. 
        c-list.nr = nr. 
        c-list.datum = h-compli.datum. 
        c-list.dept = h-compli.departement. 
        c-list.deptname = hoteldpt.depart. 
        c-list.rechnr = h-compli.rechnr. 
        c-list.p-artnr = h-compli.p-artnr. 
        FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr 
          AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN c-list.name = h-bill.bilname. 
        ELSE 
        DO: 
          FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum 
            AND h-journal.departement = h-compli.departement 
            AND h-journal.segmentcode = h-compli.p-artnr 
            AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
          IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
            c-list.name = h-journal.aendertext. 
        END. 
        c-list.bezeich = h-art.bezeich. 
      END. 
 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
        AND h-artikel.departement = h-compli.departement NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-artikel.departement NO-LOCK. 
 
      cost = 0. 
      f-cost = 0. 
      b-cost = 0. 
      o-cost = 0. 
 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        cost = h-compli.anzahl * h-cost.betrag. 
        RUN cost-correction(INPUT-OUTPUT cost).
        t-cost = t-cost + cost. 
        tt-cost = tt-cost + cost. 
        IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 
            OR artikel.umsatzart = 5 THEN 
        DO: 
          f-cost = cost. 
          tf-cost = tf-cost + f-cost. 
          ttf-cost = ttf-cost + f-cost. 
        END. 
        ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
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
      IF (NOT AVAILABLE h-cost AND h-compli.datum LT billdate) 
        OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
      DO: 
        cost = h-compli.anzahl * h-compli.epreis 
          * h-artikel.prozent / 100 * rate. 
        t-cost = t-cost + cost. 
        tt-cost = tt-cost + cost. 
        IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 
            OR artikel.umsatzart = 5 THEN 
        DO: 
          f-cost = cost. 
          tf-cost = tf-cost + cost. 
          ttf-cost = ttf-cost + cost. 
        END. 
        ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
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
        + h-compli.anzahl * h-compli.epreis * rate. 
      t-betrag = t-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      tt-betrag = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
 
/** Food Betrag **/ 
      IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 
          OR artikel.umsatzart = 5 THEN 
      DO: 
        c-list.f-betrag = c-list.f-betrag 
          + h-compli.anzahl * h-compli.epreis * rate. 
        tf-betrag = tf-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ttf-betrag = ttf-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END. 
 
/** Beverage Betrag **/ 
      ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
      DO: 
        c-list.b-betrag = c-list.b-betrag 
          + h-compli.anzahl * h-compli.epreis * rate. 
        tb-betrag = tb-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ttb-betrag = ttb-betrag + h-compli.anzahl * h-compli.epreis * rate. 
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
END.*/

  /*Modified journal-list by Gerald 21012020 for Robot n Co*/
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
    ASSIGN
      t-cost    = 0 
      tf-cost   = 0 
      tb-cost   = 0 
      to-cost   = 0 
      t-betrag  = 0 
      tf-betrag = 0 
      tb-betrag = 0 
      to-betrag = 0
      t-qty     = 0
     . 

    FOR EACH h-compli WHERE h-compli.datum GE from-date AND 
                            h-compli.datum LE to-date AND 
                            h-compli.departement = hoteldpt.num AND 
                            h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement AND 
                        h-art.artnr = h-compli.p-artnr AND 
                        h-art.artart = 11 NO-LOCK BY h-compli.rechnr: 

      /* FDL Comment Ticket 88B0A2
      IF NOT INDEX(flag-artnr, STRING(h-compli.artnr)) > 0 THEN /*Alder - Ticket 45BD01*/
      */
      DO:
          flag-artnr = flag-artnr + "," + STRING(h-compli.artnr). /*Alder - Ticket 45BD01*/
          IF double-currency AND curr-datum NE h-compli.datum THEN 
          DO: 
            curr-datum = h-compli.datum. 
            RUN find-exrate(curr-datum). 
            IF AVAILABLE exrate THEN rate = exrate.betrag. 
            ELSE rate = exchg-rate. 
          END. 
     
          FIND FIRST c1-list WHERE c1-list.datum = h-compli.datum AND c1-list.dept = h-compli.departement 
            AND c1-list.rechnr = h-compli.rechnr AND c1-list.p-artnr = h-compli.p-artnr NO-ERROR.  
          IF NOT AVAILABLE c1-list THEN 
          DO: 
            create c1-list. 
            c1-list.datum       = h-compli.datum. 
            c1-list.dept        = h-compli.departement. 
            c1-list.deptname    = hoteldpt.depart. 
            c1-list.rechnr      = h-compli.rechnr. 
            c1-list.p-artnr     = h-compli.p-artnr. 
            FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
            IF AVAILABLE h-bill THEN c1-list.name = h-bill.bilname. 
            ELSE 
            DO: 
              FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum AND h-journal.departement = h-compli.departement 
                AND h-journal.segmentcode = h-compli.p-artnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
              IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
                c1-list.name = h-journal.aendertext. 
            END. 
            c1-list.bezeich = h-art.bezeich. 
          END. 
     
          FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr AND h-artikel.departement = h-compli.departement NO-LOCK. 
          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront AND artikel.departement = h-compli.departement NO-LOCK. 
     
          cost = 0. 
          f-cost = 0. 
          b-cost = 0. 
          o-cost = 0. 
          
          /*Validation*/
          
          FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          DO:
            cost = h-compli.anzahl * h-cost.betrag. 
            RUN cost-correction(INPUT-OUTPUT cost).
            cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
            tt-cost = tt-cost + cost. 
            IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
            DO: 
              f-cost = cost. 
              ttf-cost = ttf-cost + cost. 
            END. 
            ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
            DO: 
              b-cost = cost. 
              ttb-cost = ttb-cost + cost. 
            END. 
            ELSE 
            DO: 
              o-cost = cost. 
              tto-cost = tto-cost + cost. 
            END. 
            DO: 
              c1-list.f-cost = c1-list.f-cost + f-cost. 
              c1-list.b-cost = c1-list.b-cost + b-cost. 
              c1-list.o-cost = c1-list.o-cost + o-cost. 
              c1-list.t-cost = c1-list.t-cost + cost. 
            END. 
          END. 
          ELSE
          IF (NOT AVAILABLE h-cost AND h-compli.datum LT billdate) OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
          DO: 
            cost    = h-compli.anzahl * h-compli.epreis * h-artikel.prozent / 100 * rate. 
            cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
            tt-cost = tt-cost + cost. 
            IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
            DO: 
              f-cost    = cost. 
              ttf-cost  = ttf-cost + cost. 
            END. 
            ELSE IF artikel.umsatzart = 6 THEN 
            DO: 
              b-cost    = cost. 
              ttb-cost  = ttb-cost + cost. 
            END. 
            ELSE 
            DO: 
              o-cost    = cost. 
              tto-cost  = tto-cost + cost. 
            END. 
            DO: 
              c1-list.f-cost = c1-list.f-cost + f-cost. 
              c1-list.b-cost = c1-list.b-cost + b-cost. 
              c1-list.o-cost = c1-list.o-cost + o-cost. 
              c1-list.t-cost = c1-list.t-cost + cost. 
            END. 
          END.
               
    /** Bill Amount  **/ 
          c1-list.betrag    = c1-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
          tt-betrag         = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
               
    /** Food Betrag **/ 
          IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          DO: 
            c1-list.f-betrag    = c1-list.f-betrag + h-compli.anzahl * h-compli.epreis * rate. 
            ttf-betrag          = ttf-betrag + h-compli.anzahl * h-compli.epreis * rate. 
          END. 
     
    /** Beverage Betrag **/ 
          ELSE IF  artikel.umsatzart = 6 THEN 
          DO: 
            c1-list.b-betrag    = c1-list.b-betrag + h-compli.anzahl * h-compli.epreis * rate. 
            ttb-betrag          = ttb-betrag + h-compli.anzahl * h-compli.epreis * rate. 
          END. 
     
    /** Other Betrag **/
          ELSE
          DO:
              c1-list.o-betrag    = c1-list.o-betrag + h-compli.anzahl * h-compli.epreis * rate.
              tto-betrag          = tto-betrag + h-compli.anzahl * h-compli.epreis * rate.
          END.
    
          IF mi-detail1 THEN 
          DO: 
            FIND FIRST c2-list WHERE c2-list.datum = h-compli.datum AND c2-list.dept = h-compli.departement 
              AND c2-list.rechnr = h-compli.rechnr AND c2-list.artnr = h-compli.artnr NO-ERROR. 
            IF NOT AVAILABLE c2-list THEN 
            DO: 
              FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr AND h-artikel.departement = h-compli.departement NO-LOCK NO-ERROR. 
              
              CREATE c2-list. 
              ASSIGN 
                c2-list.detailed    = YES 
                c2-list.datum       = h-compli.datum 
                c2-list.dept        = h-compli.departement 
                c2-list.deptname    = hoteldpt.depart 
                c2-list.rechnr      = h-compli.rechnr 
                c2-list.artnr       = h-artikel.artnr 
                c2-list.bezeich     = h-artikel.bezeich 
                c2-list.name        = c1-list.NAME
                . 
            END.
            c2-list.qty    = c2-list.qty + h-compli.anzahl .    /* Add by Gerald 21012020 for Robot n Co */
            c2-list.f-cost = c2-list.f-cost + f-cost. 
            c2-list.b-cost = c2-list.b-cost + b-cost. 
            c2-list.o-cost = c2-list.o-cost + o-cost. 
            c2-list.t-cost = c2-list.t-cost + cost. 
            c2-list.betrag = c2-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
            IF  artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
                c2-list.f-betrag = c2-list.f-betrag + h-compli.anzahl * h-compli.epreis * rate. 
            ELSE IF  artikel.umsatzart = 6 THEN 
                c2-list.b-betrag = c2-list.b-betrag + h-compli.anzahl * h-compli.epreis * rate.
            ELSE
                c2-list.o-betrag = c2-list.o-betrag + h-compli.anzahl * h-compli.epreis * rate.
          END. 
      END.
    END. 
  END.
  
  IF mi-detail1 = FALSE THEN
  DO:
    curr-name = "???".
    b-cost    = 0. 
    o-cost    = 0. 
    FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.rechnr BY c1-list.name BY c1-list.datum BY c1-list.dept DESCENDING : 

      IF NOT c1-list.detailed THEN 
      DO: 
        t-cost      = t-cost + c1-list.t-cost. 
        tf-cost     = tf-cost + c1-list.f-cost. 
        tb-cost     = tb-cost + c1-list.b-cost. 
        to-cost     = to-cost + c1-list.o-cost. 
        t-betrag    = t-betrag + c1-list.betrag. 
        tf-betrag   = tf-betrag + c1-list.f-betrag. 
        tb-betrag   = tb-betrag + c1-list.b-betrag.
        to-betrag   = to-betrag + c1-list.o-betrag.
      END. 
    
      CREATE c-list. 
      nr                = nr + 1. 
      c-list.nr         = nr. 
      c-list.datum      = c1-list.datum. 
      c-list.dept       = c1-list.dept. 
      c-list.deptname   = c1-list.deptname. 
      c-list.rechnr     = c1-list.rechnr. 
      c-list.artnr      = c1-list.artnr. 
      c-list.p-artnr    = c1-list.p-artnr. 
      c-list.bezeich    = c1-list.bezeich.
      c-list.betrag     = c1-list.betrag. 
      c-list.f-betrag   = c1-list.f-betrag. 
      c-list.b-betrag   = c1-list.b-betrag. 
      c-list.o-betrag   = c1-list.o-betrag. 
      c-list.f-cost     = c1-list.f-cost. 
      c-list.b-cost     = c1-list.b-cost. 
      c-list.o-cost     = c1-list.o-cost. 
      c-list.t-cost     = c1-list.t-cost. 
      c-list.name       = c1-list.name.
    END. 
  END.

  IF mi-detail1 = TRUE THEN
  DO:
    curr-name = "???".
    b-cost    = 0. 
    o-cost    = 0. 
    
    FOR EACH c1-list WHERE c1-list.betrag NE 0  BY c1-list.rechnr BY c1-list.p-artnr BY c1-list.name BY c1-list.datum BY c1-list.dept  
      BY c1-list.artnr  DESCENDING: 
        
        IF curr-name = "???" THEN curr-name = c1-list.name. 
        IF curr-name NE c1-list.name THEN  
        DO: 
          create c-list. 
          nr              = nr + 1. 
          c-list.nr       = nr. 
          c-list.bezeich  = "T O T A L". 
          c-list.qty      = t-qty.
          c-list.f-cost   = tf-cost.
          c-list.b-cost   = tb-cost. 
          c-list.o-cost   = to-cost. 
          c-list.t-cost   = t-cost. 
          c-list.betrag   = t-betrag. 
          c-list.f-betrag = tf-betrag. 
          c-list.b-betrag = tb-betrag.
          c-list.o-betrag = to-betrag.
          tt-qty          = tt-qty + t-qty.
          t-qty           = 0.
        
        
          IF sm-disp1 THEN 
          DO: 
            FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name NO-LOCK NO-ERROR. 
            IF AVAILABLE queasy THEN 
            DO: 
              it-exist            = YES. 
              c-list.creditlimit  = queasy.deci3. 
              c-list.officer      = curr-name. 
            END.
          END. 
          
          curr-name   = c1-list.name. 
          t-cost      = 0. 
          tf-cost     = 0. 
          tb-cost     = 0. 
          to-cost     = 0. 
          t-betrag    = 0. 
          tf-betrag   = 0. 
          tb-betrag   = 0. 
          to-betrag   = 0.
        END.
        
        IF NOT c1-list.detailed THEN 
        DO:
            t-cost      = t-cost + c1-list.t-cost. 
            tf-cost     = tf-cost + c1-list.f-cost. 
            tb-cost     = tb-cost + c1-list.b-cost. 
            to-cost     = to-cost + c1-list.o-cost. 
            t-betrag    = t-betrag + c1-list.betrag. 
            tf-betrag   = tf-betrag + c1-list.f-betrag. 
            tb-betrag   = tb-betrag + c1-list.b-betrag.
            to-betrag   = to-betrag + c1-list.o-betrag.
        END.

        CREATE c-list. 
        nr                = nr + 1. 
        c-list.nr         = nr. 
        c-list.datum      = c1-list.datum. 
        c-list.dept       = c1-list.dept. 
        c-list.deptname   = c1-list.deptname. 
        c-list.rechnr     = c1-list.rechnr. 
        c-list.artnr      = c1-list.artnr. 
        c-list.p-artnr    = c1-list.p-artnr. 
        c-list.bezeich    = c1-list.bezeich.
        c-list.betrag     = c1-list.betrag. 
        c-list.f-betrag   = c1-list.f-betrag. 
        c-list.b-betrag   = c1-list.b-betrag. 
        c-list.o-betrag   = c1-list.o-betrag.
        c-list.f-cost     = c1-list.f-cost. 
        c-list.b-cost     = c1-list.b-cost. 
        c-list.o-cost     = c1-list.o-cost. 
        c-list.t-cost     = c1-list.t-cost. 
        c-list.name       = c1-list.name.
        
        /* Add By Gerald 21012020 for Robot n Co */
        IF p-artnr EQ 0 THEN
        DO:
            qty         = c1-list.qty.       
            c-list.qty  = c1-list.qty.      
            t-qty       = t-qty + qty.
        END.
    END.
  END.

  create c-list. 
  nr                = nr + 1. 
  c-list.nr         = nr. 
  c-list.bezeich    = "T O T A L".
  c-list.qty        = t-qty.
  c-list.f-cost     = tf-cost. 
  c-list.b-cost     = tb-cost. 
  c-list.o-cost     = to-cost. 
  c-list.t-cost     = t-cost. 
  c-list.betrag     = t-betrag. 
  c-list.f-betrag   = tf-betrag. 
  c-list.b-betrag   = tb-betrag.
  c-list.o-betrag   = to-betrag.
  tt-qty            = tt-qty + t-qty.
  t-qty             = 0.
 
  IF sm-disp1 THEN 
  DO: 
    FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 
      it-exist           = YES. 
      c-list.creditlimit = queasy.deci3. 
      c-list.officer     = curr-name. 
    END. 
  END.
 
  create c-list. 
  nr                = nr + 1. 
  c-list.nr         = nr. 
  c-list.bezeich    = "GRAND TOTAL". 
  c-list.qty        = tt-qty.       /* Add By Gerald for Robot n Co 21012020*/
  c-list.f-cost     = ttf-cost. 
  c-list.b-cost     = ttb-cost. 
  c-list.o-cost     = tto-cost. 
  c-list.t-cost     = tt-cost. 
  c-list.betrag     = tt-betrag. 
  c-list.f-betrag   = ttf-betrag. 
  c-list.b-betrag   = ttb-betrag.
  c-list.o-betrag   = tto-betrag.
  tt-qty            = 0.
 
  IF it-exist THEN 
  DO: 
    FOR EACH s-list WHERE s-list.creditlimit NE 0 AND s-list.creditlimit LT s-list.betrag AND s-list.flag = 0: 
      create c-list. 
      nr                 = nr + 1. 
      c-list.nr          = nr. 
      c-list.flag        = 1. 
      c-list.deptname    = translateExtended ("Over CreditLimit",lvCAREA,""). 
      c-list.name        = s-list.officer. 
      c-list.creditlimit = s-list.creditlimit. 
      c-list.bezeich     = STRING(s-list.creditlimit," ->>>,>>>,>>>,>>9.99"). 
      c-list.betrag      = s-list.betrag. 
      c-list.f-betrag    = s-list.betrag - s-list.creditlimit. 
    END.
  END.
END.
/*End Modified*/ 

/*PROCEDURE journal-list1: 
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
DEFINE VARIABLE curr-artnr AS INTEGER. 
DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
 
  FOR EACH c-list: 
    delete c-list. 
  END. 
  FOR EACH c1-list: 
    delete c1-list. 
  END. 
  it-exist = NO. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.departement = hoteldpt.num 
      AND h-compli.betriebsnr = 0 NO-LOCK BY h-compli.rechnr:
      FIND FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK.
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        RUN find-exrate(curr-datum). 
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
        ELSE 
        DO: 
          FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum 
            AND h-journal.departement = h-compli.departement 
            AND h-journal.segmentcode = h-compli.p-artnr 
            AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
          IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
            c1-list.name = h-journal.aendertext. 
        END. 
        c1-list.bezeich = h-art.bezeich. 
      END. 
 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
        AND h-artikel.departement = h-compli.departement NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-compli.departement NO-LOCK. 
 
      cost = 0. 
      f-cost = 0. 
      b-cost = 0. 
      o-cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        cost = h-compli.anzahl * h-cost.betrag. 
        RUN cost-correction(INPUT-OUTPUT cost).
        tt-cost = tt-cost + cost. 
        IF artikel.umsatzart = 3 OR 
            artikel.umsatzart = 5 THEN 
        DO: 
          f-cost = cost. 
          ttf-cost = ttf-cost + cost. 
        END. 
        ELSE IF artikel.umsatzart = 6 THEN 
        DO: 
          b-cost = cost. 
          ttb-cost = ttb-cost + cost. 
        END. 
        ELSE 
        DO: 
          o-cost = cost. 
          tto-cost = tto-cost + cost. 
        END. 

        c1-list.f-cost = c1-list.f-cost + f-cost. 
        c1-list.b-cost = c1-list.b-cost + b-cost. 
        c1-list.o-cost = c1-list.o-cost + o-cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
      END.

      ELSE
      IF NOT AVAILABLE h-cost 
        OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
      DO: 
        cost = h-compli.anzahl * h-compli.epreis 
          * h-artikel.prozent / 100 * rate. 
        tt-cost = tt-cost + cost. 
        IF artikel.umsatzart = 3 OR 
            artikel.umsatzart = 5 THEN 
        DO: 
          f-cost = cost. 
          ttf-cost = ttf-cost + cost. 
        END. 
        ELSE IF artikel.umsatzart = 6 THEN 
        DO: 
          b-cost = cost. 
          ttb-cost = ttb-cost + cost. 
        END. 
        ELSE 
        DO: 
          o-cost = cost. 
          tto-cost = tto-cost + cost. 
        END. 

        c1-list.f-cost = c1-list.f-cost + f-cost. 
        c1-list.b-cost = c1-list.b-cost + b-cost. 
        c1-list.o-cost = c1-list.o-cost + o-cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
      END. 
 
/** Bill Amount  **/ 
      c1-list.betrag = c1-list.betrag 
        + h-compli.anzahl * h-compli.epreis * rate. 
      tt-betrag = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
 
/** Food Betrag **/ 
      IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR 
          artikel.umsatzart = 5 THEN 
      DO: 
        c1-list.f-betrag = c1-list.f-betrag 
          + h-compli.anzahl * h-compli.epreis * rate. 
        ttf-betrag = ttf-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END. 
 
/** Beverage Betrag **/ 
      ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
      DO: 
        c1-list.b-betrag = c1-list.b-betrag 
          + h-compli.anzahl * h-compli.epreis * rate. 
        ttb-betrag = ttb-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END.
    END. 
  END. 
 
  curr-artnr = 0. 
  f-cost = 0. 
  b-cost = 0. 
  o-cost = 0. 
  FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.p-artnr 
    BY c1-list.dept BY c1-list.datum: 
    IF curr-artnr = 0 THEN curr-artnr = c1-list.p-artnr. 
    IF curr-artnr NE c1-list.p-artnr THEN 
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
      curr-artnr = c1-list.p-artnr. 
      t-cost = 0. 
      tf-cost = 0. 
      tb-cost = 0. 
      to-cost = 0. 
      t-betrag = 0. 
      tf-betrag= 0. 
      tb-betrag = 0. 
    END. 
    t-cost = t-cost + c1-list.t-cost. 
    tf-cost = tf-cost + c1-list.f-cost. 
    tb-cost = tb-cost + c1-list.b-cost. 
    to-cost = to-cost + c1-list.o-cost. 
    t-betrag = t-betrag + c1-list.betrag. 
    tf-betrag = tf-betrag + c1-list.f-betrag. 
    tb-betrag = tb-betrag + c1-list.b-betrag. 
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
    c-list.f-betrag = c1-list.f-betrag. 
    c-list.b-betrag = c1-list.b-betrag. 
    c-list.f-cost = c1-list.f-cost. 
    c-list.b-cost = c1-list.b-cost. 
    c-list.o-cost = c1-list.o-cost. 
    c-list.t-cost = c1-list.t-cost. 
    c-list.name = c1-list.name. 
  END. 
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
END. */
 
/*Modified journal-list1 by Gerald 21012020 for Robot n Co*/
PROCEDURE journal-list1: 
DEFINE VARIABLE amount          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amount        AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-amount      AS DECIMAL. 
DEFINE VARIABLE rechnr          AS INTEGER. 
DEFINE VARIABLE dept            AS INTEGER INITIAL -1. 
DEFINE VARIABLE p-artnr         AS INTEGER. 
DEFINE VARIABLE depart          AS CHAR. 
DEFINE VARIABLE bezeich         AS CHAR. 
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE artnr           AS INTEGER. 
DEFINE VARIABLE datum           AS DATE INITIAL ?. 
DEFINE VARIABLE curr-datum      AS DATE INITIAL ?. 
DEFINE VARIABLE rate            AS DECIMAL INITIAL 1. 

DEFINE VARIABLE qty      AS INTEGER INITIAL 0.
DEFINE VARIABLE t-qty    AS INTEGER INITIAL 0.
DEFINE VARIABLE tt-qty   AS INTEGER INITIAL 0.
 
DEFINE VARIABLE f-cost  AS DECIMAL. 
DEFINE VARIABLE b-cost  AS DECIMAL. 
DEFINE VARIABLE o-cost  AS DECIMAL. 
DEFINE VARIABLE cost    AS DECIMAL. 
 
DEFINE VARIABLE t-cost  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE t-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-betrag AS DECIMAL INITIAL 0.
DEFINE VARIABLE to-betrag AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE tt-cost  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tto-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tt-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-betrag AS DECIMAL INITIAL 0.
DEFINE VARIABLE tto-betrag AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE f-endkum    AS INTEGER. 
DEFINE VARIABLE b-endkum    AS INTEGER. 
DEFINE VARIABLE curr-artnr  AS INTEGER. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 

DEFINE buffer s-list    FOR c-list.  
DEFINE buffer h-art     FOR h-artikel. 
DEFINE buffer fr-art    FOR artikel. 

  FOR EACH c-list: 
    delete c-list. 
  END. 
  FOR EACH c1-list: 
    delete c1-list. 
  END. 
  it-exist = NO. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    FOR EACH h-compli WHERE h-compli.datum GE from-date AND h-compli.datum LE to-date 
        AND h-compli.departement = hoteldpt.num AND h-compli.betriebsnr = 0 NO-LOCK BY h-compli.rechnr:
      FIND FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK.
							
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        RUN find-exrate(curr-datum). 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
 
      FIND FIRST c1-list WHERE c1-list.datum = h-compli.datum AND c1-list.dept = h-compli.departement 
        AND c1-list.rechnr = h-compli.rechnr AND c1-list.p-artnr = h-compli.p-artnr NO-ERROR. 
      IF NOT AVAILABLE c1-list THEN 
      DO: 
        create c1-list. 
        c1-list.datum       = h-compli.datum. 
        c1-list.dept        = h-compli.departement. 
        c1-list.deptname    = hoteldpt.depart. 
        c1-list.rechnr      = h-compli.rechnr. 
        c1-list.p-artnr     = h-compli.p-artnr. 
        FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN c1-list.name = h-bill.bilname. 
        ELSE 
        DO: 
          FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum AND h-journal.departement = h-compli.departement 
            AND h-journal.segmentcode = h-compli.p-artnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
          IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
            c1-list.name = h-journal.aendertext. 
        END. 
        c1-list.bezeich = h-art.bezeich. 
      END. 
 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr AND h-artikel.departement = h-compli.departement NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront AND artikel.departement = h-compli.departement NO-LOCK. 
      cost = 0. 
      f-cost = 0. 
      b-cost = 0. 
      o-cost = 0. 

      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        cost = h-compli.anzahl * h-cost.betrag. 
        RUN cost-correction(INPUT-OUTPUT cost).
        cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
        tt-cost = tt-cost + cost. 
        IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
        DO: 
          f-cost   = cost. 
          ttf-cost = ttf-cost + cost. 
        END. 
        ELSE IF artikel.umsatzart = 6 THEN 
        DO: 
          b-cost   = cost. 
          ttb-cost = ttb-cost + cost. 
        END. 
        ELSE 
        DO: 
          o-cost   = cost. 
          tto-cost = tto-cost + cost. 
        END. 

        c1-list.f-cost = c1-list.f-cost + f-cost. 
        c1-list.b-cost = c1-list.b-cost + b-cost. 
        c1-list.o-cost = c1-list.o-cost + o-cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
			 
      END.

      ELSE
      IF NOT AVAILABLE h-cost 
        OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
      DO: 
        cost    = h-compli.anzahl * h-compli.epreis * h-artikel.prozent / 100 * rate. 
        cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
        tt-cost = tt-cost + cost. 
        IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
        DO: 
          f-cost   = cost. 
          ttf-cost = ttf-cost + cost. 
        END. 
        ELSE IF artikel.umsatzart = 6 THEN 
        DO: 
          b-cost   = cost. 
          ttb-cost = ttb-cost + cost. 
        END. 
        ELSE 
        DO: 
          o-cost = cost. 
          tto-cost = tto-cost + cost. 
        END. 

        c1-list.f-cost = c1-list.f-cost + f-cost. 
        c1-list.b-cost = c1-list.b-cost + b-cost. 
        c1-list.o-cost = c1-list.o-cost + o-cost. 
        c1-list.t-cost = c1-list.t-cost + cost. 
			 
      END. 
 
/** Bill Amount  **/ 
      c1-list.betrag = c1-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
      tt-betrag      = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
 
/** Food Betrag **/ 
      IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
      DO: 
        c1-list.f-betrag = c1-list.f-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ttf-betrag       = ttf-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END. 
 
/** Beverage Betrag **/ 
      ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
      DO: 
        c1-list.b-betrag = c1-list.b-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ttb-betrag       = ttb-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END.

/** Other Betrag **/
      ELSE
      DO:
          c1-list.o-betrag    = c1-list.o-betrag + h-compli.anzahl * h-compli.epreis * rate.
          tto-betrag          = tto-betrag + h-compli.anzahl * h-compli.epreis * rate.
      END.
      /* Add By Geral 21012020 */
      
      IF mi-detail1 THEN 
      DO: 
        FIND FIRST c2-list WHERE c2-list.datum = h-compli.datum AND c2-list.dept = h-compli.departement 
          AND c2-list.rechnr = h-compli.rechnr AND c2-list.artnr = h-compli.artnr NO-ERROR. 
        IF NOT AVAILABLE c2-list THEN 
        DO: 
          FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr AND h-artikel.departement = h-compli.departement NO-LOCK. 
 
          CREATE c2-list. 
          ASSIGN 
            c2-list.detailed    = YES 
            c2-list.datum       = h-compli.datum 
            c2-list.dept        = h-compli.departement 
            c2-list.deptname    = hoteldpt.depart 
            c2-list.rechnr      = h-compli.rechnr 
            c2-list.artnr       = h-artikel.artnr 
            c2-list.bezeich     = h-artikel.bezeich 
            c2-list.name        = c1-list.NAME
          . 
        END. 
        c2-list.qty    = c2-list.qty + h-compli.anzahl.   /* Add by Gerald 21012020 for Robot n Co */
        c2-list.f-cost = c2-list.f-cost + f-cost. 
        c2-list.b-cost = c2-list.b-cost + b-cost. 
        c2-list.o-cost = c2-list.o-cost + o-cost. 
        c2-list.t-cost = c2-list.t-cost + cost. 
 
        c2-list.betrag = c2-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
        IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
            c2-list.f-betrag = c2-list.f-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
            c2-list.b-betrag = c2-list.b-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ELSE
            c2-list.o-betrag = c2-list.o-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END. 
      /* End */ 
    END. 
  END. 
  
  IF mi-detail1 = FALSE THEN
  DO:
    curr-artnr = 0. 
    f-cost     = 0. 
    b-cost     = 0. 
    o-cost     = 0. 
    FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.p-artnr BY c1-list.dept BY c1-list.datum
         BY c1-list.dept BY c1-list.rechnr BY c1-list.artnr DESCENDING: 
                                 
      IF curr-artnr = 0 THEN curr-artnr = c1-list.p-artnr. 
      IF curr-artnr NE c1-list.p-artnr THEN 
      DO: 
        create c-list. 
        nr                = nr + 1. 
        c-list.nr         = nr. 
        c-list.bezeich    = "T O T A L". 
        c-list.f-cost     = tf-cost. 
        c-list.b-cost     = tb-cost. 
        c-list.o-cost     = to-cost. 
        c-list.t-cost     = t-cost. 
        c-list.betrag     = t-betrag. 
        c-list.f-betrag   = tf-betrag. 
        c-list.b-betrag   = tb-betrag. 
        c-list.o-betrag   = to-betrag.
         
        IF sm-disp1 THEN 
        DO: 
          FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name NO-LOCK NO-ERROR. 
          IF AVAILABLE queasy THEN 
          DO: 
            it-exist              = YES. 
            c-list.creditlimit    = queasy.deci3. 
            c-list.officer        = curr-name. 
          END. 
        END. 				   
      
        curr-artnr    = c1-list.p-artnr.							
        t-cost        = 0. 
        tf-cost       = 0. 
        tb-cost       = 0. 
        to-cost       = 0. 
        t-betrag      = 0. 
        tf-betrag     = 0. 
        tb-betrag     = 0. 
        to-betrag     = 0.
      END.
    
      IF NOT c1-list.detailed THEN 
      DO: 								 
        t-cost    = t-cost + c1-list.t-cost. 
        tf-cost   = tf-cost + c1-list.f-cost. 
        tb-cost   = tb-cost + c1-list.b-cost. 
        to-cost   = to-cost + c1-list.o-cost. 
        t-betrag  = t-betrag + c1-list.betrag. 
        tf-betrag = tf-betrag + c1-list.f-betrag. 
        tb-betrag = tb-betrag + c1-list.b-betrag. 
        to-betrag = to-betrag + c1-list.o-betrag. 
      end.
    
      create c-list. 
      nr                  = nr + 1. 
      c-list.nr           = nr. 
      c-list.datum        = c1-list.datum. 
      c-list.dept         = c1-list.dept. 
      c-list.deptname     = c1-list.deptname. 
      c-list.rechnr       = c1-list.rechnr.  
      c-list.p-artnr      = c1-list.p-artnr. 
      c-list.bezeich      = c1-list.bezeich.
      /*c-list.qty          = c1-list.qty. */           /* Add by Gerald 21012020 for Robot n Co */
      c-list.betrag       = c1-list.betrag. 
      c-list.f-betrag     = c1-list.f-betrag. 
      c-list.b-betrag     = c1-list.b-betrag. 
      c-list.o-betrag     = c1-list.o-betrag.
      c-list.f-cost       = c1-list.f-cost. 
      c-list.b-cost       = c1-list.b-cost. 
      c-list.o-cost       = c1-list.o-cost. 
      c-list.t-cost       = c1-list.t-cost. 
      c-list.name         = c1-list.name. 
    END.
  END.

  IF mi-detail1 = TRUE THEN
  DO:
  curr-artnr = 0. 
  f-cost = 0. 
  b-cost = 0. 
  o-cost = 0. 
  FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.rechnr BY c1-list.p-artnr 
    BY c1-list.dept BY c1-list.datum BY c1-list.dept  BY c1-list.artnr DESCENDING: 
                               
    IF curr-artnr = 0 THEN curr-artnr = c1-list.p-artnr. 
    IF curr-artnr NE c1-list.p-artnr THEN  
    DO: 
      create c-list. 
      nr                = nr + 1. 
      c-list.nr         = nr. 
      c-list.bezeich    = "T O T A L". 
      c-list.qty        = t-qty.
      c-list.f-cost     = tf-cost. 
      c-list.b-cost     = tb-cost. 
      c-list.o-cost     = to-cost. 
      c-list.t-cost     = t-cost. 
      c-list.betrag     = t-betrag. 
      c-list.f-betrag   = tf-betrag. 
      c-list.b-betrag   = tb-betrag. 
      c-list.o-betrag   = to-betrag.
      tt-qty          = tt-qty + t-qty.
      t-qty           = 0.

      IF sm-disp1 THEN 
      DO: 
        FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN 
        DO: 
          it-exist           = YES. 
          c-list.creditlimit = queasy.deci3. 
          c-list.officer     = curr-name. 
        END. 
      END. 
 
      curr-name = c1-list.name. 
      t-cost    = 0. 
      tf-cost   = 0. 
      tb-cost   = 0. 
      to-cost   = 0. 
      t-betrag  = 0. 
      tf-betrag = 0. 
      tb-betrag = 0. 
      to-betrag = 0. 
    END. 
    IF NOT c1-list.detailed THEN 
    DO: 
      t-cost    = t-cost + c1-list.t-cost. 
      tf-cost   = tf-cost + c1-list.f-cost. 
      tb-cost   = tb-cost + c1-list.b-cost. 
      to-cost   = to-cost + c1-list.o-cost. 
      t-betrag  = t-betrag + c1-list.betrag. 
      tf-betrag = tf-betrag + c1-list.f-betrag. 
      tb-betrag = tb-betrag + c1-list.b-betrag. 
      to-betrag = to-betrag + c1-list.o-betrag. 
    END. 
 
    CREATE c-list. 
    nr                  = nr + 1. 
    c-list.nr           = nr. 
    c-list.datum        = c1-list.datum. 
    c-list.dept         = c1-list.dept. 
    c-list.deptname     = c1-list.deptname. 
    c-list.rechnr       = c1-list.rechnr. 
    c-list.artnr        = c1-list.artnr. 
    c-list.p-artnr      = c1-list.p-artnr. 
    c-list.bezeich      = c1-list.bezeich.
    c-list.betrag       = c1-list.betrag. 
    c-list.f-betrag     = c1-list.f-betrag. 
    c-list.b-betrag     = c1-list.b-betrag. 
    c-list.o-betrag     = c1-list.o-betrag.
    c-list.f-cost       = c1-list.f-cost. 
    c-list.b-cost       = c1-list.b-cost. 
    c-list.o-cost       = c1-list.o-cost. 
    c-list.t-cost       = c1-list.t-cost. 
    c-list.name         = c1-list.name. 

    /* Add By Gerald 21012020 for Robot n Co */
    IF p-artnr EQ 0 THEN
    DO:
        qty          = c1-list.qty.
        c-list.qty   = c1-list.qty.      
        t-qty        = t-qty + qty.
    END.
  END.
  END.

  create c-list. 
  nr                = nr + 1. 
  c-list.nr         = nr. 
  c-list.bezeich    = "T O T A L". 
  c-list.qty        = t-qty.        /* Add By Gerald 21012020 for Robot n Co */
  c-list.f-cost     = tf-cost. 
  c-list.b-cost     = tb-cost. 
  c-list.o-cost     = to-cost. 
  c-list.t-cost     = t-cost. 
  c-list.betrag     = t-betrag. 
  c-list.f-betrag   = tf-betrag. 
  c-list.b-betrag   = tb-betrag. 
  c-list.o-betrag   = to-betrag.
  tt-qty            = tt-qty + t-qty.  /* Add By Gerald 21012020 for Robot n Co */
  t-qty             = 0.                /* Add By Gerald 21012020 for Robot n Co */
 
  IF sm-disp1 THEN 
  DO: 
    FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 
      it-exist              = YES. 
      c-list.creditlimit    = queasy.deci3. 
      c-list.officer        = curr-name. 
    END. 
  END. 
 
  create c-list. 
  nr                = nr + 1. 
  c-list.nr         = nr. 
  c-list.bezeich    = "GRAND TOTAL". 
  c-list.qty        = tt-qty.           /* Add By Gerald 21012020 for Robot n Co */
  c-list.f-cost     = ttf-cost. 
  c-list.b-cost     = ttb-cost. 
  c-list.o-cost     = tto-cost. 
  c-list.t-cost     = tt-cost. 
  c-list.betrag     = tt-betrag. 
  c-list.f-betrag   = ttf-betrag. 
  c-list.b-betrag   = ttb-betrag.
  c-list.o-betrag   = tto-betrag.
 
  IF it-exist THEN 
  DO: 
    FOR EACH s-list WHERE s-list.creditlimit NE 0 AND s-list.creditlimit LT s-list.betrag AND s-list.flag = 0: 
      create c-list. 
      nr                 = nr + 1. 
      c-list.nr          = nr. 
      c-list.flag        = 1. 
      c-list.deptname    = translateExtended ("Over CreditLimit",lvCAREA,""). 
      c-list.name        = s-list.officer. 
      c-list.creditlimit = s-list.creditlimit. 
      c-list.bezeich     = STRING(s-list.creditlimit," ->>>,>>>,>>>,>>9.99"). 
      c-list.betrag      = s-list.betrag. 
      c-list.f-betrag    = s-list.betrag - s-list.creditlimit. 
    END. 
  END.  
END.
/*end modify*/

PROCEDURE journal-list2: 
DEFINE VARIABLE amount      AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amount    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-amount  AS DECIMAL. 
DEFINE VARIABLE rechnr      AS INTEGER. 
DEFINE VARIABLE dept        AS INTEGER INITIAL -1. 
DEFINE VARIABLE p-artnr     AS INTEGER. 
DEFINE VARIABLE depart      AS CHAR. 
DEFINE VARIABLE bezeich     AS CHAR. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE artnr       AS INTEGER. 
DEFINE VARIABLE datum       AS DATE INITIAL ?. 
DEFINE VARIABLE curr-datum  AS DATE INITIAL ?. 
DEFINE VARIABLE rate        AS DECIMAL INITIAL 1. 

DEFINE VARIABLE qty      AS INTEGER INITIAL 0.
DEFINE VARIABLE t-qty    AS INTEGER INITIAL 0.
DEFINE VARIABLE tt-qty   AS INTEGER INITIAL 0.
 
DEFINE VARIABLE f-cost AS DECIMAL. 
DEFINE VARIABLE b-cost AS DECIMAL. 
DEFINE VARIABLE o-cost AS DECIMAL. 
DEFINE VARIABLE cost   AS DECIMAL. 
 
DEFINE VARIABLE t-cost  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE t-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-betrag AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE tt-cost  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tto-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tt-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-betrag AS DECIMAL INITIAL 0.
DEFINE VARIABLE tto-betrag AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE f-endkum  AS INTEGER. 
DEFINE VARIABLE b-endkum  AS INTEGER. 
DEFINE VARIABLE curr-name AS CHAR. 
DEFINE VARIABLE nr       AS INTEGER INITIAL 0. 
DEFINE VARIABLE it-exist AS LOGICAL INITIAL NO.

DEFINE buffer s-list FOR c-list. 
DEFINE buffer h-art  FOR h-artikel. 
DEFINE buffer fr-art FOR artikel. 
 
  FOR EACH c-list: 
    delete c-list. 
  END. 
  FOR EACH c1-list: 
    delete c1-list. 
  END. 
  it-exist = NO. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num:

    FOR EACH h-compli WHERE h-compli.datum GE from-date AND h-compli.datum LE to-date 
        AND h-compli.departement = hoteldpt.num AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK BY h-compli.rechnr: 
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        RUN find-exrate(curr-datum). 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
 
      FIND FIRST c1-list WHERE c1-list.datum = h-compli.datum AND c1-list.dept = h-compli.departement 
        AND c1-list.rechnr = h-compli.rechnr AND c1-list.p-artnr = h-compli.p-artnr NO-ERROR. 
      IF NOT AVAILABLE c1-list THEN 
      DO: 
        create c1-list. 
        c1-list.datum    = h-compli.datum. 
        c1-list.dept     = h-compli.departement. 
        c1-list.deptname = hoteldpt.depart. 
        c1-list.rechnr   = h-compli.rechnr. 
        c1-list.p-artnr  = h-compli.p-artnr. 
        FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN c1-list.name = h-bill.bilname. 
        ELSE 
        DO: 
          FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum AND h-journal.departement = h-compli.departement 
            AND h-journal.segmentcode = h-compli.p-artnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
          IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
            c1-list.name = h-journal.aendertext. 
        END. 
        c1-list.bezeich = h-art.bezeich. 
      END. 
 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr AND h-artikel.departement = h-compli.departement NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront AND artikel.departement = h-compli.departement NO-LOCK. 
 
      cost   = 0. 
      f-cost = 0. 
      b-cost = 0. 
      o-cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        cost = h-compli.anzahl * h-cost.betrag. 
        RUN cost-correction(INPUT-OUTPUT cost).
        cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
        tt-cost = tt-cost + cost. 
        IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
        DO: 
          f-cost  = cost. 
          ttf-cost = ttf-cost + cost. 
        END. 
        ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
        DO: 
          b-cost  = cost. 
          ttb-cost = ttb-cost + cost. 
        END. 
        ELSE 
        DO: 
          o-cost   = cost. 
          tto-cost = tto-cost + cost. 
        END. 
        DO: 
          c1-list.f-cost = c1-list.f-cost + f-cost. 
          c1-list.b-cost = c1-list.b-cost + b-cost. 
          c1-list.o-cost = c1-list.o-cost + o-cost. 
          c1-list.t-cost = c1-list.t-cost + cost. 
        END. 
      END. 
      ELSE
      IF (NOT AVAILABLE h-cost AND h-compli.datum LT billdate) OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
      DO: 
        cost    = h-compli.anzahl * h-compli.epreis * h-artikel.prozent / 100 * rate. 
        cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
        tt-cost = tt-cost + cost. 
        IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
        DO: 
          f-cost   = cost. 
          ttf-cost = ttf-cost + cost. 
        END. 
        ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
        DO: 
          b-cost   = cost. 
          ttb-cost = ttb-cost + cost. 
        END. 
        ELSE 
        DO: 
          o-cost   = cost. 
          tto-cost = tto-cost + cost. 
        END. 
        DO: 
          c1-list.f-cost = c1-list.f-cost + f-cost. 
          c1-list.b-cost = c1-list.b-cost + b-cost. 
          c1-list.o-cost = c1-list.o-cost + o-cost. 
          c1-list.t-cost = c1-list.t-cost + cost. 
        END. 
      END. 
 
/** Bill Amount  **/ 
      c1-list.betrag = c1-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
      tt-betrag      = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
 
/** Food Betrag **/ 
      IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
      DO: 
        c1-list.f-betrag = c1-list.f-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ttf-betrag       = ttf-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END. 
 
/** Beverage Betrag **/ 
      ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
      DO: 
        c1-list.b-betrag = c1-list.b-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ttb-betrag       = ttb-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END. 

/** Other Betrag **/
      ELSE
      DO:
          c1-list.o-betrag    = c1-list.o-betrag + h-compli.anzahl * h-compli.epreis * rate.
          tto-betrag          = tto-betrag + h-compli.anzahl * h-compli.epreis * rate.
      END.

      IF mi-detail1 THEN 
      DO: 
        FIND FIRST c2-list WHERE c2-list.datum = h-compli.datum AND c2-list.dept = h-compli.departement 
          AND c2-list.rechnr = h-compli.rechnr AND c2-list.artnr = h-compli.artnr NO-ERROR. 
        IF NOT AVAILABLE c2-list THEN 
        DO: 
          FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr AND h-artikel.departement = h-compli.departement NO-LOCK. 
          CREATE c2-list. 
          ASSIGN 
            c2-list.detailed    = YES 
            c2-list.datum       = h-compli.datum 
            c2-list.dept        = h-compli.departement 
            c2-list.deptname    = hoteldpt.depart 
            c2-list.rechnr      = h-compli.rechnr 
            c2-list.artnr       = h-artikel.artnr 
            c2-list.bezeich     = h-artikel.bezeich 
            c2-list.name        = c1-list.NAME
          . 
        END. 
        c2-list.qty    = c2-list.qty + h-compli.anzahl.     /* Add by Gerald 21012020 for Robot n Co */
        c2-list.f-cost = c2-list.f-cost + f-cost. 
        c2-list.b-cost = c2-list.b-cost + b-cost. 
        c2-list.o-cost = c2-list.o-cost + o-cost. 
        c2-list.t-cost = c2-list.t-cost + cost. 
 
        c2-list.betrag = c2-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
        IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
            c2-list.f-betrag = c2-list.f-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN c2-list.b-betrag = c2-list.b-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        ELSE c2-list.o-betrag = c2-list.o-betrag + h-compli.anzahl * h-compli.epreis * rate. 
      END. 
    END.
  END. 
 
  curr-name = "???". 
  f-cost = 0. 
  b-cost = 0. 
  o-cost = 0. 
  FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.name 
    BY c1-list.datum BY c1-list.dept BY c1-list.rechnr 
    BY c1-list.artnr descending: 
    IF curr-name = "???" THEN curr-name = c1-list.name. 
    IF curr-name NE c1-list.name THEN 
    DO: 
      create c-list. 
      nr = nr + 1. 
      c-list.nr         = nr. 
      c-list.bezeich    = "T O T A L". 
      c-list.qty        = t-qty.   /* Add By Gerald 21022020 for Robot n Co */
      c-list.f-cost     = tf-cost. 
      c-list.b-cost     = tb-cost. 
      c-list.o-cost     = to-cost. 
      c-list.t-cost     = t-cost. 
      c-list.betrag     = t-betrag. 
      c-list.f-betrag   = tf-betrag. 
      c-list.b-betrag   = tb-betrag.
      c-list.o-betrag   = to-betrag.
      tt-qty            = tt-qty + t-qty.   /* Add By Gerald 21022020 for Robot n Co */
      t-qty             = 0.                /* Add By Gerald 21022020 for Robot n Co */
 
      IF sm-disp1 THEN 
      DO: 
        FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN 
        DO: 
          it-exist = YES. 
          c-list.creditlimit = queasy.deci3. 
          c-list.officer = curr-name. 
        END. 
      END. 
 
      curr-name = c1-list.name. 
      t-cost    = 0. 
      tf-cost   = 0. 
      tb-cost   = 0. 
      to-cost   = 0. 
      t-betrag  = 0. 
      tf-betrag = 0. 
      tb-betrag = 0.
      to-betrag = 0.
    END. 
    IF NOT c1-list.detailed THEN 
    DO: 
      t-cost    = t-cost + c1-list.t-cost. 
      tf-cost   = tf-cost + c1-list.f-cost. 
      tb-cost   = tb-cost + c1-list.b-cost. 
      to-cost   = to-cost + c1-list.o-cost. 
      t-betrag  = t-betrag + c1-list.betrag. 
      tf-betrag = tf-betrag + c1-list.f-betrag. 
      tb-betrag = tb-betrag + c1-list.b-betrag. 
      to-betrag = to-betrag + c1-list.o-betrag. 
    END. 
 
    CREATE c-list. 
    nr = nr + 1. 
    c-list.nr       = nr. 
    c-list.datum    = c1-list.datum. 
    c-list.dept     = c1-list.dept. 
    c-list.deptname = c1-list.deptname. 
    c-list.rechnr   = c1-list.rechnr. 
    c-list.artnr    = c1-list.artnr. 
    c-list.p-artnr  = c1-list.p-artnr. 
    c-list.bezeich  = c1-list.bezeich.
    /* c-list.qty      = c1-list.qty. */      /* Add By Gerald 21012020 for Robot n Co */
    c-list.betrag   = c1-list.betrag. 
    c-list.f-betrag = c1-list.f-betrag. 
    c-list.b-betrag = c1-list.b-betrag. 
    c-list.o-betrag = c1-list.o-betrag. 
    c-list.f-cost   = c1-list.f-cost. 
    c-list.b-cost   = c1-list.b-cost. 
    c-list.o-cost   = c1-list.o-cost. 
    c-list.t-cost   = c1-list.t-cost. 
    c-list.name     = c1-list.name. 

    IF p-artnr EQ 0 THEN
    DO:
        qty         = c1-list.qty.       
        c-list.qty  = c1-list.qty.      /* Add By Gerald 21012020 for Robot n Co */
        t-qty       = t-qty + qty.
    END.
  END. 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich    = "T O T A L". 
  c-list.qty        = t-qty.        /* Add By Gerald 21012020 for Robot n Co */
  c-list.f-cost     = tf-cost. 
  c-list.b-cost     = tb-cost. 
  c-list.o-cost     = to-cost. 
  c-list.t-cost     = t-cost. 
  c-list.betrag     = t-betrag. 
  c-list.f-betrag   = tf-betrag. 
  c-list.b-betrag   = tb-betrag. 
  c-list.o-betrag   = to-betrag.
  tt-qty            = tt-qty + t-qty.   /* Add By Gerald 21012020 for Robot n Co */
  t-qty             = 0.                /* Add By Gerald 21012020 for Robot n Co */
 
  IF sm-disp1 THEN 
  DO: 
    FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 
      it-exist           = YES. 
      c-list.creditlimit = queasy.deci3. 
      c-list.officer     = curr-name. 
    END. 
  END. 
 
  create c-list. 
  nr                = nr + 1. 
  c-list.nr         = nr. 
  c-list.bezeich    = "GRAND TOTAL". 
  c-list.qty        = tt-qty.           /* Add By Gerald 21012020 for Robot n Co */    
  c-list.f-cost     = ttf-cost. 
  c-list.b-cost     = ttb-cost. 
  c-list.o-cost     = tto-cost. 
  c-list.t-cost     = tt-cost. 
  c-list.betrag     = tt-betrag. 
  c-list.f-betrag   = ttf-betrag. 
  c-list.b-betrag   = ttb-betrag. 
  c-list.o-betrag   = tto-betrag.
 
  IF it-exist THEN 
  DO: 
    FOR EACH s-list WHERE s-list.creditlimit NE 0 AND s-list.creditlimit LT s-list.betrag AND s-list.flag = 0: 
      create c-list. 
      nr                    = nr + 1. 
      c-list.nr             = nr. 
      c-list.flag           = 1. 
      c-list.deptname       = translateExtended ("Over CreditLimit",lvCAREA,""). 
      c-list.name           = s-list.officer. 
      c-list.creditlimit    = s-list.creditlimit. 
      c-list.bezeich        = STRING(s-list.creditlimit," ->>>,>>>,>>>,>>9.99"). 
      c-list.betrag         = s-list.betrag. 
      c-list.f-betrag       = s-list.betrag - s-list.creditlimit. 
    END. 
  END. 
END. 

PROCEDURE journal-gname: 
DEFINE VARIABLE amount          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amount        AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-amount      AS DECIMAL. 
DEFINE VARIABLE rechnr          AS INTEGER. 
DEFINE VARIABLE dept            AS INTEGER INITIAL -1. 
DEFINE VARIABLE p-artnr         AS INTEGER. 
DEFINE VARIABLE depart          AS CHAR. 
DEFINE VARIABLE bezeich         AS CHAR. 
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE artnr           AS INTEGER. 
DEFINE VARIABLE datum           AS DATE INITIAL ?. 
DEFINE VARIABLE curr-datum      AS DATE INITIAL ?. 
DEFINE VARIABLE rate            AS DECIMAL INITIAL 1.  
 
DEFINE VARIABLE f-cost AS DECIMAL. 
DEFINE VARIABLE b-cost AS DECIMAL. 
DEFINE VARIABLE o-cost AS DECIMAL. 
DEFINE VARIABLE cost   AS DECIMAL. 
 
DEFINE VARIABLE t-cost  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE t-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tb-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE to-betrag AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE tt-cost  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-cost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tto-cost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tt-betrag  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttf-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ttb-betrag AS DECIMAL INITIAL 0.
DEFINE VARIABLE tto-betrag AS DECIMAL INITIAL 0.
 
DEFINE VARIABLE f-endkum    AS INTEGER. 
DEFINE VARIABLE b-endkum    AS INTEGER. 
DEFINE VARIABLE curr-name   AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE name        AS CHAR. 

DEFINE buffer h-art FOR h-artikel. 
DEFINE buffer fr-art FOR artikel.
DEFINE buffer s-list FOR c-list. 
 
  FOR EACH c-list: 
    delete c-list. 
  END. 
  FOR EACH c1-list: 
    delete c1-list. 
  END. 
  it-exist = NO. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
      FOR EACH h-compli WHERE h-compli.datum GE from-date AND h-compli.datum LE to-date 
          AND h-compli.departement = hoteldpt.num AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
          BY h-compli.departement BY h-compli.rechnr: 
 
      FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
      IF AVAILABLE h-bill THEN name = h-bill.bilname. 
      ELSE 
      DO: 
        FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum AND h-journal.departement = h-compli.departement 
          AND h-journal.segmentcode = h-compli.p-artnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
        IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
          name = h-journal.aendertext. 
      END. 
      IF name = gname THEN 
      DO: 
        IF double-currency AND curr-datum NE h-compli.datum THEN 
        DO: 
          curr-datum = h-compli.datum. 
          RUN find-exrate(curr-datum). 
          IF AVAILABLE exrate THEN rate = exrate.betrag. 
          ELSE rate = exchg-rate. 
        END. 
 
        FIND FIRST c1-list WHERE c1-list.datum = h-compli.datum AND c1-list.dept = h-compli.departement 
          AND c1-list.rechnr = h-compli.rechnr AND c1-list.p-artnr = h-compli.p-artnr NO-ERROR. 
        IF NOT AVAILABLE c1-list THEN 
        DO: 
          create c1-list. 
          c1-list.datum      = h-compli.datum. 
          c1-list.dept       = h-compli.departement. 
          c1-list.deptname   = hoteldpt.depart. 
          c1-list.rechnr     = h-compli.rechnr. 
          c1-list.p-artnr    = h-compli.p-artnr. 
          FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
          IF AVAILABLE h-bill THEN c1-list.name = h-bill.bilname. 
          ELSE 
          DO: 
            FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum AND h-journal.departement = h-compli.departement 
              AND h-journal.segmentcode = h-compli.p-artnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
            IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
              c-list.name = h-journal.aendertext. 
          END. 
          c1-list.bezeich = h-art.bezeich. 
        END. 
 
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr AND h-artikel.departement = h-compli.departement NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront AND artikel.departement = h-compli.departement NO-LOCK. 
        cost = 0. 
        f-cost = 0. 
        b-cost = 0. 
        o-cost = 0. 

        FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr AND h-cost.departement = h-compli.departement 
          AND h-cost.datum = h-compli.datum AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
        DO: 
          cost = h-compli.anzahl * h-cost.betrag. 
          RUN cost-correction(INPUT-OUTPUT cost).
          cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
          tt-cost = tt-cost + cost. 
          IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          DO: 
            f-cost   = cost. 
            ttf-cost = ttf-cost + cost. 
          END. 
          ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
          DO: 
            b-cost   = cost. 
            ttb-cost = ttb-cost + cost. 
          END. 
          ELSE 
          DO: 
            o-cost   = cost. 
            tto-cost = tto-cost + cost. 
          END. 
          c1-list.f-cost = c1-list.f-cost + f-cost. 
          c1-list.b-cost = c1-list.b-cost + b-cost. 
          c1-list.o-cost = c1-list.o-cost + o-cost. 
          c1-list.t-cost = c1-list.t-cost + cost. 
        END. 
        IF (NOT AVAILABLE h-cost AND h-compli.datum LT billdate) OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
        DO: 
          cost = h-compli.anzahl * h-compli.epreis * h-artikel.prozent / 100 * rate. 
          cost    = ROUND(cost,2).    /*FDL April 27, 2023 => 0777DC*/
          tt-cost = tt-cost + cost. 
          IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          DO: 
            f-cost   = cost. 
            ttf-cost = ttf-cost + cost. 
          END. 
          ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
          DO: 
            b-cost   = cost. 
            ttb-cost = ttb-cost + cost. 
          END. 
          ELSE 
          DO: 
            o-cost   = cost. 
            tto-cost = tto-cost + cost. 
          END. 
          c1-list.f-cost = c1-list.f-cost + f-cost. 
          c1-list.b-cost = c1-list.b-cost + b-cost. 
          c1-list.o-cost = c1-list.o-cost + o-cost. 
          c1-list.t-cost = c1-list.t-cost + cost. 
        END. 
 
/** Bill Amount  **/ 
        c1-list.betrag   = c1-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
        tt-betrag        = tt-betrag + h-compli.anzahl * h-compli.epreis * rate. 
 
/** Food Betrag **/ 
        IF /*artikel.endkum = f-endkum*/ artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
        DO: 
          c1-list.f-betrag   = c1-list.f-betrag + h-compli.anzahl * h-compli.epreis * rate. 
          ttf-betrag         = ttf-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        END. 
 
/** Beverage Betrag **/ 
        ELSE IF /*artikel.endkum = b-endkum*/ artikel.umsatzart = 6 THEN 
        DO: 
          c1-list.b-betrag = c1-list.b-betrag + h-compli.anzahl * h-compli.epreis * rate. 
          ttb-betrag       = ttb-betrag + h-compli.anzahl * h-compli.epreis * rate. 
        END.

/** Other Betrag **/
        ELSE
        DO:
            c1-list.o-betrag    = c1-list.o-betrag + h-compli.anzahl * h-compli.epreis * rate.
            tto-betrag          = tto-betrag + h-compli.anzahl * h-compli.epreis * rate.
        END.
      END. 
    END. 
  END. 

  curr-name = "". 
  f-cost    = 0. 
  b-cost    = 0. 
  o-cost    = 0. 
  FOR EACH c1-list WHERE c1-list.betrag NE 0 BY c1-list.name BY c1-list.datum BY c1-list.dept: 
    IF curr-name = "" THEN curr-name = c1-list.name. 
    IF curr-name NE c1-list.name THEN 
    DO: 
      create c-list. 
      nr                = nr + 1. 
      c-list.nr         = nr. 
      c-list.bezeich    = "T O T A L". 
      c-list.f-cost     = tf-cost. 
      c-list.b-cost     = tb-cost. 
      c-list.o-cost     = to-cost. 
      c-list.t-cost     = t-cost. 
      c-list.betrag     = t-betrag. 
      c-list.f-betrag   = tf-betrag. 
      c-list.b-betrag   = tb-betrag. 
      c-list.o-betrag   = to-betrag.
      curr-name         = c1-list.name. 
      t-cost    = 0. 
      tf-cost   = 0. 
      tb-cost   = 0. 
      to-cost   = 0. 
      t-betrag  = 0. 
      tf-betrag = 0. 
      tb-betrag = 0. 
      to-betrag = 0. 
    END. 

    t-cost      = t-cost + c1-list.t-cost. 
    tf-cost     = tf-cost + c1-list.f-cost. 
    tb-cost     = tb-cost + c1-list.b-cost. 
    to-cost     = to-cost + c1-list.o-cost. 
    t-betrag    = t-betrag + c1-list.betrag. 
    tf-betrag   = tf-betrag + c1-list.f-betrag. 
    tb-betrag   = tb-betrag + c1-list.b-betrag. 
    to-betrag   = to-betrag + c1-list.o-betrag. 
    create c-list. 
    nr              = nr + 1. 
    c-list.nr       = nr. 
    c-list.datum    = c1-list.datum. 
    c-list.dept     = c1-list.dept. 
    c-list.deptname = c1-list.deptname. 
    c-list.rechnr   = c1-list.rechnr. 
    c-list.p-artnr  = c1-list.p-artnr. 
    c-list.bezeich  = c1-list.bezeich. 
    c-list.betrag   = c1-list.betrag. 
    c-list.f-betrag = c1-list.f-betrag. 
    c-list.b-betrag = c1-list.b-betrag. 
    c-list.o-betrag = c1-list.o-betrag. 
    c-list.f-cost   = c1-list.f-cost. 
    c-list.b-cost   = c1-list.b-cost. 
    c-list.o-cost   = c1-list.o-cost. 
    c-list.t-cost   = c1-list.t-cost. 
    c-list.name     = c1-list.name. 
  END. 

  create c-list. 
  nr                = nr + 1. 
  c-list.nr         = nr. 
  c-list.bezeich    = "T O T A L". 
  c-list.f-cost     = tf-cost. 
  c-list.b-cost     = tb-cost. 
  c-list.o-cost     = to-cost. 
  c-list.t-cost     = t-cost. 
  c-list.betrag     = t-betrag. 
  c-list.f-betrag   = tf-betrag. 
  c-list.b-betrag   = tb-betrag. 
  c-list.o-betrag   = to-betrag. 
 
  IF sm-disp1 THEN 
  DO: 
    FIND FIRST queasy WHERE queasy.key = 105 AND queasy.char1 = curr-name NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 
      it-exist = YES. 
      c-list.creditlimit = queasy.deci3. 
      c-list.officer     = curr-name. 
      IF c-list.creditlimit NE 0 AND c-list.creditlimit LT c-list.betrag THEN 
      DO: 
        FIND FIRST s-list WHERE RECID(s-list) = RECID(c-list) NO-LOCK. 
        create c-list. 
        nr                  = nr + 1. 
        c-list.nr           = nr. 
        c-list.flag         = 1. 
        c-list.deptname     = translateExtended ("Over CreditLimit",lvCAREA,""). 
        c-list.name         = s-list.officer. 
        c-list.creditlimit  = s-list.creditlimit. 
        c-list.bezeich      = STRING(s-list.creditlimit," ->>>,>>>,>>>,>>9.99"). 
        c-list.betrag       = s-list.betrag. 
        c-list.f-betrag     = s-list.betrag - s-list.creditlimit. 
      END. 
    END. 
  END. 
END. 

PROCEDURE find-exrate: 
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO. 
  IF foreign-nr NE 0 THEN 
      FIND FIRST exrate WHERE exrate.artnr = foreign-nr AND exrate.datum = curr-date NO-LOCK NO-ERROR. 
  ELSE 
      FIND FIRST exrate WHERE exrate.datum = curr-date NO-LOCK NO-ERROR. 
END. 

PROCEDURE cost-correction:
DEF INPUT-OUTPUT PARAMETER cost AS DECIMAL.
  FIND FIRST h-bill-line WHERE h-bill-line.rechnr = h-compli.rechnr AND h-bill-line.bill-datum  = h-compli.datum
    AND h-bill-line.departement = h-compli.departement AND h-bill-line.artnr = h-compli.artnr
    AND h-bill-line.epreis      = h-compli.epreis NO-LOCK NO-ERROR.
  IF AVAILABLE h-bill-line AND SUBSTR(h-bill-line.bezeich, LENGTH(h-bill-line.bezeich), 1) = "*" AND h-bill-line.epreis NE 0 THEN
  DO:
    FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr AND h-artikel.departement = h-bill-line.departement NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel AND h-artikel.artart = 0 AND h-artikel.epreis1 GT h-bill-line.epreis THEN
     cost = cost * h-bill-line.epreis / h-artikel.epreis1.
  END.
END.

PROCEDURE coba:
FIND FIRST h-artikel WHERE h-artikel.artnr = artnr AND h-artikel.departement = c-list.dept NO-LOCK NO-ERROR. 
  IF AVAILABLE h-artikel THEN 
  DO:
    ASSIGN
      c-list.p-artnr = artnr
      c-list.bezeich = h-artikel.bezeich
    .
    FOR EACH h-compli WHERE h-compli.datum = c-list.datum AND c-list.dept = h-compli.departement AND c-list.rechnr = h-compli.rechnr AND h-compli.betriebsnr = 0: 
      h-compli.p-artnr = artnr.
    END.
  END.

  ASSIGN
    curr-name = c-list.NAME 
    guestname = c-list.NAME /*F :SCREEN-VALUE IN BROWSE b1 F*/
  . 
  IF guestname NE "" AND guestname NE ? AND curr-name NE guestname THEN 
  DO: 
    /*ASSIGN c-list.NAME. */
    FIND FIRST h-bill WHERE h-bill.rechnr = c-list.rechnr AND h-bill.departement = c-list.dept NO-LOCK NO-ERROR. 
    IF AVAILABLE h-bill THEN 
    DO: 
      FIND CURRENT h-bill EXCLUSIVE-LOCK. 
      h-bill.bilname = guestname. 
      FIND CURRENT h-bill NO-LOCK. 
      FIND FIRST h-journal WHERE h-journal.bill-datum = c-list.datum AND h-journal.departement = c-list.dept AND h-journal.segmentcode = c-list.p-artnr 
          AND h-journal.rechnr = c-list.rechnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
      DO WHILE AVAILABLE h-journal: 
        FIND CURRENT h-journal EXCLUSIVE-LOCK. 
        h-journal.aendertext = guestname. 
        FIND CURRENT h-journal NO-LOCK. 
        FIND NEXT h-journal WHERE h-journal.bill-datum = c-list.datum AND h-journal.departement = c-list.dept AND h-journal.segmentcode = c-list.p-artnr 
            AND h-journal.rechnr = c-list.rechnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
      END.
    END.
  END.
END.
