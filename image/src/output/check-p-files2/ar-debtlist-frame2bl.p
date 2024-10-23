.
DEFINE TEMP-TABLE edit-list
    FIELD rechnr        AS INTEGER FORMAT ">>>>>>>>>9"
    FIELD datum         AS DATE FORMAT "99/99/99"
    FIELD zinr          LIKE zimmer.zinr
    FIELD billname      AS CHAR FORMAT "x(32)"
    FIELD lamt          AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD famt          AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD fcurr         AS CHAR FORMAT "x(4)"
    FIELD ar-recid      AS INTEGER
    FIELD amt-change    AS LOGICAL INITIAL NO
    FIELD curr-change   AS LOGICAL INITIAL NO
    FIELD curr-nr       AS INTEGER
    .

DEF INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR NO-UNDO.
DEF INPUT PARAMETER TABLE FOR edit-list.
DEF OUTPUT PARAMETER msg-str AS CHAR INIT "" NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ar-debtlist". 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

FOR EACH edit-list WHERE edit-list.curr-change OR edit-list.amt-change:
    FIND FIRST debitor WHERE RECID(debitor) = edit-list.ar-recid 
        NO-LOCK NO-ERROR.
    IF AVAILABLE debitor THEN
    DO:
        FIND CURRENT debitor EXCLUSIVE-LOCK.
        IF curr-change THEN
        DO:
            DEF VAR old-curr AS CHAR FORMAT "x(4)".
            /**create log file**/
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem
                NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN old-curr = waehrung.wabkurz.
            ELSE old-curr = "".
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
            CREATE res-history.
            ASSIGN 
                res-history.nr      = bediener.nr
                res-history.datum   = TODAY
                res-history.zeit    = TIME
                res-history.action  = "A/R"
                res-history.aenderung = "Change Foreign Currency: " + 
                    old-curr + " To " 
                + STRING(edit-list.fcurr, "x(4)") .
            FIND CURRENT res-history NO-LOCK.

            ASSIGN
              debitor.betrieb-gastmem = edit-list.curr-nr.
        END.
        IF amt-change THEN
        DO:
            /**create log file**/
            
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
            CREATE res-history.
            ASSIGN 
                res-history.nr      = bediener.nr
                res-history.datum   = TODAY
                res-history.zeit    = TIME
                res-history.action  = "A/R"
                res-history.aenderung = "Change Foreign Amount: " + 
                    TRIM(STRING(debitor.vesrdep, "->>>,>>>,>>9.99")) + " To " 
                + TRIM(STRING(edit-list.famt, "->>>,>>>,>>9.99")) .
            FIND CURRENT res-history NO-LOCK.

            ASSIGN debitor.vesrdep = edit-list.famt.
        END.
        FIND CURRENT debitor NO-LOCK.
    END.
    ELSE msg-str = msg-str + translateExtended("Unable to update A/R Record BillNo", lvCAREA, "") 
                 + " " + STRING(edit-list.rechnr) + "." + CHR(2).
END.
