# reveal
This porject is a school project that aims at recreating a social media app. Our model is instagram.

For now this project only works in local, even the database.
To launch this project you need to download postgresql and create a .env file with this template: <br> <br>
DB_NAME="postgres" <br>
DB_HOST="localhost" <br>
DB_PASSWORD="enter your password" <br>
DB_PORT="5432" <br>
DB_USER="postgres" <br>
JWT_SECRET="enter another password" <br>

Here are all the dependancy you need to have to launch the project.
All you have to do is run this in your consol: <br>
pip install flask psycopg2-binary bcrypt pyjwt python-dotenv

You also need to create three folder under the static folder: <br>
-uploads <br>
    -images<br>
    -profile_pictures<br>
    -videos<br>
All the media of the application will be stored in these folders. So there will be stored inside the project. In a real project it would have been better to save theme inside a could service.