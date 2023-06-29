from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.parties_model import Party

@app.route('/parties/new')
def Show_Form():

    return render_template('party_form.html')

@app.route('/parties/create', methods=['POST'])
def Submit_Party_Form():
    if not Party.validate_party(request.form):
        return redirect('/parties/new')
    
    party_data= {
        **request.form,
        'user_id' : session['user_id']
    }

    Party.create_party(party_data)

    return redirect ('/dashboard')

@app.route('/parties/<int:party_id>')
def Show_Party(party_id):

    one_party = Party.get_one_party({'party_id': party_id})

    return render_template('show_party.html', one_party= one_party)

@app.route('/parties/edit/<int:party_id>')
def show_edit_form(party_id):
    one_party= Party.get_one_party({'party_id': party_id})
    return render_template('party_edit.html',one_party=one_party )

@app.route('/parties/update/<int:party_id>', methods=['POST'])
def submit_edit_form(party_id):

    if not Party.validate_party(request.form):
        return redirect(f'/parties/edit/{party_id}')
    
    Party. update_party({
        ** request.form,
        'party_id' : party_id
    })
    
    return redirect('/dashboard')

@app.route('/parties/cancel/<int:party_id>')
def cancel_party(party_id):
    Party.destroy({'party_id': party_id})
    return redirect('/dashboard')