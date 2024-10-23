DEFINE TEMP-TABLE t-cflow1        LIKE queasy.

DEFINE INPUT PARAMETER case-type     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-cflow1.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO INIT NO.

DEFINE BUFFER t-queasy FOR queasy.

CASE case-type:
    WHEN 1 THEN DO:  /*delete*/
        FIND FIRST t-cflow1 NO-LOCK NO-ERROR.
        IF AVAILABLE t-cflow1 THEN DO:
             FIND FIRST queasy WHERE queasy.KEY = 177 
                 AND /*queasy.number1 = t-cflow1.deci1*/ queasy.deci1 = t-cflow1.deci1 NO-LOCK NO-ERROR.  /*gerald integer gabisa 10digit 070122 #315260*/
              IF AVAILABLE queasy THEN DO:
                FIND FIRST t-queasy WHERE RECID(t-queasy) = RECID(queasy) EXCLUSIVE-LOCK.
                DELETE t-queasy.
                RELEASE t-queasy.
                success-flag = YES.
            END.
        END.             
    END.


   WHEN 2 THEN DO: /*add new*/
      FIND FIRST t-cflow1 NO-LOCK NO-ERROR.
      IF AVAILABLE t-cflow1 THEN 
      DO:
        FIND FIRST t-queasy WHERE t-queasy.KEY = 177 AND t-queasy.deci1 = t-cflow1.deci1 NO-LOCK NO-ERROR.
        IF AVAILABLE t-queasy THEN
        DO:
          success-flag = NO.
        END.
        ELSE 
        DO:
          CREATE queasy.
          BUFFER-COPY t-cflow1 TO queasy.
          success-flag = YES.
        END.
      END.
    END.

    WHEN 3 THEN DO: /*chg*/
      FIND FIRST t-cflow1 NO-LOCK NO-ERROR.
      IF AVAILABLE t-cflow1 THEN 
      DO:
        FIND FIRST queasy WHERE queasy.KEY = 177 AND t-cflow1.deci1 = queasy.deci1
           /*AND queasy.number1 = t-cflow1.deci1*/ /*queasy.deci1 = t-cflow1.deci1*/ NO-LOCK NO-ERROR. /*gerald integer gabisa 10digit 070122 #315260*/
        IF AVAILABLE queasy THEN 
        DO: 
          FIND FIRST t-queasy WHERE RECID(t-queasy) = RECID(queasy) EXCLUSIVE-LOCK.
           ASSIGN
              /*t-queasy.number1 = t-cflow1.number1*/
              t-queasy.deci1   = t-cflow1.deci1
              t-queasy.char1   = t-cflow1.char1
              t-queasy.logi1   = t-cflow1.logi1.                          
           FIND CURRENT t-queasy NO-LOCK.
           RELEASE t-queasy.
           success-flag = YES.
        END.
      END.
    END.
END CASE.



