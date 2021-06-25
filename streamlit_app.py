import pandas as pd
import streamlit as st


# List of users
user_list = {
    '---':    -1,
    'Melissa':  1,
    'Hasan':    2,
    'Megan':    3,
    'Brian':    5,
}


# Show title and dropdown list of names
st.title('Movie Recommender')
name = st.selectbox(
    'Choose a user to look at:',
    [name for name in user_list.keys()])


# Only run if actual name is chosen
if name != '---':
    user_id = user_list[name]


    # Read user data from file
    user_data = pd.read_csv('data.csv')


    # Create pivot table of users vs movie titles; each cell is the rating given to that movie by that user
    movie_user_rating = user_data.pivot_table(index='title', columns='userId', values='rating')


    # Get all ratings for our chosen user
    chosen_user_ratings = movie_user_rating[user_id]


    # Correlate with other users i.e. with similar pattern of movie ratings
    similar_users = movie_user_rating.corrwith(chosen_user_ratings)


    # Don't include our chosen user in the results
    similar_users.drop(similar_users[similar_users.index==user_id], inplace=True)


    # Put the similarity scores in a table
    corr_users = pd.DataFrame(similar_users, columns=['Correlation'])
    corr_users.dropna(inplace=True)


    # Get top 5 users by correlation
    matched_users = pd.DataFrame(corr_users.sort_values('Correlation', ascending=False))
    top_five = list(matched_users.index[:5])


    # Get top rated movies from matched users, sorted by popularity (rating count)
    recommendations = user_data[user_data['userId'].isin(top_five)].sort_values(by='rating_counts', ascending=False).sort_values(by='rating', ascending=False)


    # Filter movies user has already watched from the recommendations
    already_watched = list(chosen_user_ratings.dropna().index)
    filtered_recs = recommendations[recommendations['title'].isin(already_watched)==False]


    # Show output to user
    st.header('This user matched with:')
    st.table(pd.Series(user_data[user_data.userId.isin(top_five)].name.unique(), name='Name'))

    st.header('Recommended movies are:')
    st.table(filtered_recs[['title', 'rating']][:10])