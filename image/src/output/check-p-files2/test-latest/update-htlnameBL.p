

DEF INPUT PARAMETER htl-name  AS CHAR.
DEF INPUT PARAMETER htl-adr1  AS CHAR.
DEF INPUT PARAMETER htl-adr2  AS CHAR.
DEF INPUT PARAMETER htl-adr3  AS CHAR.
DEF INPUT PARAMETER htl-tel   AS CHAR.
DEF INPUT PARAMETER htl-fax   AS CHAR.
DEF INPUT PARAMETER htl-email AS CHAR.

RUN update-it.

PROCEDURE update-it: 
  FIND FIRST paramtext WHERE txtnr = 200 . 
  paramtext.ptexte = htl-name. 
  FIND FIRST paramtext WHERE txtnr = 201 . 
  paramtext.ptexte = htl-adr1. 
  FIND FIRST paramtext WHERE txtnr = 202 . 
  paramtext.ptexte = htl-adr2. 
  FIND FIRST paramtext WHERE txtnr = 203 . 
  paramtext.ptexte = htl-adr3. 
  FIND FIRST paramtext WHERE txtnr = 204 . 
  paramtext.ptexte = htl-tel. 
  FIND FIRST paramtext WHERE txtnr = 205 . 
  paramtext.ptexte = htl-fax. 
  FIND FIRST paramtext WHERE txtnr = 206 . 
  paramtext.ptexte = htl-email. 
END. 
