def add_time(start, duration, day=""):

    #our list of the days
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    #seperate hours, minutes, and period of the day
    start_time, period = start.split()
    start_hour, start_min = map(int, start_time.split(":"))
    duration_hour, duration_min = map(int, duration.split(":"))

    #verify that the minutes are correct
    if start_min >= 60 or duration_min >= 60:
        return "Error: Minutes should be less than 60"
    
    #convert to 24-hour format for easier calculations
    if period == "PM" and start_hour != 12:
        start_hour += 12
    if period == "AM" and start_hour == 12:
        start_hour = 0

    #define the new hours and minutes
    total_minutes = start_min + duration_min
    extra_hours = total_minutes // 60
    new_min = total_minutes % 60
    total_hours = start_hour + duration_hour + extra_hours
    new_hour = total_hours % 12

    #track the next days
    n = total_hours // 24
    
    #define the next day
    next=""
    new_day = ""

    if n == 1:
        next = " (next day)"
    elif n > 1:
        next = f" ({n} days later)"

    if day:
        day_index = weekdays.index(day.capitalize())  
        new_day = weekdays[(day_index + n) % 7]  
        new_day = f", {new_day}"

    #convert back to 12-hour format
    new_period = "AM" if (total_hours % 24) < 12 else "PM"
    new_hour = new_hour % 12 if new_hour % 12 != 0 else 12


    #put them together
    new_time = f"{new_hour}:{new_min:02d} {new_period}{new_day}{next}"

    return new_time
