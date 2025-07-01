DEFINE TEMP-TABLE res-detail
    FIELD guest-name    AS CHARACTER
    FIELD arrival       AS DATE
    FIELD departure     AS DATE
    FIELD arr-time      AS CHARACTER
    FIELD room-type     AS CHARACTER
    FIELD room-number   AS CHARACTER
    FIELD room-rate     AS DECIMAL
    FIELD room-qty      AS INTEGER
    FIELD argt-code     AS CHARACTER
    FIELD res-number    AS INTEGER
    FIELD turnover      AS DECIMAL
    FIELD art-number    AS INTEGER
    FIELD segment-code  AS INTEGER
    FIELD remark        AS CHARACTER
    .

DEFINE INPUT PARAMETER t-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER f-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER room   AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR res-detail.

FOR EACH res-line WHERE (res-line.active-flag LE 1 
    AND res-line.resstatus NE 12
    AND res-line.resstatus LE 13
    AND res-line.resstatus NE 4
    AND NOT (res-line.ankunft GT t-date) 
    AND NOT (res-line.abreise LT f-date))
    AND res-line.l-zuordnung[3] EQ 0
    AND res-line.zinr EQ room
    AND res-line.zipreis NE 0 NO-LOCK,
    FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK,    
    FIRST zimkateg WHERE zimkateg.zikatnr EQ res-line.zikatnr  
    NO-LOCK BY res-line.NAME:

    CREATE res-detail.
    ASSIGN
        res-detail.guest-name   = res-line.NAME  
        res-detail.arrival      = res-line.ankunft
        res-detail.departure    = res-line.abreise
        res-detail.arr-time     = STRING(res-line.ankzeit, "HH:MM")
        res-detail.room-type    = zimkateg.kurzbez
        res-detail.room-number  = res-line.zinr
        res-detail.room-rate    = res-line.zipreis
        res-detail.room-qty     = res-line.zimmeranz
        res-detail.argt-code    = res-line.arrangement
        res-detail.res-number   = res-line.resnr
        res-detail.segment-code = reservation.segmentcode
        res-detail.remark       = res-line.bemerk
        .
    
    res-detail.remark = REPLACE(res-detail.remark,CHR(10),"").
    res-detail.remark = REPLACE(res-detail.remark,CHR(13),"").
    res-detail.remark = REPLACE(res-detail.remark,"~n","").
    res-detail.remark = REPLACE(res-detail.remark,"\n","").
    res-detail.remark = REPLACE(res-detail.remark,"~r","").
    res-detail.remark = REPLACE(res-detail.remark,"~r~n","").
    res-detail.remark = REPLACE(res-detail.remark,"&nbsp;"," ").
    res-detail.remark = REPLACE(res-detail.remark,"</p>","</p></p>").
    res-detail.remark = REPLACE(res-detail.remark,"</p>",CHR(13)).
    res-detail.remark = REPLACE(res-detail.remark,"<BR>",CHR(13)).
    res-detail.remark = REPLACE(res-detail.remark,CHR(10) + CHR(13),"").
    res-detail.remark = REPLACE(res-detail.remark,CHR(2),"").
    res-detail.remark = REPLACE(res-detail.remark,CHR(3),"").
    res-detail.remark = REPLACE(res-detail.remark,CHR(4),"").

    IF LENGTH(res-detail.remark) LT 3 THEN res-detail.remark = REPLACE(res-detail.remark,CHR(32),"").
    IF LENGTH(res-detail.remark) LT 3 THEN res-detail.remark = "".
    IF LENGTH(res-detail.remark) EQ ? THEN res-detail.remark = "".    
END.                         
