DEFINE INPUT PARAMETER guestNo          AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER long-digit      AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER day1            AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER day2            AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER day3            AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER price-decimal   AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER from-art        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER to-art          AS INTEGER NO-UNDO.


find first htparam where paramnr = 246 no-lock.
long-digit = htparam.flogical.

find first htparam where paramnr = 330 no-lock.
if finteger NE 0 then day1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
find first htparam where paramnr = 331 no-lock.
if finteger NE 0 then day2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
find first htparam where paramnr = 332 no-lock.
    if finteger NE 0 then day3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
day2 = day2 + day1.
day3 = day3 + day2.

find first htparam where htparam.paramnr = 491.
price-decimal = htparam.finteger.

FIND FIRST guest WHERE guest.gastnr = guestNo NO-LOCK NO-ERROR.
IF AVAILABLE guest AND guest.zahlungsart NE 0 THEN
ASSIGN
    from-art = guest.zahlungsart
    to-art   = from-art.
ELSE
DO:
  FOR EACH artikel WHERE artikel.departement = 0 
     AND artikel.artart = 2 
     AND artikel.activeflag = YES NO-LOCK:
     IF from-art GT artikel.artnr THEN from-art = artikel.artnr.
     IF to-art LT artikel.artnr THEN to-art = artikel.artnr.
  END.
END.
