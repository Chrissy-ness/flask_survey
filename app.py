from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "NFAQJQL"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#Variables available outside the scope of the exisitng routes. 
title = satisfaction_survey.title
length = len(satisfaction_survey.questions)

RESPONSE = []
redirect_num = 1

@app.route('/')
def home_route():
    """Initialize the home template with basic title and button to start the survey"""

    return render_template('home.html', title=title)


@app.route('/start', methods=["POST"])
def start():
    """Clear previous instance of Response whenever a user clicks the start survey button."""
    global RESPONSE
    global redirect_num

    RESPONSE = []
    redirect_num = 1
    return redirect("/survey/1")


@app.route('/survey/<q_id>')
def q_maker(q_id):
    """Render a question template with its designated question, choices, and next button."""
    status = f"Question {q_id}"

    question = satisfaction_survey.questions[int(q_id)-1].question
    choices = satisfaction_survey.questions[int(q_id)-1].choices

    return render_template('question.html', status=status, title=title, question=question, choices=choices)

@app.route('/answer', methods=["POST"])
def process_answer():
    """Handle the answer part of the survey and append it to the RESPONSE list"""
    user_input = request.form['answer']

    #Grab the current RESPONSE list that is outside the function's scope, add to it, and update it's original variable with the new list.
    global RESPONSE 
    current_list = RESPONSE
    current_list.append(user_input)
    RESPONSE = current_list

    #When this route is triggered, update the redirect_num to assist this POST route in finding the next question.
    global redirect_num
    new_num = redirect_num + 1
    redirect_num = new_num


    #Redirect the user to the next question.
    #Logic that checks if the redirect needs to be to the next question, or the complete route. 
    if len(RESPONSE) == length:
        return redirect('/complete')

    else:
        return redirect(f'/survey/{redirect_num}')

@app.route('/complete')
def complete():
    return render_template('complete.html', response=RESPONSE)




























# @app.route("/")
# def home():
#     """Render a template of the title, instructions, and button to start the survey."""
#     instructions = satisfaction_survey.instructions

#     return render_template("home.html", title=title, instructions=instructions)

# @app.route("/question/<number>")
# def question_maker(number):
#     """Render a template with questions based on the order given by the survey object."""
#     url_num = int(number)
#     question_num = url_num + 1
#     next_num = url_num + 1

#     #Variables for question and choices generated from the given instance. 
#     question = satisfaction_survey.questions[url_num].question
#     choices = satisfaction_survey.questions[url_num].choices

#     #Variable to help the POST route render the next template.
#     redirect_num = str(url_num)

#     #Logic to execute when the next href link reaches the max number of questions, and direct the user to the concluding href. 
#     if next_num > length-1:
#         next_num = "end_survey"
#         status = "Finish"
#     else:
#         status = "Next"

#     #Variables to control the href link for the "back" button on the question.html.
#     home_href = "/"
#     previous_href = f"/question/{url_num - 1}"
#     back_href = ""

#     #Logic to execute when reaching the very first question upon spamming the back button. 
#     if url_num == 0:
#         back_href = home_href
#     else:
#         back_href = previous_href

#     return render_template("question.html", url_num=url_num, q_num=question_num, question=question, choices=choices, back=back_href, status=status, response=RESPONSES)


# @app.route("/question/next", methods=["POST"])
# def next_route():
#     answer = request.form["answer"]
#     RESPONSES.append(answer)

#     return redirect(f"/question/{redirect_num}")


# @app.route("/question/end_survey")
# def end_survey():
#     return render_template("end_survey.html", response=RESPONSES)