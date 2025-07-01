DEF TEMP-TABLE r-list 
   FIELD tischnr LIKE tisch.tischnr 
   FIELD bezeich LIKE tisch.bezeich. 

DEF INPUT PARAMETER sel-type  AS INT.
DEF INPUT PARAMETER location  AS INTEGER.
DEF INPUT PARAMETER location2 AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR r-list.

IF sel-type = 0 THEN 
DO: 
    FOR EACH tisch WHERE tisch.departement = location AND tisch.betriebsnr EQ location2
      AND NOT tisch.roomcharge NO-LOCK BY tisch.tischnr: 
        FIND FIRST queasy WHERE queasy.key = 31 AND queasy.number1 = location 
            AND queasy.number2 = tisch.tischnr AND queasy.deci3 EQ location2 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE queasy THEN 
        DO: 
            CREATE r-list. 
            ASSIGN 
                r-list.tischnr = tisch.tischnr 
                r-list.bezeich = tisch.bezeich. 
        END. 
    END. 
END. 
ELSE IF sel-type = 1 THEN 
DO: 
    FOR EACH queasy WHERE queasy.key = 31 AND queasy.number1 = location AND queasy.deci3 EQ location2 NO-LOCK: 
      FIND FIRST tisch WHERE tisch.departement = location AND tisch.betriebsnr EQ location2
        AND tisch.tischnr = queasy.number2 NO-LOCK NO-ERROR.
      IF AVAILABLE tisch THEN
      DO:
        CREATE r-list. 
        ASSIGN 
            r-list.tischnr = tisch.tischnr 
            r-list.bezeich = tisch.bezeich. 
      END.
    END. 
END. 
