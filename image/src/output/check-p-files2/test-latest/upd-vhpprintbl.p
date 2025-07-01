
{tb-printer.i}
DEFINE TEMP-TABLE t-printer LIKE PRINTER.

DEFINE INPUT  PARAMETER TABLE FOR t-printer. 

DEFINE VARIABLE content          AS LONGCHAR  NO-UNDO.
DEFINE VARIABLE newContent       AS LONGCHAR  NO-UNDO INITIAL ?.
DEFINE VARIABLE ni               AS INTEGER   NO-UNDO.
DEFINE VARIABLE maxRowPerPage    AS INTEGER   NO-UNDO.
DEFINE VARIABLE newMaxRowPerPage AS INTEGER   NO-UNDO INITIAL 0.

DEFINE VARIABLE fileSettings     AS CHARACTER NO-UNDO.

/* Rulita 230425 | Fixing serverless di vhp sudah tidak di pakai git issue 357 */
/*
FIND FIRST t-printer WHERE t-printer.make EQ "vhpprint" NO-LOCK NO-ERROR.
IF AVAILABLE t-printer THEN
DO:
    ASSIGN 
        newMaxRowPerPage = t-printer.pglen
        fileSettings     = SEARCH("VHPPrint\AppSettings.xml").

    IF fileSettings NE ? THEN
    DO:
        COPY-LOB FROM FILE fileSettings TO content.
    
        DO ni = 1 TO NUM-ENTRIES(content, CHR(13)):
            DEFINE VARIABLE aLine    AS CHARACTER NO-UNDO.
            DEFINE VARIABLE newLine  AS CHARACTER NO-UNDO.
            DEFINE VARIABLE seekLine AS CHARACTER NO-UNDO.
    
            aLine = ENTRY(ni, content, CHR(13)).
    
            IF aLine MATCHES "*<maxRowPerPage>*" THEN
            DO:
                maxRowPerPage = INTEGER( ENTRY(1, ENTRY(2, aLine, ">"), "<") ).

                IF maxRowPerPage NE newMaxRowPerPage THEN
                DO:
                    newLine = REPLACE(aLine, STRING(maxRowPerPage), STRING(newMaxRowPerPage)).
                    newContent = REPLACE(content, aLine, newLine).
                END.
            END.
        END.
    
        /* COPY-LOB FROM newContent TO FILE "C:\e1-dev\test\vhpprint\AppSettings2.xml". */
    
        IF newContent NE ? THEN COPY-LOB FROM newContent TO FILE fileSettings.
    END. 
END.
*/