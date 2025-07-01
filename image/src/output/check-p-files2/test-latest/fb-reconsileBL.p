/*ft 08/01/15 penambahan coa description*/
/*DZ 17/09/24 pindah coa ke colomn 2*/
/*DZ 18/09/24 Perbaiki length data pada column 2*/
DEFINE TEMP-TABLE fbreconsile-list
    FIELD nr        AS INTEGER
    FIELD CODE      AS INTEGER
    FIELD bezeich   AS CHARACTER
    FIELD col1      AS CHARACTER    FORMAT "x(24)"
    FIELD col2      AS CHARACTER    FORMAT "x(50)"
    FIELD col3      AS CHARACTER    FORMAT "x(15)"
    FIELD col4      AS CHARACTER    FORMAT "x(15)"
    FIELD col5      AS CHARACTER    FORMAT "x(34)"
    .
  
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER case-type    AS INTEGER.    
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-grp     AS INTEGER.
DEFINE INPUT PARAMETER mi-opt       AS LOGICAL.
DEFINE INPUT PARAMETER date1        AS DATE.
DEFINE INPUT PARAMETER date2        AS DATE.
DEFINE OUTPUT PARAMETER done        AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR fbreconsile-list.


DEFINE WORKFILE s-list 
    FIELD code AS INTEGER 
    FIELD reihenfolge AS INTEGER INITIAL 1 /* 1 = food, 2 = beverage */ 
    FIELD lager-nr AS INTEGER 
    FIELD l-bezeich AS CHAR 
    FIELD fibukonto LIKE gl-acct.fibukonto 
    FIELD bezeich LIKE gl-acct.bezeich 
    FIELD flag AS INTEGER INITIAL 2  /* 0 cost, 5 = expense */ 
    FIELD anf-wert AS DECIMAL INITIAL 0 
    FIELD end-wert AS DECIMAL INITIAL 0 
    FIELD betrag AS DECIMAL INITIAL 0. 


DEFINE VARIABLE curr-nr         AS INTEGER NO-UNDO. 
DEFINE VARIABLE curr-reihe      AS INTEGER NO-UNDO. 

DEFINE VARIABLE ldry            AS INTEGER NO-UNDO. 
DEFINE VARIABLE dstore          AS INTEGER NO-UNDO. 
DEFINE VARIABLE long-digit      AS LOGICAL NO-UNDO. 

DEFINE VARIABLE foreign-nr      AS INTEGER NO-UNDO INITIAL 0. 
DEFINE VARIABLE exchg-rate      AS DECIMAL NO-UNDO INITIAL 1. 
DEFINE VARIABLE double-currency AS LOGICAL NO-UNDO INITIAL NO. 
 
DEFINE VARIABLE type-of-acct    AS INTEGER NO-UNDO. 
DEFINE VARIABLE counter         AS INTEGER NO-UNDO. 

DEFINE VARIABLE coa-format      AS CHARACTER NO-UNDO.
DEFINE VARIABLE f-date          AS DATE NO-UNDO.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "fb-reconsile". 

/***************************************************************************/
DEFINE buffer h-art FOR h-artikel. 
FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
ldry = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
dstore = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK.
coa-format = htparam.fchar.

FIND FIRST htparam WHERE paramnr = 240 NO-LOCK.  /* double currency flag */ 
IF htparam.flogical THEN 
DO: 
    double-currency = YES. 
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
    DO: 
        foreign-nr = waehrung.waehrungsnr. 
        exchg-rate = waehrung.ankauf / waehrung.einheit. 
    END. 
    ELSE exchg-rate = 1. 
END. 

IF case-type = 0 THEN RUN create-list. 
ELSE IF case-type = 1 THEN RUN create-food. 
ELSE IF case-type = 2 THEN RUN create-beverage. 

/*M
DISP case-type.
FOR EACH fbreconsile-list :
    DISP nr.
END.
*/

/***************************************************************************/

PROCEDURE create-list: 
DEFINE VARIABLE betrag1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag3 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag4 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag5 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag6 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag61 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag62 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag56 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE consume2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE flag AS INTEGER. 
 
DEFINE VARIABLE f-eknr AS INTEGER. 
DEFINE VARIABLE b-eknr AS INTEGER. 
DEFINE VARIABLE fl-eknr AS INTEGER. 
DEFINE VARIABLE bl-eknr AS INTEGER. 
 
DEFINE VARIABLE f-cost AS DECIMAL. 
DEFINE VARIABLE b-cost AS DECIMAL. 
DEFINE VARIABLE f-sales AS DECIMAL. 
DEFINE VARIABLE b-sales AS DECIMAL. 
DEFINE VARIABLE tf-sales AS DECIMAL. 
DEFINE VARIABLE tb-sales AS DECIMAL. 
DEFINE VARIABLE f-ratio AS DECIMAL. 
DEFINE VARIABLE b-ratio AS DECIMAL. 
 
DEFINE VARIABLE fibu AS CHAR. 
 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE amount AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE bev-food AS CHAR. 
DEFINE VARIABLE food-bev AS CHAR. 
 
/*M not used*/
DEFINE VARIABLE fb-str AS CHAR EXTENT 2 INITIAL 
  ["Beverage TO Food", "Food to Beverage"]. 
fb-str[1] = translateExtended ("Beverage to Food", lvCAREA, "":U). 
fb-str[2] = translateExtended ("Food to Beverage", lvCAREA, "":U). 

 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 

 
DEFINE VARIABLE qty1 AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE buffer l-oh FOR l-bestand. 
DEFINE buffer l-ohist FOR l-besthis. 
 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  FOR EACH fbreconsile-list: 
    DELETE fbreconsile-list. 
  END. 
 
  curr-nr = 0. 
  curr-reihe = 0. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
  fl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
  bl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE paramnr = 272 NO-LOCK. 
  bev-food = fchar. 
  FIND FIRST htparam WHERE paramnr = 275 NO-LOCK. 
  food-bev = fchar. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = bev-food NO-LOCK. 
  CREATE s-list. 
  s-list.reihenfolge = 1.      /** beverage TO food **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                     + CAPS(gl-acct.bezeich). /*ft 08/01/15*/
  s-list.flag = 0. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
  CREATE s-list. 
  s-list.reihenfolge = 2.       /** food TO beverage  **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                     + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
  s-list.flag = 0. 
 
  /*FOR EACH l-lager NO-LOCK:    FT serverless*/
    FOR EACH l-bestand /*WHERE l-bestand.lager-nr = l-lager.lager-nr*/ NO-LOCK,
      FIRST l-lager WHERE l-lager.lager-nr = l-bestand.lager-nr NO-LOCK,
      FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
      AND l-oh.lager-nr = 0 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
/*    IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN  */ 
      DO: 
/****** Indicator FOOD OR BEVERAGE ********/ 
        IF l-artikel.endkum = fl-eknr THEN flag = 1. 
        ELSE IF l-artikel.endkum = bl-eknr THEN flag = 2. 
 
        qty1 = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                - l-bestand.anz-ausgang. 
        qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
                - l-oh.anz-ausgang. 
        wert = l-oh.val-anf-best + l-oh.wert-eingang 
                - l-oh.wert-ausgang. 
 
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.reihenfolge = flag. 
          s-list.lager-nr = l-lager.lager-nr. 
          s-list.l-bezeich = l-lager.bezeich. 
          s-list.flag = 0.  /*** indicator FOR beginning onhand ***/ 
        END.       
        
        IF l-bestand.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-bestand.val-anf-best / l-bestand.anz-anf-best.               
        /*MT ORI!!
        IF l-oh.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-oh.val-anf-best / l-oh.anz-anf-best.
        */
        IF qty NE 0 THEN 
          s-list.end-wert = s-list.end-wert + wert * qty1 / qty.                
      END. 
    END.
 
/* receiving */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        /*AND l-op.artnr = l-artikel.artnr*/ AND l-op.op-art = 1 
        AND l-op.loeschflag LE 1 
        /*AND l-op.lager-nr = l-lager.lager-nr*/ NO-LOCK USE-INDEX artopart_ix,
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK
        BY l-op.lscheinnr: 
        IF l-artikel.endkum = fl-eknr THEN flag = 1. 
        ELSE IF l-artikel.endkum = bl-eknr THEN flag = 2. 
        /*FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
          AND l-ophdr.op-typ = "STI" NO-LOCK. */
        IF l-op.anzahl GE 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
            AND s-list.reihenfolge = flag AND s-list.flag = 11 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = flag.  /*** indicator FOR food OR beverage ***/ 
            s-list.lager-nr = l-lager.lager-nr. 
            s-list.l-bezeich = l-lager.bezeich. 
            s-list.flag = 11.   /*** indicator FOR receiving  ***/ 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
        ELSE IF l-op.anzahl LT 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
            AND s-list.reihenfolge = flag AND s-list.flag = 12 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = flag. 
            s-list.lager-nr = l-lager.lager-nr. 
            s-list.l-bezeich = l-lager.bezeich. 
            s-list.flag = 12.       /*** indicator FOR RETURN  ***/ 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
      END. 
 
/* consumed */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        /*AND l-op.artnr = l-artikel.artnr*/ AND l-op.loeschflag LE 1 
        AND l-op.op-art = 3 
        /*AND l-op.lager-nr = l-lager.lager-nr*/ NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK,
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK BY l-op.lscheinnr: 
        DO: 
          IF l-artikel.endkum = fl-eknr THEN flag = 1. 
          ELSE IF l-artikel.endkum = bl-eknr THEN flag = 2. 
          type-of-acct = gl-acct.acc-type. 
          fibukonto = gl-acct.fibukonto. 
          bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                    + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN 
            DO: 
              type-of-acct = gl-acct1.acc-type. 
              fibukonto = gl-acct1.fibukonto. 
              bezeich = STRING(gl-acct1.fibukonto, coa-format) + " " + CAPS(gl-acct1.bezeich).  /*ft 08/01/15*/
            END. 
          END. 

          IF flag = 1 AND fibukonto = food-bev THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.lager-nr = 9999 
              AND s-list.reihenfolge = 2. 
            s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
          END. 
          ELSE IF flag = 2 AND fibukonto = bev-food THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.lager-nr = 9999 
              AND s-list.reihenfolge = 1. 
            s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
          END. 
          ELSE 
          DO: 
            FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
              AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              s-list.reihenfolge = flag. 
              s-list.fibukonto = fibukonto. 
              s-list.bezeich = bezeich. 
              s-list.flag = 5.                  /*** expenses ***/ 
            END. 
            IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4  THEN 
              s-list.betrag = s-list.betrag + l-op.warenwert. 
          END. 
        END. 
      END. 
  /*  END. 
  END. */
 
/***  Less Food & Beverage Compliment  */ 
  /*FOR EACH hoteldpt WHERE hoteldpt.num NE ldry AND hoteldpt.num NE dstore 
    NO-LOCK BY hoteldpt.num: */
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date /*AND h-compli.departement = hoteldpt.num */
      AND h-compli.betriebsnr = 0
      AND h-compli.departement NE ldry
      AND h-compli.departement NE dstore NO-LOCK,
      FIRST hoteldpt WHERE hoteldpt.num = h-compli.departement NO-LOCK,
      FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
        /* BY h-compli.p-artnr */ BY h-compli.departement BY h-compli.rechnr: 
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
          AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        ELSE FIND FIRST exrate WHERE exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
 
      FIND FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
        AND artikel.departement = 0 NO-LOCK. 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK. 
      FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK. 
 
      FIND FIRST h-artikel WHERE h-artikel.departement = h-compli.departement 
        AND h-artikel.artnr = h-compli.artnr NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-artikel.departement NO-LOCK. 
 
      f-cost = 0. 
      b-cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        IF artikel.umsatzart = 6 THEN b-cost = h-compli.anzahl * h-cost.betrag. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * h-cost.betrag. 
          RUN cost-correction(INPUT-OUTPUT f-cost).
      END. 
      ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) 
      THEN DO: 
        IF artikel.umsatzart = 6 THEN 
          b-cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
      END.

      IF f-cost NE 0 THEN 
      DO: 
        IF mi-opt = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 1. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                             + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 1. 
            s-list.code = gl-main.code. 
            s-list.bezeich = gl-main.bezeich. 
            s-list.flag = 4. 
          END. 
        END. 
        s-list.betrag = s-list.betrag + f-cost. 
      END. 
 
      IF b-cost NE 0 THEN 
      DO: 
        IF mi-opt = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 2. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                             + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 2. 
            s-list.code = gl-main.code. 
            s-list.bezeich = gl-main.bezeich. 
            s-list.flag = 4. 
          END. 
        END. 
        s-list.betrag = s-list.betrag + b-cost. 
      END. 
    END. 
  /*END. */
 
  RUN fb-sales(f-eknr, b-eknr, OUTPUT tf-sales, OUTPUT tb-sales). 
 
/******************************  FOOD  ************************************/ 
  /*Naufal Afthar - BDFB55 -> expand format on >>>,>>>,>>9.99*/

  IF from-grp = 0 OR from-grp = 1 THEN 
  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
    fbreconsile-list.col2 = STRING(translateExtended("** FOOD **", lvCAREA, "":U), "x(50)"). 
    
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
 
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
    fbreconsile-list.col1 = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
    
    FOR EACH s-list WHERE s-list.flag = 0  /*** beginning onhand ***/ 
      AND s-list.reihenfolge = 1           /*** food ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag1 = betrag1 + s-list.anf-wert. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        .
        fbreconsile-list.col1 =  STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN
      DO:
      .
      fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
      fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
      END.
      ELSE 
      DO:
        .
        fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
        fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
      END. 
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    .
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
           fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
    ELSE                                                               
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
           fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9"). 
    
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
    
    fbreconsile-list.col1 = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 11  /*** incoming ***/ 
      AND s-list.reihenfolge = 1 NO-LOCK    /*** food     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        .
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      DO:
      .
      fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
      fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      END.
      ELSE 
      DO:
      .
      fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
      fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
      END.
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
    IF NOT long-digit THEN 
    DO:
        fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)").
        fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
        . 
        END.
    ELSE
    DO:
        fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)").
        fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9"). 
        .
    END.
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
    fbreconsile-list.col1 = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 12   /*** RETURN ***/ 
      AND s-list.reihenfolge = 1             /*** food   ***/ 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag3 = betrag3 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        .
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      DO:
        .
        fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
        fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      END.
      ELSE
      DO:
          .
        fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
        fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
      END.
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
    IF NOT long-digit THEN 
    DO: 
        fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)").
        fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
        .
    END.
    ELSE 
    DO: 
        fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)").
        fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9"). 
        . 
    END.
/* BEVERAGE TO FOOD */ 
    FIND FIRST s-list WHERE s-list.lager-nr = 9999 /*** bev TO food ***/ 
      AND s-list.reihenfolge = 1 no-lock.          /*** food ***/ 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
    IF NOT long-digit THEN 
    DO:
        fbreconsile-list.col1 = STRING(("4. " + fb-str[1]), "x(24)").
        fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
        fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
        .
    END.
    ELSE 
    DO:
        fbreconsile-list.col1 = STRING(("4. " + fb-str[1]), "x(24)"). 
        fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)").
        fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
        .
    END.
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    .
 
    betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    
    IF NOT long-digit THEN 
    DO:
        fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)").
        fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)").
        fbreconsile-list.col3 = STRING("", "x(15)").
        fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
    END.
    ELSE
    DO:
        fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)").
        fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)").
        fbreconsile-list.col3 = STRING("", "x(15)").
        fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9"). 
    END.
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    
    fbreconsile-list.col1 = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)").
    FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 1 
      AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag5 = betrag5 + s-list.end-wert. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")
             fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")
             fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9"). 
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    
    IF NOT long-digit THEN 
    DO:
    fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)").
    fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
    END.
    ELSE 
    DO:
    fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)").
    fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9"). 
    END.
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    
    betrag56 = betrag4 - betrag5. 
    IF NOT long-digit THEN 
    DO:
        fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)").
        fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)").
        fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
    END.
    ELSE
    DO:
        fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)").
        fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)").
        fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9"). 
    END.
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr.
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    
    fbreconsile-list.col1 = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
    IF mi-opt = NO THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        fbreconsile-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
        ELSE fbreconsile-list.code = counter. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)")
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)")
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    IF mi-opt = NO THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 

      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
       
      fbreconsile-list.col1 = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        fbreconsile-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
        ELSE fbreconsile-list.code = counter. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
    
/*  LESS FOOD TO BEVERAGE */ 
    FIND FIRST s-list WHERE s-list.reihenfolge = 2 AND s-list.lager-nr = 9999. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING("", "x(24)"). 
    IF NOT long-digit THEN 
        ASSIGN  fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")   /*ft 08/01/15*/
                fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")    /*ft 08/01/15*/
                fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
    betrag6 = betrag6 + s-list.anf-wert. 
 
    IF mi-opt = NO THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      
     
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
   
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
           fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
           fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9"). 
    END.
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    consume2 = betrag56 - betrag6. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
     
    IF NOT long-digit THEN 
    DO:
        ASSIGN  fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)")
                fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)")
                fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9.99"). 
    END.
    ELSE
    DO:
        ASSIGN  fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)")
                fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)")
                fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9"). 
    END.
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
     
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    f-ratio = 0. 
    IF tf-sales NE 0 THEN f-ratio = ROUND(consume2, 2) / ROUND(tf-sales, 2) * 100. 
    IF f-ratio = ? THEN f-ratio = 0.

    IF NOT long-digit THEN 
    ASSIGN  fbreconsile-list.col1 = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
            fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tf-sales, "->,>>>,>>>,>>9.99") 
            fbreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)")
            fbreconsile-list.col4 = STRING(f-ratio,"->,>>>,>>9.99 %"). 
    ELSE 
    ASSIGN  fbreconsile-list.col1 = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
            fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tf-sales, " ->>>,>>>,>>>,>>9") 
            fbreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)")
            fbreconsile-list.col4 = STRING(f-ratio,"->,>>>,>>9.99 %"). 
  END. 
  IF from-grp = 1 THEN RETURN. 
 
/******************************  BEVERAGE  **********************************/ 
  /*Naufal Afthar - BDFB55 -> expand format on >>>,>>>,>>9.99*/

  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col2 = STRING(translateExtended ("** BEVERAGE **", lvCAREA, "":U), "x(50)"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
  i = 0. 
  CREATE fbreconsile-list. 
  betrag1 = 0. 
  
  fbreconsile-list.col1 = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.anf-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag1 = betrag1 + s-list.anf-wert. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN  fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")
            fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN  fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")
            fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
         fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
         fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9"). 
 
  i = 0. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
  fbreconsile-list.col1 = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
  betrag2 = 0. 
  FOR EACH s-list WHERE s-list.flag = 11 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag2 = betrag2 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN  fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
            fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN  fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
            fbreconsile-list.col3 =  STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + translateExtended ("SUB TOTAL", lvCAREA, "":U)
         fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9"). 
 
  i = 0. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr.
  
  fbreconsile-list.col1 = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
  betrag3 = 0. 
  FOR EACH s-list WHERE s-list.flag = 12 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag3 = betrag3 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col4 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col4 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9"). 
 
/*  FOOD TO BEVERAGE  */ 
  FIND FIRST s-list WHERE s-list.lager-nr = 9999 
    AND s-list.reihenfolge = 2 NO-LOCK. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(("4. " + fb-str[2]), "x(24)") 
         fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
         fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(("4. " + fb-str[2]), "x(24)") 
         fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
         fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
 
  betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9"). 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  
 
  i = 0. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)"). 
  betrag5 = 0. 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag5 = betrag5 + s-list.end-wert. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  betrag56 = betrag4 - betrag5. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col1 = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
  betrag6 = 0. 
  IF mi-opt = NO THEN 
  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
    betrag6 = betrag6 + s-list.betrag. 
    counter = counter + 1. 
    IF counter GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      fbreconsile-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
      ELSE fbreconsile-list.code = counter. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
 
  IF mi-opt = NO THEN 
  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.lager-nr: 
    counter = counter + 1. 
    betrag6 = betrag6 + s-list.betrag. 
    IF counter GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      fbreconsile-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
      ELSE fbreconsile-list.code = counter. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
 
/*  BEVERAGE TO FOOD */ 
  FIND FIRST s-list WHERE s-list.reihenfolge = 1 
    AND s-list.lager-nr = 9999. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col1 = STRING("", "x(24)"). 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")  /*ft 08/01/15*/
         fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")  /*ft 08/01/15*/
         fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
  betrag6 = betrag6 + s-list.anf-wert. 
 
  IF mi-opt = NO THEN 
  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
  END. 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9"). 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  consume2 = betrag56 - betrag6. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)") 
         fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)") 
         fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  b-ratio = 0. 
  IF tb-sales NE 0 THEN b-ratio = consume2 / tb-sales * 100. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tb-sales, "->,>>>,>>>,>>9.99") 
         fbreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
         fbreconsile-list.col4 = STRING(b-ratio,"->,>>>,>>9.99 %"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tb-sales, " ->>>,>>>,>>>,>>9")
         fbreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
         fbreconsile-list.col4 = STRING(b-ratio,"->,>>>,>>9.99 %"). 
  done = YES. 
END. 
 

PROCEDURE create-food: 
DEFINE VARIABLE betrag1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag3 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag4 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag5 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag6 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag61 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag62 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag56 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE consume2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE flag AS INTEGER. 
 
DEFINE VARIABLE f-eknr AS INTEGER. 
DEFINE VARIABLE b-eknr AS INTEGER. 
DEFINE VARIABLE fl-eknr AS INTEGER. 
DEFINE VARIABLE bl-eknr AS INTEGER. 
 
DEFINE VARIABLE f-cost AS DECIMAL. 
DEFINE VARIABLE b-cost AS DECIMAL. 
DEFINE VARIABLE f-sales AS DECIMAL. 
DEFINE VARIABLE b-sales AS DECIMAL. 
DEFINE VARIABLE tf-sales AS DECIMAL. 
DEFINE VARIABLE tb-sales AS DECIMAL. 
DEFINE VARIABLE f-ratio AS DECIMAL. 
DEFINE VARIABLE b-ratio AS DECIMAL. 
 
DEFINE VARIABLE fibu AS CHAR. 
 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE amount AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE bev-food AS CHAR. 
DEFINE VARIABLE food-bev AS CHAR. 
 
DEFINE VARIABLE fb-str AS CHAR EXTENT 2 INITIAL 
  ["Beverage TO Food", "Food to Beverage"]. 
fb-str[1] = translateExtended ("Beverage to Food", lvCAREA, "":U). 
fb-str[2] = translateExtended ("Food to Beverage", lvCAREA, "":U). 
 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE buffer h-art FOR h-artikel. 
 
DEFINE VARIABLE qty1 AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE buffer l-oh FOR l-bestand. 
 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  curr-nr = 0. 
  curr-reihe = 0. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
  fl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
  bl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE paramnr = 272 NO-LOCK. 
  bev-food = fchar. 
  FIND FIRST htparam WHERE paramnr = 275 NO-LOCK. 
  food-bev = fchar. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = bev-food NO-LOCK. 
  CREATE s-list. 
  s-list.reihenfolge = 1.      /** beverage TO food **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                     + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
  s-list.flag = 0. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
  CREATE s-list. 
  s-list.reihenfolge = 2.       /** food TO beverage  **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                     + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
  s-list.flag = 0. 
  flag = 1. 
  
  FOR EACH l-lager NO-LOCK: 
    FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
      FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
      AND l-oh.lager-nr = 0 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      AND /*l-artikel.endkum = fl-eknr*/ (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
/*    IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN */ 
      DO: 
        
         /*test ita*/
        IF l-artikel.endkum = fl-eknr THEN flag = 1. 
        ELSE IF l-artikel.endkum = bl-eknr THEN flag = 2. 
 
        qty1 = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                - l-bestand.anz-ausgang. 
        qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
                - l-oh.anz-ausgang. 
        wert = l-oh.val-anf-best + l-oh.wert-eingang 
                - l-oh.wert-ausgang. 
 
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.reihenfolge = flag. 
          s-list.lager-nr = l-lager.lager-nr. 
          s-list.l-bezeich = l-lager.bezeich. 
          s-list.flag = 0.  /*** indicator FOR beginning onhand ***/ 
        END. 
        /*IF l-oh.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-oh.val-anf-best / l-oh.anz-anf-best.*/
        IF l-bestand.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-bestand.val-anf-best / l-bestand.anz-anf-best.

        IF qty NE 0 THEN  s-list.end-wert = s-list.end-wert + wert * qty1 / qty. 
      END. 
 
/* receiving */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr = l-artikel.artnr AND l-op.op-art = 1 
        AND l-op.loeschflag LE 1 
        AND l-op.lager-nr = l-lager.lager-nr NO-LOCK USE-INDEX artopart_ix 
        BY l-op.lscheinnr: 
        FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
          AND l-ophdr.op-typ = "STI" NO-LOCK NO-ERROR. 
        IF l-op.anzahl GE 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
            AND s-list.reihenfolge = flag AND s-list.flag = 11 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = flag.  /*** indicator FOR food OR beverage ***/ 
            s-list.lager-nr = l-lager.lager-nr. 
            s-list.l-bezeich = l-lager.bezeich. 
            s-list.flag = 11.   /*** indicator FOR receiving  ***/ 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
        ELSE IF l-op.anzahl LT 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
            AND s-list.reihenfolge = flag AND s-list.flag = 12 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = flag. 
            s-list.lager-nr = l-lager.lager-nr. 
            s-list.l-bezeich = l-lager.bezeich. 
            s-list.flag = 12.       /*** indicator FOR RETURN  ***/ 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
      END. 
 
/* consumed */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr = l-artikel.artnr AND l-op.loeschflag LE 1 
        AND l-op.op-art = 3 /*AND l-op.pos GT 0 */
        AND l-op.lager-nr = l-lager.lager-nr NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
          AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
           NO-LOCK BY l-op.lscheinnr: 
        DO: 
          type-of-acct = gl-acct.acc-type. 
          FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK. 
          fibukonto = gl-acct.fibukonto. 
          bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                    + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN 
            DO: 
              type-of-acct = gl-acct1.acc-type. 
              fibukonto = gl-acct1.fibukonto. 
              bezeich = STRING(gl-acct1.fibukonto, coa-format) + " " + CAPS(gl-acct1.bezeich).  /*ft 08/01/15*/
              FIND FIRST gl-main WHERE gl-main.nr = gl-acct1.main-nr NO-LOCK. 
            END. 
          END. 
 
          /*IF fibukonto = food-bev THEN. 
          ELSE IF fibukonto = bev-food THEN.*/

          IF flag = 1 AND fibukonto = food-bev THEN 
          DO: 
              
            FIND FIRST s-list WHERE s-list.lager-nr = 9999 
              AND s-list.reihenfolge = 2. 
            s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
          END. 
          ELSE IF flag = 2 AND fibukonto = bev-food THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.lager-nr = 9999 
              AND s-list.reihenfolge = 1. 
            s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
          END. 
          ELSE 
          DO: 
            IF mi-opt = NO THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
                AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                CREATE s-list. 
                s-list.reihenfolge = flag. 
                s-list.fibukonto = fibukonto. 
                s-list.bezeich = bezeich. 
                s-list.flag = 5.                  /*** expenses ***/ 
              END. 
            END. 
            ELSE 
            DO: 
              FIND FIRST s-list WHERE s-list.code = gl-main.code 
                AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                CREATE s-list. 
                s-list.reihenfolge = flag. 
                s-list.code = gl-main.code. 
                s-list.bezeich = gl-main.bezeich. 
                s-list.flag = 5.                  /*** expenses ***/ 
              END. 
            END. 
            IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4  THEN 
              s-list.betrag = s-list.betrag + l-op.warenwert.
          END. 
        END. 
      END. 
    END. 
  END.   
 
/*** food TO beverage - baverage TO food **
 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
    AND (l-op.stornogrund = bev-food OR l-op.stornogrund = food-bev) 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK,
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
    FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK BY l-op.lscheinnr : 
    
    IF gl-acct.fibukonto = food-bev THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.lager-nr = 9999 
        AND s-list.reihenfolge = 2. 
      s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
    END. 
    ELSE IF gl-acct.fibukonto = bev-food THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.lager-nr = 9999 
        AND s-list.reihenfolge = 1. 
      s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
    END. 
  END. */ 
 
/***  Less Food & Beverage Compliment  */ 
  FOR EACH hoteldpt WHERE hoteldpt.num NE ldry AND hoteldpt.num NE dstore 
    NO-LOCK BY hoteldpt.num: 
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
 
      FIND FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
        AND artikel.departement = 0 NO-LOCK. 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK. 
      FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK. 
  
      FIND FIRST h-artikel WHERE h-artikel.departement = h-compli.departement 
        AND h-artikel.artnr = h-compli.artnr NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-artikel.departement NO-LOCK. 
 
      f-cost = 0. 
      b-cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        IF artikel.umsatzart = 6 THEN b-cost = h-compli.anzahl * h-cost.betrag. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * h-cost.betrag. 
          RUN cost-correction(INPUT-OUTPUT f-cost).
      END. 
      ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) 
      THEN DO: 
        IF artikel.umsatzart = 6 THEN 
          b-cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
      END. 
 
      IF f-cost NE 0 THEN 
      DO: 
        IF mi-opt = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 1. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                             + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 1. 
            s-list.code = gl-main.code. 
            s-list.bezeich = gl-main.bezeich. 
            s-list.flag = 4. 
          END. 
        END. 
        s-list.betrag = s-list.betrag + f-cost. 
      END. 
    END. 
  END. 
 
  RUN fb-sales(f-eknr, b-eknr, OUTPUT tf-sales, OUTPUT tb-sales). 
 
/******************************  FOOD  ************************************/ 
  /*Naufal Afthar - BDFB55 -> expand format on >>>,>>>,>>9.99*/

  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col2 = STRING(translateExtended ("** FOOD **", lvCAREA, "":U), "x(50)"). 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
 
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 0  /*** beginning onhand ***/ 
      AND s-list.reihenfolge = 1           /*** food ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag1 = betrag1 + s-list.anf-wert. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99").
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    DO:
        ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
               fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
    END.
    ELSE
    DO:
        ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
               fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9"). 
    END.
 
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 11  /*** incoming ***/ 
      AND s-list.reihenfolge = 1 NO-LOCK    /*** food     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 12   /*** RETURN ***/ 
      AND s-list.reihenfolge = 1             /*** food   ***/ 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag3 = betrag3 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9"). 
 
/* BEVERAGE TO FOOD */ 
    FIND FIRST s-list WHERE s-list.lager-nr = 9999 /*** bev TO food ***/ 
      AND s-list.reihenfolge = 1 no-lock.          /*** food ***/ 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col1 = STRING(("4. " + fb-str[1]), "x(24)") 
           fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col1 = STRING(("4. " + fb-str[1]), "x(24)") 
         fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
 
    betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)") 
           fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)") 
           fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9"). 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
 
    i = 0. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 1 
      AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag5 = betrag5 + s-list.end-wert. 
      IF i GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        curr-nr = curr-nr + 1. 
        fbreconsile-list.nr = curr-nr. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9"). 
    END. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9"). 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    betrag56 = betrag4 - betrag5. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)") 
           fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)") 
           fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9"). 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
    IF mi-opt = NO THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        fbreconsile-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
        ELSE fbreconsile-list.code = counter. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    IF mi-opt = NO THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        CREATE fbreconsile-list. 
        fbreconsile-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
        ELSE fbreconsile-list.code = counter. 
        fbreconsile-list.col1 = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)")  
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)")  
             fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
/*  LESS FOOD TO BEVERAGE */ 
    FIND FIRST s-list WHERE s-list.reihenfolge = 2 AND s-list.lager-nr = 9999. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING("", "x(24)"). 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
    betrag6 = betrag6 + s-list.anf-wert. 
 
    IF mi-opt = NO THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
    END. 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
           fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9"). 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
 
    consume2 = betrag56 - betrag6. 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)") 
           fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)") 
           fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9"). 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    f-ratio = 0. 
    IF tf-sales NE 0 THEN f-ratio = ROUND(consume2, 2) / ROUND(tf-sales, 2) * 100. 
    IF f-ratio = ? THEN f-ratio = 0.

    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tf-sales, "->,>>>,>>>,>>9.99") 
           fbreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
           fbreconsile-list.col4 = STRING(f-ratio,"->,>>>,>>9.99 %"). 
    ELSE 
    ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
           fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tf-sales, " ->>>,>>>,>>>,>>9") 
           fbreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
           fbreconsile-list.col4 = STRING(f-ratio,"->,>>>,>>9.99 %"). 
  END. 
  done = YES. 
END. 
 
PROCEDURE create-beverage: 
DEFINE VARIABLE betrag1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag3 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag4 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag5 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag6 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag61 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag62 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE betrag56 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE consume2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE flag AS INTEGER. 
 
DEFINE VARIABLE f-eknr AS INTEGER. 
DEFINE VARIABLE b-eknr AS INTEGER. 
DEFINE VARIABLE fl-eknr AS INTEGER. 
DEFINE VARIABLE bl-eknr AS INTEGER. 
 
DEFINE VARIABLE f-cost AS DECIMAL. 
DEFINE VARIABLE b-cost AS DECIMAL. 
DEFINE VARIABLE f-sales AS DECIMAL. 
DEFINE VARIABLE b-sales AS DECIMAL. 
DEFINE VARIABLE tf-sales AS DECIMAL. 
DEFINE VARIABLE tb-sales AS DECIMAL. 
DEFINE VARIABLE f-ratio AS DECIMAL. 
DEFINE VARIABLE b-ratio AS DECIMAL. 
 
DEFINE VARIABLE fibu AS CHAR. 
 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE amount AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE bev-food AS CHAR. 
DEFINE VARIABLE food-bev AS CHAR. 
 
DEFINE VARIABLE fb-str AS CHAR EXTENT 2 INITIAL 
  ["Beverage TO Food", "Food to Beverage"]. 
fb-str[1] = translateExtended ("Beverage to Food", lvCAREA, "":U). 
fb-str[2] = translateExtended ("Food to Beverage", lvCAREA, "":U). 
 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE buffer h-art FOR h-artikel. 
 
DEFINE VARIABLE qty1 AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE buffer l-oh FOR l-bestand. 
 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
  FOR EACH fbreconsile-list: 
    delete fbreconsile-list. 
  END. 
 
  curr-nr = 0. 
  curr-reihe = 0. 
 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
  fl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
  bl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST htparam WHERE paramnr = 272 NO-LOCK. 
  bev-food = fchar. 
  FIND FIRST htparam WHERE paramnr = 275 NO-LOCK. 
  food-bev = fchar. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = bev-food NO-LOCK. 
  CREATE s-list. 
  s-list.reihenfolge = 1.      /** beverage TO food **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                    + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
  s-list.flag = 0. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
  CREATE s-list. 
  s-list.reihenfolge = 2.       /** food TO beverage  **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                     + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
  s-list.flag = 0. 
 
  flag = 2. 
  FOR EACH l-lager NO-LOCK: 
    FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
      FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
      AND l-oh.lager-nr = 0 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      AND /*l-artikel.endkum = bl-eknr */ (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
/*    IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN  */ 
      DO: 

        IF l-artikel.endkum = fl-eknr THEN flag = 1. 
        ELSE IF l-artikel.endkum = bl-eknr THEN flag = 2. 
 
        qty1 = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                - l-bestand.anz-ausgang. 
        qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
                - l-oh.anz-ausgang. 
        wert = l-oh.val-anf-best + l-oh.wert-eingang 
                - l-oh.wert-ausgang. 
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          s-list.reihenfolge = flag. 
          s-list.lager-nr = l-lager.lager-nr. 
          s-list.l-bezeich = l-lager.bezeich. 
          s-list.flag = 0.  /*** indicator FOR beginning onhand ***/ 
        END. 
        
        /*
        IF l-oh.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-oh.val-anf-best / l-oh.anz-anf-best. */

        IF l-bestand.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-bestand.val-anf-best / l-bestand.anz-anf-best.

/*      s-list.anf-wert = s-list.anf-wert + l-bestand.val-anf-best.  */ 
        IF qty NE 0 THEN s-list.end-wert = s-list.end-wert + wert * qty1 / qty. 
      END. 
 
/* receiving */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr = l-artikel.artnr AND l-op.op-art = 1 
        AND l-op.loeschflag LE 1 
        AND l-op.lager-nr = l-lager.lager-nr NO-LOCK USE-INDEX artopart_ix 
        BY l-op.lscheinnr: 
        FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
          AND l-ophdr.op-typ = "STI" NO-LOCK NO-ERROR. 
        IF l-op.anzahl GE 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
            AND s-list.reihenfolge = flag AND s-list.flag = 11 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = flag.  /*** indicator FOR food OR beverage ***/ 
            s-list.lager-nr = l-lager.lager-nr. 
            s-list.l-bezeich = l-lager.bezeich. 
            s-list.flag = 11.   /*** indicator FOR receiving  ***/ 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
        ELSE IF l-op.anzahl LT 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
            AND s-list.reihenfolge = flag AND s-list.flag = 12 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = flag. 
            s-list.lager-nr = l-lager.lager-nr. 
            s-list.l-bezeich = l-lager.bezeich. 
            s-list.flag = 12.       /*** indicator FOR RETURN  ***/ 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
      END. 
 
/* consumed */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr = l-artikel.artnr AND l-op.loeschflag LE 1 
        AND l-op.op-art = 3 
        AND l-op.lager-nr = l-lager.lager-nr NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
          AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
          NO-LOCK BY l-op.lscheinnr: 
        DO: 
          type-of-acct = gl-acct.acc-type. 
          FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK. 
          fibukonto = gl-acct.fibukonto. 
          bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                    + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
          
          IF l-op.stornogrund NE "" THEN 
          DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN 
            DO: 
              type-of-acct = gl-acct1.acc-type. 
              FIND FIRST gl-main WHERE gl-main.nr = gl-acct1.main-nr NO-LOCK. 
              fibukonto = gl-acct1.fibukonto. 
              bezeich = STRING(gl-acct1.fibukonto, coa-format) + " " + CAPS(gl-acct1.bezeich).  /*ft 08/01/15*/
            END. 
          END. 
           
          /*IF fibukonto = food-bev THEN. 
          ELSE IF fibukonto = bev-food THEN. */
          IF flag = 1 AND fibukonto = food-bev THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.lager-nr = 9999 
              AND s-list.reihenfolge = 2. 
            s-list.anf-wert = s-list.anf-wert + l-op.warenwert.
          END. 
          ELSE IF flag = 2 AND fibukonto = bev-food THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.lager-nr = 9999 
              AND s-list.reihenfolge = 1. 
            s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
          END. 
          ELSE 
          DO: 
            IF mi-opt = NO THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
                AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                CREATE s-list. 
                s-list.reihenfolge = flag. 
                s-list.fibukonto = fibukonto. 
                s-list.bezeich = bezeich. 
                s-list.flag = 5.                  /*** expenses ***/ 
              END. 
            END. 
            ELSE 
            DO: 
              FIND FIRST s-list WHERE s-list.code = gl-main.code 
                AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                CREATE s-list. 
                s-list.reihenfolge = flag. 
                s-list.code = gl-main.code. 
                s-list.bezeich = gl-main.bezeich. 
                s-list.flag = 5.                  /*** expenses ***/ 
              END. 
            END. 
            IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4  THEN 
              s-list.betrag = s-list.betrag + l-op.warenwert. 
          END. 
        END. 
      END. 
    END. 
  END. 
 
/*** food TO beverage - beverage TO food ***/ 
  /*FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
    AND (l-op.stornogrund = bev-food OR l-op.stornogrund = food-bev) 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK,
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
    FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK BY l-op.lscheinnr :

    IF gl-acct.fibukonto = food-bev THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.lager-nr = 9999 
        AND s-list.reihenfolge = 2. 
      s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
    END. 
    ELSE IF gl-acct.fibukonto = bev-food THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.lager-nr = 9999 
        AND s-list.reihenfolge = 1. 
      s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
    END. 
  END. */
 
/***  Less Food & Beverage Compliment  */ 
  FOR EACH hoteldpt WHERE hoteldpt.num NE ldry AND hoteldpt.num NE dstore 
    NO-LOCK BY hoteldpt.num: 
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
 
      FIND FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
        AND artikel.departement = 0 NO-LOCK. 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK. 
      FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK. 
 
      FIND FIRST h-artikel WHERE h-artikel.departement = h-compli.departement 
        AND h-artikel.artnr = h-compli.artnr NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-artikel.departement NO-LOCK. 
 
      f-cost = 0. 
      b-cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
      DO: 
        IF artikel.umsatzart = 6 THEN b-cost = h-compli.anzahl * h-cost.betrag. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * h-cost.betrag. 
          RUN cost-correction(INPUT-OUTPUT f-cost).
      END. 
      ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) 
      THEN DO: 
        IF artikel.umsatzart = 6 THEN 
        b-cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
      END. 
 
      IF b-cost NE 0 THEN 
      DO: 
        IF mi-opt = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 2. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                             + CAPS(gl-acct.bezeich).  /*ft 08/01/15*/
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.reihenfolge = 2. 
            s-list.code = gl-main.code. 
            s-list.bezeich = gl-main.bezeich. 
            s-list.flag = 4. 
          END. 
        END. 
        s-list.betrag = s-list.betrag + b-cost. 
      END. 
    END. 
  END. 
 
  RUN fb-sales(f-eknr, b-eknr, OUTPUT tf-sales, OUTPUT tb-sales). 
 
/******************************  BEVERAGE  **********************************/ 
  /*Naufal Afthar - BDFB55 -> expand format on >>>,>>>,>>9.99*/

  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col2 = STRING(translateExtended ("** BEVERAGE **", lvCAREA, "":U), "x(50)"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  i = 0. 
  CREATE fbreconsile-list. 
  betrag1 = 0. 
  fbreconsile-list.col1 = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.anf-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag1 = betrag1 + s-list.anf-wert. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag1, "->>,>>>,>>>,>>9"). 
 
  i = 0. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col1 = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
  betrag2 = 0. 
  FOR EACH s-list WHERE s-list.flag = 11 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag2 = betrag2 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag2, "->>,>>>,>>>,>>9"). 
 
  i = 0. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col1 = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
  betrag3 = 0. 
  FOR EACH s-list WHERE s-list.flag = 12 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag3 = betrag3 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag3, "->>,>>>,>>>,>>9"). 
 
/*  FOOD TO BEVERAGE  */ 
  FIND FIRST s-list WHERE s-list.lager-nr = 9999 
    AND s-list.reihenfolge = 2 NO-LOCK. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(("4. " + fb-str[2]), "x(24)") 
         fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")
         fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(("4. " + fb-str[2]), "x(24)") 
         fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)")
         fbreconsile-list.col4 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(1 + 2 + 3 + 4)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag4, "->>,>>>,>>>,>>9"). 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  i = 0. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col1 = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)"). 
  betrag5 = 0. 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag5 = betrag5 + s-list.end-wert. 
    IF i GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      curr-nr = curr-nr + 1. 
      fbreconsile-list.nr = curr-nr. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.end-wert, "->>,>>>,>>>,>>9"). 
  END. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag5, "->>,>>>,>>>,>>9"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  betrag56 = betrag4 - betrag5. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(5 - 6)", "x(50)") 
         fbreconsile-list.col4 = STRING(betrag56, "->>,>>>,>>>,>>9"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col1 = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
  betrag6 = 0. 
  IF mi-opt = NO THEN 
  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
    betrag6 = betrag6 + s-list.betrag. 
    counter = counter + 1. 
    IF counter GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      fbreconsile-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
      ELSE fbreconsile-list.code = counter. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
 
  IF mi-opt = NO THEN 
  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
    fbreconsile-list.col1 = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.lager-nr: 
    counter = counter + 1. 
    betrag6 = betrag6 + s-list.betrag. 
    IF counter GT 1 THEN 
    DO: 
      CREATE fbreconsile-list. 
      fbreconsile-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN fbreconsile-list.code = s-list.code. 
      ELSE fbreconsile-list.code = counter. 
      fbreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN fbreconsile-list.col2 = STRING(s-list.bezeich, "x(50)") 
           fbreconsile-list.col3 = STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
  END. 
 
/*  BEVERAGE TO FOOD */ 
  FIND FIRST s-list WHERE s-list.reihenfolge = 1 
    AND s-list.lager-nr = 9999. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  fbreconsile-list.col1 = STRING("", "x(24)"). 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
         fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING(s-list.l-bezeich, "x(50)") 
         fbreconsile-list.col3 = STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
  betrag6 = betrag6 + s-list.anf-wert. 
 
  IF mi-opt = NO THEN 
  DO: 
    CREATE fbreconsile-list. 
    curr-nr = curr-nr + 1. 
    fbreconsile-list.nr = curr-nr. 
  END. 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         fbreconsile-list.col4 = STRING(betrag6, "->>,>>>,>>>,>>9"). 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  consume2 = betrag56 - betrag6. 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)") 
         fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("(7 - 8)", "x(50)") 
         fbreconsile-list.col4 = STRING(consume2,"->>,>>>,>>>,>>9"). 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
 
  CREATE fbreconsile-list. 
  curr-nr = curr-nr + 1. 
  fbreconsile-list.nr = curr-nr. 
  b-ratio = 0. 
  IF tb-sales NE 0 THEN b-ratio = consume2 / tb-sales * 100. 
  IF NOT long-digit THEN 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tb-sales, "->,>>>,>>>,>>9.99") 
         fbreconsile-list.col3 = STRING("     Cost:Sales", "x(15)") 
         fbreconsile-list.col4 = STRING(b-ratio,"->,>>>,>>9.99 %"). 
  ELSE 
  ASSIGN fbreconsile-list.col1 = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
         fbreconsile-list.col2 = STRING("", "x(16)") + STRING(tb-sales, " ->>>,>>>,>>>,>>9") 
         fbreconsile-list.col3 = STRING("     Cost:Sales", "x(15)") 
         fbreconsile-list.col4 = STRING(b-ratio,"->,>>>,>>9.99 %"). 
 
  done = YES. 
END. 


/**** F&B Sales ****/ 
PROCEDURE fb-sales: 
DEFINE INPUT PARAMETER f-eknr    AS INTEGER. 
DEFINE INPUT PARAMETER b-eknr    AS INTEGER. 
DEFINE OUTPUT PARAMETER tf-sales AS DECIMAL. 
DEFINE OUTPUT PARAMETER tb-sales AS DECIMAL. 
 
DEFINE VARIABLE f-sales     AS DECIMAL. 
DEFINE VARIABLE b-sales     AS DECIMAL. 
DEFINE VARIABLE h-service   AS DECIMAL. 
DEFINE VARIABLE h-mwst      AS DECIMAL. 
DEFINE VARIABLE vat2        AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact        AS DECIMAL NO-UNDO.
DEFINE VARIABLE amount      AS DECIMAL. 
DEFINE VARIABLE serv-taxable AS LOGICAL. 

    f-sales = 0. 
    b-sales = 0. 
    tf-sales = 0. 
    tb-sales = 0. 
    FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
    serv-taxable = htparam.flogical. 
    
    FOR EACH hoteldpt WHERE hoteldpt.num NE ldry AND hoteldpt.num NE dstore 
        NO-LOCK BY hoteldpt.num: 
        FOR EACH artikel WHERE artikel.artart = 0 
            AND artikel.departement = hoteldpt.num 
            AND (artikel.endkum = f-eknr OR artikel.endkum = b-eknr 
                 OR artikel.umsatzart = 3 OR artikel.umsatzart = 5 
                 OR artikel.umsatzart = 6) NO-LOCK: 
            FOR EACH umsatz WHERE umsatz.datum GE date1 
                AND umsatz.datum LE date2 
                AND umsatz.departement = artikel.departement 
                AND umsatz.artnr = artikel.artnr NO-LOCK: 
/*
                h-service = 0. 
                h-mwst = 0. 
                RUN calc-servvat.p(artikel.departement, artikel.artnr, 
                                   umsatz.datum, artikel.service-code, 
                                   artikel.mwst-code, 
                                   OUTPUT h-service, OUTPUT h-mwst).
*/
/* SY AUG 13 2017 */
                RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                    umsatz.datum, OUTPUT h-service, OUTPUT h-mwst, 
                    OUTPUT vat2, OUTPUT fact).
                ASSIGN h-mwst = h-mwst + vat2.

                amount = umsatz.betrag / fact. 
                IF artikel.endkum = f-eknr OR artikel.umsatzart = 3 
                    OR artikel.umsatzart = 5 THEN 
                DO: 
                    IF umsatz.datum = date2 THEN f-sales = f-sales + amount. 
                    tf-sales = tf-sales + amount. 
                END. 
                ELSE IF artikel.endkum = b-eknr OR artikel.umsatzart = 6 THEN 
                DO: 
                    IF umsatz.datum = date2 THEN b-sales = b-sales + amount. 
                    tb-sales = tb-sales + amount. 
                END. 
            END. 
        END. 
    END. 
END.

PROCEDURE cost-correction: /*ragung 041865*/
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

