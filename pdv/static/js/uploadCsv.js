// Add event listener to the div
document.querySelector('.file-upload').addEventListener('click', function() {
    // Trigger a click on the file input
    document.getElementById('csv_file').click();
});

// Show the manual form by default
document.getElementById('manual').classList.remove('hidden');
document.getElementById('csv-upload').classList.add('hidden');

document.getElementById('csv-button').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('csv-upload').classList.remove('hidden');
    document.getElementById('manual').classList.add('hidden');
});

document.getElementById('manual-button').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('csv-upload').classList.add('hidden');
    document.getElementById('manual').classList.remove('hidden');
});

document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData();
    formData.append('file', document.getElementById('csv_file').files[0]);

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch('/upload_csv', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(response => response.text())
    .then(data => {
        // Handle the response data here
        console.log(data);
    }).catch(error => {
        // Handle the error here
        console.error(error);
    });
});