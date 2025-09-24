import streamlit as st
from fsrs import Scheduler, Card, Rating, State
from datetime import timedelta
import matplotlib.pyplot as plt
import math
from copy import deepcopy


def display_info(*, card: Card, scheduler: Scheduler):
    stability = card.stability

    print(f"state = {repr(card.state)}")
    if card.state == State.Review:
        days_till_due = (card.due - card.last_review).days
        plt.axvline(x=days_till_due, color="red", linestyle="--", linewidth=1)
        print(f"days till due: {days_till_due}")

    elif card.state == State.Learning:
        num_learning_steps = len(scheduler.learning_steps)
        print(f"learning step {card.step + 1} of {num_learning_steps}")

        plt.axvline(x=0, color="red", linestyle="--", linewidth=1)
        minutes_till_due = math.ceil(
            scheduler.learning_steps[card.step].total_seconds() / 60
        )
        print(f"minutes till due: {minutes_till_due}")

    elif card.state == State.Relearning:
        num_relearning_steps = len(scheduler.relearning_steps)
        print(f"relearning step {card.step + 1} of {num_relearning_steps}")

        plt.axvline(
            x=0,
            color="red",
            linestyle="--",
            linewidth=1,
        )
        minutes_till_due = math.ceil(
            scheduler.relearning_steps[card.step].total_seconds() / 60
        )
        print(f"minutes till due: {minutes_till_due}")

    if stability is not None:
        days_range = range(0, 1000)
        retrievabilities = [
            scheduler.get_card_retrievability(
                card=card, current_datetime=card.last_review + timedelta(days=days)
            )
            for days in days_range
        ]

        plt.plot(days_range, retrievabilities)

    plt.xlabel("Days")
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


st.set_page_config(page_title="Py-FSRS Demo", page_icon="osr_logo.png")

# TODO: add link to the demo repo and to py-fsrs

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

# TODO: add current card state info
# count how many reviews the card has gotten

# maybe display key statistics and advanced statistics in different visual sections?

st.markdown("---")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col2:
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
st.markdown("")
col1, col2, col3, col4, col5 = st.columns(5)
with col3:  # Middle column
    if st.button("Reset Card"):
        st.session_state.prev_card = None
        st.session_state.card = Card()
        st.rerun()


# TODO: add some notes below explaining potentially confusing parts of this app e.g., what retrievability means, what again, hard, good and easy mean
