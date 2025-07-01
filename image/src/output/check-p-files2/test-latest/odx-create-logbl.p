DEFINE INPUT PARAMETER rechnr AS INT.
DEFINE INPUT PARAMETER dept AS INT.
DEFINE INPUT PARAMETER content AS CHAR.
DEFINE INPUT PARAMETER body AS LONGCHAR.
DEFINE INPUT PARAMETER response AS LONGCHAR.

CREATE queasy.
ASSIGN 
    queasy.KEY     = 242
    queasy.number1 = 99
    queasy.number2 = rechnr
    queasy.number3 = dept
    queasy.date1   = TODAY
    queasy.deci1   = TIME
    queasy.char1   = content
    queasy.char2   = body
    queasy.char3   = response.
