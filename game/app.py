import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
import base64


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "spotify_game_dataset.csv")
df = pd.read_csv(csv_path)

cols = [
    "track_id",
    "embed_url",
    "pred_prob",
    "pred_label",
    "true_label"
]

df = df[cols].copy()

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def sample_game_songs(df, total_songs=5):
    """Sample a mix of hits, misses, and model confidence levels."""
    hits = df[df["true_label"] == 1]
    misses = df[df["true_label"] == 0]

    hit_high_conf = hits[hits["pred_prob"] >= 0.70]
    hit_low_conf = hits[hits["pred_prob"] < 0.70]

    miss_high_conf = misses[misses["pred_prob"] <= 0.30]
    miss_low_conf = misses[misses["pred_prob"] > 0.30]

    samples = []

    def safe_sample(group, n=1):
        if len(group) >= n:
            return group.sample(n)
        elif len(group) > 0:
            return group.sample(len(group))
        return pd.DataFrame(columns=df.columns)

    samples.append(safe_sample(hit_high_conf, 1))
    samples.append(safe_sample(hit_low_conf, 1))
    samples.append(safe_sample(miss_high_conf, 2))
    samples.append(safe_sample(miss_low_conf, 1))

    sampled = pd.concat(samples)

    if len(sampled) < total_songs:
        remaining = df.drop(sampled.index, errors="ignore")
        sampled = pd.concat([
            sampled,
            remaining.sample(total_songs - len(sampled))
        ])

    return sampled.sample(frac=1).reset_index(drop=True)


def render_reveal_cards(user_guess, true_label):
    hit_selected = user_guess == 1
    miss_selected = user_guess == 0

    hit_correct = true_label == 1
    miss_correct = true_label == 0

    hit_icon = "✅" if hit_correct else "❌" if hit_selected else ""
    miss_icon = "✅" if miss_correct else "❌" if miss_selected else ""

    hit_extra_class = "faded-card" if not hit_correct else ""
    miss_extra_class = "faded-card" if not miss_correct else ""

    html = f"""
    <div class="reveal-row">
        <div class="reveal-card hit-card {hit_extra_class}">
            <span>HIT 🔥</span>
            <span>{hit_icon}</span>
        </div>
        <div class="reveal-card miss-card {miss_extra_class}">
            <span>MISS 🥶</span>
            <span>{miss_icon}</span>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

def render_rankings(user_score, model_score, total):
    robot_img = get_base64_image(os.path.join(BASE_DIR, "robot.png"))
    human_img = get_base64_image(os.path.join(BASE_DIR, "human.png"))

    players = [
        {
            "name": "XGBoost",
            "subtitle": "Machine Learning Model",
            "score": model_score,
            "image": robot_img
        },
        {
            "name": "You",
            "subtitle": "Human",
            "score": user_score,
            "image": human_img
        }
    ]

    players = sorted(players, key=lambda x: x["score"], reverse=True)

    html = '<div class="chart-table">'
    html += '<div class="chart-header">'
    html += '<div>#</div>'
    html += '<div>Player</div>'
    html += '<div>Score</div>'
    html += '</div>'

    for rank, player in enumerate(players, start=1):
        html += (
            f'<div class="chart-row">'
            f'<div class="chart-rank">{rank}</div>'

            f'<div class="chart-player">'
            f'<div class="chart-img">'
            f'<img src="data:image/png;base64,{player["image"]}" />'
            f'</div>'
            f'<div class="chart-text">'
            f'<div class="chart-name">{player["name"]}</div>'
            f'<div class="chart-sub">{player["subtitle"]}</div>'
            f'</div>'
            f'</div>'

            f'<div class="chart-score">{player["score"]}/{total}</div>'
            f'</div>'
        )

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)

if "songs" not in st.session_state:
    st.session_state.songs = sample_game_songs(df)
    st.session_state.index = 0
    st.session_state.user_score = 0
    st.session_state.model_score = 0
    st.session_state.revealed = False
    st.session_state.last_correct = None
    st.session_state.last_actual = None
    st.session_state.last_user_guess = None

if "show_instructions" not in st.session_state:
    st.session_state.show_instructions = True

songs = st.session_state.songs
i = st.session_state.index

st.markdown("""
<style>

/* ===================== */
/* GLOBAL */
/* ===================== */

header[data-testid="stHeader"] {
    background: #000000;
}

[data-testid="stToolbar"] {
    display: none;
}

.stApp {
    background-color: #000000;
    color: #FFFFFF;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

h1, h2, h3, p, label, .stMarkdown {
    color: #FFFFFF !important;
}
.opponent-copy {
    line-height: 1.5;
}

.text-spacer {
    display: block;
    height: 10px;
}

/* ===================== */
/* BUTTONS */
/* ===================== */

button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-secondary"] {
    width: 100%;
    height: 110px;
    border-radius: 18px;
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease;
}

/* CRITICAL: keep text centered like reveal cards */
button[data-testid="stBaseButton-primary"] p,
button[data-testid="stBaseButton-secondary"] p {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: inherit !important;
    text-align: center;
}

/* HIT */
button[data-testid="stBaseButton-primary"] {
    border: 2px solid #1DB954 !important;
}

/* MISS */
button[data-testid="stBaseButton-secondary"] {
    border: 2px solid #ff6b6b !important;
}

/* Hover */
button[data-testid="stBaseButton-primary"]:hover {
    background-color: rgba(29, 185, 84, 0.15) !important;
    color: #1DB954 !important;
}

button[data-testid="stBaseButton-secondary"]:hover {
    background-color: rgba(255, 107, 107, 0.12) !important;
    color: #ff6b6b !important;
}

/* Press */
button[data-testid="stBaseButton-primary"]:active,
button[data-testid="stBaseButton-secondary"]:active {
    transform: scale(0.98);
}

/* ===================== */
/* REVEAL CARDS */
/* ===================== */

.reveal-row {
    display: flex;
    gap: 24px;
    width: 100%;
}

.reveal-card {
    flex: 1;
    height: 110px;
    border-radius: 18px;
    padding: 0 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    font-size: 28px;
    font-weight: 700;
    background-color: #000000;
    color: #FFFFFF;
    transition: opacity 0.2s ease;
    box-sizing: border-box;
}

/* center text exactly like buttons */
.reveal-card span:first-child {
    text-align: center;
}

/* position check/X WITHOUT shifting layout */
.reveal-card span:last-child {
    position: absolute;
    right: 28px;
    font-size: 28px;
}

.hit-card {
    border: 2px solid #1DB954;
}

.miss-card {
    border: 2px solid #ff6b6b;
}

.faded-card {
    opacity: 0.55;
}

/* ===================== */
/* RESULTS CHART */
/* ===================== */

.chart-header {
    display: grid;
    grid-template-columns: 50px 1.5fr 120px;
    padding: 12px 0;
    font-size: 16px;
    color: rgba(255,255,255,0.6);
    border-bottom: 1px solid rgba(255,255,255,0.15);
}

.chart-row {
    display: grid;
    grid-template-columns: 50px 1.5fr 120px;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.chart-player {
    display: flex;
    align-items: center;
    gap: 14px;
}

.chart-img {
    width: 56px;
    height: 56px;
    border-radius: 10px;
    overflow: hidden;
    background-color: rgba(29,185,84,0.15);
}

.chart-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.chart-text {
    display: flex;
    flex-direction: column;
}

.chart-name {
    font-size: 22px;
    font-weight: 700;
}

.chart-sub {
    font-size: 16px;
    color: rgba(255,255,255,0.6);
}

.chart-score {
    font-size: 20px;
}

.chart-row:first-of-type .chart-name {
    color: #1DB954;
}

/* ===================== */
/* MOBILE */
/* ===================== */

@media (max-width: 768px) {

    /* STACK both states identically */
    .reveal-row {
        flex-direction: column !important;
        gap: 15px !important;
        min-height: 244px;
        margin-bottom: 5px;
    }

    /* KEEP SIZE IDENTICAL*/
    .reveal-card {
        width: 100% !important;
        height: 110px !important;
        font-size: 28px !important;
    }

    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-secondary"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    button[data-testid="stBaseButton-primary"] p,
    button[data-testid="stBaseButton-secondary"] p {
        font-size: 28px !important;
    }

    /* Slight chart tightening only */
    .chart-header,
    .chart-row {
        grid-template-columns: 40px 1fr 80px;
    }

    .chart-name {
        font-size: 18px;
    }

    .chart-score {
        font-size: 16px;
    }
    .opponent-copy {
        line-height: 1.45;
    }

    .text-spacer {
        height: 8px;
    }
}

</style>
""", unsafe_allow_html=True)

header_path = os.path.join(BASE_DIR, "game_hit_or_miss_header.png")
st.image(header_path, use_container_width=True)

if st.session_state.show_instructions:
    st.markdown(
        "Think you can beat a machine learning model? 🤖 Find out now.\n\n"
        "**Game plan:** Listen 🎧, predict 🔮, repeat 🔁. Then see how you ranked 🏆",
        unsafe_allow_html=True
    )

if i < len(songs):
    row = songs.iloc[i]

    st.write(f"**Song {i + 1} of {len(songs)}**")

    components.iframe(row["embed_url"], height=352)

    if not st.session_state.revealed:
        col1, col2 = st.columns([3, 3], gap="small")

        with col1:
            hit_clicked = st.button(
                "HIT 🔥",
                use_container_width=True,
                key=f"hit_{i}",
                type="primary"
            )

        with col2:
            miss_clicked = st.button(
                "MISS 🥶",
                use_container_width=True,
                key=f"miss_{i}",
                type="secondary"
            )

        if hit_clicked or miss_clicked:
            st.session_state.show_instructions = False

            true_label = int(row["true_label"])
            model_guess = int(row["pred_label"])
            user_guess = 1 if hit_clicked else 0

            actual = "Hit" if true_label == 1 else "Miss"
            user_correct = user_guess == true_label
            model_correct = model_guess == true_label

            if user_correct:
                st.session_state.user_score += 1

            if model_correct:
                st.session_state.model_score += 1

            st.session_state.last_correct = user_correct
            st.session_state.last_actual = actual
            st.session_state.last_user_guess = user_guess
            st.session_state.revealed = True
            st.rerun()

    else:
        render_reveal_cards(
            st.session_state.last_user_guess,
            int(row["true_label"])
        )

        # Feedback text under cards
        if st.session_state.last_correct:
            st.markdown('<div class="result-text correct-text">✅ Correct!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-text incorrect-text">❌ Incorrect!</div>', unsafe_allow_html=True)

        # Score
        st.markdown(f'<div class="score-text">Total Points: {st.session_state.user_score}</div>', unsafe_allow_html=True)

        if i < len(songs) - 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Next Song", type="primary", use_container_width=True):
                    st.session_state.index += 1
                    st.session_state.revealed = False
                    st.session_state.last_correct = None
                    st.session_state.last_actual = None
                    st.session_state.last_user_guess = None
                    st.rerun()
        else:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("See Results", type="primary", use_container_width=True):
                    st.session_state.index += 1
                    st.session_state.revealed = False
                    st.session_state.last_correct = None
                    st.session_state.last_actual = None
                    st.session_state.last_user_guess = None
                    st.rerun()

else:
    user_score = st.session_state.user_score
    model_score = st.session_state.model_score
    total = len(songs)

    st.header("🏆 Final Rankings")
    render_rankings(user_score, model_score, total)

    if user_score > model_score:
        st.success("You've got some sharp instincts. You win... this time 😉")
    elif user_score < model_score:
        st.info("Looks like you were a little off-key this time... still a strong effort 🙂")
    else:
        st.warning("It's a tie... looks like you and the model are in sync 😉")

    st.header("🤖 Meet Your Opponent")
    st.markdown(
    '<div class="opponent-copy">'
    'It may have felt like a game to you... <strong>but not to your opponent.</strong><br>'
    'Trained on over <strong>half a million tracks</strong>, it learned what makes a hit...<br>'
    '<strong>without ever listening to a single song.</strong>'
    '<span class="text-spacer"></span>'
    'Curious how it works? Take a backstage look on 👉 '
    '<a href="https://github.com/itsselsanchez/spotify-hit-prediction" target="_blank">'
    'GitHub'
    '</a>.'
    '</div>',
    unsafe_allow_html=True
)
    st.markdown(
    '<div style="margin-top:30px; opacity:0.7; font-size:14px;">'
    'from the creator<br>'
    '<em>Thanks for playing.</em> 🎧<br>'
    'I hope you enjoyed this as much as I did.<br>'
    '<strong style="opacity:0.9;">- Itssel</strong><br>'
    'your friendly data-saurus 🦖🎀'
    '</div>',
    unsafe_allow_html=True
)