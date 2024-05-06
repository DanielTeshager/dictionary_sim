# Dictionary Application

This project is a web-based Dictionary application built using Flask, a Python web framework. The application allows users to store, retrieve, and delete key-value pairs, simulating the functionality of a dictionary data structure.
Through an interactive and visual approach, this application provides a hands-on experience for understanding the inner workings of hash tables. It offers a graphical representation of how key-value pairs are efficiently stored, retrieved, and deleted, showcasing the concepts of hash functions, memory references, and collision resolution techniques.

## Features

- Store key-value pairs: Users can submit keys and their corresponding values to be stored in the dictionary.
- Retrieve values: Users can perform lookup operations by entering a key and retrieving its associated value.
- Delete keys: Users can remove a key-value pair from the dictionary by specifying the key.
- Visual representation: The application provides a visual representation of the dictionary's internal structure, including hash values, memory references, and key-value mappings.

## Technologies Used

- Flask: Python web framework for building the application backend
- HTML/CSS: Frontend markup and styling
- JavaScript: Client-side interactivity and AJAX requests
- jQuery: JavaScript library for simplified DOM manipulation and event handling
- Selenium: Browser automation tool for integration testing
- Python: Programming language used for the backend and testing

## Getting Started

### Prerequisites

- Python (version 3.x)
- Flask (Python package)
- Web browser (Chrome, Firefox)

### Installation

1. Clone the project repository:
   `git clone https://github.com/DanielTeshager/dictionary_sim.git`
2. Navigate to the project directory:
   `cd dictionary_sim`
3. Install the required Python packages:
   `pip install -r requiremnts.txt`

### Usage

1. Start the Flask development server:
   `python app.py`
2. Open a web browser and visit `http://localhost:5000` to access the application.

3. Use the provided interface to interact with the dictionary:

- Enter a key-value pair in the input field (e.g., `apple:fruit`) and click the "Insert" button to store the pair.
- Enter a key in the input field and click the "Lookup" button to retrieve the associated value.
- Enter a key in the input field and click the "Delete" button to remove the key-value pair from the dictionary.

4. Observe the visual representation of the dictionary's internal structure, including hash values, memory references, and key-value mappings.

## Testing

The project includes integration tests to verify the functionality of the Dictionary application. The tests are written using the Selenium WebDriver and Python's unittest framework.

To run the tests:

`python test_integration.py`
The test results will be displayed in the console, indicating the success or failure of each test case.

## Contributing

Contributions to the Dictionary application project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the project repository.

## License

This project is licensed under the [MIT License](LICENSE).
