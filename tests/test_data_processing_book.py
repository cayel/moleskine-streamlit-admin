import unittest
import pandas as pd
import data_processing_book  # Import your module with the function to be tested

class TestDataProcessing(unittest.TestCase):

    def test_display_books_by_year(self):
        # Create a sample DataFrame for testing
        data = {'annee': [2020, 2020, 2021, 2021, 2022],
                'rating': [5, 4, 3, 4, 5],
                'id': [1, 2, 3, 4, 5]}
        df_filtered_books = pd.DataFrame(data)

        # Call the function and check if it raises any errors
        try:
            data_processing_book.display_books_by_year(df_filtered_books)
        except Exception as e:
            self.fail(f"Function raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
