
DEF INPUT PARAMETER t-messages-resnr    AS INT.
DEF INPUT PARAMETER t-messages-reslinnr AS INT.
DEF INPUT PARAMETER rec-id              AS INT.

DO TRANSACTION: 
    FIND FIRST messages WHERE RECID(messages) = rec-id NO-LOCK.
    IF AVAILABLE messages THEN
    DO:
        FIND CURRENT messages EXCLUSIVE-LOCK. 
        messages.betriebsnr = 1. 
        FIND CURRENT messages NO-LOCK. 
    END.

    /*RUN messages-update-reslinebl.p (rec-id, t-messages-resnr, t-messages-reslinnr).*/
    FIND FIRST res-line WHERE res-line.resnr = t-messages-resnr
        AND res-line.reslinnr = t-messages-reslinnr NO-LOCK.

    FIND FIRST htparam WHERE paramnr = 310 NO-LOCK. /* license MESSAGE lamp */ 
    IF htparam.flogical AND res-line.active-flag = 1 THEN 
      RUN intevent-1.p( 5, res-line.zinr, "Message Lamp off!", res-line.resnr, res-line.reslinnr). 
    FIND CURRENT res-line EXCLUSIVE-LOCK. 
    res-line.wabkurz = "". 
    FIND CURRENT res-line NO-LOCK. 
END. 
