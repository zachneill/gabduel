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
    $.ajax( "/delete", {
        method: "POST",
        data: { postId: postId },
        success: function() {
            location.reload()
        },
        error: function(error) {
            console.log(error["responseText"]);
        }
    });
}