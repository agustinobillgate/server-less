 
/************  UPDATE Guest Name AT bill, rerservation AND res-line  *************/ 
 
DEFINE INPUT PARAMETER gastnr AS INTEGER. 

DEFINE BUFFER bbill FOR bill.
DEFINE BUFFER rsev  FOR reservation.
DEFINE BUFFER rline FOR res-line.
DEFINE BUFFER bdebt FOR debitor.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK NO-ERROR. 

FIND FIRST bill WHERE bill.gastnr = gastnr NO-LOCK NO-ERROR.
DO WHILE AVAILABLE bill:
    DO TRANSACTION:
        FIND FIRST bbill WHERE RECID(bbill) = RECID(bill) EXCLUSIVE-LOCK.
        ASSIGN bbill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                           + " " + guest.anrede1. 
        FIND CURRENT bbill NO-LOCK.
        RELEASE bbill.
    END.
    FIND NEXT bill WHERE bill.gastnr = gastnr NO-LOCK NO-ERROR.
END.

FIND FIRST reservation WHERE reservation.gastnr = gastnr 
    AND reservation.activeflag = 0 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE reservation:
    DO TRANSACTION:
        FIND FIRST rsev WHERE RECID(rsev) = RECID(reservation) EXCLUSIVE-LOCK.
        ASSIGN 
            rsev.name = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                        + " " + guest.anrede1. 
        FIND CURRENT rsev NO-LOCK.
        RELEASE rsev.
    END.

    FIND NEXT reservation WHERE reservation.gastnr = gastnr 
        AND reservation.activeflag = 0 NO-LOCK NO-ERROR.
END.
 
FIND FIRST res-line WHERE res-line.gastnrmember = gastnr 
  AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE res-line:
    DO TRANSACTION:
        FIND FIRST rline WHERE RECID(rline) = RECID(res-line) EXCLUSIVE-LOCK.
        ASSIGN rline.name = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                               + " " + guest.anrede1. 
        FIND CURRENT rline NO-LOCK.
        RELEASE rline.
    END.

    /*Alder - Serverless - Issue 481 - Start*/
    FIND FIRST htparam WHERE htparam.paramnr = 307 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam AND htparam.flogical THEN 
    DO: 
        IF res-line.active-flag = 1 THEN
        DO:
            RUN intevent-1.p(1, res-line.zinr, "Change Guestname!", 
                           res-line.resnr, res-line.reslinnr).
        END.
    END. 
    /*Alder - Serverless - Issue 481 - End*/
    
    FIND NEXT res-line WHERE res-line.gastnrmember = gastnr 
          AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
END.

FIND FIRST debitor WHERE debitor.opart LE 1
    AND debitor.gastnr = gastnr NO-LOCK NO-ERROR.
DO WHILE AVAILABLE debitor:
    DO TRANSACTION:
        FIND FIRST bdebt WHERE RECID(bdebt) = RECID(debitor) EXCLUSIVE-LOCK.
        ASSIGN 
            bdebt.name = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                           + " " + guest.anrede1. 
        FIND FIRST bdebt NO-LOCK.
        RELEASE bdebt.

    END.
    FIND NEXT debitor WHERE debitor.opart LE 1
        AND debitor.gastnr = gastnr NO-LOCK NO-ERROR.
END.


/* 
CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow"). 
*/
