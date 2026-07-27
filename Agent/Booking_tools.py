from agno.tools import Toolkit
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="railway",
    )


class RailwayTools(Toolkit):
    def __init__(self):
        super().__init__(
            name="railway_tools",
            tools=[
                self.book_ticket,
                self.view_bookings,
                self.cancel_booking,
                self.view_timetable,
            ],
        )

    # ==========================================================
    # BOOK TICKET
    # ==========================================================

    def book_ticket(
        self,
        name: str,
        age: int,
        gender: str,
        train_id: int,
        travel_date: str,
    ) -> str:
        """
        Book a railway ticket.

        Args:
            name: Passenger name
            age: Passenger age
            gender: Passenger gender
            train_id: Train ID
            travel_date: Travel date (YYYY-MM-DD)

        Returns:
            Booking confirmation.
        """

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO bookings
            (name, age, gender, train_id, travel_date)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (name, age, gender, train_id, travel_date),
        )

        conn.commit()

        booking_id = cur.lastrowid

        cur.close()
        conn.close()

        return f"Ticket booked successfully.\nBooking ID: {booking_id}"

    # ==========================================================
    # VIEW BOOKINGS
    # ==========================================================

    def view_bookings(self, request: str = "") -> list:
        """
        Return all booked railway tickets.

        Returns:
            List of bookings.
        """

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            """
            SELECT
                b.id,
                b.name,
                b.age,
                b.gender,
                b.travel_date,
                t.name AS train_name,
                t.number
            FROM bookings b
            JOIN trains t
            ON b.train_id=t.id
            """
        )

        bookings = cur.fetchall()

        cur.close()
        conn.close()

        for row in bookings:
            row["travel_date"] = str(row["travel_date"])

        return bookings

    # ==========================================================
    # CANCEL BOOKING
    # ==========================================================

    def cancel_booking(self, booking_id: int) -> str:
        """
        Cancel a railway booking.

        Args:
            booking_id: Booking ID

        Returns:
            Cancellation status.
        """

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM bookings WHERE id=%s",
            (booking_id,),
        )

        conn.commit()

        deleted = cur.rowcount

        cur.close()
        conn.close()

        if deleted == 0:
            return f"No booking found with ID {booking_id}."

        return f"Booking {booking_id} cancelled successfully."

    # ==========================================================
    # VIEW TIMETABLE
    # ==========================================================

    def view_timetable(self, request: str = "") -> list:
        """
        Return all available trains.

        Returns:
            List of trains.
        """

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            """
            SELECT
                id,
                number,
                name,
                departure_time,
                arrival_time,
                days
            FROM trains
            """
        )

        trains = cur.fetchall()

        cur.close()
        conn.close()

        # JSON serializable
        for train in trains:
            train["departure_time"] = str(train["departure_time"])
            train["arrival_time"] = str(train["arrival_time"])

        return trains


if __name__ == "__main__":
    tools = RailwayTools()
    print(tools.view_timetable())