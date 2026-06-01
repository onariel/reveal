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

You also need to create three folder under the static folder, like this architecture: <br>
static <br>
 └──uploads <br>
   ├──images<br>
   ├──avatars<br>
   └──videos<br>
All the media of the application will be stored in these folders. So there will be stored inside the project. In a real project it would have been better to save theme inside a could service.<br>

Features <br>
Done  <br>

User authentication — Register with username + email + password. Login sets an HTTP-only JWT cookie. Logout deletes the cookie. Passwords are hashed with bcrypt before storage. The login form accepts either email or username. <br>
User profiles — View any user's profile showing their post grid, post count, follower count, and following count. Click followers or following to open a modal list. <br>
Post publishing — Upload a photo or video with an optional caption. Posts can be edited (caption only) or deleted by their owner. <br>
Feed — The home page shows posts ordered by newest first. Designed with a slot for a ranking algorithm to be dropped in later. <br>
Likes — Click the heart icon to like or unlike a post. The count updates instantly without a page reload. <br>
Hierarchical comments — Comments support unlimited nesting through comment_parent_id. The build_comment_tree() service converts the flat database rows into a proper tree structure that the frontend renders with indented replies. <br>
Follow / Unfollow — Follow or unfollow users from their profile, from posts in the feed, or from the suggestions widget. The button updates instantly without a page reload. <br>
Follow recommendations — The right sidebar suggests users to follow, scored using Jaccard similarity on follow graphs plus a follower count boost. <br>
Notifications — Notifications are created automatically when someone likes your post, comments on your post, or follows you. Unread notifications show a gold dot and a red badge counter in the nav. <br>
Search — Search for users and posts from the search page. <br>
Responsive UI — Three-column layout on desktop collapses to a single feed column on mobile. <br>

In Progress <br>

Feed ranking algorithm — The slot in get_feed_post_ids() is ready. The plan is to score posts using likes, comments, time decay, and whether the author is followed. <br>
BFS trend analysis — Breadth-first search over the follow graph to surface posts that are trending within a user's social circle. <br>
Content recommendations — Recommend posts from users the current user does not yet follow, based on what people in their network are engaging with. <br>
Recommendation reasons — Show a short explanation under each recommended post ("Because @alice liked this" or "Trending in your network"). <br>
