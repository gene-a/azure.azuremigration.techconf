import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger received notification with id: %s',notification_id)

    POSTGRES_URL="techconf-postgres-db.postgres.database.azure.com"
    POSTGRES_USER="techconfadmin@techconf-postgres-db"
    POSTGRES_PW="P@ssword"
    POSTGRES_DB="techconfdb" 
    SENDGRID_API_KEY = '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'

    logging.info("getting connection to db")
    conn = psycopg2.connect(
                    host=POSTGRES_URL,
                    database=POSTGRES_DB,
                    user=POSTGRES_USER,
                    password=POSTGRES_PW)

    try:
        cursor = conn.cursor()
        
        logging.info("Get notification message and subject from database using the notification_id")
        cursor.execute("""SELECT id, subject
                            FROM notification where id = %s;""", (notification_id,))
        notification = cursor.fetchone()

        logging.info("Get attendees email and name")
        cursor.execute("""SELECT id, first_name, last_name, email FROM attendee;""")
        attendees = cursor.fetchall()

        logging.info("Loop through each attendee and send an email with a personalized subject")
        logging.info(attendees)
        for attendee in attendees:
            attendee_id = attendee[0]
            name = attendee[1]
            lastName = attendee[2]
            email = attendee[3]

            sourceEmail = 'fortylinespermethod@gmail.com'
            logging.info('mailing: attendee {0} ({1})'.format(attendee_id, email))
            subject = '{0} {1}, a personal notification for you. {2}'.format(name, lastName, notification[1])

            message = Mail(
                from_email=sourceEmail,
                to_emails=email,
                subject=subject,
                html_content='<strong>This is a notification you subscribed to from notification ID: {0}</strong>'.format(notification_id)
            )
           
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            logging.info(response.status_code)
            logging.info(response.body)
            logging.info(response.headers)
        
        logging.info("Update the notification table by setting the completed date and updating the status with the total number of attendees notified")
        cursor.execute("""UPDATE notification
                            SET status=%s, completed_date=%s
                            WHERE id = %s;""", 
                            ('Notified {0}'.format(len(attendees)), datetime.now(), notification_id,))
        conn.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        logging.warn("error occured")
        logging.error(error)
    finally:
        logging.info("closing db connection")
        conn.close()
