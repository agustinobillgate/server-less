
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

RUN update-average. 
 
FIND FIRST htparam WHERE paramnr = 232 EXCLUSIVE-LOCK. 
htparam.flogical = NO. 
FIND CURRENT htparam NO-LOCK. 

PROCEDURE update-average: 
DEFINE VARIABLE tot-anz    AS DECIMAL FORMAT "->,>>>,>>9.999" NO-UNDO. 
DEFINE VARIABLE tot-wert   AS DECIMAL NO-UNDO. 
DEFINE VARIABLE avrg-price AS DECIMAL FORMAT "->>>,>>>,>>9.999999" INITIAL 0
    NO-UNDO. 

  /*FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE l-artikel AND l-artikel.endkum GE main-grp 
      AND l-artikel.endkum LE to-grp THEN 
    DO: 
      ASSIGN
        tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang
        tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
          - l-bestand.wert-ausgang. 
 
      IF tot-anz = 0 THEN 
      ASSIGN
        tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang
        tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang
      . 
 
      IF tot-anz NE 0 THEN 
      DO TRANSACTION: 
        avrg-price = tot-wert / tot-anz. 
        FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          EXCLUSIVE-LOCK. 
        l-artikel.vk-preis = avrg-price. 
        FIND CURRENT l-artikel NO-LOCK. 
        RELEASE l-artikel.
      END. 
 
    END. 
  END. */

  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE l-bestand:

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE l-artikel AND l-artikel.endkum GE main-grp 
      AND l-artikel.endkum LE to-grp THEN 
    DO: 
      ASSIGN
        tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang
        tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
          - l-bestand.wert-ausgang. 
 
      IF tot-anz = 0 THEN 
      ASSIGN
        tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang
        tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang
      . 
 
      IF tot-anz NE 0 THEN 
      DO TRANSACTION: 
        avrg-price = tot-wert / tot-anz. 
        FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          EXCLUSIVE-LOCK. 
        l-artikel.vk-preis = avrg-price. 
        FIND CURRENT l-artikel NO-LOCK. 
        RELEASE l-artikel.
      END.
    END.
    FIND NEXT l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
  END.
END. 

