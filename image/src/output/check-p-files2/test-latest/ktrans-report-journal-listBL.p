DEFINE TEMP-TABLE c-list 
  FIELD nr      AS INTEGER 
  FIELD s-recid AS INTEGER 
  FIELD datum   AS DATE LABEL "Date" 
  FIELD dept    AS INTEGER 
  FIELD p-artnr AS INTEGER 
  FIELD dept1   AS CHAR     FORMAT "x(18)" LABEL "Transfer From" 
  FIELD dept2   AS CHAR     FORMAT "x(18)" LABEL "Transfer To" 
  FIELD artnr   AS INTEGER  FORMAT ">>>>>" LABEL "ArtNo" 
  FIELD bezeich AS CHAR     FORMAT "x(25)" LABEL "Description" 
  FIELD f-cost  AS DECIMAL  FORMAT "->>>,>>>,>>9.99"   LABEL "      Food-Cost" 
  FIELD b-cost  AS DECIMAL  FORMAT "->>>,>>>,>>9.99"   LABEL "  Beverage-Cost". 

DEF INPUT  PARAMETER sorttype  AS INT.
DEF INPUT  PARAMETER from-dept AS INT.
DEF INPUT  PARAMETER to-dept   AS INT.
DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER it-exist  AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER TABLE FOR c-list.

RUN journal-list.

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
DEFINE buffer h-dept FOR hoteldpt. 
 
DEFINE VARIABLE f-cost AS DECIMAL. 
DEFINE VARIABLE b-cost AS DECIMAL. 
DEFINE VARIABLE o-cost AS DECIMAL. 
DEFINE VARIABLE cost   AS DECIMAL. 
 
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
 
  IF sorttype = 2 THEN 
  DO: 
    RUN journal-list1. 
    RETURN. 
  END. 
 
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
    tf-cost = 0. 
    tb-cost = 0. 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.departement = hoteldpt.num 
      AND h-compli.betriebsnr GT 0 NO-LOCK, 
      FIRST h-dept WHERE h-dept.num = h-compli.betriebsnr NO-LOCK 
      BY h-compli.datum BY h-compli.betriebsnr: 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
        AND h-artikel.departement = h-compli.departement NO-LOCK. 
      create c-list. 
      nr = nr + 1. 
      ASSIGN 
        c-list.nr = nr 
        c-list.s-recid = RECID(h-compli) 
        c-list.datum = h-compli.datum 
        c-list.dept = h-compli.departement 
        c-list.dept1 = hoteldpt.depart 
        c-list.dept2 = h-dept.depart 
        c-list.p-artnr = h-compli.p-artnr 
        c-list.artnr = h-artikel.artnr 
        c-list.bezeich = h-artikel.bezeich. 
 
      f-cost = 0. 
      b-cost = 0. 
      IF h-compli.p-artnr = 1 THEN 
      DO: 
 
        c-list.f-cost = h-compli.epreis. 
        tf-cost = tf-cost + c-list.f-cost. 
        ttf-cost = ttf-cost + c-list.f-cost. 
      END. 
      ELSE IF h-compli.p-artnr = 2 THEN 
      DO: 
        c-list.b-cost = h-compli.epreis. 
        tb-cost = tb-cost + c-list.b-cost. 
        ttb-cost = ttb-cost + c-list.b-cost. 
      END. 
    END. 
    IF tf-cost NE 0 OR tb-cost NE 0 THEN 
    DO: 
      create c-list. 
      nr = nr + 1. 
      c-list.nr = nr. 
      c-list.bezeich = "T O T A L". 
      c-list.f-cost = tf-cost. 
      c-list.b-cost = tb-cost. 
    END. 
  END. 
 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich = "GRAND TOTAL". 
  c-list.f-cost = ttf-cost. 
  c-list.b-cost = ttb-cost. 
END. 

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
DEFINE buffer h-dept FOR hoteldpt. 
 
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
    tf-cost = 0. 
    tb-cost = 0. 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.betriebsnr = hoteldpt.num 
      AND h-compli.betriebsnr GT 0 NO-LOCK, 
      FIRST h-dept WHERE h-dept.num = h-compli.departement NO-LOCK 
      BY h-compli.datum BY h-compli.departement: 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
        AND h-artikel.departement = h-compli.departement NO-LOCK. 
      create c-list. 
      nr = nr + 1. 
      ASSIGN 
        c-list.s-recid = RECID(h-compli) 
        c-list.nr = nr 
        c-list.datum = h-compli.datum 
        c-list.dept = h-compli.departement 
        c-list.dept2 = hoteldpt.depart 
        c-list.dept1 = h-dept.depart 
        c-list.p-artnr = h-compli.p-artnr 
        c-list.artnr = h-artikel.artnr 
        c-list.bezeich = h-artikel.bezeich. 
 
      f-cost = 0. 
      b-cost = 0. 
      IF h-compli.p-artnr = 1 THEN 
      DO: 
 
        c-list.f-cost = h-compli.epreis. 
        tf-cost = tf-cost + c-list.f-cost. 
        ttf-cost = ttf-cost + c-list.f-cost. 
      END. 
      ELSE IF h-compli.p-artnr = 2 THEN 
      DO: 
        c-list.b-cost = h-compli.epreis. 
        tb-cost = tb-cost + c-list.b-cost. 
        ttb-cost = ttb-cost + c-list.b-cost. 
      END. 
    END. 
    IF tf-cost NE 0 OR tb-cost NE 0 THEN 
    DO: 
      create c-list. 
      nr = nr + 1. 
      c-list.nr = nr. 
      c-list.bezeich = "T O T A L". 
      c-list.f-cost = tf-cost. 
      c-list.b-cost = tb-cost. 
    END. 
  END. 
 
  create c-list. 
  nr = nr + 1. 
  c-list.nr = nr. 
  c-list.bezeich = "GRAND TOTAL". 
  c-list.f-cost = ttf-cost. 
  c-list.b-cost = ttb-cost. 
END. 
