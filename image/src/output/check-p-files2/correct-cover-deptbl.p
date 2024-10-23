
DEF INPUT PARAMETER dept1 AS INT.
DEF INPUT PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER deptname AS CHAR.
DEF OUTPUT PARAMETER fpax AS INT.
DEF OUTPUT PARAMETER bpax AS INT.
DEF OUTPUT PARAMETER pax AS INT.
DEF OUTPUT PARAMETER orig-fpax AS INT.
DEF OUTPUT PARAMETER orig-bpax AS INT.
DEF OUTPUT PARAMETER orig-pax AS INT.
DEF OUTPUT PARAMETER avail-h-umsatz AS LOGICAL INIT NO.
/*
DEFINE VARIABLE dept1 AS INT INIT 11.
DEFINE VARIABLE datum AS DATE INIT 12/11/23.
define variable dept as int.
define variable deptname as CHAR.
define variable fpax as int.
define variable bpax as int.
define variable pax as int.
define variable orig-fpax as int.
define variable orig-bpax as int.
define variable orig-pax as int.
define variable avail-h-umsatz as LOGICAL INIT NO.*/
DEFINE VARIABLE cover AS INT FORMAT "->>>9".

FIND FIRST hoteldpt WHERE hoteldpt.num = dept1 NO-LOCK.
ASSIGN
  dept = dept1
  deptname = hoteldpt.depart
.
ASSIGN fpax      = 0
       bpax      = 0
       pax       = 0
       orig-fpax = 0
       orig-bpax = 0
       orig-pax  = 0
.
FIND FIRST h-umsatz WHERE h-umsatz.datum = datum
    AND h-umsatz.departement = dept
    AND h-umsatz.betriebsnr = dept NO-LOCK NO-ERROR.
IF AVAILABLE h-umsatz THEN
DO: 
    avail-h-umsatz = YES.
    FOR EACH fbstat WHERE fbstat.datum EQ datum /*william F2F571 change cover value from h-umsatz to fbstat*/
        AND fbstat.departement EQ dept:
        cover = cover + fbstat.food-wpax[1] + fbstat.food-wpax[2] + fbstat.food-wpax[3] + fbstat.food-wpax[4]
            + fbstat.bev-wpax[1] + fbstat.bev-wpax[2] + fbstat.bev-wpax[3] + fbstat.bev-wpax[4] 
            + fbstat.other-wpax[1] + fbstat.other-wpax[2] + fbstat.other-wpax[3] + fbstat.other-wpax[4].
    END.
    ASSIGN
        pax  = cover
        fpax = h-umsatz.betrag
        bpax = h-umsatz.nettobetrag
        orig-fpax = fpax
        orig-bpax = bpax
        orig-pax  = pax
    .
END.

