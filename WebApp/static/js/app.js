// // JavaScript for Tab Toggle
// document.getElementById('roomsTab').addEventListener('click', function() {
//     document.getElementById('roomsGrid').classList.remove('hidden');
//     document.getElementById('devicesGrid').classList.add('hidden');
//     this.classList.add('text-blue-500');
//     document.getElementById('devicesTab').classList.remove('text-blue-500');
//     document.getElementById('devicesTab').classList.add('text-gray-500');
// });

// document.getElementById('devicesTab').addEventListener('click', function() {
//     document.getElementById('devicesGrid').classList.remove('hidden');
//     document.getElementById('roomsGrid').classList.add('hidden');
//     this.classList.add('text-blue-500');
//     document.getElementById('roomsTab').classList.remove('text-blue-500');
//     document.getElementById('roomsTab').classList.add('text-gray-500');
// });

// // Function to handle room selection
// function openRoomDetails(roomName) {
//     console.log(`Room selected: ${roomName}`);
//     // Implement the transition to room details here
// }

// Function to add a success alert
function addSuccessAlert(message) {
    var alert = $('<div class="alert alert-success alert-dismissible fade show" role="alert"><div class="container">'
                    + message +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                '</div></div>');
    $('#alert-container').empty();
    $('#alert-container').append(alert);
}

// Function to add an error alert
function addErrorAlert(message) {
    var alert = $('<div class="alert alert-danger alert-dismissible fade show" role="alert"><div class="container">'
                    + message +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                '</div></div>');
    $('#alert-container').empty();
    $('#alert-container').append(alert);
}
