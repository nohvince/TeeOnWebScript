SCRIPT UI
========

Pick Date (auto selected to 6 days ahead since that's the day that becomes available next morning)

Pick preferred choice tee off time
	> 5am - 11:45pm 15min intervals

Select acceptable time range
	
18 or 9 holes

Party size (1-4 players)

Select courses (website allows multiple, but only allow one)
	> Courses are loaded based on area dropdown. Have Toronto and Area options hard coded or load via web call?
	> https://www.tee-on.com/PubGolf/servlet/com.teeon.teesheet.servlets.golfersection.WebBookingSearchSteps?CourseGroupID=12&BackTarget=/ CourseGroupID seems to load different area options, keep it at 12

Enter Name to reserve as

SCRIPT RUNTIME ACTIONS
=========

At 7:00AM ET Go to https://www.tee-on.com/PubGolf/servlet/com.teeon.teesheet.servlets.golfersection.WebBookingSearchSteps?CourseGroupID=12&BackTarget=/

Make selections

Screenshot selections on first screen

Click Next

Screenshot available times

Select time based on closest to preferred time within time range (pick one after if two same distance (custom comparator?))
	> Click Next for that time

Login and select Sign In

Set name and select Book Time

Screenshot confirmation

Exit

Retry logic (up to 3 attempts) for 1 min later if not available yet
	> <p class="title">Booking Too Soon</p> under <div class="search-results-tee-times-message double-wide DVGC-message-box">

TECH DETAILS
==========
Use kaggle / pythonanywhere accounts to have python script hosted that makes reservation using selenium

Send script that opens basic GUI for C to use to fill out form details. When submitted, makes api call to pythonanywhere Files and Schedule APIs to submit file w arguments for hosted script and to schedule the script for 7AM next day
	> https://help.pythonanywhere.com/pages/API/
