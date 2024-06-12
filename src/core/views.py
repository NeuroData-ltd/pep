# -*- encoding: utf-8 -*-
from flask import (
    render_template,
    send_file,
    request,
    abort,
    jsonify,
)
from src.core import blueprint
from src import db
from src.core.models import Pep, Adress, Sanction, Identity, PersonRole, Name
from src.config import config_dict
import os
import jwt
import datetime

UPLOAD_DIR = config_dict.get("Production").UPLOAD_DIR
MEDIA_URL = config_dict.get("Production").MEDIA_URL

######## Dynamic pages #########

@blueprint.route("/add-xg4MOkc88x", methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return render_template("home/add.html")
    if request.method == "POST":
        try:
            data = request.get_json()

            if len(data["person_info"][0]["birth_date"]) > 0:
                data["person_info"][0]["birth_date"] = datetime.datetime.strptime(
                    data["person_info"][0]["birth_date"], "%Y-%m-%d"
                )
            else:
                data["person_info"][0]["birth_date"] = None
            pep = Pep(data=data["person_info"][0])
            db.session.add(pep)
            db.session.commit()

            names = []
            for row in data["names"]:
                row["person_info"] = pep
                names.append(Name(row))
            db.session.add_all(names)

            identities = []
            for row in data["identities"]:
                row["person_info"] = pep
                identities.append(Identity(row))
            db.session.add_all(identities)

            sanctions = []
            for row in data["sanctions"]:
                if len(row["sanction_begin_date"]) > 0:
                    row["sanction_begin_date"] = datetime.datetime.strptime(
                        row["sanction_begin_date"], "%Y-%m-%d"
                    )
                else:
                    row["sanction_begin_date"] = None

                row["person_info"] = pep
                sanctions.append(Sanction(row))
            db.session.add_all(sanctions)

            person_roles = []
            for row in data["person_roles"]:
                if len(row["occupation_begin_date"]) > 0:
                    date = datetime.datetime.strptime(
                        row["occupation_begin_date"], "%Y-%m-%d"
                    )
                    row["begin_day"] = date.day
                    row["begin_month"] = date.month
                    row["begin_year"] = date.year

                if len(row["occupation_end_date"]) > 0:
                    date = datetime.datetime.strptime(
                        row["occupation_end_date"], "%Y-%m-%d"
                    )
                    row["end_day"] = date.day
                    row["end_month"] = date.month
                    row["end_year"] = date.year

                row.pop("occupation_end_date")
                row.pop("occupation_begin_date")
                row["person_info"] = pep
                person_roles.append(PersonRole(row))
            db.session.add_all(person_roles)

            adresses = []
            for row in data["adresses"]:
                row["person_info"] = pep
                adresses.append(Adress(row))
            db.session.add_all(adresses)

            db.session.commit()

        except Exception as e:
            return jsonify({"message": "Failed To Add"})

    return jsonify({"message": "Added Succefully"})

@blueprint.route("/download", methods=["GET"])
def download():
    token = request.args.get("token")
    filename = Pep.get_latest(1)
    if token:
        try:
            payload = jwt.decode(
                jwt=token, key=os.environ["JWT_SECRET_KEY"], algorithms=["HS256"]
            )
            return send_file(
                path_or_file=os.path.join(os.getcwd(), filename), as_attachment=True
            )
        except jwt.exceptions.DecodeError as e:
            abort(
                401, "Failed to decode your token please provide us with the true one"
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            return jsonify(
                {
                    "message": "Your token has been expired. Please contact the sales team"
                }
            )
    return jsonify({"message": "please provide token"})


@blueprint.route("/search", methods=["GET"])
def search():
    fullname = request.args.get("fullname").strip()
    persons = Pep.search(fullname=fullname, limit=5)
    return jsonify(persons)


@blueprint.route("/download-sample")
def download_sample():
    email = request.args.get("email")
    with open("tries.txt", "a") as file:
        file.write(email + "\n")
    return send_file(path_or_file=os.path.join(f"{os.getcwd()}/utils", "sample.csv"))


@blueprint.route("images/<filename>", methods=["GET"])
def download_image(filename):
    return send_file(path_or_file=os.path.join(UPLOAD_DIR, filename))


@blueprint.route("/upload-image", methods=["POST"])
def upload_image():
    file = request.files.get("file")
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(filepath)
    return jsonify({"url": MEDIA_URL + file.filename})


######## static pages #########


@blueprint.route("/")
def index():
    return render_template("home/index.html", default_token=os.getenv("DEFAULT_TOKEN"))


@blueprint.route("/v1", methods=["GET"])
def documentation():
    return render_template("home/documentation.html")


@blueprint.route("/pricing", methods=["GET"])
def fetch_pricing():
    return render_template("home/pricing.html")


@blueprint.route("/pricing/check", methods=["GET"])
def fecth_checkapi():
    return render_template("pricing/ApiCheck.html")


@blueprint.route("/about", methods=["GET"])
def fetch_about():
    return render_template("home/about.html")


@blueprint.route("/sources/criminal-sources", methods=["GET"])
def get_criminal_sources():
    return render_template("/sources/criminal.html")


@blueprint.route("/sources/pep-sources", methods=["GET"])
def get_pep_sources():
    return render_template("/sources/pep.html")


@blueprint.route("/sources/sanction-sources", methods=["GET"])
def get_sanctions_sources():
    return render_template("/sources/sanction.html")


@blueprint.route("/sources/additional-sources", methods=["GET"])
def get_additional_sources():
    return render_template("/sources/additional.html")
