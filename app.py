import streamlit as st
import pandas as pd
import plotly.express as px

from recommender import (
    create_recommendation_model,
    recommend_tracks
)

st.set_page_config(
    page_title="Spotify MoodShift AI",
    page_icon="🎧",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #121212;
}

section[data-testid="stSidebar"] {
    background-color: #181818;
}

h1, h2, h3, h4 {
    color: white;
}
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(29,185,84,0.15),
        rgba(29,185,84,0.05)
    );
    border: 1px solid rgba(29,185,84,0.25);
    border-radius: 15px;
    padding: 20px;
}

[data-testid="stMetricValue"] {
    font-size: 3rem;
    color: #5EF38C;
}

[data-testid="stMetricLabel"] {
    font-size: 1.1rem;
}
[data-testid="stDataFrame"] {
    border:1px solid rgba(29,185,84,0.15);
    border-radius:10px;
}

div[data-testid="metric-container"] {
    background: linear-gradient(
        135deg,
        rgba(29,185,84,0.15),
        rgba(29,185,84,0.05)
    );
    border: 1px solid rgba(29,185,84,0.25);
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 0 12px rgba(29,185,84,0.15);
}

</style>
""", unsafe_allow_html=True)
# Load Dataset
df = pd.read_csv("dataset.csv")

model, scaler = create_recommendation_model(df)
# Sidebar Filter
st.sidebar.title("🎧 Filters")

genre = st.sidebar.selectbox(
    "Select Genre",
    sorted(df["track_genre"].unique())
)

filtered_df = df[df["track_genre"] == genre]

st.markdown("""
<div style="
    background: linear-gradient(90deg,#0f3d1f,#121212);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
">
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='color:#1DB954; text-align:center;'>🎧 Spotify MoodShift AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='color:white; text-align:center;'>Discover the mood behind your music</h4>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#B3B3B3; text-align:center;'>Analyze Spotify tracks using audio intelligence, explore music patterns, and discover songs that match your vibe.</p>",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

col1, col2, col3, col4 = st.columns(4)

def metric_card(title, value):
    st.markdown(
        f"""
        <div style="
    background: linear-gradient(
    135deg,
    rgba(29,185,84,0.15),
    rgba(29,185,84,0.05)
);
padding:20px;
border-radius:15px;
text-align:center;
border:1px solid rgba(29,185,84,0.25);
box-shadow:0 0 12px rgba(29,185,84,0.15);
">
            <<p style="
    color:#9CC3AE;
    margin:0;
    font-size:20px;
    font-weight:500;
">
                {title}
            </p>

            <div style="
    color:#5EF38C;
    font-size:60px;
    font-weight:700;
    margin-top:15px;
">
    {value}
</div>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success(f"🎵 Total Tracks\n\n# {len(filtered_df):,}")

with col2:
    st.success(f"🎤 Artists\n\n# {filtered_df['artists'].nunique():,}")

with col3:
    st.success(
        f"🔥 Avg Popularity\n\n# {round(filtered_df['popularity'].mean(),1)}"
    )

with col4:
    st.success(
        f"🎼 Genres\n\n# {df['track_genre'].nunique():,}"
    )

st.info(
    f"Showing recommendations for genre: {genre}. "
    f"Tracks are filtered using popularity and audio features."
)

st.divider()

st.markdown("""
<div style="
background:linear-gradient(
135deg,
rgba(6,182,212,0.15),
rgba(6,182,212,0.05)
);
padding:15px;
border-radius:15px;
border:1px solid rgba(6,182,212,0.25);
margin-bottom:15px;
">
<h3 style="
color:#22D3EE;
font-size:30px;
font-weight:700;
">
📊 Music Analytics
</h3>
</div>
""", unsafe_allow_html=True)

chart1, chart2 = st.columns(2)

fig = px.scatter(
    filtered_df,
    x="danceability",
    y="energy",
    color="popularity",
    color_continuous_scale=[
        "#1DB954",  # Spotify green
        "#1ED760",
        "#53E88B",
        "#A8F0C6"
    ],
    hover_data=["track_name", "artists"],
    title="Energy vs Danceability"
)
fig.update_layout(
    coloraxis_colorbar=dict(
        title="Popularity"
    )
)
fig2 = px.histogram(
    filtered_df,
    x="popularity",
    nbins=30,
    title="Popularity Distribution",
    color_discrete_sequence=["#1DB954"]
)
fig2.update_traces(
    marker_color="#1DB954"
)
with chart1:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

with chart2:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )
st.divider()

filtered_df["mood"] = filtered_df.apply(
    lambda x:
    "Happy"
    if x["valence"] > 0.6 and x["energy"] > 0.6
    else (
        "Calm"
        if x["energy"] < 0.4
        else "Balanced"
    ),
    axis=1
)

mood_counts = filtered_df["mood"].value_counts()

fig3 = px.pie(
    values=mood_counts.values,
    names=mood_counts.index,
    hole=0.2      # optional, gives a modern donut style
)

fig3.update_layout(
    height=600,
    width=600,
    legend=dict(
        orientation="v",
        y=0.5
    )
)
fig3 = px.pie(
    values=mood_counts.values,
    names=mood_counts.index,
    color_discrete_sequence=[
        "#1DB954",  # Spotify green
        "#1ED760",
        "#0B8457"
    ]
)

fig3.update_traces(
    textinfo="percent+label"
)

fig3.update_layout(height=600)

# Mood chart will be displayed later in the dashboard layout
st.divider()

corr = filtered_df[
    [
        "danceability",
        "energy",
        "valence",
        "acousticness",
        "popularity"
    ]
].corr()

fig_corr = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    title="Feature Correlation",
    color_continuous_scale=[
        "#06110A",
        "#0B2E13",
        "#145A32",
        "#1DB954",
        "#A8F0C6"
    ]
)

fig_corr.update_layout(
    height=600,
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

top_artists = (
    filtered_df["artists"]
    .value_counts()
    .head(10)
)


fig_artist = px.bar(
    x=top_artists.values,
    y=top_artists.index,
    orientation="h",
    color_discrete_sequence=["#1DB954"]
)

fig_artist.update_layout(
    height=600,
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white",
    yaxis_title="Artist",
    xaxis_title="Number of Tracks"
)

st.markdown("""
<div style="
background:linear-gradient(
135deg,
rgba(14,165,233,0.15),
rgba(14,165,233,0.05)
);
padding:20px;
border-radius:15px;
border:1px solid rgba(14,165,233,0.25);
margin-bottom:15px;
">
<h2 style="color:#38BDF8;
            font-size:32px;
font-weight:700;
            ">
📊 Audio Insights
</h2>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns([1, 1.5])

with col3:
    st.subheader("😊 Mood Distribution")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📊 Feature Correlation")
    st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style="
background:linear-gradient(
135deg,
rgba(16,185,129,0.15),
rgba(16,185,129,0.05)
);
padding:20px;
border-radius:15px;
border:1px solid rgba(16,185,129,0.25);
margin-bottom:15px;
">
<h2 style="
color:#34D399;
font-size:32px;
font-weight:700;
">
🎤 Top Artists
</h2>
</div>
""", unsafe_allow_html=True)

st.plotly_chart(fig_artist, use_container_width=True)
search_track = st.sidebar.text_input(
    "Search Track"
)
if search_track:
    result = filtered_df[
        filtered_df["track_name"]
        .str.contains(search_track, case=False, na=False)
    ]

    st.subheader("🔍 Search Results")

    st.dataframe(
        result[
            ["track_name",
             "artists",
             "popularity",
             "track_genre"]
        ].head(20)
    )
    st.divider()

st.markdown("---")
st.markdown("""
<div style="
background:linear-gradient(
135deg,
rgba(236,72,153,0.15),
rgba(236,72,153,0.05)
);
padding:20px;
border-radius:15px;
border:1px solid rgba(236,72,153,0.25);
margin-bottom:15px;
">
<h2 style="color:#F472B6;
            font-size:32px;
font-weight:700;
            ">
🎯 Recommended Tracks
</h2>
</div>
""", unsafe_allow_html=True)

recommended = filtered_df.sort_values(
    by="popularity",
    ascending=False
)
st.dataframe(
    recommended[
        ["track_name","artists","popularity"]
    ].head(10),
    use_container_width=True,
    height=380
)
st.divider()

st.markdown("""
<div style="
background:linear-gradient(
135deg,
rgba(255,193,7,0.15),
rgba(255,193,7,0.05)
);
padding:15px;
border-radius:15px;
border:1px solid rgba(255,193,7,0.25);
margin-bottom:15px;
">
<h3 style="color:#FFD54F;
            font-size:32px;
font-weight:700;
            ">
🤖 AI Mood Recommendation
</h3>
</div>
""", unsafe_allow_html=True)

st.write(
    "Find songs that match your current mood using audio feature similarity."
)


mood_choice = st.selectbox(
    "Choose your mood:",
    [
        "Happy 😊",
        "Calm 🌿",
        "Energetic 🔥",
        "Sad 🌧️"
    ]
)


mood_profiles = {

    "Happy 😊": {
        "valence": 0.8,
        "energy": 0.75,
        "danceability": 0.65
    },

    "Calm 🌿": {
        "valence": 0.5,
        "energy": 0.3,
        "danceability": 0.35
    },

    "Energetic 🔥": {
        "valence": 0.7,
        "energy": 0.9,
        "danceability": 0.8
    },

    "Sad 🌧️": {
        "valence": 0.25,
        "energy": 0.35,
        "danceability": 0.3
    }

}


if mood_choice:

    target = mood_profiles[mood_choice]


    temp_df = filtered_df.copy()


    temp_df["mood_score"] = (

        abs(temp_df["valence"] - target["valence"]) +

        abs(temp_df["energy"] - target["energy"]) +

        abs(temp_df["danceability"] - target["danceability"])

    )


    recommendations = (
        temp_df
        .sort_values(
            "mood_score"
        )
        [
            [
                "track_name",
                "artists",
                "popularity",
                "mood_score"
            ]
        ]
        .head(10)
    )


    recommendations["Mood Match %"] = (
        (1 - recommendations["mood_score"])
        * 100
    ).round(1)


    st.write(
        f"🎧 Songs matching your {mood_choice} mood"
    )


    st.dataframe(
    recommendations[
        [
            "track_name",
            "artists",
            "popularity",
            "Mood Match %"
        ]
    ],
    use_container_width=True,
    height=380
)

    st.divider()

st.markdown("""
<div style="
background:linear-gradient(
135deg,
rgba(138,43,226,0.15),
rgba(138,43,226,0.05)
);
padding:15px;
border-radius:15px;
border:1px solid rgba(138,43,226,0.25);
margin-bottom:15px;
">
<h3 style="color:#C084FC;
            font-size:32px;
font-weight:700;
            ">
🎵 Song-to-Song Recommendation
</h3>
</div>
""", unsafe_allow_html=True)

selected_song = st.selectbox(
    
    "Choose a song",
    df["track_name"].unique()
)

if selected_song:

    song_index = df[
        df["track_name"] == selected_song
    ].index[0]

    song_recommendations = recommend_tracks(
        song_index,
        df,
        model,
        scaler
    )

    st.dataframe(
    song_recommendations[
        ["track_name","artists","popularity"]
    ],
    use_container_width=True,
    height=350
)
    st.divider()


st.markdown(
    """
    <div style="
        text-align:center;
        color:#B3B3B3;
        padding-top:10px;
opacity:0.8;
        font-size:14px;
    ">
        🎵 Spotify MoodShift AI | Built with Streamlit, Plotly & Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)