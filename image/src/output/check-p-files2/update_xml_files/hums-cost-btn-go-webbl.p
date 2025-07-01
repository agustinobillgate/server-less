/*Eko 09 Juni 2015 tambah digit*/
DEFINE TEMP-TABLE h-list 
  FIELD artnr      AS INTEGER 
  FIELD dept       AS INTEGER 
  FIELD num        AS INTEGER 
  FIELD depart     AS CHAR 
  FIELD anz        AS INTEGER 
  FIELD m-anz      AS INTEGER 
  FIELD sales      AS DECIMAL 
  FIELD t-sales    AS DECIMAL INITIAL 0 
  FIELD comanz     AS INTEGER 
  FIELD compli     AS DECIMAL 
  FIELD t-compli   AS DECIMAL 
  FIELD t-comanz   AS INTEGER 
  FIELD cost       AS DECIMAL INITIAL 0 
  FIELD t-cost     AS DECIMAL INITIAL 0 
  FIELD ncost      AS DECIMAL INITIAL 0 
  FIELD t-ncost    AS DECIMAL INITIAL 0 
  FIELD proz       AS DECIMAL 
  FIELD t-proz     AS DECIMAL
  FIELD anz-cost   AS INTEGER
  FIELD manz-cost  AS INTEGER. 

DEFINE TEMP-TABLE output-list 
  FIELD num         AS INTEGER
  FIELD bezeich     AS CHARACTER
  FIELD anz         AS INTEGER 
  FIELD sales       AS DECIMAL
  FIELD ncost       AS DECIMAL
  FIELD comanz      AS INTEGER 
  FIELD compli      AS DECIMAL
  FIELD cost        AS DECIMAL
  FIELD proz        AS DECIMAL
  FIELD m-anz       AS INTEGER 
  FIELD t-sales     AS DECIMAL
  FIELD t-ncost     AS DECIMAL
  FIELD m-comanz    AS INTEGER 
  FIELD t-compli    AS DECIMAL
  FIELD t-cost      AS DECIMAL
  FIELD t-proz      AS DECIMAL
  FIELD anz-cost   AS INTEGER
  FIELD manz-cost  AS INTEGER
 .

DEF INPUT  PARAMETER sorttype AS INT.
DEF INPUT  PARAMETER detailed AS LOGICAL.
DEF INPUT  PARAMETER from-dept AS INT.
DEF INPUT  PARAMETER to-dept AS INT.
DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date AS DATE.
DEF INPUT  PARAMETER fact1 AS INT.
DEF INPUT  PARAMETER mi-compli-checked AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR output-list.

/*
DEF VAR sorttype AS INT INIT 4.
DEF VAR detailed AS LOGICAL INIT NO.
DEF VAR from-dept AS INT INIT 1.
DEF VAR to-dept AS INT INIT 5.
DEF VAR from-date AS DATE INIT 12/01/18.
DEF VAR to-date AS DATE INIT 12/31/18.
DEF VAR fact1 AS INT INIT 1.
DEF VAR short-flag AS LOGICAL INIT YES.
DEF VAR mi-compli-checked AS LOGICAL INIT YES.
*/
DEFINE VARIABLE exchg-rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE double-currency AS LOGICAL INITIAL NO. 
DEFINE VARIABLE foreign-nr AS INTEGER INITIAL 0 NO-UNDO. 

DEFINE VARIABLE dd-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-ncost AS DECIMAL INITIAL 0. 

DEFINE VARIABLE tot-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-ncost AS DECIMAL INITIAL 0. 

/* Naufal Afthar - 7FD6D0*/
DEFINE VARIABLE dd-anz    AS INTEGER INITIAL 0.
DEFINE VARIABLE dd-comanz AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-anz    AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-comanz AS INTEGER INITIAL 0.
/* end Naufal Afthar*/

FIND FIRST htparam WHERE paramnr = 240 no-lock. /* double currency */ 
double-currency = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO:
    foreign-nr = waehrung.waehrungsnr.
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 

IF sorttype = 1 THEN 
DO: 
  IF NOT detailed THEN RUN create-h-umsatz1. 
  ELSE RUN create-h-umsatz11. 
END. 
ELSE IF sorttype = 2 THEN 
DO: 
  IF NOT detailed THEN RUN create-h-umsatz2. 
  ELSE RUN create-h-umsatz22. 
END. 
ELSE IF sorttype = 3 THEN 
DO: 
  IF NOT detailed THEN RUN create-h-umsatz3. 
  ELSE RUN create-h-umsatz33. 
END. 
ELSE IF sorttype = 4 THEN 
DO: 
  IF NOT detailed THEN 
  DO:
    RUN create-h-umsatz1.     
    RUN create-h-umsatz2.     
    RUN create-h-umsatz3.     
  END.
  ELSE
  DO:
    RUN create-h-umsatz11.     
    RUN create-h-umsatz22.     
    RUN create-h-umsatz33.     
  END.
END.
/*
FOR EACH output-list:
    DISP output-list.bezeich FORMAT "x(25)" output-list.anz output-list.sales FORMAT ">>>,>>>,>>9.99"
        output-list.ncost FORMAT ">>>,>>>,>>9.99".
END.
*/
PROCEDURE create-h-umsatz1: 
DEFINE VARIABLE vat  AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL. 
DEFINE VARIABLE fact AS DECIMAL. 
DEFINE VARIABLE pos AS LOGICAL. 
DEFINE BUFFER h-art FOR h-artikel. 
 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost AS DECIMAL. 
 
DEFINE VARIABLE gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE m-endkum AS INTEGER. 
DEFINE VARIABLE t-anz AS INTEGER.
DEFINE VARIABLE t-m-anz AS INTEGER.
DEFINE VARIABLE t-comanz AS INTEGER.
DEFINE VARIABLE t-m-comanz AS INTEGER.
DEFINE VARIABLE t-anz-cost AS INTEGER.
DEFINE VARIABLE t-manz-cost AS INTEGER.

  dd-gsales = 0.
  dd-gcompli = 0.
  dd-gcost = 0.
  dd-ncost = 0.
  
  tot-gsales = 0.
  tot-gcompli = 0.
  tot-gcost = 0.
  tot-ncost = 0.

  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  FOR EACH h-list: 
    DELETE h-list. 
  END. 
 
  IF sorttype = 4 THEN
  DO:
    CREATE output-list.
    ASSIGN output-list.bezeich = "** Food **". 
  END.

  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 273 NO-LOCK. 
  m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    pos = NO. 
    FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN pos = YES.
    IF pos THEN 
    DO curr-datum = from-date TO to-date: 
      IF double-currency THEN 
      DO: 
        RUN find-exrate(curr-datum). 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
      rate = rate / fact1. 
      IF curr-datum = from-date THEN 
      DO: 
        CREATE h-list. 
        h-list.num = hoteldpt.num. 
        h-list.depart = hoteldpt.depart. 
      END. 
      FOR EACH artikel WHERE artikel.artart = 0 
        AND artikel.departement = hoteldpt.num 
        AND (artikel.endkum = f-endkum OR artikel.endkum = m-endkum 
        OR artikel.umsatzart = 3 OR artikel.umsatzart = 5) NO-LOCK, 
        FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum EQ curr-datum NO-LOCK: 
      
        RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
          umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
        ASSIGN vat = vat + vat2.

        /* Naufal Afthar - 7FD6D0
        FOR EACH h-artikel WHERE h-artikel.artnrfront EQ artikel.artnr
            AND h-artikel.departement EQ hoteldpt.num
            AND h-artikel.artart EQ 0 NO-LOCK,
            FIRST h-umsatz WHERE h-umsatz.datum EQ curr-datum
            AND h-umsatz.artnr EQ h-artikel.artnr
            AND h-umsatz.departement EQ h-artikel.departement NO-LOCK:

            IF h-umsatz.datum EQ to-date THEN
            DO:
              h-list.anz    = h-list.anz + h-umsatz.anzahl.
              h-list.sales = h-list.sales + h-umsatz.betrag / fact. /** h-list.sales + umsatz.betrag / fact. */ 
              gsales = gsales + h-umsatz.betrag / fact. 
              dd-gsales = dd-gsales + h-umsatz.betrag / fact.
            END.
            h-list.m-anz    = h-list.m-anz + h-umsatz.anzahl.
            h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
            t-gsales = t-gsales + h-umsatz.betrag / fact. 
            tot-gsales = tot-gsales + h-umsatz.betrag / fact.
        END.*/
             
        /* end Naufal Afthar*/
        
        IF umsatz.datum = to-date THEN 
        DO: 
          h-list.anz    = h-list.anz + umsatz.anzahl.
          h-list.sales = h-list.sales + umsatz.betrag / fact. /** h-list.sales + umsatz.betrag / fact. */ 
          gsales = gsales + umsatz.betrag / fact. 
          dd-gsales = dd-gsales + umsatz.betrag / fact. 
        END. 
        h-list.m-anz    = h-list.m-anz + umsatz.anzahl.
        h-list.t-sales = h-list.t-sales + umsatz.betrag / fact. 
        t-gsales = t-gsales + umsatz.betrag / fact. 
        tot-gsales = tot-gsales + umsatz.betrag / fact.
        
      END.

      FOR EACH h-compli WHERE h-compli.departement = hoteldpt.num AND 
        h-compli.datum EQ curr-datum AND h-compli.betriebsnr = 0 NO-LOCK, 
        FIRST h-art WHERE h-art.departement = h-compli.departement 
          AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK: 
        FIND FIRST h-artikel WHERE h-artikel.departement = h-compli.departement 
          AND h-artikel.artnr = h-compli.artnr NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
          AND artikel.departement = h-artikel.departement NO-LOCK. 
        IF (artikel.endkum = f-endkum OR artikel.endkum = m-endkum 
        OR artikel.umsatzart = 3 OR artikel.umsatzart = 5) THEN 
        DO: 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
            AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            cost = h-compli.anzahl * h-cost.betrag / fact1. 
          ELSE cost = h-compli.anzahl * 
            h-compli.epreis * h-artikel.prozent / 100 * rate. 
          IF h-compli.datum = to-date THEN 
          DO: 
            h-list.compli = h-list.compli + cost. 
            h-list.comanz = h-list.comanz + h-compli.anzahl. 
            gcompli = gcompli + cost. 
            dd-gcompli = dd-gcompli + cost. 
          END. 
          h-list.t-compli = h-list.t-compli + cost. 
          h-list.t-comanz = h-list.t-comanz + h-compli.anzahl. 
          t-gcompli = t-gcompli + cost. 
          tot-gcompli = tot-gcompli + cost. 
        END. 
      END. 
 
      FOR EACH h-journal WHERE h-journal.departement = hoteldpt.num AND 
        h-journal.bill-datum EQ curr-datum NO-LOCK, 
        FIRST h-art WHERE h-art.artnr = h-journal.artnr 
          AND h-art.departement = h-journal.departement 
          AND h-art.artart = 0 NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
          AND artikel.departement = h-art.departement 
          AND (artikel.endkum = f-endkum OR artikel.endkum = m-endkum 
          OR artikel.umsatzart = 3 OR artikel.umsatzart = 5) NO-LOCK: 
        cost = 0. 
        FIND FIRST h-cost WHERE h-cost.artnr = h-journal.artnr 
          AND h-cost.departement = h-journal.departement 
          AND h-cost.datum = h-journal.bill-datum 
          AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          cost = h-journal.anzahl * h-cost.betrag / fact1. 
        ELSE cost = h-journal.anzahl * h-journal.epreis * rate 
          * h-art.prozent / 100. 
        IF h-journal.bill-datum = to-date THEN 
        DO: 
          h-list.cost = h-list.cost + cost. 
          h-list.anz-cost = h-list.anz-cost + h-journal.anzahl.
          gcost = gcost + cost. 
          dd-gcost = dd-gcost + cost. 
        END. 
        h-list.t-cost = h-list.t-cost + cost. 
        h-list.manz-cost = h-list.manz-cost + h-journal.anzahl.
        t-gcost = t-gcost + cost. 
        tot-gcost = tot-gcost + cost. 
      END. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 no-lock. /* price DECIMAL */ 
  FOR EACH h-list: 
    h-list.ncost = h-list.cost - h-list.compli. 
    ncost = ncost + h-list.ncost. 
    dd-ncost = dd-ncost + h-list.ncost. 
    h-list.t-ncost = h-list.t-cost - h-list.t-compli. 
    t-ncost = t-ncost + h-list.t-ncost. 
    tot-ncost = tot-ncost + h-list.t-ncost. 
    IF h-list.sales NE 0 THEN h-list.proz = h-list.ncost / h-list.sales * 100. 
    IF h-list.t-sales NE 0 THEN h-list.t-proz 
      = h-list.t-ncost / h-list.t-sales * 100.

    ASSIGN
        t-anz       =  t-anz        + h-list.anz      
        t-m-anz     =  t-m-anz      + h-list.m-anz    
        t-comanz    =  t-comanz     + h-list.comanz   
        t-m-comanz  =  t-m-comanz   + h-list.t-comanz 
        t-anz-cost  =  t-anz-cost   + h-list.anz-cost 
        t-manz-cost =  t-manz-cost  + h-list.manz-cost.

/*  IF h-list.t-sales NE 0 THEN */ 
    DO: 
      CREATE output-list.
      ASSIGN
        output-list.num = h-list.num
        output-list.bezeich = STRING(h-list.num, "99 ") + STRING(h-list.depart, "x(20)")
        output-list.anz = h-list.anz
        output-list.sales = h-list.sales
        output-list.ncost = h-list.ncost
        output-list.comanz = h-list.comanz
        output-list.compli = h-list.compli
        output-list.cost = h-list.cost
        output-list.proz = h-list.proz
        output-list.m-anz = h-list.m-anz
        output-list.t-sales = h-list.t-sales
        output-list.t-ncost = h-list.t-ncost
        output-list.m-comanz = h-list.t-comanz
        output-list.t-compli = h-list.t-compli
        output-list.t-cost = h-list.t-cost
        output-list.t-proz = h-list.t-proz
        output-list.anz-cost = h-list.anz-cost
        output-list.manz-cost = h-list.manz-cost.
    END.
  END. 
 
  IF gsales NE 0 THEN proz = ncost / gsales * 100. 
  IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 
 
  CREATE output-list.
  ASSIGN
    output-list.bezeich = "T O T A L"
    output-list.sales = gsales
    output-list.ncost = ncost
    output-list.compli = gcompli
    output-list.cost = gcost
    output-list.proz = proz
    output-list.t-sales = t-gsales
    output-list.t-ncost = t-ncost
    output-list.t-compli = t-gcompli
    output-list.t-cost = t-gcost
    output-list.t-proz = t-proz
    output-list.anz         = t-anz       
    output-list.m-anz       = t-m-anz     
    output-list.comanz      = t-comanz    
    output-list.m-comanz    = t-m-comanz  
    output-list.anz-cost    = t-anz-cost  
    output-list.manz-cost   = t-manz-cost .

  /* Naufal Afthar - 7FD6D0 -> add grand total*/
  ASSIGN 
      dd-anz = dd-anz + t-anz
      dd-comanz = dd-comanz + t-comanz
      tm-anz = tm-anz + t-m-anz
      tm-comanz = tm-comanz + t-m-comanz.
END. 
 

PROCEDURE create-h-umsatz2: 

DEFINE VARIABLE vat AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL. 
DEFINE VARIABLE fact AS DECIMAL. 
DEFINE VARIABLE pos AS LOGICAL. 
DEFINE BUFFER h-art FOR h-artikel. 
 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost AS DECIMAL. 
 
DEFINE VARIABLE gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE b-endkum AS INTEGER. 

DEFINE VARIABLE t-anz       AS INTEGER.
DEFINE VARIABLE t-m-anz     AS INTEGER.
DEFINE VARIABLE t-comanz    AS INTEGER.
DEFINE VARIABLE t-m-comanz  AS INTEGER.
DEFINE VARIABLE t-anz-cost  AS INTEGER.
DEFINE VARIABLE t-manz-cost AS INTEGER.
 
  IF sorttype NE 4 THEN
  FOR EACH output-list: 
    DELETE output-list. 
  END. 

  FOR EACH h-list: 
    DELETE h-list. 
  END. 

  IF sorttype = 4 THEN
  DO:
    CREATE output-list.
    CREATE output-list.
    ASSIGN output-list.bezeich = "** Beverage **".
  END.
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    pos = NO. 
    FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN pos = YES. 
    IF pos THEN 
    DO curr-datum = from-date TO to-date: 
      IF double-currency THEN 
      DO: 
        RUN find-exrate(curr-datum). 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
      rate = rate / fact1. 
      IF curr-datum = from-date THEN 
      DO: 
        create h-list. 
        h-list.num = hoteldpt.num. 
        h-list.depart = hoteldpt.depart. 
      END. 
      FOR EACH artikel WHERE artikel.artart = 0 
        AND artikel.departement = hoteldpt.num 
        AND (artikel.endkum = b-endkum OR artikel.umsatzart = 6) NO-LOCK, 
        FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum EQ curr-datum NO-LOCK: 
/* SY AUG 13 2017 */
        RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
        ASSIGN vat = vat + vat2.

        /* Naufal Afthar - 7FD6D0
        FOR EACH h-artikel WHERE h-artikel.artnrfront EQ artikel.artnr
            AND h-artikel.departement EQ hoteldpt.num
            AND h-artikel.artart EQ 0 NO-LOCK,
            FIRST h-umsatz WHERE h-umsatz.datum EQ curr-datum
            AND h-umsatz.artnr EQ h-artikel.artnr
            AND h-umsatz.departement EQ h-artikel.departement NO-LOCK:

            IF h-umsatz.datum = to-date THEN 
            DO: 
              h-list.anz   = h-list.anz + h-umsatz.anzahl.
              h-list.sales = h-list.sales + h-umsatz.betrag / fact. /** h-list.sales + umsatz.betrag / fact. */ 
              gsales = gsales + h-umsatz.betrag / fact. 
              dd-gsales = dd-gsales + h-umsatz.betrag / fact. 
            END. 
            h-list.m-anz   = h-list.m-anz + h-umsatz.anzahl.
            h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
            t-gsales = t-gsales + h-umsatz.betrag / fact. 
            tot-gsales = tot-gsales + h-umsatz.betrag / fact.
        END.*/
        /* end Naufal Afthar*/
        
        IF umsatz.datum = to-date THEN 
        DO: 
          h-list.anz   = h-list.anz + umsatz.anzahl.
          h-list.sales = h-list.sales + umsatz.betrag / fact. /** h-list.sales + umsatz.betrag / fact. */ 
          gsales = gsales + umsatz.betrag / fact. 
          dd-gsales = dd-gsales + umsatz.betrag / fact. 
        END. 
         h-list.m-anz   = h-list.m-anz + umsatz.anzahl.
        h-list.t-sales = h-list.t-sales + umsatz.betrag / fact. 
        t-gsales = t-gsales + umsatz.betrag / fact. 
        tot-gsales = tot-gsales + umsatz.betrag / fact.
         
      END. 
 
      FOR EACH h-compli WHERE h-compli.departement = hoteldpt.num AND 
        h-compli.datum EQ curr-datum AND h-compli.betriebsnr = 0 NO-LOCK, 
        FIRST h-art WHERE h-art.departement = h-compli.departement 
          AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK: 
        FIND FIRST h-artikel WHERE h-artikel.departement = h-compli.departement 
          AND h-artikel.artnr = h-compli.artnr NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
          AND artikel.departement = h-artikel.departement NO-LOCK. 
        IF (artikel.endkum = b-endkum OR artikel.umsatzart = 6) THEN 
        DO: 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
            AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            cost = h-compli.anzahl * h-cost.betrag / fact1. 
          ELSE cost = h-compli.anzahl * 
            h-compli.epreis * h-artikel.prozent / 100 * rate. 
          IF h-compli.datum = to-date THEN 
          DO: 
            h-list.compli = h-list.compli + cost. 
            h-list.comanz = h-list.comanz + h-compli.anzahl. 
            gcompli = gcompli + cost. 
            dd-gcompli = dd-gcompli + cost. 
          END. 
          h-list.t-compli = h-list.t-compli + cost. 
          h-list.t-comanz = h-list.t-comanz + h-compli.anzahl. 
          t-gcompli = t-gcompli + cost. 
          tot-gcompli = tot-gcompli + cost. 
        END. 
      END. 
 
      FOR EACH h-journal WHERE h-journal.departement = hoteldpt.num AND 
        h-journal.bill-datum EQ curr-datum NO-LOCK, 
        FIRST h-art WHERE h-art.artnr = h-journal.artnr 
          AND h-art.departement = h-journal.departement 
          AND h-art.artart = 0 NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
          AND artikel.departement = h-art.departement 
          AND (artikel.endkum = b-endkum OR artikel.umsatzart = 6) NO-LOCK: 
        cost = 0. 
        FIND FIRST h-cost WHERE h-cost.artnr = h-journal.artnr 
          AND h-cost.departement = h-journal.departement 
          AND h-cost.datum = h-journal.bill-datum 
          AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          cost = h-journal.anzahl * h-cost.betrag / fact1. 
        ELSE cost = h-journal.anzahl * h-journal.epreis * rate 
          * h-art.prozent / 100. 
        IF h-journal.bill-datum = to-date THEN 
        DO: 
          h-list.cost = h-list.cost + cost. 
          h-list.anz-cost = h-list.anz-cost + h-journal.anzahl.
          gcost = gcost + cost. 
          dd-gcost = dd-gcost + cost. 
        END. 
        h-list.manz-cost = h-list.manz-cost + h-journal.anzahl.
        h-list.t-cost = h-list.t-cost + cost. 
        t-gcost = t-gcost + cost. 
        tot-gcost = tot-gcost + cost. 
      END. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 no-lock. /* price DECIMAL */ 
  FOR EACH h-list: 
    h-list.ncost = h-list.cost - h-list.compli. 
    ncost = ncost + h-list.ncost. 
    dd-ncost = dd-ncost + h-list.ncost. 
    h-list.t-ncost = h-list.t-cost - h-list.t-compli. 
    t-ncost = t-ncost + h-list.t-ncost. 
    tot-ncost = tot-ncost + h-list.t-ncost. 
    IF h-list.sales NE 0 THEN h-list.proz = h-list.ncost / h-list.sales * 100. 
    IF h-list.t-sales NE 0 THEN h-list.t-proz 
      = h-list.t-ncost / h-list.t-sales * 100. 

    ASSIGN
        t-anz       =  t-anz        + h-list.anz      
        t-m-anz     =  t-m-anz      + h-list.m-anz    
        t-comanz    =  t-comanz     + h-list.comanz   
        t-m-comanz  =  t-m-comanz   + h-list.t-comanz 
        t-anz-cost  =  t-anz-cost   + h-list.anz-cost 
        t-manz-cost =  t-manz-cost  + h-list.manz-cost.

/*  IF h-list.t-sales NE 0 THEN */ 
    DO:
      CREATE output-list.
      ASSIGN
        output-list.num = h-list.num
        output-list.bezeich = STRING(h-list.num, "99 ") + STRING(h-list.depart, "x(20)")
        output-list.anz = h-list.anz
        output-list.sales = h-list.sales
        output-list.ncost = h-list.ncost
        output-list.comanz = h-list.comanz
        output-list.compli = h-list.compli
        output-list.cost = h-list.cost
        output-list.proz = h-list.proz
        output-list.m-anz = h-list.m-anz
        output-list.t-sales = h-list.t-sales
        output-list.t-ncost = h-list.t-ncost
        output-list.m-comanz = h-list.t-comanz
        output-list.t-compli = h-list.t-compli
        output-list.t-cost = h-list.t-cost
        output-list.t-proz = h-list.t-proz
        output-list.anz-cost = h-list.anz-cost
        output-list.manz-cost = h-list.manz-cost.
    END. 
  END. 
 
  IF gsales NE 0 THEN proz = ncost / gsales * 100. 
  IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 
 
  CREATE output-list.
  ASSIGN
    output-list.bezeich = "T O T A L"
    output-list.sales = gsales
    output-list.ncost = ncost
    output-list.compli = gcompli
    output-list.cost = gcost
    output-list.proz = proz
    output-list.t-sales = t-gsales
    output-list.t-ncost = t-ncost
    output-list.t-compli = t-gcompli
    output-list.t-cost = t-gcost
    output-list.t-proz = t-proz
    output-list.anz         = t-anz       
    output-list.m-anz       = t-m-anz     
    output-list.comanz      = t-comanz    
    output-list.m-comanz    = t-m-comanz  
    output-list.anz-cost    = t-anz-cost  
    output-list.manz-cost   = t-manz-cost.

  /* Naufal Afthar - 7FD6D0 -> add grand total*/
  ASSIGN 
      dd-anz = dd-anz + t-anz
      dd-comanz = dd-comanz + t-comanz
      tm-anz = tm-anz + t-m-anz
      tm-comanz = tm-comanz + t-m-comanz.
END. 
 
PROCEDURE create-h-umsatz3: 
DEFINE VARIABLE vat  AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL. 
DEFINE VARIABLE fact AS DECIMAL. 
DEFINE VARIABLE pos AS LOGICAL. 
DEFINE BUFFER h-art FOR h-artikel. 
 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost AS DECIMAL. 
 
DEFINE VARIABLE gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE b-endkum AS INTEGER. 
DEFINE VARIABLE t-anz       AS INTEGER.
DEFINE VARIABLE t-m-anz     AS INTEGER.
DEFINE VARIABLE t-comanz    AS INTEGER.
DEFINE VARIABLE t-m-comanz  AS INTEGER.
DEFINE VARIABLE t-anz-cost  AS INTEGER.
DEFINE VARIABLE t-manz-cost AS INTEGER.
 
  IF sorttype NE 4 THEN
  FOR EACH output-list: 
    DELETE output-list. 
  END. 

  FOR EACH h-list: 
    DELETE h-list. 
  END. 
 
  IF sorttype = 4 THEN
  DO:
    CREATE output-list.
    CREATE output-list.
    ASSIGN output-list.bezeich = "** Others **".
   END.

  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    pos = NO. 
    FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN pos = YES. 
    IF pos THEN 
    DO curr-datum = from-date TO to-date: 
      IF double-currency THEN 
      DO: 
        RUN find-exrate(curr-datum). 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
      rate = rate / fact1. 
      IF curr-datum = from-date THEN 
      DO: 
        create h-list. 
        h-list.num = hoteldpt.num. 
        h-list.depart = hoteldpt.depart. 
      END. 

      FOR EACH artikel WHERE artikel.artart = 0 
        AND artikel.departement = hoteldpt.num 
        AND artikel.umsatzart = 4 NO-LOCK, 
        FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum EQ curr-datum NO-LOCK: 
        
        /* SY AUG 13 2017 */
        RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            umsatz.datum, OUTPUT serv, OUTPUT vat, 
            OUTPUT vat2, OUTPUT fact).
        ASSIGN vat = vat + vat2.

        /* Naufal Afthar - 7FD6D0
        FOR EACH h-artikel WHERE h-artikel.artnrfront EQ artikel.artnr
            AND h-artikel.departement EQ hoteldpt.num
            AND h-artikel.artart EQ 0 NO-LOCK,
            FIRST h-umsatz WHERE h-umsatz.datum EQ curr-datum
            AND h-umsatz.artnr EQ h-artikel.artnr
            AND h-umsatz.departement EQ h-artikel.departement NO-LOCK:

            IF h-umsatz.datum = to-date THEN 
            DO: 
              h-list.sales = h-list.sales + h-umsatz.betrag / fact. /** h-list.sales + umsatz.betrag / fact. */ 
              h-list.anz = h-list.anz + h-umsatz.anzahl.
              gsales = gsales + h-umsatz.betrag / fact. 
              dd-gsales = dd-gsales + h-umsatz.betrag / fact. 
            END. 
            h-list.m-anz = h-list.m-anz + h-umsatz.anzahl.
            h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
            t-gsales = t-gsales + h-umsatz.betrag / fact. 
            tot-gsales = tot-gsales + h-umsatz.betrag / fact.
        END.*/
        /* end Naufal Afthar */
        
        IF umsatz.datum = to-date THEN 
        DO: 
          h-list.sales = h-list.sales + umsatz.betrag / fact. /** h-list.sales + umsatz.betrag / fact. */ 
          h-list.anz = h-list.anz + umsatz.anzahl.
          gsales = gsales + umsatz.betrag / fact. 
          dd-gsales = dd-gsales + umsatz.betrag / fact. 
        END. 
        h-list.m-anz = h-list.m-anz + umsatz.anzahl.
        h-list.t-sales = h-list.t-sales + umsatz.betrag / fact. 
        t-gsales = t-gsales + umsatz.betrag / fact. 
        tot-gsales = tot-gsales + umsatz.betrag / fact. 
        
      END. 
 
      FOR EACH h-compli WHERE h-compli.departement = hoteldpt.num AND 
        h-compli.datum EQ curr-datum AND h-compli.betriebsnr = 0 NO-LOCK, 
        FIRST h-art WHERE h-art.departement = h-compli.departement 
          AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK: 
        FIND FIRST h-artikel WHERE h-artikel.departement = h-compli.departement 
          AND h-artikel.artnr = h-compli.artnr NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
          AND artikel.departement = h-artikel.departement NO-LOCK. 
        IF artikel.umsatzart = 4 THEN 
        DO: 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
            AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            cost = h-compli.anzahl * h-cost.betrag / fact1. 
          ELSE cost = h-compli.anzahl * 
            h-compli.epreis * h-artikel.prozent / 100 * rate. 
          IF h-compli.datum = to-date THEN 
          DO: 
            h-list.compli = h-list.compli + cost. 
            h-list.comanz = h-list.comanz + h-compli.anzahl. 
            gcompli = gcompli + cost. 
            dd-gcompli = dd-gcompli + cost. 
          END. 
          h-list.t-compli = h-list.t-compli + cost. 
          h-list.t-comanz = h-list.t-comanz + h-compli.anzahl. 
          t-gcompli = t-gcompli + cost. 
          tot-gcompli = tot-gcompli + cost. 
        END. 
      END. 
 
      FOR EACH h-journal WHERE h-journal.departement = hoteldpt.num AND 
        h-journal.bill-datum EQ curr-datum NO-LOCK, 
        FIRST h-art WHERE h-art.artnr = h-journal.artnr 
          AND h-art.departement = h-journal.departement 
          AND h-art.artart = 0 NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
          AND artikel.departement = h-art.departement 
          AND artikel.umsatzart = 4 NO-LOCK: 
        cost = 0. 
        FIND FIRST h-cost WHERE h-cost.artnr = h-journal.artnr 
          AND h-cost.departement = h-journal.departement 
          AND h-cost.datum = h-journal.bill-datum 
          AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          cost = h-journal.anzahl * h-cost.betrag / fact1. 
        ELSE cost = h-journal.anzahl * h-journal.epreis * rate 
          * h-art.prozent / 100. 
        IF h-journal.bill-datum = to-date THEN 
        DO: 
          h-list.cost = h-list.cost + cost. 
          h-list.anz-cost = h-list.anz-cost + h-journal.anzahl. 
          gcost = gcost + cost. 
          dd-gcost = dd-gcost + cost. 
        END. 
        h-list.t-cost = h-list.t-cost + cost. 
        h-list.manz-cost = h-list.manz-cost + h-journal.anzahl. 
        t-gcost = t-gcost + cost. 
        tot-gcost = tot-gcost + cost. 
      END. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 no-lock. /* price DECIMAL */ 
  FOR EACH h-list: 
    h-list.ncost = h-list.cost - h-list.compli. 
    ncost = ncost + h-list.ncost. 
    dd-ncost = dd-ncost + h-list.ncost. 
    h-list.t-ncost = h-list.t-cost - h-list.t-compli. 
    t-ncost = t-ncost + h-list.t-ncost. 
    tot-ncost = tot-ncost + h-list.t-ncost. 
    IF h-list.sales NE 0 THEN h-list.proz = h-list.ncost / h-list.sales * 100. 
    IF h-list.t-sales NE 0 THEN h-list.t-proz 
      = h-list.t-ncost / h-list.t-sales * 100. 


    ASSIGN
        t-anz       =  t-anz        + h-list.anz      
        t-m-anz     =  t-m-anz      + h-list.m-anz    
        t-comanz    =  t-comanz     + h-list.comanz   
        t-m-comanz  =  t-m-comanz   + h-list.t-comanz 
        t-anz-cost  =  t-anz-cost   + h-list.anz-cost 
        t-manz-cost =  t-manz-cost  + h-list.manz-cost.
/*  IF h-list.t-sales NE 0 THEN */ 
    DO: 
      CREATE output-list.
      ASSIGN
        output-list.num = h-list.num
        output-list.bezeich = STRING(h-list.num, "99 ") + STRING(h-list.depart, "x(20)")
        output-list.anz = h-list.anz
        output-list.sales = h-list.sales
        output-list.ncost = h-list.ncost
        output-list.comanz = h-list.comanz
        output-list.compli = h-list.compli
        output-list.cost = h-list.cost
        output-list.proz = h-list.proz
        output-list.m-anz = h-list.m-anz
        output-list.t-sales = h-list.t-sales
        output-list.t-ncost = h-list.t-ncost
        output-list.m-comanz = h-list.t-comanz
        output-list.t-compli = h-list.t-compli
        output-list.t-cost = h-list.t-cost
        output-list.t-proz = h-list.t-proz
        output-list.anz-cost = h-list.anz-cost
        output-list.manz-cost = h-list.manz-cost.
    END. 
  END. 
 
  IF gsales NE 0 THEN proz = ncost / gsales * 100. 
  IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 
 
  CREATE output-list.
  ASSIGN
    output-list.bezeich = "T O T A L"
    output-list.sales = gsales
    output-list.ncost = ncost
    output-list.compli = gcompli
    output-list.cost = gcost
    output-list.proz = proz
    output-list.t-sales = t-gsales
    output-list.t-ncost = t-ncost
    output-list.t-compli = t-gcompli
    output-list.t-cost = t-gcost
    output-list.t-proz = t-proz
    output-list.anz         = t-anz       
    output-list.m-anz       = t-m-anz     
    output-list.comanz      = t-comanz    
    output-list.m-comanz    = t-m-comanz  
    output-list.anz-cost    = t-anz-cost  
    output-list.manz-cost   = t-manz-cost.

  /* Naufal Afthar - 7FD6D0 -> add grand total*/
  ASSIGN 
      dd-anz = dd-anz + t-anz
      dd-comanz = dd-comanz + t-comanz
      tm-anz = tm-anz + t-m-anz
      tm-comanz = tm-comanz + t-m-comanz.

  IF sorttype = 4 THEN
  DO:
    CREATE output-list.
    CREATE output-list.
    ASSIGN
      output-list.bezeich = "GRAND TOTAL"
      output-list.sales = dd-gsales
      output-list.ncost = dd-ncost
      output-list.compli = dd-gcompli
      output-list.cost = dd-gcost
      output-list.t-sales = tot-gsales
      output-list.t-ncost = tot-ncost
      output-list.t-compli = tot-gcompli
      output-list.t-cost = tot-gcost
      /* Naufal Afthar - 7FD6D0 -> add grand total*/
      output-list.anz = dd-anz
      output-list.comanz = dd-comanz
      output-list.m-anz = tm-anz
      output-list.m-comanz = tm-comanz.
  END.
END. 

PROCEDURE create-h-umsatz11: 

DEFINE VARIABLE vat AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL. 
DEFINE VARIABLE fact AS DECIMAL. 
DEFINE VARIABLE pos AS LOGICAL. 
DEFINE BUFFER h-art FOR h-artikel. 
 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost AS DECIMAL. 
 
DEFINE VARIABLE gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE m-endkum AS INTEGER. 
 
DEFINE VARIABLE dd-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-ncost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tot-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-ncost AS DECIMAL INITIAL 0. 

/* Naufal Afthar - 7FD6D0 -> add grand total*/
DEFINE VARIABLE dd-anz      AS INTEGER INITIAL 0.
DEFINE VARIABLE dd-comanz   AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-anz      AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-comanz   AS INTEGER INITIAL 0.

DEFINE VARIABLE t-anz       AS INTEGER.
DEFINE VARIABLE t-m-anz     AS INTEGER.
DEFINE VARIABLE t-comanz    AS INTEGER.
DEFINE VARIABLE t-m-comanz  AS INTEGER.
DEFINE VARIABLE t-anz-cost  AS INTEGER.
DEFINE VARIABLE t-manz-cost AS INTEGER.

DEFINE VARIABLE ind AS INTEGER. 
DEFINE VARIABLE price-decimal AS INTEGER. 
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  FOR EACH h-list: 
    DELETE h-list. 
  END. 
 
  IF sorttype = 4 THEN
  DO:
    CREATE output-list.
    CREATE output-list.
    ASSIGN output-list.bezeich = "** Food **". 
   END.

  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 273 NO-LOCK. 
  m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    pos = NO. 
    FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN 
    DO: 
      create h-list. 
      h-list.num = hoteldpt.num. 
      h-list.depart = hoteldpt.depart. 
 
      FOR EACH h-artikel WHERE h-artikel.artart = 0 
        AND h-artikel.departement = hoteldpt.num NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = hoteldpt.num 
        AND (artikel.endkum = f-endkum OR artikel.endkum = m-endkum 
        OR artikel.umsatzart = 3 OR artikel.umsatzart = 5) NO-LOCK 
        BY h-artikel.bezeich: 
 
        CREATE h-list. 
        h-list.depart = h-artikel.bezeich. 

        FOR EACH h-umsatz WHERE h-umsatz.departement = h-artikel.departement 
          AND h-umsatz.artnr = h-artikel.artnr AND 
          h-umsatz.datum GE from-date AND h-umsatz.datum LE to-date NO-LOCK: 
/* SY AUG 13 2017 */
          RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            h-umsatz.datum, OUTPUT serv, OUTPUT vat, 
            OUTPUT vat2, OUTPUT fact).
          ASSIGN vat = vat + vat2.

          IF double-currency THEN 
          DO: 
            RUN find-exrate(h-umsatz.datum). 
            IF AVAILABLE exrate THEN rate = exrate.betrag. 
            ELSE rate = exchg-rate. 
          END. 
          rate = rate / fact1. 
          IF h-umsatz.datum = to-date THEN 
          DO: 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = FALSE THEN*/
            IF mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
                h-list.anz = h-list.anz + h-umsatz.anzahl.
            h-list.sales = h-list.sales + h-umsatz.betrag / fact. 
            dd-gsales = dd-gsales + h-umsatz.betrag / fact. 
          END. 
          /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = FALSE THEN*/
          IF mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
            h-list.m-anz = h-list.m-anz + h-umsatz.anzahl.
          h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
          tot-gsales = tot-gsales + h-umsatz.betrag / fact. 
 
 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-umsatz.artnr 
            AND h-cost.departement = h-umsatz.departement 
            AND h-cost.datum = h-umsatz.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          DO: 
            cost = h-cost.anzahl * h-cost.betrag / fact1. 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
            IF NOT mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
            DO: 
              IF h-umsatz.datum = to-date THEN 
                h-list.anz = h-list.anz + h-cost.anzahl. 
              h-list.m-anz = h-list.m-anz + h-cost.anzahl. 
            END. 
            /*
            IF h-umsatz.datum = to-date THEN 
                h-list.anz = h-list.anz + h-cost.anzahl.
            h-list.m-anz = h-list.m-anz + h-cost.anzahl. */
          END. 
          ELSE 
          DO: 
            FOR EACH h-journal WHERE h-journal.artnr = h-umsatz.artnr 
              AND h-journal.departement = h-umsatz.departement 
              AND h-journal.bill-datum EQ h-umsatz.datum NO-LOCK: 
              cost = cost + h-journal.anzahl *  h-journal.epreis 
                * h-artikel.prozent * rate / 100. 
              /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
              IF NOT mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
              DO: 
                IF h-umsatz.datum = to-date THEN 
                  h-list.anz = h-list.anz + h-journal.anzahl. 
                h-list.m-anz = h-list.m-anz + h-journal.anzahl. 
              END. 
              /*
              IF h-umsatz.datum = to-date THEN 
                  h-list.anz = h-list.anz + h-journal.anzahl.
              h-list.m-anz = h-list.m-anz + h-journal.anzahl. */
            END. 
          END. 
          IF h-umsatz.datum = to-date THEN 
          DO: 
            h-list.cost = h-list.cost + cost. 
            dd-gcost = dd-gcost + cost. 
          END. 
          h-list.t-cost = h-list.t-cost + cost. 
          tot-gcost = tot-gcost + cost. 
        END. 
 
        FOR EACH h-compli WHERE h-compli.departement = h-artikel.departement 
          AND h-compli.artnr = h-artikel.artnr 
          AND h-compli.datum GE from-date AND h-compli.datum LE to-date 
          AND h-compli.betriebsnr = 0 NO-LOCK, 
          FIRST h-art WHERE h-art.departement = h-compli.departement 
            AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK: 
          IF double-currency THEN 
          DO: 
            RUN find-exrate(h-compli.datum). 
            IF AVAILABLE exrate THEN rate = exrate.betrag. 
            ELSE rate = exchg-rate. 
          END. 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
            AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            cost = h-compli.anzahl * h-cost.betrag / fact1. 
          ELSE cost = h-compli.anzahl * 
            h-compli.epreis * h-artikel.prozent / 100 * rate. 
          IF h-compli.datum = to-date THEN 
          DO: 
            h-list.compli = h-list.compli + cost. 
            h-list.comanz = h-list.comanz + h-compli.anzahl. 
            dd-gcompli = dd-gcompli + cost. 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
            IF NOT mi-compli-checked THEN
              h-list.anz = h-list.anz - h-compli.anzahl. /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
          END. 
          h-list.t-compli = h-list.t-compli + cost. 
          h-list.t-comanz = h-list.t-comanz + h-compli.anzahl. 
          tot-gcompli = tot-gcompli + cost. 
          /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
          IF NOT mi-compli-checked THEN 
            h-list.m-anz = h-list.m-anz - h-compli.anzahl. /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
        END. 
      END. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 no-lock. /* price DECIMAL */ 
  price-decimal = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  ind = 0. 
  gsales = 0. 
  ncost = 0.
  gcompli = 0. 
  gcost= 0. 
  t-gsales = 0. 
  t-gcompli = 0. 
  t-gcost= 0. 
  t-ncost = 0. 
  t-proz = 0. 
  FOR EACH h-list WHERE h-list.t-cost NE 0 OR h-list.num NE 0 
    OR h-list.t-sales NE 0 OR h-list.t-compli NE 0:
    ind = ind + 1. 
    IF h-list.num NE 0 THEN 
    DO: 
      IF ind GT 1 THEN 
      DO: 
        IF gsales NE 0 THEN proz = ncost / gsales * 100. 
        IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100.
        CREATE output-list.
        ASSIGN
          output-list.bezeich = "T O T A L"
          output-list.anz = h-list.anz
          output-list.m-anz = h-list.m-anz
          output-list.comanz = h-list.comanz 
          output-list.m-comanz = h-list.t-comanz
          output-list.sales = gsales
          output-list.ncost = ncost
          output-list.compli = gcompli
          output-list.cost = gcost
          output-list.proz = proz
          output-list.t-proz = t-proz
          output-list.anz         = t-anz       
          output-list.m-anz       = t-m-anz     
          output-list.comanz      = t-comanz    
          output-list.m-comanz    = t-m-comanz  
          output-list.anz-cost    = t-anz-cost  
          output-list.manz-cost   = t-manz-cost.
        IF t-gsales GE 0 THEN
        DO:
          ASSIGN
            output-list.t-sales = t-gsales
            output-list.t-ncost = t-ncost
            output-list.t-compli = t-gcompli
            output-list.t-cost = t-gcost.
        END.
      END. 
      ncost = 0.
      gsales = 0. 
      gcompli = 0. 
      gcost= 0. 
      t-gsales = 0. 
      t-gcompli = 0. 
      t-gcost= 0. 
      t-ncost = 0. 
      t-proz = 0.

      /* Naufal Afthar - 7FD6D0 -> add grand total*/
      ASSIGN
          dd-anz = dd-anz + t-anz
          dd-comanz = dd-comanz + t-comanz
          tm-anz = tm-anz + t-m-anz
          tm-comanz = tm-comanz + t-m-comanz.

      ASSIGN
        t-anz       =  0    
        t-m-anz     =  0    
        t-comanz    =  0   
        t-m-comanz  =  0 
        t-anz-cost  =  0 
        t-manz-cost =  0.

      CREATE output-list.
      ASSIGN
        output-list.num = h-list.num
        output-list.bezeich = h-list.depart
        output-list.anz = h-list.anz
        output-list.comanz = h-list.comanz
        output-list.m-anz = h-list.m-anz
        output-list.m-comanz = h-list.comanz.
    END. 
    ELSE 
    DO: 
      gsales = gsales + h-list.sales. 
      gcost = gcost + h-list.cost. 
      gcompli = gcompli + h-list.compli. 
      t-gsales = t-gsales + h-list.t-sales. 
      t-gcost = t-gcost + h-list.t-cost. 
      t-gcompli = t-gcompli + h-list.t-compli. 
      h-list.ncost = h-list.cost - h-list.compli. 
      ncost = ncost + h-list.ncost. 
      h-list.t-ncost = h-list.t-cost - h-list.t-compli. 
      t-ncost = t-ncost + h-list.t-ncost. 
      tot-ncost = tot-ncost + h-list.t-ncost. 
      IF h-list.sales NE 0 THEN h-list.proz = h-list.ncost / h-list.sales * 100. 
      IF h-list.t-sales NE 0 THEN h-list.t-proz 
        = h-list.t-ncost / h-list.t-sales * 100. 

      ASSIGN
        t-anz       =  t-anz        + h-list.anz      
        t-m-anz     =  t-m-anz      + h-list.m-anz    
        t-comanz    =  t-comanz     + h-list.comanz   
        t-m-comanz  =  t-m-comanz   + h-list.t-comanz 
        t-anz-cost  =  t-anz-cost   + h-list.anz-cost 
        t-manz-cost =  t-manz-cost  + h-list.manz-cost.

      CREATE output-list.
      ASSIGN
        output-list.anz = h-list.anz
        output-list.m-anz = h-list.m-anz
        output-list.comanz = h-list.comanz
        output-list.m-comanz = h-list.t-comanz
        output-list.num = h-list.num
        output-list.bezeich = h-list.depart
        output-list.sales = h-list.sales
        output-list.ncost = h-list.ncost
        output-list.compli = h-list.compli
        output-list.cost = h-list.cost
        output-list.proz = h-list.proz
        output-list.t-proz = h-list.t-proz
        output-list.anz-cost = h-list.anz-cost
        output-list.manz-cost = h-list.manz-cost.
      IF h-list.t-sales GE 0 THEN
        ASSIGN
          output-list.t-sales = h-list.t-sales
          output-list.t-ncost = h-list.t-ncost
          output-list.t-compli = h-list.t-compli
          output-list.t-cost = h-list.t-cost.
      
    END. 
  END. 
  proz = 0. 
  t-proz = 0. 
  IF gsales NE 0 THEN proz = ncost / gsales * 100. 
  IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 

  /* Naufal Afthar - 7FD6D0 -> add grand total for the last TOTAL row*/
  ASSIGN 
      dd-anz = dd-anz + t-anz
      dd-comanz = dd-comanz + t-comanz
      tm-anz = tm-anz + t-m-anz
      tm-comanz = tm-comanz + t-m-comanz.
 
  CREATE output-list. 
  ASSIGN
    output-list.bezeich = "T O T A L"
    output-list.sales = gsales
    output-list.ncost = ncost
    output-list.compli = gcompli
    output-list.cost = gcost
    output-list.proz = proz
    output-list.t-proz = t-proz
    output-list.anz         = t-anz       
    output-list.m-anz       = t-m-anz     
    output-list.comanz      = t-comanz    
    output-list.m-comanz    = t-m-comanz  
    output-list.anz-cost    = t-anz-cost  
    output-list.manz-cost   = t-manz-cost
   .

  IF t-gsales GE 0 THEN
    ASSIGN
      output-list.t-sales = t-gsales
      output-list.t-ncost = t-ncost
      output-list.t-compli = t-gcompli
      output-list.t-cost = t-gcost.
      
  proz = 0. 
  t-proz = 0. 
  dd-ncost = dd-gcost - dd-gcompli. 
  IF dd-gsales NE 0 THEN proz = dd-ncost / dd-gsales * 100. 
  IF tot-gsales NE 0 THEN t-proz = tot-ncost / tot-gsales * 100. 
 
  CREATE output-list.
  ASSIGN
    output-list.bezeich = "GRAND TOTAL"
    output-list.sales = dd-gsales
    output-list.ncost = dd-ncost
    output-list.compli = dd-gcompli
    output-list.cost = dd-gcost
    output-list.proz = proz
    output-list.t-proz = t-proz
    /* Naufal Afthar - 7FD6D0 -> add grand total*/
    output-list.anz = dd-anz
    output-list.comanz = dd-comanz
    output-list.m-anz = tm-anz
    output-list.m-comanz = tm-comanz.
  IF tot-gsales GE 0 THEN
    ASSIGN
      output-list.t-sales = tot-gsales
      output-list.t-ncost = tot-ncost
      output-list.t-compli = tot-gcompli
      output-list.t-cost = tot-gcost.
END. 

PROCEDURE create-h-umsatz22: 
DEFINE VARIABLE vat AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL. 
DEFINE VARIABLE fact AS DECIMAL. 
DEFINE VARIABLE pos AS LOGICAL. 
DEFINE BUFFER h-art FOR h-artikel. 
 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost AS DECIMAL. 
 
DEFINE VARIABLE gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE b-endkum AS INTEGER. 
 
DEFINE VARIABLE dd-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-ncost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tot-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-ncost AS DECIMAL INITIAL 0. 

/* Naufal Afthar - 7FD6D0 -> add grand total*/
DEFINE VARIABLE dd-anz      AS INTEGER INITIAL 0.
DEFINE VARIABLE dd-comanz   AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-anz      AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-comanz   AS INTEGER INITIAL 0.

DEFINE VARIABLE t-anz       AS INTEGER.
DEFINE VARIABLE t-m-anz     AS INTEGER.
DEFINE VARIABLE t-comanz    AS INTEGER.
DEFINE VARIABLE t-m-comanz  AS INTEGER.
DEFINE VARIABLE t-anz-cost  AS INTEGER.
DEFINE VARIABLE t-manz-cost AS INTEGER.
 
DEFINE VARIABLE ind AS INTEGER. 
DEFINE VARIABLE price-decimal AS INTEGER. 

  IF sorttype NE 4 THEN
  FOR EACH output-list: 
    DELETE output-list. 
  END. 

  FOR EACH h-list: 
    DELETE h-list. 
  END. 
 
  IF sorttype = 4 THEN
  DO:
    CREATE output-list.
    CREATE output-list.
    ASSIGN output-list.bezeich = "** Beverage **".
   END.
  
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    pos = NO. 
    FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN 
    DO: 
      create h-list. 
      h-list.num = hoteldpt.num. 
      h-list.depart = hoteldpt.depart. 
 
      FOR EACH h-artikel WHERE h-artikel.artart = 0 
        AND h-artikel.departement = hoteldpt.num NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = hoteldpt.num 
        AND (artikel.endkum = b-endkum OR artikel.umsatzart = 6) NO-LOCK 
        BY h-artikel.bezeich: 
 
        CREATE h-list. 
        h-list.depart = h-artikel.bezeich. 
 
        FOR EACH h-umsatz WHERE h-umsatz.departement = h-artikel.departement 
          AND h-umsatz.artnr = h-artikel.artnr AND 
          h-umsatz.datum GE from-date AND h-umsatz.datum LE to-date NO-LOCK: 

/* SY AUG 13 2017 */
          RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            h-umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
          ASSIGN vat = vat + vat2.

          IF double-currency THEN 
          DO: 
            RUN find-exrate(h-umsatz.datum). 
            IF AVAILABLE exrate THEN rate = exrate.betrag. 
            ELSE rate = exchg-rate. 
          END. 
          rate = rate / fact1. 
          IF h-umsatz.datum = to-date THEN 
          DO: 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = FALSE THEN*/
            IF mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
              h-list.anz = h-list.anz + h-umsatz.anzahl. 
            h-list.sales = h-list.sales + h-umsatz.betrag / fact. 
            dd-gsales = dd-gsales + h-umsatz.betrag / fact. 
          END. 
          /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = FALSE THEN*/
          IF mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
            h-list.m-anz = h-list.m-anz + h-umsatz.anzahl. 
          h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
          tot-gsales = tot-gsales + h-umsatz.betrag / fact. 
 
 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-umsatz.artnr 
            AND h-cost.departement = h-umsatz.departement 
            AND h-cost.datum = h-umsatz.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          DO: 
            cost = h-cost.anzahl * h-cost.betrag / fact1. 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
            IF NOT mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
            DO: 
              IF h-umsatz.datum = to-date THEN 
                h-list.anz = h-list.anz + h-cost.anzahl. 
              h-list.m-anz = h-list.m-anz + h-cost.anzahl.
            END. 
          END. 
          ELSE 
          DO: 
            FOR EACH h-journal WHERE h-journal.artnr = h-umsatz.artnr 
              AND h-journal.departement = h-umsatz.departement 
              AND h-journal.bill-datum EQ h-umsatz.datum NO-LOCK: 
              cost = cost + h-journal.anzahl *  h-journal.epreis 
                * h-artikel.prozent * rate / 100. 
              /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
              IF NOT mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
              DO: 
                IF h-umsatz.datum = to-date THEN 
                  h-list.anz = h-list.anz + h-journal.anzahl. 
                h-list.m-anz = h-list.m-anz + h-journal.anzahl. 
              END. 
            END. 
          END. 
          IF h-umsatz.datum = to-date THEN 
          DO: 
            h-list.cost = h-list.cost + cost. 
            dd-gcost = dd-gcost + cost. 
          END. 
          h-list.t-cost = h-list.t-cost + cost. 
          tot-gcost = tot-gcost + cost. 
        END. 
 
        FOR EACH h-compli WHERE h-compli.departement = h-artikel.departement 
          AND h-compli.artnr = h-artikel.artnr 
          AND h-compli.datum GE from-date AND h-compli.datum LE to-date 
          AND h-compli.betriebsnr = 0 NO-LOCK, 
          FIRST h-art WHERE h-art.departement = h-compli.departement 
            AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK: 
          IF double-currency THEN 
          DO: 
            RUN find-exrate(h-compli.datum). 
            IF AVAILABLE exrate THEN rate = exrate.betrag. 
            ELSE rate = exchg-rate. 
          END. 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
            AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            cost = h-compli.anzahl * h-cost.betrag / fact1. 
          ELSE cost = h-compli.anzahl * 
            h-compli.epreis * h-artikel.prozent / 100 * rate. 
          IF h-compli.datum = to-date THEN 
          DO: 
            h-list.compli = h-list.compli + cost. 
            h-list.comanz = h-list.comanz + h-compli.anzahl. 
            dd-gcompli = dd-gcompli + cost. 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
            IF NOT mi-compli-checked THEN 
              h-list.anz = h-list.anz - h-compli.anzahl. /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
          END. 
          h-list.t-compli = h-list.t-compli + cost. 
          h-list.t-comanz = h-list.t-comanz + h-compli.anzahl. 
          /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
          IF NOT mi-compli-checked THEN
            h-list.m-anz = h-list.m-anz - h-compli.anzahl. /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
          tot-gcompli = tot-gcompli + cost. 
        END. 
      END. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. /* price DECIMAL */ 
  price-decimal = htparam.finteger.              /* Rulita 211024 | Fixing for serverless */  
  ind = 0. 
  gsales = 0. 
  ncost = 0.
  gcompli = 0. 
  gcost= 0. 
  t-gsales = 0. 
  t-gcompli = 0. 
  t-gcost= 0. 
  t-ncost = 0. 
  t-proz = 0. 

  ASSIGN
        t-anz       =  0     
        t-m-anz     =  0    
        t-comanz    =  0  
        t-m-comanz  =  0 
        t-anz-cost  =  0 
        t-manz-cost =  0.

  FOR EACH h-list WHERE h-list.t-cost NE 0 OR h-list.num NE 0 
    OR h-list.t-sales NE 0 OR h-list.t-compli NE 0:
    ind = ind + 1. 
    IF h-list.num NE 0 THEN 
    DO: 
      IF ind GT 1 THEN 
      DO: 
        IF gsales NE 0 THEN proz = ncost / gsales * 100. 
        IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 
        CREATE output-list. 
        ASSIGN
          output-list.bezeich = "T O T A L"
          output-list.anz = h-list.anz
          output-list.m-anz = h-list.m-anz
          output-list.comanz = h-list.comanz
          output-list.m-comanz = h-list.t-comanz
          output-list.sales = gsales
          output-list.ncost = ncost
          output-list.compli = gcompli
          output-list.cost = gcost
          output-list.proz = proz
          output-list.t-proz = t-proz
          output-list.anz         = t-anz       
          output-list.m-anz       = t-m-anz     
          output-list.comanz      = t-comanz    
          output-list.m-comanz    = t-m-comanz  
          output-list.anz-cost    = t-anz-cost  
          output-list.manz-cost   = t-manz-cost.

        IF t-gsales GE 0 THEN
          ASSIGN
            output-list.t-sales = t-gsales
            output-list.t-ncost = t-ncost
            output-list.t-compli = t-gcompli
            output-list.t-cost = t-gcost.
      END. 
      gsales = 0. 
      gcompli = 0. 
      gcost= 0. 
      ncost = 0.
      t-gsales = 0. 
      t-gcompli = 0. 
      t-gcost= 0. 
      t-ncost = 0. 
      t-proz = 0. 


      /* Naufal Afthar - 7FD6D0 -> add grand total*/
      ASSIGN
          dd-anz = dd-anz + t-anz
          dd-comanz = dd-comanz + t-comanz
          tm-anz = tm-anz + t-m-anz
          tm-comanz = tm-comanz + t-m-comanz.

      ASSIGN
        t-anz       =  0     
        t-m-anz     =  0    
        t-comanz    =  0  
        t-m-comanz  =  0 
        t-anz-cost  =  0 
        t-manz-cost =  0.

      CREATE output-list. 
      ASSIGN
        output-list.num = h-list.num
        output-list.anz = h-list.anz 
        output-list.m-anz = h-list.m-anz
        output-list.comanz = h-list.comanz
        output-list.m-comanz = h-list.t-comanz
        output-list.bezeich = h-list.depart.
    END. 
    ELSE 
    DO: 
      gsales = gsales + h-list.sales. 
      gcost = gcost + h-list.cost. 
      gcompli = gcompli + h-list.compli. 
      t-gsales = t-gsales + h-list.t-sales. 
      t-gcost = t-gcost + h-list.t-cost. 
      t-gcompli = t-gcompli + h-list.t-compli. 
      h-list.ncost = h-list.cost - h-list.compli. 
      ncost = ncost + h-list.ncost. 
      h-list.t-ncost = h-list.t-cost - h-list.t-compli. 
      t-ncost = t-ncost + h-list.t-ncost. 
      tot-ncost = tot-ncost + h-list.t-ncost. 
      IF h-list.sales NE 0 THEN h-list.proz = h-list.ncost / h-list.sales * 100. 
      IF h-list.t-sales NE 0 THEN h-list.t-proz 
        = h-list.t-ncost / h-list.t-sales * 100. 

      ASSIGN
        t-anz       =  t-anz        + h-list.anz      
        t-m-anz     =  t-m-anz      + h-list.m-anz    
        t-comanz    =  t-comanz     + h-list.comanz   
        t-m-comanz  =  t-m-comanz   + h-list.t-comanz 
        t-anz-cost  =  t-anz-cost   + h-list.anz-cost 
        t-manz-cost =  t-manz-cost  + h-list.manz-cost.

      CREATE output-list. 
      ASSIGN
        output-list.num = h-list.num
        output-list.bezeich = h-list.depart
        output-list.anz = h-list.anz 
        output-list.m-anz = h-list.m-anz
        output-list.comanz = h-list.comanz
        output-list.m-comanz = h-list.t-comanz
        output-list.sales = h-list.sales
        output-list.ncost = h-list.ncost
        output-list.compli = h-list.compli
        output-list.cost = h-list.cost
        output-list.proz = h-list.proz
        output-list.t-proz = h-list.t-proz
        output-list.anz-cost = h-list.anz-cost
        output-list.manz-cost = h-list.manz-cost
       .
      IF h-list.t-sales GE 0 THEN
        ASSIGN
          output-list.t-sales = h-list.t-sales
          output-list.t-ncost = h-list.t-ncost
          output-list.t-compli = h-list.t-compli
          output-list.t-cost = h-list.t-cost.
    END. 
  END. 
  proz = 0. 
  t-proz = 0. 
  IF gsales NE 0 THEN proz = ncost / gsales * 100. 
  IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 

  /* Naufal Afthar - 7FD6D0 -> add grand total for the last TOTAL row*/
  ASSIGN 
      dd-anz = dd-anz + t-anz
      dd-comanz = dd-comanz + t-comanz
      tm-anz = tm-anz + t-m-anz
      tm-comanz = tm-comanz + t-m-comanz.

  CREATE output-list. 
  ASSIGN
    output-list.bezeich = "T O T A L"
    output-list.sales = gsales
    output-list.ncost = ncost
    output-list.compli = gcompli
    output-list.cost = gcost
    output-list.proz = proz
    output-list.t-proz = t-proz
    output-list.anz         = t-anz       
    output-list.m-anz       = t-m-anz     
    output-list.comanz      = t-comanz    
    output-list.m-comanz    = t-m-comanz  
    output-list.anz-cost    = t-anz-cost  
    output-list.manz-cost   = t-manz-cost
  .

  IF t-gsales GE 0 THEN
    ASSIGN
      output-list.t-sales = t-gsales
      output-list.t-ncost = t-ncost
      output-list.t-compli = t-gcompli
      output-list.t-cost = t-gcost.
      
  proz = 0. 
  t-proz = 0. 
  dd-ncost = dd-gcost - dd-gcompli. 
  IF dd-gsales NE 0 THEN proz = dd-ncost / dd-gsales * 100. 
  IF tot-gsales NE 0 THEN t-proz = tot-ncost / tot-gsales * 100. 
 
  CREATE output-list.
  ASSIGN
    output-list.bezeich = "GRAND TOTAL"
    output-list.sales = dd-gsales
    output-list.ncost = dd-ncost
    output-list.compli = dd-gcompli
    output-list.cost = dd-gcost
    output-list.proz = proz
    output-list.t-proz = t-proz
    /* Naufal Afthar - 7FD6D0 -> add grand total*/
    output-list.anz = dd-anz
    output-list.comanz = dd-comanz
    output-list.m-anz = tm-anz
    output-list.m-comanz = tm-comanz.
  IF tot-gsales GE 0 THEN
    ASSIGN
      output-list.t-sales = tot-gsales
      output-list.t-ncost = tot-ncost
      output-list.t-compli = tot-gcompli
      output-list.t-cost = tot-gcost.
END. 

PROCEDURE create-h-umsatz33: 
DEFINE VARIABLE vat AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE vat2 AS DECIMAL NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL. 
DEFINE VARIABLE fact AS DECIMAL. 
DEFINE VARIABLE pos AS LOGICAL. 
DEFINE BUFFER h-art FOR h-artikel. 
 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost AS DECIMAL. 
 
DEFINE VARIABLE gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-ncost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-proz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE b-endkum AS INTEGER. 
 
DEFINE VARIABLE dd-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE dd-ncost AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE tot-gsales AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcompli AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-gcost AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-ncost AS DECIMAL INITIAL 0. 

/* Naufal Afthar - 7FD6D0 -> add grand total*/
DEFINE VARIABLE dd-anz      AS INTEGER INITIAL 0.
DEFINE VARIABLE dd-comanz   AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-anz      AS INTEGER INITIAL 0.
DEFINE VARIABLE tm-comanz   AS INTEGER INITIAL 0.

DEFINE VARIABLE t-anz       AS INTEGER.
DEFINE VARIABLE t-m-anz     AS INTEGER.
DEFINE VARIABLE t-comanz    AS INTEGER.
DEFINE VARIABLE t-m-comanz  AS INTEGER.
DEFINE VARIABLE t-anz-cost  AS INTEGER.
DEFINE VARIABLE t-manz-cost AS INTEGER.
 
DEFINE VARIABLE ind AS INTEGER. 
DEFINE VARIABLE price-decimal AS INTEGER. 

  IF sorttype NE 4 THEN
  FOR EACH output-list: 
    DELETE output-list. 
  END. 

  FOR EACH h-list: 
    DELETE h-list. 
  END. 
 
  IF sorttype = 4 THEN
  DO:
    CREATE output-list.
    CREATE output-list.
    ASSIGN output-list.bezeich = "** Others **".
  END.
  
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    pos = NO. 
    FIND FIRST h-artikel WHERE h-artikel.departement = hoteldpt.num 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN 
    DO: 
      create h-list. 
      h-list.num = hoteldpt.num. 
      h-list.depart = hoteldpt.depart. 
 
      FOR EACH h-artikel WHERE h-artikel.artart = 0 
        AND h-artikel.departement = hoteldpt.num NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = hoteldpt.num 
        AND artikel.umsatzart = 4 NO-LOCK 
        BY h-artikel.bezeich: 
 
        create h-list. 
        h-list.depart = h-artikel.bezeich. 

        FOR EACH h-umsatz WHERE h-umsatz.departement = h-artikel.departement 
          AND h-umsatz.artnr = h-artikel.artnr AND 
          h-umsatz.datum GE from-date AND h-umsatz.datum LE to-date NO-LOCK: 
/* SY AUG 13 2017 */
          RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            h-umsatz.datum, OUTPUT serv, OUTPUT vat, 
            OUTPUT vat2, OUTPUT fact).
          ASSIGN vat = vat + vat2.

          IF double-currency THEN 
          DO: 
            RUN find-exrate(h-umsatz.datum). 
            IF AVAILABLE exrate THEN rate = exrate.betrag. 
            ELSE rate = exchg-rate. 
          END. 
          rate = rate / fact1. 
          IF h-umsatz.datum = to-date THEN 
          DO: 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = FALSE THEN*/
            IF mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
              h-list.anz = h-list.anz + h-umsatz.anzahl. 
            h-list.sales = h-list.sales + h-umsatz.betrag / fact. 
            dd-gsales = dd-gsales + h-umsatz.betrag / fact. 
          END. 
          /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = FALSE THEN*/
          IF mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
            h-list.m-anz = h-list.m-anz + h-umsatz.anzahl. 
          h-list.t-sales = h-list.t-sales + h-umsatz.betrag / fact. 
          tot-gsales = tot-gsales + h-umsatz.betrag / fact. 
 
 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-umsatz.artnr 
            AND h-cost.departement = h-umsatz.departement 
            AND h-cost.datum = h-umsatz.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          DO: 
            cost = h-cost.anzahl * h-cost.betrag / fact1. 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
            IF NOT mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
            DO: 
              IF h-umsatz.datum = to-date THEN 
                h-list.anz = h-list.anz + h-cost.anzahl. 
              h-list.m-anz = h-list.m-anz + h-cost.anzahl. 
            END. 
          END. 
          ELSE 
          DO: 
            FOR EACH h-journal WHERE h-journal.artnr = h-umsatz.artnr 
              AND h-journal.departement = h-umsatz.departement 
              AND h-journal.bill-datum EQ h-umsatz.datum NO-LOCK: 
              cost = cost + h-journal.anzahl *  h-journal.epreis 
                * h-artikel.prozent * rate / 100. 
              /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
              IF NOT mi-compli-checked THEN /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
              DO: 
                IF h-umsatz.datum = to-date THEN 
                  h-list.anz = h-list.anz + h-journal.anzahl. 
                h-list.m-anz = h-list.m-anz + h-journal.anzahl.
              END. 
            END. 
          END. 
          IF h-umsatz.datum = to-date THEN 
          DO: 
            h-list.cost = h-list.cost + cost. 
            dd-gcost = dd-gcost + cost. 
          END. 
          h-list.t-cost = h-list.t-cost + cost. 
          tot-gcost = tot-gcost + cost. 
        END. 
 
        FOR EACH h-compli WHERE h-compli.departement = h-artikel.departement 
          AND h-compli.artnr = h-artikel.artnr 
          AND h-compli.datum GE from-date AND h-compli.datum LE to-date 
          AND h-compli.betriebsnr = 0 NO-LOCK, 
          FIRST h-art WHERE h-art.departement = h-compli.departement 
            AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK: 
          IF double-currency THEN 
          DO: 
            RUN find-exrate(h-compli.datum). 
            IF AVAILABLE exrate THEN rate = exrate.betrag. 
            ELSE rate = exchg-rate. 
          END. 
          cost = 0. 
          FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
            AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            cost = h-compli.anzahl * h-cost.betrag / fact1. 
          ELSE cost = h-compli.anzahl * 
            h-compli.epreis * h-artikel.prozent / 100 * rate. 
          IF h-compli.datum = to-date THEN 
          DO: 
            h-list.compli = h-list.compli + cost. 
            h-list.comanz = h-list.comanz + h-compli.anzahl. 
            dd-gcompli = dd-gcompli + cost. 
            /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
            IF NOT mi-compli-checked THEN
              h-list.anz = h-list.anz - h-compli.anzahl. /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
          END. 
          h-list.t-compli = h-list.t-compli + cost. 
          h-list.t-comanz = h-list.t-comanz + h-compli.anzahl. 
          /*MTIF MENU-ITEM mi-compli:CHECKED IN MENU mbar = TRUE THEN*/
          IF NOT mi-compli-checked THEN
            h-list.m-anz = h-list.m-anz - h-compli.anzahl. /* Naufal Afthar - 33E72E -> disamain seperti di desktop */
          tot-gcompli = tot-gcompli + cost. 
        END. 
      END. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 491 no-lock. /* price DECIMAL */ 
  price-decimal = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  ind = 0. 
  gsales = 0. 
  ncost = 0.
  gcompli = 0. 
  gcost= 0. 
  t-gsales = 0. 
  t-gcompli = 0. 
  t-gcost= 0. 
  t-ncost = 0. 
  t-proz = 0. 
  FOR EACH h-list WHERE h-list.t-cost NE 0 OR h-list.num NE 0 
    OR h-list.t-sales NE 0 OR h-list.t-compli NE 0: 
    ind = ind + 1. 
    IF h-list.num NE 0 THEN 
    DO: 
      IF ind GT 1 THEN 
      DO: 
        IF gsales NE 0 THEN proz = ncost / gsales * 100. 
        IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 
        CREATE output-list. 
        ASSIGN
          output-list.bezeich = "T O T A L"
          output-list.anz = h-list.anz
          output-list.m-anz = h-list.m-anz
          output-list.comanz = h-list.comanz
          output-list.m-comanz = h-list.t-comanz
          output-list.sales = gsales
          output-list.ncost = ncost
          output-list.compli = gcompli
          output-list.cost = gcost
          output-list.proz = proz
          output-list.t-proz = t-proz
          output-list.anz         = t-anz       
          output-list.m-anz       = t-m-anz     
          output-list.comanz      = t-comanz    
          output-list.m-comanz    = t-m-comanz  
          output-list.anz-cost    = t-anz-cost  
          output-list.manz-cost   = t-manz-cost.

        IF t-gsales GE 0 THEN
          ASSIGN
            output-list.t-sales = t-gsales
            output-list.t-ncost = t-ncost
            output-list.t-compli = t-gcompli
            output-list.t-cost = t-gcost.
      END. 
      gsales = 0. 
      gcompli = 0. 
      gcost= 0. 
      ncost = 0.
      t-gsales = 0. 
      t-gcompli = 0. 
      t-gcost= 0. 
      t-ncost = 0. 
      t-proz = 0. 

      /* Naufal Afthar - 7FD6D0 -> add grand total*/
      ASSIGN 
          dd-anz = dd-anz + t-anz
          dd-comanz = dd-comanz + t-comanz
          tm-anz = tm-anz + t-m-anz
          tm-comanz = tm-comanz + t-m-comanz.

      ASSIGN
        t-anz       =  0     
        t-m-anz     =  0    
        t-comanz    =  0  
        t-m-comanz  =  0 
        t-anz-cost  =  0 
        t-manz-cost =  0.

      CREATE output-list. 
      ASSIGN
        output-list.num = h-list.num
        output-list.anz = h-list.anz 
        output-list.m-anz = h-list.m-anz
        output-list.comanz = h-list.comanz
        output-list.m-comanz = h-list.t-comanz
        output-list.bezeich = h-list.depart.
    END. 
    ELSE 
    DO: 
      gsales = gsales + h-list.sales. 
      gcost = gcost + h-list.cost. 
      gcompli = gcompli + h-list.compli. 
      t-gsales = t-gsales + h-list.t-sales. 
      t-gcost = t-gcost + h-list.t-cost. 
      t-gcompli = t-gcompli + h-list.t-compli. 
      h-list.ncost = h-list.cost - h-list.compli. 
      ncost = ncost + h-list.ncost. 
      h-list.t-ncost = h-list.t-cost - h-list.t-compli. 
      t-ncost = t-ncost + h-list.t-ncost. 
      tot-ncost = tot-ncost + h-list.t-ncost. 
      IF h-list.sales NE 0 THEN h-list.proz = h-list.ncost / h-list.sales * 100. 
      IF h-list.t-sales NE 0 THEN h-list.t-proz 
        = h-list.t-ncost / h-list.t-sales * 100. 


      ASSIGN
        t-anz       =  t-anz        + h-list.anz      
        t-m-anz     =  t-m-anz      + h-list.m-anz    
        t-comanz    =  t-comanz     + h-list.comanz   
        t-m-comanz  =  t-m-comanz   + h-list.t-comanz 
        t-anz-cost  =  t-anz-cost   + h-list.anz-cost 
        t-manz-cost =  t-manz-cost  + h-list.manz-cost.

      CREATE output-list. 
      ASSIGN
        output-list.num = h-list.num
        output-list.bezeich = h-list.depart
        output-list.anz = h-list.anz 
        output-list.m-anz = h-list.m-anz
        output-list.comanz = h-list.comanz
        output-list.m-comanz = h-list.t-comanz
        output-list.sales = h-list.sales
        output-list.ncost = h-list.ncost
        output-list.compli = h-list.compli
        output-list.cost = h-list.cost
        output-list.proz = h-list.proz
        output-list.t-proz = h-list.t-proz
        output-list.anz-cost = h-list.anz-cost
        output-list.manz-cost = h-list.manz-cost
          /* Naufal Afthar - C7D66D -> hotfix repeating mtd qty and sales*/
        /*output-list.anz         = t-anz       
        output-list.m-anz       = t-m-anz     
        output-list.comanz      = t-comanz    
        output-list.m-comanz    = t-m-comanz  
        output-list.anz-cost    = t-anz-cost  
        output-list.manz-cost   = t-manz-cost */
      .
      IF h-list.t-sales GE 0 THEN
        ASSIGN
          output-list.t-sales = h-list.t-sales
          output-list.t-ncost = h-list.t-ncost
          output-list.t-compli = h-list.t-compli
          output-list.t-cost = h-list.t-cost.
    END. 
  END. 
  proz = 0. 
  t-proz = 0. 
  IF gsales NE 0 THEN proz = ncost / gsales * 100. 
  IF t-gsales NE 0 THEN t-proz = t-ncost / t-gsales * 100. 

  /* Naufal Afthar - 7FD6D0 -> add grand total for the last TOTAL row*/
  ASSIGN 
      dd-anz = dd-anz + t-anz
      dd-comanz = dd-comanz + t-comanz
      tm-anz = tm-anz + t-m-anz
      tm-comanz = tm-comanz + t-m-comanz.
 
  CREATE output-list. 
  ASSIGN
    output-list.bezeich = "T O T A L"
    output-list.sales = gsales
    output-list.ncost = ncost
    output-list.compli = gcompli
    output-list.cost = gcost
    output-list.proz = proz
    output-list.t-proz = t-proz
    output-list.anz         = t-anz       
    output-list.m-anz       = t-m-anz     
    output-list.comanz      = t-comanz    
    output-list.m-comanz    = t-m-comanz  
    output-list.anz-cost    = t-anz-cost  
    output-list.manz-cost   = t-manz-cost
  .
  IF t-gsales GE 0 THEN 
    ASSIGN
      output-list.t-sales = t-gsales
      output-list.t-ncost = t-ncost
      output-list.t-compli = t-gcompli
      output-list.t-cost = t-gcost.
  
  proz = 0. 
  t-proz = 0. 
  dd-ncost = dd-gcost - dd-gcompli. 
  IF dd-gsales NE 0 THEN proz = dd-ncost / dd-gsales * 100. 
  IF tot-gsales NE 0 THEN t-proz = tot-ncost / tot-gsales * 100. 

  CREATE output-list.
  ASSIGN
    output-list.bezeich = "GRAND TOTAL"
    output-list.sales = dd-gsales
    output-list.ncost = dd-ncost
    output-list.compli = dd-gcompli
    output-list.cost = dd-gcost
    output-list.proz = proz
    output-list.t-proz = t-proz
    /* Naufal Afthar - 7FD6D0 -> add grand total*/
    output-list.anz = dd-anz
    output-list.comanz = dd-comanz
    output-list.m-anz = tm-anz
    output-list.m-comanz = tm-comanz.
  IF tot-gsales GE 0 THEN
    ASSIGN
      output-list.t-sales = tot-gsales
      output-list.t-ncost = tot-ncost
      output-list.t-compli = tot-gcompli
      output-list.t-cost = tot-gcost.
END. 

PROCEDURE find-exrate: 
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO. 
  IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
    AND exrate.datum = curr-date NO-LOCK NO-ERROR. 
  ELSE FIND FIRST exrate WHERE exrate.datum = curr-date NO-LOCK NO-ERROR. 
END. 

