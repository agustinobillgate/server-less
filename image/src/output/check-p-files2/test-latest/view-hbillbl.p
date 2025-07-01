DEF TEMP-TABLE t-h-journal 
    FIELD artnr         LIKE h-journal.artnr
    FIELD bezeich       LIKE h-journal.bezeich
    FIELD anzahl        LIKE h-journal.anzahl
    FIELD epreis        LIKE h-journal.epreis
    FIELD betrag        LIKE h-journal.betrag
    FIELD rechnr        LIKE h-journal.rechnr
    FIELD departement   LIKE h-journal.departement
    FIELD bill-datum    LIKE h-journal.bill-datum
    FIELD sysdate       LIKE h-journal.sysdate
    FIELD zeit          LIKE h-journal.zeit
    FIELD rec-id        AS INTEGER
    .

DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER inp-rechnr AS INT.
DEF INPUT PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER depart AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-journal.

FIND FIRST hoteldpt WHERE hoteldpt.num = dept NO-LOCK. 
depart = hoteldpt.depart.
FOR EACH h-journal WHERE h-journal.rechnr = inp-rechnr 
    AND h-journal.departement = dept AND h-journal.bill-datum = datum 
    NO-LOCK BY h-journal.sysdate BY h-journal.zeit:
    CREATE t-h-journal.
    ASSIGN
    t-h-journal.artnr         = h-journal.artnr
    t-h-journal.bezeich       = h-journal.bezeich
    t-h-journal.anzahl        = h-journal.anzahl
    t-h-journal.epreis        = h-journal.epreis
    t-h-journal.betrag        = h-journal.betrag
    t-h-journal.rechnr        = h-journal.rechnr
    t-h-journal.departement   = h-journal.departement
    t-h-journal.bill-datum    = h-journal.bill-datum
    t-h-journal.sysdate       = h-journal.sysdate
    t-h-journal.zeit          = h-journal.zeit
    t-h-journal.rec-id        = RECID(h-journal)   
    .
END.
