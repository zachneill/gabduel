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
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function (err) {
        console.log('ServiceWorker registration failed: ', err);
        });
    });
}
// Support function
function support(authorNumber, postId, authorId) {
    // Gets post id and support id
    let supportId = authorNumber
    let otherAuthorId = supportId === 1 ?
        $("#support_"+postId).data("author2_id") :
        $("#support_"+postId).data("author1_id")
    let mindChanged = false
    // Check if there already is a green border around a previously supported author
    mindChanged = $('#avatar_'+otherAuthorId).hasClass("supported")

    if (!mindChanged && $('#avatar_'+authorId).hasClass("supported")){
        console.log("Already supporting this author")
    } else {
        $.ajax("/post/support", {
            method: "POST",
            data: {
                postId: postId,
                authorNumber: authorNumber,
                supportId: supportId,
                mindChanged: mindChanged
            },
            success: function () {
                // Add a green border around supported author's image
                if (mindChanged) {
                    $("#avatar_"+otherAuthorId).removeClass("supported")
                    $("#avatar_"+otherAuthorId).addClass("opacity-50")

                    $("#avatar_"+authorId).addClass("supported")
                    $("#avatar_"+authorId).removeClass("opacity-50")

                } else {
                    $("#avatar_"+authorId).addClass("supported")
                    $("#avatar_"+otherAuthorId).addClass("opacity-50")
                }
            },
            error: function (error) {
                // Logs error to console if unsuccessful
                console.log(error["responseText"]);
            }
        })
    }
}