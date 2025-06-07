import sys
import math
from datetime import datetime

def calculate_reimbursement(days, miles, receipts):
    try:
        days = int(float(days))
        miles = float(miles)
        receipts = float(receipts)
    except:
        return 0.00
    
    total = 252.17 + (50.40 * days) + (0.47 * miles) + (0.39 * receipts)
    
    return total

# Get command line arguments
days = sys.argv[1]
miles = sys.argv[2]
receipts = sys.argv[3]

# Calculate and print result
print(calculate_reimbursement(days, miles, receipts))