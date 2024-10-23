
DEF INPUT PARAMETER resnr AS INT.
DEF OUTPUT PARAMETER bq-rechnr AS INT.

DEF BUFFER bk-main FOR bk-veran. 
DEF BUFFER gast FOR guest. 
DEF BUFFER b-dept FOR htparam. 

FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK. 
FIND FIRST b-dept WHERE b-dept.paramnr = 900 NO-LOCK. 
FIND FIRST bk-main WHERE bk-main.veran-nr = bk-veran.veran-nr EXCLUSIVE-LOCK. 
FIND FIRST gast WHERE gast.gastnr = bk-main.gastnrver NO-LOCK. 
FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
counters.counter = counters.counter + 1. 
FIND CURRENT counter NO-LOCK. 
CREATE bill. 
ASSIGN 
    bill.gastnr = gast.gastnr 
    bill.billtyp = b-dept.finteger 
    bill.name = gast.name + ", " + gast.vorname1 + gast.anredefirma 
      + " " + gast.vorname1 
    bill.reslinnr = 1 
    bill.rgdruck = 1 
    bill.rechnr = counters.counter 
    . 
bk-main.rechnr = bill.rechnr. 
FIND CURRENT bk-main NO-LOCK. 
FIND CURRENT bill NO-LOCK. 
bq-rechnr = bill.rechnr. 
