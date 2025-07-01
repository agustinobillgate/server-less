DEF INPUT PARAMETER  pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER gastno       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-kontcode AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER error-flag  AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER msg-str     AS CHAR    NO-UNDO INIT "".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "global-allotment". 

RUN check-global-allotment.

PROCEDURE check-global-allotment:
DEF BUFFER kline FOR kontline.
  DEF VAR tokcounter AS INTEGER NO-UNDO.
  DEF VAR mesValue   AS CHAR    NO-UNDO.

  FIND FIRST queasy WHERE queasy.KEY = 147
    AND queasy.number1 = gastno
    AND queasy.char1   = inp-kontcode NO-LOCK.

  DO tokcounter = 1 TO NUM-ENTRIES(queasy.char3, ","):
    mesValue = ENTRY(tokcounter, queasy.char3, ",").
    IF mesValue NE "" THEN
    DO:
      FOR EACH res-line WHERE res-line.gastnr = integer(mesValue)
        AND res-line.kontignr GT 0 AND res-line.active-flag LE 1 NO-LOCK:
        FIND FIRST kline WHERE kline.kontignr = res-line.kontignr NO-LOCK NO-ERROR.
        IF AVAILABLE kline AND kline.kontcode = queasy.char1 THEN
        DO:
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                NO-LOCK.
            msg-str = translateExtended ("Can not remove as reservation found using the allotment:",lvCAREA,"")
                + CHR(10)
                + STRING(reservation.NAME) + " #" + STRING(res-line.resnr)
                + " " + STRING(res-line.ankunft) + "-" + STRING(res-line.abreise) + CHR(10).
            error-flag = YES.
            RETURN.
        END.
      END.
    END.
  END.
END. 
