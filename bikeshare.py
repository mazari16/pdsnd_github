
import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    cities = ['chicago', 'new york city', 'washington']
    city = input('Which city would you like to select?').lower()
    while city not in cities:
        print('Sorry, the input must be: chicago, new york city or washington')
        city = input(
            'Which city would you like to select: chicago,new york city or washington?\n'
        )
    # get user input for month (all, january, february, ... , june)
    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = input('Which month ? ').lower()
    while month not in months.keys():
        print(
            'Sorry, the day must be:all,January, February, March, April, May, or June'
        )
        month = input(
            'Which month would you like to select? '
        ).lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)
    days = [
        'all',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ]
    day = input('Which day ? ').lower()
    while day not in days:
        print(
            'Sorry, the day must be:Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday'
        )
        day = input("Which day ? ").lower()

    print('-' * 40)
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
    # same as practice 3
    # loading the data into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converting the Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

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
    common_month = df['month'].mode()[0]
    print('The most common month is:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of week is:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print('The most common start station is:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['common trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    common_trip = df['common trip'].mode()[0]
    print("The most common trip is: from ", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('the mean Travel Time was:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types as in practice 2
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('No gender in the data')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print("The earliest Year is:", earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('The most Recent Year is:', most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Year is:', most_common_year)
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print('No Birth Year in the data')


def raw_data(df):
    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no?')
    if view_data.lower() == 'yes':
        start_loc = 0
        while True:
            print(df.iloc[start_loc: start_loc + 5])
            start_loc += 5
            view_display = input("Do you wish to continue?: ").lower()
            if view_display.lower() != 'yes':
                break


# noinspection PyTypeChecker
def main() -> object:
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()