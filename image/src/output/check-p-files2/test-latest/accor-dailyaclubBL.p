DEFINE TEMP-TABLE aclub-daily LIKE mc-aclub
    FIELD count-no AS INTEGER.

DEFINE INPUT PARAMETER fdate AS DATE NO-UNDO.
DEFINE INPUT PARAMETER tdate AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR aclub-daily.

DEFINE VARIABLE nomor AS INTEGER INIT 0.


FOR EACH mc-aclub WHERE mc-aclub.billdatum GE fdate AND mc-aclub.billdatum LE tdate 
    AND (mc-aclub.KEY = 2 OR mc-aclub.KEY = 1) NO-LOCK:
    CREATE aclub-daily.
    BUFFER-COPY mc-aclub TO aclub-daily.
    ASSIGN 
        nomor                = nomor + 1
        aclub-daily.count-no = nomor.
END.
