
DEF INPUT  PARAMETER rec-id         AS INTEGER.
DEF INPUT  PARAMETER i-case         AS INT.
DEF INPUT  PARAMETER gastnr         AS INT.
DEF INPUT  PARAMETER resnr          AS INT.
DEF INPUT  PARAMETER reslinnr       AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER mess-text-sv   AS CHAR.
DEF INPUT  PARAMETER caller-sv      AS CHAR.
DEF INPUT  PARAMETER rufnr-sv       AS CHAR.
DEF OUTPUT PARAMETER res-line-zinr  AS CHAR.
DEF OUTPUT PARAMETER recid-msg      AS INT.

FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-LOCK. 

IF i-case = 1 THEN
DO :
    RUN create-messages.
END.
ELSE
DO:
    FIND FIRST messages WHERE RECID(messages) = rec-id NO-LOCK.
    FIND CURRENT messages EXCLUSIVE-LOCK. 
    messages.messtext[1] = mess-text-sv.
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    /*username = bediener.username. */ /*Eko FIX LOG APPSRV 12April2016*/
    messages.usre = bediener.userinit. 
    FIND CURRENT messages NO-LOCK. 
END.


PROCEDURE create-messages: 
  create messages. 
  messages.gastnr = gastnr. 
  messages.resnr = resnr. 
  messages.reslinnr = reslinnr. 
  messages.zeit = time. 
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
  messages.usre = bediener.userinit. 
  messages.zinr = res-line.zinr. 
  
  messages.messtext[1] = /*mess-text:screen-value IN FRAME frame1.*/ mess-text-sv.
  messages.messtext[2] = /*caller:screen-value IN FRAME frame1.*/ caller-sv.
  messages.messtext[3] = /*rufnr:screen-value IN FRAME frame1.*/ rufnr-sv.

  res-line-zinr = res-line.zinr.
  recid-msg = RECID(messages).
  /*
  tot = tot + 1. 
  nr = tot. 
  create mess-list. 
  mess-list.nr = nr. 
  mess-list.mess-recid = RECID(messages). 
  */
  FIND CURRENT messages NO-LOCK. 
 
  /** switch ON MESSAGE lamp ***/ 
  FIND FIRST htparam WHERE paramnr = 310 NO-LOCK. 
  IF flogical THEN 
  DO: 
   IF res-line.active-flag = 1 THEN 
     RUN intevent-1.p( 4, res-line.zinr, "Message Lamp on!", res-line.resnr, res-line.reslinnr). 
  END. 
END. 
