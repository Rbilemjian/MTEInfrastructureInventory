MTE Infrastructure Inventory
-

<br>

<h3>Technologies Used</h3>

<br>

<strong>Back-end / Server-Side Logic</strong>
    
    Python using the Django Framework
    
<strong>Front-end Logic</strong>

    JQuery, Javascript

<strong>Front-end Styling</strong>

    HTML, CSS, Bootstrap

<br>

<h3>Overall Design of the application</h3>

<br>

<strong>Back-end</strong>

Designations of URLs and view functions to be called when they are visited contained in the file:

    urls.py

Definitions for tables and relationships within the database are contained in the file:

    models.py
    
Definitions & logic for forms and auto-fill suggestions for them are defined in the file:
    
    forms.py
    
Logic for view behavior (GET and POST requests) are contained in the files:

    views.py    infoblox_views.py
  
<strong>Front-end</strong>

All HTML files can be found in the folder 

    templates

There is some custom logic that executes within the Django templating system defined in the folder

    templatetags
    
Some custom CSS and Javascript exists in the following files

    styles.css (in static folder)
    script.js (in the bootstrap distribution/js folder)
    
<br>

<h3>App Deployment on CentOS Server</h3>

<br>

<strong>Installing MySQL</strong>

    https://www.tecmint.com/install-latest-mysql-on-rhel-centos-and-fedora/
    
Following installation and securing the MySQL installation as per the linked tutorial, enter into the
MySQL command line and create a database called "mteinfrastructure"

<strong>Installing & using Git</strong>

Install Git with the following command:

    yum install git
    
CD into the home directory and run the command

    git clone https://github.com/Rbilemjian/MTEInfrastructureInventory.git
    
Find the settings.py in the following directory:

    /home/mteinfrastructureinventory/infrastructureinventoryproject/infrastructureinventoryproject
    
Delete the current settings.py file and run the following command to make the production_settings.py the new main settings.py file:

    mv production_settings.py settings.py
    
Additionally, in order to hide debug messages from end users, the following setting should be changed in the settings.py file:

    DEBUG = True --> DEBUG = False
    
    
<strong> Installing Python </strong>

You will want to install Python version 3.4.8 for this application.
A guide to install 3.6 (same thing but use a 4 instead of a 6) can be found at:

    https://dev.to/lechatthecat/how-to-install-python3-in-centos7-1bk6
    
<strong>Installing Virtual Environment, Django, Setting up Apache</strong>

Here is a guide to give an idea of the process (the guide also covers configuring apache):

    https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7
    
If there are problems setting up the virtual environment with that guide, this guide does it slightly differently:

    https://dev.to/lechatthecat/how-to-install-django-in-centos7-vm-2f5i
    
Once the virtual environment is set up, it can be activated with the following command:

    source your-env-name-here/bin/activate

Once that is activated, Django and package requirements can be installed wherever the requirements.txt file is located in the project
directory with the command:

    pip install -r requirements.txt
    
Create a directory called static_root within /home/mteinfrastructureinventory directory and run following command as well
in order to place all the static files for the project where they need to be:

    python manage.py collectstatic
    
Make sure to create a migrations folder in the following directory if it does not already exist and create an empty file called "\__init\__.py" within it:

    /home/mteinfrastructure/infrastructureinventoryproject/infrastructureinventoryapp
    
Then you can run the following commands in the same directory as the manage.py file:

    python manage.py makemigrations
    python manage.py migrate
    
You can create a superuser with the following command: 

    python manage.py createsuperuser
    
That user can then log into the admin panel and add other users who will then be able to log into the application using their guardhouse credentials

You will have to place the django.conf file from the repository in the following directory for the Apache server to work:

    /etc/httpd/conf.d/(django.conf goes here [within conf.d])
    
Refer to the second guide under the "Installing Python" header in order to see how Apache should be configured in a general sense.
After configuration, the following command should be run in order to start the Apache server:

    systemctl start httpd
    
And in order to restart the server:

    systemctl restart httpd
    
And to stop the server completely:

    systemctl stop httpd
    
In order to start apache automatically at boot of VM:

    systemctl enable httpd

<br>

<h3>Modifying the Application</h3>

<br>

<strong>Updating Infoblox Credentials</strong>

If the credentials for Infoblox need to be updated, this can be done by updating the assignment of the infobloxCredentials to be the new username and password in the format (username, password) 
in the following file (should be ~ line 583): 

    infoblox_views.py
    
    
<strong>Changing Import Timeout Duration (Currently 5 minutes)</strong>
    
If the time-out needs to be changed, it can be modified by changing the comparison of "diff", which is currently diff<5, to be diff<x where x is the desired timeout period. 
This change should be done in the same file as the credential change above (should be ~ line 554):

    infoblox_views.py
    
<strong>Adding New Users</strong>

Adding users should be done through a superuser/staff account using the admin panel. This can be done by going to the url of the deployed site like the following example in the case that it is hosted through an IP:

    100.115.100.116/admin
    
After authenticating to enter the admin interface, a user can be added by entering their SSO into the "Add User" form and entering a dummy password 
(authentication is done through guardhouse with SSO & NBCU password so the dummy password entered will not actually be used).
In order for that user to have permissions to import/delete records, the checkbox to make them a staff user should be checked right after creation.

In the case that it is a fresh instance of the project with no users, the following command should be run:

    python manage.py createsuperuser
    
That superuser should be set to have the SSO of the person who it will represent it as its username, and a dummy password which doesn't matter because as mentioned above, the authentication is done through guardhouse.
The email prompt when creating the superuser can simply be left blank.
Note that this command can only be run if the python virtual environment has been set up correctly, but if a new installation of the application has been set up that should be the case.

<strong>In the Case of Trouble with Lock Mechanism</strong>

If a user is conducting an import from infoblox, they cannot update authoritative zones in another tab without encountering a server error. This is because a user can only hold one lock at once, 
and the infoblox import lock is a different type of lock than the authoritative zone update lock. The issue should be cleared up if the user completes the import and re-attempts to update the authoritative zones.
    
<strong>What to do After Making Modifications</strong>

Run the following command to restart Apache server (unneeded if all that's been changed is the addition of new users):

    systemctl restart httpd
    


    
    

    

    


