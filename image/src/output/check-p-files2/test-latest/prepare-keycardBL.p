DEF INPUT  PARAMETER res-number     AS INT.
DEF INPUT  PARAMETER resline-number AS INT.
DEF OUTPUT PARAMETER guest-name     AS CHARACTER.
DEF OUTPUT PARAMETER room-number    AS CHARACTER.
DEF OUTPUT PARAMETER checkout-date  AS DATE.
DEF OUTPUT PARAMETER gname          AS CHARACTER.
DEF OUTPUT PARAMETER checkout-time  AS INT.
DEF OUTPUT PARAMETER checkin-date   AS DATE.
DEF OUTPUT PARAMETER checkin-time   AS INT.

DEFINE BUFFER bfR FOR res-line.
FIND FIRST res-line WHERE res-line.resnr EQ res-number AND res-line.reslinnr EQ resline-number NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN 
DO:
    ASSIGN
    guest-name    = res-line.name
    room-number   = res-line.zinr
    checkout-date = res-line.abreise
    gname         = res-line.name
    checkout-time = res-line.abreisezeit
    checkin-date  = res-line.ankunft
    checkin-time  = res-line.ankzeit
    .
END.
