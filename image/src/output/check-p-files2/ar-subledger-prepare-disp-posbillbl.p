
DEF TEMP-TABLE t-h-journal LIKE h-journal.

DEF INPUT  PARAMETER a-rechnr AS INT.
DEF INPUT  PARAMETER a-dept AS INT.
DEF INPUT  PARAMETER a-rid AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-journal.

DEFINE BUFFER ar-buff FOR debitor.

FIND FIRST ar-buff WHERE RECID(ar-buff) = a-rid NO-LOCK.
FOR EACH h-journal WHERE h-journal.bill-datum EQ ar-buff.rgdatum AND
    h-journal.rechnr = a-rechnr AND 
    h-journal.departement = a-dept NO-LOCK :
    CREATE t-h-journal.
    BUFFER-COPY h-journal TO t-h-journal.
END.
