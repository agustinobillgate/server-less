DEFINE TEMP-TABLE mess-list 
  FIELD nr AS INTEGER 
  FIELD mess-recid AS INTEGER. 

DEF INPUT  PARAMETER if-flag    AS LOGICAL. 
DEF INPUT  PARAMETER gastnr     AS INT.
DEF INPUT  PARAMETER resnr      AS INT.
DEF INPUT  PARAMETER reslinnr   AS INT.
DEF OUTPUT PARAMETER nr         AS INT.
DEF OUTPUT PARAMETER tot        AS INT.
DEF OUTPUT PARAMETER TABLE FOR mess-list.

FOR EACH mess-list:
    delete mess-list.
END. 
FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-LOCK.
nr = 0. 
FOR EACH messages WHERE messages.gastnr = gastnr AND 
    messages.resnr = resnr AND messages.reslinnr = reslinnr NO-LOCK 
    BY (STRING(year(datum)) + STRING(month(datum)) 
      + STRING(day(datum)) + STRING(zeit)) : 
    create mess-list. 
    nr = nr + 1. 
    mess-list.nr = nr. 
    mess-list.mess-recid = RECID(messages). 
END. 
tot = nr. 
IF nr GT 1 THEN nr = 1.

IF tot = 0 THEN 
DO TRANSACTION: 
    FIND FIRST htparam WHERE paramnr = 310 NO-LOCK. /* license MESSAGE lamp */ 
    IF htparam.flogical AND if-flag AND res-line.active-flag = 1 THEN 
      RUN intevent-1.p( 5, res-line.zinr, "Message Lamp off!", res-line.resnr, res-line.reslinnr). 
    FIND CURRENT res-line EXCLUSIVE-LOCK. 
    res-line.wabkurz = "". 
    FIND CURRENT res-line NO-LOCK. 
END. 
