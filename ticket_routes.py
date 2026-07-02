from flask import Blueprint, render_template, request, redirect, url_for, flash
from ticket_service import delete_ticket, get_all_tickets, get_ticket_by_id, add_ticket, resolve_ticket, start_progress_ticket, update_ticket

ticket_bp = Blueprint("tickets", __name__)


@ticket_bp.route("/")
def home():
    user_name = "Mostafa"
    return render_template("home.html", name=user_name, tickets=get_all_tickets())


@ticket_bp.route("/tickets/<int:ticket_id>")
def ticket_details(ticket_id):
    selected_ticket = get_ticket_by_id(ticket_id)
    return render_template("ticket_details.html", ticket=selected_ticket)


@ticket_bp.route("/tickets/new")
def show_create_ticket_form():
    return render_template("create_ticket.html")


@ticket_bp.route("/tickets", methods=["POST"])
def create_ticket():
    title = request.form["title"]
    description = request.form["description"]

    if title.strip() == "":
        return render_template("create_ticket.html", error="Title is required")

    if description.strip() == "":
        return render_template("create_ticket.html", error="Description is required")

    add_ticket(title, description)

    flash("Ticket created successfully")

    return redirect(url_for("tickets.home"))


@ticket_bp.route("/tickets/<int:ticket_id>/resolve", methods=["POST"])
def resolve_ticket_route(ticket_id):
    ticket, message = resolve_ticket(ticket_id)

    flash(message)

    if ticket is None:
        return redirect(url_for("tickets.home"))

    return redirect(url_for("tickets.ticket_details", ticket_id=ticket_id))


@ticket_bp.route("/tickets/<int:ticket_id>/start", methods=["POST"])
def start_progress_ticket_route(ticket_id):
    ticket, message = start_progress_ticket(ticket_id)

    flash(message)

    if ticket is None:
        return redirect(url_for("tickets.home"))

    return redirect(url_for("tickets.ticket_details", ticket_id=ticket_id))

@ticket_bp.route("/tickets/<int:ticket_id>/edit")
def edit_ticket_form(ticket_id):
    ticket = get_ticket_by_id(ticket_id)

    if ticket is None:
        flash("Ticket not found")
        return redirect(url_for("tickets.home"))

    return render_template("edit_ticket.html", ticket=ticket)

@ticket_bp.route("/tickets/<int:ticket_id>/edit", methods=["POST"])
def update_ticket_route(ticket_id):
    title = request.form["title"]
    description = request.form["description"]

    ticket, message = update_ticket(ticket_id, title, description)

    flash(message)

    if ticket is None:
        return redirect(url_for("tickets.home"))

    if message != "Ticket updated successfully":
        return render_template("edit_ticket.html", ticket=ticket)

    return redirect(url_for("tickets.ticket_details", ticket_id=ticket_id))


@ticket_bp.route("/tickets/<int:ticket_id>/delete", methods=["POST"])
def delete_ticket_route(ticket_id):
    message = delete_ticket(ticket_id)

    flash(message)

    return redirect(url_for("tickets.home"))