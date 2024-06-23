import mysql.connector
from PIL import Image
from io import BytesIO

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="divyanshu@@!Sql1",
    database="foodpurchasinghistory"
)

# Check if the connection was successful
if connection.is_connected():
    print("Connected to the database")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    try:
        # Execute a SQL query to fetch the image data
        cursor.execute("SELECT image FROM image_table WHERE id = 1")

        # Fetch the result (image data)
        result = cursor.fetchone()

        # Process the result (in this case, save the image as a PNG file)
        image_data = result[0]
        # Open the image using Pillow
        image = Image.open(BytesIO(image_data))
        # Save the image as a PNG file
        save_path = r"C:\Users\ASUS\Desktop\image.png"
        image.save(save_path, format="PNG")
        print("Image saved as image.png")

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Connection closed")
