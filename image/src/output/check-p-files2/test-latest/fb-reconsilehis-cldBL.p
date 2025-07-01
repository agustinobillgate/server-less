
DEFINE TEMP-TABLE output-list 
  FIELD nr AS INTEGER 
  FIELD code AS INTEGER 
  FIELD bezeich AS CHAR 
  FIELD s AS CHAR.
DEFINE TEMP-TABLE s-list
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

DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER from-grp AS INT.
DEF INPUT PARAMETER food AS INT.
DEF INPUT PARAMETER bev AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER ldry AS INTEGER. 
DEF INPUT PARAMETER dstore AS INTEGER. 
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER foreign-nr AS INT.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER mi-opt-chk AS LOGICAL.
DEF INPUT PARAMETER date1 AS DATE.
DEF INPUT PARAMETER date2 AS DATE.
DEF OUTPUT PARAMETER done AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER TABLE FOR output-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fb-reconsilehis".

DEFINE VARIABLE type-of-acct AS INTEGER NO-UNDO.
DEFINE VARIABLE counter AS INTEGER.
DEFINE VARIABLE curr-nr AS INTEGER. 
DEFINE VARIABLE curr-reihe AS INTEGER. 
DEFINE VARIABLE coa-format AS CHARACTER NO-UNDO.
DEFINE VARIABLE betrag AS DECIMAL.

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK.
coa-format = htparam.fchar.

IF from-grp = 0 THEN RUN create-list. 
ELSE IF from-grp = food THEN RUN create-food. 
ELSE IF from-grp = bev THEN RUN create-beverage.

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

DEFINE buffer l-oh FOR l-besthis. 
 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
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
  create s-list. 
  s-list.reihenfolge = 1.      /** beverage TO food **/ 
  s-list.lager-nr = 9999. 
 s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                   + CAPS(gl-acct.bezeich). 
  s-list.flag = 0. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
  create s-list. 
  s-list.reihenfolge = 2.       /** food TO beverage  **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                   + CAPS(gl-acct.bezeich).  
  s-list.flag = 0. 
 
  /*FOR EACH l-lager NO-LOCK: */
    FOR EACH l-besthis WHERE 
      l-besthis.anf-best-dat = from-date    AND
      /*l-besthis.lager-nr = l-lager.lager-nr AND*/
      l-besthis.artnr LE 2999999 NO-LOCK,
      FIRST l-oh WHERE 
      l-oh.anf-best-dat = from-date AND
      l-oh.lager-nr = 0             AND
      l-oh.artnr = l-besthis.artnr  NO-LOCK,
      FIRST l-lager WHERE l-lager.lager-nr = l-besthis.lager-nr NO-LOCK:
/*
      FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr 
      AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
     IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN  
*/ 
      DO: 
/****** Indicator FOOD OR BEVERAGE ********/ 
/*
        IF l-artikel.endkum = fl-eknr THEN flag = 1. 
        ELSE IF l-artikel.endkum = bl-eknr THEN flag = 2. 
*/ 
        IF l-besthis.artnr LE 1999999 THEN flag = 1.
        ELSE flag = 2.

        qty1 = l-besthis.anz-anf-best + l-besthis.anz-eingang 
                - l-besthis.anz-ausgang. 
        qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
                - l-oh.anz-ausgang. 
        wert = l-oh.val-anf-best + l-oh.wert-eingang 
                - l-oh.wert-ausgang. 
 
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.reihenfolge = flag. 
          s-list.lager-nr = l-lager.lager-nr. 
          s-list.l-bezeich = l-lager.bezeich. 
          s-list.flag = 0.  /*** indicator FOR beginning onhand ***/ 
        END. 
        s-list.anf-wert = s-list.anf-wert + l-besthis.val-anf-best. 
        IF qty NE 0 THEN 
          s-list.end-wert = s-list.end-wert + wert * qty1 / qty. 
      END. 
    END.
/* receiving */ 
      /*MTIF CONNECTED ("vhparch") THEN
      DO:
          RUN fbrecon-arch.p('list-rec', from-date, to-date, l-artikel.artnr, 
                l-lager.lager-nr, flag, l-lager.bezeich, food-bev, bev-food,
                cr-con, fl-eknr, bl-eknr ).
      END.
      ELSE
      DO:*/
          FOR EACH vhp.l-ophis NO-LOCK WHERE 
            vhp.l-ophis.datum GE from-date   AND 
            vhp.l-ophis.datum LE to-date AND
            /*vhp.l-ophis.artnr = l-besthis.artnr AND */
            vhp.l-ophis.artnr LE 2999999 AND
            vhp.l-ophis.op-art = 1 AND
            /*vhp.l-ophis.lager-nr = l-lager.lager-nr AND */
            NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*"  USE-INDEX l-art-dat-op_ix ,
            FIRST l-lager WHERE l-lager.lager-nr = l-lager.lager-nr NO-LOCK BY vhp.l-ophis.lscheinnr: 
            FIND FIRST vhp.l-ophhis WHERE vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
              AND vhp.l-ophhis.op-typ = "STI" NO-LOCK. 
            IF vhp.l-ophis.anzahl GE 0 THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
                AND s-list.reihenfolge = flag AND s-list.flag = 11 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                create s-list. 
                s-list.reihenfolge = flag.  /*** indicator FOR food OR beverage ***/ 
                s-list.lager-nr = l-lager.lager-nr. 
                s-list.l-bezeich = l-lager.bezeich. 
                s-list.flag = 11.   /*** indicator FOR receiving  ***/ 
              END. 
              s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
            END. 
            ELSE IF vhp.l-ophis.anzahl LT 0 THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
                AND s-list.reihenfolge = flag AND s-list.flag = 12 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                create s-list. 
                s-list.reihenfolge = flag. 
                s-list.lager-nr = l-lager.lager-nr. 
                s-list.l-bezeich = l-lager.bezeich. 
                s-list.flag = 12.       /*** indicator FOR RETURN  ***/ 
              END. 
              s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
            END. 
          END. 
      /*MTEND.*/

 
/* consumed */ 
      /*MTIF CONNECTED ("vhparch") THEN
      DO:
          RUN fbrecon-arch.p('list-con', from-date, to-date, l-artikel.artnr, 
                l-lager.lager-nr, flag, l-lager.bezeich, food-bev, bev-food,
                cr-con, fl-eknr, bl-eknr ).
      END.
      ELSE
      DO:*/
          FOR EACH vhp.l-ophis NO-LOCK WHERE 
            vhp.l-ophis.datum GE from-date      AND
            vhp.l-ophis.datum LE to-date        AND
           /* vhp.l-ophis.artnr = l-besthis.artnr AND */
            vhp.l-ophis.artnr LE 2999999 AND 
            vhp.l-ophis.op-art = 3              AND 
            /*vhp.l-ophis.lager-nr = l-lager.lager-nr AND */
            NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" USE-INDEX l-art-dat-op_ix, 

            FIRST l-lager WHERE l-lager.lager-nr = vhp.l-ophis.lager-nr NO-LOCK,
            
            FIRST vhp.l-ophhis WHERE vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
              AND vhp.l-ophhis.op-typ = "STT" NO-LOCK, 

            FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto 
              NO-LOCK BY vhp.l-ophis.lscheinnr: 
            DO: 
              type-of-acct = gl-acct.acc-type. 
              fibukonto = gl-acct.fibukonto. 
              bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                         + CAPS(gl-acct.bezeich). 

              IF vhp.l-ophis.fibukonto NE "" THEN 
              DO: 
                FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto 
                  NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct1 THEN 
                DO: 
                  type-of-acct = gl-acct1.acc-type. 
                  fibukonto = gl-acct1.fibukonto. 
                  /*bezeich = gl-acct1.bezeich. */
                  bezeich = STRING(gl-acct1.fibukonto, coa-format) + " " 
                            + CAPS(gl-acct1.bezeich).
                END. 
              END. 
     
              IF flag = 1 AND fibukonto = food-bev THEN 
              DO: 
                FIND FIRST s-list WHERE s-list.lager-nr = 9999 
                  AND s-list.reihenfolge = 2. 
                s-list.anf-wert = s-list.anf-wert + vhp.l-ophis.warenwert. 
              END. 
              ELSE IF flag = 2 AND fibukonto = bev-food THEN 
              DO: 
                FIND FIRST s-list WHERE s-list.lager-nr = 9999 
                  AND s-list.reihenfolge = 1. 
                s-list.anf-wert = s-list.anf-wert + vhp.l-ophis.warenwert. 
              END. 
              ELSE 
              DO: 
                FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
                  AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
                IF NOT AVAILABLE s-list THEN 
                DO: 
                  create s-list. 
                  s-list.reihenfolge = flag. 
                  s-list.fibukonto = fibukonto. 
                  s-list.bezeich = bezeich. 
                  s-list.flag = 5.                  /*** expenses ***/ 
                END. 
                IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4 THEN 
                  s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
              END. 
            END. 
          END. 
      /*MTEND.*/
    /*END. 
  END.*/ 
 
/***  Less Food & Beverage Compliment  */ 
  /*FOR EACH hoteldpt WHERE hoteldpt.num NE ldry AND hoteldpt.num NE dstore 
    NO-LOCK BY hoteldpt.num: */
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND /*h-compli.departement = hoteldpt.num */
      h-compli.departement NE ldry AND h-compli.departement NE dstore
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
        IF h-cost.betrag = 1 THEN ASSIGN betrag = 0.
        ELSE ASSIGN betrag = h-cost.betrag.

        IF artikel.umsatzart = 6 THEN b-cost = h-compli.anzahl * betrag. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * betrag. 
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
        IF mi-opt-chk = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.reihenfolge = 1. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                           + CAPS(gl-acct.bezeich). 
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
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
        IF mi-opt-chk = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.reihenfolge = 2. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                             + CAPS(gl-acct.bezeich). 
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
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
  IF from-grp = 0 OR from-grp = 1 THEN 
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
    output-list.s =STRING("", "x(24)") + STRING(translateExtended ("** FOOD **", lvCAREA, "":U), "x(50)"). 
    
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
 
    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
    output-list.s = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
    
    FOR EACH s-list WHERE s-list.flag = 0  /*** beginning onhand ***/ 
      AND s-list.reihenfolge = 1           /*** food ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag1 = betrag1 + s-list.anf-wert. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        .
        output-list.s =  STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN
      DO:
      .
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
      END.
      ELSE 
      DO:
        .
        output-list.s =  output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
      END. 
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    .
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    DO:
        output-list.s =  STRING("", "x(24)") 
          + STRING("", "x(41)") 
          + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
          + STRING("", "x(18)") 
          + STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
        
    END.
    ELSE 
    DO:
        .
        output-list.s = STRING("", "x(24)") 
          + STRING("", "x(41)") 
          + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
          + STRING("", "x(18)") 
          + STRING(betrag1, "->,>>>,>>>,>>>,>>9"). 
        
    END.

    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 

    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
    
    output-list.s = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 11  /*** incoming ***/ 
      AND s-list.reihenfolge = 1 NO-LOCK    /*** food     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        .
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      DO:
      .
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      END.
      ELSE 
      DO:
      .
      output-list.s =  output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
      END.
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
    IF NOT long-digit THEN 
    DO:
        output-list.s =  STRING("", "x(24)") 
          + STRING("", "x(41)") 
          + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
          + STRING("", "x(18)") 
          + STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
        . 
        END.
    ELSE
    DO:
        output-list.s =  STRING("", "x(24)") 
          + STRING("", "x(41)") 
          + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
          + STRING("", "x(18)") 
          + STRING(betrag2, "->,>>>,>>>,>>>,>>9"). 
        .
    END.
    
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 

    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
    output-list.s = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 12   /*** RETURN ***/ 
      AND s-list.reihenfolge = 1             /*** food   ***/ 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag3 = betrag3 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        .
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      DO:
        .
        output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      END.
      ELSE
      DO:
          .
        output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
      END.
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
    IF NOT long-digit THEN 
    DO: 
        output-list.s = STRING("", "x(24)") 
          + STRING("", "x(41)") 
          + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
          + STRING("", "x(18)") 
          + STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
        .
    END.
    ELSE 
    DO: 
        output-list.s = STRING("", "x(24)") 
          + STRING("", "x(41)") 
          + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
          + STRING("", "x(18)") 
          + STRING(betrag3, "->,>>>,>>>,>>>,>>9"). 
        . 
    END.
    
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
/* BEVERAGE TO FOOD */ 
    FIND FIRST s-list WHERE s-list.lager-nr = 9999 /*** bev TO food ***/ 
      AND s-list.reihenfolge = 1 no-lock.          /*** food ***/ 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
    IF NOT long-digit THEN 
    DO:
        output-list.s = STRING(("4. " + fb-str[1]), "x(24)") 
          + STRING(s-list.l-bezeich, "x(50)") 
          + STRING("", "x(18)") 
          + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
        .
    END.
    ELSE 
    DO:
        output-list.s = STRING(("4. " + fb-str[1]), "x(24)") 
          + STRING(s-list.l-bezeich, "x(50)") 
          + STRING("", "x(18)") 
          + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
        .
    END.
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    .
 
    betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
    IF NOT long-digit THEN 
    DO:
        output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
          + STRING("(1 + 2 + 3 + 4)", "x(50)") 
          + STRING("", "x(18)") 
          + STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
        
    END.
    ELSE
    DO:
        output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
          + STRING("(1 + 2 + 3 + 4)", "x(50)") 
          + STRING("", "x(18)") 
          + STRING(betrag4, "->,>>>,>>>,>>>,>>9"). 
        
    END.
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
    output-list.s = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 1 
      AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag5 = betrag5 + s-list.end-wert. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->,>>>,>>>,>>>,>>9"). 
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
    IF NOT long-digit THEN 
    DO:
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
    
    END.
    ELSE 
    DO:
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->,>>>,>>>,>>>,>>9"). 
    
    END.

    
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
    betrag56 = betrag4 - betrag5. 
    IF NOT long-digit THEN 
    DO:
        output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
          + STRING("(5 - 6)", "x(50)") 
          + STRING("", "x(18)") 
          + STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
    END.
    ELSE
    DO:
        output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
          + STRING("(5 - 6)", "x(50)") 
          + STRING("", "x(18)") 
          + STRING(betrag56, "->,>>>,>>>,>>>,>>9"). 
    END.
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr.
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    
    output-list.s = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
    IF mi-opt-chk = NO THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        create output-list. 
        output-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN output-list.code = s-list.code. 
        ELSE output-list.code = counter. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
    END. 
 
    IF mi-opt-chk = NO THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 

      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
       
      output-list.s = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        create output-list. 
        output-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN output-list.code = s-list.code. 
        ELSE output-list.code = counter. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
    END. 
/*  LESS FOOD TO BEVERAGE */ 
    FIND FIRST s-list WHERE s-list.reihenfolge = 2 AND s-list.lager-nr = 9999. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING("", "x(24)"). 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
    betrag6 = betrag6 + s-list.anf-wert. 
 
    IF mi-opt-chk = NO THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      
     
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
   
    IF NOT long-digit THEN 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag6, "->,>>>,>>>,>>>,>>9"). 
    END.
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    consume2 = betrag56 - betrag6. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
     
    IF NOT long-digit THEN 
    DO:
        output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
          + STRING("(7 - 8)", "x(50)") 
          + STRING("", "x(18)") 
          + STRING(consume2,"->>,>>>,>>>,>>9.99"). 
  
    END.
    ELSE
    DO:
        output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
          + STRING("(7 - 8)", "x(50)") 
          + STRING("", "x(18)") 
          + STRING(consume2,"->,>>>,>>>,>>>,>>9"). 
       
    END.
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
     
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    f-ratio = 0. 
    IF tf-sales NE 0 THEN f-ratio = consume2 / tf-sales * 100. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tf-sales, "->,>>>,>>>,>>9.99") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(18)") 
      + STRING(f-ratio,"->,>>>,>>9.99 %"). 
    ELSE 
    output-list.s = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tf-sales, " ->>>,>>>,>>>,>>9") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(18)") 
      + STRING(f-ratio,"->,>>>,>>9.99 %"). 
  END. 
  IF from-grp = 1 THEN RETURN. 
 
/******************************  BEVERAGE  **********************************/ 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING("", "x(24)") + STRING(translateExtended ("** BEVERAGE **", lvCAREA, "":U), "x(50)"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  i = 0. 
  create output-list. 
  betrag1 = 0. 
  
  output-list.s = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.anf-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag1 = betrag1 + s-list.anf-wert. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag1, "->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 

  i = 0. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  output-list.s = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
  betrag2 = 0. 
  FOR EACH s-list WHERE s-list.flag = 11 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag2 = betrag2 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag2, "->,>>>,>>>,>>>,>>9"). 
  
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 

  i = 0. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr.
  
  output-list.s = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
  betrag3 = 0. 
  FOR EACH s-list WHERE s-list.flag = 12 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag3 = betrag3 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag3, "->,>>>,>>>,>>>,>>9"). 
 
/*  FOOD TO BEVERAGE  */ 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  FIND FIRST s-list WHERE s-list.lager-nr = 9999 
    AND s-list.reihenfolge = 2 NO-LOCK. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  output-list.s = STRING(("4. " + fb-str[2]), "x(24)") 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING("", "x(18)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(("4. " + fb-str[2]), "x(24)") 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING("", "x(18)") 
      + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
 
  betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
      + STRING("(1 + 2 + 3 + 4)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
      + STRING("(1 + 2 + 3 + 4)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag4, "->,>>>,>>>,>>>,>>9"). 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
 
  i = 0. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)"). 
  betrag5 = 0. 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag5 = betrag5 + s-list.end-wert. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  betrag56 = betrag4 - betrag5. 
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(5 - 6)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(5 - 6)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag56, "->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
  betrag6 = 0. 
  IF mi-opt-chk = NO THEN 
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
    betrag6 = betrag6 + s-list.betrag. 
    counter = counter + 1. 
    IF counter GT 1 THEN 
    DO: 
      create output-list. 
      output-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN output-list.code = s-list.code. 
      ELSE output-list.code = counter. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
 
  IF mi-opt-chk = NO THEN 
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.lager-nr: 
    counter = counter + 1. 
    betrag6 = betrag6 + s-list.betrag. 
    IF counter GT 1 THEN 
    DO: 
      create output-list. 
      output-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN output-list.code = s-list.code. 
      ELSE output-list.code = counter. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
 
/*  BEVERAGE TO FOOD */ 
  FIND FIRST s-list WHERE s-list.reihenfolge = 1 
    AND s-list.lager-nr = 9999. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING("", "x(24)"). 
  IF NOT long-digit THEN 
  output-list.s = output-list.s 
    + STRING(s-list.l-bezeich, "x(50)") 
    + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = output-list.s 
    + STRING(s-list.l-bezeich, "x(50)") 
    + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
  betrag6 = betrag6 + s-list.anf-wert. 
 
  IF mi-opt-chk = NO THEN 
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
  END. 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
    + STRING("", "x(41)") 
    + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
    + STRING("", "x(18)") 
    + STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
    + STRING("", "x(41)") 
    + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
    + STRING("", "x(18)") 
    + STRING(betrag6, "->,>>>,>>>,>>>,>>9"). 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 

  consume2 = betrag56 - betrag6. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(7 - 8)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(consume2,"->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(7 - 8)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(consume2,"->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  b-ratio = 0. 
  IF tb-sales NE 0 THEN b-ratio = consume2 / tb-sales * 100. 
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tb-sales, "->,>>>,>>>,>>9.99") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(18)") 
      + STRING(b-ratio,"->,>>>,>>9.99 %"). 
  ELSE 
  output-list.s = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tb-sales, " ->>>,>>>,>>>,>>9") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(18)") 
      + STRING(b-ratio,"->,>>>,>>9.99 %"). 
 
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
DEFINE buffer l-oh FOR l-besthis. 
 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
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
  create s-list. 
  s-list.reihenfolge = 1.      /** beverage TO food **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                     + CAPS(gl-acct.bezeich). 
  s-list.flag = 0. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
  create s-list. 
  s-list.reihenfolge = 2.       /** food TO beverage  **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                     + CAPS(gl-acct.bezeich).  
  s-list.flag = 0. 
 
  flag = 1. 
  FOR EACH l-lager NO-LOCK: 
    FOR EACH l-besthis WHERE 
      l-besthis.anf-best-dat = from-date    AND
      l-besthis.lager-nr = l-lager.lager-nr AND
      l-besthis.artnr GE 1000001            AND
      l-besthis.artnr LE 1999999    NO-LOCK, 
      FIRST l-oh WHERE 
      l-oh.anf-best-dat = from-date AND
      l-oh.lager-nr = 0             AND 
      l-oh.artnr = l-besthis.artnr  NO-LOCK: 
/*
      FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr 
      AND l-artikel.endkum = fl-eknr NO-LOCK: 
      IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN 
*/ 
      DO: 
 
        qty1 = l-besthis.anz-anf-best + l-besthis.anz-eingang 
                - l-besthis.anz-ausgang. 
        qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
                - l-oh.anz-ausgang. 
        wert = l-oh.val-anf-best + l-oh.wert-eingang 
                - l-oh.wert-ausgang. 
 
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.reihenfolge = flag. 
          s-list.lager-nr = l-lager.lager-nr. 
          s-list.l-bezeich = l-lager.bezeich. 
          s-list.flag = 0.  /*** indicator FOR beginning onhand ***/ 
        END. 
        IF l-oh.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-besthis.anz-anf-best 
            * l-oh.val-anf-best / l-oh.anz-anf-best. 
        IF qty NE 0 THEN  s-list.end-wert = s-list.end-wert + wert * qty1 / qty.         
      END. 
 
/* receiving */ 
      /*MTIF CONNECTED ("vhparch") THEN
      DO:
          RUN fbrecon-arch.p('food-rec', from-date, to-date, l-artikel.artnr, 
                l-lager.lager-nr, flag, l-lager.bezeich, food-bev, bev-food,
                cr-con, fl-eknr, bl-eknr ).
      END.
      ELSE
      DO:*/
          FOR EACH vhp.l-ophis NO-LOCK WHERE 
            vhp.l-ophis.datum GE from-date   AND 
            vhp.l-ophis.datum LE to-date AND
            vhp.l-ophis.artnr = l-besthis.artnr AND 
            vhp.l-ophis.op-art = 1 AND
            vhp.l-ophis.lager-nr = l-lager.lager-nr AND 
            NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" USE-INDEX l-art-dat-op_ix 
            BY vhp.l-ophis.lscheinnr: 
            FIND FIRST vhp.l-ophhis WHERE vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
              AND vhp.l-ophhis.op-typ = "STI" NO-LOCK NO-ERROR. 
            IF vhp.l-ophis.anzahl GE 0 THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
                AND s-list.reihenfolge = flag AND s-list.flag = 11 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                create s-list. 
                s-list.reihenfolge = flag.  /*** indicator FOR food OR beverage ***/ 
                s-list.lager-nr = l-lager.lager-nr. 
                s-list.l-bezeich = l-lager.bezeich. 
                s-list.flag = 11.   /*** indicator FOR receiving  ***/ 
              END. 
              s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
            END. 
            ELSE IF vhp.l-ophis.anzahl LT 0 THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
                AND s-list.reihenfolge = flag AND s-list.flag = 12 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                create s-list. 
                s-list.reihenfolge = flag. 
                s-list.lager-nr = l-lager.lager-nr. 
                s-list.l-bezeich = l-lager.bezeich. 
                s-list.flag = 12.       /*** indicator FOR RETURN  ***/ 
              END. 
              s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
            END. 
          END. 
      /*MTEND.*/
 
/* consumed */ 
      /*MTIF CONNECTED ("vhparch") THEN
      DO:
          IF mi-opt-chk = NO THEN
              cr-con = YES.
          RUN fbrecon-arch.p('food-con', from-date, to-date, l-artikel.artnr, 
                l-lager.lager-nr, flag, l-lager.bezeich, food-bev, bev-food,
                cr-con, fl-eknr, bl-eknr ).
      END.
      ELSE
      DO:*/
          FOR EACH vhp.l-ophis NO-LOCK WHERE 
            vhp.l-ophis.datum GE from-date      AND
            vhp.l-ophis.datum LE to-date        AND
            vhp.l-ophis.artnr = l-besthis.artnr AND 
            vhp.l-ophis.op-art = 3              AND 
            vhp.l-ophis.lager-nr = l-lager.lager-nr AND 
            NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" USE-INDEX l-art-dat-op_ix, 
            FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto 
              NO-LOCK BY vhp.l-ophis.lscheinnr: 
            DO: 
              type-of-acct = gl-acct.acc-type. 
              FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK. 
              fibukonto = gl-acct.fibukonto. 
              bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                        + CAPS(gl-acct.bezeich). 
     
              IF fibukonto = food-bev THEN. 
              ELSE IF fibukonto = bev-food THEN. 
              ELSE 
              DO: 
                IF mi-opt-chk = NO THEN 
                DO: 
                  FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
                    AND s-list.reihenfolge = 1 AND s-list.flag = 5 NO-ERROR. 
                  IF NOT AVAILABLE s-list THEN 
                  DO: 
                    create s-list. 
                    s-list.reihenfolge = 1. 
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
                    create s-list. 
                    s-list.reihenfolge = 1. 
                    s-list.code = gl-main.code. 
                    s-list.bezeich = gl-main.bezeich. 
                    s-list.flag = 5.                  /*** expenses ***/ 
                  END. 
                END. 
                IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4 THEN 
                  s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
              END. 
            END. 
          END. 
      /*MTEND.*/
    END. 
  END. 
 
/*** food TO beverage - baverage TO food ***/ 

  /*MTIF CONNECTED ("vhparch") THEN
  DO:
      RUN fbrecon-arch.p('food-tr', from-date, to-date, 0, 0, flag, '', 
          food-bev, bev-food, cr-con, fl-eknr, bl-eknr ).
  END.
  ELSE
  DO:*/
        
      FOR EACH vhp.l-ophis NO-LOCK WHERE 
        vhp.l-ophis.datum GE from-date AND 
        vhp.l-ophis.datum LE to-date   AND
        (vhp.l-ophis.fibukonto = bev-food OR vhp.l-ophis.fibukonto = food-bev) AND
        vhp.l-ophis.op-art = 3 AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*", 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK,
        FIRST vhp.l-ophhis WHERE vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
              AND vhp.l-ophhis.op-typ = "STT" NO-LOCK,
        FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophhis.fibukonto NO-LOCK BY vhp.l-ophis.lscheinnr: 

        fibukonto = gl-acct.fibukonto. 
        IF vhp.l-ophis.fibukonto NE "" THEN 
        DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN 
            DO: 
              fibukonto = gl-acct1.fibukonto.               
            END. 
        END. 

        IF fibukonto = food-bev
           AND l-ophis.artnr GE 1000001            
           AND l-ophis.artnr LE 1999999 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = 9999 AND s-list.reihenfolge = 2. 
          s-list.anf-wert = s-list.anf-wert + vhp.l-ophis.warenwert. 
        END. 
        ELSE IF fibukonto = bev-food AND l-ophis.artnr GT 1999999 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = 9999 AND s-list.reihenfolge = 1. 
          s-list.anf-wert = s-list.anf-wert + vhp.l-ophis.warenwert. 
        END. 
      END. 
  /*MTEND.*/
 
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
        IF h-cost.betrag = 1 THEN ASSIGN betrag = 0.
        ELSE ASSIGN betrag = h-cost.betrag.

        IF artikel.umsatzart = 6 THEN b-cost = h-compli.anzahl * betrag. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * betrag. 
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
        IF mi-opt-chk = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.reihenfolge = 1. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                           + CAPS(gl-acct.bezeich). 
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
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
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING("", "x(24)") + STRING(translateExtended ("** FOOD **", lvCAREA, "":U), "x(50)"). 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
 
    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 0  /*** beginning onhand ***/ 
      AND s-list.reihenfolge = 1           /*** food ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag1 = betrag1 + s-list.anf-wert. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    DO:
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
    END.
    ELSE
    DO:
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag1, "->,>>>,>>>,>>>,>>9"). 
    END.
    
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 

    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 11  /*** incoming ***/ 
      AND s-list.reihenfolge = 1 NO-LOCK    /*** food     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag2, "->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 

    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 12   /*** RETURN ***/ 
      AND s-list.reihenfolge = 1             /*** food   ***/ 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag3 = betrag3 + s-list.betrag. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag3, "->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 

/* BEVERAGE TO FOOD */ 
    FIND FIRST s-list WHERE s-list.lager-nr = 9999 /*** bev TO food ***/ 
      AND s-list.reihenfolge = 1 no-lock.          /*** food ***/ 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    output-list.s = STRING(("4. " + fb-str[1]), "x(24)") 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING("", "x(18)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING(("4. " + fb-str[1]), "x(24)") 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING("", "x(18)") 
      + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
 
    betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
      + STRING("(1 + 2 + 3 + 4)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
      + STRING("(1 + 2 + 3 + 4)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag4, "->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
 
    i = 0. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 1 
      AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
      NO-LOCK BY s-list.lager-nr: 
      i = i + 1. 
      betrag5 = betrag5 + s-list.end-wert. 
      IF i GT 1 THEN 
      DO: 
        create output-list. 
        curr-nr = curr-nr + 1. 
        output-list.nr = curr-nr. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->,>>>,>>>,>>>,>>9"). 
    END. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 

    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    betrag56 = betrag4 - betrag5. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(5 - 6)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(5 - 6)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag56, "->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
    IF mi-opt-chk = NO THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        create output-list. 
        output-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN output-list.code = s-list.code. 
        ELSE output-list.code = counter. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
    END. 
 
    IF mi-opt-chk = NO THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
      counter = 0. 
    END. 
    ELSE counter = 1. 
    FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 1 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        create output-list. 
        output-list.nr = curr-nr. 
        IF s-list.code GT 0 THEN output-list.code = s-list.code. 
        ELSE output-list.code = counter. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
    END. 
 
/*  LESS FOOD TO BEVERAGE */ 
    FIND FIRST s-list WHERE s-list.reihenfolge = 2 AND s-list.lager-nr = 9999. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING("", "x(24)"). 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
    betrag6 = betrag6 + s-list.anf-wert. 
 
    IF mi-opt-chk = NO THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
    END. 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(24)") 
      + STRING(translateExtended ("SUB TOTAL",lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag6, "->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
 
    consume2 = betrag56 - betrag6. 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(7 - 8)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(consume2,"->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(7 - 8)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(consume2,"->,>>>,>>>,>>>,>>9"). 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    f-ratio = 0. 
    IF tf-sales NE 0 THEN f-ratio = consume2 / tf-sales * 100. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tf-sales, "->,>>>,>>>,>>9.99") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(18)") 
      + STRING(f-ratio,"->,>>>,>>9.99 %"). 
    ELSE 
    output-list.s = STRING(translateExtended ("Net Food Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tf-sales, " ->>>,>>>,>>>,>>9") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(18)") 
      + STRING(f-ratio,"->,>>>,>>9.99 %"). 
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
DEFINE buffer l-oh FOR l-besthis. 
 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
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
  create s-list. 
  s-list.reihenfolge = 1.      /** beverage TO food **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                   + CAPS(gl-acct.bezeich). 
  s-list.flag = 0. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
  create s-list. 
  s-list.reihenfolge = 2.       /** food TO beverage  **/ 
  s-list.lager-nr = 9999. 
  s-list.l-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                   + CAPS(gl-acct.bezeich).  
  s-list.flag = 0. 
 
  flag = 2. 
  FOR EACH l-lager NO-LOCK: 
    FOR EACH l-besthis WHERE 
      l-besthis.anf-best-dat = from-date    AND
      l-besthis.lager-nr = l-lager.lager-nr AND
      l-besthis.artnr GE 2000001            AND
      l-besthis.artnr LE 2999999            NO-LOCK,
      FIRST l-oh WHERE 
      l-oh.anf-best-dat = from-date AND 
      l-oh.lager-nr = 0             AND
      l-oh.artnr = l-besthis.artnr  NO-LOCK:
/*
      FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr 
      AND l-artikel.endkum = bl-eknr NO-LOCK: 
      IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN  
*/ 
      DO: 
 
        qty1 = l-besthis.anz-anf-best + l-besthis.anz-eingang 
                - l-besthis.anz-ausgang. 
        qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
                - l-oh.anz-ausgang. 
        wert = l-oh.val-anf-best + l-oh.wert-eingang 
                - l-oh.wert-ausgang. 
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.reihenfolge = flag. 
          s-list.lager-nr = l-lager.lager-nr. 
          s-list.l-bezeich = l-lager.bezeich. 
          s-list.flag = 0.  /*** indicator FOR beginning onhand ***/ 
        END. 
        IF l-oh.anz-anf-best NE 0 THEN 
          s-list.anf-wert = s-list.anf-wert + l-besthis.anz-anf-best 
            * l-oh.val-anf-best / l-oh.anz-anf-best. 
/*      s-list.anf-wert = s-list.anf-wert + l-besthis.val-anf-best.  */ 
        IF qty NE 0 THEN s-list.end-wert = s-list.end-wert + wert * qty1 / qty. 
      END. 
 
/* receiving */ 
      /*MTIF CONNECTED ("vhparch") THEN
      DO:
          RUN fbrecon-arch.p('bev-rec', from-date, to-date, l-artikel.artnr, 
                l-lager.lager-nr, flag, l-lager.bezeich, food-bev, bev-food,
                cr-con, fl-eknr, bl-eknr ).
      END.
      ELSE
      DO:*/
          FOR EACH vhp.l-ophis NO-LOCK WHERE 
            vhp.l-ophis.datum GE from-date      AND
            vhp.l-ophis.datum LE to-date        AND
            vhp.l-ophis.artnr = l-besthis.artnr AND 
            vhp.l-ophis.op-art = 1              AND
            vhp.l-ophis.lager-nr = l-lager.lager-nr 
            AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" USE-INDEX l-art-dat-op_ix 
            BY vhp.l-ophis.lscheinnr: 
            FIND FIRST vhp.l-ophhis WHERE vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
              AND vhp.l-ophhis.op-typ = "STI" NO-LOCK NO-ERROR. 
            IF vhp.l-ophis.anzahl GE 0 THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
                AND s-list.reihenfolge = flag AND s-list.flag = 11 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                create s-list. 
                s-list.reihenfolge = flag.  /*** indicator FOR food OR beverage ***/ 
                s-list.lager-nr = l-lager.lager-nr. 
                s-list.l-bezeich = l-lager.bezeich. 
                s-list.flag = 11.   /*** indicator FOR receiving  ***/ 
              END. 
              s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
            END. 
            ELSE IF vhp.l-ophis.anzahl LT 0 THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
                AND s-list.reihenfolge = flag AND s-list.flag = 12 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                create s-list. 
                s-list.reihenfolge = flag. 
                s-list.lager-nr = l-lager.lager-nr. 
                s-list.l-bezeich = l-lager.bezeich. 
                s-list.flag = 12.       /*** indicator FOR RETURN  ***/ 
              END. 
              s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
            END. 
          END. 
      /*MTEND.*/
 
/* consumed */ 
      /*MTIF CONNECTED ("vhparch") THEN
      DO:
          IF mi-opt-chk = NO THEN
              cr-con = YES.
          RUN fbrecon-arch.p('bev-con', from-date, to-date, l-artikel.artnr, 
                l-lager.lager-nr, flag, l-lager.bezeich, food-bev, bev-food,
                cr-con, fl-eknr, bl-eknr ).
      END.
      ELSE
      DO:*/
          FOR EACH vhp.l-ophis NO-LOCK WHERE 
            vhp.l-ophis.datum GE from-date      AND 
            vhp.l-ophis.datum LE to-date        AND
            vhp.l-ophis.artnr = l-besthis.artnr AND 
            vhp.l-ophis.op-art = 3              AND
            vhp.l-ophis.lager-nr = l-lager.lager-nr 
            AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" USE-INDEX l-art-dat-op_ix, 
    /*
            FIRST l-ophhis WHERE l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
              AND l-ophhis.op-typ = "STT" AND l-ophhis.fibukonto NE "" NO-LOCK, 
    */        
            FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto 
              NO-LOCK BY vhp.l-ophis.lscheinnr: 
            DO: 
              type-of-acct = gl-acct.acc-type. 
              FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK. 
              fibukonto = gl-acct.fibukonto. 
              bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                        + CAPS(gl-acct.bezeich). 
              IF vhp.l-ophis.fibukonto NE "" THEN 
              DO: 
                FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = vhp.l-ophis.fibukonto 
                  NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct1 THEN 
                DO: 
                  type-of-acct = gl-acct1.acc-type. 
                  FIND FIRST gl-main WHERE gl-main.nr = gl-acct1.main-nr NO-LOCK. 
                  fibukonto = gl-acct1.fibukonto. 
                  /*bezeich = gl-acct1.bezeich. */
                  bezeich = STRING(gl-acct1.fibukonto, coa-format) + " " 
                            + CAPS(gl-acct1.bezeich).
                END. 
              END. 
     
              IF fibukonto = food-bev THEN. 
              ELSE IF fibukonto = bev-food THEN. 
              ELSE 
              DO: 
                IF mi-opt-chk = NO THEN 
                DO: 
                  FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
                    AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
                  IF NOT AVAILABLE s-list THEN 
                  DO: 
                    create s-list. 
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
                    create s-list. 
                    s-list.reihenfolge = flag. 
                    s-list.code = gl-main.code. 
                    s-list.bezeich = gl-main.bezeich. 
                    s-list.flag = 5.                  /*** expenses ***/ 
                  END. 
                END. 
                IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4 THEN 
                  s-list.betrag = s-list.betrag + vhp.l-ophis.warenwert. 
              END. 
            END. 
          END. 
      /*MTEND.*/
    END. 
  END. 
 
/*** food TO beverage - beverage TO food ***/ 
  /*MTIF CONNECTED ("vhparch") THEN
  DO:
      RUN fbrecon-arch.p('bev-tr', from-date, to-date, 0, 0, flag, '', 
          food-bev, bev-food, cr-con, fl-eknr, bl-eknr ).
  END.
  ELSE
  DO:*/
      FOR EACH vhp.l-ophis NO-LOCK WHERE 
        vhp.l-ophis.datum GE from-date AND 
        vhp.l-ophis.datum LE to-date   AND
        (vhp.l-ophis.fibukonto = bev-food OR vhp.l-ophis.fibukonto = food-bev) AND
        vhp.l-ophis.op-art = 3 AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" USE-INDEX l-art-dat-op_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
        AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 

        IF vhp.l-ophis.fibukonto = food-bev
           AND l-ophis.artnr GE 1000001            
           AND l-ophis.artnr LE 1999999 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = 9999 
            AND s-list.reihenfolge = 2. 
          s-list.anf-wert = s-list.anf-wert + vhp.l-ophis.warenwert. 
        END. 
        ELSE IF vhp.l-ophis.fibukonto = bev-food
            AND l-ophis.artnr GE 1999999 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.lager-nr = 9999 
            AND s-list.reihenfolge = 1. 
          s-list.anf-wert = s-list.anf-wert + vhp.l-ophis.warenwert. 
        END. 
      END. 
  /*MTEND.*/
 
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
        IF h-cost.betrag = 1 THEN ASSIGN betrag = 0.
        ELSE ASSIGN betrag = h-cost.betrag.

        IF artikel.umsatzart = 6 THEN b-cost = h-compli.anzahl * betrag. 
        ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN 
          f-cost = h-compli.anzahl * betrag. 
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
        IF mi-opt-chk = NO THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.reihenfolge = 2. 
            s-list.fibukonto = gl-acct.fibukonto. 
            s-list.bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                             + CAPS(gl-acct.bezeich). 
            s-list.flag = 4. 
          END. 
        END. 
        ELSE 
        DO: 
          FIND FIRST s-list WHERE s-list.code = gl-main.code 
            AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
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
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING("", "x(24)") + STRING(translateExtended ("** BEVERAGE **", lvCAREA, "":U), "x(50)"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  i = 0. 
  create output-list. 
  betrag1 = 0. 
  output-list.s = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.anf-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag1 = betrag1 + s-list.anf-wert. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag1, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag1, "->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 

  i = 0. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
  betrag2 = 0. 
  FOR EACH s-list WHERE s-list.flag = 11 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag2 = betrag2 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag2, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag2, "->,>>>,>>>,>>>,>>9"). 

  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr.  

  i = 0. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
  betrag3 = 0. 
  FOR EACH s-list WHERE s-list.flag = 12 AND s-list.reihenfolge = 2 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag3 = betrag3 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag3, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag3, "->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
/*  FOOD TO BEVERAGE  */ 
  FIND FIRST s-list WHERE s-list.lager-nr = 9999 
    AND s-list.reihenfolge = 2 NO-LOCK. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING(("4. " + fb-str[2]), "x(24)") 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING("", "x(18)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(("4. " + fb-str[2]), "x(24)") 
      + STRING(s-list.l-bezeich, "x(50)") 
      + STRING("", "x(18)") 
      + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
      + STRING("(1 + 2 + 3 + 4)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag4, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(translateExtended ("5. Inventory Available", lvCAREA, "":U), "x(24)") 
      + STRING("(1 + 2 + 3 + 4)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag4, "->,>>>,>>>,>>>,>>9"). 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  i = 0. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING(translateExtended ("6. Closing Inventory", lvCAREA, "":U), "x(24)"). 
  betrag5 = 0. 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 2 
    AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag5 = betrag5 + s-list.end-wert. 
    IF i GT 1 THEN 
    DO: 
      create output-list. 
      curr-nr = curr-nr + 1. 
      output-list.nr = curr-nr. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.l-bezeich, "x(50)") 
        + STRING(s-list.end-wert, "->,>>>,>>>,>>>,>>9"). 
  END. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
      + STRING("", "x(41)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(18)") 
      + STRING(betrag5, "->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  betrag56 = betrag4 - betrag5. 
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(5 - 6)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag56, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(translateExtended ("7. Gross Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(5 - 6)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(betrag56, "->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING(translateExtended ("8. Credits", lvCAREA, "":U), "x(24)"). 
  betrag6 = 0. 
  IF mi-opt-chk = NO THEN 
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("- Compliment Cost", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
    betrag6 = betrag6 + s-list.betrag. 
    counter = counter + 1. 
    IF counter GT 1 THEN 
    DO: 
      create output-list. 
      output-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN output-list.code = s-list.code. 
      ELSE output-list.code = counter. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
 
  IF mi-opt-chk = NO THEN 
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
    output-list.s = STRING(translateExtended ("- Department Expenses", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
  END. 
  ELSE counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = 2 
    AND s-list.betrag NE 0 NO-LOCK BY s-list.lager-nr: 
    counter = counter + 1. 
    betrag6 = betrag6 + s-list.betrag. 
    IF counter GT 1 THEN 
    DO: 
      create output-list. 
      output-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN output-list.code = s-list.code. 
      ELSE output-list.code = counter. 
      output-list.s = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(50)") 
        + STRING(s-list.betrag, "->,>>>,>>>,>>>,>>9"). 
  END. 
 
/*  BEVERAGE TO FOOD */ 
  FIND FIRST s-list WHERE s-list.reihenfolge = 1 
    AND s-list.lager-nr = 9999. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  output-list.s = STRING("", "x(24)"). 
  IF NOT long-digit THEN 
  output-list.s = output-list.s 
    + STRING(s-list.l-bezeich, "x(50)") 
    + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = output-list.s 
    + STRING(s-list.l-bezeich, "x(50)") 
    + STRING(s-list.anf-wert, "->,>>>,>>>,>>>,>>9"). 
  betrag6 = betrag6 + s-list.anf-wert. 
 
  IF mi-opt-chk = NO THEN 
  DO: 
    create output-list. 
    curr-nr = curr-nr + 1. 
    output-list.nr = curr-nr. 
  END. 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING("", "x(24)") 
    + STRING("", "x(41)") 
    + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
    + STRING("", "x(18)") 
    + STRING(betrag6, "->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING("", "x(24)") 
    + STRING("", "x(41)") 
    + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
    + STRING("", "x(18)") 
    + STRING(betrag6, "->,>>>,>>>,>>>,>>9"). 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  consume2 = betrag56 - betrag6. 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(7 - 8)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(consume2,"->>,>>>,>>>,>>9.99"). 
  ELSE 
  output-list.s = STRING(translateExtended ("9. Net Consumption", lvCAREA, "":U), "x(24)") 
      + STRING("(7 - 8)", "x(50)") 
      + STRING("", "x(18)") 
      + STRING(consume2,"->,>>>,>>>,>>>,>>9"). 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
 
  create output-list. 
  curr-nr = curr-nr + 1. 
  output-list.nr = curr-nr. 
  b-ratio = 0. 
  IF tb-sales NE 0 THEN b-ratio = consume2 / tb-sales * 100. 
  IF NOT long-digit THEN 
  output-list.s = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tb-sales, "->,>>>,>>>,>>9.99") 
      + STRING("     Cost:Sales", "x(18)") 
      + STRING(b-ratio,"->,>>>,>>9.99 %"). 
  ELSE 
  output-list.s = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(33)") 
      + STRING(tb-sales, " ->>>,>>>,>>>,>>9") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(18)") 
      + STRING(b-ratio,"->,>>>,>>9.99 %"). 
 
  done = YES. 
END. 


PROCEDURE fb-sales: 
DEFINE INPUT PARAMETER f-eknr AS INTEGER. 
DEFINE INPUT PARAMETER b-eknr AS INTEGER. 
DEFINE OUTPUT PARAMETER tf-sales AS DECIMAL. 
DEFINE OUTPUT PARAMETER tb-sales AS DECIMAL. 
 
DEFINE VARIABLE f-sales AS DECIMAL. 
DEFINE VARIABLE b-sales AS DECIMAL. 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE amount AS DECIMAL. 
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
        h-service = 0. 
        h-mwst = 0. 

        RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
             artikel.mwst-code, OUTPUT h-service, OUTPUT h-mwst).

        /*IF artikel.service-code NE 0 THEN 
        DO: 
          FIND FIRST htparam WHERE htparam.paramnr 
            = artikel.service-code NO-LOCK. 
          IF htparam.fdecimal NE 0 THEN h-service = htparam.fdecimal / 100. 
        END. 
        IF artikel.mwst-code NE 0 THEN 
        DO: 
          FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK. 
          IF htparam.fdecimal NE 0 THEN 
          DO: 
            h-mwst = htparam.fdecimal. 
            IF serv-taxable THEN h-mwst = h-mwst * (1 + h-service) / 100. 
            ELSE h-mwst = h-mwst / 100. 
          END. 
        END. */
         
        amount = umsatz.betrag / (1 + h-service + h-mwst). 
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

