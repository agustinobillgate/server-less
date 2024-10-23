DEF TEMP-TABLE t-reslin-queasy LIKE reslin-queasy.

DEF INPUT PARAMETER TABLE FOR t-reslin-queasy.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

  FIND FIRST t-reslin-queasy NO-ERROR.
  IF AVAILABLE t-reslin-queasy THEN
  FIND FIRST reslin-queasy WHERE
    reslin-queasy.KEY          = t-reslin-queasy.KEY         AND
    reslin-queasy.resnr        = t-reslin-queasy.resnr       AND
    reslin-queasy.reslinnr     = t-reslin-queasy.reslinnr    AND
    reslin-queasy.number1      = t-reslin-queasy.number1     AND
    reslin-queasy.number2      = t-reslin-queasy.number2     AND
    reslin-queasy.number3      = t-reslin-queasy.number3     AND
    reslin-queasy.date1        = t-reslin-queasy.date1       AND
    reslin-queasy.date2        = t-reslin-queasy.date2       AND
    reslin-queasy.date3        = t-reslin-queasy.date3       AND
    reslin-queasy.char1        = t-reslin-queasy.char1       AND
    reslin-queasy.char2        = t-reslin-queasy.char2       AND
    reslin-queasy.char3        = t-reslin-queasy.char3       AND
    reslin-queasy.deci1        = t-reslin-queasy.deci1       AND
    reslin-queasy.deci2        = t-reslin-queasy.deci2       AND
    reslin-queasy.deci3        = t-reslin-queasy.deci3       AND
    reslin-queasy.logi1        = t-reslin-queasy.logi1       AND
    reslin-queasy.logi2        = t-reslin-queasy.logi2       AND
    reslin-queasy.logi3        = t-reslin-queasy.logi3 
    EXCLUSIVE-LOCK NO-ERROR.

  IF AVAILABLE reslin-queasy THEN
  DO:
      DELETE reslin-queasy.
      RELEASE reslin-queasy.
      success-flag = YES.
  END.
