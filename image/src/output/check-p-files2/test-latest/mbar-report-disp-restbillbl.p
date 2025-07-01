DEF TEMP-TABLE t-h-journal LIKE h-journal.

DEF INPUT PARAMETER billno AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-h-journal.

FOR EACH h-journal WHERE h-journal.rechnr = billno 
    AND h-journal.departement = dept 
    AND h-journal.bill-datum = datum NO-LOCK 
    BY h-journal.sysdate BY h-journal.zeit:
    CREATE t-h-journal.
    BUFFER-COPY h-journal TO t-h-journal.
END.
