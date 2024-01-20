## Accessibility Hub

A community focused on accessibility. It provides space for discussion and reviews on accessibility.

> Accessibility isn't only screen reader and blindness. To me, accessibility has to do with providing the things some people need to use your tool. People that require that feature are people that depends on the accessibility of the tool.

This repo has the first alpha version of the website. All subsequent versions are under different licences.

The website is not live yet.

## Try it!

You need python to be able to test this web app.

To run this locally, do this:

1. **Clone the repo**; `git clone https://github.com/arfs6/AccessibilityHub`
2. **Switch to the directory / folder**; `cd AccessibilityHub`
3. **Get the pip dependencies**; `pip install -r requirements.txt`
4. **Switch to the django project**; `cd src/accessibilityHub`
5. **Start the local server**; `python manage.py runserver`

**BOOM!** Now, you can open your browser and type localhost:5000 in the address bar to open the website.

## Disassemble

Accessibility hub is made up of

- [Django](django)
- [Gunicorn](#gunicorn)
- [Nginx](#nginx)
- [MySQL](#mysql)
- [HTMX](#htmx)
- [Fabric](#fabric)

### Django {#django}

Accessibility hub was built using the django frame work. I think one of the biggest reason why I chose django over flask is the batteries included stuffs. It has three django apps;

- `core`: This apps has the core part of the website. This could be parts that fit everywhere (like templates) or parts that fits nowhere (like home page).
- `review`; This app has code related to the review feature of accessibility hub.
- `api`; As the name suggests, the api app has api related code. Although, I am thinking of removing this app because I am using [HTMX](#htmx).

So far, no external django app / middle-ware has been used.

### Gunicorn {#gunicorn}

I used [gunicorn]() as the wsgi server that nginx proxies to. Gunicorn has it's own systemd script, so it's possible to start / stop / restart the app using systemctl.

### Nginx {#nginx}

Nginx is the web server that serves the static files of the website and proxies all other requests to gunicorn.

### MySQL {#mysql}

I chose MySQL over postgresql because I know MySQL. I thought of using postgresql but as this is a portfolio project with a deadline, I decided sticking with what I know here is better. Django manages the sql migrations and most things.

### Fabric {#fabric}

Automation!!! I used fabric to automate some stuffs. Like creating and setting up new servers. The fabric script most probably needs some updates because somethings has changed in the project.

Now, this is the disassembling of accessibility hub.
