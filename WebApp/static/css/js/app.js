// JavaScript for Tab Toggle
document.getElementById('roomsTab').addEventListener('click', function() {
    document.getElementById('roomsGrid').classList.remove('hidden');
    document.getElementById('devicesGrid').classList.add('hidden');
    this.classList.add('text-blue-500');
    document.getElementById('devicesTab').classList.remove('text-blue-500');
    document.getElementById('devicesTab').classList.add('text-gray-500');
});

document.getElementById('devicesTab').addEventListener('click', function() {
    document.getElementById('devicesGrid').classList.remove('hidden');
    document.getElementById('roomsGrid').classList.add('hidden');
    this.classList.add('text-blue-500');
    document.getElementById('roomsTab').classList.remove('text-blue-500');
    document.getElementById('roomsTab').classList.add('text-gray-500');
});

// Function to handle room selection
function openRoomDetails(roomName) {
    console.log(`Room selected: ${roomName}`);
    // Implement the transition to room details here
}
