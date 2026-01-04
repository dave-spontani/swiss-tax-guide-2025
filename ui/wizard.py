"""
Multi-step wizard UI logic for tax questionnaire
"""
import streamlit as st


def init_wizard_state():
    """Initialize wizard state in Streamlit session."""
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1

    if 'profile' not in st.session_state:
        from models.tax_data import UserProfile
        st.session_state.profile = UserProfile()

    if 'deductions' not in st.session_state:
        from models.tax_data import DeductionResult
        st.session_state.deductions = DeductionResult()


def render_progress_bar(current_step: int, total_steps: int = 4):
    """Render wizard progress bar."""
    progress = current_step / total_steps
    st.progress(progress)
    st.caption(f"Step {current_step} of {total_steps}")


def render_navigation_buttons(current_step: int, total_steps: int = 4):
    """Render navigation buttons for wizard."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_step > 1:
            if st.button("← Back", use_container_width=True):
                st.session_state.wizard_step = current_step - 1
                st.rerun()

    with col3:
        if current_step < total_steps:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.wizard_step = current_step + 1
                st.rerun()
        else:
            # On last step, show "Calculate Taxes" button
            if st.button("View Results", type="primary", use_container_width=True):
                st.session_state.wizard_step = current_step
                st.rerun()


def restart_wizard():
    """Restart the wizard from step 1."""
    st.session_state.wizard_step = 1
    from models.tax_data import UserProfile, DeductionResult
    st.session_state.profile = UserProfile()
    st.session_state.deductions = DeductionResult()
    st.rerun()
