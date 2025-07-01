
DEFINE INPUT  PARAMETER case-type   AS INTEGER        NO-UNDO.
DEFINE OUTPUT PARAMETER i           AS INTEGER INIT 0 NO-UNDO.
DEFINE OUTPUT PARAMETER j           AS INTEGER INIT 0 NO-UNDO.

DEFINE VARIABLE anz     AS INTEGER  NO-UNDO INIT 762. 
DEFINE VARIABLE ci-date AS DATE     NO-UNDO.

/* storage duration for FO statistic */
FIND FIRST htparam WHERE paramnr = 277 NO-LOCK.  
IF htparam.paramgr = 9 AND htparam.finteger NE 0 THEN
  ASSIGN anz = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

/* SY 04 June 2016 */
RUN check-co-guestbill.

IF case-type = 1 THEN RUN del-old-stat1.
ELSE IF case-type = 2  THEN RUN del-old-stat2.
ELSE IF case-type = 3  THEN RUN del-old-stat3.
ELSE IF case-type = 4  THEN RUN del-old-stat4.
ELSE IF case-type = 41 THEN RUN del-old-stat41.
ELSE IF case-type = 5  THEN RUN del-old-stat5.
ELSE IF case-type = 6  THEN RUN del-old-stat6.
ELSE IF case-type = 7  THEN RUN del-old-stat7.
ELSE IF case-type = 8  THEN RUN del-old-stat8.
ELSE IF case-type = 9  THEN RUN del-old-stat9.
ELSE IF case-type = 999  THEN RUN del-dml.


/* SY 04 June 2016 */
PROCEDURE check-co-guestbill:
DEF BUFFER bbuff FOR bill.
DEF VARIABLE bl-saldo  AS DECIMAL NO-UNDO.
DEF VARIABLE bl-saldo2 AS DECIMAL NO-UNDO.

   FIND FIRST bill WHERE bill.resnr GT 0 AND bill.reslinnr GT 0
       AND bill.flag = 0 AND bill.saldo = 0 NO-LOCK NO-ERROR.
   DO WHILE AVAILABLE bill:
       FIND FIRST res-line WHERE res-line.resnr = bill.resnr
           AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
       IF NOT AVAILABLE res-line THEN
       DO:
           FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
               EXCLUSIVE-LOCK.
           bbuff.flag = 1.
           FIND CURRENT bbuff NO-LOCK.
           RELEASE bbuff.
       END.
       ELSE IF res-line.active-flag = 2 THEN
       DO:
           FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
               EXCLUSIVE-LOCK.
           bbuff.flag = 1.
           FIND CURRENT bbuff NO-LOCK.
           RELEASE bbuff.
       END.
       FIND NEXT bill WHERE bill.resnr GT 0 AND bill.reslinnr GT 0
          AND bill.flag = 0 AND bill.saldo = 0 NO-LOCK NO-ERROR.
   END.

   /*ITA 130616 cek billsaldo = pertambahan semua transaksi*/
   FIND FIRST bill WHERE bill.flag = 0 AND bill.rechnr GT 0
       NO-LOCK NO-ERROR.
   DO WHILE AVAILABLE bill:
       ASSIGN bl-saldo = 0.
       FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
           ASSIGN bl-saldo = bl-saldo + bill-line.betrag.
       END.

       IF bl-saldo NE bill.saldo THEN DO:
           FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
               EXCLUSIVE-LOCK.
           bbuff.saldo = bl-saldo.
           FIND CURRENT bbuff NO-LOCK.
           RELEASE bbuff.
       END.
       FIND NEXT bill WHERE bill.flag = 0 AND bill.rechnr GT 0
            NO-LOCK NO-ERROR. 
   END.
   /*end*/


   FOR EACH res-line WHERE res-line.active-flag = 1
       AND res-line.resstatus NE 12 
       AND res-line.l-zuordnung[3] = 0 NO-LOCK:
       FIND FIRST bill WHERE bill.resnr = res-line.resnr 
           AND bill.parent-nr = res-line.reslinnr NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE bill:
           ASSIGN bl-saldo2 = 0.
           
           FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
               ASSIGN bl-saldo2 = bl-saldo2 + bill-line.betrag.
           END.

           IF bill.zinr NE res-line.zinr THEN
           DO:
               FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                   EXCLUSIVE-LOCK.
               bbuff.zinr = res-line.zinr.
               FIND CURRENT bbuff NO-LOCK.
               RELEASE bbuff.
           END.
            
           /*ITA 130616 cek billsaldo = pertambahan semua transaksi*/
           IF bl-saldo2 NE bill.saldo THEN DO:
               FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                   EXCLUSIVE-LOCK.
               bbuff.saldo = bl-saldo2.
               FIND CURRENT bbuff NO-LOCK.
               RELEASE bbuff.
           END.
           FIND NEXT bill WHERE bill.resnr = res-line.resnr 
              AND bill.parent-nr = res-line.reslinnr NO-LOCK NO-ERROR.
       END.   
   END.
END.

PROCEDURE del-old-stat1: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  DO TRANSACTION: 
    FOR EACH zimmer NO-LOCK: 
      FIND FIRST zinrstat WHERE zinrstat.datum LE curr-date 
        AND zinrstat.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
      DO WHILE AVAILABLE zinrstat: 
        i = i + 1.
        FIND CURRENT zinrstat EXCLUSIVE-LOCK. 
        DELETE zinrstat. 
        FIND NEXT zinrstat WHERE zinrstat.datum LE curr-date 
          AND zinrstat.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
      END. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "ooo" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "SegArr" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "ArgArr" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "CatArr" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "SegDep" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "ArgDep" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "CatDep" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "SegInh" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
 
    FOR EACH zinrstat WHERE zinrstat.zinr = "ArgInh" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
    FOR EACH zinrstat WHERE zinrstat.zinr = "CatInh" 
      AND zinrstat.datum LE (ci-date - anz): 
      DELETE zinrstat. 
    END. 
  END. 
END. 


PROCEDURE del-old-stat2: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FOR EACH zimkateg NO-LOCK: 
    FIND FIRST zkstat WHERE zkstat.datum LE curr-date 
    AND zkstat.zikatnr = zimkateg.zikatnr 
      NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE zkstat: 
       DO TRANSACTION: 
        i = i + 1.
        FIND CURRENT zkstat EXCLUSIVE-LOCK. 
        DELETE zkstat. 
      END. 
      FIND NEXT zkstat WHERE zkstat.datum LE curr-date 
        AND zkstat.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR. 
    END. 
  END. 
END. 


PROCEDURE del-old-stat3: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FOR EACH sourccod NO-LOCK: 
    FIND FIRST sources WHERE sources.datum LE curr-date 
      AND sources.source-code = sourccod.source-code NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE sources: 
       DO TRANSACTION: 
        i = i + 1. 
        FIND CURRENT sources EXCLUSIVE-LOCK. 
        DELETE sources. 
      END. 
      FIND NEXT sources WHERE sources.datum LE curr-date 
        AND sources.source-code = sourccod.source-code NO-LOCK NO-ERROR. 
    END. 
  END. 
END. 


PROCEDURE del-old-stat4: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FOR EACH segment NO-LOCK: 
    FIND FIRST segmentstat WHERE segmentstat.datum LE curr-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE segmentstat: 
       DO TRANSACTION: 
        i = i + 1. 
        FIND CURRENT segmentstat EXCLUSIVE-LOCK. 
        DELETE segmentstat. 
      END. 
      FIND NEXT segmentstat WHERE segmentstat.datum LE curr-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK NO-ERROR. 
    END. 
  END. 
END. 

PROCEDURE del-old-stat41: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FOR EACH guest-queasy WHERE guest-queasy.betriebsnr = 0 
  AND guest-queasy.key = "msegm" 
  AND guest-queasy.date1 LE curr-date USE-INDEX b-date_ix: 
    i = i + 1. 
    DELETE guest-queasy. 
  END. 
END. 

PROCEDURE del-old-stat5: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FOR EACH nation NO-LOCK: 
    FIND FIRST nationstat WHERE nationstat.datum LE curr-date 
      AND nationstat.nationnr = nation.nationnr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE nationstat: 
       DO TRANSACTION: 
        i = i + 1. 
        FIND CURRENT nationstat EXCLUSIVE-LOCK. 
        DELETE nationstat. 
      END. 
      FIND NEXT nationstat WHERE nationstat.datum LE curr-date 
        AND nationstat.nationnr = nation.nationnr NO-LOCK NO-ERROR. 
    END. 
  END. 
END. 


PROCEDURE del-old-stat6: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    j         = 0
    curr-date = ci-date - anz
  .   
  FOR EACH artikel NO-LOCK BY artikel.departement BY artikel.artnr: 
    FIND FIRST umsatz WHERE umsatz.datum LE curr-date 
      AND umsatz.artnr = artikel.artnr 
      AND umsatz.departement = artikel.departement 
      NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE umsatz: 
      DO TRANSACTION: 
        i = i + 1. 
        FIND FIRST kontplan WHERE kontplan.betriebsnr = umsatz.departement
          AND kontplan.kontignr = umsatz.artnr
          AND kontplan.datum    = umsatz.datum EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE kontplan THEN DELETE kontplan.
        FIND CURRENT umsatz EXCLUSIVE-LOCK. 
        DELETE umsatz. 
      END. 
      FIND NEXT umsatz WHERE umsatz.datum LE curr-date 
        AND umsatz.artnr = artikel.artnr 
        AND umsatz.departement = artikel.departement 
        NO-LOCK NO-ERROR. 
    END. 
    
    FIND FIRST budget WHERE budget.datum LE curr-date 
      AND budget.artnr = artikel.artnr 
      AND budget.departement = artikel.departement 
      NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE budget: 
       DO TRANSACTION: 
        j = j + 1. 
        FIND CURRENT budget EXCLUSIVE-LOCK. 
        DELETE budget. 
      END. 
      FIND NEXT budget WHERE budget.datum LE curr-date 
        AND budget.artnr = artikel.artnr 
        AND budget.departement = artikel.departement 
        NO-LOCK NO-ERROR. 
    END. 
  END. 
 
/* DELETE old GL outstanding */ 
  FOR EACH uebertrag WHERE uebertrag.datum LT curr-date EXCLUSIVE-LOCK: 
    DELETE uebertrag. 
  END. 
 
END. 

PROCEDURE del-old-stat7: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FOR EACH h-artikel NO-LOCK BY h-artikel.departement BY h-artikel.artnr: 
    FIND FIRST h-umsatz WHERE h-umsatz.datum LE curr-date 
      AND h-umsatz.artnr = h-artikel.artnr 
      AND h-umsatz.departement = h-artikel.departement 
      NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE h-umsatz: 
       DO TRANSACTION: 
        i = i + 1. 
        FIND CURRENT h-umsatz EXCLUSIVE-LOCK. 
        DELETE h-umsatz. 
      END. 
      FIND NEXT h-umsatz WHERE h-umsatz.datum LE curr-date 
        AND h-umsatz.artnr = h-artikel.artnr 
        AND h-umsatz.departement = h-artikel.departement 
        NO-LOCK NO-ERROR. 
    END. 
  END. 
END. 
 
PROCEDURE del-old-stat8: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FIND FIRST h-cost WHERE h-cost.datum LE curr-date NO-LOCK 
    USE-INDEX date_ix NO-ERROR. 
  DO WHILE AVAILABLE h-cost: 
    DO TRANSACTION: 
      i = i + 1. 
      FIND CURRENT h-cost EXCLUSIVE-LOCK. 
      DELETE h-cost. 
    END. 
    FIND NEXT h-cost WHERE h-cost.datum LE curr-date NO-LOCK 
      USE-INDEX date_ix NO-ERROR. 
  END. 
END. 


PROCEDURE del-old-stat9: 
DEFINE VARIABLE curr-date AS DATE NO-UNDO. 
  ASSIGN
    i         = 0 
    curr-date = ci-date - anz
  .   
  FIND FIRST exrate WHERE exrate.datum LE curr-date NO-LOCK 
    USE-INDEX date_ix NO-ERROR. 
  DO WHILE AVAILABLE exrate: 
    DO TRANSACTION: 
      i = i + 1. 
      FIND CURRENT exrate EXCLUSIVE-LOCK. 
      DELETE exrate. 
    END. 
    FIND NEXT exrate WHERE exrate.datum LE curr-date NO-LOCK 
      USE-INDEX date_ix NO-ERROR. 
  END. 
END. 

PROCEDURE del-dml:
  FOR EACH dml-art WHERE dml-art.datum LE (ci-date - 60):
    FIND FIRST queasy WHERE queasy.KEY = 202
          AND queasy.number1 = 0
          AND queasy.number2 = dml-art.artnr
          AND queasy.date1   = dml-art.datum NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
          FIND CURRENT queasy EXCLUSIVE-LOCK.
          DELETE queasy.
          RELEASE queasy.
    END.                 
    DELETE dml-art. 
  END. 
  FOR EACH dml-artdep WHERE dml-artdep.datum LE (ci-date - 60): 
    FIND FIRST queasy WHERE queasy.KEY = 202
          AND queasy.number1 = dml-artdep.departement
          AND queasy.number2 = dml-artdep.artnr
          AND queasy.date1   = dml-artdep.datum NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
          FIND CURRENT queasy EXCLUSIVE-LOCK.
          DELETE queasy.
          RELEASE queasy.
    END.              
    DELETE dml-artdep. 
  END. 
END. 
