
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER depttype AS INT.

RUN transfer-journals.
RUN checked-journals. /*ITA 210425 -> pengecheckan batch jurnal untuk issue data tersangkut*/

PROCEDURE transfer-journals:
DEFINE BUFFER gl-jouhdr1 FOR gl-jouhdr. 
DEFINE BUFFER gl-jouhdr2 FOR gl-jouhdr.

DEFINE BUFFER bjouhdr FOR gl-jouhdr.
DEFINE VARIABLE date1 AS DATE. 
DEFINE VARIABLE date2 AS DATE. 

    FIND FIRST htparam WHERE htparam.paramnr = 558 NO-LOCK.    /* LAST Accounting Period */ 
    date1 = htparam.fdate + 1. 
    FIND FIRST htparam WHERE htparam.paramnr = 597 NO-LOCK.   /* journal closing DATE */ 
    date2 = htparam.fdate. 
    
    IF from-date GT date1 THEN date1 = from-date. 
    IF to-date LT date2 THEN date2 = to-date.
    
    FOR EACH gl-jouhdr1 WHERE gl-jouhdr1.activeflag = 0 
        AND gl-jouhdr1.datum GE date1 AND gl-jouhdr1.datum LE date2 
        AND gl-jouhdr1.jtype = depttype AND gl-jouhdr1.batch = YES NO-LOCK: 

        FIND FIRST bjouhdr WHERE RECID(bjouhdr) = RECID(gl-jouhdr1) EXCLUSIVE-LOCK.
        bjouhdr.batch = NO. 
        FIND CURRENT bjouhdr NO-LOCK.
        RELEASE bjouhdr.
    END. 
    
    /*FDL Nov 22, 2024 => Ticket C28693*/
    FOR EACH gl-jouhdr2 WHERE gl-jouhdr2.activeflag EQ 0 
        AND gl-jouhdr2.datum GE date1 AND gl-jouhdr2.datum LE date2 
        AND gl-jouhdr2.jtype EQ 0 AND gl-jouhdr2.batch EQ YES NO-LOCK:

        FIND FIRST bjouhdr WHERE RECID(bjouhdr) = RECID(gl-jouhdr2) EXCLUSIVE-LOCK.
        bjouhdr.batch = NO. 
        FIND CURRENT bjouhdr NO-LOCK.
        RELEASE bjouhdr.
    END.
END. 


PROCEDURE checked-journals:
DEFINE BUFFER gl-jouhdr3 FOR gl-jouhdr. 
DEFINE BUFFER gl-jouhdr4 FOR gl-jouhdr.

DEFINE BUFFER bjouhdr FOR gl-jouhdr.
DEFINE VARIABLE date3 AS DATE. 
DEFINE VARIABLE date4 AS DATE. 

    FIND FIRST htparam WHERE htparam.paramnr = 558 NO-LOCK.    /* LAST Accounting Period */ 
    date3 = htparam.fdate + 1. 
    FIND FIRST htparam WHERE htparam.paramnr = 597 NO-LOCK.   /* journal closing DATE */ 
    date4 = htparam.fdate. 
    
    IF from-date GT date3 THEN date3 = from-date. 
    IF to-date LT date4 THEN date4 = to-date.
    
    FOR EACH gl-jouhdr3 WHERE gl-jouhdr3.activeflag = 0 
        AND gl-jouhdr3.datum GE date3 AND gl-jouhdr3.datum LE date4 
        AND gl-jouhdr3.jtype = depttype AND gl-jouhdr3.batch = YES NO-LOCK: 

        FIND FIRST bjouhdr WHERE RECID(bjouhdr) = RECID(gl-jouhdr3) EXCLUSIVE-LOCK.
        bjouhdr.batch = NO. 
        FIND CURRENT bjouhdr NO-LOCK.
        RELEASE bjouhdr.
    END. 
    
    /*FDL Nov 22, 2024 => Ticket C28693*/
    FOR EACH gl-jouhdr4 WHERE gl-jouhdr4.activeflag EQ 0 
        AND gl-jouhdr4.datum GE date3 AND gl-jouhdr4.datum LE date4 
        AND gl-jouhdr4.jtype EQ 0 AND gl-jouhdr4.batch EQ YES NO-LOCK:

        FIND FIRST bjouhdr WHERE RECID(bjouhdr) = RECID(gl-jouhdr4) EXCLUSIVE-LOCK.
        bjouhdr.batch = NO. 
        FIND CURRENT bjouhdr NO-LOCK.
        RELEASE bjouhdr.
    END.
END. 
