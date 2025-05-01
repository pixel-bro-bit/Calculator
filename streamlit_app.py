import streamlit as st
import math

# ------------------------ Custom CSS ------------------------
# This CSS block creates a colorful, modern look for the calculator.
st.markdown("""
<style>
/* Container for the entire calculator */
.calc-container {
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  padding: 20px;
  border-radius: 15px;
  max-width: 420px;
  margin: auto;
  margin-top: 20px;
}

/* Styling for the expression display */
.expression-box {
  background-color: #ffffff;
  color: #000000;
  font-size: 2em;
  text-align: right;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  min-height: 50px;
}

/* Layout for a row of buttons */
.button-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

/* Each button occupies equal space and has some margin */
.button-col {
  flex: 1;
  margin: 4px;
}

/* Style all Streamlit buttons inside our calculator.
   (Note: Streamlit renders its buttons inside a div with class "stButton") */
div.stButton > button {
  background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
  color: white;
  font-size: 1.5em;
  border: none;
  border-radius: 10px;
  padding: 10px;
  width: 100%;
}
div.stButton > button:hover {
  background: linear-gradient(135deg, #c2e9fb, #a1c4fd);
}
</style>
""", unsafe_allow_html=True)

# ------------------------ Session State Initialization ------------------------
if 'calc' not in st.session_state:
    st.session_state.calc = ""

# ------------------------ Safe Math Environment ------------------------
# Define a dictionary of allowed functions, variables, and constants for safe evaluation.
allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
allowed_names['abs'] = abs
allowed_names['round'] = round

# ------------------------ Button Processing Function ------------------------
def process_button(btn):
    """Update the calculator expression based on the button pressed."""
    # Clear the expression
    if btn == "C":
        st.session_state.calc = ""
    # Evaluate the expression safely
    elif btn == "=":
        try:
            # Evaluate using a restricted environment.
            st.session_state.calc = str(eval(st.session_state.calc, {"__builtins__": None}, allowed_names))
        except Exception as e:
            st.session_state.calc = "Error"
    # Toggle the sign (if the current expression is a number)
    elif btn == "±":
        try:
            value = float(st.session_state.calc)
            st.session_state.calc = str(-value)
        except:
            pass
    # Convert percent (by simply appending "/100" to the expression)
    elif btn == "%":
        st.session_state.calc += "/100"
    # For advanced functions, automatically add the function name and an opening parenthesis
    else:
        mapping = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "log": "log(",
            "√": "sqrt(",
            "exp": "exp(",
            "^": "**",
        }
        if btn in mapping:
            st.session_state.calc += mapping[btn]
        else:
            st.session_state.calc += str(btn)

# ------------------------ Layout the Calculator ------------------------
with st.container():
    # Wrap everything in a container with our colorful styling.
    st.markdown("<div class='calc-container'>", unsafe_allow_html=True)
    
    # Display the current expression/result in a styled expression box.
    st.markdown(f"<div class='expression-box'>{st.session_state.calc}</div>", unsafe_allow_html=True)
    
    # Define the rows of buttons.
    button_rows = [
        ["C", "(", ")", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "±", "="],
        ["sin", "cos", "tan", "log"],
        ["√", "exp", "^", "%"],
        ["pi", "e"]
    ]
    
    # For each row, create a set of columns and place a button in each one.
    for row in button_rows:
        cols = st.columns(len(row))
        for i, btn in enumerate(row):
            if cols[i].button(btn, key=f"{btn}_{i}"):
                process_button(btn)
        st.markdown("<br>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
