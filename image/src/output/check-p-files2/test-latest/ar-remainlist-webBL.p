
DEFINE TEMP-TABLE ar-remainderlist
    FIELD debtrecid     AS INTEGER 
    FIELD debt-day      AS INTEGER  
    FIELD descrip       AS CHARACTER
    FIELD bill-date     AS CHARACTER
    FIELD bill-no       AS CHARACTER
    FIELD bill-receive  AS CHARACTER
    FIELD debt-amount   AS CHARACTER
    FIELD paid-amount   AS CHARACTER
    FIELD oustanding    AS CHARACTER
    FIELD days          AS CHARACTER
    FIELD last-print    AS CHARACTER
    FIELD level         AS CHARACTER
    FIELD address1      AS CHARACTER
    FIELD address2      AS CHARACTER
    FIELD address3      AS CHARACTER
    FIELD contact       AS CHARACTER
    FIELD periode-stay  AS CHARACTER
    .

DEFINE INPUT PARAMETER  from-art    AS INTEGER.
DEFINE INPUT PARAMETER  to-art      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR ar-remainderlist.

DEFINE VARIABLE day1            AS INTEGER. 
DEFINE VARIABLE day2            AS INTEGER. 
DEFINE VARIABLE day3            AS INTEGER. 
 
DEFINE VARIABLE letter1         AS INTEGER. 
DEFINE VARIABLE letter2         AS INTEGER. 
DEFINE VARIABLE letter3         AS INTEGER. 
DEFINE VARIABLE price-decimal   AS INTEGER. 

FIND FIRST htparam WHERE paramnr = 330 NO-LOCK. 
day1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 331 NO-LOCK. 
day2 = htparam.finteger + day1. 
FIND FIRST htparam WHERE paramnr = 332 NO-LOCK. 
day3 = htparam.finteger + day2. 
 
FIND FIRST htparam WHERE paramnr = 670 NO-LOCK. 
letter1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 671 NO-LOCK. 
letter2 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 388 NO-LOCK. 
letter3 = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

RUN create-list.

PROCEDURE create-list:
    DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
    DEFINE VARIABLE t-debit     AS DECIMAL. 
    DEFINE VARIABLE tot-debit   AS DECIMAL. 
    DEFINE VARIABLE i           AS INTEGER. 
    DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
    DEFINE VARIABLE address1    AS CHAR FORMAT "x(32)".
    DEFINE VARIABLE address2    AS CHAR FORMAT "x(32)".
    DEFINE VARIABLE address3    AS CHAR FORMAT "x(32)".
    DEFINE VARIABLE contact     AS CHAR FORMAT "x(32)".    
    DEFINE VARIABLE debt-pay    AS DECIMAL. 
    DEFINE VARIABLE outstand    AS DECIMAL. 
    DEFINE VARIABLE debt-day    AS INTEGER. 
    DEFINE VARIABLE maildate    AS CHAR FORMAT "x(8)". 
    DEFINE VARIABLE periode_stay AS CHAR FORMAT "x(20)". 

    DEFINE BUFFER debtpay FOR debitor. 

    FOR EACH ar-remainderlist:
        DELETE ar-remainderlist.
    END.

    FOR EACH debitor WHERE debitor.zahlkonto EQ 0 AND debitor.opart EQ 0 
        AND debitor.artnr GE from-art AND debitor.artnr LE to-art NO-LOCK, 
        FIRST artikel WHERE artikel.artnr EQ debitor.artnr 
        AND artikel.artart EQ 2 AND artikel.departement EQ 0 NO-LOCK, 
        FIRST guest WHERE guest.gastnr EQ debitor.gastnr NO-LOCK
        BY artikel.artnr BY debitor.rgdatum BY debitor.name:

        FIND FIRST res-line WHERE res-line.gastnr EQ debitor.gastnr NO-LOCK NO-ERROR.  
        IF AVAILABLE res-line THEN periode_stay = STRING(res-line.ankunft) + " - " + STRING(res-line.abreise).

        FIND FIRST akt-kon WHERE akt-kon.gastnr EQ guest.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE akt-kon THEN contact = akt-kon.NAME.

        address1  = guest.adresse1.
        address2  = guest.adresse2.
        address3  = guest.adresse3.

        debt-day = today - debitor.rgdatum. 

        IF debt-day GT day1 THEN
        DO:
            receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1. 

            debt-pay = 0. 
            FOR EACH debtpay WHERE debtpay.rechnr EQ debitor.rechnr 
                AND debtpay.opart EQ 1 AND debtpay.counter EQ debitor.counter NO-LOCK: 
                debt-pay = debt-pay + debtpay.saldo. 
            END. 
            outstand = debitor.saldo + debt-pay. 
            
            maildate = "". 
            IF versanddat NE ? THEN maildate = STRING(versanddat). 

            CREATE ar-remainderlist.
            ASSIGN
                ar-remainderlist.debtrecid  = RECID(debitor) 
                ar-remainderlist.debt-day   = debt-day
                .
    
            IF price-decimal EQ 2 THEN
            DO:
                ASSIGN
                    ar-remainderlist.descrip      = artikel.bezeich
                    ar-remainderlist.bill-date    = STRING(debitor.rgdatum, "99/99/99")
                    ar-remainderlist.bill-no      = STRING(debitor.rechnr, ">>>>>>>>9")
                    ar-remainderlist.bill-receive = receiver
                    ar-remainderlist.debt-amount  = STRING(debitor.saldo, "->>,>>>,>>>,>>>,>>9.99") 
                    ar-remainderlist.paid-amount  = STRING(debt-pay, "->>,>>>,>>>,>>>,>>9.99") 
                    ar-remainderlist.oustanding   = STRING(outstand, "->>,>>>,>>>,>>>,>>9.99") 
                    ar-remainderlist.days         = STRING(debt-day, ">>>>9")
                    ar-remainderlist.last-print   = STRING(maildate, "99/99/99")
                    ar-remainderlist.level        = STRING(debitor.mahnstufe, ">>9")
                    ar-remainderlist.address1     = address1
                    ar-remainderlist.address2     = address2
                    ar-remainderlist.address3     = address3
                    ar-remainderlist.contact      = contact 
                    ar-remainderlist.periode-stay = periode_stay
                .
            END.
            ELSE
            DO:
                ASSIGN
                    ar-remainderlist.descrip      = artikel.bezeich
                    ar-remainderlist.bill-date    = STRING(debitor.rgdatum, "99/99/99")
                    ar-remainderlist.bill-no      = STRING(debitor.rechnr, ">>>>>>>>9")
                    ar-remainderlist.bill-receive = receiver
                    ar-remainderlist.debt-amount  = STRING(debitor.saldo, "->,>>>,>>>,>>>,>>>,>>9") 
                    ar-remainderlist.paid-amount  = STRING(debt-pay, "->,>>>,>>>,>>>,>>>,>>9") 
                    ar-remainderlist.oustanding   = STRING(outstand, "->,>>>,>>>,>>>,>>>,>>9") 
                    ar-remainderlist.days         = STRING(debt-day, ">>>>9")
                    ar-remainderlist.last-print   = STRING(maildate, "99/99/99")
                    ar-remainderlist.level        = STRING(debitor.mahnstufe, ">>9")
                    ar-remainderlist.address1     = address1
                    ar-remainderlist.address2     = address2
                    ar-remainderlist.address3     = address3
                    ar-remainderlist.contact      = contact 
                    ar-remainderlist.periode-stay = periode_stay
                .
            END.
        END.       
    END.
END PROCEDURE.
