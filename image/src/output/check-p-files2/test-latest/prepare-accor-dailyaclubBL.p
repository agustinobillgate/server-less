DEFINE OUTPUT PARAMETER bill-date     AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER price-decimal AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER foreign-rate  AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER rm-vat        AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER rm-serv       AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER serv-taxable  AS LOGICAL NO-UNDO.


FIND FIRST htparam WHERE paramnr = 110 NO-LOCK NO-ERROR.  
bill-date = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK NO-ERROR. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK NO-ERROR. 
foreign-rate = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR. 
rm-vat = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK NO-ERROR. 
rm-serv = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK NO-ERROR.
serv-taxable = htparam.flogical.
