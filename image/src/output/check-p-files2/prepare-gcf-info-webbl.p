DEFINE TEMP-TABLE gcfinfo-list
    FIELD nr            AS INTEGER  FORMAT "99"
    FIELD dept          AS INTEGER 
    FIELD rechnr        AS INTEGER
    FIELD datum         AS DATE
    FIELD str           AS CHAR     FORMAT "x(94)"
    FIELD dept-str      AS CHARACTER
    FIELD amount-food   AS CHARACTER
    FIELD amount-bev    AS CHARACTER
    FIELD amount-other  AS CHARACTER
    FIELD room-number   AS CHARACTER
    FIELD room-type     AS CHARACTER
    FIELD arrival       AS CHARACTER
    FIELD departure     AS CHARACTER
    .
DEFINE TEMP-TABLE t-guest LIKE guest.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER gastnr       AS INTEGER.
DEFINE OUTPUT PARAMETER payment     AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-guest.
DEFINE OUTPUT PARAMETER TABLE FOR gcfinfo-list.


FIND FIRST guest WHERE guest.gastnr EQ gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
DO:
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.

    IF guest.zahlungsart GT 0 THEN 
    DO: 
        FIND FIRST artikel WHERE departement EQ 0 AND artikel.artnr EQ guest.zahlungsart NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN payment = STRING(guest.zahlungsart) + "  -  " + artikel.bezeich. 
    END. 
END.

RUN create-list.

/************************************* PROCEDURE *************************************/
PROCEDURE create-list:
DEFINE BUFFER reslin FOR res-line.
DEFINE BUFFER htldpt FOR hoteldpt.
DEFINE BUFFER ginfo FOR guest-queasy. 

DEFINE VARIABLE str1        AS CHAR NO-UNDO.
DEFINE VARIABLE i           AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE dept-str    AS CHAR FORMAT "x(24)"      NO-UNDO.
DEFINE VARIABLE cistr       AS CHAR FORMAT "x(8)"       NO-UNDO.
DEFINE VARIABLE costr       AS CHAR FORMAT "x(8)"       NO-UNDO.
DEFINE VARIABLE curr-dept   AS INTEGER                  NO-UNDO.
DEFINE VARIABLE sub-tot     AS DECIMAL                  NO-UNDO.
DEFINE VARIABLE sub-tot2    AS DECIMAL                  NO-UNDO.
DEFINE VARIABLE sub-tot3    AS DECIMAL                  NO-UNDO.
DEFINE VARIABLE total1      AS DECIMAL                  NO-UNDO.
DEFINE VARIABLE total2      AS DECIMAL                  NO-UNDO.
DEFINE VARIABLE total3      AS DECIMAL                  NO-UNDO.
DEFINE VARIABLE sub-str     AS CHAR    FORMAT "x(24)"   NO-UNDO.
DEFINE VARIABLE it-exists   AS LOGICAL INITIAL NO.
DEFINE VARIABLE rmno        AS CHAR    INITIAL "".
DEFINE VARIABLE rmcat       AS CHAR    INITIAL "".
          
DEFINE VARIABLE invDept     AS INTEGER                  NO-UNDO.
DEFINE VARIABLE invNo       AS INTEGER                  NO-UNDO.
DEFINE VARIABLE invDate     AS DATE                     NO-UNDO.

DEFINE VARIABLE deptname    AS CHARACTER. 
DEFINE VARIABLE amt-food    AS CHARACTER.
DEFINE VARIABLE amt-bev     AS CHARACTER.
DEFINE VARIABLE amt-other   AS CHARACTER.    

    FOR EACH gcfinfo-list:
        DELETE gcfinfo-list.
    END.

    sub-str = "SUBTOTAL".
    FOR EACH ginfo WHERE ginfo.KEY = "gast-info" AND ginfo.gastnr = gastnr
        NO-LOCK BY ginfo.number1 BY ginfo.date1:
        IF curr-dept NE ginfo.number1 AND curr-dept NE 0 THEN
        DO:
            i = i + 1.           
            RUN add-line(i, FILL("-", 30), FILL("-", 30), FILL("-", 30), FILL("-", 30), "", "", -1, 0, ?, "", "").

            i = i + 1.            
            deptname    = sub-str.
            amt-food    = STRING(sub-tot, "->>,>>>,>>>,>>>,>>9.99").
            amt-bev     = STRING(sub-tot2, "->>,>>>,>>>,>>>,>>9.99").
            amt-other   = STRING(sub-tot3, "->>,>>>,>>>,>>>,>>9.99").
            ASSIGN
              invDept  = ginfo.number1
              invNo    = INTEGER(ginfo.char1)
              invDate  = ginfo.date1
            .
            RUN add-line(i, deptname, amt-food, amt-bev, amt-other, "", "", -1, 0, ?, "", "").
            /*Break Line*/
            i = i + 1.
            RUN add-line(i, "", "", "", "", "", "", -3, 0, ?, "", "").
            sub-tot = 0.
            sub-tot2 = 0.
            sub-tot3 = 0.
        END.
        
        it-exists = YES.

        i = i + 1.
        FIND FIRST htldpt WHERE htldpt.num EQ ginfo.number1 NO-LOCK NO-ERROR.
        IF AVAILABLE htldpt THEN dept-str = htldpt.depart.
        ELSE dept-str = "UNKNOWN".

        ASSIGN 
            cistr = STRING(ginfo.date1, "99/99/99")
            costr = cistr
        .

        FIND FIRST reslin WHERE reslin.resnr EQ ginfo.number2 
            AND reslin.reslinnr EQ ginfo.number3 USE-INDEX relinr_index NO-LOCK NO-ERROR.
        IF AVAILABLE reslin THEN
        DO:
            cistr = STRING(reslin.ankunft, "99/99/99").
            costr = STRING(reslin.abreise, "99/99/99").
            rmno  = reslin.zinr.
            FIND FIRST zimmer WHERE zimmer.zinr EQ rmno NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer THEN 
            DO:
                FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ zimmer.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN rmcat = zimkateg.kurzbez.
            END.                
        END.
        ELSE
        DO:
            FIND FIRST history WHERE history.gastnr EQ gastnr 
                AND history.resnr EQ ginfo.number2 
                AND history.reslinnr EQ ginfo.number3 USE-INDEX res_ix NO-LOCK NO-ERROR.
            IF AVAILABLE history THEN
            DO:
                cistr   = STRING(history.ankunft, "99/99/99").
                costr   = STRING(history.abreise, "99/99/99").
                rmno    = history.zinr.
                FIND FIRST zimmer WHERE zimmer.zinr EQ rmno NO-LOCK NO-ERROR.
                IF AVAILABLE zimmer THEN 
                DO:
                    FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ zimmer.zikatnr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN rmcat = zimkateg.kurzbez.
                END.                    
            END.
            ELSE
            DO:
                rmno  = "".
                rmcat = "".
            END.
        END.

        ASSIGN
            deptname    = dept-str 
            amt-food    = STRING(ginfo.deci1, "->>,>>>,>>>,>>>,>>9.99")
            amt-bev     = STRING(ginfo.deci2, "->>,>>>,>>>,>>>,>>9.99")
            amt-other   = STRING(ginfo.deci3, "->>,>>>,>>>,>>>,>>9.99")
            invDept     = ginfo.number1
            invNo       = INTEGER(ginfo.char1)
            invDate     = ginfo.date1
        .
        RUN add-line(i, deptname, amt-food, amt-bev, amt-other, rmno, rmcat, invDept, invNo, invDate, cistr, costr).
        curr-dept = ginfo.number1.
        sub-tot = sub-tot + ginfo.deci1.
        sub-tot2 = sub-tot2 + ginfo.deci2.
        sub-tot3 = sub-tot3 + ginfo.deci3.
    END.

    IF it-exists THEN
    DO:
        i = i + 1.
        RUN add-line(i, FILL("-", 30), FILL("-", 30), FILL("-", 30), FILL("-", 30), "", "", -1, 0, ?, "", "").
    
        i = i + 1.
        deptname    = sub-str.
        amt-food    = STRING(sub-tot, "->>,>>>,>>>,>>>,>>9.99").
        amt-bev     = STRING(sub-tot2, "->>,>>>,>>>,>>>,>>9.99").
        amt-other   = STRING(sub-tot3, "->>,>>>,>>>,>>>,>>9.99").
        
        RUN add-line(i, deptname, amt-food, amt-bev, amt-other, "", "", -1, 0, ?, "", "").
        sub-tot = 0.
        sub-tot2 = 0.
        sub-tot3 = 0.
    END.
    
    i = 0.
    FOR EACH gcfinfo-list WHERE gcfinfo-list.dept-str EQ "SUBTOTAL" NO-LOCK:        
        total1 = total1 + DEC( gcfinfo-list.amount-food).
        total2 = total2 + DEC( gcfinfo-list.amount-bev).
        total3 = total3 + DEC( gcfinfo-list.amount-other).
    END.
    FOR EACH gcfinfo-list NO-LOCK BY gcfinfo-list.nr DESC:
        i = gcfinfo-list.nr + 1.
        LEAVE.
    END.

    FIND FIRST gcfinfo-list NO-LOCK NO-ERROR.
    IF AVAILABLE gcfinfo-list THEN
    DO:
        CREATE gcfinfo-list.
        ASSIGN 
            gcfinfo-list.nr              = i        
            gcfinfo-list.dept            = -1
            gcfinfo-list.rechnr          = 0
            gcfinfo-list.datum           = ?
            gcfinfo-list.dept-str        = ""
            gcfinfo-list.amount-food     = ""
            gcfinfo-list.amount-bev      = "" 
            gcfinfo-list.amount-other    = ""
            gcfinfo-list.room-number     = ""  
            gcfinfo-list.room-type       = ""  
            gcfinfo-list.arrival         = ""
            gcfinfo-list.departure       = ""
            .
        
        i = i + 1.
        CREATE gcfinfo-list.
        ASSIGN 
            gcfinfo-list.nr              = i        
            gcfinfo-list.dept            = -2
            gcfinfo-list.rechnr          = 0
            gcfinfo-list.datum           = ?
            gcfinfo-list.dept-str        = "TOTAL" 
            gcfinfo-list.amount-food     = STRING(total1, "->>,>>>,>>>,>>>,>>9.99")
            gcfinfo-list.amount-bev      = STRING(total2, "->>,>>>,>>>,>>>,>>9.99")  
            gcfinfo-list.amount-other    = STRING(total3, "->>,>>>,>>>,>>>,>>9.99")
            gcfinfo-list.room-number     = ""  
            gcfinfo-list.room-type       = ""  
            gcfinfo-list.arrival         = ""
            gcfinfo-list.departure       = ""
            .    
        i = 0.
    END.    
END.

PROCEDURE add-line:
DEFINE INPUT PARAMETER nr           AS INTEGER.
DEFINE INPUT PARAMETER deptname     AS CHARACTER. 
DEFINE INPUT PARAMETER amt-food     AS CHARACTER.
DEFINE INPUT PARAMETER amt-bev      AS CHARACTER.
DEFINE INPUT PARAMETER amt-other    AS CHARACTER.
DEFINE INPUT PARAMETER room-no      AS CHARACTER.
DEFINE INPUT PARAMETER rm-type      AS CHARACTER.
DEFINE INPUT PARAMETER dept         AS INTEGER.
DEFINE INPUT PARAMETER rechnr       AS INTEGER.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE INPUT PARAMETER arrival      AS CHARACTER.
DEFINE INPUT PARAMETER departure    AS CHARACTER.

    CREATE gcfinfo-list.
    ASSIGN 
        gcfinfo-list.nr              = nr        
        gcfinfo-list.dept            = dept
        gcfinfo-list.rechnr          = rechnr
        gcfinfo-list.datum           = datum
        gcfinfo-list.dept-str        = deptname 
        gcfinfo-list.amount-food     = amt-food 
        gcfinfo-list.amount-bev      = amt-bev  
        gcfinfo-list.amount-other    = amt-other
        gcfinfo-list.room-number     = room-no  
        gcfinfo-list.room-type       = rm-type 
        gcfinfo-list.arrival         = arrival
        gcfinfo-list.departure       = departure
        .
END.
