import os
from flask import Flask, request, make_response, render_template, url_for, session
import tweepy

app = Flask(__name__)
app.secret_key = "secret-key"


@app.route('/', methods=["GET"])
def index():
    response = make_response(render_template('index.html'))
    return


@app.route('/follow/<list_id>', methods=["GET", "POST"])
def follow_list(list_id: int):
    """
    Follow a specific list. The GET request returns a form, asking for the user's Twitter username, and sets a cookie
    describing the list they've asked to follow. When this is POSTed, the user is put through the authentication
    process, which returns in the end to /redirect
    :param list_id:
    :return:
    """
    if request.method == "POST":
        pass
        # TODO: redirect to authentication flow
        auth = tweepy.OAuthHandler(os.environ.get('consumer_key'), os.environ.get('consumer_secret'), url_for('redirect'))
        session['request_token'] = auth.request_token
        return redirect(auth.get_authorization_url())
    elif request.method == "GET":
        response = make_response(render_template('follow.html'))
        session['list_id'] = list_id
        return response


@app.route('/redirect')
def redirect():
    if request.cookies.get('list_id', None) is None:
        pass  # return 404
    else:
        request_token = session['request_token']
        del session['request_token']

        auth = tweepy.OAuthHandler(os.environ.get('consumer_key'), os.environ.get('consumer_secret'), url_for('redirect'))
        auth.request_token = request_token
        verifier = request.args.get('oauth_verifier')
        auth.get_access_token(verifier)

        api = tweepy.API(auth)
        user_id = session.get('user_id')
        db_.get_app_db().add_item(user_id)
        db_.get_app_db().update_item(user_id, 'access_token', auth.access_token)
        db_.get_app_db().update_item(user_id, 'access_token_secret', auth.access_token_secret)

        process_queue = queues()[2]
        process_queue.send_message(MessageBody=user_id)

        # enqueue_follows(*get_people_to_follow(api), twitter_api=api)
        # this takes too long - needs to be queued
    list_to_follow = request.cookies.get('list_id')
    # TODO: pass list_to_follow with username


if __name__ == '__main__':
app.run()
