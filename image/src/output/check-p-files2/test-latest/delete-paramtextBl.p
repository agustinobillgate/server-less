

DEF INPUT PARAMETER case-type   AS INTEGER.
DEF INPUT PARAMETER int1        AS INTEGER.
DEF INPUT PARAMETER int2        AS INTEGER.
DEF INPUT PARAMETER int3        AS INTEGER.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEFINE VARIABLE counter AS INTEGER NO-UNDO INIT 0.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST paramtext WHERE paramtext.txtnr EQ int1
            AND paramtext.number EQ int2 AND paramtext.sprachcode EQ int3
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN
        DO:
            DELETE paramtext.
            RELEASE paramtext.
            success-flag = YES.
        END.
    END.
    WHEN 2 THEN /*del for setup bed and outlook*/
    DO:
        FIND FIRST paramtext WHERE paramtext.txtnr EQ int1
            AND paramtext.number EQ int2 AND paramtext.sprachcode EQ int3
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN
        DO:
            /* SY AUG 26 2017 */
            FIND FIRST zimmer WHERE zimmer.setup = paramtext.txtnr - 9200
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE zimmer AND paramtext.txtnr = 230 THEN
            FIND FIRST zimmer WHERE zimmer.typ = paramtext.sprachcode
               NO-LOCK NO-ERROR.
            IF NOT AVAILABLE zimmer THEN
            DO:
                DELETE paramtext.
                RELEASE paramtext.
                success-flag = YES.
            END.
        END.
    END.
END CASE.
