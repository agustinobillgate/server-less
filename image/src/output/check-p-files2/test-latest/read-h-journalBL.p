DEF TEMP-TABLE t-h-journal LIKE h-journal.

DEF INPUT PARAMETER case-type   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER billNo      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER artNo       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER dept        AS INTEGER NO-UNDO.
DEF INPUT PARAMETER datum       AS DATE    NO-UNDO.
DEF INPUT PARAMETER waehrungNo  AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-h-journal.

IF NOT CONNECTED("vhp") THEN RETURN.

CASE case-type :
    WHEN 1 THEN
    FOR EACH h-journal WHERE h-journal.rechnr = billNo
        AND h-journal.departement = dept 
        AND h-journal.bill-datum = datum NO-LOCK 
        BY h-journal.sysdate BY h-journal.zeit:
        CREATE t-h-journal.
        BUFFER-COPY h-journal TO t-h-journal.
    END.
    WHEN 2 THEN
    FOR EACH h-journal WHERE h-journal.rechnr = billNo
        AND h-journal.departement = dept 
        AND h-journal.bill-datum = datum 
        AND h-journal.waehrungsnr = waehrungNo NO-LOCK :
        CREATE t-h-journal.
        BUFFER-COPY h-journal TO t-h-journal.
    END.

END CASE.
