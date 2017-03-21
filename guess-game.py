import random

from flask import Flask, flash, redirect, session, url_for, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a string that is very hard to guess'


@app.route('/')
def index():
    # generate a random number in 0~1000, store it into session.
    session['number'] = random.randint(0, 1000)
    session['times'] = 10
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if request.method == 'POST':
        print('start guess')
        times = session['times']
        result = session.get('number')
        if not request.form['number'].isdigit():
            flash('Please enter an integer.', 'warning')
        else:
            times -= 1
            print(times, result)
            session['times'] = times  # update session value
            if times == 0:
                flash('Game Over. You lost. The integer is %s.' % result, 'danger')
                return redirect(url_for('.index'))
            answer = int(request.form['number'])
            if answer < 1 or answer > 1000:
                flash('Please enter an integer between 1 and 1000. You still have %s times.' % times,'warning')
            else:
                if answer > result:
                    if times == 1:
                        flash('Too large! This will be your last guess.', 'warning')
                    else:
                        flash('Too large! You still have %s times.' % times, 'warning')
                elif answer < result:
                    if times == 1:
                        flash('Too small! This will be your last guess.', 'info')
                    else:
                        flash('Too small! You still have %s times.' % times, 'info')
                else:
                    flash('Congratulations! You won V(＾－＾)V', 'success')
                    return redirect(url_for('.index'))
    return render_template('guess.html')


if __name__ == '__main__':
    app.run()
