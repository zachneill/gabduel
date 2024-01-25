$(document).ready(function () {
    // Set CSRF token to avoid CSRF error when deleting post
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("#delete").data("csrf")
        }
    });
});

function deletePost(postId) {
    // Delete post
    $.ajax("/delete", {
        method: "POST",
        data: {postId: postId},
        success: function () {
            // Reloads page if successful
            location.reload()
        },
        error: function (error) {
            // Logs error to console if unsuccessful
            console.log(error["responseText"]);
        }
    });
}