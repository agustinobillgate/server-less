
DEFINE TEMP-TABLE coa-list LIKE gl-acct.

DEF INPUT PARAMETER TABLE FOR coa-list.
DEF INPUT PARAMETER sorttype AS INT.

RUN update-budget.

PROCEDURE update-budget:
    DEF BUFFER cbuff FOR coa-list.
    FOR EACH cbuff NO-LOCK:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = cbuff.fibukonto 
            NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            FIND CURRENT gl-acct EXCLUSIVE-LOCK.
            IF sorttype = 1 THEN
            DO:
                ASSIGN
                    gl-acct.budget[1] = cbuff.budget[1]
                    gl-acct.budget[2] = cbuff.budget[2]
                    gl-acct.budget[3] = cbuff.budget[3]
                    gl-acct.budget[4] = cbuff.budget[4]
                    gl-acct.budget[5] = cbuff.budget[5]
                    gl-acct.budget[6] = cbuff.budget[6]
                    gl-acct.budget[7] = cbuff.budget[7]
                    gl-acct.budget[8] = cbuff.budget[8]
                    gl-acct.budget[9] = cbuff.budget[9]
                    gl-acct.budget[10] = cbuff.budget[10]
                    gl-acct.budget[11] = cbuff.budget[11]
                    gl-acct.budget[12] = cbuff.budget[12].
            END.
            ELSE
            DO:
                ASSIGN
                    gl-acct.debit[1] = cbuff.debit[1]
                    gl-acct.debit[2] = cbuff.debit[2]
                    gl-acct.debit[3] = cbuff.debit[3]
                    gl-acct.debit[4] = cbuff.debit[4]
                    gl-acct.debit[5] = cbuff.debit[5]
                    gl-acct.debit[6] = cbuff.debit[6]
                    gl-acct.debit[7] = cbuff.debit[7]
                    gl-acct.debit[8] = cbuff.debit[8]
                    gl-acct.debit[9] = cbuff.debit[9]
                    gl-acct.debit[10] = cbuff.debit[10]
                    gl-acct.debit[11] = cbuff.debit[11]
                    gl-acct.debit[12] = cbuff.debit[12].

            END.
            FIND CURRENT gl-acct NO-LOCK.
        END.
    END.
END.
