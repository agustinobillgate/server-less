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
 
DEFINE buffer s1-list FOR s-list. 

DEFINE TEMP-TABLE output-list 
  FIELD curr-counter AS INTEGER 
  FIELD nr           AS INTEGER INITIAL 0 
  FIELD store        AS INTEGER INITIAL 0 
  FIELD amount       AS DECIMAL INITIAL 0 
  FIELD bezeich      AS CHAR 
  FIELD s            AS CHAR.

DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER from-grp    AS INT.
DEF INPUT PARAMETER food        AS INT.
DEF INPUT PARAMETER bev         AS INT.

DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER date1       AS DATE. 
DEF INPUT PARAMETER date2       AS DATE. 


DEF INPUT PARAMETER mi-opt-chk AS LOGICAL.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER exchg-rate AS DECIMAL .
DEF INPUT PARAMETER foreign-nr AS INT.

DEF OUTPUT PARAMETER done      AS LOGICAL INITIAL NO. 
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE counter        AS INTEGER. 
DEFINE VARIABLE output-counter AS INTEGER INITIAL 0.
DEFINE VARIABLE coa-format     AS CHARACTER NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fb-reconsile1".


DEFINE VARIABLE type-of-acct    AS INTEGER NO-UNDO. 
DEFINE VARIABLE long-digit      AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK.
coa-format = htparam.fchar.


IF from-grp = food THEN RUN create-food. 
ELSE IF from-grp = bev THEN RUN create-beverage. 

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
DEFINE VARIABLE net-cost AS DECIMAL INITIAL 0 NO-UNDO. 
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
 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE buffer h-art FOR h-artikel. 
 
DEFINE VARIABLE qty1 AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE onhand AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE netcost-flag AS LOGICAL. 
DEFINE BUFFER gl-acct1 FOR gl-acct. 
DEFINE BUFFER l-oh FOR l-bestand. 
DEFINE BUFFER l-oh1 FOR l-bestand. 
 
DEF VAR tot-foodcost       AS DECIMAL   NO-UNDO INITIAL 0. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
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
 
  RUN create-output-list. 
  output-list.s = STRING("", "x(24)") 
      + STRING(translateExtended ("** FOOD **", lvCAREA, "":U), "x(33)"). 
 
  flag = 1. 
  FOR EACH l-lager WHERE l-lager.betriebsnr GT 0 NO-LOCK: 
 
    FOR EACH s-list: 
      delete s-list. 
    END. 
    betrag1 = 0. 
    betrag2 = 0. 
    betrag3 = 0. 
    betrag4 = 0. 
    betrag5 = 0. 
    betrag6 = 0. 
    net-cost = 0. 
 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = bev-food NO-LOCK. 
    CREATE s-list. 
    ASSIGN
        s-list.reihenfolge = 1      /** beverage TO food **/ 
        s-list.lager-nr    = 9999 
        s-list.l-bezeich   = STRING(gl-acct.fibukonto, coa-format) + " " 
                           + CAPS(gl-acct.bezeich)
        s-list.flag        = 0
    .  
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
    CREATE s-list. 
    ASSIGN
        s-list.reihenfolge = 2       /** food TO beverage  **/ 
        s-list.lager-nr    = 9999 
        s-list.l-bezeich   = STRING(gl-acct.fibukonto, coa-format) + " " 
                           + CAPS(gl-acct.bezeich) 
        s-list.flag        = 0
    .  
    RUN create-output-list. 
    RUN create-output-list. 
    output-list.s = STRING("", "x(24)") 
      + STRING(l-lager.lager-nr, "99 ") + STRING(l-lager.bezeich, "x(30)"). 
 
    FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
      FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
      AND l-oh.lager-nr = 0 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      AND l-artikel.endkum = fl-eknr NO-LOCK: 
/*    IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN */ 
      DO: 
        ASSIGN
          qty1 = l-bestand.anz-anf-best + l-bestand.anz-eingang 
               - l-bestand.anz-ausgang
          qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
               - l-oh.anz-ausgang 
          wert = l-oh.val-anf-best + l-oh.wert-eingang 
               - l-oh.wert-ausgang
        . 
 
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
 
        FIND FIRST s1-list WHERE s1-list.lager-nr = l-lager.lager-nr 
          AND s1-list.reihenfolge = flag AND s1-list.flag = 1 NO-ERROR. 
        IF NOT AVAILABLE s1-list THEN 
        DO: 
          CREATE s1-list. 
          ASSIGN
            s1-list.flag        = 1 /*** indicator Adjustm FOR begin OH ***/ 
            s1-list.reihenfolge = flag 
            s1-list.lager-nr    = l-lager.lager-nr 
            s1-list.l-bezeich   = l-lager.bezeich
          . 
        END. 
 
        IF l-oh.anz-anf-best NE 0 THEN 
        ASSIGN
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-oh.val-anf-best / l-oh.anz-anf-best
          s1-list.anf-wert = s1-list.anf-wert + l-bestand.anz-anf-best * 
            (l-artikel.vk-preis - l-oh.val-anf-best / l-oh.anz-anf-best)
        . 
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
            ASSIGN
              s-list.flag        = 11   /*** indicator FOR receiving  ***/ 
              s-list.reihenfolge = flag /*** indicator FOR food OR beverage ***/ 
              s-list.lager-nr    = l-lager.lager-nr
              s-list.l-bezeich   = l-lager.bezeich
            . 
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
            ASSIGN
              s-list.flag        = 12   /*** indicator FOR RETURN  ***/ 
              s-list.reihenfolge = flag 
              s-list.lager-nr    = l-lager.lager-nr 
              s-list.l-bezeich   = l-lager.bezeich
            . 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
      END. 
 
/* consumed */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr = l-artikel.artnr AND l-op.loeschflag LE 1 
        AND l-op.op-art = 3 AND l-op.pos GT 0 
        AND l-op.lager-nr = l-lager.lager-nr NO-LOCK USE-INDEX artopart_ix 
        BY l-op.lscheinnr: 
        IF SUBSTR(l-op.stornogrund,1,8) = "00000000" THEN 
          net-cost = net-cost + l-op.warenwert. 
        ELSE 
        DO: 
          FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE gl-acct1 THEN 
          DO: 
            ASSIGN
              fibukonto = gl-acct1.fibukonto 
              bezeich   = STRING(gl-acct1.fibukonto, coa-format) + " " 
                        + CAPS(gl-acct1.bezeich)
              type-of-acct = gl-acct1.acc-type. /*ITA 110417*/ 
            FIND FIRST gl-main WHERE gl-main.nr = gl-acct1.main-nr NO-LOCK. 
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
                CREATE s-list. 
                ASSIGN
                  s-list.flag        = 5   /*** expenses ***/ 
                  s-list.reihenfolge = flag 
                  s-list.fibukonto   = fibukonto 
                  s-list.bezeich     = bezeich
                . 
              END. 
            END. 
            ELSE 
            DO: 
              FIND FIRST s-list WHERE s-list.code = gl-main.code 
                AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                CREATE s-list. 
                ASSIGN
                  s-list.flag        = 5       /*** expenses ***/ 
                  s-list.reihenfolge = flag 
                  s-list.code        = gl-main.CODE 
                  s-list.bezeich     = gl-main.bezeich
                . 
              END. 
            END. 
            IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4 THEN  /*ITA 110417*/
                    s-list.betrag = s-list.betrag + l-op.warenwert. 
          END. 
        END. 
      END. 
    END. 
 
/* stock transfer */ 
    CREATE s-list. 
    ASSIGN
      s-list.flag        = 111   /*** indicator FOR Stock Transfer  ***/ 
      s-list.reihenfolge = flag  /*** indicator FOR food OR beverage ***/ 
      s-list.lager-nr    = l-lager.lager-nr
      s-list.l-bezeich   = l-lager.bezeich
    . 
    
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date /*ITA 110417*/
      AND l-op.loeschflag LE 1 AND l-op.op-art = 4 
      AND l-op.herkunftflag = 1 
      AND (l-op.lager-nr = l-lager.lager-nr 
      OR l-op.pos = l-lager.lager-nr) NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum = fl-eknr NO-LOCK: 
 
/** deduct onhand due TO transferred from side store **/ /*ITA 110417*/
      IF l-op.lager-nr = l-lager.lager-nr THEN 
        /*s-list.betrag = s-list.betrag - l-op.anzahl * l-artikel.vk-preis. */
          s-list.betrag = s-list.betrag - l-op.warenwert.
 
/** add onhand due TO transferred TO side-store */ 
      IF l-op.pos = l-lager.lager-nr THEN 
        /*s-list.betrag = s-list.betrag + l-op.anzahl * l-artikel.vk-preis.*/ 
          s-list.betrag = s-list.betrag + l-op.warenwert.
    END. 
 
/**** Kitchen Transfer ***/ 
    CREATE s-list. 
    ASSIGN
      s-list.flag        = 112 
      s-list.reihenfolge = flag
      s-list.lager-nr    = l-lager.lager-nr
      s-list.bezeich     = "KITCHEN TRANSFER IN" 
    . 
    CREATE s-list. 
    ASSIGN
      s-list.flag        = 113 
      s-list.reihenfolge = flag 
      s-list.lager-nr    = l-lager.lager-nr
      s-list.bezeich     = "KITCHEN TRANSFER OUT" 
    . 
 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.betriebsnr GT 0 
      AND h-compli.p-artnr = 1 /**** FOOD ****/ NO-LOCK BY h-compli.departement: 
 
/** add cost due TO transferred from other kitchen **/ 
      FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.betriebsnr NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.flag = 112. 
        s-list.betrag = s-list.betrag + h-compli.epreis. 
      END. 
/** reduce cost due TO transferred TO other kitchen **/ 
      ELSE 
      DO: 
        FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.departement 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.flag = 113. 
          s-list.betrag = s-list.betrag - h-compli.epreis. 
        END. 
      END. 
    END. 
 
/*** food TO beverage - baverage TO food ***/ 
    FOR EACH l-op WHERE l-op.op-art = 3 AND l-op.loeschflag LE 1 
      AND l-op.datum GE date1 AND l-op.datum LE date2 
      AND (l-op.stornogrund = bev-food OR l-op.stornogrund = food-bev) 
      AND l-op.lager-nr = l-lager.lager-nr NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
      IF l-op.stornogrund = food-bev THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.lager-nr = 9999 
          AND s-list.reihenfolge = 2. 
        s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
      END. 
      ELSE IF l-op.stornogrund = bev-food THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.lager-nr = 9999 
          AND s-list.reihenfolge = 1. 
        s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
      END. 
    END. 
/***  Less Food & Beverage Compliment  */ 
    FOR EACH hoteldpt WHERE hoteldpt.num GT 0 AND 
      (hoteldpt.num EQ l-lager.betriebsnr OR 
       hoteldpt.betriebsnr = l-lager.lager-nr) NO-LOCK BY hoteldpt.num: 
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
          IF artikel.endkum = b-eknr THEN b-cost 
            = h-compli.anzahl * h-cost.betrag. 
          ELSE IF artikel.endkum = f-eknr THEN 
            f-cost = h-compli.anzahl * h-cost.betrag. 
          IF artikel.endkum = f-eknr THEN tot-foodcost = tot-foodcost + f-cost. 
        END. 
        ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) 
        THEN DO: 
          IF artikel.endkum = b-eknr THEN 
            b-cost = h-compli.anzahl * h-compli.epreis * 
            h-artikel.prozent / 100 * rate. 
          ELSE IF artikel.endkum = f-eknr THEN 
            f-cost = h-compli.anzahl * h-compli.epreis * 
            h-artikel.prozent / 100 * rate. 
          IF artikel.endkum = f-eknr THEN tot-foodcost = tot-foodcost + f-cost. 
        END. 
 
        IF f-cost NE 0 THEN 
        DO: 
          IF mi-opt-chk = NO THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
              AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              ASSIGN
                s-list.flag        = 4
                s-list.reihenfolge = flag
                s-list.fibukonto   = gl-acct.fibukonto
                s-list.bezeich     = STRING(gl-acct.fibukonto, coa-format) + " " 
                                   + CAPS(gl-acct.bezeich)
              . 
            END. 
          END. 
          ELSE 
          DO: 
            FIND FIRST s-list WHERE s-list.code = gl-main.code 
              AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              ASSIGN
                s-list.flag        = 4
                s-list.reihenfolge = 1 
                s-list.code        = gl-main.CODE
                s-list.bezeich     = gl-main.bezeich
              . 
            END. 
          END. 
          s-list.betrag = s-list.betrag + f-cost. 
        END. 
      END. 
    END. 
 
    IF l-lager.betriebsnr NE 0 THEN 
      RUN fb-sales(f-eknr, b-eknr, OUTPUT tf-sales, OUTPUT tb-sales). 
 
/******************************  FOOD  ************************************/ 
    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 0  /*** beginning onhand ***/ 
      AND s-list.reihenfolge = flag           /*** food ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 NO-ERROR. 
      IF AVAILABLE s-list THEN onhand = s-list.anf-wert. 
      i = i + 1. 
      betrag1 = betrag1 + onhand. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(onhand, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    onhand = 0. 
    FIND FIRST s-list WHERE s-list.flag = 1  /*** onhand ***/ 
      AND s-list.reihenfolge = flag           /*** food ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 NO-ERROR. 
    IF AVAILABLE s-list THEN onhand = s-list.anf-wert. 
    i = i + 1. 
    betrag1 = betrag1 + onhand. 
    RUN create-output-list. 
    ASSIGN 
      output-list.s = STRING(translateExtended ("   OpenInv Adjustment", lvCAREA, "":U), "x(24)") 
        + STRING("", "x(33)") 
      output-list.nr = 1 
      output-list.store = l-lager.lager-nr 
      output-list.amount = onhand. 

    IF NOT long-digit THEN 
      output-list.s = output-list.s + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 11  /*** incoming ***/ 
      AND s-list.reihenfolge = flag no-error.   /*** food     ***/ 
    IF AVAILABLE s-list THEN onhand = s-list.betrag. 
    i = i + 1. 
    betrag2 = betrag2 + onhand. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 12   /*** RETURN ***/ 
      AND s-list.reihenfolge = flag             /*** food   ***/   NO-ERROR. 
    IF AVAILABLE s-list THEN onhand = s-list.betrag. 
    i = i + 1. 
    betrag3 = betrag3 + onhand. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("4. Store Transfer", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 111  /*** transfer ***/ 
      AND s-list.reihenfolge = flag NO-LOCK    /*** food     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    i = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("5. Kitchen Transfer In", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 112  /*** transfer ***/ 
      AND s-list.reihenfolge = flag NO-LOCK    /*** food     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    i = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("   Kitchen Transfer Out", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 113  /*** transfer ***/ 
      AND s-list.reihenfolge = flag NO-LOCK    /*** food     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
/* BEVERAGE TO FOOD */ 
    FIND FIRST s-list WHERE s-list.lager-nr = 9999 /*** bev TO food ***/ 
      AND s-list.reihenfolge = flag no-lock.          /*** food ***/ 
    RUN create-output-list. 
    output-list.s = STRING(("6. " + s-list.l-bezeich), "x(24)") 
      + STRING("", "x(33)"). 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.anf-wert, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
 
    betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
    RUN create-output-list. 
    ASSIGN 
      output-list.s = STRING(translateExtended ("7. Inventory Available", lvCAREA, "":U), "x(24)") 
        + STRING("(1 + 2 + 3 + 4 + 5 + 6)", "x(33)") 
        + STRING("", "x(15)") 
      output-list.nr = 2 
      output-list.store = l-lager.lager-nr 
      output-list.amount = betrag4. 
 
    IF NOT long-digit THEN 
      output-list.s = output-list.s + STRING(betrag4, "->>>,>>>,>>9.99"). 
    ELSE 
      output-list.s = output-list.s + STRING(betrag4, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("8. Closing Inventory", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = flag 
      AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 NO-ERROR. 
    IF AVAILABLE s-list THEN onhand = s-list.end-wert. 
    i = i + 1. 
    betrag5 = betrag5 + onhand. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING("", "x(15)") 
      + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    RUN create-output-list. 
    betrag56 = betrag4 - betrag5. 
    ASSIGN 
      output-list.s = STRING(translateExtended ("9. Tot. Cost Consumption", lvCAREA, "":U), "x(24)") 
        + STRING("(7 - 8)", "x(33)") + STRING("", "x(15)") 
      output-list.nr = 3 
      output-list.store = l-lager.lager-nr 
      output-list.amount = betrag56. 
 
    IF NOT long-digit THEN 
      output-list.s = output-list.s + STRING(betrag56, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s + STRING(betrag56, "->>,>>>,>>>,>>9"). 
 
 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("10 Less by Expenses", lvCAREA, "":U), "x(24)"). 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("-  Compliment Cost", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
    FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = flag 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        RUN create-output-list. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("-  Department Expenses", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
    FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = flag 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        RUN create-output-list. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
/*  LESS FOOD TO BEVERAGE */ 
    FIND FIRST s-list WHERE s-list.reihenfolge = 2 AND s-list.lager-nr = 9999. 
    RUN create-output-list. 
    output-list.s = STRING("", "x(24)"). 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(33)") 
      + STRING(s-list.anf-wert, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(33)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
    betrag6 = betrag6 + s-list.anf-wert. 
 
    RUN create-output-list. 
    IF NOT long-digit THEN 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(24)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(15)") 
      + STRING(betrag6, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(24)") 
      + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
      + STRING("", "x(15)") 
      + STRING(betrag6, "->>,>>>,>>>,>>9"). 
 
 
    consume2 = betrag56 - betrag6. 
/*  consume2 = net-cost - (betrag56 - betrag6). who made this?? 
    DO i = 1 TO 3: 
      FIND FIRST output-list WHERE output-list.nr = i 
        AND output-list.store = l-lager.lager-nr. 
      output-list.amount = output-list.amount + consume2. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING(output-list.amount, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING(output-list.amount, "->>,>>>,>>>,>>9"). 
    END. 
*/ 
    RUN create-output-list. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended ("11 Net Cost Consumed", lvCAREA, "":U), "x(24)") 
      + STRING("(9 - 10)", "x(33)") 
      + STRING("", "x(15)") 
/*    + STRING(net-cost,"->>>,>>>,>>9.99"). who made this? */
      + STRING(consume2,"->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("11 Net Cost Consumed", "x(24)") 
      + STRING("(9 - 10)", "x(33)") 
      + STRING("", "x(15)") 
/*    + STRING(net-cost,"->>,>>>,>>>,>>9").  who made this?? */
      + STRING(consume2,"->>,>>>,>>>,>>9"). 
 
    RUN create-output-list. 
    f-ratio = 0. 
    IF tf-sales NE 0 THEN f-ratio = consume2 / tf-sales * 100. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended (">> Net Food Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(16)") 
      + STRING(tf-sales, "->,>>>,>>>,>>9.99") 
      + STRING("     Cost:Sales", "x(15)") 
      + STRING(f-ratio,"->,>>>,>>9.99 %"). 
    ELSE 
    output-list.s = STRING("Net Food Sales", "x(24)") 
      + STRING("", "x(16)") 
      + STRING(tf-sales, " ->>>,>>>,>>>,>>9") 
      + STRING("     Cost:Sales", "x(15)") 
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
DEFINE VARIABLE net-cost AS DECIMAL INITIAL 0 NO-UNDO. 
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
 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE buffer h-art FOR h-artikel. 
 
DEFINE VARIABLE qty1 AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE buffer l-oh FOR l-bestand. 
DEFINE buffer l-oh1 FOR l-bestand. 
 
DEFINE VARIABLE onhand AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
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
 
  RUN create-output-list. 
  output-list.s = STRING("", "x(24)") + STRING(translateExtended ("** BEVERAGE **", lvCAREA, "":U), "x(33)"). 
 
  flag = 2. 
  FOR EACH l-lager WHERE l-lager.betriebsnr GT 0 NO-LOCK: 
    
    FOR EACH s-list: 
      DELETE s-list. 
    END. 
    ASSIGN
      betrag1  = 0 
      betrag2  = 0 
      betrag3  = 0 
      betrag4  = 0 
      betrag5  = 0 
      betrag6  = 0 
      net-cost = 0
    . 
 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = bev-food NO-LOCK. 
    CREATE s-list. 
    ASSIGN
      s-list.reihenfolge = 1      /** beverage TO food **/ 
      s-list.lager-nr    = 9999 
      s-list.l-bezeich   = STRING(gl-acct.fibukonto, coa-format) + " " 
                         + CAPS(gl-acct.bezeich)
      s-list.flag        = 0
    . 
 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = food-bev NO-LOCK. 
    CREATE s-list. 
    ASSIGN
      s-list.reihenfolge = 2       /** food TO beverage  **/ 
      s-list.lager-nr    = 9999
      s-list.l-bezeich   = STRING(gl-acct.fibukonto, coa-format) + " " 
                         + CAPS(gl-acct.bezeich)
      s-list.flag        = 0
    . 
 
    RUN create-output-list. 
    RUN create-output-list. 
    output-list.s = STRING("", "x(24)") 
      + STRING(l-lager.lager-nr, "99 ") + STRING(l-lager.bezeich, "x(30)"). 
 
    FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
      FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
      AND l-oh.lager-nr = 0 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      AND l-artikel.endkum = bl-eknr NO-LOCK: 
/*    IF val-anf-best NE 0 OR wert-eingang NE 0 OR wert-ausgang NE 0 THEN */ 
      DO: 
        ASSIGN
          qty1 = l-bestand.anz-anf-best + l-bestand.anz-eingang 
               - l-bestand.anz-ausgang
          qty  = l-oh.anz-anf-best + l-oh.anz-eingang 
               - l-oh.anz-ausgang
          wert = l-oh.val-anf-best + l-oh.wert-eingang 
               - l-oh.wert-ausgang
        .
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          ASSIGN
            s-list.reihenfolge = flag 
            s-list.lager-nr    = l-lager.lager-nr 
            s-list.l-bezeich   = l-lager.bezeich 
            s-list.flag        = 0  /*** indicator FOR beginning onhand ***/ 
          .
        END. 
 
       FIND FIRST s1-list WHERE s1-list.lager-nr = l-lager.lager-nr 
          AND s1-list.reihenfolge = flag AND s1-list.flag = 1 NO-ERROR. 
        IF NOT AVAILABLE s1-list THEN 
        DO: 
          CREATE s1-list. 
          ASSIGN
            s1-list.flag        = 1  /* indicator Adjustm FOR begin OH */
            s1-list.reihenfolge = flag 
            s1-list.lager-nr    = l-lager.lager-nr 
            s1-list.l-bezeich   = l-lager.bezeich 
          .
        END. 
 
        IF l-oh.anz-anf-best NE 0 THEN 
        ASSIGN
          s-list.anf-wert = s-list.anf-wert + l-bestand.anz-anf-best 
            * l-oh.val-anf-best / l-oh.anz-anf-best
          s1-list.anf-wert = s1-list.anf-wert + l-bestand.anz-anf-best * 
            (l-artikel.vk-preis - l-oh.val-anf-best / l-oh.anz-anf-best)
        .
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
            ASSIGN
              s-list.flag        = 11   /*** indicator FOR receiving  ***/ 
              s-list.reihenfolge = flag  /*** indicator FOR food OR beverage ***/ 
              s-list.lager-nr    = l-lager.lager-nr
              s-list.l-bezeich   = l-lager.bezeich
            . 
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
            ASSIGN
              s-list.flag        = 12   /*** indicator FOR RETURN  ***/ 
              s-list.reihenfolge = flag 
              s-list.lager-nr    = l-lager.lager-nr
              s-list.l-bezeich   = l-lager.bezeich
            . 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
      END. 
 
/* consumed */ 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr = l-artikel.artnr AND l-op.loeschflag LE 1 
        AND l-op.op-art = 3 AND l-op.pos GT 0 
        AND l-op.lager-nr = l-lager.lager-nr NO-LOCK USE-INDEX artopart_ix 
        BY l-op.lscheinnr: 
        IF SUBSTR(l-op.stornogrund,1,8) = "00000000" THEN 
          net-cost = net-cost + l-op.warenwert. 
        ELSE 
        DO: 
          FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE gl-acct1 THEN 
          DO: 
            ASSIGN
              fibukonto = gl-acct1.fibukonto
              bezeich   = STRING(gl-acct1.fibukonto, coa-format) + " " 
                        + CAPS(gl-acct1.bezeich)
              type-of-acct = gl-acct1.acc-type. /*ITA 110417*/ 
            . 
            FIND FIRST gl-main WHERE gl-main.nr = gl-acct1.main-nr NO-LOCK. 
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
                CREATE s-list.
                ASSIGN
                  s-list.flag        = 5   /*** expenses ***/ 
                  s-list.reihenfolge = flag 
                  s-list.fibukonto   = fibukonto
                  s-list.bezeich     = bezeich
                . 
              END. 
            END. 
            ELSE 
            DO: 
              FIND FIRST s-list WHERE s-list.code = gl-main.code 
                AND s-list.reihenfolge = flag AND s-list.flag = 5 NO-ERROR. 
              IF NOT AVAILABLE s-list THEN 
              DO: 
                CREATE s-list. 
                ASSIGN
                  s-list.flag        = 5   /*** expenses ***/ 
                  s-list.reihenfolge = flag 
                  s-list.code        = gl-main.CODE
                  s-list.bezeich     = gl-main.bezeich
                . 
              END. 
            END. 
            IF type-of-acct = 5 OR type-of-acct = 3 OR type-of-acct = 4 THEN  /*ITA 110417*/
                s-list.betrag = s-list.betrag + l-op.warenwert. 
          END. 
        END. 
      END. 
    END. 
 
/* stock transfer */ 
    CREATE s-list. 
    ASSIGN
      s-list.flag        = 111   /*** indicator FOR Stock Transfer  ***/ 
      s-list.reihenfolge = flag  /*** indicator FOR food OR beverage ***/ 
      s-list.lager-nr    = l-lager.lager-nr 
      s-list.l-bezeich   = l-lager.bezeich
    . 
    
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date /*ITA 110417*/
      AND l-op.loeschflag LE 1 AND l-op.op-art = 4 
      AND l-op.herkunftflag = 1 
      AND (l-op.lager-nr = l-lager.lager-nr 
      OR l-op.pos = l-lager.lager-nr) NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum = bl-eknr NO-LOCK: 


/** deduct onhand due TO transferred from side store **/ /*ITA 110417*/
      IF l-op.lager-nr = l-lager.lager-nr THEN 
        /*s-list.betrag = s-list.betrag - l-op.anzahl * l-artikel.vk-preis. */
          s-list.betrag = s-list.betrag - l-op.warenwert.
 
/** add onhand due TO transferred TO side-store */ 
      IF l-op.pos = l-lager.lager-nr THEN 
        /*s-list.betrag = s-list.betrag + l-op.anzahl * l-artikel.vk-preis.*/ 
          s-list.betrag = s-list.betrag + l-op.warenwert.
    END. 
 
/**** Kitchen Transfer ***/ 
    CREATE s-list. 
    ASSIGN
      s-list.flag        = 112 
      s-list.reihenfolge = flag 
      s-list.lager-nr    = l-lager.lager-nr
      s-list.bezeich     = "KITCHEN TRANSFER IN" 
    . 
    CREATE s-list. 
    ASSIGN
      s-list.reihenfolge = flag 
      s-list.lager-nr    = l-lager.lager-nr
      s-list.bezeich     = "KITCHEN TRANSFER OUT" 
      s-list.flag        = 113
    . 
 
    FOR EACH h-compli WHERE h-compli.datum GE from-date 
      AND h-compli.datum LE to-date AND h-compli.betriebsnr GT 0 
      AND h-compli.p-artnr = 2 /**** BEV ****/ NO-LOCK BY h-compli.departement: 
/** add cost due TO transferred from other kitchen **/ 
      FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.betriebsnr NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.flag = 112. 
        s-list.betrag = s-list.betrag + h-compli.epreis. 
      END. 
/** reduce cost due TO transferred TO other kitchen **/ 
      ELSE 
      DO: 
        FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.departement 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.flag = 113. 
          s-list.betrag = s-list.betrag - h-compli.epreis. 
        END. 
      END. 
    END. 
 
    FOR EACH l-op WHERE l-op.op-art = 3 AND l-op.loeschflag LE 1 
      AND l-op.datum GE date1 AND l-op.datum LE date2 
      AND (l-op.stornogrund = bev-food OR l-op.stornogrund = food-bev) 
      AND l-op.lager-nr = l-lager.lager-nr NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
      IF l-op.stornogrund = food-bev THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.lager-nr = 9999 
          AND s-list.reihenfolge = 2. 
        s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
      END. 
      ELSE IF l-op.stornogrund = bev-food THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.lager-nr = 9999 
          AND s-list.reihenfolge = 1. 
        s-list.anf-wert = s-list.anf-wert + l-op.warenwert. 
      END. 
    END. 
/***  Less Food & Beverage Compliment  */ 
    FOR EACH hoteldpt WHERE hoteldpt.num GT 0 AND 
      (hoteldpt.num EQ l-lager.betriebsnr OR 
       hoteldpt.betriebsnr = l-lager.lager-nr) NO-LOCK BY hoteldpt.num: 
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
          ELSE FIND FIRST exrate WHERE exrate.datum = curr-datum NO-LOCK 
            NO-ERROR. 
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
          IF artikel.endkum = b-eknr THEN b-cost 
            = h-compli.anzahl * h-cost.betrag. 
          ELSE IF artikel.endkum = f-eknr THEN 
            f-cost = h-compli.anzahl * h-cost.betrag. 
        END. 
        ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) 
        THEN DO: 
          IF artikel.endkum = b-eknr THEN 
            b-cost = h-compli.anzahl * h-compli.epreis * 
            h-artikel.prozent / 100 * rate. 
          ELSE IF artikel.endkum = f-eknr THEN 
            f-cost = h-compli.anzahl * h-compli.epreis * 
            h-artikel.prozent / 100 * rate. 
        END. 
 
        IF b-cost NE 0 THEN 
        DO: 
          IF mi-opt-chk = NO THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
              AND s-list.reihenfolge = flag AND s-list.flag = 4 NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              ASSIGN
                s-list.flag        = 4
                s-list.reihenfolge = flag
                s-list.fibukonto   = gl-acct.fibukonto
                s-list.bezeich     = STRING(gl-acct.fibukonto, coa-format) + " " 
                                   + CAPS(gl-acct.bezeich)
              . 
            END. 
          END. 
          ELSE 
          DO: 
            FIND FIRST s-list WHERE s-list.code = gl-main.code 
              AND s-list.reihenfolge = 2 AND s-list.flag = 4 NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              ASSIGN
                s-list.flag        = 4 
                s-list.reihenfolge = 2 
                s-list.code        = gl-main.CODE 
                s-list.bezeich     = gl-main.bezeich
              . 
            END. 
          END. 
          s-list.betrag = s-list.betrag + b-cost. 
        END. 
      END. 
    END. 
    IF l-lager.betriebsnr NE 0 THEN 
      RUN fb-sales(f-eknr, b-eknr, OUTPUT tf-sales, OUTPUT tb-sales). 
 
/******************************  BEVERAGE  ************************************/ 
    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 0  /*** beginning onhand ***/ 
      AND s-list.reihenfolge = flag           /*** bev ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 NO-ERROR. 
      IF AVAILABLE s-list THEN onhand = s-list.anf-wert. 
      i = i + 1. 
      betrag1 = betrag1 + onhand. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(onhand, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    onhand = 0. 
    FIND FIRST s-list WHERE s-list.flag = 1  /*** onhand ***/ 
      AND s-list.reihenfolge = flag           /*** bev ***/ 
      AND s-list.lager-nr NE 9999          /* NOT food-to-bev OR bev-to-food */ 
      AND s-list.anf-wert NE 0 NO-ERROR. 
    IF AVAILABLE s-list THEN onhand = s-list.anf-wert. 
    i = i + 1. 
    betrag1 = betrag1 + onhand. 
    RUN create-output-list. 
    ASSIGN 
      output-list.s = STRING(translateExtended ("   OpenInv Adjustment", lvCAREA, "":U), "x(24)") 
        + STRING("", "x(33)") 
      output-list.nr = 1 
      output-list.store = l-lager.lager-nr 
      output-list.amount = onhand
    . 
    IF NOT long-digit THEN 
      output-list.s = output-list.s + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s + STRING(onhand, "->>,>>>,>>>,>>9").  
 
    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 11  /*** incoming ***/ 
      AND s-list.reihenfolge = flag no-error.   /*** bev    ***/ 
    IF AVAILABLE s-list THEN onhand = s-list.betrag. 
    i = i + 1. 
    betrag2 = betrag2 + onhand. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 12   /*** RETURN ***/ 
      AND s-list.reihenfolge = flag             /*** bev   ***/   NO-ERROR. 
    IF AVAILABLE s-list THEN onhand = s-list.betrag. 
    i = i + 1. 
    betrag3 = betrag3 + onhand. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    i = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("4. Store Transfer", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 111  /*** transfer ***/ 
      AND s-list.reihenfolge = flag NO-LOCK    /*** bev     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    i = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("5. Kitchen Transfer In", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 112  /*** transfer ***/ 
      AND s-list.reihenfolge = flag NO-LOCK    /*** bev     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    i = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("   Kitchen Transfer Out", lvCAREA, "":U), "x(24)"). 
    FOR EACH s-list WHERE s-list.flag = 113  /*** transfer ***/ 
      AND s-list.reihenfolge = flag NO-LOCK    /*** bev     ***/ 
      BY s-list.lager-nr: 
      i = i + 1. 
      betrag2 = betrag2 + s-list.betrag. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING("", "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
/* FOOD TO BEVERAGE */ 
    FIND FIRST s-list WHERE s-list.lager-nr = 9999 /*** bev TO food ***/ 
      AND s-list.reihenfolge = 2 no-lock.          /*** food ***/ 
    RUN create-output-list. 
    output-list.s = STRING(("6. " + s-list.l-bezeich), "x(24)") 
      + STRING("", "x(33)"). 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.anf-wert, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
 
    betrag4 = betrag1 + betrag2 + betrag3 + s-list.anf-wert. 
    RUN create-output-list. 
    ASSIGN 
      output-list.s = STRING(translateExtended ("7. Inventory Available", lvCAREA, "":U), "x(24)") 
        + STRING("(1 + 2 + 3 + 4 + 5 + 6)", "x(33)") 
        + STRING("", "x(15)") 
      output-list.nr = 2 
      output-list.store = l-lager.lager-nr 
      output-list.amount = betrag4. 

    IF NOT long-digit THEN 
      output-list.s = output-list.s + STRING(betrag4, "->>>,>>>,>>9.99"). 
    ELSE 
      output-list.s = output-list.s + STRING(betrag4, "->>,>>>,>>>,>>9"). 

    i = 0. 
    onhand = 0. 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("8. Closing Inventory", lvCAREA, "":U), "x(24)"). 
    FIND FIRST s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = flag 
      AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 NO-ERROR. 
    IF AVAILABLE s-list THEN onhand = s-list.end-wert. 
    i = i + 1. 
    betrag5 = betrag5 + onhand. 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING("", "x(15)") 
      + STRING(onhand, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING("", "x(33)") 
      + STRING(onhand, "->>,>>>,>>>,>>9"). 
 
    RUN create-output-list. 
    betrag56 = betrag4 - betrag5. 
    ASSIGN 
      output-list.s = STRING(translateExtended ("9. Tot. Cost Consumption", lvCAREA, "":U), "x(24)") 
        + STRING("(7 - 8)", "x(33)") + STRING("", "x(15)") 
      output-list.nr = 3 
      output-list.store = l-lager.lager-nr 
      output-list.amount = betrag56. 

    IF NOT long-digit THEN 
      output-list.s = output-list.s + STRING(betrag56, "->>>,>>>,>>9.99"). 
    ELSE output-list.s = output-list.s + STRING(betrag56, "->>,>>>,>>>,>>9"). 
 
 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("10 Less by Expenses", lvCAREA, "":U), "x(24)"). 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("-  Compliment Cost", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
    FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = flag 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        RUN create-output-list. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
    RUN create-output-list. 
    output-list.s = STRING(translateExtended ("-  Department Expenses", lvCAREA, "":U), "x(24)"). 
    counter = 0. 
    FOR EACH s-list WHERE s-list.flag = 5 AND s-list.reihenfolge = flag 
      AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
      betrag6 = betrag6 + s-list.betrag. 
      counter = counter + 1. 
      IF counter GT 1 THEN 
      DO: 
        RUN create-output-list. 
        output-list.s = STRING("", "x(24)"). 
      END. 
      IF NOT long-digit THEN 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>>,>>>,>>9.99"). 
      ELSE 
      output-list.s = output-list.s 
        + STRING(s-list.bezeich, "x(33)") 
        + STRING(s-list.betrag, "->>,>>>,>>>,>>9"). 
    END. 
 
/*  LESS BEVERAGE TO FOOD */ 
    FIND FIRST s-list WHERE s-list.reihenfolge = 1 AND s-list.lager-nr = 9999. 
    RUN create-output-list. 
    output-list.s = STRING("", "x(24)"). 
    IF NOT long-digit THEN 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(33)") 
      + STRING(s-list.anf-wert, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = output-list.s 
      + STRING(s-list.l-bezeich, "x(33)") 
      + STRING(s-list.anf-wert, "->>,>>>,>>>,>>9"). 
    betrag6 = betrag6 + s-list.anf-wert. 
 
    RUN create-output-list. 
    IF NOT long-digit THEN 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(24)") 
      + STRING("SUB TOTAL", "x(9)") 
      + STRING("", "x(15)") 
      + STRING(betrag6, "->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING("", "x(24)") 
      + STRING("", "x(24)") 
      + STRING("SUB TOTAL", "x(9)") 
      + STRING("", "x(15)") 
      + STRING(betrag6, "->>,>>>,>>>,>>9"). 
 
    consume2 = betrag56 - betrag6. 

/*  
    consume2 = net-cost - (betrag56 - betrag6). who made this?? 
    DO i = 1 TO 3: 
      FIND FIRST output-list WHERE output-list.nr = i 
        AND output-list.store = l-lager.lager-nr. 
      output-list.amount = output-list.amount + consume2. 
      IF NOT long-digit THEN output-list.s = output-list.s 
        + STRING(output-list.amount, "->>>,>>>,>>9.99"). 
      ELSE output-list.s = output-list.s 
        + STRING(output-list.amount, "->>,>>>,>>>,>>9"). 
    END. 
*/ 
    RUN create-output-list. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended ("11 Net Cost Consumed", lvCAREA, "":U), "x(24)") 
      + STRING("(9 - 10)", "x(33)") 
      + STRING("", "x(15)") 
/*    + STRING(net-cost,"->>>,>>>,>>9.99"). who made this?? */
      + STRING(consume2,"->>>,>>>,>>9.99"). 
    ELSE 
    output-list.s = STRING(translateExtended ("11 Net Cost Consumed", lvCAREA, "":U), "x(24)") 
      + STRING("(9 - 10)", "x(33)") 
      + STRING("", "x(15)") 
/*    + STRING(net-cost,"->>,>>>,>>>,>>9"). */
      + STRING(consume2,"->>,>>>,>>>,>>9"). 
 
    RUN create-output-list. 
    b-ratio = 0. 
    IF tb-sales NE 0 THEN b-ratio = consume2 / tb-sales * 100. 
    IF NOT long-digit THEN 
    output-list.s = STRING(translateExtended (">> Net Beverage Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(16)") 
      + STRING(tb-sales, "->,>>>,>>>,>>9.99") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
      + STRING(b-ratio,"->,>>>,>>9.99 %"). 
    ELSE 
    output-list.s = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
      + STRING("", "x(16)") 
      + STRING(tb-sales, " ->>>,>>>,>>>,>>9") 
      + STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
      + STRING(b-ratio,"->,>>>,>>9.99 %"). 
  END. 
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
 
  FOR EACH hoteldpt WHERE (hoteldpt.num EQ l-lager.betriebsnr 
    OR hoteldpt.betriebsnr = l-lager.lager-nr) NO-LOCK BY hoteldpt.num: 
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

       /* IF artikel.service-code NE 0 THEN 
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


PROCEDURE create-output-list: /*FDL: #655 Serverless chg from . to :*/ 
  output-counter = output-counter + 1. 
  CREATE output-list. 
  ASSIGN output-list.curr-counter = output-counter. 
END. 

