DEF TEMP-TABLE r-list 
   FIELD zinr      LIKE zimmer.zinr 
   FIELD bezeich   LIKE zimmer.bezeich
   FIELD location  AS INT
   FIELD floor     AS INT. 

DEF INPUT PARAMETER show-all AS LOGICAL.
DEF INPUT PARAMETER sel-type AS INT.
DEF INPUT PARAMETER etage    AS INT.
DEF INPUT PARAMETER location AS INT.
DEF OUTPUT PARAMETER TABLE FOR r-list.

IF NOT show-all THEN RUN create-list1.
ELSE RUN create-list2.

PROCEDURE create-list1: 
  FOR EACH r-list: 
    DELETE r-list. 
  END. 
  IF sel-type = 0 THEN 
  DO: 
    FOR EACH zimmer WHERE zimmer.etage = etage NO-LOCK BY zimmer.zinr: 
        FIND FIRST queasy WHERE queasy.KEY = 25 AND queasy.number1 = location 
            AND queasy.number2 = etage AND queasy.char1 = zimmer.zinr 
            NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE queasy THEN 
        DO: 
            CREATE r-list. 
            ASSIGN 
                r-list.zinr     = zimmer.zinr 
                r-list.bezeich  = zimmer.bezeich
                r-list.location = INT(zimmer.CODE)
                r-list.floor    = zimmer.etage. 
        END.  
     END. 
  END. 
  ELSE IF sel-type = 1 THEN 
  DO: 
    FOR EACH queasy WHERE queasy.KEY = 25 AND queasy.number1 = location 
        AND queasy.number2 = etage NO-LOCK: 
        FIND FIRST zimmer WHERE zimmer.zinr = queasy.char1 NO-LOCK NO-ERROR. /* Malik Serverless 307 : NO-LOCK -> NO-LOCK NO-ERROR */
        IF NOT AVAILABLE zimmer THEN NEXT. /* Malik Serverless 307 */
        CREATE r-list. 
        ASSIGN 
            r-list.zinr     = zimmer.zinr 
            r-list.bezeich  = zimmer.bezeich
            r-list.location = INT(zimmer.CODE)
            r-list.floor    = zimmer.etage.
    END.
  END. 
END. 
 
PROCEDURE create-list2: 
  FOR EACH r-list: 
    DELETE r-list. 
  END. 
  IF sel-type = 0 THEN 
  DO: 
    FOR EACH zimmer NO-LOCK BY zimmer.zinr: 
        FIND FIRST queasy WHERE queasy.KEY = 25 
            AND queasy.number2 = etage AND queasy.char1 = zimmer.zinr 
            NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE queasy THEN 
        DO: 
            CREATE r-list. 
            ASSIGN 
                r-list.zinr     = zimmer.zinr 
                r-list.bezeich  = zimmer.bezeich
                r-list.location = INT(zimmer.CODE)
                r-list.floor    = zimmer.etage. 
        END.
    END.
  END. 
  ELSE IF sel-type = 1 THEN 
  DO: 
    FOR EACH queasy WHERE queasy.KEY = 25 NO-LOCK: 
        FIND FIRST zimmer WHERE zimmer.zinr = queasy.char1 NO-LOCK NO-ERROR. /* Malik Serverless 307 : NO-LOCK -> NO-LOCK NO-ERROR */
        IF NOT AVAILABLE zimmer THEN NEXT. /* Malik Serverless 307 */
        CREATE r-list. 
        ASSIGN 
            r-list.zinr     = zimmer.zinr 
            r-list.bezeich  = zimmer.bezeich
            r-list.location = INT(zimmer.CODE)
            r-list.floor    = zimmer.etage.
    END. 
  END. 
END. 


