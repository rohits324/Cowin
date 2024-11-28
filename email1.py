import requests

def send_simple_message(email_id,name, pincode):
    	
		text = "Hi "+ name + ","+ "\n" + "\n" + "Your vaccination slot is availiable in your area ("+pincode + ")." + "\n" + "Please register on https://www.cowin.gov.in/home to get vaccinated." + "\n" + "Stay Safe!" + "\n" + "\n" + "Regards," + "\n" + "CowinInfo Team"
		return requests.post(
		"https://api.mailgun.net/v3/cowininfo.com/messages",
		auth=("api", "556d61b8ac61913705eae4664aa877ad-602cc1bf-4a261731"),
		data={"from": "COWIN Information <info@cowininfo.com>",
			"to": [email_id],
			"subject": "Vaccination slots are available",
			"text": text})

def welcome_message(email_id, name):
    	
		text = "Hi "+ name + ","+ "\n" + "\n" + "We will notify you, when vaccine slots are availiable in your area." + "\n" + "Stay safe." + "\n" + "\n" + "Regards," + "\n" + "CowinInfo Team"
		return requests.post(
		"https://api.mailgun.net/v3/cowininfo.com/messages",
		auth=("api", "556d61b8ac61913705eae4664aa877ad-602cc1bf-4a261731"),
		data={"from": "COWIN Information <info@cowininfo.com>",
			"to": [email_id],
			"subject": "Welcome to CowinInfo",
			"text": text})


