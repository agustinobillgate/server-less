/*
*** Program     : rate-code-changes-webbl.p
*** Description : Program untuk menampilkan perubahan rate code
*** Last Update : 19-05-25
*** Created By  : BLY
*/

DEFINE TEMP-TABLE tt-rate-changes
    FIELD dated1            AS DATE     FORMAT "99/99/9999"
    FIELD dated2            AS DATE     FORMAT "99/99/9999"
    FIELD timed             AS INTEGER
    FIELD logi              AS LOGICAL
    FIELD rate-before       AS CHARACTER
    FIELD rate-after        AS CHARACTER
    FIELD amount-after      AS DECIMAL
    FIELD amount-before     AS DECIMAL
    FIELD room-category     AS CHARACTER
    INDEX idx1 dated1 dated2 timed
    .

/* input-output parameter */
DEFINE INPUT PARAMETER from-date          AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER to-date            AS DATE     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tt-rate-changes.

/* test local 
DEF VAR from-date AS DATE NO-UNDO.
DEF VAR to-date AS DATE NO-UNDO.

ASSIGN
    from-date = 05/16/2025
    to-date = 05/19/2025
    .
*/

/* Local Variable */
DEFINE VARIABLE delimiterd          AS CHARACTER    NO-UNDO     INIT ";".
DEFINE VARIABLE char-data           AS CHARACTER    NO-UNDO.
DEFINE VARIABLE v-rate-before       AS CHARACTER    NO-UNDO.
DEFINE VARIABLE v-rate-after        AS CHARACTER    NO-UNDO.
DEFINE VARIABLE v-amount-before     AS DECIMAL      NO-UNDO.
DEFINE VARIABLE v-amount-after      AS DECIMAL      NO-UNDO.
DEFINE VARIABLE v-room-category     AS CHARACTER    NO-UNDO.

/* Delete temp table */
EMPTY TEMP-TABLE tt-rate-changes.

/* main logic */
FOR EACH reslin-queasy WHERE reslin-queasy.KEY EQ "dynaChanges" 
    AND reslin-queasy.date2 GE from-date
    AND reslin-queasy.date2 LE to-date NO-LOCK:

    ASSIGN
        char-data = reslin-queasy.char3.

    IF NUM-ENTRIES(char-data, delimiterd) GE 5 THEN
    DO:
        ASSIGN
            v-rate-before           = ENTRY(1, char-data, delimiterd)
            v-rate-after            = ENTRY(2, char-data, delimiterd)
            v-amount-before         = DECIMAL(ENTRY(3, char-data, delimiterd))
            v-amount-after          = DECIMAL(ENTRY(4, char-data, delimiterd))
            v-room-category         = ENTRY(5, char-data, delimiterd)
            .

        CREATE tt-rate-changes.
            ASSIGN
                tt-rate-changes.dated1               = reslin-queasy.date1
                tt-rate-changes.dated2               = reslin-queasy.date2
                tt-rate-changes.timed                = reslin-queasy.number1
                tt-rate-changes.logi                 = reslin-queasy.logi1
                tt-rate-changes.rate-before          = v-rate-before
                tt-rate-changes.rate-after           = v-rate-after
                tt-rate-changes.amount-before        = v-amount-before
                tt-rate-changes.amount-after         = v-amount-after
                tt-rate-changes.room-category        = v-room-category
                .
    END.
END.

/* Local Display
CURRENT-WINDOW:WIDTH = 200.
FOR EACH tt-rate-changes NO-LOCK:
    DISP 
        tt-rate-changes.dated1
        tt-rate-changes.dated2
        tt-rate-changes.timed
        tt-rate-changes.logi
        tt-rate-changes.rate-before
        tt-rate-changes.rate-after
        tt-rate-changes.amount-before FORMAT "->>,>>>,>>9.99"
        tt-rate-changes.amount-after FORMAT "->>,>>>,>>9.99"
        tt-rate-changes.room-category
        WITH WIDTH 190.
END.

*/
