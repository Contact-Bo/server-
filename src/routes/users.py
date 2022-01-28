from flask import Blueprint, jsonify, request, current_app
from util.database import Database
from util.response import create_error_response
import re
import bcrypt


users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/register", methods=["POST"])
@Database.with_connection
def register(**kwargs):
    cursor = kwargs["cursor"]
    connection = kwargs["connection"]

    try:
        # Takes incoming data as json
        incoming_data = request.get_json()

        firsname_ = incoming_data["firstname"]
        lastname_ = incoming_data["lastname"]
        email_ = incoming_data["email"]
        password_ = incoming_data["password"]
        comfirm_Pwrd = incoming_data["comfirm_pass"]

        # If variables were inserted then proceed
        if firsname_ and lastname_ and email_ and password_:
            if password_ != comfirm_Pwrd:
                return create_error_response("Passwords do not match!", 409)

            hashed_Password = bcrypt.hashpw(password_.encode("utf-8"), bcrypt.gensalt())

            # sql query to check if Email exists already
            cursor.execute("SELECT * FROM users WHERE email = %s", (email_,))
            exist_acc = cursor.fetchone()

            # Check to see if account exist already or not
            if exist_acc:
                return create_error_response("Account already exists!", 404)
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email_):
                return create_error_response("Invalid email address!", 404)
            else:
                sql_Query = """
                  INSERT INTO users(firstname, lastname, email, password)
                  VALUES(%s, %s, %s, %s)
                """
                data = (
                    firsname_,
                    lastname_,
                    email_,
                    hashed_Password,
                )
                cursor.execute(sql_Query, data)
                connection.commit()

                return jsonify({"message": "New account created"})

        else:
            return create_error_response("Please enter the required fields!", 409)

    except Exception as err:
        print(err)
        return create_error_response("Error", 500)
