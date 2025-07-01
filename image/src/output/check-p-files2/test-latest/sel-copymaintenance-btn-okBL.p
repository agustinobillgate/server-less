
DEFINE TEMP-TABLE property
    FIELD prop-nr       AS INTEGER
    FIELD prop-nm       AS CHAR     FORMAT "x(30)"
    FIELD prop-loc      AS INTEGER
    FIELD prop-loc-nm   AS CHAR     FORMAT "x(30)"
    FIELD prop-zinr     AS CHAR
    FIELD prop-Selected AS LOGICAL INITIAL NO
    FIELD str           AS CHAR     FORMAT "x(1)" INITIAL "".

DEF INPUT PARAMETER TABLE FOR property.
DEF INPUT PARAMETER maintain-nr AS INT.
DEF INPUT PARAMETER all-main    AS LOGICAL.
DEF INPUT PARAMETER all-only    AS LOGICAL.
DEF INPUT PARAMETER fdate       AS DATE.
DEF INPUT PARAMETER tdate       AS DATE.
DEF INPUT PARAMETER stnumber    AS INT.
DEF INPUT PARAMETER lsNumber    AS INT.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT-OUTPUT PARAMETER blCpy AS INT.
DEF INPUT-OUTPUT PARAMETER lsNo  AS INT.
DEF INPUT-OUTPUT PARAMETER stNo  AS INT.

DEF VAR blcopy AS CHAR NO-UNDO.

DEF VAR YEAR         AS INT NO-UNDO.
DEF VAR MONTH        AS INT NO-UNDO.
DEF VAR week         AS INT NO-UNDO.
DEF VAR maintask     AS INT NO-UNDO.
DEF VAR TYPE         AS INT NO-UNDO.
DEF VAR propertynr   AS INT NO-UNDO.
DEF VAR workdate     AS DATE.
DEF VAR comments     AS CHAR NO-UNDO.
DEF VAR created-by   AS CHAR NO-UNDO.
DEF VAR created-date AS DATE.
DEF VAR estworkdate  AS DATE.
DEF VAR typework     AS INT NO-UNDO.     
DEF VAR nr           AS INTEGER NO-UNDO.

DEF VAR stLocation AS INTEGER.
DEF VAR stZinr     AS CHAR.

DEF VAR a AS DATE.
DEF VAR b AS DATE.

DEF BUFFER qbuff FOR eg-mdetail.

FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = maintain-nr NO-LOCK NO-ERROR.
IF AVAILABLE eg-maintain THEN
DO:
    blcopy = "1".
    ASSIGN
      TYPE =  eg-maintain.TYPE
      propertynr =  eg-maintain.propertynr 
      comments  =  eg-maintain.comments
      created-by =  eg-maintain.created-by
      created-date = TODAY
      estworkdate =  eg-maintain.estworkdate
      typework =  eg-maintain.typework.
END.
ELSE blcopy = "0".

IF all-main THEN
DO:
    FOR EACH property :
        property.prop-selected = YES.
    END.
END.

IF blcopy = "1" THEN
DO:
    ASSIGN a = fdate.

    IF all-only THEN
    DO:
        DO WHILE a <= tdate:
            FIND FIRST eg-maintain WHERE eg-maintain.propertynr = propertynr AND eg-maintain.estworkdate = a NO-LOCK NO-ERROR.
            IF AVAILABLE eg-maintain THEN
            DO:
            END.
            ELSE
            DO:
                FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
                IF NOT AVAILABLE counters THEN
                DO:
                    CREATE counters.
                    ASSIGN counters.counter-no = 38
                        counters.counter-bez = "Counter for maintenance in engineering"
                        counters.counter = 0.
                END.
                counters.counter = counters.counter + 1.

                FIND CURRENT counters NO-LOCK.

                nr = counters.counter.

                IF stnumber = 0 THEN stNumber = nr.

                IF lsNumber = 0 THEN lsNumber = nr.
                ELSE 
                DO:
                    IF lsNumber < nr THEN lsnumber = nr.
                END.

                FIND FIRST eg-property WHERE eg-property.nr = propertynr NO-LOCK NO-ERROR.
                IF AVAILABLE eg-property THEN
                DO:
                    stLocation = eg-property.location.
                    stZinr     = eg-property.zinr.
                END.
                ELSE
                DO:
                    stLocation = 0.
                    stZinr = "".
                END.

                CREATE eg-maintain.
                ASSIGN
                      eg-maintain.maintainnr = nr
                      eg-maintain.TYPE = 1 /*TYPE*/
                      eg-maintain.propertynr = propertynr  
                      eg-maintain.location  = stLocation
                      eg-maintain.zinr = stZinr
                      eg-maintain.comments = comments  
                      eg-maintain.created-by = user-init 
                      eg-maintain.created-date = TODAY 
                      eg-maintain.estworkdate = a 
                      eg-maintain.typework = typework.


                FIND FIRST eg-mdetail WHERE eg-mdetail.maintainnr =  maintain-nr NO-LOCK NO-ERROR.
                IF AVAILABLE eg-mdetail THEN
                DO:
                    FOR EACH qbuff WHERE qbuff.maintainnr = maintain-nr NO-LOCK :
                        CREATE eg-mdetail.
                        ASSIGN
                            eg-mdetail.KEY = qbuff.KEY
                            eg-mdetail.maintainnr = nr
                            eg-mdetail.nr = qbuff.nr
                            eg-mdetail.bezeich = qbuff.bezeich
                            eg-mdetail.TYPE = qbuff.TYPE
                            eg-mdetail.create-date = TODAY
                            eg-mdetail.create-time = TIME
                            eg-mdetail.create-by   = user-init.
                    END.
                END.
            END.
            
            IF typework = 1 THEN
                a = a + 1.
            ELSE IF typework = 2 THEN
                a = a + 7.
            ELSE IF typework = 3 THEN
                a = a + 30.            
            ELSE IF typework = 4 THEN
                a = a + 90.
            ELSE IF typework = 5 THEN
                a = a + 180.
            ELSE IF typework = 6 THEN
                a = a + 365.
        END.

        ASSIGN a = fdate.
    END.

    DO WHILE a <= tdate :
        FOR EACH property WHERE property.prop-selected NO-LOCK:
            FIND FIRST eg-maintain WHERE eg-maintain.propertynr = property.prop-nr AND eg-maintain.estworkdate = a NO-LOCK NO-ERROR.
            IF AVAILABLE eg-maintain THEN
            DO:
            END.
            ELSE
            DO:
                FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
                IF NOT AVAILABLE counters THEN
                DO:
                    CREATE counters.
                    ASSIGN counters.counter-no = 38
                        counters.counter-bez = "Counter for maintenance in engineering"
                        counters.counter = 0.
                END.
                counters.counter = counters.counter + 1.

                FIND CURRENT counters NO-LOCK.

                nr = counters.counter.

                IF stnumber = 0 THEN stNumber = nr.

                IF lsNumber = 0 THEN lsNumber = nr.
                ELSE
                DO:
                    IF lsNumber < nr THEN lsnumber = nr.
                END.

                CREATE eg-maintain.

                FIND FIRST eg-property WHERE eg-property.nr = property.prop-nr NO-LOCK NO-ERROR.
                IF AVAILABLE eg-property THEN
                DO:
                    stLocation = eg-property.location.
                    stZinr     = eg-property.zinr.
                END.
                ELSE
                DO:
                    stLocation = 0.
                    stZinr = "".
                END.

                ASSIGN
                      eg-maintain.maintainnr = nr
                      eg-maintain.TYPE = 1 /*TYPE*/
                      eg-maintain.propertynr = property.prop-nr  
                      eg-maintain.location  = stLocation
                      eg-maintain.zinr = stZinr
                      eg-maintain.comments = comments  
                      eg-maintain.created-by = user-init 
                      eg-maintain.created-date = TODAY 
                      eg-maintain.estworkdate = a 
                      eg-maintain.typework = typework.


                FIND FIRST eg-mdetail WHERE eg-mdetail.maintainnr =  maintain-nr NO-LOCK NO-ERROR.
                IF AVAILABLE eg-mdetail THEN
                DO:
                    FOR EACH qbuff WHERE qbuff.maintainnr = maintain-nr NO-LOCK :
                        CREATE eg-mdetail.
                        ASSIGN
                            eg-mdetail.KEY = qbuff.KEY
                            eg-mdetail.maintainnr = nr
                            eg-mdetail.nr = qbuff.nr
                            eg-mdetail.bezeich = qbuff.bezeich
                            eg-mdetail.TYPE = qbuff.TYPE
                            eg-mdetail.create-date = TODAY
                            eg-mdetail.create-time = TIME
                            eg-mdetail.create-by   = user-init.
                    END.
                END.
                    
            END.
        END.
            
        IF typework = 1 THEN
            a = a + 1.
        ELSE IF typework = 2 THEN
            a = a + 7.
        ELSE IF typework = 3 THEN
            a = a + 30.            
        ELSE IF typework = 4 THEN
            a = a + 90.
        ELSE IF typework = 5 THEN
            a = a + 180.
        ELSE IF typework = 6 THEN
            a = a + 365.
    END.
END.

IF lsnumber = 0 AND stnumber = 0 THEN
DO:
    ASSIGN blCpy   = 0
           lsNo = lsNumber
           stNo = stNumber.
END.
ELSE
DO:
    ASSIGN blCpy   = 1
           lsNo = lsNumber
           stNo = stNumber.
END.
