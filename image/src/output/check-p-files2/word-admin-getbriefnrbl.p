
DEF OUTPUT PARAMETER briefnr AS INT INIT 0.

DEFINE buffer brief1 FOR brief.

FOR EACH brief1 NO-LOCK BY brief1.briefnr DESCENDING: 
    briefnr = briefnr + brief1.briefnr.
    LEAVE.
END. 
briefnr = briefnr + 1.
