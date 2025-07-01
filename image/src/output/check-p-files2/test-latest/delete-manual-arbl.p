/* Created by Michael @ 25/07/2019 */
 
DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER rechnr          AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER ar-recid        AS INTEGER NO-UNDO. 
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL NO-UNDO INITIAL NO. 
DEFINE OUTPUT PARAMETER msg-str         AS CHAR.

DEF TEMP-TABLE t-gl-journal LIKE gl-journal
    FIELD b-recid AS INTEGER.

DEFINE VARIABLE acc-close       AS DATE NO-UNDO.
DEFINE VARIABLE ar-gl           AS DATE NO-UNDO.

{ supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "delete-manual-ar". 
/**********  MAIN LOGIC  **********/ 
DEFINE VARIABLE char1 AS CHAR NO-UNDO.

RUN htpdate.p (558, OUTPUT acc-close).
RUN htpdate.p (1014, OUTPUT ar-gl).

char1 = STRING(rechnr).

/*RUN read-gl-journalbl.p(3, ?, ?, ?, ?, ?, rechnr, "", "", ?, ?, OUTPUT TABLE t-gl-journal). FT serverless*/
RUN read-gl-journalbl.p(3, ?, ?, ?, ?, ?, char1 , "", "", ?, ?, OUTPUT TABLE t-gl-journal).

FIND FIRST t-gl-journal NO-LOCK NO-ERROR.
IF AVAILABLE t-gl-journal THEN
DO: 
    FIND FIRST debitor WHERE RECID(debitor) EQ ar-recid NO-LOCK NO-ERROR.
    IF AVAILABLE debitor /*FT serverless*/ AND debitor.zahlkonto EQ 0 AND debitor.counter EQ 0 THEN
    DO:
        IF debitor.rgdatum GT acc-close AND debitor.rgdatum GT ar-gl THEN
        DO:
            RUN delete-debitorbl.p(1, ar-recid, OUTPUT success-flag).
            RUN delete-gl-jouhdrbl.p(3, t-gl-journal.jnr, ?, "", ?, OUTPUT success-flag).
            RUN delete-gl-journalbl.p(2, ?, STRING(rechnr), OUTPUT success-flag).
        END.
        ELSE
        DO:
            ASSIGN success-flag = NO.
            ASSIGN msg-str = translateExtended("The transaction has closed", lvCAREA, "").
            RETURN NO-APPLY.
        END.
    END.
    ELSE
    DO:
        ASSIGN success-flag = NO.
        ASSIGN msg-str = translateExtended("The transaction has paid", lvCAREA, "").
        RETURN NO-APPLY.
    END.
END.
ELSE
DO: 
    FIND FIRST debitor WHERE RECID(debitor) EQ ar-recid NO-LOCK NO-ERROR.
    IF AVAILABLE debitor /*FT serverless*/ AND debitor.zahlkonto EQ 0 AND debitor.counter EQ 0 THEN
    DO:
        IF debitor.rgdatum GT acc-close AND debitor.rgdatum GT ar-gl THEN
        DO:
            RUN delete-debitorbl.p(1, ar-recid, OUTPUT success-flag).
        END.
        ELSE
        DO:
            ASSIGN success-flag = NO.
            ASSIGN msg-str = translateExtended("The transaction has closed", lvCAREA, "").
            RETURN NO-APPLY.
        END.
    END.
    ELSE
    DO:
        ASSIGN success-flag = NO.
        ASSIGN msg-str = translateExtended("The transaction has paid", lvCAREA, "").
        RETURN NO-APPLY.
    END.
END.
