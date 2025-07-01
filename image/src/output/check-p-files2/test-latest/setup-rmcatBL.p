DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT PARAMETER i-case      AS INTEGER       NO-UNDO.
DEF INPUT PARAMETER TABLE       FOR t-queasy.
DEF INPUT PARAMETER t-bezeich   AS CHAR EXTENT 8 NO-UNDO.
DEF INPUT PARAMETER t-code      AS CHAR EXTENT 8 NO-UNDO.
DEF OUTPUT PARAMETER error-code AS INTEGER       NO-UNDO INIT 0.
DEF OUTPUT PARAMETER msg-str    AS CHAR          NO-UNDO INIT "".

FIND FIRST t-queasy.

CASE i-case:
    WHEN 1 THEN RUN add-rmcat.
    WHEN 2 THEN RUN modify-rmcat.
    WHEN 3 THEN RUN delete-rmcat.
END CASE.

PROCEDURE add-rmcat:
DEF VARIABLE curr-i      AS INTEGER NO-UNDO.
DEF VARIABLE curr-zikat  AS INTEGER NO-UNDO INIT 0.
DEF VARIABLE curr-categ  AS INTEGER NO-UNDO INIT 1.
DEF BUFFER zbuff FOR zimkateg.

  FIND FIRST queasy WHERE queasy.KEY = 152 
      AND (queasy.char1 = t-queasy.char1) OR
      (queasy.char3 = t-queasy.char3) NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN
  DO:
      ASSIGN
          msg-str    = queasy.char3 + " - " + queasy.char1
          error-code = 1
      .
      RETURN.
  END.
  DO curr-i = 1 TO 8:
      IF t-bezeich[curr-i] NE "" THEN
      DO:
        FIND FIRST zimkateg WHERE 
          (zimkateg.bezeichnung = t-bezeich[curr-i]) OR
          (zimkateg.kurzbez = t-code[curr-i]) NO-LOCK NO-ERROR. 
        IF AVAILABLE zimkateg THEN
        DO:
           ASSIGN
               msg-str    = zimkateg.bezeichnung + " - " + zimkateg.kurzbez
               error-code = 2
           .
           RETURN.
        END.
      END.
  END.
  
  FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK
      BY queasy.number1 DESCENDING:
      curr-categ = queasy.number1 + 1.
      LEAVE.
  END.

  CREATE queasy.
  BUFFER-COPY t-queasy EXCEPT number1 TO queasy.
  ASSIGN queasy.number1 = curr-categ.

  DO curr-i = 1 TO 8:
      IF t-bezeich[curr-i] NE "" THEN
      DO:
          curr-zikat = 1.
          FIND FIRST zbuff WHERE zbuff.zikatnr = curr-zikat
              NO-LOCK NO-ERROR.
          DO WHILE AVAILABLE zbuff:
              curr-zikat = curr-zikat + 1.
              FIND NEXT zbuff WHERE zbuff.zikatnr = curr-zikat
                  NO-LOCK NO-ERROR.
          END.

          CREATE zimkateg.
          ASSIGN
              zimkateg.zikatnr        = curr-zikat
              zimkateg.kurzbez        = t-code[curr-i]
              zimkateg.bezeich        = t-bezeich[curr-i]
              zimkateg.typ            = curr-categ
              zimkateg.overbooking    = 0
              zimkateg.verfuegbarkeit = YES
              zimkateg.ACTIVE         = YES
              zimkateg.zibelstat      = YES
          .
      END.
  END.
  
END.

PROCEDURE modify-rmcat:
DEF VARIABLE curr-i      AS INTEGER NO-UNDO.
DEF VARIABLE curr-zikat  AS INTEGER NO-UNDO INIT 0.
DEF VARIABLE foundFlag   AS LOGICAL NO-UNDO INIT NO.
DEF VARIABLE currCode    AS CHAR    NO-UNDO INIT ?.
DEF BUFFER zbuff FOR zimkateg.

  FIND FIRST queasy WHERE queasy.KEY = 152 
      AND ((queasy.char1 = t-queasy.char1) OR
            (queasy.char3 = t-queasy.char3)) 
      AND (queasy.number1 NE t-queasy.number1) NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN
  DO:
      ASSIGN
          msg-str    = queasy.char3 + " - " + queasy.char1
          error-code = 11
      .
      RETURN.
  END.
  DO curr-i = 1 TO 8:
      IF t-bezeich[curr-i] NE "" THEN
      DO:
        FIND FIRST zimkateg WHERE 
          ((zimkateg.bezeichnung = t-bezeich[curr-i]) OR
          (zimkateg.kurzbez = t-code[curr-i])) 
          AND zimkateg.typ NE t-queasy.number1 NO-LOCK NO-ERROR. 
        IF AVAILABLE zimkateg THEN
        DO:
           ASSIGN
               msg-str    = zimkateg.bezeichnung + " - " + zimkateg.kurzbez
               error-code = 12
           .
           RETURN.
        END.
      END.
  END.
  
  FOR EACH ratecode NO-LOCK,
      FIRST zimkateg WHERE zimkateg.zikatnr = ratecode.zikatnr
      AND zimkateg.typ = t-queasy.number1 NO-LOCK
      BY ratecode.CODE:
      IF currCode NE ratecode.CODE THEN
      DO:
          ASSIGN
              currCode  = ratecode.CODE
              foundFlag = NO
          .
          DO curr-i = 1 TO 8:
              IF zimkateg.kurzbez = t-code[curr-i] THEN
              DO:
                  foundFlag = YES.
                  LEAVE.
              END.
          END.
          IF NOT foundFlag THEN
          DO:
              ASSIGN
                  msg-str    = zimkateg.kurzbez + " - " + ratecode.CODE 
                  error-code = 13
              .
              RETURN.
          END.
      END.
  END.

  FOR EACH zimkateg NO-LOCK WHERE zimkateg.typ = queasy.number1:
      ASSIGN foundFlag = NO.
      DO curr-i = 1 TO 8:
          IF zimkateg.kurzbez = t-code[curr-i] THEN
          DO:
              foundFlag = YES.
              LEAVE.
          END.
      END.
      IF foundFlag THEN
      DO:
          FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr
              NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer THEN
          DO:
              ASSIGN
                  msg-str    = zimkateg.kurzbez + " - " + zimmer.zinr
                  error-code = 14
              .
              RETURN.
          END.
      END.
  END.

  FIND FIRST queasy WHERE queasy.KEY = 152
      AND queasy.number1 = t-queasy.number1 EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN
  DO:
      BUFFER-COPY t-queasy TO queasy.
      FIND CURRENT queasy NO-LOCK.
  END.

  FIND FIRST zimkateg WHERE zimkateg.typ = queasy.number1
      NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE zimkateg:
      DO:
          FIND FIRST zbuff WHERE RECID(zbuff) = RECID(zimkateg)
              EXCLUSIVE-LOCK.
          DELETE zbuff.
          RELEASE zbuff.
      END.
      FIND NEXT zimkateg WHERE zimkateg.typ = queasy.number1
          NO-LOCK NO-ERROR.
  END.

  DO curr-i = 1 TO 8:
      IF t-bezeich[curr-i] NE "" THEN
      DO:
          curr-zikat = 1.
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = curr-zikat
              NO-LOCK NO-ERROR.
          DO WHILE AVAILABLE zimkateg:
              curr-zikat = curr-zikat + 1.
              FIND NEXT zimkateg WHERE zimkateg.zikatnr = curr-zikat
                  NO-LOCK NO-ERROR.
          END.
          CREATE zimkateg.
          ASSIGN
              zimkateg.zikatnr        = curr-zikat
              zimkateg.kurzbez        = t-code[curr-i]
              zimkateg.bezeich        = t-bezeich[curr-i]
              zimkateg.typ            = t-queasy.number1
              zimkateg.overbooking    = 0
              zimkateg.verfuegbarkeit = YES
              zimkateg.ACTIVE         = YES
              zimkateg.zibelstat      = YES
          .
          FIND CURRENT zimkateg NO-LOCK.
          RELEASE zimkateg.
      END.
  END.
  
END.

PROCEDURE delete-rmcat:
DEF VARIABLE curr-i      AS INTEGER NO-UNDO.
DEF VARIABLE curr-zikat  AS INTEGER NO-UNDO INIT 0.
DEF VARIABLE foundFlag   AS LOGICAL NO-UNDO INIT NO.
DEF VARIABLE currCode    AS CHAR    NO-UNDO INIT ?.
DEF BUFFER zbuff FOR zimkateg.

  FIND FIRST queasy WHERE queasy.KEY = 152 
      AND (queasy.char1 = t-queasy.char1) OR
      (queasy.char3 = t-queasy.char3) NO-LOCK NO-ERROR.
  IF NOT AVAILABLE queasy THEN RETURN.

  
  FOR EACH zimkateg NO-LOCK WHERE zimkateg.typ = queasy.number1:
      FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr
          NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
          error-code = 21.
          msg-str    = zimkateg.kurzbez + " - " + zimmer.zinr.
          RETURN.
      END.
  END.
  
  FOR EACH ratecode NO-LOCK,
      FIRST zimkateg WHERE zimkateg.zikatnr = ratecode.zikatnr
      AND zimkateg.typ = t-queasy.number1 NO-LOCK
      BY ratecode.CODE:
      IF currCode NE ratecode.CODE THEN
      DO:
          ASSIGN
              currCode  = ratecode.CODE
              foundFlag = NO
          .
          DO curr-i = 1 TO 8:
              IF zimkateg.kurzbez = t-code[curr-i] THEN
              DO:
                  foundFlag = YES.
                  LEAVE.
              END.
          END.
          IF foundFlag THEN
          DO:
              ASSIGN
                  msg-str    = zimkateg.kurzbez + " - " + ratecode.CODE 
                  error-code = 22
              .
              RETURN.
          END.
      END.
  END.

  FIND FIRST zimkateg WHERE zimkateg.typ = queasy.number1
      NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE zimkateg:
      DO TRANSACTION:
          FIND FIRST zbuff WHERE RECID(zbuff) = RECID(zimkateg)
              EXCLUSIVE-LOCK.
          DELETE zbuff.
          RELEASE zbuff.
      END.
      FIND NEXT zimkateg WHERE zimkateg.typ = queasy.number1
         NO-LOCK NO-ERROR.
  END.

  DO TRANSACTION:
      FIND CURRENT queasy EXCLUSIVE-LOCK.
      DELETE queasy.
      RELEASE queasy.
  END.

END.
