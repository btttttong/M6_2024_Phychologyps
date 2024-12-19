from typing import List, Any
import csv


def read_csv_with_column_filter(
    filename: str, column_name: str, value_to_match: Any
) -> List[List[str]]:
    """
    Read a CSV file and filter rows based on a specific column's value.

    Args:
        filename (str): The path to the CSV file.
        column_name (str): The name of the column to filter.
        value_to_match (Any): The value to match in the specified column.

    Returns:
        List[List[str]]: A list of rows that match the filter criteria.

    Raises:
        ValueError: If the specified column is not found in the CSV file.
    """
    data: List[List[str]] = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        column_index = None
        for i, col in enumerate(header):
            if col == column_name:
                column_index = i
                break
        if column_index is None:
            raise ValueError(f"Column '{column_name}' not found in the CSV file.")

        for row in csv_reader:
            if row[column_index] == value_to_match:
                data.append(row)
    return data
