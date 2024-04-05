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
    var alert = $(`
        <div class="toast align-items-center text-bg-success border-0 w-75" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `);
    $('#alert-container').empty();
    $('#alert-container').append(alert);
    $(".toast").toast('show');
}

// Function to add an error alert
function addErrorAlert(message) {
    var alert = $(`
        <div class="toast align-items-center text-bg-danger border-0 w-75" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `);
    $('#alert-container').empty();
    $('#alert-container').append(alert);
    $(".toast").toast('show');
}


var socket = io();
socket.on("connect", (msg) => {
});
socket.on("error", (err) => {
    addErrorAlert("Could not connect to the web server.");
    console.error(err);
})