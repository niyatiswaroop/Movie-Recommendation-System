from recommender import recommend

movie_name = input("Enter movie name: ")

results = recommend(movie_name)

print("\nRecommended Movies:\n")

for movie in results:
    print(movie)