
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
 
/** inventory is running **/ 
DO TRANSACTION:
    FIND FIRST htparam WHERE paramnr = 232 EXCLUSIVE-LOCK. 
    htparam.flogical = YES.
    FIND CURRENT htparam NO-LOCK.
END.
 
/* CURRENT closing DATE */ 
IF art-type LE 2 THEN FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
ELSE FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
to-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */
from-date = DATE(MONTH(to-date), 1, year(to-date)).


RUN init-onhand.


PROCEDURE init-onhand:
DEF BUFFER l-oh FOR l-bestand.
DEF BUFFER buf-lart FOR l-artikel.
DEFINE VARIABLE loopi AS INTEGER.

  /*FDL June 16, 2025 - Serverless F5516E | #835*/
  FOR EACH l-bestand EXCLUSIVE-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr EQ l-bestand.artnr NO-LOCK:   
    IF l-artikel.endkum GE main-grp AND l-artikel.endkum LE to-grp THEN
    DO:
      ASSIGN
        l-bestand.anz-eingang  = 0
        l-bestand.wert-eingang = 0 
        l-bestand.anz-ausgang  = 0 
        l-bestand.wert-ausgang = 0.    
    END.         
  END.
  RELEASE l-bestand.
  
  /*FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ 0 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE l-bestand:
    /*DO TRANSACTION: */
        FIND FIRST buf-lart WHERE buf-lart.artnr = l-bestand.artnr 
          AND buf-lart.endkum GE main-grp 
          AND buf-lart.endkum LE to-grp NO-LOCK NO-ERROR. 
        IF AVAILABLE buf-lart THEN DO TRANSACTION:
          FIND FIRST l-oh WHERE RECID(l-oh) = RECID(l-bestand) 
              EXCLUSIVE-LOCK.
          ASSIGN
            l-oh.anz-eingang  = 0
            l-oh.wert-eingang = 0 
            l-oh.anz-ausgang  = 0 
            l-oh.wert-ausgang = 0. 
          FIND CURRENT l-oh NO-LOCK.
          RELEASE l-oh.
        END.
    /*END. */
    FIND NEXT l-bestand WHERE l-bestand.lager-nr EQ 0 NO-LOCK NO-ERROR. 
  END.*/
  /*    
  FIND FIRST l-lager NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE l-lager:
    FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ l-lager.lager-nr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-bestand:
        /*DO TRANSACTION:*/
            FIND FIRST buf-lart WHERE buf-lart.artnr = l-bestand.artnr 
                AND buf-lart.endkum GE main-grp 
                AND buf-lart.endkum LE to-grp
                NO-LOCK NO-ERROR. 
            IF AVAILABLE buf-lart THEN 
            DO TRANSACTION:
                FIND FIRST l-oh WHERE RECID(l-oh) = RECID(l-bestand) EXCLUSIVE-LOCK.
                ASSIGN
                  l-oh.anz-eingang  = 0 
                  l-oh.wert-eingang = 0 
                  l-oh.anz-ausgang  = 0 
                  l-oh.wert-ausgang = 0
                .
                FIND CURRENT l-oh NO-LOCK.
                RELEASE l-oh.
            END.
            FIND NEXT l-bestand WHERE l-bestand.lager-nr EQ l-lager.lager-nr NO-LOCK NO-ERROR.
        /*END.*/
    END.
    FIND NEXT l-lager NO-LOCK NO-ERROR.
  END.

  */
  /*FIND FIRST l-oh NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE l-oh:
    FIND FIRST l-lager WHERE l-lager.lager-nr = l-oh.lager-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-lager THEN
    DO:
        FIND FIRST buf-lart WHERE buf-lart.artnr = l-oh.artnr 
            AND buf-lart.endkum GE main-grp 
            AND buf-lart.endkum LE to-grp
            NO-LOCK NO-ERROR. 
        IF AVAILABLE buf-lart THEN 
        DO TRANSACTION:
            FIND FIRST l-bestand WHERE RECID(l-bestand) = RECID(l-oh)
                EXCLUSIVE-LOCK NO-ERROR.
            ASSIGN
              l-bestand.anz-eingang  = 0 
              l-bestand.wert-eingang = 0 
              l-bestand.anz-ausgang  = 0 
              l-bestand.wert-ausgang = 0
            .
            FIND CURRENT l-bestand NO-LOCK.
            RELEASE l-bestand.
        END.
    END.
    FIND NEXT l-oh NO-LOCK NO-ERROR.
  END.*/
END. 
