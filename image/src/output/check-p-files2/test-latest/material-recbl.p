DEFINE TEMP-TABLE mtreconsile-list
    FIELD nr        AS INTEGER
    FIELD CODE      AS INTEGER
    FIELD bezeich   AS CHARACTER
    FIELD col1      AS CHARACTER    FORMAT "x(24)"
    FIELD col2      AS CHARACTER    FORMAT "x(50)"
    FIELD col3      AS CHARACTER    FORMAT "x(20)"
    FIELD col4      AS CHARACTER    FORMAT "x(20)"
    FIELD col5      AS CHARACTER    FORMAT "x(34)".
  
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-grp     AS INTEGER.
DEFINE INPUT PARAMETER lager-no     AS INT.
DEFINE INPUT PARAMETER from-main    AS INT.
DEFINE INPUT PARAMETER to-main      AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR mtreconsile-list.
DEFINE WORKFILE s-list 
    FIELD code AS INTEGER 
    FIELD reihenfolge AS INTEGER 
    FIELD lager-nr AS INTEGER 
    FIELD l-bezeich AS CHAR 
    FIELD fibukonto LIKE gl-acct.fibukonto 
    FIELD bezeich LIKE gl-acct.bezeich 
    FIELD flag AS INTEGER  
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

RUN create-list. 
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
 
DEFINE VARIABLE m-cost AS DECIMAL. 
DEFINE VARIABLE m-ratio AS DECIMAL.  
DEFINE VARIABLE fibu AS CHAR. 
DEFINE VARIABLE m-sales AS DECIMAL. 
DEFINE VARIABLE mm-sales AS DECIMAL. 
 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE amount AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
/*M not used
DEFINE VARIABLE fb-str AS CHAR EXTENT 2 INITIAL 
  ["Beverage TO Food", "Food to Beverage"]. 
fb-str[1] = translateExtended ("Beverage to Food", lvCAREA, "":U). 
fb-str[2] = translateExtended ("Food to Beverage", lvCAREA, "":U). 
*/
 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE buffer h-art FOR h-artikel. 
 
DEFINE VARIABLE qty1 AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE j AS INTEGER INITIAL 0. 
DEFINE VARIABLE qty0 AS DECIMAL. 
DEFINE VARIABLE val0 AS DECIMAL. 
DEFINE buffer l-oh FOR l-bestand. 
DEFINE buffer l-ohist FOR l-besthis. 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  FOR EACH mtreconsile-list: 
    DELETE mtreconsile-list. 
  END. 
 
  curr-nr = 0. 
  curr-reihe = 0.
  flag = 1.
    
  FIND FIRST l-lager WHERE l-lager.lager-nr = lager-no NO-LOCK NO-ERROR.
  IF AVAILABLE l-lager THEN DO:
    FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      AND l-artikel.endkum GE from-main 
      AND l-artikel.endkum LE to-main NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK,
      FIRST l-oh WHERE l-oh.lager-nr = 0 AND l-oh.artnr = l-bestand.artnr NO-LOCK
      BY l-untergrup.fibukonto BY l-artikel.artnr: 
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
      /*FIND FIRST l-oh WHERE l-oh.lager-nr = 0 AND l-oh.artnr = l-bestand.artnr 
        NO-LOCK. */
      qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
      qty0 = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
      val0 = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
      IF qty0 NE 0 THEN 
      s-list.end-wert  = s-list.end-wert + (qty / qty0) * val0. 
      s-list.anf-wert = s-list.anf-wert + l-bestand.val-anf-best. 
      FIND FIRST s-list WHERE s-list.fibukonto = l-untergrup.fibukonto 
        AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        CREATE s-list. 
        ASSIGN
          s-list.reihenfolge = 1
          s-list.fibukonto = l-untergrup.fibukonto
          s-list.bezeich = l-untergrup.bezeich
          s-list.flag = 4. 
      END.
    END.
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        /*AND l-op.artnr = l-artikel.artnr*/
        AND (l-op.op-art = 1 OR l-op.op-art = 3 OR l-op.op-art = 4)
        AND l-op.lager-nr = lager-no AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix,
        FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          AND l-artikel.endkum GE from-main 
          AND l-artikel.endkum LE to-main NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK BY l-op.artnr : 
        IF l-op.op-art = 1 THEN 
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
        ELSE
        DO:
          FIND FIRST s-list WHERE s-list.fibukonto = l-untergrup.fibukonto 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF AVAILABLE s-list THEN
          DO: 
            IF l-op.op-art = 3 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
            ELSE IF l-op.op-art = 4 THEN s-list.betrag = s-list.betrag + l-op.anzahl * l-artikel.vk-preis. 
          END. 
        END.
      END.
  END.
  ELSE 
  DO: 
      FOR EACH l-bestand NO-LOCK, 
        FIRST l-lager WHERE l-lager.lager-nr = l-bestand.lager-nr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          AND l-artikel.endkum GE from-main 
          AND l-artikel.endkum LE to-main NO-LOCK,  
        FIRST l-oh WHERE l-oh.lager-nr = 0 AND l-oh.artnr = l-bestand.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
        BY l-bestand.lager-nr BY l-untergrup.fibukonto BY l-artikel.artnr: 
        FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
          AND s-list.reihenfolge = flag AND s-list.flag = 0 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO:
          CREATE s-list. 
          ASSIGN
            s-list.reihenfolge = flag
            s-list.lager-nr = l-lager.lager-nr
            s-list.l-bezeich = l-lager.bezeich 
            s-list.flag = 0.  /*** indicator FOR beginning onhand ***/ 
        END.  
        ASSIGN
          qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang
          qty0 = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang
          val0 = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
        IF qty0 NE 0 THEN 
          s-list.end-wert  = s-list.end-wert + (qty / qty0) * val0. 
        s-list.anf-wert = s-list.anf-wert + l-bestand.val-anf-best. 
       
        FIND FIRST s-list WHERE s-list.fibukonto = l-untergrup.fibukonto 
          AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          CREATE s-list. 
          ASSIGN
            s-list.reihenfolge = 1
            s-list.fibukonto = l-untergrup.fibukonto
            s-list.bezeich = l-untergrup.bezeich
            s-list.flag = 4.                         
        END.
      END.
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND (l-op.op-art = 1 OR l-op.op-art = 3 OR l-op.op-art = 4) AND l-op.loeschflag LE 1 NO-LOCK 
        USE-INDEX artopart_ix,
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          AND l-artikel.endkum GE from-main 
          AND l-artikel.endkum LE to-main NO-LOCK,  
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK BY l-op.lager-nr: 
      
        IF l-op.op-art = 1 THEN
        DO:
          FIND FIRST s-list WHERE s-list.lager-nr = l-lager.lager-nr 
            AND s-list.reihenfolge = flag AND s-list.flag = 11 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            ASSIGN
              s-list.reihenfolge = flag  /*** indicator FOR food OR beverage ***/ 
              s-list.lager-nr = l-lager.lager-nr
              s-list.l-bezeich = l-lager.bezeich 
              s-list.flag = 11.   /*** indicator FOR receiving  ***/ 
          END. 
          s-list.betrag = s-list.betrag + l-op.warenwert. 
        END.
        ELSE
        DO:
          FIND FIRST s-list WHERE s-list.fibukonto = l-untergrup.fibukonto 
            AND s-list.reihenfolge = 1 AND s-list.flag = 4 NO-ERROR. 
          IF AVAILABLE s-list THEN
          DO:
            IF l-op.op-art = 3 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
            ELSE IF l-op.op-art = 4 THEN s-list.betrag = s-list.betrag + l-op.anzahl * l-artikel.vk-preis. 
          END. 
        END. 
      END. 
  END.     
    
/******************************  Material  **********************************/ 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  mtreconsile-list.col2 = STRING(translateExtended ("** MATERIAL **", lvCAREA, "":U), "x(33)"). 
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  
  i = 0. 
  CREATE mtreconsile-list. 
  betrag1 = 0. 
  
  mtreconsile-list.col1 = STRING(translateExtended ("1. Opening Inventory", lvCAREA, "":U), "x(24)"). 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 1 
    AND s-list.lager-nr NE 9999 AND s-list.anf-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag1 = betrag1 + s-list.anf-wert. 
    IF i GT 1 THEN 
    DO: 
      CREATE mtreconsile-list. 
      curr-nr = curr-nr + 1. 
      mtreconsile-list.nr = curr-nr. 
      mtreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN  mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)")
            mtreconsile-list.col3 = STRING(s-list.anf-wert, "     ->>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN  mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)")
            mtreconsile-list.col3 = STRING(s-list.anf-wert, "     ->>,>>>,>>>,>>9"). 
  END. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
         mtreconsile-list.col4 = STRING(betrag1, "     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)")
         mtreconsile-list.col4 = STRING(betrag1, "     ->>,>>>,>>>,>>9"). 
 
  i = 0. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  
  mtreconsile-list.col1 = STRING(translateExtended ("2. Incoming Stocks", lvCAREA, "":U), "x(24)"). 
  betrag2 = 0. 
  FOR EACH s-list WHERE s-list.flag = 11 AND s-list.reihenfolge = 1 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag2 = betrag2 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      CREATE mtreconsile-list. 
      curr-nr = curr-nr + 1. 
      mtreconsile-list.nr = curr-nr. 
      mtreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN  mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)") 
            mtreconsile-list.col3 = STRING(s-list.betrag, "     ->>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN  mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)") 
            mtreconsile-list.col3 = STRING(s-list.betrag, "     ->>,>>>,>>>,>>9"). 
  END. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + translateExtended ("SUB TOTAL", lvCAREA, "":U)
         mtreconsile-list.col4 = STRING(betrag2, "     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         mtreconsile-list.col4 = STRING(betrag2, "     ->>,>>>,>>>,>>9"). 
 
  i = 0. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr.
  
  /*mtreconsile-list.col1 = STRING(translateExtended ("3. Returned Stocks", lvCAREA, "":U), "x(24)"). 
  betrag3 = 0. 
  FOR EACH s-list WHERE s-list.flag = 12 AND s-list.reihenfolge = 1 NO-LOCK 
    BY s-list.lager-nr: 
    i = i + 1. 
    betrag3 = betrag3 + s-list.betrag. 
    IF i GT 1 THEN 
    DO: 
      CREATE mtreconsile-list. 
      curr-nr = curr-nr + 1. 
      mtreconsile-list.nr = curr-nr. 
      mtreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)") 
           mtreconsile-list.col4 = STRING(s-list.betrag, "     ->>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)") 
           mtreconsile-list.col4 = STRING(s-list.betrag, "     ->>,>>>,>>>,>>9"). 
  END. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         mtreconsile-list.col4 = STRING(betrag3, "     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         mtreconsile-list.col4 = STRING(betrag3, "     ->>,>>>,>>>,>>9"). */
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  betrag4 = betrag1 + betrag2 /* + betrag3 */ + betrag4.
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("3. Inventory Available", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("(1 + 2)", "x(33)") 
         mtreconsile-list.col4 = STRING(betrag4, "     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("3. Inventory Available", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("(1 + 2)", "x(33)") 
         mtreconsile-list.col4 = STRING(betrag4, "     ->>,>>>,>>>,>>9"). 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  
 
  i = 0. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("4. Closing Inventory", lvCAREA, "":U), "x(24)"). 
  betrag5 = 0. 
  FOR EACH s-list WHERE s-list.flag = 0 AND s-list.reihenfolge = 1 
    AND s-list.lager-nr NE 9999 AND s-list.end-wert NE 0 
    NO-LOCK BY s-list.lager-nr: 
    i = i + 1. 
    betrag5 = betrag5 + s-list.end-wert. 
    IF i GT 1 THEN 
    DO: 
      CREATE mtreconsile-list. 
      curr-nr = curr-nr + 1. 
      mtreconsile-list.nr = curr-nr. 
      mtreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)") 
           mtreconsile-list.col3 = STRING(s-list.end-wert, "     ->>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN mtreconsile-list.col2 = STRING(s-list.l-bezeich, "x(33)") 
           mtreconsile-list.col3 = STRING(s-list.end-wert, "     ->>,>>>,>>>,>>9"). 
  END. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         mtreconsile-list.col4 = STRING(betrag5, "     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         mtreconsile-list.col4 = STRING(betrag5, "     ->>,>>>,>>>,>>9"). 
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  betrag56 = betrag4 - betrag5. 
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("5. Gross Consumption", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("(3 - 4)", "x(33)") 
         mtreconsile-list.col4 = STRING(betrag56, "     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("5. Gross Consumption", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("(3 - 4)", "x(33)") 
         mtreconsile-list.col4 = STRING(betrag56, "     ->>,>>>,>>>,>>9"). 
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  mtreconsile-list.col1 = STRING(translateExtended ("6. Consumed", lvCAREA, "":U), "x(24)"). 
  betrag6 = 0. 
  counter = 1. 
  FOR EACH s-list WHERE s-list.flag = 4 AND s-list.reihenfolge = 1
    AND s-list.betrag NE 0 NO-LOCK BY s-list.bezeich: 
    betrag6 = betrag6 + s-list.betrag. 
    counter = counter + 1. 
    IF counter GT 1 THEN 
    DO: 
      CREATE mtreconsile-list. 
      mtreconsile-list.nr = curr-nr. 
      IF s-list.code GT 0 THEN mtreconsile-list.code = s-list.code. 
      ELSE mtreconsile-list.code = counter. 
      mtreconsile-list.col1 = STRING("", "x(24)"). 
    END. 
    IF NOT long-digit THEN 
    ASSIGN mtreconsile-list.col2 = STRING(s-list.bezeich, "x(33)") 
           mtreconsile-list.col3 = STRING(s-list.betrag, "     ->>>,>>>,>>9.99"). 
    ELSE 
    ASSIGN mtreconsile-list.col2 = STRING(s-list.bezeich, "x(33)") 
           mtreconsile-list.col3 = STRING(s-list.betrag, "     ->>,>>>,>>>,>>9"). 
  END. 
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         mtreconsile-list.col4 = STRING(betrag6, "     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col2 = STRING("", "x(24)") + STRING(translateExtended ("SUB TOTAL", lvCAREA, "":U), "x(9)") 
         mtreconsile-list.col4 = STRING(betrag6, "     ->>,>>>,>>>,>>9"). 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
 
  consume2 = betrag56 - betrag6. 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("7. Net Consumption", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("(5 - 6)", "x(33)") 
         mtreconsile-list.col4 = STRING(consume2,"     ->>>,>>>,>>9.99"). 
  ELSE 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("7. Net Consumption", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("(5 - 6)", "x(33)") 
         mtreconsile-list.col4 = STRING(consume2,"     ->>,>>>,>>>,>>9"). 
 
  CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
 
  /*CREATE mtreconsile-list. 
  curr-nr = curr-nr + 1. 
  mtreconsile-list.nr = curr-nr. 
  m-ratio = 0. 
  IF mm-sales NE 0 THEN m-ratio = consume2 / mm-sales * 100. 
  IF NOT long-digit THEN 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("", "x(16)") + STRING(mm-sales, "->,>>>,>>>,>>9.99") 
         mtreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
         mtreconsile-list.col4 = STRING(m-ratio,"->,>>>,>>9.99 %"). 
  ELSE 
  ASSIGN mtreconsile-list.col1 = STRING(translateExtended ("Net Beverage Sales", lvCAREA, "":U), "x(24)") 
         mtreconsile-list.col2 = STRING("", "x(16)") + STRING(mm-sales, " ->>>,>>>,>>>,>>9")
         mtreconsile-list.col3 = STRING(translateExtended ("     Cost:Sales", lvCAREA, "":U), "x(15)") 
         mtreconsile-list.col4 = STRING(m-ratio,"->,>>>,>>9.99 %"). 
         
 done = yes.        */
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
