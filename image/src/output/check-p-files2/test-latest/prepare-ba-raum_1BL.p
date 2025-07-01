

DEF TEMP-TABLE t-bk-raum LIKE bk-raum
    FIELD rec-id AS INT
    FIELD flag-desc AS LOGICAL.

DEF OUTPUT PARAMETER TABLE FOR t-bk-raum.

FOR EACH bk-raum NO-LOCK BY bk-raum.departement BY bk-raum.raum:
    CREATE t-bk-raum.
    BUFFER-COPY bk-raum TO t-bk-raum.
    ASSIGN t-bk-raum.rec-id = RECID(bk-raum).

    /*FD 19 Dec, 19 - Req Chanti tiket no 7241F8*/
    IF bk-raum.betriebsnr = 0 THEN
        t-bk-raum.flag-desc = NO.
    ELSE IF bk-raum.betriebsnr = 1 THEN
        t-bk-raum.flag-desc = YES.
END.

