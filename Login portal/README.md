This is a school project in which I created a mock website where you can log in an existing user, register a new one, log out and so on.
The website in itself is completely useless, but is connected to a server and database with encrypted (hashed and salted) passwords.
This means it is very safe to use, and uses database technology and SQL to process and store data. 

The website greets the logged on username upon login. If the user tries to access a not found URL they are redirected to the login page.
If they are logged in and try to visit another page except the profile page, they are redirected to the profile page. If several
sessions are registered for the same user, the user is presented with the opportunity to log out all other sessions. If the user is
idle for more than 10 seconds (no mouse movement, clicks, etc) the user is logged out.
