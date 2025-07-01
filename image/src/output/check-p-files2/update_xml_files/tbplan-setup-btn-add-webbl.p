
DEF INPUT  PARAMETER curr-n     AS INT.
DEF INPUT  PARAMETER location   AS INT.
DEF INPUT  PARAMETER from-table AS INT.
DEF INPUT  PARAMETER location2  AS INT.
DEF OUTPUT PARAMETER err-flag   AS INT INIT 0.

FIND FIRST queasy WHERE queasy.key = 31 AND queasy.number1 = location 
    AND queasy.number2 = from-table AND queasy.betriebsnr = 0 AND queasy.deci3 EQ location2
    NO-LOCK NO-ERROR. 
IF AVAILABLE queasy THEN 
DO: 
   err-flag = 1.
   RETURN NO-APPLY. 
END. 

FIND FIRST tisch WHERE tisch.departement = location
    AND tisch.tischnr = from-table AND tisch.betriebsnr EQ location2 NO-LOCK. 

IF curr-n = 100 THEN 
DO:
   err-flag = 2.
   RETURN NO-APPLY. 
END. 
