import os
from flask import Flask, request, make_response, render_template, session, abort
from flask import redirect as flask_redirect
import tweepy
from process_interface import ProcessInterfaceFactory, Interfaces
import secrets

BACKEND = Interfaces[os.environ.get("QUEUE_TOOL")]
TWITTER_CALLBACK_URL = os.environ.get("CALLBACK_URL", "http://127.0.0.1:5000/redirect")

app = Flask(__name__)
app.secret_key = secrets.token_bytes(24)
app.queue_interface = ProcessInterfaceFactory.create_interface(BACKEND)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/follow/<list_id>", methods=["GET", "POST"])
def follow_list(list_id: int):
    """
    Follow a specific list. The GET request returns a form, asking for the user's Twitter username, and sets a cookie
    describing the list they've asked to follow. When this is POSTed, the user is put through the authentication
    process, which returns in the end to /redirect
    :param list_id:
    :return:
    """
    if request.method == "POST":
        session["user_id"] = request.form.get("twitter-username")
        auth = tweepy.OAuthHandler(
            os.environ.get("CONSUMER_KEY"),
            os.environ.get("CONSUMER_SECRET"),
            callback=TWITTER_CALLBACK_URL,
        )
        auth_url = auth.get_authorization_url()
        session["request_token"] = auth.request_token.get("oauth_token", None)
        return flask_redirect(location=auth_url)
    elif request.method == "GET":
        response = make_response(render_template("follow-list.html"))
        session["list_id"] = list_id
        return response


@app.route("/redirect")
def redirect():
    if session.get("list_id", None) is None:
        abort(404)  # return 404
    else:
        request_token = session["request_token"]
        del session["request_token"]

        auth = tweepy.OAuthHandler(
            os.environ.get("CONSUMER_KEY"),
            os.environ.get("CONSUMER_SECRET"),
            callback=TWITTER_CALLBACK_URL,
        )
        verifier = request.args.get("oauth_verifier")

        auth.request_token = {
            "oauth_token": request_token,
            "oauth_token_secret": verifier,
        }
        auth.get_access_token(verifier)

        app.queue_interface.process(
            session["user_id"],
            session["list_id"],
            auth.access_token,
            auth.access_token_secret,
        )

        return flask_redirect(f"https://twitter.com/i/lists/{session['list_id']}")


if __name__ == "__main__":
    app.run()
