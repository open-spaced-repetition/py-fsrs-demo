import streamlit as st
from fsrs import Scheduler, Card, Rating, State
from datetime import timedelta
import matplotlib.pyplot as plt
from copy import deepcopy
from streamlit_extras.stylable_container import stylable_container


def display_info(*, card: Card, scheduler: Scheduler):
    plt.figure(figsize=(7, 4))

    stability = card.stability

    if card.state == State.Review:
        days_till_due = (card.due - card.last_review).days
        plt.axvline(x=days_till_due, color="red", linestyle="--", linewidth=1)

    elif card.state == State.Learning:
        plt.axvline(x=0, color="red", linestyle="--", linewidth=1)

    elif card.state == State.Relearning:
        num_relearning_steps = len(scheduler.relearning_steps)
        print(f"relearning step {card.step + 1} of {num_relearning_steps}")

        plt.axvline(
            x=0,
            color="red",
            linestyle="--",
            linewidth=1,
        )

    if stability is not None:
        days_range = range(0, 1000)
        retrievabilities = [
            scheduler.get_card_retrievability(
                card=card, current_datetime=card.last_review + timedelta(days=days)
            )
            for days in days_range
        ]

        plt.plot(days_range, retrievabilities)

    plt.xlabel("Days since last review\n(up to 1,000)")
    plt.ylabel("Retrievability")
    plt.title("FSRS Forgetting Curve")
    plt.axhline(
        y=scheduler.desired_retention,
        color="grey",
        linestyle="--",
        linewidth=1,
        label="Desired Retention",
    )

    plt.xlim(0, 1000)
    plt.ylim(0.4, 1)

    plt.legend()

    # plt.show()
    st.pyplot(plt.gcf())
    plt.clf()


st.set_page_config(page_title="Interactive Forgetting Curve", page_icon="osr_logo.png")


# Add slider for desired retention value
desired_retention = st.slider(
    "Desired Retention",
    min_value=0.50,
    max_value=0.95,
    value=0.9,
    step=0.05,
    help="The target retention rate for the FSRS algorithm",
)

if "card" not in st.session_state:
    st.session_state.card = Card()

if "prev_card" not in st.session_state:
    st.session_state.prev_card = None

if "prev_rating" not in st.session_state:
    st.session_state.prev_rating = None

# TODO: look into potentially simplifying logic around session_state for scheduler/desired_retention

# Initialize scheduler with the selected retention value
if "desired_retention" not in st.session_state:
    st.session_state.desired_retention = desired_retention
    st.session_state.scheduler = Scheduler(
        desired_retention=desired_retention, enable_fuzzing=False
    )

elif st.session_state.desired_retention != desired_retention:
    st.session_state.desired_retention = desired_retention
    st.session_state.scheduler = Scheduler(
        desired_retention=desired_retention, enable_fuzzing=False
    )

    # get previous rating

    if st.session_state.prev_card is not None:
        st.session_state.card, _ = st.session_state.scheduler.review_card(
            card=st.session_state.prev_card,
            rating=st.session_state.prev_rating,
            review_datetime=st.session_state.card.last_review,
        )


scheduler = st.session_state.scheduler

display_info(card=st.session_state.card, scheduler=scheduler)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col2:
    with stylable_container(
        "again",
        css_styles="""
        button {
            background-color: #d32f2f;
            color: white;
        }
        """,
    ):
        if st.button("Again"):
            rating = Rating.Again
            st.session_state.prev_card = deepcopy(st.session_state.card)
            st.session_state.prev_rating = rating
            st.session_state.card, _ = scheduler.review_card(
                card=st.session_state.card,
                rating=rating,
                review_datetime=st.session_state.card.due,
            )
            st.rerun()

with col3:
    with stylable_container(
        "hard",
        css_styles="""
        button {
            background-color: #455a64;
            color: white;
        }""",
    ):
        if st.button("Hard"):
            rating = Rating.Hard
            st.session_state.prev_card = deepcopy(st.session_state.card)
            st.session_state.prev_rating = rating
            st.session_state.card, _ = scheduler.review_card(
                card=st.session_state.card,
                rating=rating,
                review_datetime=st.session_state.card.due,
            )
            st.rerun()

with col4:
    with stylable_container(
        "good",
        css_styles="""
        button {
            background-color: #4caf50;
            color: white;
        }""",
    ):
        if st.button("Good"):
            rating = Rating.Good
            st.session_state.prev_card = deepcopy(st.session_state.card)
            st.session_state.prev_rating = rating
            st.session_state.card, _ = scheduler.review_card(
                card=st.session_state.card,
                rating=rating,
                review_datetime=st.session_state.card.due,
            )
            st.rerun()

with col5:
    with stylable_container(
        "easy",
        css_styles="""
        button {
            background-color: #03a9f4;
            color: white;
        }""",
    ):
        if st.button("Easy"):
            rating = Rating.Easy
            st.session_state.prev_card = deepcopy(st.session_state.card)
            st.session_state.prev_rating = rating
            st.session_state.card, _ = scheduler.review_card(
                card=st.session_state.card,
                rating=rating,
                review_datetime=st.session_state.card.due,
            )
            st.rerun()

st.markdown("")
st.markdown("")
col1, col2, col3, col4, col5 = st.columns(5)
with col3:  # Middle column
    if st.button("Reset Card 🔄"):
        st.session_state.prev_card = None
        st.session_state.card = Card()
        st.rerun()

st.markdown("---")

st.markdown(
    "*([Link](https://github.com/open-spaced-repetition/py-fsrs) to py-fsrs and [link](https://github.com/open-spaced-repetition/py-fsrs-demo) for demo source code)*"
)

st.markdown(
    "*([Link](https://en.wikipedia.org/wiki/Forgetting_curve) to forgetting curve wikipedia article.)*"
)

st.markdown(
    "This forgetting curve in particular uses the [FSRS](https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler) model."
)

st.markdown(
    "**Retrievability** is the predicted probability that a card is correctly recalled at the time of review. **Hard**, **Good** and **Easy** all count as correctly recalling the card. Only **Again** counts as a failure of recall."
)

st.markdown(
    "**Desired Retention** is the rate that determines when a learner should review a card. A card becomes due as soon as it's retrievability falls below the desired retention. Higher desired retention rates generally lead to more reviews and shorter spaces between reviews."
)

st.markdown("(And yes, this app is clunky. It's a streamlit app)")
