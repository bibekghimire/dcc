document.addEventListener('DOMContentLoaded', function () {
    // Get the user status from Django context (using data attributes or AJAX)
    var isLoggedIn = document.body.getAttribute('data-is-logged-in') === 'true';
    var isAdmin = document.body.getAttribute('data-is-admin') === 'true';
    
    let timeout;

    function resetTimer() {
        // Clear the existing timeout and set a new one
        clearTimeout(timeout);

        // Set the timer to redirect after 30 seconds of inactivity
        timeout = setTimeout(function() {
            if (isLoggedIn) {
                if (isAdmin) {
                    window.location.href = '/';  // Redirect to admin page
                } else {
                    window.location.href = "/person/";  // Redirect to user page
                }
            } else {
                window.location.href = '/';  // Redirect to home if not logged in
            }
        }, 30000); // 30 seconds of inactivity
    }

    // Listeners for user activity
    document.addEventListener('mousemove', resetTimer);
    document.addEventListener('keypress', resetTimer);
    document.addEventListener('click', resetTimer);
    document.addEventListener('scroll', resetTimer);  // To detect scroll activity
    document.addEventListener('touchstart', resetTimer);  // For touch screens

    // Initialize the timer
    resetTimer();
});