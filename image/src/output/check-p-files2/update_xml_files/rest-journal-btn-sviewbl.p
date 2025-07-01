DEFINE buffer h-jou FOR h-journal. 

DEF INPUT PARAMETER h-recid AS INT.
DEF OUTPUT PARAMETER t-rechnr AS INT.
DEF OUTPUT PARAMETER t-departement AS INT.
DEF OUTPUT PARAMETER t-bill-datum AS DATE.

FIND FIRST h-jou WHERE RECID(h-jou) = h-recid NO-LOCK.
ASSIGN
t-rechnr = h-jou.rechnr
t-departement = h-jou.departement
t-bill-datum = h-jou.bill-datum.
