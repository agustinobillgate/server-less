
/*MT 29/10/14 --> delete all about translateExtended
{supertrans.i} 
DEF VAR lvCAREA AS CHAR INITIAL "nt-autodeduct". 
*/
/*
RUN add-persist-procedure. 
PROCEDURE add-persist-procedure: 
    DEFINE VARIABLE lvHS AS HANDLE              NO-UNDO. 
    DEFINE VARIABLE lvI AS INTEGER              NO-UNDO. 
    DEFINE VARIABLE lFound AS LOGICAL INIT FALSE    NO-UNDO. 
 
    DO lvI = 1 TO NUM-ENTRIES(SESSION:SUPER-PROCEDURES): 
        lvHS = WIDGET-HANDLE(ENTRY(lvI, SESSION:SUPER-PROCEDURES)). 
        IF VALID-HANDLE(lvHS) THEN DO: 
            IF lvHS:NAME BEGINS "supertrans" THEN 
                lFound = TRUE. 
        END. 
    END. 
 
    IF NOT lFound THEN DO: 
        RUN supertrans.p PERSISTENT SET lvHS. 
        SESSION:ADD-SUPER-PROCEDURE(lvHS). 
    END. 
END. 
*/

DEF TEMP-TABLE s-list
    FIELD dept      AS INTEGER
    FIELD store     AS INTEGER INITIAL 0
    FIELD artnr     AS INTEGER
    FIELD price     AS DECIMAL
    FIELD qty       AS DECIMAL FORMAT ">>9.999"
    FIELD fibukonto AS CHAR INIT "0000000000"
    INDEX dept_ix dept.
.

DEF TEMP-TABLE t-list
    FIELD dept      AS INTEGER
    FIELD rechnr    AS INTEGER
    FIELD pay       AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD rmTrans   AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD compli    AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD coupon    AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD fibukonto AS CHAR INIT "0000000000"
.

DEF VAR bill-date       AS DATE             NO-UNDO.
DEF VAR inv-closeDate   AS DATE             NO-UNDO.
DEF VAR food-closeDate  AS DATE             NO-UNDO.
DEF VAR transDate       AS DATE             NO-UNDO.
DEF VAR deductFlag      AS LOGICAL INIT YES NO-UNDO.
DEF VAR mm1             AS INTEGER          NO-UNDO.
DEF VAR yy1             AS INTEGER          NO-UNDO.
DEF VAR mm2             AS INTEGER          NO-UNDO.
DEF VAR yy2             AS INTEGER          NO-UNDO.
DEF VAR deduct-compli   AS LOGICAL          NO-UNDO.

DEFINE VARIABLE to-date      AS DATE. 
DEFINE VARIABLE from-date    AS DATE. 

DEFINE VARIABLE main-grp1    AS INTEGER. 
DEFINE VARIABLE main-grp2    AS INTEGER. 
DEFINE VARIABLE main-grp3    AS INTEGER. 

RUN htpdate.p  (110, OUTPUT bill-date). /*Invoicing DATE */
RUN htpdate.p  (224, OUTPUT inv-closedate). 
RUN htpdate.p  (221, OUTPUT food-closedate). 

RUN htplogic.p (947, OUTPUT deduct-compli).

FIND FIRST htparam WHERE htparam.paramnr = 257 NO-LOCK. 
main-grp1 = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 258 NO-LOCK. 
main-grp2 = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 268 NO-LOCK. 
main-grp3 = htparam.finteger. 

IF main-grp1 = 1 OR main-grp2 = 2 THEN
    FIND FIRST htparam WHERE paramnr = 224 NO-LOCK.
ELSE FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
to-date = htparam.fdate. 
from-date = DATE(MONTH(to-date), 1, year(to-date)).

ASSIGN
  transDate = bill-date
  mm1       = MONTH(bill-date)
  yy1       = YEAR(bill-date)
  mm2       = MONTH(inv-closeDate)
  yy2       = YEAR(inv-closeDate).

IF (mm1 LT mm2) OR (yy1 LT yy2) THEN  /* Inventory early closing */
ASSIGN transdate  = DATE(mm2, 1, yy2).

IF (mm1 GT mm2) OR (yy1 GT yy2) THEN  /* Inventory not closing yet */
ASSIGN deductFlag = NO.

RUN create-list.
RUN get-l-artikels.
RUN create-outgoing.

PROCEDURE create-list:

  FOR EACH h-bill-line WHERE h-bill-line.bill-datum = bill-date NO-LOCK
    BY h-bill-line.departement BY h-bill-line.rechnr:
      
    FIND FIRST t-list WHERE t-list.dept = h-bill-line.departement
      AND t-list.rechnr = h-bill-line.rechnr NO-ERROR.
    IF NOT AVAILABLE t-list THEN
    DO:
      CREATE t-list.
      ASSIGN
        t-list.dept   = h-bill-line.departement
        t-list.rechnr = h-bill-line.rechnr
      .
    END.
  
    IF h-bill-line.artnr = 0 THEN
    DO:
      IF h-bill-line.bezeich MATCHES("*RmNo*") THEN 
        t-list.rmTrans = t-list.rmTrans + h-bill-line.betrag.
      ELSE t-list.pay = t-list.pay + h-bill-line.betrag.
    END.
    ELSE
    DO:
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
        AND h-artikel.departement = h-bill-line.departement NO-LOCK NO-ERROR.
      IF NOT AVAILABLE h-artikel THEN .
      ELSE IF AVAILABLE h-artikel THEN DO:
          IF h-artikel.artart EQ 0 THEN DO: 
              FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                  AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
              IF AVAILABLE artikel THEN DO:
                  ASSIGN t-list.fibukonto = artikel.bezeich1.
              END.
          END.
          ELSE 
          DO:
            IF h-artikel.artart LE 7 THEN 
              t-list.pay = t-list.pay - h-bill-line.betrag.
            ELSE IF h-artikel.artart = 11 THEN 
            DO:
              t-list.compli = t-list.compli - h-bill-line.betrag.  
            END.
            ELSE IF h-artikel.artart = 12 THEN 
              t-list.coupon = t-list.coupon - h-bill-line.betrag. 
          END.
      END.      
    END.
  END.
END.

PROCEDURE get-l-artikels:
DEF VAR do-it AS LOGICAL.
  FOR EACH t-list WHERE /*t-list.pay NE 0*/ t-list.pay GE 0 OR t-list.rmTrans NE 0
    OR t-list.compli NE 0 OR t-list.coupon NE 0:

    IF t-list.compli NE 0 THEN do-it = deduct-compli.
    ELSE do-it = YES.
    IF t-list.coupon NE 0 THEN do-it = deduct-compli.
    ELSE do-it = YES.  /*FTautodeduct for meal coupon*/

    IF do-it THEN
    FOR EACH h-bill-line WHERE h-bill-line.departement = t-list.dept
      AND h-bill-line.rechnr = t-list.rechnr
      AND h-bill-line.steuercode NE 99999 /*ITA 221216 yang tersplit tidak ikut kehitung*/ 
      NO-LOCK:
      IF h-bill-line.artnr = 0 THEN .
      ELSE
      DO:
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
          AND h-artikel.departement = h-bill-line.departement 
          NO-LOCK NO-ERROR.
        IF NOT AVAILABLE h-artikel THEN .
        ELSE IF h-artikel.artart EQ 0 THEN
        DO:
          IF h-artikel.artnrlager NE 0 THEN   /* stock article */ 
          DO: 
            FIND FIRST l-artikel WHERE l-artikel.artnr = h-artikel.artnrlager 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE l-artikel /*AND l-artikel.endkum LE 2*/ THEN 
            DO:
              FIND FIRST s-list WHERE s-list.dept = t-list.dept
                AND s-list.artnr = l-artikel.artnr 
                AND s-list.fibukonto = t-list.fibukonto NO-ERROR.
              IF NOT AVAILABLE s-list THEN
              DO:
                CREATE s-list.
                ASSIGN
                  s-list.dept       = t-list.dept                  
                  s-list.artnr      = l-artikel.artnr
                  s-list.price      = l-artikel.vk-preis
                  s-list.store      = h-artikel.lagernr
                .

                FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                  AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                        ASSIGN s-list.fibukonto  = artikel.bezeich1.

              END.
              s-list.qty = s-list.qty + h-bill-line.anzahl.
            END.
          END.
          ELSE IF h-artikel.artnrrezept NE 0 THEN
          DO:
            FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-artikel.artnrrezept 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE h-rezept THEN 
              RUN get-recipe(h-rezept.artnrrezept, 1). 
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
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel /*AND l-artikel.endkum LE 2*/ THEN 
      DO:
        FIND FIRST s-list WHERE s-list.dept = t-list.dept
          AND s-list.artnr = l-artikel.artnr 
          AND s-list.fibukonto = t-list.fibukonto NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN
            s-list.dept         = t-list.dept
            /*s-list.fibukonto    = t-list.fibukonto*/
            s-list.artnr        = l-artikel.artnr
            s-list.price        = l-artikel.vk-preis
          .

          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
              AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN ASSIGN s-list.fibukonto  = artikel.bezeich1.

          IF h-artikel.lagernr NE 0 THEN
          DO:
            FIND FIRST l-lager WHERE l-lager.lager-nr = h-artikel.lagernr
                NO-LOCK NO-ERROR.
            IF AVAILABLE l-lager THEN
            ASSIGN
                store-found  = YES
                s-list.store = h-artikel.lagernr
            .
          END.
          IF NOT store-found THEN
          DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = s-list.dept NO-LOCK.
            ASSIGN s-list.store = hoteldpt.betriebsnr.
          END.
        END.
        
        ASSIGN inh = inh / l-art.inhalt /*ITA*/
               s-list.qty = s-list.qty + h-bill-line.anzahl * inh.
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
      IF AVAILABLE l-artikel /*AND l-artikel.endkum LE 2*/ THEN 
      DO:
        FIND FIRST s-list WHERE s-list.dept = t-list.dept
          AND s-list.artnr = l-artikel.artnr 
          AND s-list.fibukonto = t-list.fibukonto NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN
            s-list.dept         = t-list.dept
            /*s-list.fibukonto    = t-list.fibukonto*/
            s-list.artnr        = l-artikel.artnr
            s-list.price        = l-artikel.vk-preis
          .

          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
              AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN ASSIGN s-list.fibukonto  = artikel.bezeich1.

          IF h-artikel.lagernr NE 0 THEN
          DO:
            FIND FIRST l-lager WHERE l-lager.lager-nr = h-artikel.lagernr
                NO-LOCK NO-ERROR.
            IF AVAILABLE l-lager THEN
            ASSIGN
                store-found  = YES
                s-list.store = h-artikel.lagernr
            .
          END.
          IF NOT store-found THEN
          DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = s-list.dept NO-LOCK.
            ASSIGN s-list.store = hoteldpt.betriebsnr.
          END.
        END.

        ASSIGN inh = inh / l-art.inhalt /*ITA*/
               s-list.qty = s-list.qty + h-bill-line.anzahl * inh.
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
      IF AVAILABLE l-artikel /*AND l-artikel.endkum LE 2*/ THEN 
      DO:
        FIND FIRST s-list WHERE s-list.dept = t-list.dept
          AND s-list.artnr = l-artikel.artnr 
          AND s-list.fibukonto = t-list.fibukonto NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN
            s-list.dept         = t-list.dept
            /*s-list.fibukonto    = t-list.fibukonto*/
            s-list.artnr        = l-artikel.artnr
            s-list.price        = l-artikel.vk-preis
          .

          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
              AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN ASSIGN s-list.fibukonto  = artikel.bezeich1.

          IF h-artikel.lagernr NE 0 THEN
          DO:
            FIND FIRST l-lager WHERE l-lager.lager-nr = h-artikel.lagernr
                NO-LOCK NO-ERROR.
            IF AVAILABLE l-lager THEN
            ASSIGN
                store-found  = YES
                s-list.store = h-artikel.lagernr
            .
          END.
          IF NOT store-found THEN
          DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = s-list.dept NO-LOCK.
            ASSIGN s-list.store = hoteldpt.betriebsnr.
          END.
        END.
        ASSIGN inh = inh / l-art.inhalt /*ITA*/
               s-list.qty = s-list.qty + h-bill-line.anzahl * inh.
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
      IF AVAILABLE l-artikel /*AND l-artikel.endkum LE 2*/ THEN 
      DO:
        FIND FIRST s-list WHERE s-list.dept = t-list.dept
          AND s-list.artnr = l-artikel.artnr 
          AND s-list.fibukonto = t-list.fibukonto NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN
            s-list.dept         = t-list.dept
            /*s-list.fibukonto    = t-list.fibukonto*/
            s-list.artnr        = l-artikel.artnr
            s-list.price        = l-artikel.vk-preis
          .

          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
               AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN ASSIGN s-list.fibukonto  = artikel.bezeich1.

          IF h-artikel.lagernr NE 0 THEN
          DO:
            FIND FIRST l-lager WHERE l-lager.lager-nr = h-artikel.lagernr
                NO-LOCK NO-ERROR.
            IF AVAILABLE l-lager THEN
            ASSIGN
                store-found  = YES
                s-list.store = h-artikel.lagernr
            .
          END.
          IF NOT store-found THEN
          DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = s-list.dept NO-LOCK.
            ASSIGN s-list.store = hoteldpt.betriebsnr.
          END.
        END.
        ASSIGN inh = inh / l-art.inhalt /*ITA*/
               s-list.qty = s-list.qty + h-bill-line.anzahl * inh.
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

    /*IF h-rezlin.recipe-flag = YES THEN RUN get-recipe2(h-rezlin.artnrlager, inh). 
    ELSE */
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel /*AND l-artikel.endkum LE 2*/ THEN 
      DO:
        FIND FIRST s-list WHERE s-list.dept = t-list.dept
          AND s-list.artnr = l-artikel.artnr 
          AND s-list.fibukonto = t-list.fibukonto NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN
            s-list.dept         = t-list.dept
            /*s-list.fibukonto    = t-list.fibukonto*/
            s-list.artnr        = l-artikel.artnr
            s-list.price        = l-artikel.vk-preis
          .

          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN ASSIGN s-list.fibukonto  = artikel.bezeich1.

          IF h-artikel.lagernr NE 0 THEN
          DO:
            FIND FIRST l-lager WHERE l-lager.lager-nr = h-artikel.lagernr
                NO-LOCK NO-ERROR.
            IF AVAILABLE l-lager THEN
            ASSIGN
                store-found  = YES
                s-list.store = h-artikel.lagernr
            .
          END.
          IF NOT store-found THEN
          DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = s-list.dept NO-LOCK.
            ASSIGN s-list.store = hoteldpt.betriebsnr.
          END.
        END.
        ASSIGN inh = inh / l-art.inhalt /*ITA*/
               s-list.qty = s-list.qty + h-bill-line.anzahl * inh.
      END.
    END.
  END. 
END.

PROCEDURE create-outgoing:
DEF VAR curr-dept   AS INTEGER INIT -1  NO-UNDO.
DEF VAR lscheinnr   AS CHAR             NO-UNDO.
DEF VAR curr-lager  AS INTEGER          NO-UNDO.
DEF VAR curr-onhand AS DECIMAL          NO-UNDO.

DEF BUFFER sbuff FOR s-list.

  FIND FIRST s-list WHERE s-list.store = 0 USE-INDEX dept_ix NO-ERROR.
  DO WHILE AVAILABLE s-list:
    FIND FIRST hoteldpt WHERE hoteldpt.num = s-list.dept NO-LOCK.
    curr-lager = hoteldpt.betriebsnr.
    IF curr-lager = 0 THEN .
    ELSE ASSIGN s-list.store = curr-lager.
    FIND NEXT s-list WHERE s-list.store = 0 USE-INDEX dept_ix NO-LOCK NO-ERROR.
  END.

  FOR EACH s-list WHERE s-list.store = 0 OR s-list.qty = 0:
      DELETE s-list.
  END.

  IF mm1 = mm2 THEN
  FOR EACH s-list BY s-list.store:
    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STT"
      AND SUBSTR(l-ophdr.lscheinnr,1,3) = "INV"
      AND l-ophdr.datum GE bill-date 
      AND l-ophdr.lager-nr = s-list.store NO-LOCK NO-ERROR.
    IF AVAILABLE l-ophdr THEN
    FOR EACH sbuff WHERE sbuff.store = s-list.store:
      DELETE sbuff.
    END.
  END.

  FOR EACH s-list BY s-list.dept:
    IF curr-dept NE s-list.dept THEN
    DO:
      lscheinnr = "SAD" + SUBSTR(STRING(YEAR(transdate)),3,2) + STRING(MONTH(transDate),"99") 
        + STRING(DAY(transDate),"99") + "-" + STRING(s-list.dept,"99"). 
      CREATE l-ophdr. 
      ASSIGN
        l-ophdr.datum     =  transdate
        l-ophdr.lager-nr  = s-list.store
        l-ophdr.docu-nr   = lscheinnr 
        l-ophdr.lscheinnr = lscheinnr 
        l-ophdr.op-typ    = "STT"
        l-ophdr.fibukonto = s-list.fibukonto
        curr-dept         = s-list.dept
      . 
      FIND CURRENT l-ophdr NO-LOCK.
    END.
    CREATE l-op.
    ASSIGN 
      l-op.datum          = transDate 
      l-op.lager-nr       = s-list.store 
      l-op.artnr          = s-list.artnr 
      l-op.zeit           = TIME 
      l-op.anzahl         = s-list.qty
      l-op.einzelpreis    = s-list.price 
      l-op.warenwert      = s-list.qty * s-list.price
      l-op.op-art         = 3 
      l-op.herkunftflag   = 4    /* 4 = inventory !!! */ 
      l-op.lscheinnr      = lscheinnr 
      l-op.pos            = 1 
      l-op.fuellflag      = 0
    . 
    IF DECIMAL(s-list.fibukonto) NE 0 THEN
      l-op.stornogrund = s-list.fibukonto.

    FIND CURRENT l-op NO-LOCK.     
  END.


  IF deductFlag THEN DO:
      /*INIT ONHAND*/
      RUN init-onhand.
        
      /*Incoming Stock*/
      FOR EACH l-op WHERE (op-art = 1 OR op-art = 2) AND l-op.loeschflag LT 2 
        AND (l-op.datum GE from-date AND l-op.datum LE to-date) 
        AND l-op.pos GE 1 AND l-op.lager-nr GT 0 NO-LOCK BY l-op.artnr: 
        FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR. 
        IF AVAILABLE l-artikel THEN RUN update-eingang.
      END. 
    
      /*outgoing stock*/
      FOR EACH l-op WHERE (op-art = 3 OR op-art = 4) AND l-op.loeschflag LT 2 
            AND (l-op.datum GE from-date AND l-op.datum LE to-date) 
            AND l-op.pos GE 1 AND l-op.lager-nr GT 0 NO-LOCK BY l-op.artnr: 
            FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR. 
            IF AVAILABLE l-artikel THEN RUN update-ausgang.
      END. 
  END.
END.

PROCEDURE init-onhand:
DEF BUFFER l-oh FOR l-bestand.
DEF BUFFER buf-lart FOR l-artikel.
  
  FIND FIRST l-oh WHERE l-oh.lager-nr EQ 0 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE l-oh:
    DO TRANSACTION: 
        FIND FIRST buf-lart WHERE buf-lart.artnr = l-oh.artnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE buf-lart THEN 
        DO:
          FIND FIRST l-bestand WHERE RECID(l-bestand) = RECID(l-oh).
          ASSIGN
            l-bestand.anz-eingang  = 0
            l-bestand.wert-eingang = 0 
            l-bestand.anz-ausgang  = 0 
            l-bestand.wert-ausgang = 0
          . 
          FIND CURRENT l-bestand NO-LOCK.
        END.
    END. 
    FIND NEXT l-oh WHERE l-oh.lager-nr EQ 0 NO-LOCK NO-ERROR. 
  END.

  FIND FIRST l-lager NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE l-lager:
    FIND FIRST l-oh WHERE l-oh.lager-nr EQ l-lager.lager-nr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-oh:
        DO TRANSACTION:
            FIND FIRST buf-lart WHERE buf-lart.artnr = l-oh.artnr NO-LOCK NO-ERROR. 
            IF AVAILABLE buf-lart THEN 
            DO:
                FIND FIRST l-bestand WHERE RECID(l-bestand) = RECID(l-oh).
                ASSIGN
                  l-bestand.anz-eingang  = 0 
                  l-bestand.wert-eingang = 0 
                  l-bestand.anz-ausgang  = 0 
                  l-bestand.wert-ausgang = 0
                .
                FIND CURRENT l-bestand NO-LOCK.
            END.
            FIND NEXT l-oh WHERE l-oh.lager-nr EQ l-lager.lager-nr NO-LOCK NO-ERROR.
        END.
    END.
    FIND NEXT l-lager NO-LOCK NO-ERROR.
  END.
END. 

PROCEDURE update-eingang: 
DEFINE VARIABLE s-artnr     AS INTEGER NO-UNDO. 
DEFINE VARIABLE anzahl      AS DECIMAL FORMAT "->,>>>,>>9.999" NO-UNDO. 
DEFINE VARIABLE wert        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE transdate   AS DATE    NO-UNDO. 
DEFINE VARIABLE curr-lager  AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-anz     AS DECIMAL FORMAT "->,>>>,>>9.999" NO-UNDO. 
DEFINE VARIABLE tot-wert    AS DECIMAL. 
DEFINE VARIABLE avrg-price  AS DECIMAL FORMAT "->>>,>>>,>>9.999999" INITIAL 0. 
  
  ASSIGN
    s-artnr     = l-op.artnr
    anzahl      = l-op.anzahl 
    wert        = l-op.warenwert 
    transdate   = l-op.datum
    curr-lager  = l-op.lager-nr
  . 

  DO TRANSACTION:
/* UPDATE stock onhand  IF NOT transferred*/ 
    IF l-op.op-art = 1 OR (l-op.op-art = 2 AND l-op.herkunftflag = 3) THEN 
    DO: 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
        l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO: 
        CREATE l-bestand. 
        ASSIGN
          l-bestand.artnr = s-artnr
          l-bestand.anf-best-dat = transdate. 
      END. 
      ASSIGN
        l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl
        l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      CREATE l-bestand. 
      ASSIGN
        l-bestand.lager-nr = curr-lager
        l-bestand.artnr = s-artnr
        l-bestand.anf-best-dat = transdate. 
    END. 
    ASSIGN
      l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 
END.

PROCEDURE update-ausgang: 
DEFINE VARIABLE s-artnr         AS INTEGER NO-UNDO. 
DEFINE VARIABLE anzahl          AS DECIMAL FORMAT "->,>>>,>>9.999" NO-UNDO. 
DEFINE VARIABLE wert            AS DECIMAL NO-UNDO. 
DEFINE VARIABLE transdate       AS DATE    NO-UNDO. 
DEFINE VARIABLE curr-lager      AS INTEGER NO-UNDO. 
 
  ASSIGN
    s-artnr     = l-op.artnr 
    anzahl      = l-op.anzahl 
    wert        = l-op.warenwert 
    transdate   = l-op.datum
    curr-lager  = l-op.lager-nr
  . 
 
  DO TRANSACTION:
/* UPDATE stock onhand IF NOT transferred */ 
    IF l-op.op-art EQ 3 OR (l-op.op-art = 4 AND l-op.herkunftflag = 3) THEN 
    DO: 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
        l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO: 
        CREATE l-bestand. 
        ASSIGN
          l-bestand.artnr = s-artnr
          l-bestand.anf-best-dat = transdate. 
      END. 
      ASSIGN
        l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl
        l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      CREATE l-bestand. 
      ASSIGN
        l-bestand.lager-nr = curr-lager
        l-bestand.artnr = s-artnr
        l-bestand.anf-best-dat = transdate. 
    END. 
    ASSIGN
      l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl
      l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 
END.


