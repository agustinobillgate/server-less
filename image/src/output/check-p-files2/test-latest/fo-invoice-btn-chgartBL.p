
DEF INPUT  PARAMETER new-dept       AS INT.
DEF OUTPUT PARAMETER hotel-depart   AS CHAR.

FIND FIRST hoteldpt WHERE hoteldpt.num = new-dept NO-LOCK. 
hotel-depart = hoteldpt.depart.

