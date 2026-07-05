from flask import Blueprint, render_template, request, redirect, session, url_for, flash, abort
from ticket_service import delete_ticket, get_all_tickets, get_filtered_tickets, get_ticket_by_id, add_ticket, resolve_ticket, search_tickets, start_progress_ticket, update_ticket,get_tickets_by_status
from auth_helpers import login_required

ticket_bp = Blueprint("tickets", __name__)


@ticket_bp.route("/")
def home():
    user_name = "Mostafa"

    status = request.args.get("status")
    q = request.args.get("q")

    page = request.args.get("page", 1, type=int)
    page_size = 5

    tickets = get_filtered_tickets(status, q, page, page_size)

    return render_template(
        "home.html",
        name=user_name,
        tickets=tickets,
        selected_status=status,
        search_keyword=q,
        page=page
    )

@ticket_bp.route("/tickets/<int:ticket_id>")
def ticket_details(ticket_id):
    selected_ticket = get_ticket_by_id(ticket_id)

    if selected_ticket is None:
        abort(404)

    return render_template("ticket_details.html", ticket=selected_ticket)


@ticket_bp.route("/tickets/new")
@login_required
def show_create_ticket_form():
    return render_template("create_ticket.html")


@ticket_bp.route("/tickets", methods=["POST"])
@login_required
def create_ticket():
    title = request.form["title"]
    description = request.form["description"]

    if title.strip() == "":
        return render_template("create_ticket.html", error="Title is required", title=title, description=description)

    if description.strip() == "":
        return render_template("create_ticket.html", error="Description is required", title=title, description=description)

    add_ticket(title, description, session["user_id"])

    flash("Ticket created successfully")

    return redirect(url_for("tickets.home"))


@ticket_bp.route("/tickets/<int:ticket_id>/resolve", methods=["POST"])
@login_required
def resolve_ticket_route(ticket_id):
    ticket, message = resolve_ticket(ticket_id)

    flash(message)

    if ticket is None:
        return redirect(url_for("tickets.home"))

    return redirect(url_for("tickets.ticket_details", ticket_id=ticket_id))


@ticket_bp.route("/tickets/<int:ticket_id>/start", methods=["POST"])
@login_required
def start_progress_ticket_route(ticket_id):
    ticket, message = start_progress_ticket(ticket_id)

    flash(message)

    if ticket is None:
        return redirect(url_for("tickets.home"))

    return redirect(url_for("tickets.ticket_details", ticket_id=ticket_id))

@ticket_bp.route("/tickets/<int:ticket_id>/edit")
@login_required
def edit_ticket_form(ticket_id):
    ticket = get_ticket_by_id(ticket_id)

    if ticket is None:
        flash("Ticket not found")
        return redirect(url_for("tickets.home"))

    return render_template("edit_ticket.html", ticket=ticket)

@ticket_bp.route("/tickets/<int:ticket_id>/edit", methods=["POST"])
@login_required
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
@login_required
def delete_ticket_route(ticket_id):
    message = delete_ticket(ticket_id)

    flash(message)

    return redirect(url_for("tickets.home"))


