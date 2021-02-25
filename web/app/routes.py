from app import app, db, service_bus_client, queue_name
from datetime import datetime
from app.models import Attendee, Conference, Notification
from flask import render_template, session, request, redirect, url_for, flash, make_response, session
from azure.servicebus import ServiceBusMessage

# from azure.servicebus import Message
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import logging

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        attendee = Attendee()
        attendee.first_name = request.form['first_name']
        attendee.last_name = request.form['last_name']
        attendee.email = request.form['email']
        attendee.job_position = request.form['job_position']
        attendee.company = request.form['company']
        attendee.city = request.form['city']
        attendee.state = request.form['state']
        attendee.interests = request.form['interest']
        attendee.comments = request.form['message']
        attendee.conference_id = app.config.get('CONFERENCE_ID')

        try:
            db.session.add(attendee)
            db.session.commit()
            session['message'] = 'Thank you, {} {}, for registering!'.format(attendee.first_name, attendee.last_name)
            return redirect('/Registration')
        except:
            logging.error('Error occured while saving your information')

    else:
        if 'message' in session:
            message = session['message']
            session.pop('message', None)
            return render_template('registration.html', message=message)
        else:
             return render_template('registration.html')

@app.route('/Attendees')
def attendees():
    attendees = Attendee.query.order_by(Attendee.submitted_date).all()
    return render_template('attendees.html', attendees=attendees)


@app.route('/Notifications')
def notifications():
    notifications = Notification.query.order_by(Notification.id).all()
    logging.info(notifications)
    return render_template('notifications.html', notifications=notifications)

@app.route('/Notification', methods=['POST', 'GET'])
def notification():
    logging.info("entered method")
    if request.method == 'POST':
        notification = Notification()
        notification.message = request.form['message']
        notification.subject = request.form['subject']
        notification.status = 'Notifications submitted'
        notification.submitted_date = datetime.utcnow()

        try:
            db.session.add(notification)
            db.session.commit()
            db.session.flush()
            notification_id = notification.id
            logging.info('processing notification with id: {0}'.format(notification_id))

            with service_bus_client.get_queue_sender(queue_name) as sender:
                single_message = ServiceBusMessage('{0}'.format(notification_id))
                sender.send_messages(single_message)

            # REFACTORED TO FUNCTION APP
            ##################################################
            ## TODO: Refactor This logic into an Azure Function
            ## Code below will be replaced by a message queue
            #################################################
            #attendees = Attendee.query.all()

            # for attendee in attendees:
            #     subject = '{}: {}'.format(attendee.first_name, notification.subject)
            #     send_email(attendee.email, subject, notification.message)

            # notification.completed_date = datetime.utcnow()
            # notification.status = 'Notified {} attendees'.format(len(attendees))
            # db.session.commit()
            # TODO Call servicebus queue_client to enqueue notification ID

            #################################################
            ## END of TODO
            #################################################

            return redirect('/Notifications')
        except Exception as e:
            logging.error(e)
            logging.error(("log unable to save notification %s", datetime.now()))
            return render_template('notification.html')
    else:
        return render_template('notification.html')


# UNUSED, REFACTORED OUT
# def send_email(email, subject, body):
#     api_key = app.config.get('SENDGRID_API_KEY')
#     if not api_key:
#         message = Mail(from_email=app.config.get('ADMIN_EMAIL_ADDRESS'),to_emails=email,subject=subject,plain_text_content=body)
#         sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
#         sg.send(message)
