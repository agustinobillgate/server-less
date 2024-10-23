
DEF INPUT PARAMETER recid-resline AS INT.
DEF INPUT PARAMETER zeit AS INT.

DEFINE buffer resline FOR res-line. 

DO TRANSACTION:
    FIND FIRST resline WHERE RECID(resline) = recid-resline EXCLUSIVE-LOCK. 
    resline.abreisezeit = zeit. 
    FIND CURRENT resline NO-LOCK. 

    FIND FIRST htparam WHERE paramnr = 341 NO-LOCK. 
    IF htparam.fchar NE "" AND resline.resstatus = 6 THEN 
        RUN intevent-1.p( 9, resline.zinr, "Chg DepTime!", resline.resnr, resline.reslinnr). 
END.
