DEFINE TEMP-TABLE t-segment LIKE segment.

DEFINE INPUT PARAMETER vKey         AS INTEGER.
DEFINE INPUT PARAMETER bill-number  AS INTEGER.
DEFINE INPUT PARAMETER dept-number  AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-segment.

IF vKey EQ 1 THEN   /*All Active Segment*/
DO:
    FOR EACH segment WHERE NUM-ENTRIES(segment.bezeich, "$$0") EQ 1 
        NO-LOCK BY segment.segmentcode:
        CREATE t-segment.
        BUFFER-COPY segment TO t-segment.
    END.
END.
ELSE IF vKey EQ 2 THEN
DO:
    FIND FIRST h-bill WHERE h-bill.rechnr EQ bill-number
        AND h-bill.departement EQ dept-number
        AND h-bill.segmentcode NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        IF h-bill.resnr GT 0 THEN
        DO:
            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN
            DO:
                CREATE t-segment.
                BUFFER-COPY segment TO t-segment.
            END.
        END.        
    END.
END.
