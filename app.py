from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tickets = [
    {
        'id': 1,
        'title': 'Ticket 1',
        'description': 'Description for Ticket 1'
    },
    {
        'id': 2,
        'title': 'Ticket 2',
        'description': 'Description for Ticket 2'
    
    },
    {
        'id': 3,
        'title': 'Ticket 3',
        'description': 'Description for Ticket 3'
    }
]


@app.route('/')
def home():
    user_name = "mostafa"

    

    return render_template('home.html', name=user_name, tickets=tickets)

@app.route('/tickets/<int:ticket_id>')
def ticket_detail(ticket_id):

    selcted_ticket = None

    for ticket in tickets:
        if ticket['id'] == ticket_id:
            selcted_ticket = ticket
            break
    
    return render_template('ticket_details.html', ticket=selcted_ticket)


@app.route('/tickets', methods=['POST'])
def create_ticket():
    title = request.form['title']
    description = request.form['description']

    new_ticket = {
        'id': len(tickets) + 1,
        'title': title,
        'description': description
    }

    tickets.append(new_ticket)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)