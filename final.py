import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

monthlist = ["1","2","3","4","5","6","all"]

daylist = ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n\nHello! Let\'s explore some US bikeshare data!\n')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    citylist = ["chicago", "new york city", "washington", "all"]
    city = input('Please tell us what city you would like to explore bikeshare data for? \n\nInput one of the following:\n -CHICAGO\n -NEW YORK CITY\n -WASHINGTON\n -ALL\n\n').lower()

    while city not in citylist:
        print("\n INVALID CITY, please input a valid city.\n")
        city = input('Please tell us what city you would like to explore bikeshare data for?\n').lower()
    print("\nYou selected city(s) " + city +".\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    monthlist = ["1","2","3","4","5","6","all"]
    month = input('\nWhat month of data from 1-6 (JAN-JUN) would you like to explore?  \n Input as a numeric # format IE: 3 for March or 1 for January OR "all". \n')

    while month not in monthlist:
            print("\n INVALID MONTH, please input a valid month using the first numeric # format")
            month = input('\n What month of data from 1-6 (JAN-JUN) would you like to explore?\n').lower()
    print("\nYou selected month(s) " + month +".\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    daylist = ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

    day = input('\nWhat day of the week would you like to investigate? (All, Monday, Tuesday ... Sunday) \n\n').lower()

    while day not in daylist:
            print("\n INVALID DAY, please input a valid day typed out \n")
            day = input('\n What day of the week would you like to investigate?\n').lower()
    print("\nYou selected day(s) " + day + ".\n")
    print("\nExporting data for:\n" + "  -Location: " + city + "\n"+ "  -Month: " + month + "\n" + "  -Day: " + day + "\n")
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
    if city.lower() != 'all':
        filename = CITY_DATA.get(city.lower(), None)
        df = pd.read_csv(filename)
    else:
        df = pd.concat([pd.read_csv(f) for f in CITY_DATA.values()], sort=False)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = monthlist.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    else:
        df = df

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        max_month = df['month'].mode()[0]
        print('Most Common Month:', max_month)
    else:
        month_counts = df['month'].value_counts().reset_index()
        if not month_counts.empty:
            max_month = month_counts.loc[month_counts['month'].idxmax(), 'index']
            print('Most Common Month:', max_month)
        else:
            print('No data available for the selected month.')

    # TO DO: display the most common day of week
    if day == 'all':
        max_day = df['day_of_week'].mode()[0]
        print('Most Common Day of Week:', max_day)
    else:
        day_counts = df['day_of_week'].value_counts().reset_index()
        max_day = day_counts.loc[day_counts['day_of_week'].idxmax(), 'index']
        print('Most Common Day of Week:', max_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    max_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', max_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start = df['Start Station'].value_counts().nlargest().index[0]
    print('Most Common Start Station: ',pop_start)


    # TO DO: display most commonly used end station
    pop_end = df['End Station'].value_counts().nlargest().index[0]
    print('Most Common End Station: ',pop_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start-End Combination'] = df['Start Station'] + ' TO ' + df['End Station']
    pop_combo = df['Start-End Combination'].value_counts().nlargest().index[0]
    print('Most Common Start-End Station Combination: ', pop_combo)

    # Remove the temporary column
    #df.drop('Start-End Combination', axis=1, inplace=True)

    print("\nThis took %s seconds:" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    Travel_Time_Sum = sum(df['Trip Duration'])
    print('Total Travel Time (seconds): ',Travel_Time_Sum)

    # TO DO: display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean Travel Time (seconds): ',Mean_Travel_Time)

    print("\nThis took %s seconds:" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts = df['User Type'].value_counts()
    Subscriber_Counts = counts['Subscriber']
    Customer_Count = counts['Customer']
    print("User Types \n Subscriber: ",Subscriber_Counts,'\n Customer: ',Customer_Count,'\n')

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        Male_counts = gender_counts['Male']
        Female_counts = gender_counts['Female']
        print("Gender Counts \n Male: ",Male_counts,'\n Female: ',Female_counts)

    else:
        print("Gender data not available for this dataset.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        Common = df['Birth Year'].value_counts().nlargest().index[0]
        print("\nMost common birth year: ",Common)

        oldest =  df['Birth Year'].min()
        print("Oldest birth year: ",oldest)

        newest =  df['Birth Year'].max()
        print("Newest birth year: ",newest)


    else:
        print("Birth Year data not available for this dataset.")

    print("\nThis took %s seconds:" % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        displaydata = input('\nWould you like to display the 5 rows of data? Enter yes or no.\n')
        if displaydata.lower() != 'no':
            start_loc = 0
            while True:
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
                view_data = input("Do you wish to continue?: ").lower()
                if view_data != 'yes':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
