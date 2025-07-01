DEF INPUT PARAMETER art-type AS INT.

DEFINE VARIABLE main-grp     AS INTEGER. 
DEFINE VARIABLE to-grp       AS INTEGER. 
DEFINE VARIABLE to-date      AS DATE. 
DEFINE VARIABLE from-date    AS DATE. 

IF art-type = 1 THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 257 NO-LOCK. 
  main-grp = htparam.finteger. 
  to-grp = main-grp. 
END.
ELSE IF art-type = 2 THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 258 NO-LOCK. 
  main-grp = htparam.finteger. 
  to-grp = main-grp. 
END. 
ELSE IF art-type = 3 THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 268 NO-LOCK. 
  main-grp = htparam.finteger. 
  to-grp = 9. 
END. 

/* CURRENT closing DATE */ 
IF art-type LE 2 THEN FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
ELSE FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
to-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */
from-date = DATE(MONTH(to-date), 1, year(to-date)).

FOR EACH l-op WHERE (op-art = 3 OR op-art = 4) AND l-op.loeschflag LT 2 
    AND (l-op.datum GE from-date AND l-op.datum LE to-date) 
    AND l-op.pos GE 1 AND l-op.lager-nr GT 0 NO-LOCK BY l-op.artnr: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-artikel AND l-artikel.endkum GE main-grp 
    AND l-artikel.endkum LE to-grp THEN RUN update-ausgang.
END. 

PROCEDURE update-ausgang: 
DEFINE VARIABLE s-artnr         AS INTEGER NO-UNDO. 
DEFINE VARIABLE anzahl          AS DECIMAL FORMAT "->,>>>,>>9.999" NO-UNDO. 
DEFINE VARIABLE wert            AS DECIMAL NO-UNDO. 
DEFINE VARIABLE transdate       AS DATE    NO-UNDO. 
DEFINE VARIABLE curr-lager      AS INTEGER NO-UNDO. 

DEFINE BUFFER bbest FOR l-bestand.
 
  ASSIGN
    s-artnr     = l-op.artnr 
    anzahl      = l-op.anzahl 
    wert        = l-op.warenwert 
    transdate   = l-op.datum
    curr-lager  = l-op.lager-nr
  . 
 
  /*DO TRANSACTION:*/
/* UPDATE stock onhand IF NOT transferred */ 
    IF l-op.op-art EQ 3 OR (l-op.op-art = 4 /*AND l-op.herkunftflag = 3*/) THEN 
    DO: 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
        l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO TRANSACTION: 
        CREATE l-bestand. 
        ASSIGN
          l-bestand.artnr        = s-artnr
          l-bestand.anf-best-dat = transdate
          l-bestand.anz-ausgang  = l-bestand.anz-ausgang + anzahl
          l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
      END. 
      ELSE DO TRANSACTION:
          FIND FIRST bbest WHERE RECID(bbest) = RECID(l-bestand)
              EXCLUSIVE-LOCK.
          ASSIGN
            bbest.anz-ausgang  = bbest.anz-ausgang + anzahl
            bbest.wert-ausgang = bbest.wert-ausgang + wert. 
          FIND CURRENT bbest NO-LOCK. 
          RELEASE bbest.
      END.      
    END. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO TRANSACTION: 
      CREATE l-bestand. 
      ASSIGN
        l-bestand.lager-nr      = curr-lager
        l-bestand.artnr         = s-artnr
        l-bestand.anf-best-dat  = transdate
        l-bestand.anz-ausgang   = l-bestand.anz-ausgang + anzahl
        l-bestand.wert-ausgang  = l-bestand.wert-ausgang + wert. 
    END. 
    ELSE DO TRANSACTION:
        FIND FIRST bbest WHERE RECID(bbest) = RECID(l-bestand)
            EXCLUSIVE-LOCK.
        ASSIGN
          bbest.anz-ausgang  = bbest.anz-ausgang + anzahl
          bbest.wert-ausgang = bbest.wert-ausgang + wert. 
        FIND CURRENT bbest NO-LOCK. 
        RELEASE bbest.
    END.   
  /*END. */
END.

