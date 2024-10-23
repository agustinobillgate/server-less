
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER comments       AS CHAR.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */

RUN init-display.

PROCEDURE init-display:
  IF AVAILABLE l-kredit THEN comments = l-kredit.bemerk. 
  ELSE comments = "". 
END. 
