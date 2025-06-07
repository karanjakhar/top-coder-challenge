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
    
    # Base daily rates with degressive scaling
    if days == 1:
        base = 45.0
    elif days == 2:
        base = 55.0 * days
    elif days == 3:
        base = 70.0 * days 
    elif days == 4:
        base = 85.0 * days
    elif days == 5:  # Special bonus for 5-day trips
        base = 100.0 * days * 1.1  # 10% bonus
    elif 6 <= days <= 7:
        base = 90.0 * days
    elif 8 <= days <= 12:
        base = 80.0 * days
    else:  # 13+ days
        base = 70.0 * days
    
    # Mileage component with efficiency bonuses
    miles_per_day = miles / days
    if miles_per_day < 50:
        mileage_rate = 0.35
    elif 50 <= miles_per_day < 100:
        mileage_rate = 0.45
    elif 100 <= miles_per_day < 180:  # Sweet spot range
        mileage_rate = 0.55
    elif 180 <= miles_per_day < 220:  # Peak efficiency bonus
        mileage_rate = 0.60
    elif 220 <= miles_per_day < 400:
        mileage_rate = 0.50
    else:  # Very high mileage (possible penalty)
        mileage_rate = 0.40
    
    mileage_comp = miles * mileage_rate
    
    # Receipts component with progressive scaling
    if receipts <= 25:
        if days > 1:  # Penalty for small receipts on multi-day trips
            receipts_comp = receipts * 0.5
        else:
            receipts_comp = receipts * 0.7
    elif 25 < receipts <= 100:
        receipts_comp = 12.5 + (receipts - 25) * 0.8
    elif 100 < receipts <= 500:
        receipts_comp = 75 + (receipts - 100) * 0.6
    else:
        receipts_comp = 315 + (receipts - 500) * 0.4
    
    # Interaction adjustments
    # High receipts on long trips get penalized
    if days >= 5 and receipts > 300:
        receipts_comp *= 0.85
    
    # Very high mileage on short trips gets penalized
    if miles > 400 and days < 4:
        mileage_comp *= 0.85
    
    # Special 1-day trip high mileage penalty
    if days == 1 and miles > 500:
        base *= 0.8
    
    # Efficiency bonus for optimal miles/day
    if 180 <= miles_per_day < 220:
        base *= 1.05
    
    # Combine components
    total = base + mileage_comp + receipts_comp
    
    # Seasonal adjustments (based on month)
    current_month = datetime.now().month
    if current_month in [3, 6, 9, 12]:  # End of quarter
        total *= 1.03
    
    # Day-of-week effect (Tuesday bonus)
    if datetime.now().weekday() == 1:  # Tuesday
        total *= 1.02
    
    # Special rounding rules
    total = round(total * 4) / 4  # Round to nearest 0.25
    
    # Favorable rounding for certain receipt endings
    if receipts > 0 and (str(receipts).endswith('49') or str(receipts).endswith('99')):
        total += 0.11
    
    # Final cleanup rounding
    total = round(total, 2)
    
    # Ensure minimum reimbursement
    if total < 50 * days:
        total = 50 * days
    
    return total

# Get command line arguments
days = sys.argv[1]
miles = sys.argv[2]
receipts = sys.argv[3]

# Calculate and print result
print(calculate_reimbursement(days, miles, receipts))