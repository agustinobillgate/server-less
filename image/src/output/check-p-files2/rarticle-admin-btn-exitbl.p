DEFINE TEMP-TABLE h-list LIKE h-artikel.

DEF INPUT PARAMETER TABLE FOR h-list.
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER fract-flag  AS LOGICAL.
DEF INPUT PARAMETER ask-voucher AS LOGICAL.
DEF INPUT PARAMETER bezeich2    AS CHAR.

FIND FIRST h-list.
IF case-type = 1 THEN   /*MT add */
DO:
    create h-artikel. 
    RUN fill-artikel. 
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST h-artikel WHERE h-artikel.artnr = h-list.artnr
        AND h-artikel.departement = h-list.departement NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
      RUN fill-artikel. 
      FIND CURRENT h-artikel NO-LOCK. 
    END.
END.

PROCEDURE fill-artikel: 
  ASSIGN 
    h-artikel.artnr  = h-list.artnr 
    h-artikel.departement = h-list.departement 
    h-artikel.bezaendern = h-list.bezaendern 
    h-artikel.bezeich = h-list.bezeich 
    h-artikel.zwkum   = h-list.zwkum 
    h-artikel.endkum  = h-list.endkum 
    h-artikel.epreis1  = h-list.epreis1 
    h-artikel.abbuchung  = h-list.abbuchung
    h-artikel.autosaldo = h-list.autosaldo 
    h-artikel.artart  = h-list.artart 
    h-artikel.epreis2  = h-list.epreis2 
    h-artikel.gang = INTEGER(fract-flag)
    h-artikel.bondruckernr[1]   = h-list.bondruckernr[1] 
    h-artikel.aenderwunsch = h-list.aenderwunsch 
    h-artikel.artnrfront = h-list.artnrfront 
    h-artikel.mwst-code  = h-list.mwst-code 
    h-artikel.service-code = h-list.service-code 
    h-artikel.activeflag = h-list.activeflag 
    h-artikel.s-gueltig  = h-list.s-gueltig 
    h-artikel.e-gueltig = h-list.e-gueltig 
    h-artikel.artnrlager = h-list.artnrlager 
    h-artikel.artnrrezept = h-list.artnrrezept 
    h-artikel.prozent = h-list.prozent 
    h-artikel.lagernr = h-list.lagernr 
    h-artikel.betriebsnr = h-list.betriebsnr 
    h-artikel.bondruckernr[4] = INTEGER(ask-voucher) 
  . 
  IF bezeich2 = "" THEN
  DO:
      FIND FIRST queasy WHERE queasy.key = 38 AND queasy.number1 = h-list.departement
          AND queasy.number2 = h-list.artnr EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN DELETE queasy.
  END.
  ELSE
  DO:
      FIND FIRST queasy WHERE queasy.key = 38 AND queasy.number1 = h-list.departement
          AND queasy.number2 = h-list.artnr EXCLUSIVE-LOCK NO-ERROR.
      IF NOT AVAILABLE queasy THEN
      DO:
          CREATE queasy.
          ASSIGN
              queasy.key = 38
              queasy.number1 = h-list.departement
              queasy.number2 = h-list.artnr
          .
      END.
      ASSIGN queasy.char3 = bezeich2.
      FIND CURRENT queasy NO-LOCK.
  END.
END. 

