
DEF INPUT PARAMETER bk-veran-veran-nr AS INT.
DEF OUTPUT PARAMETER avail-reser-buff AS LOGICAL INIT NO.

DEF BUFFER reser-buff FOR bk-reser.

FIND FIRST reser-buff WHERE reser-buff.veran-nr = bk-veran-veran-nr
    AND reser-buff.resstatus EQ 1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE reser-buff THEN
DO:
    avail-reser-buff = YES.
    /*MT
    HIDE MESSAGE NO-PAUSE.
    MESSAGE translateExtended ("Banquet bill for GUARANTED reservation only.",lvCAREA,"")
      VIEW-AS ALERT-BOX INFORMATION.
    */
    RETURN NO-APPLY.
END.
/*MT
HIDE MESSAGE NO-PAUSE. 
MESSAGE translateExtended ("Do you want to create the Banquet Bill now?",lvCAREA,"") 
    VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
IF answer THEN RUN create-banquet-bill. 
*/
