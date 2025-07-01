
/* count-expired.p */


DEF INPUT PARAMETER  code-num AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER exp-date  AS DATE   NO-UNDO.
DEF VAR  memtype  AS INTEGER             NO-UNDO.
DEF VAR  fdate    AS DATE                NO-UNDO.
DEF VAR  dauer    AS INTEGER             NO-UNDO.

DEF VAR i  AS INTEGER NO-UNDO.
DEF VAR dd AS INTEGER NO-UNDO.
DEF VAR mm AS INTEGER NO-UNDO.
DEF VAR yy AS INTEGER NO-UNDO.
DEF VAR total-days AS INTEGER  NO-UNDO INITIAL 0.
DEF VAR count-month AS INTEGER NO-UNDO INITIAL 0.
DEF VAR curr-month AS INTEGER  NO-UNDO INITIAL 0.
DEF BUFFER tbuff FOR cl-memtype.
DEF VAR sum-day AS INTEGER EXTENT 12.

DO:
    FIND FIRST cl-member WHERE cl-member.codenum = code-num NO-LOCK.
    IF cl-member.memstatus = 0 THEN
    DO:
      exp-date = cl-member.expired-date.
      RETURN.
    END.
    
    FIND FIRST mc-fee WHERE mc-fee.KEY = 2
        AND mc-fee.nr = cl-member.membertype
        AND mc-fee.gastnr = cl-member.gastnr
        AND mc-fee.activeflag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE mc-fee THEN
    DO:
        exp-date = mc-fee.bis-datum.
        RETURN.
    END.

    ASSIGN
        memtype = cl-member.membertype
        fdate   = cl-member.expired-date
        dauer   = cl-member.num1
    .
    sum-day[1] = 31.
    IF (YEAR(fdate) MODULO 4) = 0 THEN
        sum-day[2] = 29.
    ELSE sum-day[2] = 28.
    sum-day[3] = 31.
    sum-day[4] = 30.
    sum-day[5] = 31.
    sum-day[6] = 30.
    sum-day[7] = 31.
    sum-day[8] = 31.
    sum-day[9] = 30.
    sum-day[10] = 31.
    sum-day[11] = 30.
    sum-day[12] = 31.

    FIND FIRST tbuff WHERE tbuff.nr = memtype NO-LOCK NO-ERROR.
    IF AVAILABLE tbuff THEN
    DO:
        IF dauer = 0 THEN dauer = tbuff.dauer.
        dd = DAY(fdate).
        mm = MONTH(fdate).
        yy = YEAR(fdate).
        total-days = sum-day[mm] - dd.
        count-month = 1.
        curr-month = mm + 1.
        IF curr-month = 13 THEN curr-month = 1.
        REPEAT:
            IF count-month = dauer THEN LEAVE.
            total-days = total-days + sum-day[curr-month].
            count-month = count-month + 1.
            curr-month = curr-month + 1.
            IF curr-month = 13 THEN curr-month = 1.
            IF curr-month = 0 THEN curr-month = 12.
        END.
        exp-date = fdate + total-days + dd - 1.
    END.
END.


