DEFINE TEMP-TABLE sVendor
    FIELD nr           AS CHAR FORMAT "x(2)"
    FIELD vendor-nr    AS INTEGER
    FIELD docno         AS CHAR
    FIELD reqnr       AS INTEGER
    FIELD startdate   AS DATE
    FIELD estfinishdate  AS DATE
    FIELD finishdate    AS DATE
    FIELD price         AS DECIMAL FORMAT "->>,>>>,>>>,>>9"  
    FIELD bezeich       AS CHAR     FORMAT "x(30)"
    FIELD pic           AS CHAR     FORMAT "x(30)"
    FIELD created-by    AS CHAR
    FIELD created-date   AS DATE
    FIELD created-time   AS INTEGER
    FIELD perform-nr     AS CHAR
    FIELD stat           AS CHAR.

DEFINE TEMP-TABLE attchment 
    FIELD nr        AS INTEGER  FORMAT ">>>"   COLUMN-LABEL "No"
    FIELD att-file  AS CHAR     COLUMN-LABEL "Attachment File"
    FIELD bezeich   AS CHAR     COLUMN-LABEL "Description".

DEFINE TEMP-TABLE stock
    FIELD nr          AS INTEGER  FORMAT ">>9"         COLUMN-LABEL "No"
    FIELD stock-nr    AS INTEGER  FORMAT ">>>>>>>"     COLUMN-LABEL "ArticleNo"
    FIELD stock-nm    AS CHAR     FORMAT "x(30)"       COLUMN-LABEL "Article Name"
    /*FIELD stock-qty   AS INTEGER  FORMAT ">>>"         COLUMN-LABEL "Qty"*/
    FIELD stock-qty   AS DECIMAL  FORMAT ">>>9.99"          COLUMN-LABEL "Qty"
    FIELD stock-price AS INTEGER  FORMAT "->>,>>9.999" COLUMN-LABEL "Price"
    FIELD stock-total AS INTEGER  FORMAT ">>,>>>,>>9.999" COLUMN-LABEL "Total"  .

DEFINE TEMP-TABLE request1 LIKE eg-request.

DEFINE TEMP-TABLE treqdetail
    FIELD reqnr AS INTEGER
    FIELD actionnr AS INTEGER
    FIELD action AS CHAR FORMAT "x(256)"
    FIELD create-date AS DATE
    FIELD create-time AS INTEGER
    FIELD create-str  AS CHAR
    FIELD create-by AS CHAR
    FIELD flag AS LOGICAL.


DEF INPUT PARAMETER TABLE FOR treqdetail.
DEF INPUT-OUTPUT PARAMETER TABLE FOR request1.
DEF INPUT PARAMETER TABLE FOR stock.
DEF INPUT PARAMETER TABLE FOR attchment.
DEF INPUT PARAMETER TABLE FOR sVendor.
DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER sub-str AS CHAR.
DEF INPUT PARAMETER solution AS CHAR.
DEF INPUT PARAMETER estfin-str AS CHAR.
DEF INPUT PARAMETER a AS INT.
DEF INPUT PARAMETER blout AS INT.
DEF INPUT PARAMETER reqno AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER prop-bezeich AS CHAR.
DEF INPUT PARAMETER sguestflag AS LOGICAL.

DEF OUTPUT PARAMETER blrange AS INT INIT 0.
DEF OUTPUT PARAMETER avail-eg-staff AS LOGICAL INIT NO.

DEF BUFFER usr   FOR bediener.
DEF VAR usrnr    AS INTEGER INITIAL 0  NO-UNDO.
DEF VAR char1 AS CHAR NO-UNDO.

DEF BUFFER buff-property FOR eg-property.
DEF VARIABLE prop-nr AS INTEGER INIT 0.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "eg-chgreq". 
DEFINE VARIABLE urgstr      AS CHAR     EXTENT 10 FORMAT "x(10)" NO-UNDO.
urgstr[1]  = translateExtended("Low", lvCAREA, "").
urgstr[2]  = translateExtended("Medium", lvCAREA, "").
urgstr[3]  = translateExtended("High", lvCAREA, "").

DEFINE VARIABLE statstr     AS CHAR     EXTENT 5  FORMAT "x(16)" NO-UNDO.
statstr[1] = translateExtended("New", lvCAREA, "").
statstr[2] = translateExtended("Processed", lvCAREA, "").
statstr[3] = translateExtended("Done", lvCAREA, "").
statstr[4] = translateExtended("Postponed", lvCAREA, "").
statstr[5] = translateExtended("Closed", lvCAREA, "").

FIND FIRST request1.
DO TRANSACTION:
    IF request1.propertynr = 0 THEN
    DO:
        FOR EACH buff-property NO-LOCK BY buff-property.nr DESC:
            prop-nr = buff-property.nr.
            LEAVE.
        END.
        prop-nr = prop-nr + 1.
            
        CREATE eg-property.
        ASSIGN
            eg-property.nr          = prop-nr
            eg-property.bezeich     = prop-bezeich
            eg-property.maintask    = request1.maintask                    
            eg-property.zinr        = request1.zinr   
            eg-property.datum       = TODAY
       .
       IF sguestflag EQ YES THEN
       DO:
          FIND FIRST eg-location WHERE eg-location.guestflag = YES NO-LOCK NO-ERROR.
          IF AVAILABLE eg-location THEN eg-property.location = eg-location.nr. 
       END.                                  
       ELSE eg-property.location = request1.reserve-int.   
       request1.propertynr = prop-nr.
    END.
    RUN create-log.
    RUN execute-it.

    FOR EACH treqdetail WHERE treqdetail.flag = NO AND treqdetail.action NE "" NO-LOCK:
        CREATE eg-reqdetail.
        ASSIGN eg-reqdetail.reqnr = treqdetail.reqnr
                eg-reqdetail.actionnr = treqdetail.actionnr
                eg-reqdetail.action   = treqdetail.action
                eg-reqdetail.create-date = treqdetail.create-date        
                eg-reqdetail.create-time = treqdetail.create-time
                eg-reqdetail.create-by = treqdetail.create-by.
    END.

    FOR EACH eg-reqdetail :
        IF eg-reqdetail.actionnr = 0 THEN
        DO:
            FIND FIRST treqdetail WHERE treqdetail.action = eg-reqdetail.action NO-LOCK NO-ERROR.
            IF NOT AVAILABLE treqdetail THEN
            DO:
                DELETE eg-reqdetail.
            END.
        END.
        ELSE
        DO:
            FIND FIRST treqdetail WHERE treqdetail.actionnr = eg-reqdetail.actionnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE treqdetail THEN
            DO:
                DELETE eg-reqdetail.
            END.
        END.
    END.
    
    IF blout = 2 THEN
    DO:
        FIND FIRST usr WHERE usr.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE usr THEN usrnr = usr.nr.

        FIND FIRST eg-vperform WHERE eg-vperform.reqnr = reqno NO-ERROR.
        IF AVAILABLE eg-vperform THEN
        DO:

        char1 = STRING(eg-vperform.reqnr,"->,>>>,>>9") + ";" + 
                string(eg-vperform.created-by) + ";" +
                string(eg-vperform.created-date, "99/99/99") + ";" + 
                string(eg-vperform.created-time, "->,>>>,>>9") + ";" + 
                string(eg-vperform.vendor-nr,"->,>>>,>>9") + ";" + 
                string(eg-vperform.startdate, "99/99/99") + ";" + 
                string(eg-vperform.estfinishdate, "99/99/99") + ";" + 
                string(eg-vperform.finishdate, "99/99/99") + ";" + 
                string(eg-vperform.price, "->>,>>>,>>>,>>9.99") + ";" + 
                eg-vperform.bezeich + ";" + 
                eg-vperform.pic.
            
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering Vendor Perform"
                res-history.aenderung   = "Delete outsource ReqNo " + STRING(reqNo)
                    + ": " + char1 .

            ASSIGN eg-vperform.logi1 = YES.
            /*MTAPPLY "CHOOSE" TO btn-exit3 IN FRAME frame3.*/
        END.

    END.
    
    RUN save-vendor.
    /*MT
    blout = 0.
    statvendor = 0.
    solution = "".
    RUN create-request.
    RUN create-combo.
    RUN save-vendor.

    RUN disp-all.
    APPLY "entry" TO request1.reqnr.
    RUN mkreadonly(YES).
    curr-select = "".
    IF blRange = 1 THEN
    DO:
        RUN create-frame4(1) .
    END.

    ENABLE /*btn-chg*/ btn-print WITH FRAME frame1.

    FIND FIRST eg-staff WHERE eg-staff.nr = request1.assign-to AND eg-staff.mobile NE "" NO-LOCK NO-ERROR.
    IF AVAILABLE eg-staff THEN
    DO:
        ENABLE btn-sendsms WITH FRAME frame1.
    END.
    ELSE
    DO:
        DISABLE btn-sendsms WITH FRAME frame1.
    END.

    RUN Define-sms.
    DISABLE ALL EXCEPT btn-stop btn-print btn-alert btn-sendsms btn-look WITH FRAME frame1.
    IF request1.reqstatus = 1 THEN
    DO:
        DISABLE btn-print WITH FRAME frame1.
    END.

    DISABLE /*btn-outsource*/ btn-go btn-help WITH FRAME frame1.
    FIND CURRENT rbuff NO-LOCK.
    */
    FIND FIRST eg-staff WHERE eg-staff.nr = request1.assign-to AND eg-staff.mobile NE "" NO-LOCK NO-ERROR.
    IF AVAILABLE eg-staff THEN avail-eg-staff = YES.
END.


PROCEDURE create-log:
    DEF BUFFER usr   FOR bediener.
    DEF VAR usrnr    AS INTEGER INITIAL 0  NO-UNDO.
    DEF VAR char1    AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR char2    AS CHAR    INITIAL "" NO-UNDO.
    
    DEF VAR hour    AS INTEGER NO-UNDO.
    DEF VAR minute  AS INTEGER NO-UNDO.
    DEF VAR timeest AS INTEGER NO-UNDO.

    FIND FIRST usr WHERE usr.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN usrnr = usr.nr.


    FIND FIRST eg-request WHERE eg-request.reqnr = reqNo NO-LOCK NO-ERROR.
    IF AVAILABLE eg-request THEN
    DO:
        IF eg-request.reqstatus NE request1.reqstatus THEN
        DO:
            IF eg-request.reqstatus =  3 AND  request1.reqstatus = 2 THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Change Status ReqNo " + STRING(reqno)
                        + ": " + statstr[eg-request.reqstatus] + " To " + statstr[request1.reqstatus]
                        + " record status done by : " + eg-request.done-by + " date : " + STRING(eg-request.done-date, "99/99/99") +
                        " time : "+ STRING(eg-request.done-time, "->,>>>,>>9") .
                    
            END.
            ELSE
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Change Status ReqNo " + STRING(reqno)
                        + ": " + statstr[eg-request.reqstatus] + " To " + statstr[request1.reqstatus]
                    .
            END.
        END.

        IF eg-request.SOURCE NE request1.SOURCE THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 130 AND queasy.number1 = 
                eg-request.SOURCE NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN char1 = queasy.char1.
            FIND FIRST queasy WHERE queasy.KEY = 130 AND queasy.number1 = 
                request1.SOURCE NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN char2 = queasy.char1.
    
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change Source ReqNo " + STRING(reqNo)
                    + ": " + char1 + " To " + char2
                .
        END.
  
        IF eg-request.deptnum NE request1.deptnum THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.number1 = eg-request.deptnum
                NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN char1 = queasy.char1.

            FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.number1 = request1.deptnum
                NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN char2 = queasy.char1.
    
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change Dept In Charge ReqNo " + STRING(reqNo)
                    + ": " + char1 + " To " + char2
                .
        END.

        IF eg-request.SOURCE-name NE request1.SOURCE-name THEN
        DO:
            IF eg-request.source-name = "" THEN
                CHAR1 = ''.

            IF request1.source-name = "" THEN
                char2 = ''.

            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change Source-name ReqNo " + STRING(reqNo)
                    + ": " + char1 + " To " + char2
                .
        END.
        
        IF eg-request.propertynr = 0 THEN
        DO:
            IF request1.maintask NE eg-request.maintask THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY = 133 AND queasy.number1 = 
                    eg-request.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN char1 = queasy.char1.
                FIND FIRST queasy WHERE queasy.KEY = 133 AND queasy.number1 = 
                    request1.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN char2 = queasy.char1.
                
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Change Sub Group ReqNo " + STRING(reqNo)
                        + ": " + char1 + " To " + char2
                    .
            END.
        
            IF request1.category NE eg-request.category THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY = 132 AND queasy.number1 = 
                    eg-request.category NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN char1 = queasy.char1.
                FIND FIRST queasy WHERE queasy.KEY = 132 AND queasy.number1 = 
                    request1.category NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN char2 = queasy.char1.
                
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Change Main Group ReqNo " + STRING(reqNo)
                        + ": " + char1 + " To " + char2
                    .
            END.
        END.
        ELSE
        DO:
            IF eg-request.propertynr NE request1.propertynr AND request1.propertynr NE 0 THEN
            DO:
                char1 = string(eg-request.propertynr, ">,>>>,>>9").
                char2 = string(request1.propertynr, ">,>>>,>>9").

                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Change Article ReqNo " + STRING(reqNo)
                        + ": " + char1 + " To " + char2
                    .
    
            END.
            ELSE
            DO:
                
            END.
        END.
  
        IF request1.sub-task NE eg-request.sub-task THEN
        DO:
            FIND FIRST eg-subtask WHERE eg-subtask.sub-code = eg-request.sub-task 
                /*AND eg-subtask.reserve-int = ""*/ USE-INDEX CODE_ix NO-LOCK NO-ERROR.
            IF AVAILABLE eg-subtask THEN char1 = eg-subtask.bezeich.
            FIND FIRST eg-subtask WHERE eg-subtask.sub-code = request1.sub-task 
                /*AND eg-subtask.reserve-int = ""*/ USE-INDEX CODE_ix NO-LOCK NO-ERROR.
            IF AVAILABLE eg-subtask THEN char2 = eg-subtask.bezeich.
            
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change Sub Task ReqNo " + STRING(reqNo)
                    + ": " + char1 + " To " + char2
                .
        END.

        IF sub-str NE eg-request.subtask-bezeich THEN
        DO:         
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change Sub Task ReqNo " + STRING(reqNo)
                    + ": " + eg-request.subtask-bezeich + " To " + sub-str
                .
        END.

        IF request1.assign-to NE eg-request.assign-to THEN
        DO: 
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change PIC ReqNo " + STRING(reqNo)
                    + ": " + string(eg-request.assign-to) + " To " + string(request1.assign-to)
                .
        END.
    
        IF request1.zinr NE eg-request.zinr THEN
        DO: 
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change RmNo ReqNo " + STRING(reqNo)
                    + ": " + eg-request.zinr + " To " + request1.zinr
                .
        END.
    
        IF solution NE "" THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Add Solution ReqNo " + STRING(reqNo)
                    + ": " + solution.
                .
        END.
    
        IF eg-request.urgency NE request1.urgency THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Change Urgency ReqNo " + STRING(reqNo)
                    + ": " + urgstr[eg-request.urgency] + " To " + urgstr[request1.urgency].
            .
        END.

        IF eg-request.ex-finishdate NE ? THEN
        DO:

            IF eg-request.ex-finishdate NE request1.ex-finishdate THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Change Ex Finish Date ReqNo " + STRING(reqNo)
                        + ": " + STRING(eg-request.ex-finishdate, "99/99/99") + " To " + 
                       STRING(request1.ex-finishdate,"99/99/99")
                .
    
                CREATE eg-reqdetail.
                ASSIGN eg-reqdetail.reqnr = reqno
                       eg-reqdetail.estfinishdate   = request1.ex-finishdate
                       eg-reqdetail.estfinishtime   = request1.ex-finishtime
                       eg-reqdetail.create-date     = TODAY
                       eg-reqdetail.create-time     = TIME
                       eg-reqdetail.create-by       = user-init.
            END.
            ELSE
            DO:

                IF eg-request.ex-finishtime NE request1.ex-finishtime THEN
                DO:
                    CREATE res-history.
                    ASSIGN
                        res-history.nr          = usrnr
                        res-history.datum       = TODAY
                        res-history.zeit        = TIME
                        res-history.Action      = "Engineering"
                        res-history.aenderung   = "Change Ex Finish Time ReqNo " + STRING(reqNo)
                            + ": " + STRING(eg-request.ex-finishtime, "HH:MM") + " To " + 
                           STRING(request1.ex-finishtime,"HH:MM").
    
                    CREATE eg-reqdetail.
                    ASSIGN eg-reqdetail.reqnr = reqno
                           eg-reqdetail.estfinishdate   = request1.ex-finishdate
                           eg-reqdetail.estfinishtime   = request1.ex-finishtime
                           eg-reqdetail.create-date     = TODAY
                           eg-reqdetail.create-time     = TIME
                           eg-reqdetail.create-by       = user-init.
                END. 
                ELSE
                DO:
                    IF trim(replace(estfin-str, ":", "")) NE "" THEN
                    DO:
                        hour    = (INT(estfin-str) / 100)  .
                        minute  = (INT(estfin-str) - (hour * 100))  .
                
                        timeEst = (hour * 3600) + (minute * 60).
                    END.

                    IF eg-request.ex-finishtime NE timeEst THEN
                    DO:
                        CREATE res-history.
                        ASSIGN
                            res-history.nr          = usrnr
                            res-history.datum       = TODAY
                            res-history.zeit        = TIME
                            res-history.Action      = "Engineering"
                            res-history.aenderung   = "Change Ex Finish Time ReqNo " + STRING(reqNo)
                                + ": " + STRING(eg-request.ex-finishtime, "HH:MM") + " To " + 
                               STRING(timeest ,"HH:MM").
                    END.
                   
                END.
            END.
        END.
    END.


    FOR EACH eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = 
        reqNo USE-INDEX keyreq_ix NO-LOCK:
        char1 = "".
        FIND FIRST stock WHERE stock.stock-nr = eg-queasy.stock-nr NO-LOCK 
            NO-ERROR.
        IF NOT AVAILABLE stock THEN
        DO:
            FIND FIRST l-artikel WHERE l-artikel.artnr = eg-queasy.stock-nr
                USE-INDEX artnr_ix NO-LOCK NO-ERROR.
            IF AVAILABLE l-artikel THEN char1 = l-artikel.bezeich.
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Delete Stock ReqNo " + STRING(reqNo)
                    + ": " + char1.
        END.
        ELSE
        DO:
            /*IF stock.stock-qty NE eg-queasy.stock-qty THEN*/
            IF stock.stock-qty NE eg-queasy.deci1 THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Change Stock Qty ReqNo " + STRING(reqNo)
                        + ": " + STRING(eg-queasy.deci1) + " To " + 
                        STRING(stock.stock-qty).
            END.
        END. /*available stock*/
    END. /*for each eg-queasy */

    FOR EACH stock NO-LOCK:
        IF stock.stock-nr NE 0 THEN
        DO:
            FIND FIRST eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = reqNo AND
                eg-queasy.stock-nr = stock.stock-nr USE-INDEX keynrstock_ix NO-LOCK NO-ERROR.
            IF NOT AVAILABLE eg-queasy THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Add Stock ReqNo " + STRING(reqNo)
                        + ": " + stock.stock-nm + " Qty: " + STRING(stock.stock-qty).
            END.
        END.
    END.

    FOR EACH attchment NO-LOCK:
        IF attchment.att-file NE "" THEN
        DO:
            FIND FIRST eg-queasy WHERE eg-queasy.KEY = 2 AND eg-queasy.reqnr = reqNo
                AND eg-queasy.number1 = attchment.nr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE eg-queasy THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = usrnr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.Action      = "Engineering"
                    res-history.aenderung   = "Add Attachment ReqNo " + STRING(reqNo)
                        + ": " + attchment.att-file.
            END.
            ELSE
            DO:
                IF attchment.att-file NE eg-queasy.ATTACHMENT THEN
                DO:
                    CREATE res-history.
                    ASSIGN
                        res-history.nr          = usrnr
                        res-history.datum       = TODAY
                        res-history.zeit        = TIME
                        res-history.Action      = "Engineering"
                        res-history.aenderung   = "Chg Attachment's ReqNo " + STRING(reqNo)
                            + ": " + eg-queasy.ATTACHMENT + " To " + attchment.att-file.
                END.
                IF attchment.bezeich NE eg-queasy.att-desc THEN
                DO:
                    CREATE res-history.
                    ASSIGN
                        res-history.nr          = usrnr
                        res-history.datum       = TODAY
                        res-history.zeit        = TIME
                        res-history.Action      = "Engineering"
                        res-history.aenderung   = "Chg Attachment's desc ReqNo " + STRING(reqNo)
                            + ": " + eg-queasy.att-desc + " To " + attchment.bezeich.
                END. 
            END.     /* available eg-queasy*/
        END. /*attchment.att-file ne ""*/
    END.

    FOR EACH eg-queasy WHERE eg-queasy.KEY = 2 AND eg-queasy.reqnr = reqNo
        USE-INDEX keyreq_ix NO-LOCK:
        FIND FIRST attchment WHERE attchment.nr = eg-queasy.number1
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE attchment OR attchment.att-file = "" THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering"
                res-history.aenderung   = "Delete Attachment ReqNo " + STRING(reqNo)
                    + ": " + eg-queasy.ATTACHMENT.
        END.
    END.
END.

PROCEDURE execute-it:
    DEF VAR timeStr  AS CHAR INITIAL "" NO-UNDO.
    DEF VAR number1  AS INTEGER INITIAL 0 NO-UNDO.
    DEF VAR hist-ctr AS INTEGER INITIAL 0 NO-UNDO.

    DEF VAR hour AS INTEGER.
    DEF VAR minute AS INTEGER.
    DEF VAR TimeEst AS INTEGER.

    DEF BUFFER usr FOR eg-staff.

    FOR EACH eg-queasy WHERE eg-queasy.KEY = 3 AND eg-queasy.reqnr = reqNo
        USE-INDEX keyreq_ix NO-LOCK:
        IF eg-queasy.hist-nr GT hist-ctr THEN hist-ctr = eg-queasy.hist-nr.
    END.
    hist-ctr = hist-ctr + 1. 
    
    IF request1.assign-to NE eg-request.assign-to THEN
    DO:

        FIND FIRST usr WHERE usr.nr = request1.assign-to NO-LOCK NO-ERROR.
        IF AVAILABLE usr THEN number1 = usr.nr.
        CREATE eg-queasy.
        ASSIGN 
            eg-queasy.KEY        = 3
            eg-queasy.reqnr      = reqNo
            eg-queasy.hist-nr    = hist-ctr
            eg-queasy.hist-time  = TIME
            eg-queasy.hist-fdate = TODAY
            eg-queasy.usr-nr     = number1
            .
        FIND CURRENT eg-queasy NO-LOCK.
    END.

    IF request1.reqstatus = 5 AND eg-request.reqstatus NE 5 THEN
        ASSIGN
        request1.closed-date = TODAY
        request1.closed-by   = user-init
        request1.closed-time = TIME.
        /*IF request1.reqstatus =  THEN*/
    ELSE IF request1.reqstatus = 2 AND eg-request.reqstatus NE 2 THEN
    DO:

        ASSIGN
            request1.done-by      = ""
            request1.done-date    = ?
            request1.done-time    = 0
            request1.process-date = TODAY
            request1.process-by   = user-init
            request1.process-time = TIME.

        /*MTENABLE btn-print WITH FRAME frame1.
        HIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Print work order ?",lvCAREA, "")
            VIEW-AS ALERT-BOX QUESTION BUTTON YES-NO UPDATE answer.
        IF answer THEN
        DO:

            APPLY "choose" TO btn-print.
        END.
        */
    END.
    ELSE IF request1.reqstatus = 3 AND eg-request.reqstatus NE 3 THEN
    DO:
        ASSIGN
            request1.done-date = TODAY
            request1.done-by   = user-init
            request1.done-time = TIME.
        
        IF eg-request.ex-finishdate NE ? THEN
        DO:
            IF eg-request.ex-finishdate = TODAY THEN
            DO:
                IF eg-request.ex-finishtime < TIME THEN
                DO:
                    blrange = 1.
                END.
            END.
            ELSE IF eg-request.ex-finishdate < TODAY THEN
            DO:
                blrange = 1.
            END.
        END.
        ELSE
        DO:
            ASSIGN request1.ex-finishdate = request1.done-date
                   request1.ex-finishtime = request1.done-time.
            /*
            IF eg-request.ex-finishdate = TODAY THEN
            DO:
                IF eg-request.ex-finishtime < TIME THEN
                DO:
                    blrange = 1.
                END.
            END.
            ELSE IF eg-request.ex-finishdate < TODAY THEN
            DO:
                blrange = 1.
            END.
            */
        END.

    END.

    ASSIGN request1.subtask-bezeich = sub-str.

    FIND CURRENT eg-request EXCLUSIVE-LOCK.
    
    IF request1.propertynr NE 0 THEN
    DO:
        ASSIGN request1.maintask = 0
            request1.category = 0
           /* request1.reserve-int = 0
            request1.zinr        = ""*/ 
            .
    END.
    
    IF trim(replace(estfin-str, ":", "")) NE "" THEN
    DO:
        hour    = (INT(estfin-str) / 100)  .
        minute  = (INT(estfin-str) - (hour * 100))  .

        timeEst = (hour * 3600) + (minute * 60).
        request1.ex-finishtime = timeEst.
    END.


    BUFFER-COPY request1 TO eg-request.
    IF solution NE "" THEN
        eg-request.task-solv = eg-request.task-solv + solution + CHR(10) + 
        STRING(TODAY, "99/99/9999") + " - " + STRING(TIME,"HH:MM:SS") + CHR(10).

    FIND CURRENT eg-request NO-LOCK.

    FOR EACH eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = reqNo
        USE-INDEX keyreq_ix:
        DELETE eg-queasy.
    END.

    DEFINE BUFFER sbuff FOR stock.
    FOR EACH sbuff BY sbuff.stock-nr:
        IF sbuff.stock-nr NE 0 THEN
        DO:
            CREATE eg-queasy.
            ASSIGN 
                eg-queasy.KEY       = 1
                eg-queasy.reqnr     = reqNo
                eg-queasy.stock-nr  = sbuff.stock-nr
                /*eg-queasy.stock-qty = sbuff.stock-qty*/
                eg-queasy.deci1     = sbuff.stock-qty
                eg-queasy.price     = sbuff.stock-price.
        END.
    END.

    FOR EACH eg-queasy WHERE eg-queasy.KEY = 2 AND eg-queasy.reqnr = reqNo
        USE-INDEX keyreq_ix:
        DELETE eg-queasy.
    END.

    FOR EACH attchment:
        IF attchment.att-file NE "" THEN
        DO:
            CREATE eg-queasy.
            ASSIGN
                eg-queasy.KEY        = 2
                eg-queasy.reqnr      = reqNo
                eg-queasy.number1    = attchment.nr
                eg-queasy.ATTACHMENT = attchment.att-file
                eg-queasy.att-desc   = attchment.bezeich.
        END.
    END.
END.


PROCEDURE save-vendor:
    DEF BUFFER usr   FOR bediener.
    DEF VAR usrnr    AS INTEGER INITIAL 0  NO-UNDO.

    DEFINE VAR char1 AS CHAR NO-UNDO.
    DEFINE VAR char2 AS CHAR NO-UNDO.

    DEFINE BUFFER pbuff FOR eg-vperform.
    DEFINE BUFFER vbuff FOR eg-request.
    DEFINE VAR strVendor AS CHAR.
    DEFINE VAR strfull AS CHAR.

    FOR EACH svendor WHERE svendor.stat = "0":
        FIND FIRST eg-vperform WHERE eg-vperform.reqnr = reqno AND eg-vperform.perform-nr = svendor.perform-nr NO-ERROR.
        IF AVAILABLE eg-vperform THEN 
        DO:
            ASSIGN eg-vperform.logi1 = YES.
        END.   
    END.

    FIND FIRST pbuff WHERE pbuff.reqnr = request1.reqnr AND pbuff.logi1 = NO NO-LOCK NO-ERROR.
    IF AVAILABLE pbuff THEN
    DO:
        FIND FIRST eg-vendor WHERE eg-vendor.vendor-nr = pbuff.vendor-nr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-vendor THEN char1 = eg-vendor.bezeich.
        FIND FIRST eg-vendor WHERE eg-vendor.vendor-nr = svendor.vendor-nr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-vendor THEN char2 = eg-vendor.bezeich.

        FIND FIRST svendor WHERE svendor.reqnr = reqno AND svendor.perform-nr = pbuff.perform-nr NO-LOCK NO-ERROR.
        IF AVAILABLE svendor THEN
        DO:
               IF pbuff.vendor-nr NE svendor.vendor-nr THEN
                DO:
                    CREATE res-history.
                    ASSIGN
                        res-history.nr          = usrnr
                        res-history.datum       = TODAY
                        res-history.zeit        = TIME
                        res-history.Action      = "Engineering Vendor Perform"
                        res-history.aenderung   = "Chg vendor ReqNo " + STRING(reqNo)
                            + ": " + char1 + " To " + char2.
                END.

                IF pbuff.documentno NE svendor.docno THEN
                DO:
                    CREATE res-history.
                    ASSIGN
                        res-history.nr          = usrnr
                        res-history.datum       = TODAY
                        res-history.zeit        = TIME
                        res-history.Action      = "Engineering Vendor Perform"
                        res-history.aenderung   = "Chg vendor ReqNo " + STRING(reqNo)
                            + ": " + pbuff.documentno + " To " + svendor.docno .
                END.

                IF pbuff.startdate NE svendor.startdate THEN
                DO:
                    CREATE res-history.
                      ASSIGN
                          res-history.nr          = usrnr
                          res-history.datum       = TODAY
                          res-history.zeit        = TIME
                          res-history.Action      = "Engineering Vendor Perform"
                          res-history.aenderung   = "Chg vendor start-date ReqNo " + STRING(reqNo)
                              + ": " + string(pbuff.startdate , "99/99/99") + " To " + string(svendor.startdate , "99/99/99").
                END.

                IF pbuff.estfinishdate NE svendor.estfinishdate THEN
                DO:
                    CREATE res-history.
                      ASSIGN
                          res-history.nr          = usrnr
                          res-history.datum       = TODAY
                          res-history.zeit        = TIME
                          res-history.Action      = "Engineering Vendor Perform"
                          res-history.aenderung   = "Chg vendor estfinishdate ReqNo " + STRING(reqNo)
                              + ": " + string(pbuff.estfinishdate , "99/99/99") + " To " + string(svendor.estfinishdate , "99/99/99").
                END.

                IF pbuff.finishdate NE svendor.finishdate THEN
                DO:
                    CREATE res-history.
                      ASSIGN
                          res-history.nr          = usrnr
                          res-history.datum       = TODAY
                          res-history.zeit        = TIME
                          res-history.Action      = "Engineering Vendor Perform"
                          res-history.aenderung   = "Chg vendor finishdate ReqNo " + STRING(reqNo)
                              + ": " + string(pbuff.finishdate , "99/99/99") + " To " + string(svendor.finishdate , "99/99/99").
                END.

                IF pbuff.price NE svendor.price THEN
                DO:
                    CREATE res-history.
                      ASSIGN
                          res-history.nr          = usrnr
                          res-history.datum       = TODAY
                          res-history.zeit        = TIME
                          res-history.Action      = "Engineering Vendor Perform"
                          res-history.aenderung   = "Chg vendor Reparation Fee ReqNo " + STRING(reqNo)
                              + ": " + string(pbuff.price , "->>,>>>,>>>,>>9.99") + " To " + string(svendor.price , "->>,>>>,>>>,>>9.99").
                END.

                IF pbuff.pic NE svendor.pic THEN
                DO:
                    CREATE res-history.
                      ASSIGN
                          res-history.nr          = usrnr
                          res-history.datum       = TODAY
                          res-history.zeit        = TIME
                          res-history.Action      = "Engineering Vendor Perform"
                          res-history.aenderung   = "Chg vendor Reparation Fee ReqNo " + STRING(reqNo)
                              + ": " + pbuff.pic + " To " + svendor.pic .
                END.
        END.
    END.

    DEF VAR startC AS INTEGER NO-UNDO.

    FIND LAST eg-vperform WHERE eg-vperform.reqnr = reqno NO-LOCK NO-ERROR .
    IF AVAILABLE eg-vperform THEN
    DO:
        startC = int(eg-vperform.perform-nr) + 1.    
    END.
    ELSE
    DO:
        startC = 1.
    END.

    FOR EACH svendor WHERE svendor.stat = "1" :
        IF SUBSTR(sVendor.perform-nr, 1, 1 ) NE "n" THEN
        DO:
            FIND FIRST eg-vperform WHERE eg-vperform.reqnr = reqno AND eg-vperform.perform-nr = svendor.perform-nr NO-ERROR.
            IF AVAILABLE eg-vperform THEN
            DO:
                /*BUFFER-COPY svendor TO eg-vperform.*/
                ASSIGN eg-vperform.reqnr = reqno
                    eg-vperform.created-by = user-init
                    eg-vperform.created-date = TODAY
                    eg-vperform.created-time = TIME
                    eg-vperform.documentno = svendor.docno
                    eg-vperform.vendor-nr = svendor.vendor-nr
                    eg-vperform.startdate = svendor.startdate
                    eg-vperform.estfinishdate = svendor.estfinishdate
                    eg-vperform.finishdate = svendor.finishdate
                    eg-vperform.price = svendor.price
                    eg-vperform.bezeich = svendor.bezeich
                    eg-vperform.pic = svendor.pic.
            END.
            ELSE
            DO:
    
            END.
        END.
        ELSE
        DO:
            CREATE eg-vperform.
            ASSIGN eg-vperform.reqnr = reqno
                    eg-vperform.created-by = user-init
                    eg-vperform.created-date = TODAY
                    eg-vperform.created-time = TIME
                    eg-vperform.documentno = svendor.docno
                    eg-vperform.vendor-nr = svendor.vendor-nr
                    eg-vperform.startdate = svendor.startdate
                    eg-vperform.estfinishdate = svendor.estfinishdate
                    eg-vperform.finishdate = svendor.finishdate
                    eg-vperform.price = svendor.price
                    eg-vperform.bezeich = svendor.bezeich
                    eg-vperform.pic = svendor.pic
                    eg-vperform.perform-nr = STRING(startC).
    
            startC = startC + 1.
        END.
    END.

END.

