
DEF INPUT PARAMETER all-flag AS LOGICAL.
DEF INPUT PARAMETER dept1 AS INT.
DEF INPUT PARAMETER dept2 AS INT.
DEF INPUT PARAMETER art1 AS INT.
DEF INPUT PARAMETER art2 AS INT.
DEF INPUT PARAMETER overwrite-flag AS LOGICAL.
DEF OUTPUT PARAMETER anzahl AS CHAR.

DEFINE BUFFER subgrp FOR wgrpdep. 
DEFINE buffer h-art FOR h-artikel. 
DEFINE buffer art FOR artikel. 

IF NOT all-flag THEN RUN copy-sales. 
ELSE RUN copy-all. 

PROCEDURE copy-sales: 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE BUFFER qbuff FOR queasy.

  anzahl = STRING(n). 
  FOR EACH h-art WHERE h-art.departement = dept1 
    AND h-art.activeflag AND h-art.artart = 0 
    AND h-art.artnr GE art1 AND h-art.artnr LE art2 NO-LOCK: 
    FIND FIRST h-artikel WHERE h-artikel.artnr = h-art.artnr 
      AND h-artikel.departement = dept2 EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel AND NOT overwrite-flag THEN . 
    ELSE 
    DO: 
      n = n + 1. 
      anzahl = STRING(n). 
      /*MTDISP anzahl WITH FRAME frame1. */
      FIND FIRST subgrp WHERE subgrp.departement = dept1 
        AND subgrp.zknr = h-art.zwkum NO-LOCK NO-ERROR. 
      FIND FIRST wgrpdep WHERE wgrpdep.departement = dept2 
        AND wgrpdep.zknr = h-art.zwkum NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE wgrpdep AND AVAILABLE subgrp THEN 
      DO: 
       CREATE wgrpdep. 
         ASSIGN 
           wgrpdep.departement = dept2 
           wgrpdep.zknr = subgrp.zknr 
           wgrpdep.bezeich = subgrp.bezeich. 
      END. 
      IF NOT AVAILABLE h-artikel THEN CREATE h-artikel. 
      ASSIGN 
            h-artikel.artnr = h-art.artnr 
            h-artikel.departement = dept2 
            h-artikel.bezeich = h-art.bezeich 
            h-artikel.epreis1 = h-art.epreis1 
            h-artikel.epreis2 = h-art.epreis2 
            h-artikel.zwkum = h-art.zwkum 
            h-artikel.endkum = h-art.endkum 
            h-artikel.mwst-code   = h-art.mwst-code 
            h-artikel.service-code = h-art.service-code 
            h-artikel.autosaldo = h-art.autosaldo 
            h-artikel.bezaendern = h-art.bezaendern 
            h-artikel.bondruckernr[1] = h-art.bondruckernr[1] 
            h-artikel.aenderwunsch = h-art.aenderwunsch 
            h-artikel.s-gueltig  = h-art.s-gueltig 
            h-artikel.e-gueltig = h-art.e-gueltig 
            h-artikel.artnrlager = h-art.artnrlager 
            h-artikel.artnrrezept = h-art.artnrrezept 
            h-artikel.lagernr = h-art.lagernr 
            h-artikel.prozent = h-art.prozent 
            h-artikel.artnrfront = h-art.artnrfront 
            h-artikel.activeflag = YES. 

      FIND FIRST queasy WHERE queasy.KEY = 38 AND queasy.number1 = dept1
          AND queasy.number2 = h-art.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
          CREATE qbuff.
          BUFFER-COPY queasy EXCEPT number1 TO qbuff.
          ASSIGN qbuff.number1 = dept2.
          FIND CURRENT qbuff NO-LOCK.
      END.

      FIND FIRST art WHERE art.artnr = h-art.artnrfront AND 
        art.departement = dept1 NO-LOCK NO-ERROR. 
      FIND FIRST artikel WHERE artikel.artnr = h-art.artnrfront AND 
        artikel.departement = dept2 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE artikel AND AVAILABLE art THEN 
      DO: 
        CREATE artikel. 
        ASSIGN 
          artikel.departement = dept2 
          artikel.artnr = art.artnr 
          artikel.bezeich = art.bezeich 
          artikel.activeflag = YES 
          artikel.fibukonto = art.fibukonto 
          artikel.bezeich1 = art.bezeich1 
          artikel.zwkum = art.zwkum 
          artikel.endkum = art.endkum 
          artikel.epreis  = art.epreis 
          artikel.autosaldo = art.autosaldo 
          artikel.artart  = art.artart 
          artikel.umsatzart  = art.umsatzart 
          artikel.kassarapport   = art.kassarapport 
          artikel.kassabuch = art.kassabuch 
          artikel.mwst-code  = art.mwst-code 
          artikel.service-code = art.service-code 
          artikel.fibukonto  = art.fibukonto 
          artikel.bezeich1   = art.bezeich 
          artikel.pricetab = art.pricetab 
          artikel.activeflag = art.activeflag 
          artikel.s-gueltig  = art.s-gueltig 
          artikel.e-gueltig = art.e-gueltig 
          artikel.artnrlager = art.artnrlager 
          artikel.artnrrezept = art.artnrrezept 
          artikel.prozent = art.prozent 
          artikel.lagernr = art.lagernr. 
       END. 
     END. 
   END. 
END. 
 
PROCEDURE copy-all: 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  anzahl = STRING(n). 
  FOR EACH h-art WHERE h-art.departement = dept1 
    AND h-art.activeflag 
    AND h-art.artnr GE art1 AND h-art.artnr LE art2 NO-LOCK: 
    FIND FIRST h-artikel WHERE h-artikel.artnr = h-art.artnr 
      AND h-artikel.departement = dept2 EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel AND NOT overwrite-flag THEN . 
    ELSE 
    DO: 
      n = n + 1. 
      anzahl = STRING(n). 
      /*MTDISP anzahl WITH FRAME frame1. */
      FIND FIRST subgrp WHERE subgrp.departement = dept1 
        AND subgrp.zknr = h-art.zwkum NO-LOCK NO-ERROR. 
      FIND FIRST wgrpdep WHERE wgrpdep.departement = dept2 
        AND wgrpdep.zknr = h-art.zwkum NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE wgrpdep AND AVAILABLE subgrp THEN 
      DO: 
       CREATE wgrpdep. 
         ASSIGN 
           wgrpdep.departement = dept2 
           wgrpdep.zknr = subgrp.zknr 
           wgrpdep.bezeich = subgrp.bezeich. 
      END. 
      IF NOT AVAILABLE h-artikel THEN CREATE h-artikel. 
      ASSIGN 
            h-artikel.artnr = h-art.artnr 
            h-artikel.artart = h-art.artart 
            h-artikel.departement = dept2 
            h-artikel.bezeich = h-art.bezeich 
            h-artikel.epreis1 = h-art.epreis1 
            h-artikel.epreis2 = h-art.epreis2 
            h-artikel.zwkum = h-art.zwkum 
            h-artikel.endkum = h-art.endkum 
            h-artikel.mwst-code   = h-art.mwst-code 
            h-artikel.service-code = h-art.service-code 
            h-artikel.autosaldo = h-art.autosaldo 
            h-artikel.bezaendern = h-art.bezaendern 
            h-artikel.bondruckernr[1] = h-art.bondruckernr[1] 
            h-artikel.aenderwunsch = h-art.aenderwunsch 
            h-artikel.s-gueltig  = h-art.s-gueltig 
            h-artikel.e-gueltig = h-art.e-gueltig 
            h-artikel.artnrlager = h-art.artnrlager 
            h-artikel.artnrrezept = h-art.artnrrezept 
            h-artikel.lagernr = h-art.lagernr 
            h-artikel.prozent = h-art.prozent 
            h-artikel.artnrfront = h-art.artnrfront 
            h-artikel.activeflag = YES. 
      IF h-art.artart = 0 THEN 
      DO: 
        FIND FIRST art WHERE art.artnr = h-art.artnrfront AND 
          art.departement = dept1 NO-LOCK NO-ERROR. 
        FIND FIRST artikel WHERE artikel.artnr = h-art.artnrfront AND 
          artikel.departement = dept2 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE artikel AND AVAILABLE art THEN 
        DO: 
          CREATE artikel. 
          ASSIGN 
            artikel.departement = dept2 
            artikel.artnr = art.artnr 
            artikel.bezeich = art.bezeich 
            artikel.activeflag = YES 
            artikel.fibukonto = art.fibukonto 
            artikel.bezeich1 = art.bezeich1 
            artikel.zwkum = art.zwkum 
            artikel.endkum = art.endkum 
            artikel.epreis  = art.epreis 
            artikel.autosaldo = art.autosaldo 
            artikel.artart  = art.artart 
            artikel.umsatzart  = art.umsatzart 
            artikel.kassarapport   = art.kassarapport 
            artikel.kassabuch = art.kassabuch 
            artikel.mwst-code  = art.mwst-code 
            artikel.service-code = art.service-code 
            artikel.fibukonto  = art.fibukonto 
            artikel.bezeich1   = art.bezeich 
            artikel.pricetab = art.pricetab 
            artikel.activeflag = art.activeflag 
            artikel.s-gueltig  = art.s-gueltig 
            artikel.e-gueltig = art.e-gueltig 
            artikel.artnrlager = art.artnrlager 
            artikel.artnrrezept = art.artnrrezept 
            artikel.prozent = art.prozent 
            artikel.lagernr = art.lagernr. 
         END. 
       END. 
     END. 
   END.
END. 

