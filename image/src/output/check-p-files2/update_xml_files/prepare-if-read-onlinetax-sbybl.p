DEFINE OUTPUT PARAMETER hname AS CHAR NO-UNDO.

FIND FIRST paramtext WHERE txtnr = 200 NO-ERROR. 
hname = paramtext.ptexte. 
