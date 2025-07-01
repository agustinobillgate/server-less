DEF TEMP-TABLE t-queasy33 LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER curr-dept AS INT.
DEF INPUT  PARAMETER curr-date AS DATE.
DEF INPUT  PARAMETER rec-id    AS INT.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-queasy33.

RUN del-res.

FOR EACH queasy WHERE queasy.KEY = 33 AND queasy.number1 = curr-dept 
    AND queasy.date1 = curr-date AND queasy.logi2 = NO 
    AND queasy.logi3 = YES AND queasy.betriebsnr = 0 NO-LOCK: /*FD add queasy.betriebsnr = 0*/
    CREATE t-queasy33.
    BUFFER-COPY queasy TO t-queasy33.
    ASSIGN t-queasy33.rec-id = RECID(queasy).
END.

PROCEDURE del-res:
DEF BUFFER qsy FOR queasy.
    DO TRANSACTION:
        FIND FIRST qsy WHERE RECID(qsy) = rec-id EXCLUSIVE-LOCK.
        ASSIGN
            qsy.logi3 = NO
            qsy.date3 = TODAY
            qsy.deci3 = TIME
            qsy.char3 = qsy.char3 + user-init + ";"
            qsy.betriebsnr = 2      /*FD Dec 13, 2022 => Feature Deposit Resto, betriebsnr = 2 (Cancel)*/
        .
        FIND CURRENT qsy NO-LOCK.
        RELEASE qsy.
    END.
END.
