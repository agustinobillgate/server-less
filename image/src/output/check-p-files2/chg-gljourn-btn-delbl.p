DEF INPUT PARAMETER jnr         AS INT.
DEF INPUT PARAMETER rec-id      AS INT.
/*
/*naufal - add input param for logfile*/
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER fibukonto   LIKE gl-acct.fibukonto.
/*end*/
*/
DEF OUTPUT PARAMETER debits     LIKE gl-jouhdr.debit.
DEF OUTPUT PARAMETER credits    LIKE gl-jouhdr.credit.
DEF OUTPUT PARAMETER remains    LIKE gl-jouhdr.remain.
/*
/*naufal - add var for logfile*/
DEF VAR str         AS CHAR.
DEF VAR datum       LIKE gl-jouhdr.datum.
DEF VAR refno       LIKE gl-jouhdr.refno.
DEF VAR debit       LIKE gl-journal.debit.
DEF VAR credit      LIKE gl-journal.credit.
/*end*/
*/
FIND FIRST gl-journal WHERE RECID(gl-journal) = rec-id.
FIND FIRST gl-jouhdr  WHERE gl-jouhdr.jnr  = jnr EXCLUSIVE-LOCK.
/*
/*naufal - assign var for logfile*/
datum   = gl-jouhdr.datum.
refno   = gl-jouhdr.refno.
debit   = gl-journal.debit.   
credit  = gl-journal.credit.
/*end*/
*/
gl-jouhdr.debit = gl-jouhdr.debit - gl-journal.debit. 
gl-jouhdr.credit = gl-jouhdr.credit - gl-journal.credit. 
gl-jouhdr.remain =  gl-jouhdr.debit - gl-jouhdr.credit. 
FIND CURRENT gl-jouhdr NO-LOCK. 
debits  = gl-jouhdr.debit. 
credits = gl-jouhdr.credit. 
remains = gl-jouhdr.remain. 

FIND CURRENT gl-journal EXCLUSIVE-LOCK. 
delete gl-journal.
/*
/*naufal - str for logfile*/
str = "Delete Journal, Date: " + STRING(datum) + ", AcctNo: " + fibukonto + ", RefNo: " + refno.
IF debit NE 0 THEN
    str = str + ", Debit: " + STRING(debit).
ELSE
    str = str + ", Credit: " + STRING(credit). 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO:
    CREATE res-history.
    ASSIGN
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.aenderung   = str
        res-history.action      = "G/L".
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.
*/
