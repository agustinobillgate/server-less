DEFINE TEMP-TABLE payment-list
    FIELD paymentDate       AS DATE
    FIELD invoiceNumber     AS CHAR
    FIELD depositAmount     AS DECIMAL
    FIELD paymentAmount     AS DECIMAL
    FIELD chgDate           AS DATE
    FIELD chgTime           AS CHAR
    FIELD userinit          AS CHAR
 .

DEFINE INPUT PARAMETER reservationId  AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR payment-list.


 FOR EACH queasy WHERE queasy.KEY = 312
     AND queasy.number1 = reservationId NO-LOCK:

     CREATE payment-list.
     ASSIGN payment-list.paymentDate    = queasy.date2
            payment-list.invoiceNumber  = queasy.char1
            payment-list.depositAmount  = queasy.deci1
            payment-list.paymentAmount  = queasy.deci2
            payment-list.chgDate        = queasy.date1
            payment-list.chgTime        = STRING(queasy.number2, "HH:MM:SS")
            payment-list.userinit       = queasy.char3            
         .
 END.


