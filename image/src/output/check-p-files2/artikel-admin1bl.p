
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER artNo          AS INT.
DEF INPUT  PARAMETER deptNo         AS INT.
DEF INPUT  PARAMETER rec-id         AS INT.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "artikel-admin".

FIND FIRST argt-line WHERE argt-line.argt-artnr = artNo
 AND argt-line.departement = deptNo NO-LOCK NO-ERROR. 
IF AVAILABLE argt-line THEN 
DO: 
 msg-str = msg-str + CHR(2)
         + translateExtended ("Arrangement Line exists, deleting not possible.",lvCAREA,"").
 RETURN NO-APPLY.
END. 
FIND FIRST umsatz WHERE umsatz.artnr = artNo
 AND umsatz.departement = deptNo NO-LOCK NO-ERROR. 
IF AVAILABLE umsatz THEN 
DO: 
 msg-str = msg-str + CHR(2)
         + translateExtended ("Turnover exists, deleting not possible.",lvCAREA,"").
 RETURN NO-APPLY.
END. 
DO: 
 FIND FIRST artikel WHERE RECID(artikel) = rec-id EXCLUSIVE-LOCK. 
 DELETE artikel.
END.
