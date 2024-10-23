

DEF INPUT PARAMETER lief-nr AS INTEGER. 
DEF INPUT PARAMETER docu-nr AS CHAR. 
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER f-endkum       AS INT.
DEF OUTPUT PARAMETER b-endkum       AS INT.
DEF OUTPUT PARAMETER m-endkum       AS INT.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER fb-closedate   AS DATE.
DEF OUTPUT PARAMETER m-closedate    AS DATE.

DEFINE VARIABLE negative-oh AS LOGICAL INITIAL NO.
DEFINE VARIABLE lscheinnr AS CHAR. 
DEFINE VARIABLE curr-lager AS INTEGER. 
DEFINE VARIABLE anzahl AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE t-amount AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE VARIABLE tot-wert AS DECIMAL. 

FIND FIRST bediener WHERE bediener.userinit = user-init.
FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-closedate = htparam.fdate. 
 
RUN check-onhand. 
IF negative-oh THEN RETURN. 
 
FOR EACH l-op WHERE l-op.lief-nr = lief-nr 
  AND l-op.docu-nr = docu-nr AND l-op.lscheinnr = docu-nr 
  AND l-op.op-art = 1 AND l-op.loeschflag LE 1 AND l-op.pos GT 0: 
  FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK. 
  l-op.loeschflag = 2. 
  curr-lager = l-op.lager-nr. 
  billdate = l-op.datum. 
  anzahl = - l-op.anzahl. 
  wert = - l-op.warenwert. 
  t-amount = t-amount + wert. 
 
/* UPDATE stock onhand  */ 
  IF ((endkum = f-endkum OR endkum = b-endkum) AND NOT l-op.flag 
      AND billdate LE fb-closedate) 
  OR (endkum GE m-endkum AND billdate LE m-closedate AND NOT l-op.flag) THEN 
  DO: 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 
    l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
    tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang. 
    tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
          - l-bestand.wert-ausgang. 
    FIND CURRENT l-bestand NO-LOCK. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      create l-bestand. 
      l-bestand.anf-best-dat = billdate. 
      l-bestand.artnr = l-artikel.artnr. 
      l-bestand.lager-nr = curr-lager. 
    END. 
 
    l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
 
/* UPDATE average price */ 
    IF tot-anz NE 0 THEN 
    DO: 
      FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
      l-artikel.vk-preis = tot-wert / tot-anz. 
      FIND CURRENT l-artikel NO-LOCK. 
    END. 
/* 
    RUN adjust-stock-value. 
*/ 
  END. 
 
/* UPDATE supplier turnover */ 
    FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = lief-nr 
      AND l-liefumsatz.datum = billdate 
    EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-liefumsatz THEN 
  DO: 
    create l-liefumsatz. 
    l-liefumsatz.datum = billdate. 
    l-liefumsatz.lief-nr = lief-nr. 
  END. 
  l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + wert. 
END. 
 
RUN update-ap. 

PROCEDURE check-onhand: 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-closedate = htparam.fdate. 
 
  FOR EACH l-op WHERE l-op.lief-nr = lief-nr 
    AND l-op.docu-nr = docu-nr AND l-op.lscheinnr = docu-nr 
    AND l-op.op-art = 1 AND l-op.loeschflag LE 1 AND l-op.pos GT 0 NO-LOCK: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK. 
    IF (l-artikel.endkum LE 2 AND l-op.datum LE fb-closedate) OR 
       (l-artikel.endkum GT 2 AND l-op.datum LE m-closedate) THEN 
    DO: 
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr 
        AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR. 
      IF AVAILABLE l-bestand AND 
      (anz-anf-best + anz-eingang - anz-ausgang - l-op.anzahl) LT 0 THEN 
      DO: 
        /*MThide MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Stock",lvCAREA,"") + " " + STRING(l-artikel.artnr,"9999999") + " - " 
          + l-artikel.bezeich + " " + translateExtended ("would have negative onhand!!",lvCAREA,"") 
          SKIP 
          translateExtended ("Deleting not possible (Check outgoing records).",lvCAREA,"") 
          VIEW-AS ALERT-BOX INFORMATION.*/
        negative-oh = YES. 
        RETURN.
      END. 
    END. 
  END. 
END. 



PROCEDURE update-ap: 
DEFINE VARIABLE ap-license AS LOGICAL INITIAL NO. 
DEFINE VARIABLE ap-acct AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL INITIAL YES. 
 
  FIND FIRST htparam WHERE paramnr = 1016 no-lock. /* ap license */ 
  IF NOT flogical THEN RETURN. 
 
  FIND FIRST htparam WHERE paramnr = 986 NO-LOCK. 
  ap-acct = htparam.fchar. 
  /*FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-acct THEN 
  DO: 
    IF l-lieferant.z-code NE "" THEN 
    DO: 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-lieferant.z-code 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct AND (l-lieferant.z-code NE ap-acct) THEN do-it = NO. 
    END. 
  END.*/

  FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN ASSIGN do-it = NO.
  IF NOT do-it THEN RETURN. 
 
  FIND FIRST l-kredit WHERE l-kredit.name = docu-nr 
    AND l-kredit.saldo = - t-amount 
    AND l-kredit.lief-nr = lief-nr 
    AND l-kredit.rgdatum = billdate NO-LOCK NO-ERROR. 
  IF AVAILABLE l-kredit THEN 
  DO: 
    FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
    delete l-kredit. 
  END. 
  ELSE 
  DO: 
    create l-kredit. 
    l-kredit.name = docu-nr. 
    l-kredit.lief-nr = lief-nr. 
    l-kredit.lscheinnr = lscheinnr. 
    l-kredit.rgdatum = billdate. 
    l-kredit.datum = ?. 
    l-kredit.saldo = t-amount. 
    l-kredit.ziel = 0. 
    l-kredit.netto = t-amount. 
    l-kredit.bediener-nr = bediener.nr. 
  END. 
 
  create ap-journal. 
  ap-journal.lief-nr = lief-nr. 
  ap-journal.docu-nr = docu-nr. 
  ap-journal.lscheinnr = docu-nr. 
  ap-journal.rgdatum = billdate. 
  ap-journal.saldo = t-amount. 
  ap-journal.netto = t-amount. 
  ap-journal.userinit = bediener.userinit. 
  ap-journal.zeit = time. 
  ap-journal.bemerk = "Cancel Direct Purchase". 
END.
