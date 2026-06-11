import streamlit as st
import pandas as pd
import copy
import time

import solver
from solver import solve
from image_processor import extract_board

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Sudoku Solver",
    page_icon="🧩",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

[data-testid="stMetric"]{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

st.title("🧩 AI Sudoku Solver")

st.write(
    "Upload a Sudoku image and solve it automatically."
)

# ==================================================
# FILE UPLOADER
# ==================================================

uploaded_file = st.file_uploader(
    "📤 Upload Sudoku Image",
    type=["png", "jpg", "jpeg"]
)

# ==================================================
# MAIN APP
# ==================================================

if uploaded_file:

    # OCR

    with st.spinner("🔍 Reading Sudoku..."):

        board = extract_board(
            uploaded_file
        )

    st.success("OCR Complete")

    # Count detected digits

    filled = sum(
        1
        for row in board
        for value in row
        if value != 0
    )

    st.metric(
        "Detected Digits",
        filled
    )

    # Display image + board

    col1, col2 = st.columns([1, 1])

    with col1:

        st.subheader("Uploaded Image")

        st.image(
            uploaded_file,
            width=250
        )

    with col2:

        st.subheader("Detected Sudoku")

        detected_df = pd.DataFrame(board)

        st.table(
            detected_df
        )

    st.divider()

    # Debug board

    with st.expander("🔍 View OCR Output"):

        st.code(board)

    # Safety

    if filled < 15:

        st.error(
            "Too few digits detected. OCR likely failed."
        )

        st.stop()

    # ==================================================
    # SOLVE BUTTON
    # ==================================================

    if st.button(
        "🚀 Solve Sudoku",
        use_container_width=True
    ):

        progress = st.progress(0)

        try:

            with st.spinner(
                "🧠 Solving Sudoku..."
            ):

                progress.progress(20)

                solver.calls = 0
                solver.START_TIME = time.time()

                start = time.time()

                solved_board = copy.deepcopy(
                    board
                )

                progress.progress(50)

                solved = solve(
                    solved_board
                )

                progress.progress(100)

                end = time.time()

            progress.empty()

            if solved:

                st.success(
                    "✅ Sudoku Solved!"
                )

                metric1, metric2 = st.columns(2)

                with metric1:

                    st.metric(
                        "Solve Time",
                        f"{end-start:.4f}s"
                    )

                with metric2:

                    st.metric(
                        "Recursive Calls",
                        solver.calls
                    )

                st.subheader(
                    "Solved Sudoku"
                )

                solved_df = pd.DataFrame(
                    solved_board
                )

                st.table(
                    solved_df
                )

                csv = solved_df.to_csv(
                    index=False
                )

                st.download_button(
                    label="📥 Download Solution",
                    data=csv,
                    file_name="sudoku_solution.csv",
                    mime="text/csv"
                )

            else:

                st.error(
                    "❌ No solution found."
                )

        except TimeoutError:

            st.error(
                "Solver timed out. OCR likely produced an invalid board."
            )