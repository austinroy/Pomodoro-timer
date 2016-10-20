#### POMODORO TIMER
Repo will hold information about a Pomodoro Timer Project

To run the app install the virtual environment and `requirements.txt`

###What is a pomodoro timer??
This is a timer that alolows you to schedule breaks between your work for better efficiency in the task at hand. It counts time periods each with a default interval of 25 minutes but the interval can be adjusted.  
There is a short break between each cycle with a default time of 5 minutes but its adjustable  
After the third cycle the user is forced into a long break that has a default time 15 minutes but it is also adjustable  

This app is built use docopt command line framework which is similar to the unix command line.

To run this app input command `python main.py -i`

The pomodoro Timer application has the following commands:

     1. pomodoro start <task -title> which creates a new task to be implemented by the timer 
    `pomodoro create swim` 
     
     2. pomodoro config_time <duration-in-minutes> this command modifies the default duration time 
     `pomodoro config_time 5` sets an duration of 5 minutes 
    
     3. pomodoro config_shortbreak <duration-in-mnutes> 
     `pomodoro config_shortbreak 2` sets short break length to 2 minutes 

     4. pomodoro config_longbreak <duration-in-mnutes> 
    `pomodoro config_longbreak 3` sets the long break time to 3 minutes 

     5. pomodoro config_sound <on/off> Command sets the sound to either ring or not 
    `pomodoro config_sound*on` set sound on 

     6. pomodoro config_time <duration-in-mnutes> command set time from which the timer should start counting default time is now  
    `pomodoro timer*1:30:0` command sets to start the timer to start in 1hr and 30min  

   
     7. pomodoro pause\*<title> command moves a task that is in status active to status pending which means its timer has  been stopped temporarirly  
     `pomodoro pause run` 

     8. pomodoro stop\*<title> task is moved at status finished. At this status a task is considered permanently stopped or   its timer rang `pomodoro stop run`
    
     9. pomodoro list all This command list all the data in the database`listitems`

    10. pomodoro list <dd:mm:YYYY> This command Lists all task with the start time equal to the given parameter  
    `list 20-08-2016` lists all the tasks with the completion date as 20th October 2016  

    11. pomodoro delete <dd:mm:YYYY> Deletes all the tasks done on a particular day
    `clear 20:10:2016` deletes all tasks done on 20th October 2016

__To do List__
  *Implement command 7 -will require deeper understanding of multithreading
  *Implement command 8 -will require deeper understanding of multithreading
  *Implement command 11
  *add bell


