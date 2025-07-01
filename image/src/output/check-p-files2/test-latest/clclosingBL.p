

DEFINE VARIABLE billdate AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN billdate = htparam.fdate.

RUN check-class.
RUN check-inhouse.
RUN check-locker.
RUN check-visit.
RUN create-renewal.
RUN check-expired.
RUN delete-history.
RUN check-others.




PROCEDURE check-memtype:
    DEF BUFFER memtype FOR cl-memtype.
    FOR EACH cl-memtype NO-LOCK:
        IF cl-memtype.tdate LT TODAY AND cl-memtype.activeflag = YES THEN
        DO:
            FIND FIRST memtype WHERE RECID(memtype) = RECID(cl-memtype)
                EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE memtype THEN 
            DO:
                memtype.activeflag = NO.
                FIND CURRENT memtype NO-LOCK.
            END.
        END.                           
        ELSE IF cl-memtype.activeflag = NO AND cl-memtype.tdate GT TODAY THEN
        DO:
            FIND FIRST memtype WHERE RECID(memtype) = RECID(cl-memtype)
                EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE memtype THEN
            DO:
                memtype.activeflag = YES.
                FIND CURRENT memtype NO-LOCK.
            END.                         
        END.
    END.           
END.

PROCEDURE check-class:
    DEF BUFFER class FOR cl-class.
    FOR EACH cl-class NO-LOCK:
        IF cl-class.end-date LT TODAY AND cl-class.activeflag = YES THEN
        DO:
            FIND FIRST class WHERE RECID(class) = RECID(cl-class)
                EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE class THEN
            DO:
                class.activeflag = NO.
                FIND CURRENT class NO-LOCK.
            END.
        END.
        ELSE IF cl-class.activeflag = NO AND cl-class.start-date LE TODAY THEN
        DO:
            FIND FIRST class WHERE RECID(class) = RECID(cl-class) 
                EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE class THEN
            DO:
                class.activeflag = YES.
                FIND CURRENT class NO-LOCK.
            END.
        END.
    END.                                    
END.

PROCEDURE check-inhouse:
    DEF BUFFER membr FOR cl-member.
    FOR EACH cl-member WHERE checked-in = YES AND last-visit LT TODAY NO-LOCK:
        FIND FIRST membr WHERE RECID(membr) = RECID(cl-member) EXCLUSIVE-LOCK 
            NO-ERROR.
        IF AVAILABLE membr THEN
        DO:
            membr.checked-in = NO.
            membr.co-time = TIME.
            FIND CURRENT membr NO-LOCK.
        END.
        FIND FIRST cl-histci WHERE cl-histci.codenum = cl-member.codenum AND
            cl-histci.datum = cl-member.last-visit AND cl-histci.starttime = 
            cl-member.ci-time EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-histci THEN 
        DO:
            cl-histci.endtime = cl-member.co-time.
            FIND CURRENT cl-histci NO-LOCK.
        END.
        /*
        FIND FIRST guest WHERE guest.gastnr = cl-member.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN 
        */
    END.
END.

PROCEDURE check-others:
    DEF BUFFER hbuff FOR cl-histci.
    FOR EACH cl-histci WHERE cl-histci.datum LT TODAY AND cl-histci.num1 = 2
        AND cl-histci.voucherno NE "" NO-LOCK:
        FIND FIRST hbuff WHERE RECID(hbuff) = RECID(cl-histci) EXCLUSIVE-LOCK.
        ASSIGN hbuff.num1 = 5.
        RELEASE hbuff.
    END.
END.

PROCEDURE check-locker:
    FOR EACH cl-locker WHERE valid-flag = YES AND cl-locker.to-date LT TODAY
        AND cl-locker.locknum NE "" NO-LOCK:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 118
            queasy.char1 = cl-locker.locknum
            queasy.number1 = cl-locker.location
            queasy.date1 = cl-locker.from-date
            queasy.date2 = cl-locker.to-date
            queasy.number2 = cl-locker.from-time
            queasy.number3 = cl-locker.to-time.
        FIND CURRENT queasy NO-LOCK.
    END.
END.

PROCEDURE check-visit:
    DEF BUFFER visit FOR cl-histvisit.
    DEF BUFFER gbuff FOR guest.
    DEF BUFFER mbuff FOR cl-member.

    FOR EACH cl-histvisit WHERE datum LT TODAY AND endtime = ? NO-LOCK :
        FIND FIRST cl-class WHERE cl-class.nr = cl-histvisit.service NO-LOCK NO-ERROR.
        IF cl-histvisit.trainflag THEN
        DO:  
            FIND FIRST visit WHERE RECID(visit) = RECID(cl-histvisit)
                EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE visit THEN
            DO:
                visit.endtime = (Integer(SUBSTR(cl-class.end-time, 1, 2)) * 3600) + 
                (INTEGER(SUBSTR(cl-class.end-time, 3, 2)) * 60).
                FIND CURRENT visit NO-LOCK.
            END.
        END.
        ELSE
        DO:
            FIND FIRST visit WHERE RECID(visit) = RECID(cl-histvisit)
                EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE visit THEN
            DO:
                visit.endtime = TIME. 
                FIND CURRENT visit NO-LOCK.
            END.
        END. 

        FIND FIRST mbuff WHERE mbuff.codenum = cl-histvisit.codenum USE-INDEX codenum_ix NO-LOCK NO-ERROR.
        IF AVAILABLE mbuff THEN
        DO:
            /*
            FIND FIRST gbuff WHERE gbuff.gastnr = mbuff.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            curr-bezeich1 = gbuff.NAME + ", " + gbuff.vorname1 + gbuff.anrede1.
            */
        END.
    END.
END.

PROCEDURE create-renewal:
    DEF VAR ndays     AS INTEGER INITIAL 30 NO-UNDO.
    DEF VAR curr-date AS DATE NO-UNDO.
    DEF VAR exp-date  AS DATE NO-UNDO.
    DEF VAR mfee      AS DECIMAL NO-UNDO.
    DEF BUFFER gbuff  FOR guest.
    DEF BUFFER mbuff  FOR cl-member.
    DEF BUFFER mbuff1 FOR cl-member.

    FIND FIRST htparam WHERE paramnr = 1049 NO-LOCK NO-ERROR.
    IF (NOT AVAILABLE htparam) 
      OR (AVAILABLE htparam AND htparam.finteger GT 0) THEN
    ASSIGN ndays = htparam.finteger.

    FOR EACH mbuff WHERE mbuff.memstatus = 1 AND 
        (mbuff.expired-date - billdate ) EQ ndays NO-LOCK:
        FIND FIRST cl-memtype WHERE cl-memtype.nr = mbuff.membertype 
            NO-LOCK NO-ERROR.
        RUN clcount-expiredbl.p(mbuff.codenum, OUTPUT exp-date).
        
        mfee = cl-memtype.fee1.
        IF mbuff.deci2 NE 0 OR mbuff.logi1 THEN mfee = mbuff.deci2.

        DO:
          FOR EACH mc-fee WHERE
              mc-fee.KEY        = 2                 AND
              mc-fee.gastnr     = mbuff.gastnr      AND
              mc-fee.activeflag = 1:
            ASSIGN mc-fee.activeflag = 2.
          END.
          FIND FIRST mc-fee EXCLUSIVE-LOCK WHERE
              mc-fee.KEY        = 2                 AND
              mc-fee.nr         = mbuff.membertype  AND
              mc-fee.gastnr     = mbuff.gastnr      AND
              mc-fee.bis-datum  = exp-date          NO-ERROR.

          IF NOT AVAILABLE mc-fee THEN CREATE mc-fee.
          DO:
            ASSIGN 
              mc-fee.KEY        = 2
              mc-fee.usr-init   = "$$"
              mc-fee.bez-datum2 = billdate
              mc-fee.von-datum  = mbuff.expired-date + 1
              mc-fee.bis-datum  = exp-date
              mc-fee.nr         = mbuff.membertype
              mc-fee.gastnr     = mbuff.gastnr
              mc-fee.betrag     = mfee
            .
          END.
        END.

        /*
        FIND FIRST gbuff WHERE gbuff.gastnr = mbuff.gastnr 
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE gbuff THEN curr-bezeich1 = gbuff.NAME + ", " + gbuff.vorname1.
        */
    END.
END.

PROCEDURE check-expired:
    DEF VAR max-freeze  AS INTEGER NO-UNDO.
    DEF VAR curr-status AS INTEGER NO-UNDO.
    DEF VAR add-days    AS INTEGER NO-UNDO.
    DEF BUFFER guest1   FOR guest.
    DEF BUFFER mbuff    FOR cl-member.

    FIND FIRST htparam WHERE paramnr = 1040 NO-LOCK NO-ERROR.
    max-freeze = htparam.finteger.
    FIND FIRST htparam WHERE paramnr = 1066 NO-LOCK.
    add-days = htparam.finteger.

    FOR EACH cl-member WHERE cl-member.memstatus = 1 AND
        (billdate - cl-member.expired-date - add-days) GE 0 NO-LOCK:
        DO TRANSACTION:
/*            
            IF cl-member.numfreeze LE max-freeze  THEN
                curr-status = 2.
            ELSE
                curr-status = 3.
*/          ASSIGN curr-status = 2.

            FIND FIRST guest1 WHERE guest1.gastnr = cl-member.gastnr NO-LOCK NO-ERROR.
            CREATE cl-log.
            ASSIGN
                cl-log.codenum   = cl-member.codenum
                cl-log.datum     = TODAY
                cl-log.zeit      = TIME
                cl-log.user-init = " "
                cl-log.CHAR1 = string(cl-member.membertype)     + " ; " + string(cl-member.membertype) 
                + " ; " + STRING(cl-member.memstatus)           + " ; " + STRING(curr-status) 
                + " ; " + cl-member.pict-file                   + " ; " + cl-member.pict-file
                + " ; " + cl-member.load-by                     + " ; " + cl-member.load-by
                + " ; " + STRING(cl-member.billgastnr, ">>>>>9") + " ; " + STRING(cl-member.billgastnr, ">>>>>9") 
                + " ; " + STRING(guest1.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + STRING(guest1.kreditlimit, ">>,>>>,>>>,>>9")
                + " ; " + STRING(cl-member.paysched)            + " ; " + STRING(cl-member.paysched)
                + " ; " + STRING(cl-member.billcycle)           + " ; " + STRING(cl-member.billcycle)
                + " ; " + STRING(cl-member.expired)             + " ; " + STRING(TODAY)
                + " ; " + cl-member.user-init1                  + " ; "  + " " 
                + " ; " + STRING(cl-member.main-gastnr)         + " ; " + STRING(cl-member.gastnr)
                .
            FIND FIRST mbuff WHERE RECID(mbuff) = RECID(cl-member)
                EXCLUSIVE-LOCK.
            ASSIGN mbuff.memstatus = curr-status.
            FIND CURRENT mbuff NO-LOCK.
            
            /*
            FIND FIRST guest WHERE guest.gastnr = cl-member.gastnr 
                USE-INDEX gastnr_index EXCLUSIVE-LOCK.
            IF AVAILABLE guest THEN curr-bezeich1 = guest.NAME + " " + guest.vorname1.
            */
            CREATE cl-histstat.
            ASSIGN cl-histstat.datum = TODAY
                cl-histstat.codenum = mbuff.codenum
                cl-histstat.memstatus = mbuff.memstatus
                cl-histstat.user-init = "Night Audit"
                cl-histstat.zeit = TIME
                .
            
            FOR EACH cl-enroll WHERE cl-enroll.codenum = cl-member.codenum :
                DELETE cl-enroll.
            END.
        END.
    END.
END.

PROCEDURE delete-history.
    DEF BUFFER visit   FOR cl-histvisit.
    DEF BUFFER checkin FOR cl-checkin.
    DEF BUFFER clhist  FOR cl-histci.
    DEF VAR store-dur AS INTEGER INITIAL 360 NO-UNDO.
    FIND FIRST htparam WHERE paramnr = 1057 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN store-dur = htparam.finteger.

    FOR EACH cl-checkin WHERE (cl-checkin.datum - TODAY) GT store-dur 
        NO-LOCK:
        FIND FIRST checkin WHERE RECID(checkin) = RECID(cl-checkin)
            EXCLUSIVE-LOCK.
        DELETE checkin.
        RELEASE checkin.
    END.

    FOR EACH cl-histci WHERE (cl-histci.datum - TODAY) GT store-dur
        NO-LOCK:
        FIND FIRST clhist WHERE RECID(clhist) = RECID(cl-histci)
            EXCLUSIVE-LOCK.
        DELETE clhist.
        RELEASE clhist.
    END.

    FOR EACH cl-histvisit WHERE (cl-histvisit.datum - TODAY) GT 
        store-dur NO-LOCK:
        FIND FIRST visit WHERE RECID(visit) = RECID(cl-histvisit)
            EXCLUSIVE-LOCK.
        DELETE visit.
        RELEASE visit.
    END.

END.

    
