
DEF VAR ci-date AS DATE.
DEF VAR active-deposit AS LOGICAL.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr EQ 588 NO-LOCK NO-ERROR. /*FDL Dec 26, 2022 => Resto Deposit*/
IF AVAILABLE htparam THEN active-deposit = htparam.flogical.

RUN del-old-bons.

PROCEDURE del-old-bons: 
DEFINE VARIABLE bill-date AS DATE. 
DEFINE VARIABLE anz AS INTEGER.
DEFINE BUFFER qsy           FOR queasy.
DEFINE BUFFER q251          FOR queasy.
DEFINE BUFFER qkds-header   FOR queasy.
DEFINE BUFFER qkds-line     FOR queasy.

  FIND FIRST htparam WHERE paramnr = 110 no-lock.   /* bill-date*/ 
  bill-date = htparam.fdate. 

  /*FDL Dec 26, 2022 => Feature Resto Deposit*/
  FIND FIRST htparam WHERE paramnr = 164 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 7. 

  FIND FIRST queasy WHERE key = 3 AND queasy.date1 LT bill-date NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE queasy: 
      DO TRANSACTION: 
        FIND CURRENT queasy EXCLUSIVE-LOCK. 
        DELETE queasy. 
      END. 
      FIND NEXT queasy WHERE key = 3 AND queasy.date1 LT bill-date NO-LOCK NO-ERROR. 
  END.

  /*MASDOD 18/07/24 => Feature Delete Data Kitchen Display*/
  FIND FIRST qkds-line WHERE qkds-line.KEY EQ 255
      AND qkds-line.char1 EQ "kds-line"
      AND qkds-line.date1 EQ bill-date NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE qkds-line:  
      DO TRANSACTION:
          FIND CURRENT qkds-line EXCLUSIVE-LOCK.
          qkds-line.char3 = "4".
          FIND CURRENT qkds-line NO-LOCK.
          RELEASE qkds-line.
      END.
      FIND NEXT qkds-line WHERE qkds-line.KEY EQ 255
          AND qkds-line.char1 EQ "kds-line"
          AND qkds-line.date1 EQ bill-date NO-LOCK NO-ERROR.
  END.
  
  FIND FIRST qkds-header WHERE qkds-header.KEY EQ 257
      AND qkds-header.char1 EQ "kds-header"
      AND qkds-header.date1 EQ bill-date NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE qkds-header:  
      DO TRANSACTION:
          FIND CURRENT qkds-header EXCLUSIVE-LOCK.
          qkds-header.deci2 = 4.
          FIND CURRENT qkds-header NO-LOCK.  
          RELEASE qkds-header.
      END.
      FIND NEXT qkds-header WHERE qkds-header.KEY EQ 257
          AND qkds-header.char1 EQ "kds-header"
          AND qkds-header.date1 EQ bill-date NO-LOCK NO-ERROR.
  END.
  
  IF active-deposit THEN /*FDL Dec 26, 2022 => Feature Resto Deposit*/
  DO:
    /* delete old table reservation with Resto Deposit*/
    FIND FIRST queasy WHERE queasy.key = 33
        AND queasy.date1 LE (ci-date - anz)  NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE queasy: 
        DO TRANSACTION: 
            FIND FIRST q251 WHERE q251.KEY EQ 251 
                AND q251.number2 EQ INT(RECID(queasy)) EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE q251 THEN
            DO:
                DELETE q251.
                RELEASE q251.
            END.

            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK. 
            DELETE qsy.
            RELEASE qsy.
        END. 
        FIND NEXT queasy WHERE queasy.key = 33
            AND queasy.date1 LE (ci-date - anz) NO-LOCK NO-ERROR. 
    END.
  END.
  ELSE /*ORI*/
  DO:
      /*OLD FDL Comment
    /* delete old table reservation */
    FIND FIRST queasy WHERE queasy.key = 33
      AND queasy.date1 LE (ci-date - 2)  NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE queasy: 
        DO TRANSACTION: 
          FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) 
            EXCLUSIVE-LOCK. 
          DELETE qsy.
          RELEASE qsy.
        END. 
        FIND NEXT queasy WHERE queasy.key = 33
          AND queasy.date1 LE (ci-date - 2) NO-LOCK NO-ERROR. 
    END. */

    /* FDL delete old table reservation after 2 years*/
    FIND FIRST queasy WHERE queasy.key = 33
      AND queasy.date1 LE (ci-date - 730)  NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE queasy: 
        DO TRANSACTION: 
          FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) 
            EXCLUSIVE-LOCK. 
          DELETE qsy.
          RELEASE qsy.
        END. 
        FIND NEXT queasy WHERE queasy.key = 33
          AND queasy.date1 LE (ci-date - 730) NO-LOCK NO-ERROR. 
    END. 
  END.
END. 
