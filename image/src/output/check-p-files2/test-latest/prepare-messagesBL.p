
DEF INPUT  PARAMETER gastnr     AS INT.
DEF INPUT  PARAMETER resnr      AS INT.
DEF INPUT  PARAMETER reslinnr   AS INT.
DEF OUTPUT PARAMETER gname      AS CHAR.
DEF OUTPUT PARAMETER arrival    AS DATE.
DEF OUTPUT PARAMETER depart     AS DATE.
DEF OUTPUT PARAMETER zinr       AS CHAR.
DEF OUTPUT PARAMETER pguest     AS LOGICAL.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
        + " " + guest.anrede1. 
FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-LOCK. 
arrival = res-line.ankunft. 
depart = res-line.abreise. 
zinr = res-line.zinr. 
IF res-line.resstatus = 6 OR res-line.resstatus = 13 THEN pguest = YES. 
