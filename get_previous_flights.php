<?php
session_start();
require 'db_connect.php'; // include your DB connection

$user_id = $_SESSION['user_id'];

$sql = "SELECT f.id, f.destination, f.departure_date, f.airline 
        FROM flights f
        JOIN bookings b ON b.flight_id = f.id
        WHERE b.user_id = ? AND f.departure_date < NOW()";

$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();

$flights = [];
while ($row = $result->fetch_assoc()) {
    $flights[] = $row;
}

echo json_encode($flights);
?>
