DEFINE TEMP-TABLE bline-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD userinit AS CHARACTER
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD name AS CHARACTER
  FIELD bl-recid AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE cash-art
    FIELD pos-nr        AS INTEGER
    FIELD artnr         AS INTEGER
    FIELD bezeich       AS CHARACTER
    FIELD amount        AS DECIMAL FORMAT "->>,>>>,>>9.99"
    FIELD tamount       AS DECIMAL FORMAT "->>,>>>,>>9.99".

DEFINE TEMP-TABLE summary1
    FIELD usrinit       AS CHARACTER
    FIELD username      AS CHARACTER
    FIELD artnr         AS INTEGER
    FIELD amount        AS DECIMAL FORMAT "->>,>>>,>>9.99".

DEFINE TEMP-TABLE summary-list
    FIELD username AS CHAR
    FIELD price AS DECIMAL EXTENT 20
    FIELD total-price AS DECIMAL.

DEF INPUT  PARAMETER TABLE FOR bline-list.
DEF INPUT  PARAMETER TABLE FOR summary1.
DEF INPUT  PARAMETER TABLE FOR cash-art.
DEF OUTPUT PARAMETER label-list AS CHARACTER EXTENT 20.
DEF OUTPUT PARAMETER TABLE FOR summary-list.

DEFINE BUFFER cbuff  FOR cash-art.
DEFINE VARIABLE i AS INTEGER. 

RUN daysale-list.

PROCEDURE daysale-list:
    DEF VAR str1 AS CHAR.
    DEF VAR ttl AS DECIMAL FORMAT "->>>,>>>,>>9.99".
    DEF VAR gttl AS DECIMAL FORMAT "->>>,>>>,>>9.99".

    DEF VAR counter AS INT INIT 0.

    FIND FIRST summary1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE summary1 THEN
        RETURN.

    FOR EACH cash-art BY cash-art.pos-nr:
        counter = counter + 1.
        label-list[counter] = cash-art.bezeich.
    END.    
    
    FOR EACH bline-list WHERE bline-list.SELECTED = YES BY bline-list.NAME:
        FOR EACH cash-art:
            cash-art.amount = 0.
        END.
        FOR EACH cash-art BY pos-nr:
            FIND FIRST summary1 WHERE summary1.artnr = cash-art.artnr
                AND summary1.usrinit = bline-list.userinit NO-LOCK NO-ERROR.
            IF AVAILABLE summary1 THEN
            DO:
                FIND FIRST cbuff WHERE RECID(cbuff) = RECID(cash-art).
                ASSIGN cbuff.amount = summary1.amount
                    cbuff.tamount = cbuff.tamount + summary1.amount.
            END.  
        END. /*each cash-art*/
        FIND FIRST cbuff WHERE cbuff.amount NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE cbuff THEN
        DO:
            CREATE summary-list.
            summary-list.username = bline-list.NAME.
            ttl = 0.
            counter = 0.
            FOR EACH cash-art BY cash-art.pos-nr:
                counter = counter + 1.
                summary-list.price[counter] = cash-art.amount.
                ttl = ttl + cash-art.amount.
                gttl = gttl + cash-art.amount.
            END.
            summary-list.total-price = ttl.
        END.
    END. /*each bline-list*/
    
    CREATE summary-list.
    
    CREATE summary-list.
    ASSIGN summary-list.username = "G-TOTAL".
    counter = 0.
    FOR EACH cash-art BY cash-art.pos-nr:
        counter = counter + 1.
        summary-list.price[counter] = cash-art.tamount.
    END.    
    summary-list.total-price = gttl.
END.
