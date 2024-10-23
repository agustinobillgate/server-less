DEF TEMP-TABLE old-rqBuff     LIKE reslin-queasy.
DEF TEMP-TABLE new-rqbuff     LIKE reslin-queasy.

DEF INPUT PARAMETER case-type     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER TABLE         FOR old-rqBuff.
DEF INPUT PARAMETER TABLE         FOR new-rqbuff.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

  CASE case-type:
    WHEN 1 THEN 
    DO:    
      FIND FIRST new-rqBuff NO-ERROR.
      IF NOT AVAILABLE new-rqBuff THEN RETURN.
      CREATE reslin-queasy.  /* create new record */
      BUFFER-COPY new-rQbuff TO reslin-queasy.
      FIND CURRENT reslin-queasy NO-LOCK.
      RELEASE reslin-queasy.
      success-flag = YES.
    END.
    WHEN 2 THEN /* update */
    DO:
      FIND FIRST old-rqBuff NO-ERROR.
      FIND FIRST new-rqBuff NO-ERROR.
      FIND FIRST reslin-queasy WHERE
        reslin-queasy.KEY          = old-rqBuff.KEY         AND
        reslin-queasy.resnr        = old-rqBuff.resnr       AND
        reslin-queasy.reslinnr     = old-rqBuff.reslinnr    AND
        reslin-queasy.number1      = old-rqBuff.number1     AND
        reslin-queasy.number2      = old-rqBuff.number2     AND
        reslin-queasy.number3      = old-rqBuff.number3     AND
        reslin-queasy.date1        = old-rqBuff.date1       AND
        reslin-queasy.date2        = old-rqBuff.date2       AND
        reslin-queasy.date3        = old-rqBuff.date3       AND
        reslin-queasy.char1        = old-rqBuff.char1       AND
        reslin-queasy.char2        = old-rqBuff.char2       AND
        reslin-queasy.char3        = old-rqBuff.char3       AND
        reslin-queasy.deci1        = old-rqBuff.deci1       AND
        reslin-queasy.deci2        = old-rqBuff.deci2       AND
        reslin-queasy.deci3        = old-rqBuff.deci3       AND
        reslin-queasy.logi1        = old-rqBuff.logi1       AND
        reslin-queasy.logi2        = old-rqBuff.logi2       AND
        reslin-queasy.logi3        = old-rqBuff.logi3 
      EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN 
      DO:
        BUFFER-COPY new-rqBuff TO reslin-queasy.
        FIND CURRENT reslin-queasy NO-LOCK.
        RELEASE reslin-queasy.
        success-flag = YES.
      END.
    END.
    WHEN 3 THEN /* delete */
    DO:
      FIND FIRST old-rqBuff NO-ERROR.
      FIND FIRST reslin-queasy WHERE
        reslin-queasy.KEY          = old-rqBuff.KEY         AND
        reslin-queasy.resnr        = old-rqBuff.resnr       AND
        reslin-queasy.reslinnr     = old-rqBuff.reslinnr    AND
        reslin-queasy.number1      = old-rqBuff.number1     AND
        reslin-queasy.number2      = old-rqBuff.number2     AND
        reslin-queasy.number3      = old-rqBuff.number3     AND
        reslin-queasy.date1        = old-rqBuff.date1       AND
        reslin-queasy.date2        = old-rqBuff.date2       AND
        reslin-queasy.date3        = old-rqBuff.date3       AND
        reslin-queasy.char1        = old-rqBuff.char1       AND
        reslin-queasy.char2        = old-rqBuff.char2       AND
        reslin-queasy.char3        = old-rqBuff.char3       AND
        reslin-queasy.deci1        = old-rqBuff.deci1       AND
        reslin-queasy.deci2        = old-rqBuff.deci2       AND
        reslin-queasy.deci3        = old-rqBuff.deci3       AND
        reslin-queasy.logi1        = old-rqBuff.logi1       AND
        reslin-queasy.logi2        = old-rqBuff.logi2       AND
        reslin-queasy.logi3        = old-rqBuff.logi3 
      EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN 
      DO:
        DELETE reslin-queasy.
        RELEASE reslin-queasy.
        success-flag = YES.
      END.
    END.
    /* SY 01 JUL 2017 */
    WHEN 4 THEN /* Save Guest Special Request */
    DO:
    DEF VARIABLE i-pos    AS INTEGER NO-UNDO.
    DEF VARIABLE ct       AS CHAR    NO-UNDO.
    DEF BUFFER rqbuff FOR reslin-queasy.
        FIND FIRST new-rqbuff.
        FIND FIRST reslin-queasy WHERE 
            reslin-queasy.key      = new-rqbuff.KEY   AND
            reslin-queasy.resnr    = new-rqbuff.resnr AND
            reslin-queasy.reslinnr = new-rqbuff.reslinnr 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
        DO:
            ASSIGN 
                reslin-queasy.date2   = new-rqbuff.date1
                reslin-queasy.number2 = new-rqbuff.number1
                reslin-queasy.char2   = new-rqbuff.char1
                reslin-queasy.char3   = new-rqbuff.char3.
            FIND CURRENT reslin-queasy NO-LOCK.
        END.
        ELSE
        DO:
            CREATE reslin-queasy.
            BUFFER-COPY new-rqbuff TO reslin-queasy.
            FIND CURRENT reslin-queasy NO-LOCK.
        END.
    END.
  END CASE.
