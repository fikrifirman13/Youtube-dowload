document.getElementById('download-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var playlistUrl = document.getElementById('playlist_url').value;
    var socket = io();
    var progressDiv = document.getElementById('progress');
    var alertSound = document.getElementById('alert-sound');
    progressDiv.innerHTML = ''; // Clear previous progress messages

    socket.emit('start_download', playlistUrl);
    socket.on('update', function(msg) {
        var message = document.createElement('p');
        message.textContent = msg;
        progressDiv.appendChild(message);
    });

    socket.on('finished', function() {
        var message = document.createElement('p');
        message.textContent = 'Proses download dan konversi selesai!';
        progressDiv.appendChild(message);
        alertSound.play(); // Play the alert sound

        // Tambahkan kalimat setelah suara notifikasi selesai dimainkan
        alertSound.onended = function() {
            var finishedMessage = document.createElement('p');
            finishedMessage.textContent = 'Semua lagu telah berhasil didownload dan dikonversi!';
            progressDiv.appendChild(finishedMessage);
        };
    });
});
