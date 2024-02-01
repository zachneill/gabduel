$(document).ready(function () {
    // Set CSRF token to avoid CSRF error when ajax calling
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("#csrf").val()
        }
    });
});

function deletePost(postId) {
    // Delete post
    $.ajax("/delete", {
        method: "POST",
        data: {
            postId: postId
        },
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
// Search bar function on search page
$('#searchButton').on("click", function () {
    // Gets search query
    let query = $("#searchInput").val()
    if (query !== "") {
        // Redirects to search page
        window.location.href = `/search/${query}`;
    }
});
// Service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register("/sw.js").then(function (registration) {
    }, function (err) {
        console.log('ServiceWorker registration failed: ', err);
        });
    });
}
// Support function
function support(winnerId, loserId, postId) {
    // Check if there already is a green border around a previously supported author
    let mindChanged = $('#avatar_'+loserId).hasClass("supported")

    if (!mindChanged && $('#avatar_'+winnerId).hasClass("supported")){
        console.log("Already supporting this author")
    } else {
        $.ajax("/post/support", {
            method: "POST",
            data: {
                postId: postId,
                winnerId: winnerId,
                mindChanged: mindChanged
            },
            success: function () {
                // Add a green border around supported author's image
                $("#avatar_"+winnerId).addClass("supported")
                $("#avatar_"+winnerId).removeClass("opacity-50")

                $("#avatar_"+loserId).removeClass("supported")
                $("#avatar_"+loserId).addClass("opacity-50")
            },
            error: function (error) {
                // Logs error to console if unsuccessful
                console.log(error["responseText"]);
            }
        })
    }
}