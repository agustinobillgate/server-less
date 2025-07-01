
DEF INPUT PARAMETER bezeich AS CHAR.
DEF INPUT PARAMETER exrate  AS DECIMAL.
DEF INPUT PARAMETER amt     AS DECIMAL.

DEF OUTPUT PARAMETER art-exrate     AS DECIMAL.
DEF OUTPUT PARAMETER amount         AS DECIMAL.
DEF OUTPUT PARAMETER paid           AS DECIMAL.
DEF OUTPUT PARAMETER lpaid          AS DECIMAL.
DEF OUTPUT PARAMETER change         AS DECIMAL.
DEF OUTPUT PARAMETER lchange        AS DECIMAL.

FIND FIRST waehrung WHERE waehrung.wabkurz = bezeich NO-LOCK. 
ASSIGN 
    art-exrate = exrate 
    amount     = ROUND(amt / exrate, 2) 
    paid       = - amount 
    lpaid      = - amt 
    change     = 0 
    lchange    = 0 
  .
