
DEFINE TEMP-TABLE coa-list LIKE gl-acct.

DEF OUTPUT PARAMETER max-row AS INTEGER  NO-UNDO INITIAL 2.
DEF OUTPUT PARAMETER TABLE FOR coa-list.

RUN create-list.
FOR EACH gl-acct NO-LOCK:
    max-row = max-row + 1.
END.

PROCEDURE create-list:
    FOR EACH coa-list:
        DELETE coa-list.
    END.

    FOR EACH gl-acct WHERE gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 4 
        NO-LOCK BY gl-acct.fibukonto:
        CREATE coa-list.
        BUFFER-COPY gl-acct TO coa-list.
    END.
END.
