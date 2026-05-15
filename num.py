import numpy as np
months=np.array(["jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
sales=[]
print("Enter the sales (in $1000) for each month")
for month in months:
    value=float(input (f"{month}: "))
    sales.append(value)
    
sales= np.array(sales)
print("\n ---Company sales Analysis--")
print("Total sales of the year:",np.sum(sales), "$")
print("Average Monthly sales:", np.mean(sales), "$")
print("Highest sales:",np.max(sales), "$")
print("Lower sales", np.min(sales), "$")

best_month= months [np.argmax(sales)]
worst_month=months [np.argmin(sales)]

print ("Best Month:",best_month)
print("Worst Month:",worst_month)

above_avg= months[sales > np.mean(sales)]
below_avg= months[sales < np.mean(sales)]

print("Above Average Months:", above_avg)
print("Below Average Months:", below_avg)