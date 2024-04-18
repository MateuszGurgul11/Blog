from flask import render_template, request, redirect, url_for, flash, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm

@app.route("/")
def index():
   posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", posts=posts)


@app.route("/post<int:entry_id>", methods=['GET', 'POST'])
@app.route("/post", defaults={'entry_id': None}, methods=['GET', 'POST'])
def manage_entry(entry_id):
   entry = Entry.query.get(entry_id) if entry_id else Entry()
   form = EntryForm(obj=entry)
   errors = None

   if request.method == 'POST':
      if form.validate_on_submit():
         if not entry_id:
            db.session.add(entry)
         form.populate_obj(entry)
         db.session.commit()
         flash("Post zostal zaktualizowany" if entry_id else "Post został dodany")
         return redirect(url_for("index"))
      else:
         errors == form.errors
         return render_template("entry_form.html", form=form, errors=errors)
   return render_template("entry_form.html", form=form, errors=errors)

@app.route("/login", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get("next")
   if request.method == 'POST':
      if form.validate_on_submit():
         session['logged_in'] = True
         session.permanent = True
         flash('Jestes teraz zalogowany!', 'success')
         return redirect(next_url or url_for('index'))
      else:
         errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
      session.clear()
      flash("Zostales wylogowany!", "success")
   return redirect(url_for("index"))