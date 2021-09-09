# Capstone-ImageToRepair
The project involves 4-5 subsystems that will be integrated by the end of 2021.
Subsystem #1: Image Capture Device
Subsystem #2: Web Application
Subsystem #3: Database
Subsystem #4: Machine Learning
Subsystem #5: 3D Printer
#
#
How the project works:
  The user first takes the image capture device and plugs it into their computer/laptop via USB.
  Then, the user takes image(s) of their broken part, which will be directly uploaded to the web application.
  After the user sees and reviews the image(s) they took displayed on the web application, the web application will send the image(s) to the machine learning model.
  The machine learning model will take those image(s), identify the broken part, and send the name of the broken part back to the web application.
  The web application will then send a request to the database for any files on the broken part.
  The database will look for the broken part's files and send them back to the web application.
  The web application will display these files for the user to see.
  Finally, the web application will send a SECURE REQUEST to a local 3D printer for manufacturing.
