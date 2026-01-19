from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List

from acbrightspace.fraction import Fraction

type Cell = str | List[str] | Fraction | None
"""A cell can be a string, a list of strings, a Fraction, or None."""

@dataclass
class Row:
    """Represents a row in a Brightspace table."""

    cells: List[Cell]
    """List of cells in the row."""

    element: WebElement
    """The original WebElement representing the row."""

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

        # If cell is empty, return None
        if not cell_texts:
            return None

        # Attempt to parse as Fraction
        try:
            return Fraction.from_string(cell.text)
        except ValueError:
            pass
        
        # Return single string if only one line
        if len(cell_texts) == 1:
            # If the string is "- / -", return None
            if cell_texts[0] == "- / -":
                return None
            return cell_texts[0]
        
        # Otherwise, return list of strings
        return cell_texts
    
    def parse_row(self, row: WebElement) -> Row | None:
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
            if self._category is not None:
                cells = cells[1:]
            for cell in cells:
                parsed_cells.append(self.parse_cell(cell))

            return Row(parsed_cells, row)
        return None

    def parse(self, table: WebElement) -> List[Row]:
        """Parses an entire table into a list of rows and cells.

        Args:
            table (WebElement): The WebElement representing the table.

        Returns:
            List[Row]: A list of Row objects representing the parsed rows.
        """
    
        rows = table.find_elements(By.TAG_NAME, "tr")
        parsed_rows = []
        # Skip header row
        for row in rows[1:]:  
            parsed_row = self.parse_row(row)
            if parsed_row:  # Only add non-empty rows
                parsed_rows.append(parsed_row)

        return parsed_rows