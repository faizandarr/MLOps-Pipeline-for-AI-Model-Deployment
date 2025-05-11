$(document).ready(function() {
    // Toggle between login and signup sections
    $('#showSignup').click(function(e) {
        e.preventDefault();
        $('#loginSection').hide();
        $('#signupSection').show();
    });

    $('#showLogin').click(function(e) {
        e.preventDefault();
        $('#signupSection').hide();
        $('#loginSection').show();
    });

    $('#logoutButton').on('click', function() {
        $.ajax({
            url: 'http://localhost:5000/logout',
            method: 'POST',
            success: function(response) {
                alert(response.message);
                localStorage.removeItem('user_id'); // Clear user ID from local storage
                window.location.href = '/'; // Redirect to login page
            },
            error: function(xhr) {
                var err = xhr.responseJSON ? xhr.responseJSON.error : xhr.responseText;
                alert(`Error: ${err}`);
            }
        });
    });

    // Handle signup form submission
    $('#signupForm').on('submit', function(e) {
        e.preventDefault();
        
        const username = $('#signupUsername').val();
        const password = $('#signupPassword').val();

        $.ajax({
            url: 'http://localhost:5000/signup',
            method: 'POST',
            data: JSON.stringify({ username: username, password: password }),
            dataType: 'json',
            contentType: 'application/json',
            success: function(response) {
                $('#authResult').html(`<div class="alert alert-success">${response.message}</div>`);
                $('#signupSection').hide();
                $('#loginSection').show();
            },
            error: function(xhr) {
                var err = xhr.responseJSON ? xhr.responseJSON.error : xhr.responseText;
                $('#authResult').html(`<div class="alert alert-danger">Error: ${err}</div>`);
            }
        });
    });

    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        
        const username = $('#loginUsername').val();
        const password = $('#loginPassword').val();
    
        $.ajax({
            url: 'http://localhost:5000/login',
            method: 'POST',
            data: JSON.stringify({ username: username, password: password }),
            dataType: 'json',
            contentType: 'application/json',
            success: function(response) {
                $('#authResult').html(`<div class="alert alert-success">${response.message}</div>`);
                localStorage.setItem('user_id', response.user_id); // Store user ID
                window.location.href = '/weather.html'; // Redirect to weather prediction page
            },
            error: function(xhr) {
                var err = xhr.responseJSON ? xhr.responseJSON.error : xhr.responseText;
                $('#authResult').html(`<div class="alert alert-danger">Error: ${err}</div>`);
            }
        });        
    });

    $('#weatherForm').on('submit', function(e) {
        e.preventDefault();
        
        const humidity = parseFloat($('#humidity').val());
        const windSpeed = parseFloat($('#windSpeed').val());
        const user_id = localStorage.getItem('user_id'); // Retrieve user ID

        $.ajax({
            url: 'http://localhost:5000/predict',
            method: 'POST',
            data: JSON.stringify({ humidity: humidity, windSpeed: windSpeed, user_id: user_id }),
            dataType: 'json',
            contentType: 'application/json',
            success: function(response) {
                if (response.error) {
                    $('#predictionResult').html(`<div class="alert alert-danger">${response.error}</div>`);
                } else {
                    $('#predictionResult').html(`
                        <h4>Predicted Temperature:</h4>
                        <p>${response.temperature}°C</p>
                    `);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", status, error);
                console.error("Response:", xhr.responseText);
                var err = xhr.responseJSON ? xhr.responseJSON.error : xhr.responseText;
                $('#predictionResult').html(`<div class="alert alert-danger">Error: ${err}</div>`);
            }
        });
    });
});