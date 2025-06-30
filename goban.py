import enum
from typing import List


class Status(enum.Enum):
    """
    Enum representing the Status of a position on a goban
    """

    WHITE = 1
    BLACK = 2
    EMPTY = 3
    OUT = 4


class Goban:
    def __init__(self, goban: List[str]) -> None:
        self.goban = goban

    def get_status(self, x: int, y: int) -> Status:
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if (
                not self.goban
                or x < 0
                or y < 0
                or y >= len(self.goban)
                or x >= len(self.goban[0])
        ):
            return Status.OUT
        elif self.goban[y][x] == ".":
            return Status.EMPTY
        elif self.goban[y][x] == "o":
            return Status.WHITE
        elif self.goban[y][x] == "#":
            return Status.BLACK
        raise ValueError(f"Unknown goban value {self.goban[y][x]}")

    """
    Check if a position has at least one liberty
        Args:
        x: the x coordinate
        y: the y coordinate

    Returns:
        a Boolean
    """

    def _is_free(self, x, y, previous_positions=None, color=None):
        # Init
        # Assert we are testing a player position: should be either white or black.
        if color is None:
            color = self.get_status(x, y)
            if color not in [Status.BLACK, Status.WHITE]:
                raise ValueError("The position does not belong to any player."
                                 "Please check only positions which are white or black.")

        # Keep all tested positions in memory to avoid testing twice the same position
        if previous_positions is None:
            previous_positions = []

        # Check if there is a freedom next to the current position
        freedom = self.get_status(x - 1, y) == Status.EMPTY \
                  or self.get_status(x + 1, y) == Status.EMPTY \
                  or self.get_status(x, y - 1) == Status.EMPTY \
                  or self.get_status(x, y + 1) == Status.EMPTY
        if freedom:
            # There is at least one freedom, so the position is free. Stop there.
            return True
        else:
            # Test adjacent connections of the same color until we find freedom
            positions_to_check = []
            # 4 positions can be potentially checked
            for position in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                # But already tested positions should not be included in the following check...
                if position not in previous_positions:
                    x, y = position
                    # ... and we have to test only the current player color.
                    if self.get_status(x, y) is color:
                        positions_to_check.append(position)
                        previous_positions.append(position)
            # Now, we check the positions we previously included
            for position in positions_to_check:
                x, y = position
                return self._is_free(x, y, previous_positions, color)

            # If no freedom has been found: the position is definitely taken
            return False

    """
    Check if a position has at least one liberty, otherwise it's taken.
        Args:
        x: the x coordinate
        y: the y coordinate

    Returns:
        a Boolean
    """

    def is_taken(self, x: int, y: int) -> bool:
        return not self._is_free(x, y)
