DEFINE TEMP-TABLE outlet-transaction
    FIELD trans-date AS DATE
    FIELD department AS INT FORMAT ">>>"
    FIELD waiter-name AS CHAR FORMAT "x(30)"
    FIELD table-no AS INT FORMAT ">>>"
    FIELD bill-no AS INT FORMAT ">>>>>>"
    FIELD guest-name AS CHAR FORMAT "x(30)"
    FIELD pax AS INT FORMAT ">>>"
    FIELD total-amount AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    .

DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR outlet-transaction.

/*
DEFINE VARIABLE from-date AS DATE INIT 01/01/19.
DEFINE VARIABLE to-date AS DATE INIT 01/31/19.
*/
DEF VAR curr-dept AS INT INIT 1.
DEF VAR waiter AS CHAR.

FOR EACH h-bill WHERE h-bill.saldo NE 0 
    AND h-bill.departement EQ curr-dept  
    NO-LOCK USE-INDEX dept1_ix BY h-bill.rechnr: 
    FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr 
    AND h-bill-line.bill-datum GE from-date
    AND h-bill-line.bill-datum LE to-date
    AND h-bill-line.departement EQ curr-dept USE-INDEX bildat_index NO-LOCK NO-ERROR.  
    IF AVAILABLE h-bill-line THEN
    DO:
        FIND FIRST kellner WHERE kellner.kellner-nr = h-bill.kellner-nr NO-LOCK NO-ERROR. 
        IF AVAILABLE kellner THEN waiter = kellner.kellnername.

        CREATE outlet-transaction. 
        ASSIGN
            outlet-transaction.trans-date = h-bill-line.bill-datum
            outlet-transaction.department = curr-dept 
            outlet-transaction.waiter-name = waiter 
            outlet-transaction.table-no = h-bill.tischnr
            outlet-transaction.bill-no = h-bill.rechnr 
            outlet-transaction.guest-name = h-bill.bilname
            outlet-transaction.pax = h-bill.belegung
            outlet-transaction.total-amount = h-bill.saldo
            .
    END.
END.
/*
CURRENT-WINDOW:WIDTH = 140.
FOR EACH outlet-transaction:
    DISP outlet-transaction WITH WIDTH 140.
END.
*/
