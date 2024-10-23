
DEFINE TEMP-TABLE rmcat-list 
  FIELD zikatnr                 AS INTEGER 
  FIELD anzahl                  AS INTEGER 
  FIELD sleeping                AS LOGICAL INITIAL YES
  FIELD kurzbez                 AS CHAR 
  FIELD bezeich                 AS CHAR FORMAT "x(20)" 
  FIELD zinr                    AS CHAR 
. 

DEF INPUT PARAMETER curr-zikat  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER mi-inactive AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rmcat-list.

RUN active-room.

PROCEDURE active-room :
DEFINE VARIABLE zikatnr   AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE VARIABLE troom     AS INTEGER INITIAL 0 NO-UNDO.

  FOR EACH zimmer WHERE zimmer.sleeping = YES 
    AND zimmer.zikatnr = curr-zikat AND zimmer.zinr NE "" NO-LOCK : 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimkateg.verfuegbarkeit  THEN 
    DO: 
        CREATE rmcat-list. 
        ASSIGN
            rmcat-list.zikatnr       = zimkateg.zikatnr
            rmcat-list.zinr          = zimmer.zinr
            rmcat-list.kurzbez       = zimkateg.kurzbez
            rmcat-list.bezeich       = zimkateg.bezeichnung                                 /* CR 05/04/24 | Fix for Serverless */
            .
         troom = troom + 1.
    END. 
  END. 
  CREATE rmcat-list.
  ASSIGN 
      rmcat-list.kurzbez      = "TOTAL" 
      rmcat-list.zinr         = STRING(troom)
      .

  /* %%% */ 
  IF NOT mi-inactive THEN RETURN. 
  zikatnr = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = NO 
      AND zimmer.zikatnr = curr-zikat AND zimmer.zinr NE "" NO-LOCK BY zimmer.zikatnr: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimkateg.verfuegbarkeit THEN 
    DO: 
        create rmcat-list. 
        ASSIGN
            rmcat-list.zikatnr       = zimkateg.zikatnr
            rmcat-list.zinr          = zimmer.zinr
            rmcat-list.kurzbez       = zimkateg.kurzbez
            rmcat-list.bezeich       = zimkateg.bezeichnung                                 /* CR 05/04/24 | Fix for Serverless */
            .
         troom = troom + 1.
    END. 
  END. 

  IF troom NE 0 THEN
  DO:
  CREATE rmcat-list.
  ASSIGN 
      rmcat-list.kurzbez      = "TOTAL" 
      rmcat-list.zinr         = STRING(troom)
      .
  END.
  
END.
