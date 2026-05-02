# reveal
This porject is a school project that aims at recreating a social media app. Our model is instagram.

For now this project only works in local, even the database.
To launch this project you need to download postgresql and create a .env file with this template:

DB_NAME="postgres"

DB_HOST="localhost"

DB_PASSWORD="enter your password"

DB_PORT="5432"

DB_USER="postgres"

JWT_SECRET="enter another password"

Here are all the dependancy you need to have to launch the project.
All you have to do is run this in your consol:
pip install flask psycopg2-binary bcrypt pyjwt python-dotenv