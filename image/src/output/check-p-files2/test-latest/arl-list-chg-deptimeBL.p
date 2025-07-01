
DEF INPUT PARAMETER recid-resline AS INT.
DEF INPUT PARAMETER zeit AS INT.

DEFINE buffer resline FOR res-line. 

DO TRANSACTION:
    /* Rulita 131224 | Fixing serveless issue git 299 */
    /* FIND FIRST resline WHERE RECID(resline) = recid-resline EXCLUSIVE-LOCK.  */
    FIND FIRST resline WHERE RECID(resline) = recid-resline NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN 
    DO:    
        FIND CURRENT resline EXCLUSIVE-LOCK. 
        resline.abreisezeit = zeit. 

        FIND FIRST htparam WHERE paramnr = 341 NO-LOCK NO-ERROR. 
        IF htparam.fchar NE "" AND resline.resstatus = 6 THEN 
            RUN intevent-1.p( 9, resline.zinr, "Chg DepTime!", resline.resnr, resline.reslinnr). 

        FIND CURRENT resline NO-LOCK.
        RELEASE resline.
    END.
    /* End Rulita */
END.
