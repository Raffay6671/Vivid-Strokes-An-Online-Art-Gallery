Vivid Strokes Exhibit
Overview
Vivid Strokes Exhibit is an online art gallery platform designed to showcase a diverse collection of art pieces across various categories including Paintings, Drawings, Abstract Art, and Digital Art. The application allows users to browse through the gallery, add art pieces to their cart, and make purchases. It also features an admin dashboard for inventory management.

Features
User Authentication: Supports user signup, login, and session management.
Art Gallery: Users can view different categories of art.
Shopping Cart: Users can add items to their cart and view them before purchasing.
Admin Dashboard: Admins can login to view and manage the inventory, including updating item counts and checking which items are out of stock.
Technologies Used
Flask: A micro web framework written in Python used for backend development.
MongoDB: A NoSQL database used to store user and product data.
HTML/CSS: Used for creating and styling web pages.
JavaScript: Enhances interactivity on client side.
Installation
To set up the project locally, follow these steps:

Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/vivid-strokes-exhibit.git
cd vivid-strokes-exhibit
Set up a virtual environment (Optional but recommended):
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install required packages:
bash
Copy code
pip install -r requirements.txt
Set up your MongoDB database:
Ensure MongoDB is installed and running on your machine.
Create a database named vividstrokes and import the initial data if provided.
Environment Variables:
Create a .env file in the root directory.
Add MONGO_URI, FLASK_APP, and FLASK_ENV configurations.
Example:
makefile
Copy code
MONGO_URI="mongodb://localhost:27017/vividstrokes"
FLASK_APP=app.py
FLASK_ENV=development
Run the application:
bash
Copy code
flask run
Usage
After installation, you can access:

Home page: http://localhost:5000/
Admin Dashboard: Navigate to http://localhost:5000/admin/login and use the admin credentials to access.
Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

Please ensure to update tests as appropriate.

License
MIT
