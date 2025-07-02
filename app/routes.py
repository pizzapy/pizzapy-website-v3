from flask import Flask, render_template, request, jsonify, redirect, url_for, g
import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Middleware-like functionality for token handling


@app.before_request
def token_middleware():
    g.token = get_token_from_request(request)


def get_token_from_request(request):
    if 'code' in request.args:
        code = request.args['code']
        token = get_access_token(code)
        if not token:
            return '1dfe48423a8e298af487ffad0b27f22d'  # Default token
    else:
        # Default token if no code is provided
        token = '1dfe48423a8e298af487ffad0b27f22d'
    return token


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/events')
def events():
    group_name = request.args.get('group_name', 'pizzapy-ph')
    return get_upcoming_events(group_name)

# BASE URL SETUP


def get_redirect_uri():
    default_group_name = "pizzapy-ph"
    current_location = request.url

    if current_location.startswith("http://127.0.0.1:8001/"):
        current_location = current_location.replace(
            "http://127.0.0.1:8001/", "https://pizzapy.ph/"
        )

    parsed_url = urlparse(current_location)
    path = parsed_url.path.rstrip("/")
    parts = path.split("/")

    if len(parts) >= 3:
        if len(parts) == 3:  # URL is like /events/upcoming-events
            parts.append(default_group_name)  # Append default group name
        # Join all parts to form the redirect URI
        redirect_uri = "/".join(parts)
        return redirect_uri
    else:
        return None  # Unable to determine redirect URI

# MEETUP TOKEN ACCESS


def get_access_token(code):
    REDIRECT_URI = get_redirect_uri()
    if not REDIRECT_URI:
        return None  # Unable to determine redirect URI

    token_url = "https://secure.meetup.com/oauth2/access"
    payload = {
        "client_id": os.environ.get("MEETUP_CLIENT_ID"),
        "client_secret": os.environ.get("MEETUP_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

# FETCH EVENT VIA QUERY


def fetch_events(query, token, variables):
    url = "https://api.meetup.com/gql"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        url, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        return None

# EXTRACT EVENTS TO RENDER


def extract_events(data, event_timeline):
    return (
        data.get("data", {})
        .get("groupByUrlname", {})
        .get(event_timeline, {})
        .get("edges", [])
    )

# GET ALL UPCOMING EVENTS API


def get_upcoming_events(group_name):
    upcoming_events_query = """
    query ($urlname: String!) {
        groupByUrlname(urlname: $urlname) {
            id,
            upcomingEvents(input: { first: 3 }, sortOrder: ASC){
                count,
                pageInfo {
                    endCursor
                },
                edges {
                    node {
                        id
                        title
                        description
                        eventType
                        images {
                                source
                        }
                        venue {
                            address
                            city
                            postalCode
                        }
                        createdAt
                        dateTime
                        endTime
                        timezone
                        going
                        shortUrl
                        host {
                            name
                            username
                            email
                            memberPhoto {
                                id
                                baseUrl
                                preview
                                source
                            }
                            memberUrl
                            organizedGroupCount
                        }
                    }
                }
            }
        }
    """
    token = g.token  # Use the token from the middleware
    variables = {"urlname": group_name}
    data = fetch_events(upcoming_events_query, token, variables)

    if data:
        events = extract_events(data, "upcomingEvents")
        if events:
            first_event = events[0]["node"]
            other_events = [event["node"] for event in events[1:]]
            return render_template(
                "events.html",
                first_event=first_event,
                other_events=other_events,
                events_json=events,
            )
        else:
            return render_template(
                "events.html",
                error_message="No upcoming events found",
                first_event=None,
                other_events=[],
                events_json="[]",
            )
    else:
        return render_template(
            "events.html",
            error_message="Failed to retrieve events",
            first_event=None,
            other_events=[],
            events_json="[]",
        )


@app.route('/events/<event_timeline>')
@app.route('/events/<event_timeline>/<group_name>')
def event_dispatcher(event_timeline=None, group_name="pizzapy-ph"):
    if event_timeline == "past-events":
        # Placeholder for future implementation
        return render_template("events.html", error_message="Past events not yet implemented")
    elif event_timeline == "upcoming-events":
        return get_upcoming_events(group_name)
    else:
        return render_template("events.html", error_message="Event type not found"), 404


if __name__ == '__main__':
    app.run(debug=True)
