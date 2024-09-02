DEFINE INPUT PARAMETER roomnumber AS CHAR.
DEFINE INPUT PARAMETER userinit   AS CHAR.

DEFINE VARIABLE sysdate AS DATE.

FIND FIRST htparam WHERE paramnr = 87.
sysdate = DATE(MONTH(htparam.fdate), DAY(htparam.fdate), YEAR(htparam.fdate)).

/* Delete Temp-OutOrder where Datum = sysdate First
FOR EACH queasy WHERE queasy.date1 = sysdate AND queasy.KEY=900.
    DELETE queasy.
END.
*/

FOR EACH outorder WHERE outorder.zinr EQ roomnumber 
    AND sysdate GE outorder.gespstart 
    AND sysdate LE outorder.gespende 
    AND outorder.betriebsnr NE 2 NO-LOCK:
    FIND FIRST zimmer WHERE outorder.zinr = zimmer.zinr NO-ERROR.

    CREATE queasy.
    ASSIGN queasy.KEY = 900
           queasy.number1 = zimmer.zikatnr
           queasy.char1 = outorder.zinr
           queasy.char2 = outorder.gespgrund
           queasy.char3 = userinit
           queasy.date1 = sysdate
           queasy.date2 = outorder.gespstart
           queasy.date3 = outorder.gespende.
END.
