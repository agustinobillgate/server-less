DEFINE TEMP-TABLE op-list LIKE fa-op
    FIELD Arive-Amount   AS DECIMAL 
    FIELD Sorting        AS CHAR FORMAT "x(2)" INITIAL "" .

DEFINE TEMP-TABLE fa-ordheaderlist LIKE fa-ordheader
    FIELD create-name    AS CHAR  FORMAT "x(30)"
    FIELD modify-name    AS CHAR  FORMAT "x(30)"
    FIELD total-amount1  AS DECIMAL  FORMAT "->,>>>,>>>,>>>,>>9.99" .

DEF OUTPUT PARAMETER TABLE FOR op-list.
DEF OUTPUT PARAMETER TABLE FOR fa-ordheaderlist.

RUN Distinct-op.
RUN create-faOrdHeaderlist.


PROCEDURE Distinct-OP :
    DEFINE VARIABLE temp-Number         AS CHAR.

    FOR EACH op-list :
        DELETE op-list.
    END.

    /*FOR EACH fa-op NO-LOCK BY fa-op.docu-nr BY fa-op.lscheinnr BY fa-op.zeit :*/
    FOR EACH fa-op WHERE fa-op.loeschflag <= 1 AND 
        fa-op.warenwert > 0 NO-LOCK BY fa-op.docu-nr BY fa-op.lscheinnr BY fa-op.zeit :
        IF temp-Number = "" THEN
        DO:
            temp-number = fa-op.lscheinnr.

            CREATE op-list.
            BUFFER-COPY fa-op TO op-list.
        END.
        ELSE
        DO:
            IF temp-number NE fa-op.lscheinnr THEN
            DO:
                temp-number = fa-op.lscheinnr.
                
                CREATE op-list.
                BUFFER-COPY fa-op TO op-list.      
            END.
        END.

    END.
    
END PROCEDURE.

PROCEDURE create-faOrdHeaderlist :
    DEF VAR temp-create AS CHAR FORMAT "x(30)".
    DEF VAR temp-modify AS CHAR FORMAT "x(30)".
    DEF VAR total-amount  AS DECIMAL INITIAL 0.

    FOR EACH fa-ordheaderlist :
        DELETE fa-ordheaderlist.
    END.

    FOR EACH fa-ordheader NO-LOCK USE-INDEX datumactive :

        IF fa-ordheader.created-by NE "" THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.created-by NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN temp-create = bediener.username.
            ELSE temp-create = "".
        END.
        ELSE
        DO:
            temp-create = "".
        END.

        IF fa-ordheader.modified-by NE "" THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.modified-by NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN temp-modify = bediener.username.
            ELSE temp-modify = "".
        END.
        ELSE
        DO:
            temp-modify = "".
        END.
        
        FOR EACH fa-order WHERE fa-order.order-nr  = fa-ordheader.order-nr NO-LOCK:
            total-amount = total-amount + fa-order.order-amount.    
        END.

        CREATE fa-ordheaderlist.
        BUFFER-COPY fa-ordheader TO fa-ordheaderlist.
        ASSIGN fa-ordheaderlist.create-name = temp-create
               fa-ordheaderlist.modify-name = temp-modify
               fa-ordheaderlist.total-amount1 = total-amount.

        temp-create     = "".
        temp-modify     = "".
        total-amount    = 0.
    END.


END PROCEDURE.
