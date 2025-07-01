DEFINE TEMP-TABLE hj-buff LIKE h-journal
    FIELD rec-id AS INT.

DEF INPUT PARAMETER rechNo AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR hj-buff.

FOR EACH h-journal WHERE h-journal.rechnr = rechNo 
    AND h-journal.departement = dept
    AND h-journal.bill-datum = billdate NO-LOCK 
    BY h-journal.sysdate BY h-journal.zeit:
    CREATE hj-buff.
    BUFFER-COPY h-journal TO hj-buff.
    ASSIGN hj-buff.rec-id = RECID(h-journal).
END.
