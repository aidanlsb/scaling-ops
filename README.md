# Scaling Operations Modeling

## How does the business work?
* The amount of waste to pick up is driven by the number of customers (lever) and the waste per customer (non-lever)
* This translates to a number of lifts that need to be performed
  * Number of lifts to perform translates to a number of shifts -> this is dictated by the business's efficiency
    * Lower LPS means more trucks, more labor, more fuel cost, etc. 
    * Performing these lifts at the lowest possible cost is the key operation for the business
* Once the lifts have been performed, they are disposed of, which incurs another cost based on the weight of the waste


* Revenue = Lifts * $/Lift
  * Lifts = lifts/shift * shifts
    * Shifts = days worked * shifts_per_day
    * lifts/shift = ?
  * $/Lift = $/volume * volume/lift
    * $/volume = ?
    * volume/lift = fixed

* Cost to serve = lifts * cost/lift
  * Lifts = lifts/shift * shifts
    * Shifts = days worked * shifts_per_day
    * lifts/shift = ?
  * cost/lift = driver_labor/lift + other_labor/lift + disposal/lift + fuel/lift + maintenance/lift + depreciation/lift
    * 
 