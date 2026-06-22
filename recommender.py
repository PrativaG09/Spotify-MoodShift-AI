import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


def create_recommendation_model(df):

    features = [
        "danceability",
        "energy",
        "valence",
        "acousticness",
        "instrumentalness",
        "liveness",
        "speechiness",
        "tempo"
    ]

    data = df[features]

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(data)


    model = NearestNeighbors(
        n_neighbors=10,
        metric="cosine"
    )

    model.fit(scaled_features)


    return model, scaler



def recommend_tracks(
        track_index,
        df,
        model,
        scaler
):

    features = [
        "danceability",
        "energy",
        "valence",
        "acousticness",
        "instrumentalness",
        "liveness",
        "speechiness",
        "tempo"
    ]


    track_features = df.loc[
        [track_index],
        features
    ]


    scaled_track = scaler.transform(
        track_features
    )


    distances, indices = model.kneighbors(
        scaled_track
    )
    similarity_score = (
    1 - distances[0]
) * 100

    recommendations = df.iloc[
        indices[0]
    ]

    recommendations = recommendations[
        recommendations["track_id"] != df.loc[track_index, "track_id"]
    ]

    recommendations = recommendations[
        ["track_name", "artists", "popularity"]
    ].head(10)

    return recommendations


if __name__ == "__main__":

    df = pd.read_csv("dataset.csv")

    model, scaler = create_recommendation_model(df)

    recommendations = recommend_tracks(
        0,
        df,
        model,
        scaler
    )

    print(recommendations)