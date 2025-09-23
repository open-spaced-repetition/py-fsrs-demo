import streamlit as st
from fsrs import Scheduler, Card, Rating, State
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math

def display_info(*, card: Card, scheduler: Scheduler):

    stability = card.stability

    print(f"state = {repr(card.state)}")
    if card.state == State.Review:
        days_till_due = (card.due - card.last_review).days
        plt.axvline(x=days_till_due, color="red", linestyle="--", linewidth=1)
        print(f"days till due: {days_till_due}")

        
    elif card.state == State.Learning:
        num_learning_steps = len(scheduler.learning_steps)
        print(f"learning step {card.step+1} of {num_learning_steps}")

        plt.axvline(x=0, color="red", linestyle="--", linewidth=1)
        minutes_till_due = math.ceil(scheduler.learning_steps[card.step].total_seconds() / 60)
        print(f"minutes till due: {minutes_till_due}")
        
    elif card.state == State.Relearning:
        num_relearning_steps = len(scheduler.relearning_steps)
        print(f"relearning step {card.step+1} of {num_relearning_steps}")

        plt.axvline(x=0, color="red", linestyle="--", linewidth=1,)
        minutes_till_due = math.ceil(scheduler.relearning_steps[card.step].total_seconds() / 60)
        print(f"minutes till due: {minutes_till_due}")
    
    if stability is not None:
        
        days_range = range(0,1000)
        retrievabilities = [scheduler.get_card_retrievability(card=card, current_datetime=card.last_review+timedelta(days=days)) for days in days_range]
        
        plt.plot(days_range, retrievabilities)
        
        
    plt.xlabel("Days")
    plt.ylabel("Retrievability")
    plt.title("FSRS Forgetting Curve")
    plt.axhline(y=scheduler.desired_retention, color="grey", linestyle="--", linewidth=1, label="Desired Retention")

    plt.xlim(0,1000)
    plt.ylim(0.4,1)
    
    plt.legend()
    
    # plt.show()
    st.pyplot(plt.gcf())
    plt.clf()

st.set_page_config(
    page_title="Py-FSRS Demo",
    page_icon="osr_logo.png"
)

# TODO: add link to the demo repo and to py-fsrs

# Add slider for desired retention value
desired_retention = st.slider(
    "Desired Retention",
    min_value=0.50,
    max_value=0.95,
    value=0.9,
    step=0.05,
    help="The target retention rate for the FSRS algorithm"
)

# Initialize scheduler with the selected retention value
if 'desired_retention' not in st.session_state or st.session_state.desired_retention != desired_retention:
    st.session_state.desired_retention = desired_retention
    st.session_state.scheduler = Scheduler(desired_retention=desired_retention, enable_fuzzing=False)

scheduler = st.session_state.scheduler

if 'card' not in st.session_state:
    st.session_state.card = Card()

card = st.session_state.card

display_info(card=card, scheduler=scheduler)

# TODO: add current card state info
# count how many reviews the card has gotten

# maybe display key statistics and advanced statistics in different visual sections?

st.markdown("---")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col2:
    if st.button("Again"):
        st.session_state.card, _ = scheduler.review_card(card=card, rating=Rating.Again, review_datetime=card.due)
        st.rerun()

with col3:
    if st.button("Hard"):
        st.session_state.card, _ = scheduler.review_card(card=card, rating=Rating.Hard, review_datetime=card.due)
        st.rerun()

with col4:
    if st.button("Good"):
        st.session_state.card, _ = scheduler.review_card(card=card, rating=Rating.Good, review_datetime=card.due)
        st.rerun()

with col5:
    if st.button("Easy"):
        st.session_state.card, _ = scheduler.review_card(card=card, rating=Rating.Easy, review_datetime=card.due)
        st.rerun()

st.markdown("")
st.markdown("")
st.markdown("")
col1, col2, col3, col4, col5 = st.columns(5)
with col3:  # Middle column
    if st.button("Reset Card"):
        st.session_state.card = Card()
        st.rerun()


# TODO: add some notes below explaining potentially confusing parts of this app e.g., what retrievability means, what again, hard, good and easy mean