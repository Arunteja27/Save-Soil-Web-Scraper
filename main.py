import json
import os
import os.path
import smtplib
import getpass
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen


curr_path = os.getcwd()
save_path = os.path.join(curr_path, "Letters")
user = input("Enter user: ")
home_country = input("Enter user's home country: ")


def write_to_file(country, email, name, title):
    unacceptable_chars = ['\\', '/', ':', '*', '?', '<', '>', '|']
    Title = title
    for c in title:
        if c in unacceptable_chars:
            Title = title.replace(c, "")

    if email == "":
        return

    for c in email:
        if c in unacceptable_chars:
            return

    completeName = os.path.join(save_path, country + "_del_" + email + "_del_" + name + ".txt");
    with open(completeName, "w", encoding="utf-8") as f:
        f = open(completeName, "w")
        f.write("The Honorable ")
        f.write(Title + " ")
        f.write(name)
        f.write(", \n\n")
        f.write("""A major UN report found that 52% of agricultural soils are degraded. Scientists have warned that we only have 40-50 years worth of agricultural soils remaining. Which means that in 30-35 years, we will reach a “point of no return” for soil. We need an urgent call to action to ensure soil, the lifeline on this planet, continues to benefit present & future generations.
        
The Save Soil movement, launched by global leader Sadhguru, was presented at the 15th session of the Conference of Parties (COP15) to the United Nations Convention to Combat Desertification (UNCCD). Sadhguru addressed 197 Parties at Cote d'Ivoire with one overarching objective - ensuring a minimum of 3-6% organic content in agricultural soil through a three-pronged strategy below:
    
    1. An appropriately phased program of providing inspiration, and incentives to farmers.
    
    2. Simplifying the process by which farmers can take advantage of carbon credits.
    
    3. Develop a special label for foods grown from soil with the target levels of organic content and promote the health benefits of these foods.
    
Sadhguru has spent the last 24 years leading a global people’s movement to save the world’s soil. His Conscious Planet: Save Soil movement aims to turn the world’s attention to soil; encourage around 4 billion people, or 60% of the global electorate, to push for soil-healthy policies; and ensure that soil has an organic content of three to six percent.

With the development of appropriate Government policies, we can turn the clock back on the impending extinction of soil. To facilitate this, the Save Soil movement is creating a handbook of recommendations for every one of the 193 countries. See http://Savesoil.org/Handbook

I request you to enact policies to increase the organic content of our country’s soil to minimum 3-6%. This is an opportunity to save our soil from the brink of extinction.

Thank you for your support.\n\n""")
        f.write(user + "\n")
        f.write("A Voice to Save Soil from " + home_country)
        f.close()

    return


#Open the URL
url = "https://consciousplanet.org/letters"
page = urlopen(url)

#Read in the HTML data and convert it into a string
html_bytes = page.read()
html_page = html_bytes.decode("utf-8")

#Splice this string to only get each country's information
first_object_index = html_page.find('[{"countryName":"Albania"')
ending_index = html_page.find('"_common"') -1
countries_data = html_page[first_object_index:ending_index]

#Convert this spliced string into a JSON object
countries_as_json = json.loads(countries_data)

for country in countries_as_json:
    for person in country['contactInformation']:
        write_to_file(country['countryName'], person['contactEmail'], person['name'], person['title'])



# Setup port number and server name
smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email lists
email_from = input("Enter the sender's email: ")

# Define the password (better to reference externally)
pswd = input("Enter App Password: ")

# name the email subject
subject = "Sadhguru Presents Save Soil at UNCCD COP 15"


# Define the email function (dont call it email!)
def send_emails(person, body, TIE_server):

    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = person
    msg['Subject'] = subject

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    # Cast as string
    text = msg.as_string()

    print(f"Sending email to: {person}...")
    TIE_server.sendmail(email_from, person, text)
    print(f"Email sent to: {person}")
    print()

# Connect with the server
print("Connecting to server...")
TIE_server = smtplib.SMTP(smtp_server, smtp_port)
TIE_server.ehlo()
TIE_server.starttls()
TIE_server.ehlo()
TIE_server.login(email_from, pswd)
print("Succesfully connected to server")
print()

i = 0
files = os.listdir(save_path)
for f in files:
    if(i % 50 == 0 and i != 0):
        time.sleep(180)
    first = f.find('_del_')
    last = f.find('_del_', first+1)
    email = f[first+5:last]
    with open(os.path.join(save_path, f)) as fileCurr:
        content = fileCurr.read()
        # Run the function
        send_emails(email, content, TIE_server)
    i+=1

# Close the port
TIE_server.quit()





