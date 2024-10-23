DEFINE TEMP-TABLE t-argtline-rate
    FIELD argt-artnr        LIKE argt-line.argt-artnr
    FIELD bezeich           LIKE artikel.bezeich
    FIELD deci1             LIKE reslin-queasy.deci1
    FIELD deci2             LIKE reslin-queasy.deci2
    FIELD deci3             LIKE reslin-queasy.deci3
    FIELD date1             LIKE reslin-queasy.date1
    FIELD date2             LIKE reslin-queasy.date2
    FIELD departement       LIKE argt-line.departement
    FIELD fakt-modus        LIKE argt-line.fakt-modus
    
    FIELD KEY               LIKE reslin-queasy.KEY
    FIELD char1             LIKE reslin-queasy.char1
    FIELD number1           LIKE reslin-queasy.number1
    FIELD number2           LIKE reslin-queasy.number2
    FIELD number3           LIKE reslin-queasy.number3
    FIELD resnr             LIKE reslin-queasy.resnr
    FIELD reslinnr          LIKE reslin-queasy.reslinnr
    FIELD artnr             LIKE artikel.artnr
    FIELD s-recid           AS INTEGER
    .

DEFINE INPUT PARAMETER prcode       AS CHAR.
DEFINE INPUT PARAMETER marknr       AS INT.
DEFINE INPUT PARAMETER argtnr       AS INT.
DEFINE INPUT PARAMETER zikatnr      AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-argtline-rate.


FOR EACH reslin-queasy WHERE key = "argt-line" 
    AND reslin-queasy.char1 = prcode 
    AND reslin-queasy.number1 = marknr 
    AND reslin-queasy.number2 =  argtnr 
    AND reslin-queasy.reslinnr = zikatnr NO-LOCK, 
    FIRST argt-line WHERE argt-line.argtnr = reslin-queasy.number2 
    AND argt-line.argt-artnr = reslin-queasy.number3 
    AND argt-line.departement = reslin-queasy.resnr NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = reslin-queasy.reslinnr NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
    AND artikel.departement = argt-line.departement NO-LOCK 
    BY argt-line.argt-artnr BY reslin-queasy.date1 :
    CREATE t-argtline-rate.
    ASSIGN  t-argtline-rate.argt-artnr        = argt-line.argt-artnr
            t-argtline-rate.bezeich           = artikel.bezeich
            t-argtline-rate.deci1             = reslin-queasy.deci1
            t-argtline-rate.deci2             = reslin-queasy.deci2
            t-argtline-rate.deci3             = reslin-queasy.deci3
            t-argtline-rate.date1             = reslin-queasy.date1
            t-argtline-rate.date2             = reslin-queasy.date2
            t-argtline-rate.departement       = argt-line.departement
            t-argtline-rate.fakt-modus        = argt-line.fakt-modus
            
            t-argtline-rate.KEY               = reslin-queasy.KEY
            t-argtline-rate.char1             = reslin-queasy.char1
            t-argtline-rate.number1           = reslin-queasy.number1
            t-argtline-rate.number2           = reslin-queasy.number2
            t-argtline-rate.number3           = reslin-queasy.number3
            t-argtline-rate.resnr             = reslin-queasy.resnr
            t-argtline-rate.reslinnr          = reslin-queasy.reslinnr
            t-argtline-rate.artnr             = artikel.artnr
            t-argtline-rate.s-recid           = RECID(argt-line)
            .
END.
