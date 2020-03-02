import time
import pandas as pd
import numpy as np




CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july','august','september','october','november','december']

WEEKDAY_LIST = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday','all']

def convert(seconds): 
    """
    Converts seconds to days,hours, minutes, seconds 
    """
    minutes, sec = divmod(seconds, 60) 
    hour, minutes = divmod(minutes, 60) 
    days, hour = divmod(hour, 24)
    return int(days), int(hour), int(minutes), int(sec)


def chunker(iterable, size):
    """Yield successive chunks of specified size from provided iterable data set."""

    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]
        raw_display =  get_yes_no_input('Would you like to see raw data? Enter yes or no')
        if raw_display != 'yes':
               break

    
def get_yes_no_input(question):
    '''
    returns yes or no input from user for given question 

    '''
    answer_key = ['yes', 'no']
    while True:
            try:
                response =  input('\n'+ question + '.\n')
                response = response.lower()
                if response not in answer_key:
                  print("Not valid input. yes or no are the only valid values.")
                  continue
                else:
                  break
            except ValueError:
                print("Sorry, I didn't understand that. yes or no are the only valid values.")
                continue


    print("Your response is :", response)
    return   response
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Please enter city : chicago, new york city or washington: ")
        except ValueError:
            print("Sorry, I didn't understand that. chicago, new york city or washington are the only valid values.")
            continue

        if city.lower() not in CITY_DATA:
            print("Not valid input. chicago, new york city or washington are the only valid values")
            continue 
        else:
            break

    city=city.lower()
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please specify a  month like january, february or  all for no month filter: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if month.lower() not in MONTH_LIST:
            print("Not valid input. ")
            continue 
        else:
            break

    month=month.lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Please specify a  day like monday, tuesday or  all for no day filter: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if day.lower() not in WEEKDAY_LIST:
            print("Not valid input. ")
            continue 
        else:
            break

    day=day.lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # Although Month list if zero based we dont need to add 1 here because we made first element to be 'all'
        month = MONTH_LIST.index(month) 

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()



    # display the most common month
    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', MONTH_LIST[popular_month])


    # display the most common day of week
    # find the most popular week day
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day Of Week:', popular_day_of_week)


    # display the most common start hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # find the most popular start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start_station)


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end_station)


    # display most frequent combination of start station and end station trip
    #Create combination column of start and end station
    df['Start End Station'] = df['Start Station'] + " to " +  df['End Station']
    popular_start_end_station = df['Start End Station'].mode()[0]
    print('Most Common combination of start and End Station:', popular_start_end_station)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    days, hours, minutes, seconds = convert(total_duration)
    print('Total travel time {} seconds equivalent to {} days, {} hours, {} minutes and {} seconds.  '.format( total_duration, days, hours, minutes, seconds))


    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    days, hours, minutes, seconds = convert(mean_duration)
    print('Mean  travel time {}  seconds equivalend to {} days, {} hours, {} minutes and {} seconds. '.format( mean_duration,  days, hours, minutes, seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("******************************")
    print("Counts of User Type: ")
    print(df['User Type'].value_counts())


    # Display counts of gender
    print("******************************")
    print("Counts of Gender: ")
    if 'Gender' in df:
       print(df['Gender'].value_counts())
    else:
       print("Gender does not exist")


    # Display earliest, most recent, and most common year of birth
    print("******************************")
    print("Birth Year stats: ")
    if 'Birth Year' in df:
    #Eariest birth year
       print("******************************")
       print("Earliest Birth Year : ", int(df['Birth Year'].min()))
    #Recent birth year
       print("******************************")
       print("Recent Birth Year : ", int(df['Birth Year'].max()))
    #Common birth year
       print("******************************")
       print("Common Birth Year : ", int(df['Birth Year'].mode()[0]))
    else:
       print("Birth Year does not exist")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print("Processing data for city:{} month:{} and day:{} ".format(city, month, day))

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
    
        raw_display =  get_yes_no_input('Would you like to see raw data? Enter yes or no')
        if raw_display == 'yes':
            for chunk in  chunker(df, 5):
                print("\nDisplaying raw data:\n")
                pd.options.display.max_columns = None
                pd.options.display.width=None
                print(chunk)
                
                
                


        restart  =  get_yes_no_input('Would you like to restart with another city month day combination ? Enter yes or no')
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
