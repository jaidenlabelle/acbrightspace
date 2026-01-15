from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List

from acbrightspace.fraction import Fraction

type Cell = str | List[str] | Fraction
"""A cell can be a string, a list of strings, or a Fraction."""

class Table:
    """A class for parsing Brightspace tables."""

    def __init__(self) -> None:
        self._category: str | None = None
    
    def parse_cell(self, cell: WebElement) -> Cell:
        """Parses a table cell into a Cell type.

        Args:
            cell (WebElement): The WebElement representing the table cell.
        
        Returns:
            Cell: The parsed cell content.
        """
        # Split cell text into lines and strip whitespace
        cell_texts = [line.strip() for line in cell.text.splitlines() if line.strip()]

        # Attempt to parse as Fraction
        try:
            return Fraction.from_string(cell.text)
        except ValueError:
            pass
        
        # Return single string if only one line
        if len(cell_texts) == 1:
            return cell_texts[0]
        
        # Otherwise, return list of strings
        return cell_texts
    
    def parse_row(self, row: WebElement) -> List[Cell] | None:
        """Parses a table row into a list of Cells.

        Args:
            row (WebElement): The WebElement representing the table row.
        
        Returns:
            List[Cell] | None: A list of parsed cells in the row, or None if the row is a category header.
        """
        cells = row.find_elements(By.XPATH, ".//td | .//th")

        # Check if first cell is a category header
        if cells and cells[0].get_attribute("scope") == "row"  and cells[0].get_attribute("colspan") == "2":        
            self._category = cells[0].text.strip()
        else:            
            parsed_cells: List[Cell] = []

            # Skip first cell if it's a category header, because it's a white space cell
            for cell in cells[1:]:
                parsed_cells.append(self.parse_cell(cell))

            return parsed_cells
        return None

    def parse(self, table: WebElement) -> List[List[Cell]]:
        """Parses an entire table into a list of rows and cells.

        Args:
            table (WebElement): The WebElement representing the table.

        Returns:
            List[List[Cell]]: A list of rows, each containing a list of parsed cells.
        """
    
        rows = table.find_elements(By.TAG_NAME, "tr")
        parsed_rows = []
        # Skip header row
        for row in rows[1:]:  
            parsed_row = self.parse_row(row)
            if parsed_row:  # Only add non-empty rows
                parsed_rows.append(parsed_row)

        return parsed_rows