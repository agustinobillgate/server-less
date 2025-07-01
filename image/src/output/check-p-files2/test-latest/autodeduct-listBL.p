DEFINE TEMP-TABLE c-list
     FIELD artnr       LIKE l-artikel.artnr 
     FIELD bezeich     AS CHARACTER FORMAT "x(36)"             
     FIELD munit       AS CHARACTER FORMAT "x(3)"               
     FIELD inhalt      AS DECIMAL   FORMAT ">>>9.99"            
     FIELD zwkum       AS INTEGER 
     FIELD endkum      AS INTEGER 
     FIELD qty         AS DECIMAL  FORMAT "->>>,>>9.999"       
     FIELD qty1        AS DECIMAL  FORMAT "->>>,>>9.999"        
     FIELD amount      AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"  
     FIELD avrg-amount AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"  
     FIELD fibukonto   LIKE gl-acct.fibukonto           
     FIELD cost-center AS CHARACTER FORMAT "x(50)" 
     FIELD store       AS INTEGER INITIAL 0
     FIELD dept        AS INTEGER
     FIELD price       AS DECIMAL
     FIELD item-artno  AS INTEGER.

DEFINE TEMP-TABLE t-list
    FIELD dept      AS INTEGER
    FIELD rechnr    AS INTEGER
    FIELD pay       AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD rmTrans   AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD compli    AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD coupon    AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD fibukonto AS CHAR INIT "0000000000"
    FIELD pax       AS INTEGER.


DEFINE INPUT PARAMETER sorttype            AS INTEGER.
DEFINE INPUT PARAMETER curr-lager          AS INTEGER.
DEFINE INPUT PARAMETER from-grp            AS INTEGER.
DEFINE INPUT PARAMETER transdate           AS DATE.
DEFINE INPUT PARAMETER fDate               AS DATE.
DEFINE INPUT PARAMETER tDate               AS DATE.
DEFINE OUTPUT PARAMETER tot-amount         AS DECIMAL.
DEFINE OUTPUT PARAMETER tot-avrg-amount    AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR c-list.

DEFINE VARIABLE deduct-compli   AS LOGICAL          NO-UNDO.

RUN journal-list1.

PROCEDURE journal-list1: 
  FOR EACH c-list: 
    delete c-list. 
  END. 

  IF from-grp = 0 THEN DO:
      IF sorttype = 1 THEN 
      DO:
          FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.anzahl NE 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
              BY l-artikel.artnr /*BY l-op.datum BY l-op.lscheinnr*/:
              
              CREATE c-list. 
              ASSIGN 
                c-list.artnr       = l-artikel.artnr 
                c-list.bezeich     = l-artikel.bezeich 
                c-list.munit       = l-artikel.masseinheit 
                c-list.inhalt      = l-artikel.inhalt 
                c-list.zwkum       = l-artikel.zwkum 
                c-list.endkum      = l-artikel.endkum 
                c-list.qty         = l-op.anzahl                     
                c-list.fibukonto   = l-op.stornogrund 
                c-list.amount      = l-op.warenwert
                c-list.avrg-amount = l-op.warenwert / l-op.anzahl .
                 
              tot-amount = tot-amount + l-op.warenwert.
              tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
              FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
              IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
          END. 
      END.
      ELSE IF sorttype = 2 THEN 
      DO:
          FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.anzahl NE 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
              BY l-artikel.bezeich /*BY l-op.datum BY l-op.lscheinnr*/:
              
              CREATE c-list. 
              ASSIGN 
                c-list.artnr       = l-artikel.artnr 
                c-list.bezeich     = l-artikel.bezeich 
                c-list.munit       = l-artikel.masseinheit 
                c-list.inhalt      = l-artikel.inhalt 
                c-list.zwkum       = l-artikel.zwkum 
                c-list.endkum      = l-artikel.endkum 
                c-list.qty         = l-op.anzahl                     
                c-list.fibukonto   = l-op.stornogrund 
                c-list.amount      = l-op.warenwert
                c-list.avrg-amount = l-op.warenwert / l-op.anzahl .
                 
              tot-amount = tot-amount + l-op.warenwert.
              tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
              FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
              IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
          END. 
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
          FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate 
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.anzahl NE 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
              BY l-artikel.zwkum BY l-artikel.bezeich BY l-op.datum BY l-op.lscheinnr: 

              FIND FIRST c-list WHERE c-list.artnr = 0 
              AND c-list.endkum = l-artikel.endkum
              AND c-list.zwkum = l-artikel.zwkum NO-ERROR.
              IF NOT AVAILABLE c-list THEN
              DO:
                  CREATE c-list.
                  ASSIGN 
                      c-list.artnr     = 0
                      c-list.fibukonto = ""
                      c-list.endkum    = l-artikel.endkum
                      c-list.zwkum     = l-artikel.zwkum
                      c-list.bezeich   = l-untergrup.bezeich.
              END.

              CREATE c-list. 
              ASSIGN 
                c-list.artnr       = l-artikel.artnr 
                c-list.bezeich     = l-artikel.bezeich 
                c-list.munit       = l-artikel.masseinheit 
                c-list.inhalt      = l-artikel.inhalt 
                c-list.zwkum       = l-artikel.zwkum 
                c-list.endkum      = l-artikel.endkum 
                c-list.qty         = l-op.anzahl 
                c-list.qty1        = l-op.deci1[1] - l-op.anzahl 
                c-list.fibukonto   = l-op.stornogrund 
                c-list.amount      = l-op.warenwert
                c-list.avrg-amount = l-op.warenwert / l-op.anzahl .
             
              tot-amount = tot-amount + l-op.warenwert.
              tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
              FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
              IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
          END.  
      END.
      ELSE IF sorttype = 4 THEN
      DO:
          RUN create-list.
          RUN get-l-artikels.
      END.
  END.
  ELSE DO:
      IF sorttype = 1 THEN 
      DO:
          FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.anzahl NE 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
              BY l-artikel.artnr /*BY l-op.datum BY l-op.lscheinnr*/: 
              
              
              CREATE c-list. 
              ASSIGN 
                c-list.artnr       = l-artikel.artnr 
                c-list.bezeich     = l-artikel.bezeich 
                c-list.munit       = l-artikel.masseinheit 
                c-list.inhalt      = l-artikel.inhalt 
                c-list.zwkum       = l-artikel.zwkum 
                c-list.endkum      = l-artikel.endkum 
                c-list.qty         = l-op.anzahl                    
                c-list.fibukonto   = l-op.stornogrund 
                c-list.amount      = l-op.warenwert
                c-list.avrg-amount = l-op.warenwert / l-op.anzahl .
                 
              tot-amount = tot-amount + l-op.warenwert.
              tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
              FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
              IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
          END. 
      END.
      ELSE IF sorttype = 2 THEN 
      DO:
          FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.anzahl NE 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
              BY l-artikel.bezeich /*BY l-op.datum BY l-op.lscheinnr*/: 
              
              
              CREATE c-list. 
              ASSIGN 
                c-list.artnr       = l-artikel.artnr 
                c-list.bezeich     = l-artikel.bezeich 
                c-list.munit       = l-artikel.masseinheit 
                c-list.inhalt      = l-artikel.inhalt 
                c-list.zwkum       = l-artikel.zwkum 
                c-list.endkum      = l-artikel.endkum 
                c-list.qty         = l-op.anzahl
                    
                c-list.fibukonto   = l-op.stornogrund 
                c-list.amount      = l-op.warenwert
                c-list.avrg-amount = l-op.warenwert / l-op.anzahl .
                 
              tot-amount = tot-amount + l-op.warenwert.
              tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
              FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
              IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
          END. 
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
          FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate 
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.anzahl NE 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
              BY l-artikel.zwkum BY l-artikel.bezeich BY l-op.datum BY l-op.lscheinnr: 

              FIND FIRST c-list WHERE c-list.artnr = 0 
              AND c-list.endkum = l-artikel.endkum
              AND c-list.zwkum = l-artikel.zwkum NO-ERROR.
              IF NOT AVAILABLE c-list THEN
              DO:
                  CREATE c-list.
                  ASSIGN 
                      c-list.artnr     = 0
                      c-list.fibukonto = ""
                      c-list.endkum    = l-artikel.endkum
                      c-list.zwkum     = l-artikel.zwkum
                      c-list.bezeich   = l-untergrup.bezeich.
              END.
              
              CREATE c-list. 
              ASSIGN 
                c-list.artnr       = l-artikel.artnr 
                c-list.bezeich     = l-artikel.bezeich 
                c-list.munit       = l-artikel.masseinheit 
                c-list.inhalt      = l-artikel.inhalt 
                c-list.zwkum       = l-artikel.zwkum 
                c-list.endkum      = l-artikel.endkum 
                c-list.qty         = l-op.anzahl 
                c-list.qty1        = l-op.deci1[1] - l-op.anzahl 
                c-list.fibukonto   = l-op.stornogrund 
                c-list.amount      = l-op.warenwert
                c-list.avrg-amount = l-op.warenwert / l-op.anzahl .
             
              tot-amount = tot-amount + l-op.warenwert.
              tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
              FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
              IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
          END.  
      END.
      ELSE IF sorttype = 4 THEN
      DO:
          RUN create-list.
          RUN get-l-artikels.
      END.
   END.     
END.

  
PROCEDURE create-list:
        FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE fDate AND h-bill-line.bill-datum LE tDate NO-LOCK,
            FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr NO-LOCK :

            FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr.
            IF AVAILABLE h-artikel AND h-artikel.artart = 0 THEN
            DO:
                FIND FIRST t-list WHERE t-list.dept = h-bill-line.departement
                    AND t-list.rechnr = h-bill-line.rechnr NO-ERROR.
                IF NOT AVAILABLE t-list THEN
                DO:
                    CREATE t-list.
                    ASSIGN
                     t-list.dept   = h-bill-line.departement
                     t-list.rechnr = h-bill-line.rechnr
                     t-list.pax    = h-bill.belegung.
                END.
            END.

    END.
END.

PROCEDURE get-l-artikels:
DEFINE VARIABLE do-it AS LOGICAL.
DEFINE VARIABLE pax   AS INTEGER INIT 0.

FOR EACH t-list: 
      FOR EACH h-bill-line WHERE h-bill-line.departement = t-list.dept
          AND h-bill-line.rechnr = t-list.rechnr NO-LOCK BY h-bill-line.rechnr .
          IF h-bill-line.artnr = 0 THEN .
          ELSE
          DO:
              FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
                    AND h-artikel.departement = h-bill-line.departement NO-LOCK NO-ERROR.
              IF NOT AVAILABLE h-artikel THEN .
              ELSE 
              IF h-artikel.artart EQ 0 THEN DO:
                  IF h-artikel.artnrlager NE 0 THEN   /* stock article */ 
                  DO: 
                      FIND FIRST l-artikel WHERE l-artikel.artnr = h-artikel.artnrlager AND l-artikel.bezeich = h-artikel.bezeich NO-LOCK NO-ERROR. 
                      IF AVAILABLE l-artikel AND l-artikel.endkum LE 2 THEN 
                      DO:
                          FIND FIRST c-list WHERE c-list.dept = t-list.dept
                              AND c-list.artnr = l-artikel.artnr 
                              AND c-list.fibukonto = c-list.fibukonto
                              AND c-list.item-artno = h-bill-line.artnr NO-ERROR.
                          IF NOT AVAILABLE c-list THEN DO:
                                  CREATE c-list.
                                  ASSIGN
                                  c-list.dept         = t-list.dept
                                  c-list.fibukonto    = t-list.fibukonto
                                  c-list.bezeich      = l-artikel.bezeich 
                                  c-list.artnr        = l-artikel.artnr
                                  c-list.price        = l-artikel.vk-preis
                                  c-list.store        = h-artikel.lagernr
                                  c-list.item-artno   = h-bill-line.artnr
                                  c-list.inhalt       = l-artikel.inhalt.
                          END.
                          
                          FOR EACH l-op WHERE l-op.lager-nr = h-artikel.lagernr AND l-op.op-art = 3 
                              AND l-op.datum GE fDate AND l-op.datum LE tDate 
                              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
                              AND l-op.loeschflag LE 1
                              AND l-op.anzahl NE 0
                              AND l-op.artnr = l-artikel.artnr NO-LOCK,
                              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum BY l-op.datum BY l-op.lscheinnr:
                                ASSIGN 
                                    c-list.qty         = l-op.anzahl
                                    c-list.qty1        = l-op.deci1[1] -  h-bill-line.anzahl
                                    c-list.fibukonto   = l-op.stornogrund 
                                    c-list.amount      = l-op.warenwert
                                    c-list.avrg-amount = l-op.warenwert / l-op.anzahl.

                                 tot-amount = tot-amount + l-op.warenwert.
                                 tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
                                 FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
                                 IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
                        END.
                      END.
                  END.
                  ELSE IF h-artikel.artnrrezept NE 0 THEN
                  DO:
                     FIND FIRST c-list WHERE c-list.dept = t-list.dept
                          AND c-list.artnr = h-artikel.artnr
                          AND c-list.fibukonto = c-list.fibukonto
                          AND c-list.item-artno = h-bill-line.artnr NO-ERROR.
                      IF NOT AVAILABLE c-list THEN DO:
                              ASSIGN pax = pax + t-list.pax.

                              CREATE c-list.
                              ASSIGN
                              c-list.dept         = t-list.dept
                              c-list.fibukonto    = t-list.fibukonto
                              c-list.bezeich      = h-artikel.bezeich + " - " + STRING(pax, ">>>9") + " pax"
                              c-list.artnr        = h-artikel.artnr
                              c-list.store        = h-artikel.lagernr
                              c-list.item-artno   = h-bill-line.artnr.
                      END.
                      ELSE ASSIGN c-list.qty1     = c-list.qty + h-bill-line.anzahl.
                     
                      FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-artikel.artnrrezept NO-LOCK NO-ERROR. 
                      IF AVAILABLE h-rezept THEN RUN get-recipe(h-rezept.artnrrezept, 1).
                  END.
                      
              END.
          END.                                          
      END.
  END.
END.

PROCEDURE get-recipe:
DEF INPUT PARAMETER p-artnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER menge   AS DECIMAL NO-UNDO.
DEF VARIABLE inh            AS DECIMAL NO-UNDO. 
DEF VARIABLE store-found    AS LOGICAL NO-UNDO INIT NO. 
DEF BUFFER h-recipe         FOR h-rezept.

  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    ASSIGN inh = menge * h-rezlin.menge / h-recipe.portion. 

    IF h-rezlin.recipe-flag = YES THEN RUN get-recipe2(h-rezlin.artnrlager, inh). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel AND l-artikel.endkum LE 2 THEN 
      DO:
        FIND FIRST c-list WHERE c-list.dept = t-list.dept
          AND c-list.artnr = l-artikel.artnr 
          /*AND c-list.fibukonto = t-list.fibukonto */
          AND c-list.item-artno = h-bill-line.artnr NO-ERROR.
        IF NOT AVAILABLE c-list THEN
        DO:
          CREATE c-list.
          ASSIGN
             c-list.bezeich      = l-artikel.bezeich
             c-list.dept         = t-list.dept
             c-list.fibukonto    = t-list.fibukonto 
             c-list.munit        = l-artikel.masseinheit 
             c-list.artnr        = l-artikel.artnr
             c-list.price        = l-artikel.vk-preis
             c-list.item-artno   = h-bill-line.artnr
             c-list.inhalt       = l-artikel.inhalt .

          /*hitung l-op*/
            FOR EACH l-op WHERE l-op.lager-nr = h-artikel.lagernr AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate 
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.artnr = l-artikel.artnr
              AND l-op.anzahl NE 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum BY l-op.datum BY l-op.lscheinnr:
                ASSIGN 
                    c-list.qty         = l-op.anzahl 
                    c-list.qty1        = l-op.deci1[1] - (h-bill-line.anzahl * inh) 
                    c-list.fibukonto   = l-op.stornogrund 
                    c-list.amount      = l-op.warenwert
                    c-list.avrg-amount = l-op.warenwert / l-op.anzahl.
                tot-amount = tot-amount + l-op.warenwert.
                tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
            END.

        END.
      END.
    END.
  END. 
END.

PROCEDURE get-recipe2:
DEF INPUT PARAMETER p-artnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER menge   AS DECIMAL NO-UNDO.
DEF VARIABLE inh            AS DECIMAL NO-UNDO. 
DEF VARIABLE store-found    AS LOGICAL NO-UNDO INIT NO. 
DEF BUFFER h-recipe         FOR h-rezept.

  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    ASSIGN inh = menge * h-rezlin.menge / h-recipe.portion. 

    IF h-rezlin.recipe-flag = YES THEN RUN get-recipe3(h-rezlin.artnrlager, inh). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel AND l-artikel.endkum LE 2 THEN 
      DO:
        FIND FIRST c-list WHERE c-list.dept = t-list.dept
          AND c-list.artnr = l-artikel.artnr 
          /*AND c-list.fibukonto = t-list.fibukonto*/
          AND c-list.item-artno = h-bill-line.artnr   NO-ERROR.
        IF NOT AVAILABLE c-list THEN
        DO:
          CREATE c-list. 
          ASSIGN
            c-list.bezeich      = l-artikel.bezeich
            c-list.dept         = t-list.dept
            c-list.fibukonto    = t-list.fibukonto
            c-list.munit        = l-artikel.masseinheit 
            c-list.artnr        = l-artikel.artnr
            c-list.price        = l-artikel.vk-preis
            c-list.qty1         = c-list.qty + h-bill-line.anzahl
            c-list.item-artno   = h-bill-line.artnr
            c-list.inhalt       = l-artikel.inhalt.

          /*hitung l-op*/
            FOR EACH l-op WHERE l-op.lager-nr = h-artikel.lagernr AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate 
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.artnr = l-artikel.artnr
              AND l-op.anzahl NE 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum BY l-op.datum BY l-op.lscheinnr:
                ASSIGN 
                    c-list.qty         = l-op.anzahl 
                    c-list.qty1        = l-op.deci1[1] - (h-bill-line.anzahl * inh) 
                    c-list.fibukonto   = l-op.stornogrund 
                    c-list.amount      = l-op.warenwert
                    c-list.avrg-amount = l-op.warenwert / l-op.anzahl.
    
                tot-amount = tot-amount + l-op.warenwert.
                tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
            END.
        END.
      END.
    END.
  END. 
END.


PROCEDURE get-recipe3:
DEF INPUT PARAMETER p-artnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER menge   AS DECIMAL NO-UNDO.
DEF VARIABLE inh            AS DECIMAL NO-UNDO. 
DEF VARIABLE store-found    AS LOGICAL NO-UNDO INIT NO. 
DEF BUFFER h-recipe         FOR h-rezept.

  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    ASSIGN inh = menge * h-rezlin.menge / h-recipe.portion. 

    IF h-rezlin.recipe-flag = YES THEN RUN get-recipe4(h-rezlin.artnrlager, inh). 
    ELSE 
    DO:
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel AND l-artikel.endkum LE 2 THEN 
      DO:
        FIND FIRST c-list WHERE c-list.dept = t-list.dept
          AND c-list.artnr = l-artikel.artnr 
          /*AND c-list.fibukonto = t-list.fibukonto */
          AND c-list.item-artno = h-bill-line.artnr NO-ERROR.
        IF NOT AVAILABLE c-list THEN
        DO:
          CREATE c-list. 
          ASSIGN
            c-list.bezeich      = l-artikel.bezeich
            c-list.dept         = t-list.dept
            c-list.fibukonto    = t-list.fibukonto
            c-list.artnr        = l-artikel.artnr
            c-list.munit        = l-artikel.masseinheit 
            c-list.price        = l-artikel.vk-preis
            c-list.item-artno   = h-bill-line.artnr
            c-list.inhalt       = l-artikel.inhalt .

          /*hitung l-op*/
            FOR EACH l-op WHERE l-op.lager-nr = h-artikel.lagernr AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate 
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.artnr = l-artikel.artnr
              AND l-op.anzahl NE 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum BY l-op.datum BY l-op.lscheinnr:
                ASSIGN 
                    c-list.qty         = l-op.anzahl 
                    c-list.qty1        = l-op.deci1[1] - (h-bill-line.anzahl * inh)
                    c-list.fibukonto   = l-op.stornogrund 
                    c-list.amount      = l-op.warenwert
                    c-list.avrg-amount = l-op.warenwert / l-op.anzahl.
                tot-amount = tot-amount + l-op.warenwert.
                tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
            END.
        END.        
      END.
    END.
  END. 
END.

PROCEDURE get-recipe4:
DEF INPUT PARAMETER p-artnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER menge   AS DECIMAL NO-UNDO.
DEF VARIABLE inh            AS DECIMAL NO-UNDO. 
DEF VARIABLE store-found    AS LOGICAL NO-UNDO INIT NO. 
DEF BUFFER h-recipe         FOR h-rezept.

  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 

    ASSIGN inh = menge * h-rezlin.menge / h-recipe.portion. 

    IF h-rezlin.recipe-flag = YES THEN RUN get-recipe5(h-rezlin.artnrlager, inh). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel AND l-artikel.endkum LE 2 THEN 
      DO:
        FIND FIRST c-list WHERE c-list.dept = t-list.dept
          AND c-list.artnr = l-artikel.artnr 
          AND c-list.fibukonto = t-list.fibukonto 
          AND c-list.item-artno = h-bill-line.artnr NO-ERROR.
        IF NOT AVAILABLE c-list THEN
        DO: 
          CREATE c-list.
          ASSIGN
            c-list.bezeich      = l-artikel.bezeich
            c-list.dept         = t-list.dept
            c-list.fibukonto    = t-list.fibukonto
            c-list.artnr        = l-artikel.artnr
            c-list.price        = l-artikel.vk-preis
            c-list.munit        = l-artikel.masseinheit 
            c-list.qty1         = c-list.qty + h-bill-line.anzahl
            c-list.item-artno   = h-bill-line.artnr
            c-list.inhalt       = l-artikel.inhalt .
            
            /*hitung l-op*/
            FOR EACH l-op WHERE l-op.lager-nr = h-artikel.lagernr AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate 
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.artnr = l-artikel.artnr
              AND l-op.anzahl NE 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum BY l-op.datum BY l-op.lscheinnr:
                ASSIGN 
                    c-list.qty         = l-op.anzahl 
                    c-list.qty1        = l-op.deci1[1] - (h-bill-line.anzahl * inh) 
                    c-list.fibukonto   = l-op.stornogrund 
                    c-list.amount      = l-op.warenwert
                    c-list.avrg-amount = l-op.warenwert / l-op.anzahl.
                tot-amount = tot-amount + l-op.warenwert.
                tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
            END.
        END.
      END.
    END.
  END. 
END.


PROCEDURE get-recipe5:
DEF INPUT PARAMETER p-artnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER menge   AS DECIMAL NO-UNDO.
DEF VARIABLE inh            AS DECIMAL NO-UNDO. 
DEF VARIABLE store-found    AS LOGICAL NO-UNDO INIT NO. 
DEF BUFFER h-recipe         FOR h-rezept.

  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 

    ASSIGN inh = menge * h-rezlin.menge / h-recipe.portion. 

    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel AND l-artikel.endkum LE 2 THEN 
      DO:
        FIND FIRST c-list WHERE c-list.dept = t-list.dept
          AND c-list.artnr = l-artikel.artnr 
          AND c-list.fibukonto = t-list.fibukonto 
          AND c-list.item-artno = h-bill-line.artnr NO-ERROR.
        IF NOT AVAILABLE c-list THEN
        DO:
          CREATE c-list.
          ASSIGN
            c-list.bezeich      = l-artikel.bezeich
            c-list.dept         = t-list.dept
            c-list.fibukonto    = t-list.fibukonto
            c-list.artnr        = l-artikel.artnr
            c-list.price        = l-artikel.vk-preis
            c-list.munit        = l-artikel.masseinheit 
            c-list.qty1         = c-list.qty + h-bill-line.anzahl
            c-list.item-artno   = h-bill-line.artnr
            c-list.inhalt       = l-artikel.inhalt.

          /*hitung l-op*/
            FOR EACH l-op WHERE l-op.lager-nr = h-artikel.lagernr AND l-op.op-art = 3 
              AND l-op.datum GE fDate AND l-op.datum LE tDate 
              AND (SUBSTR(l-op.lscheinnr,1,3) = "SAD") 
              AND l-op.loeschflag LE 1
              AND l-op.artnr = l-artikel.artnr
              AND l-op.anzahl NE 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum BY l-op.datum BY l-op.lscheinnr:
                ASSIGN 
                    c-list.qty         = l-op.anzahl 
                    c-list.qty1        = l-op.deci1[1] - (h-bill-line.anzahl * inh) 
                    c-list.fibukonto   = l-op.stornogrund 
                    c-list.amount      = l-op.warenwert
                    c-list.avrg-amount = l-op.warenwert / l-op.anzahl.
                
                tot-amount = tot-amount + l-op.warenwert.
                tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
            END.
        END.
      END.
    END.
  END.
END. 

